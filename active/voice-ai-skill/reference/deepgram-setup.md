# Deepgram STT Setup Guide

Production-ready patterns for Deepgram Nova-3 streaming speech-to-text, extracted from VozLux telephony voice AI implementation.

## Overview

Deepgram provides real-time streaming transcription with:
- Nova-3 model (latest, most accurate)
- ~150ms typical latency
- Utterance end detection
- Bilingual Spanish/English support
- Enterprise-tier VAD (Voice Activity Detection) for barge-in

## Installation

```bash
pip install deepgram-sdk>=5.0.0
```

## Core Configuration

### STT Provider Config

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class STTProviderConfig:
    """Configuration for Deepgram STT provider."""

    language: str = "en"
    model: str = "nova-3"  # Latest model (nova-2 also available)

    # Streaming settings
    interim_results: bool = True      # Get partial results as user speaks
    punctuate: bool = True            # Auto-add punctuation
    smart_format: bool = True         # Smart formatting (numbers, dates)

    # Utterance detection (CRITICAL for turn-taking)
    utterance_end_ms: int = 1000      # Silence to end utterance
    vad_events: bool = False          # VAD events for Enterprise tier

    # Audio format (Twilio Media Streams default)
    sample_rate: int = 8000
    encoding: str = "mulaw"           # Twilio's format
```

### Language Mappings

```python
# Deepgram language codes
DEEPGRAM_LANGUAGES = {
    "en": "en-US",
    "es": "es-419",      # Latin American Spanish
    "es-MX": "es-419",
}
```

## Provider Implementation

### Complete Streaming STT Provider

```python
from typing import Optional, Any
import logging
import asyncio

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.events import EventType

logger = logging.getLogger(__name__)


class DeepgramSTTProvider:
    """
    Deepgram streaming STT provider using Nova models.

    Features:
    - Real-time streaming transcription
    - Low latency (~150ms typical)
    - Utterance end detection
    - Smart formatting and punctuation
    - Bilingual Spanish/English support
    """

    def __init__(self, api_key: str):
        """
        Initialize Deepgram provider.

        Args:
            api_key: Deepgram API key from environment
        """
        if not api_key:
            raise ValueError(
                "Deepgram API key not configured. "
                "Set DEEPGRAM_API_KEY in .env file."
            )

        self._api_key = api_key
        self._client: Optional[AsyncDeepgramClient] = None
        self._connection: Optional[Any] = None
        self._config: Optional[STTProviderConfig] = None
        self._listen_task: Optional[asyncio.Task] = None
        self._is_connected: bool = False

        # Callbacks
        self._on_transcript = None
        self._on_utterance_end = None
        self._on_speech_started = None

    @property
    def name(self) -> str:
        return "deepgram-nova"

    @property
    def supports_streaming(self) -> bool:
        return True

    def get_latency_estimate_ms(self) -> int:
        """Nova models have ~150ms latency."""
        return 150
```

### Connection Setup

```python
async def connect(self, config: STTProviderConfig) -> None:
    """
    Connect to Deepgram streaming transcription.

    Uses Deepgram SDK v5+ with async context manager.
    """
    if self._is_connected:
        logger.warning("Already connected to Deepgram")
        return

    self._config = config

    try:
        # Initialize async Deepgram client
        self._client = AsyncDeepgramClient(api_key=self._api_key)

        # Get language code
        language = DEEPGRAM_LANGUAGES.get(config.language, config.language)

        # Create WebSocket connection using v1 API
        # SDK v5 uses listen.v1.connect() with parameters
        self._connection = await self._client.listen.v1.connect(
            model=config.model,
            language=language,
            encoding=config.encoding,
            sample_rate=str(config.sample_rate),
        )

        # Register event handlers (v5 SDK uses EventType enum)
        self._connection.on(EventType.OPEN, self._handle_open)
        self._connection.on(EventType.MESSAGE, self._handle_message)
        self._connection.on(EventType.CLOSE, self._handle_close)
        self._connection.on(EventType.ERROR, self._handle_error)

        # Start listening for events in background
        self._listen_task = asyncio.create_task(
            self._connection.start_listening()
        )

        self._is_connected = True
        logger.info(
            f"Connected to Deepgram STT (model={config.model}, "
            f"lang={language}, sample_rate={config.sample_rate})"
        )

    except Exception as e:
        logger.error(f"Deepgram connection failed: {e}")
        await self.disconnect()
        raise ConnectionError(f"Deepgram connection failed: {e}") from e
