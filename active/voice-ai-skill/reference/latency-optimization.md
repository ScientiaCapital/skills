# Voice AI Latency Optimization

Reference patterns extracted from VozLux production codebase for achieving sub-500ms voice AI latency.

## Target Latency Breakdown

Total voice response latency = STT + LLM + TTS

```
Component    | Target   | Provider
-------------|----------|------------------
STT          | ~150ms   | Deepgram Nova-2
LLM          | ~220ms   | Groq (llama-3.1-8b-instant)
TTS          | ~90ms    | Cartesia Sonic-3
-------------|----------|------------------
TOTAL        | ~460ms   | End-to-end target
```

---

## Tier-Based Latency Targets

Different subscription tiers have different latency SLAs:

| Tier | Target Latency | Architecture |
|------|----------------|--------------|
| Free | 3000ms | TwiML-based, Polly TTS |
| Starter | 2500ms | TwiML-based, Polly TTS |
| Pro | 600ms | Media Streams + Deepgram + Cartesia |
| Enterprise | 400ms | Full streaming + interruption support |

### Tier Configuration

```python
from dataclasses import dataclass
from enum import Enum


class Tier(Enum):
    """Voice tier levels mapped to subscription plans."""
    FREE = "free"
    STARTER = "starter"      # $149/mo - TwiML/Polly
    PRO = "pro"              # $249/mo - Media Streams + Cartesia
    ENTERPRISE = "enterprise"  # $499/mo - Full streaming + emotions


@dataclass
class VoiceConfig:
    """Configuration for a voice session."""
    tier: Tier
    language: str = "en"

    # Feature flags based on tier
    enable_streaming: bool = False
    enable_emotions: bool = False
    enable_interruptions: bool = False

    # Latency targets
    target_latency_ms: int = 2000  # Default for STARTER

    # Deepgram settings (PRO/ENTERPRISE)
    utterance_end_ms: int = 1000
    vad_events: bool = False

    def __post_init__(self):
        """Set tier-specific defaults after initialization."""
        if self.tier == Tier.FREE:
            self.enable_streaming = False
            self.enable_emotions = False
            self.enable_interruptions = False
            self.target_latency_ms = 3000
            self.utterance_end_ms = 1000
        elif self.tier == Tier.STARTER:
            self.enable_streaming = False
            self.enable_emotions = False
            self.enable_interruptions = False
            self.target_latency_ms = 2500
            self.utterance_end_ms = 1000
        elif self.tier == Tier.PRO:
            self.enable_streaming = True
            self.enable_emotions = True  # Basic presets
            self.enable_interruptions = False
            self.target_latency_ms = 600
            self.utterance_end_ms = 800
        elif self.tier == Tier.ENTERPRISE:
            self.enable_streaming = True
            self.enable_emotions = True  # Full control
            self.enable_interruptions = True
            self.target_latency_ms = 400
            self.utterance_end_ms = 500
            self.vad_events = True
```

---

## Streaming All Components

The key to low latency is streaming every component in the pipeline:

```
Audio In -> [Streaming STT] -> tokens -> [Streaming LLM] -> tokens -> [Streaming TTS] -> Audio Out
               |                             |                            |
               v                             v                            v
          ~150ms TTFT                   ~220ms TTFB                   ~90ms TTFA
```

### STT Streaming (Deepgram)

```python
"""
Deepgram streaming STT for low-latency transcription.

- Real-time streaming: ~150ms latency
- Utterance end detection for natural turn-taking
- Smart formatting and punctuation
"""

from deepgram import AsyncDeepgramClient


class DeepgramSTTProvider:
    """
    Deepgram streaming STT provider using Nova models.

    Features:
    - Real-time streaming transcription
    - Low latency (~150ms typical)
    - Utterance end detection
    - Smart formatting and punctuation
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None
        self._connection = None
        self._is_connected = False

    def get_latency_estimate_ms(self) -> int:
        """Nova models have ~150ms latency."""
        return 150

    async def connect(self, config):
        """Connect to Deepgram streaming transcription."""
        self._client = AsyncDeepgramClient(api_key=self.api_key)

        # Create WebSocket connection
        self._connection = await self._client.listen.v1.connect(
            model="nova-2",          # Latest model
            language=config.language,
            encoding="mulaw",        # Twilio format
            sample_rate="8000",      # Telephony standard
        )

        # Register event handlers
        self._connection.on("message", self._handle_message)
        self._connection.on("utterance_end", self._handle_utterance_end)

        self._is_connected = True

    async def send_audio(self, audio: bytes):
        """Send audio chunk for transcription (non-blocking)."""
        if self._is_connected and audio:
            await self._connection.send_media(audio)
```

