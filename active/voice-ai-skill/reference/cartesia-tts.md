# Cartesia TTS Setup Guide

Production-ready patterns for Cartesia Sonic-3 text-to-speech with emotion controls, extracted from VozLux telephony voice AI implementation.

## Overview

Cartesia Sonic provides ultra-low latency TTS with:
- Sonic-3 model with ~90ms time-to-first-byte
- 57 emotion controls with intensity levels
- Speed control (slowest to fastest)
- Bilingual Spanish/English support
- Streaming audio synthesis

## Installation

```bash
pip install cartesia>=1.4.0
```

## Core Configuration

### TTS Provider Config

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TTSProviderConfig:
    """Configuration for Cartesia TTS provider."""

    voice_id: str                    # Required: Cartesia voice ID
    language: str = "en"             # "en" or "es"
    model_id: str = "sonic-3"        # sonic-3 or sonic-2
    sample_rate: int = 8000          # 8000 for telephony, 24000 for high quality
    encoding: str = "pcm_s16le"      # 16-bit PCM little-endian

    # Speed control: "slowest", "slow", "normal", "fast", "fastest"
    speed: str = "normal"

    # Emotion controls (Sonic-3 only)
    # e.g., ["positivity:high", "warmth:medium"]
    emotions: Optional[List[str]] = None
```

### Voice ID Presets

```python
# Bilingual voice presets (Mexican Spanish / US English)
VOICE_PRESETS = {
    "en": {
        "default": "a0e99841-438c-4a64-b679-ae501e7d6091",      # Warm female English
        "professional": "a0e99841-438c-4a64-b679-ae501e7d6091",
        "friendly": "a0e99841-438c-4a64-b679-ae501e7d6091",
    },
    "es": {
        "default": "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",      # Mexican Woman
        "professional": "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",
        "friendly": "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",
    }
}
```

## Speed Control

### Speed Values

```python
# Speed string values for Cartesia API
VALID_SPEEDS = {"slowest", "slow", "normal", "fast", "fastest"}

# Speed to numeric multiplier mapping (sonic-3)
SPEED_TO_MULTIPLIER = {
    "slowest": 0.6,
    "slow": 0.8,
    "normal": 1.0,
    "fast": 1.2,
    "fastest": 1.5,
}
```

## Emotion Controls

### Complete Emotions List (57 emotions)

```python
# All valid emotions for Cartesia Sonic-3
# Source: https://docs.cartesia.ai/build-with-cartesia/sonic-3/volume-speed-emotion
VALID_EMOTIONS = {
    # Positive High-Energy
    "happy", "excited", "enthusiastic", "elated", "euphoric",
    "triumphant", "amazed", "surprised",

    # Positive Calm
    "content", "peaceful", "serene", "calm", "grateful", "affectionate",

    # Curious/Engaged
    "curious", "anticipation", "mysterious", "flirtatious", "joking/comedic",

    # Professional/Neutral
    "neutral", "confident", "proud", "determined", "contemplative", "trust",

    # Negative (use sparingly for hospitality)
    "angry", "mad", "outraged", "frustrated", "agitated", "threatened",
    "disgusted", "contempt", "envious", "sarcastic", "ironic",
    "sad", "dejected", "melancholic", "disappointed", "hurt", "guilty",
    "bored", "tired", "rejected", "nostalgic", "wistful", "apologetic",

    # Uncertain/Anxious
    "hesitant", "insecure", "confused", "resigned",
    "anxious", "panicked", "alarmed", "scared",

    # Distanced
    "distant", "skeptical",
}
```

### Hospitality Emotion Presets

```python
# Emotion presets optimized for voice AI agents
EMOTION_PRESETS = {
    # Universal hospitality emotions by scenario
    "hospitality": {
        "greeting": "excited",
        "confirmation": "grateful",
        "info": "calm",
        "complaint": "sympathetic",
        "emergency": "calm",
        "farewell": "grateful",
        "upsell": "enthusiastic",
        "apology": "apologetic",
    },
    # Agent-specific emotion overrides
    "by_agent": {
        "airbnb": {
            "default": "content",
            "greeting": "excited",
            "confirmation": "grateful",
            "complaint": "sympathetic",
        },
        "hotel": {
            "default": "calm",
            "greeting": "content",
            "confirmation": "grateful",
            "complaint": "sympathetic",
        },
        "restaurant": {
            "default": "enthusiastic",
            "greeting": "excited",
            "confirmation": "grateful",
            "complaint": "apologetic",
        },
        "coaching": {
            "default": "confident",
            "greeting": "enthusiastic",
            "confirmation": "content",
            "complaint": "sympathetic",
        },
        "fitness": {
            "default": "excited",
            "greeting": "enthusiastic",
            "confirmation": "proud",
            "complaint": "sympathetic",
        },
    },
}