```

### Audio Streaming

```python
async def send_audio(self, audio: bytes) -> None:
    """
    Send audio chunk for transcription.

    Args:
        audio: Audio data (must match config encoding/sample_rate)
    """
    if not self._is_connected or not self._connection:
        raise RuntimeError("Not connected to Deepgram")

    if not audio:
        return

    try:
        # v5 SDK uses send_media with a typed message
        from deepgram.extensions.types.sockets import ListenV1MediaMessage
        await self._connection.send_media(ListenV1MediaMessage(data=audio))
    except Exception as e:
        logger.error(f"Error sending audio to Deepgram: {e}")
        raise
```

### Event Handling

```python
def _handle_message(self, message: Any) -> None:
    """
    Handle message event from Deepgram.

    In SDK v5, all transcript events come through MESSAGE.
    Check message type and extract data accordingly.
    """
    if message is None:
        return

    try:
        msg_type = getattr(message, "type", None)

        if msg_type == "Results":
            # Transcript result
            self._process_transcript(message)
        elif msg_type == "UtteranceEnd":
            # User finished speaking (silence detected)
            logger.debug("Deepgram utterance end detected")
            asyncio.create_task(self._emit_utterance_end())
        elif msg_type == "SpeechStarted":
            # Voice activity detected (Enterprise tier)
            # Used for barge-in / interruption handling
            logger.debug("Deepgram speech started - for interruption handling")
            asyncio.create_task(self._emit_speech_started())
        elif msg_type == "Metadata":
            logger.debug(f"Deepgram metadata: {message}")

    except Exception as e:
        logger.error(f"Error handling Deepgram message: {e}")


def _process_transcript(self, result: Any) -> None:
    """Process a transcript result from Deepgram."""
    try:
        channel = getattr(result, "channel", None)
        if not channel:
            return

        alternatives = getattr(channel, "alternatives", [])
        if not alternatives:
            return

        alt = alternatives[0]
        text = getattr(alt, "transcript", "")

        if not text:
            return

        # Build result object
        transcript_result = TranscriptResult(
            text=text,
            is_final=getattr(result, "is_final", False),
            confidence=getattr(alt, "confidence", 0.0),
            words=getattr(alt, "words", None),
            start_time=getattr(result, "start", 0.0),
            end_time=getattr(result, "start", 0.0) + getattr(result, "duration", 0.0),
        )

        # Emit to callback
        asyncio.create_task(self._emit_transcript(transcript_result))

        if transcript_result.is_final:
            logger.debug(f"Deepgram transcript (final): {text}")
        else:
            logger.debug(f"Deepgram transcript (interim): {text[:50]}...")

    except Exception as e:
        logger.error(f"Error processing Deepgram transcript: {e}")
```

### Cleanup and Control

```python
async def disconnect(self) -> None:
    """Disconnect from Deepgram and cleanup."""
    # Cancel listening task
    if self._listen_task:
        self._listen_task.cancel()
        try:
            await self._listen_task
        except asyncio.CancelledError:
            pass
        self._listen_task = None

    # Close connection gracefully
    if self._connection:
        try:
            from deepgram.extensions.types.sockets import ListenV1ControlMessage
            await self._connection.send_control(
                ListenV1ControlMessage(type="CloseStream")
            )
        except Exception as e:
            logger.warning(f"Error closing Deepgram connection: {e}")

        self._connection = None

    self._client = None
    self._is_connected = False
    logger.debug("Disconnected from Deepgram STT")


async def flush(self) -> None:
    """
    Flush pending audio and wait for final results.

    Signals end of audio stream to Deepgram.
    """
    if self._connection and self._is_connected:
        try:
            from deepgram.extensions.types.sockets import ListenV1ControlMessage
            await self._connection.send_control(
                ListenV1ControlMessage(type="Finalize")
            )
            # Give time for final results
            await asyncio.sleep(0.2)
        except Exception as e:
            logger.warning(f"Error flushing Deepgram: {e}")