### LLM Streaming (Groq)

```python
"""
Groq streaming LLM for ultra-low latency inference.

- ~220ms TTFB with llama-3.1-8b-instant
- Stream tokens to TTS as they arrive
"""

from groq import AsyncGroq


async def generate_stream(prompt: str, system_prompt: str = None):
    """
    Streaming generation for lowest TTFB.

    Yields tokens as they arrive - pipe directly to TTS.
    """
    client = AsyncGroq()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    stream = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=150,
        stream=True,
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
```

### TTS Streaming (Cartesia)

```python
"""
Cartesia streaming TTS for low-latency synthesis.

- ~90ms TTFA (Time To First Audio)
- Stream audio chunks as they're generated
"""

from cartesia import AsyncCartesia


class CartesiaTTSProvider:
    """
    Cartesia Sonic TTS provider with streaming and emotion support.

    Features:
    - Ultra-low latency (~90ms TTFB)
    - Streaming audio output
    - Emotion controls
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None

    def get_latency_estimate_ms(self) -> int:
        """Sonic has ~90ms TTFB latency."""
        return 90

    async def synthesize_stream(self, text: str, config):
        """
        Stream synthesized audio chunks.

        Yields audio chunks as they're generated for low-latency playback.
        First chunk typically arrives in ~90ms.
        """
        if not self._client:
            self._client = AsyncCartesia(api_key=self.api_key)

        response = await self._client.tts.sse(
            model_id="sonic-2",
            transcript=text,
            voice_id=config.voice_id,
            output_format={
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 8000,  # Telephony standard
            },
            language=config.language,
        )

        async for chunk in response:
            if hasattr(chunk, "audio") and chunk.audio:
                yield chunk.audio
```

---

## Connection Warming and Pre-initialization

Warm up connections before calls to eliminate cold-start latency:

```python
"""
Connection warming strategies for voice AI.

Pre-initialize connections to eliminate cold-start latency.
"""

import asyncio


class WarmableProvider:
    """Base class for providers that support connection warming."""

    _is_warmed_up: bool = False

    async def warmup(self) -> None:
        """
        Warm up the connection.

        Call this during application startup or before first call.
        """
        raise NotImplementedError


class CartesiaTTSProvider(WarmableProvider):
    """Cartesia TTS with connection warming."""

    async def warmup(self) -> None:
        """
        Warm up the Cartesia connection.

        Makes a minimal API call to establish the connection
        and reduce latency on first synthesis.
        """
        if self._is_warmed_up:
            return

        try:
            # Ensure client is initialized
            if not self._client:
                self._client = AsyncCartesia(api_key=self.api_key)

            # Simple warmup - just ensure connection is established
            # Could make a test synthesis but that costs money
            self._is_warmed_up = True
        except Exception as e:
            print(f"Cartesia warmup failed: {e}")


class VoicePipelineManager:
    """
    Manager for voice pipelines with connection warming.

    Warms up all providers on startup.
    """

    def __init__(self):
        self._stt_provider = None
        self._tts_provider = None
        self._llm = None

    async def warmup_all(self) -> None:
        """Warm up all providers in parallel."""
        await asyncio.gather(
            self._warmup_stt(),
            self._warmup_tts(),
            self._warmup_llm(),
        )

    async def _warmup_stt(self):
        """Warm up STT connection."""
        self._stt_provider = DeepgramSTTProvider()
        # Deepgram connection is established on first connect()
        # No explicit warmup needed

    async def _warmup_tts(self):
        """Warm up TTS connection."""
        self._tts_provider = CartesiaTTSProvider()
        await self._tts_provider.warmup()

    async def _warmup_llm(self):
        """Warm up LLM (Groq has no connection to warm)."""
        # Groq uses HTTP, no persistent connection
        # But we can verify the API key is valid
        self._llm = GroqLLM()
```