def get_emotion_for_context(
    agent_type: str,
    scenario: str,
    language: str = "en"
) -> str:
    """
    Get appropriate emotion for a given context.

    Args:
        agent_type: Type of agent (airbnb, hotel, restaurant, coaching, fitness)
        scenario: Conversation scenario (greeting, confirmation, info, complaint, etc.)
        language: Language code ("en" or "es") - Spanish may prefer warmer tones

    Returns:
        Emotion string for Cartesia API

    Example:
        emotion = get_emotion_for_context("airbnb", "greeting", "es")
        # Returns "excited"
    """
    # Check agent-specific overrides first
    agent_emotions = EMOTION_PRESETS["by_agent"].get(agent_type, {})
    if scenario in agent_emotions:
        return agent_emotions[scenario]

    # Fall back to hospitality defaults
    emotion = EMOTION_PRESETS["hospitality"].get(scenario, "neutral")

    # Spanish callers may appreciate slightly warmer tones
    if language == "es" and scenario == "greeting":
        return "enthusiastic"

    return emotion
```

## Provider Implementation

### Complete TTS Provider

```python
from typing import AsyncGenerator, List, Optional, Dict, Any
import logging

from cartesia import AsyncCartesia

logger = logging.getLogger(__name__)


class CartesiaTTSProvider:
    """
    Cartesia Sonic-3 TTS provider with streaming and emotion support.

    Features:
    - Ultra-low latency (~90ms TTFB)
    - Streaming audio output
    - Emotion controls via generation_config
    - Bilingual Spanish/English support
    - 8kHz telephony-optimized output
    """

    def __init__(self, api_key: str):
        """
        Initialize Cartesia provider.

        Args:
            api_key: Cartesia API key from environment
        """
        if not api_key:
            raise ValueError(
                "Cartesia API key not configured. "
                "Set CARTESIA_API_KEY in .env file."
            )

        self._api_key = api_key
        self._client: Optional[AsyncCartesia] = None
        self._is_warmed_up = False

    async def __aenter__(self) -> "CartesiaTTSProvider":
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - ensures cleanup."""
        await self.close()

    @property
    def name(self) -> str:
        return "cartesia-sonic"

    @property
    def supports_streaming(self) -> bool:
        return True

    @property
    def supports_emotions(self) -> bool:
        return True

    def get_latency_estimate_ms(self) -> int:
        """Sonic-3 has ~90ms TTFB latency."""
        return 90

    async def _ensure_client(self) -> AsyncCartesia:
        """Lazy client initialization."""
        if self._client is None:
            self._client = AsyncCartesia(api_key=self._api_key)
        return self._client

    async def close(self) -> None:
        """Close the Cartesia client connection."""
        if self._client:
            await self._client.close()
            self._client = None
            self._is_warmed_up = False
```

### Output Format Configuration

```python
def _build_output_format(self, config: TTSProviderConfig) -> Dict[str, Any]:
    """Build output format configuration for Cartesia API."""
    return {
        "container": "raw",
        "encoding": config.encoding,      # pcm_s16le for Twilio
        "sample_rate": config.sample_rate,  # 8000 for telephony
    }
```

### Generation Config (Sonic-3)

```python
def _build_generation_config(self, config: TTSProviderConfig) -> Dict[str, Any]:
    """
    Build generation_config for Sonic-3 API.

    Sonic-3 uses generation_config instead of __experimental_controls.
    Recommended API for models after sonic-2-2025-03-07.
    """
    generation_config: Dict[str, Any] = {}

    # Speed (0.6 to 1.5 multiplier)
    if config.speed:
        speed_val = SPEED_TO_MULTIPLIER.get(config.speed.lower(), 1.0)
        generation_config["speed"] = speed_val

    # Volume (0.5 to 2.0 multiplier) - default 1.0
    if hasattr(config, 'volume') and config.volume is not None:
        generation_config["volume"] = max(0.5, min(2.0, config.volume))

    # Emotion (single string for sonic-3, not list with levels)
    if config.emotions and len(config.emotions) > 0:
        # Strip intensity level if present
        emotion = config.emotions[0].split(":")[0]
        if emotion in VALID_EMOTIONS:
            generation_config["emotion"] = emotion
        else:
            logger.warning(f"Unknown emotion '{emotion}', using 'neutral'")
            generation_config["emotion"] = "neutral"

    return generation_config
```

### Model Version Detection

```python
def _is_sonic3_model(self, model_id: str) -> bool:
    """
    Check if model is Sonic-3 (uses generation_config).

    Models after sonic-2-2025-03-07 should use generation_config.
    """
    if not model_id:
        return False

    model_lower = model_id.lower()

    # Explicitly sonic-3
    if "sonic-3" in model_lower:
        return True

    # sonic-2 with date after 2025-03-07 uses new API
    if "sonic-2-2025" in model_lower:
        try:
            date_part = model_lower.split("sonic-2-")[1][:10]
            if date_part >= "2025-03-08":
                return True
        except (IndexError, ValueError):
            pass

    return False
```

### Voice Config (Legacy Sonic-2)

```python
def _build_voice_config(self, config: TTSProviderConfig) -> Dict[str, Any]:
    """
    Build voice configuration with emotion controls.

    For legacy sonic-2 models using experimental_controls.
    """
    voice_config: Dict[str, Any] = {
        "mode": "id",
        "id": config.voice_id,
    }

    experimental_controls: Dict[str, Any] = {}

    # Speed control (string format)
    speed = config.speed.lower() if config.speed else "normal"
    if speed in VALID_SPEEDS:
        experimental_controls["speed"] = speed
    else:
        experimental_controls["speed"] = "normal"

    # Emotion controls
    if config.emotions:
        validated_emotions = self.format_emotions(config.emotions)
        if validated_emotions:
            experimental_controls["emotion"] = validated_emotions
    else:
        experimental_controls["emotion"] = []

    voice_config["experimental_controls"] = experimental_controls
    return voice_config
```

### Streaming Synthesis

```python
async def synthesize_stream(
    self,
    text: str,
    config: TTSProviderConfig
) -> AsyncGenerator[bytes, None]:
    """
    Stream synthesized audio chunks.

    Yields audio chunks as they're generated for low-latency playback.
    First chunk typically arrives in ~90ms for Sonic models.

    Automatically detects model version and uses appropriate API:
    - Sonic-3 / sonic-2 after 2025-03-07: Uses generation_config
    - Sonic-2 legacy: Uses _experimental_voice_controls
    """
    if not text or not text.strip():
        logger.warning("Empty text provided to synthesize_stream")
        return

    client = await self._ensure_client()

    try:
        output_format = self._build_output_format(config)
        use_sonic3_api = self._is_sonic3_model(config.model_id)

        if use_sonic3_api:
            # Sonic-3 API: use generation_config
            generation_config = self._build_generation_config(config)
            logger.debug(
                f"Cartesia synthesize_stream (sonic-3): text={text[:50]}..., "
                f"model={config.model_id}, voice={config.voice_id}"
            )

            sse_response = await client.tts.sse(
                model_id=config.model_id,
                transcript=text,
                voice_id=config.voice_id,
                output_format=output_format,
                language=config.language,
                generation_config=generation_config if generation_config else None,
            )
        else:
            # Legacy sonic-2 API: use _experimental_voice_controls
            voice_config = self._build_voice_config(config)
            voice_controls = voice_config.get("experimental_controls")

            sse_response = await client.tts.sse(
                model_id=config.model_id,
                transcript=text,
                voice_id=config.voice_id,
                output_format=output_format,
                language=config.language,
                _experimental_voice_controls=voice_controls,
            )

        # Process response chunks
        async for chunk in sse_response:
            audio_data = None
            if isinstance(chunk, dict) and "audio" in chunk:
                audio_data = chunk["audio"]
            elif hasattr(chunk, "audio") and chunk.audio:
                audio_data = chunk.audio
            elif hasattr(chunk, "data") and chunk.data:
                audio_data = chunk.data

            if audio_data and isinstance(audio_data, bytes):
                yield audio_data

    except Exception as e:
        logger.error(f"Cartesia synthesis error: {e}")
        raise
```

### Non-Streaming Synthesis

```python
async def synthesize(
    self,
    text: str,
    config: TTSProviderConfig
) -> bytes:
    """
    Synthesize text to audio (non-streaming).

    Collects all audio chunks and returns complete audio.
    Use for short utterances where latency isn't critical.
    """
    chunks: List[bytes] = []
    async for chunk in self.synthesize_stream(text, config):
        chunks.append(chunk)

    audio_data = b"".join(chunks)
    logger.debug(
        f"Synthesized {len(text)} chars -> {len(audio_data)} bytes "
        f"({config.sample_rate}Hz, {config.encoding})"
    )
    return audio_data
```

### Convenience Method with Emotions

```python
async def synthesize_with_emotions(
    self,
    text: str,
    emotions: List[str],
    voice_id: Optional[str] = None,
    language: str = "en"
) -> AsyncGenerator[bytes, None]:
    """
    Convenience method for synthesis with emotion controls.

    Args:
        text: Text to synthesize
        emotions: Emotion tags like ["positivity:high", "warmth:medium"]
        voice_id: Voice ID (uses default for language if not provided)
        language: Language code ("en" or "es")

    Yields:
        Audio chunks as bytes
    """
    if not voice_id:
        lang_presets = VOICE_PRESETS.get(language, VOICE_PRESETS["en"])
        voice_id = lang_presets.get("default")

    config = TTSProviderConfig(
        voice_id=voice_id,
        language=language,
        model_id="sonic-3",
        sample_rate=8000,
        encoding="pcm_s16le",
        emotions=emotions,
    )

    async for chunk in self.synthesize_stream(text, config):
        yield chunk
```

## Audio Format Conversion

### PCM to mu-law (for Twilio)

```python
def convert_pcm_s16le_to_mulaw(pcm_data: bytes) -> bytes:
    """
    Convert PCM 16-bit signed little-endian to mu-law.

    Twilio Media Streams use mu-law encoding for audio.
    Required when streaming directly to Twilio WebSocket.

    Args:
        pcm_data: PCM 16-bit signed little-endian audio data

    Returns:
        Mu-law encoded audio data
    """
    import audioop

    if not pcm_data:
        return b""

    # PCM s16le has 2 bytes per sample
    if len(pcm_data) % 2 != 0:
        raise ValueError(
            f"Invalid PCM s16le data: length {len(pcm_data)} not divisible by 2"
        )

    try:
        return audioop.lin2ulaw(pcm_data, 2)  # 2 bytes per sample (16-bit)
    except audioop.error as e:
        raise ValueError(f"Audio conversion failed: {e}") from e
```

### mu-law to PCM (from Twilio)

```python
def convert_mulaw_to_pcm_s16le(mulaw_data: bytes) -> bytes:
    """
    Convert mu-law to PCM 16-bit signed little-endian.

    Used when receiving audio from Twilio Media Streams.

    Args:
        mulaw_data: Mu-law encoded audio data

    Returns:
        PCM 16-bit signed little-endian audio data
    """
    import audioop

    if not mulaw_data:
        return b""

    try:
        return audioop.ulaw2lin(mulaw_data, 2)
    except audioop.error as e:
        raise ValueError(f"Audio conversion failed: {e}") from e
```

## Usage Examples

### Basic Streaming

```python
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    async with CartesiaTTSProvider(os.getenv("CARTESIA_API_KEY")) as provider:
        config = TTSProviderConfig(
            voice_id="5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",
            language="es",
            model_id="sonic-3",
            emotions=["excited"],
        )

        async for chunk in provider.synthesize_stream("Hola, bienvenido!", config):
            # Send to Twilio or audio output
            await send_to_twilio(chunk)
```

### With Emotion Context

```python
async def handle_greeting(language: str = "es"):
    emotion = get_emotion_for_context("hotel", "greeting", language)

    async with CartesiaTTSProvider(api_key) as provider:
        config = TTSProviderConfig(
            voice_id=VOICE_PRESETS[language]["default"],
            language=language,
            model_id="sonic-3",
            emotions=[emotion],
        )

        greeting = "Buenas tardes, Hotel Elegante, en que le puedo ayudar?"
        async for chunk in provider.synthesize_stream(greeting, config):
            yield chunk
```

### Warmup for Low Latency

```python
async def init_tts_provider():
    """Initialize and warm up TTS provider at startup."""
    provider = CartesiaTTSProvider(api_key=os.getenv("CARTESIA_API_KEY"))
    await provider.warmup()
    return provider


async def warmup(self) -> None:
    """
    Warm up the Cartesia connection.

    Makes minimal API call to establish connection
    and reduce latency on first synthesis.
    """
    if self._is_warmed_up:
        return

    try:
        await self._ensure_client()
        logger.debug("Cartesia connection warmed up")
        self._is_warmed_up = True
    except Exception as e:
        logger.warning(f"Cartesia warmup failed: {e}")
```

## Environment Setup

```bash
# .env file
CARTESIA_API_KEY=your_cartesia_api_key_here
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CARTESIA_API_KEY")
if not api_key:
    raise ValueError("CARTESIA_API_KEY environment variable required")
```

## Best Practices

1. **Use context managers** - Ensures proper client cleanup
2. **Warm up at startup** - Reduces first-synthesis latency
3. **Choose emotions carefully** - Match to conversation context
4. **Use streaming** - ~90ms TTFB vs waiting for full audio
5. **Handle empty text** - Skip synthesis for empty strings
6. **Log synthesis metrics** - Track latency and audio sizes
7. **Match sample rate to use case** - 8kHz for telephony, 24kHz for quality
8. **Convert for Twilio** - PCM s16le to mu-law when needed

## SDK Version Notes

This guide is for Cartesia SDK v1.4.0+:
- Uses `AsyncCartesia` for async operations
- Uses `client.tts.sse()` for streaming
- Sonic-3 uses `generation_config` parameter
- Legacy Sonic-2 uses `_experimental_voice_controls`
- Audio chunks come as `dict` with "audio" key or object with `.audio` attribute