```

## Endpointing Configuration

Endpointing controls when Deepgram considers an utterance complete. Choose based on your tier:

### Enterprise Tier (Recommended)

```python
# Fast endpointing for low-latency conversations
config = STTProviderConfig(
    model="nova-3",
    utterance_end_ms=300,   # 300ms silence = end of utterance
    vad_events=True,        # Enable SpeechStarted events for barge-in
)
```

### Pro Tier

```python
# More conservative endpointing
config = STTProviderConfig(
    model="nova-3",
    utterance_end_ms=800,   # 800ms silence = end of utterance
    vad_events=False,       # VAD events not available
)
```

## VAD (Voice Activity Detection)

VAD events enable barge-in (interruption) handling for voice AI agents:

```python
# Register callback for speech start (Enterprise tier only)
def on_speech_started(self, callback):
    """
    Set callback for speech start detection.

    Called when voice activity is detected.
    Use to stop TTS playback when user interrupts.

    Requires STTProviderConfig.vad_events = True
    """
    self._on_speech_started = callback


# Usage in voice agent
provider.on_speech_started(handle_interruption)

async def handle_interruption():
    """Stop TTS when user starts speaking."""
    await tts_provider.stop_playback()
    logger.info("User interrupted - stopped TTS playback")
```

## Callback Registration

```python
# Type aliases for callbacks
TranscriptCallback = Callable[[TranscriptResult], Awaitable[None]]
UtteranceEndCallback = Callable[[], Awaitable[None]]
SpeechStartedCallback = Callable[[], Awaitable[None]]


def on_transcript(self, callback: TranscriptCallback) -> None:
    """
    Set callback for transcript results.

    Callback receives TranscriptResult for each transcription.
    May be called multiple times with interim_results (is_final=False)
    before the final result.
    """
    self._on_transcript = callback


def on_utterance_end(self, callback: UtteranceEndCallback) -> None:
    """
    Set callback for utterance end detection.

    Called when silence is detected after speech, indicating
    the user has finished speaking.
    """
    self._on_utterance_end = callback
```

## Context Manager Usage

```python
async with DeepgramSTTProvider(api_key=os.getenv("DEEPGRAM_API_KEY")) as provider:
    # Set up callbacks
    provider.on_transcript(handle_transcript)
    provider.on_utterance_end(handle_utterance_end)

    # Connect and stream audio
    await provider.connect(config)

    for audio_chunk in audio_stream:
        await provider.send_audio(audio_chunk)

    # Cleanup happens automatically
```

## Error Handling

```python
def _handle_error(self, error: Any) -> None:
    """Handle error event from Deepgram."""
    logger.error(f"Deepgram error: {error}")
    # Implement reconnection logic here if needed


def _handle_close(self, *args, **kwargs) -> None:
    """Handle connection close event."""
    logger.debug("Deepgram WebSocket connection closed")
    self._is_connected = False
    # Trigger reconnection if unexpected close
```

## Environment Setup

```bash
# .env file
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DEEPGRAM_API_KEY")
if not api_key:
    raise ValueError("DEEPGRAM_API_KEY environment variable required")
```

## Best Practices

1. **Always use async/await** - Deepgram SDK v5 is fully async
2. **Set appropriate utterance_end_ms** - 300ms for Enterprise, 800ms for Pro
3. **Handle reconnection** - WebSocket connections can drop
4. **Use context managers** - Ensures proper cleanup
5. **Log transcripts** - Helps debug speech recognition issues
6. **Buffer audio** - Don't send tiny chunks; batch to ~20ms frames
7. **Match audio format** - Ensure sample_rate and encoding match source

## SDK Version Notes

This guide is for Deepgram SDK v5+:
- Uses `AsyncDeepgramClient` instead of `Deepgram`
- Uses `listen.v1.connect()` instead of `transcription.live`
- Uses `EventType` enum instead of string events
- Uses `ListenV1MediaMessage` for audio
- Uses `ListenV1ControlMessage` for control signals