---

## WebSocket Optimization for Media Streams

```python
"""
WebSocket optimization for Twilio Media Streams.

Key optimizations:
- Async message processing
- Audio queue for smooth playback
- Parallel send/receive
"""

import asyncio
import base64
import json
from fastapi import WebSocket


class MediaStreamsHandler:
    """
    Handler for Twilio Media Streams WebSocket connections.

    Optimizations:
    - Async message processing
    - Send queue for non-blocking audio output
    - Parallel send/receive tasks
    """

    def __init__(self, websocket: WebSocket, config: VoiceConfig):
        self.websocket = websocket
        self.config = config

        # Audio queue for smooth playback
        self._send_queue: asyncio.Queue = asyncio.Queue()
        self._send_task = None
        self._is_running = False

    async def run(self):
        """Main loop with parallel send/receive."""
        await self.websocket.accept()
        self._is_running = True

        # Start send queue processor in background
        self._send_task = asyncio.create_task(self._process_send_queue())

        # Process incoming messages
        while self._is_running:
            try:
                message = await self.websocket.receive_text()
                await self._handle_message(json.loads(message))
            except Exception:
                break

        await self._cleanup()

    async def _process_send_queue(self):
        """
        Process outgoing audio queue.

        Runs in background, sending audio as it becomes available.
        Non-blocking to prevent audio stuttering.
        """
        while self._is_running:
            try:
                # Wait for audio with timeout
                audio_data = await asyncio.wait_for(
                    self._send_queue.get(),
                    timeout=0.1  # 100ms timeout
                )
                await self._send_audio(audio_data)
            except asyncio.TimeoutError:
                continue

    async def _send_audio(self, audio_data: bytes):
        """Send audio chunk to Twilio (non-blocking)."""
        if not self._stream_sid:
            return

        payload = base64.b64encode(audio_data).decode("utf-8")
        message = {
            "event": "media",
            "streamSid": self._stream_sid,
            "media": {"payload": payload}
        }
        await self.websocket.send_text(json.dumps(message))

    async def queue_audio(self, audio_data: bytes):
        """Queue audio for sending (non-blocking)."""
        await self._send_queue.put(audio_data)
```

---

## Parallel Processing Patterns

Process independent operations in parallel to minimize total latency:

```python
"""
Parallel processing patterns for voice AI.

Run independent operations concurrently to minimize latency.
"""

import asyncio


async def parallel_init_example():
    """Initialize all providers in parallel."""
    # DON'T do this (sequential):
    # stt = await init_stt()  # 100ms
    # tts = await init_tts()  # 100ms
    # llm = await init_llm()  # 100ms
    # Total: 300ms

    # DO this (parallel):
    stt, tts, llm = await asyncio.gather(
        init_stt(),  # 100ms
        init_tts(),  # 100ms (concurrent)
        init_llm(),  # 100ms (concurrent)
    )
    # Total: ~100ms (concurrent)


async def parallel_cleanup_example(providers: list):
    """Cleanup all providers in parallel."""
    await asyncio.gather(
        *[p.close() for p in providers],
        return_exceptions=True  # Don't fail on individual errors
    )


class ProPipeline:
    """
    PRO tier voice pipeline with parallel operations.
    """

    async def start_session(self) -> str:
        """Initialize providers in parallel."""
        try:
            # Initialize TTS and STT in parallel
            await asyncio.gather(
                self._init_tts(),
                self._init_stt(),
            )
            return self._session_id
        except Exception as e:
            await self._cleanup_providers()
            raise

    async def _init_tts(self):
        """Initialize and warm up TTS."""
        self._tts_provider = CartesiaTTSProvider()
        await self._tts_provider.warmup()

    async def _init_stt(self):
        """Initialize and connect STT."""
        self._stt_provider = DeepgramSTTProvider()
        await self._stt_provider.connect(self._stt_config)
```

---

## Caching Strategies

```python
"""
Caching strategies for voice AI.

Cache common responses and embeddings to reduce latency.
"""

from functools import lru_cache
from typing import Optional
import hashlib


# In-memory cache for common greetings/responses
RESPONSE_CACHE = {}


def cache_key(text: str, language: str) -> str:
    """Generate cache key from text and language."""
    return hashlib.md5(f"{language}:{text}".encode()).hexdigest()


async def get_cached_audio(text: str, language: str) -> Optional[bytes]:
    """Get cached audio if available."""
    key = cache_key(text, language)
    return RESPONSE_CACHE.get(key)


async def cache_audio(text: str, language: str, audio: bytes):
    """Cache audio for future use."""
    key = cache_key(text, language)
    RESPONSE_CACHE[key] = audio


class CachingTTSProvider:
    """
    TTS provider with caching for common phrases.

    Caches greetings and common responses to eliminate TTS latency.
    """

    # Common phrases to pre-cache
    COMMON_PHRASES = {
        "en": [
            "Hello! Thank you for calling. How can I help you today?",
            "I'm sorry, I didn't catch that. Could you please repeat?",
            "Let me check that for you.",
            "Is there anything else I can help you with?",
            "Thank you for calling. Goodbye!",
        ],
        "es": [
            "Hola! Gracias por llamar. Como puedo ayudarle hoy?",
            "Lo siento, no entendi. Podria repetir, por favor?",
            "Dejeme verificar eso para usted.",
            "Hay algo mas en que pueda ayudarle?",
            "Gracias por llamar. Adios!",
        ],
    }

    async def warmup_cache(self):
        """Pre-generate and cache common phrases."""
        for language, phrases in self.COMMON_PHRASES.items():
            for phrase in phrases:
                audio = await self._synthesize(phrase, language)
                await cache_audio(phrase, language, audio)

    async def synthesize(self, text: str, language: str = "en") -> bytes:
        """Synthesize with cache check."""
        # Check cache first
        cached = await get_cached_audio(text, language)
        if cached:
            return cached

        # Generate and cache
        audio = await self._synthesize(text, language)

        # Cache if it's a short phrase (likely to be repeated)
        if len(text) < 100:
            await cache_audio(text, language, audio)

        return audio
```

---

## Latency Monitoring and Persistence

```python
"""
Latency monitoring for voice AI pipelines.

Track and persist latency metrics for analysis and alerting.
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TurnLatency:
    """Latency metrics for a single turn."""
    stt_latency_ms: int
    llm_ttft_ms: int
    tts_ttfa_ms: int
    total_latency_ms: int
    stt_provider: str
    llm_provider: str
    tts_provider: str


class LatencyTracker:
    """
    Track latency metrics for voice pipeline.

    Persists to Supabase for analytics.
    """

    def __init__(self, supabase_client, target_latency_ms: int):
        self._supabase = supabase_client
        self._target_latency_ms = target_latency_ms
        self._latencies = []

    async def record_turn(
        self,
        turn_number: int,
        content: str,
        stt_latency_ms: int,
        llm_ttft_ms: int,
        tts_ttfa_ms: int,
        session_id: str,
    ):
        """Record and persist turn latency."""
        total_latency_ms = stt_latency_ms + llm_ttft_ms + tts_ttfa_ms
        self._latencies.append(total_latency_ms)

        # Check for latency violation
        if total_latency_ms > self._target_latency_ms * 1.5:
            print(
                f"LATENCY VIOLATION: {total_latency_ms}ms "
                f"(target: {self._target_latency_ms}ms)"
            )

        # Persist to database
        if self._supabase:
            await self._supabase.table("turns").insert({
                "session_id": session_id,
                "turn_number": turn_number,
                "content": content,
                "stt_latency_ms": stt_latency_ms,
                "llm_ttft_ms": llm_ttft_ms,
                "tts_ttfa_ms": tts_ttfa_ms,
                "total_latency_ms": total_latency_ms,
                "stt_provider": "deepgram",
                "llm_provider": "groq",
                "tts_provider": "cartesia",
            }).execute()

    def get_average_latency(self) -> float:
        """Get average latency across all turns."""
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    def is_meeting_target(self) -> bool:
        """Check if average latency meets target."""
        return self.get_average_latency() <= self._target_latency_ms
```

---

## Full Pipeline Example

```python
"""
Complete voice pipeline with all latency optimizations.

Target: <600ms total latency (PRO tier)
- STT: ~150ms (Deepgram Nova-2)
- LLM: ~220ms (Groq llama-3.1-8b-instant)
- TTS: ~90ms (Cartesia Sonic)
"""

import asyncio
import time


class ProPipeline:
    """
    PRO tier voice pipeline with streaming audio.

    Features:
    - Real-time audio streaming via Media Streams
    - Deepgram Nova STT for fast transcription
    - Groq LLM for ultra-low latency inference
    - Cartesia Sonic TTS for low-latency synthesis
    - Target latency: <600ms end-to-end
    """

    # Configuration constants
    TARGET_LATENCY_MS = 600
    AGENT_TIMEOUT_SECONDS = 10.0
    MAX_CONVERSATION_HISTORY = 20

    async def process_audio(self, audio_chunk):
        """
        Process incoming audio and yield response audio.

        Pipeline flow:
        1. Send audio to STT (streaming)
        2. Wait for utterance end
        3. Generate LLM response (streaming)
        4. Synthesize with TTS (streaming)
        5. Yield audio chunks

        All steps are streaming for minimum latency.
        """
        if not self._is_active:
            raise RuntimeError("Pipeline not active")

        # Send audio to STT (non-blocking)
        await self._stt_provider.send_audio(audio_chunk.data)

        # Check if we have a complete utterance
        user_text = await self._get_complete_utterance()

        if user_text:
            turn_start = time.time()

            # Generate response with timeout
            llm_start = time.time()
            try:
                response_text = await asyncio.wait_for(
                    self._generate_response(user_text),
                    timeout=self.AGENT_TIMEOUT_SECONDS
                )
                llm_ttft_ms = int((time.time() - llm_start) * 1000)
            except asyncio.TimeoutError:
                response_text = "I apologize, I'm taking too long. Could you repeat that?"
                llm_ttft_ms = int(self.AGENT_TIMEOUT_SECONDS * 1000)

            # Stream TTS response
            tts_start = time.time()
            first_chunk = True
            async for pcm_chunk in self._tts_provider.synthesize_stream(
                response_text,
                self._tts_config
            ):
                if first_chunk:
                    tts_ttfa_ms = int((time.time() - tts_start) * 1000)
                    first_chunk = False

                # Convert PCM to mulaw for Twilio
                mulaw_data = convert_pcm_to_mulaw(pcm_chunk)
                yield AudioChunk(data=mulaw_data)

            # Record latency
            total_latency = (time.time() - turn_start) * 1000
            await self._latency_tracker.record_turn(
                turn_number=self._turns_count,
                content=response_text,
                stt_latency_ms=0,  # Streaming, no discrete latency
                llm_ttft_ms=llm_ttft_ms,
                tts_ttfa_ms=tts_ttfa_ms,
                session_id=self._session_id,
            )

            if total_latency > self.TARGET_LATENCY_MS:
                print(f"Latency: {total_latency:.0f}ms (target: {self.TARGET_LATENCY_MS}ms)")
```

---

## Key Takeaways

1. **Stream Everything** - STT, LLM, and TTS should all stream for minimum latency
2. **Warm Connections** - Pre-initialize providers to eliminate cold-start latency
3. **Use Async** - All I/O should be async to prevent blocking
4. **Parallel Processing** - Run independent operations concurrently
5. **Cache Common Phrases** - Pre-generate greetings and common responses
6. **Monitor Latency** - Track and alert on latency violations
7. **Use Fast Providers**:
   - STT: Deepgram Nova-2 (~150ms)
   - LLM: Groq llama-3.1-8b-instant (~220ms)
   - TTS: Cartesia Sonic (~90ms)
8. **Keep Responses Short** - 150 max tokens for voice
9. **Limit Context** - Keep conversation history short
10. **Non-Blocking Audio** - Use queues for smooth playback
