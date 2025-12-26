---
name: voice-ai-skill
description: |
  Build production voice AI agents with ultra-low latency (<500ms). Covers STT (Deepgram),
  TTS (Cartesia), LLM (GROQ), telephony (Twilio), and orchestration (LangGraph).
  Use when building voice agents, phone bots, IVR systems, or real-time audio applications.
  Triggers: "voice agent", "phone bot", "STT", "TTS", "Deepgram", "Cartesia", "Twilio",
  "voice AI", "speech to text", "text to speech", "IVR", "call center", "voice latency".
---

# Voice AI Skill

Production-ready patterns for building voice AI agents with ultra-low latency, extracted from VozLux telephony platform.

**CRITICAL CONSTRAINT: NO OPENAI - Use Groq, Deepgram, Cartesia only.**

## Quick Start - Voice Agent From Prompt

Fastest path to a working voice agent:

```python
"""
Minimal voice agent in ~50 lines.
Stack: Deepgram STT -> Groq LLM -> Cartesia TTS
Target latency: <500ms
"""

import os
import asyncio
from groq import AsyncGroq
from deepgram import AsyncDeepgramClient
from cartesia import AsyncCartesia

# NEVER use: from openai import OpenAI

async def voice_agent_pipeline(user_audio: bytes) -> bytes:
    """Process audio input and return audio response."""

    # 1. STT: Deepgram Nova-3 (~150ms)
    dg = AsyncDeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
    transcript = await dg.listen.rest.v1.transcribe(
        {"buffer": user_audio, "mimetype": "audio/wav"},
        {"model": "nova-3", "language": "en-US"}
    )
    user_text = transcript.results.channels[0].alternatives[0].transcript

    # 2. LLM: Groq llama-3.1-8b-instant (~220ms)
    groq = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    response = await groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant. Keep responses under 2 sentences."},
            {"role": "user", "content": user_text}
        ],
        max_tokens=150,
        temperature=0.7
    )
    response_text = response.choices[0].message.content

    # 3. TTS: Cartesia Sonic-3 (~90ms)
    cartesia = AsyncCartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    audio_chunks = []
    async for chunk in await cartesia.tts.sse(
        model_id="sonic-3",
        transcript=response_text,
        voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",  # Warm female
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 8000}
    ):
        if hasattr(chunk, "audio") and chunk.audio:
            audio_chunks.append(chunk.audio)

    return b"".join(audio_chunks)  # Total: ~460ms
```

---

## Optimal Stack (VozLux-Tested)

| Component | Provider | Model | Latency | Notes |
|-----------|----------|-------|---------|-------|
| **STT** | Deepgram | Nova-3 | ~150ms | Streaming, VAD, utterance detection |
| **LLM** | Groq | llama-3.1-8b-instant | ~220ms | LPU hardware, fastest inference |
| **TTS** | Cartesia | Sonic-3 | ~90ms | 57 emotions, streaming, bilingual |
| **TOTAL** | - | - | **~460ms** | Sub-500ms target achieved |

### Provider Priority (Never OpenAI)

```python
# LLM priority for voice (by latency)
LLM_PRIORITY = [
    ("groq", "GROQ_API_KEY", "~220ms"),      # Primary - fastest
    ("cerebras", "CEREBRAS_API_KEY", "~200ms"),  # Fallback
    ("anthropic", "ANTHROPIC_API_KEY", "~500ms"),  # Quality fallback
]

# NEVER: from openai import OpenAI
```

---

## Tier-Based Architecture

| Tier | Target Latency | STT | LLM | TTS | Features |
|------|----------------|-----|-----|-----|----------|
| **Free** | 3000ms | TwiML Gather | Groq | Polly | Basic IVR |
| **Starter** | 2500ms | TwiML Gather | Groq | Polly | TwiML-based |
| **Pro** | 600ms | Deepgram Nova | Groq | Cartesia | Media Streams |
| **Enterprise** | 400ms | Deepgram + VAD | Groq | Cartesia + Emotions | Full streaming + barge-in |

### Tier Configuration

```python
from dataclasses import dataclass
from enum import Enum

class Tier(Enum):
    FREE = "free"           # 3000ms - TwiML/Polly
    STARTER = "starter"     # 2500ms - TwiML/Polly
    PRO = "pro"             # 600ms - Media Streams + Cartesia
    ENTERPRISE = "enterprise"  # 400ms - Full streaming + interruption

@dataclass
class VoiceConfig:
    """Voice session configuration by tier."""
    tier: Tier
    language: str = "en"

    # Feature flags
    enable_streaming: bool = False
    enable_emotions: bool = False
    enable_interruptions: bool = False  # Barge-in support

    # Latency targets
    target_latency_ms: int = 2500
    utterance_end_ms: int = 1000  # Silence to end utterance
    vad_events: bool = False      # Enterprise only

    def __post_init__(self):
        if self.tier == Tier.PRO:
            self.enable_streaming = True
            self.enable_emotions = True
            self.target_latency_ms = 600
            self.utterance_end_ms = 800
        elif self.tier == Tier.ENTERPRISE:
            self.enable_streaming = True
            self.enable_emotions = True
            self.enable_interruptions = True
            self.target_latency_ms = 400
            self.utterance_end_ms = 500
            self.vad_events = True
```

---

## Core Pattern: Deepgram STT (Streaming)

```python
"""
Deepgram Nova-3 streaming STT with VAD.
~150ms latency with utterance end detection.
"""

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType

class DeepgramSTTProvider:
    """Streaming STT with voice activity detection."""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._client = None
        self._connection = None
        self._on_transcript = None
        self._on_utterance_end = None

    async def connect(self, language: str = "en-US"):
        """Connect to Deepgram streaming transcription."""
        self._client = AsyncDeepgramClient(api_key=self._api_key)

        self._connection = await self._client.listen.v1.connect(
            model="nova-3",           # Latest model
            language=language,
            encoding="mulaw",         # Twilio format
            sample_rate="8000",       # Telephony standard
        )

        # Register event handlers
        self._connection.on(EventType.MESSAGE, self._handle_message)

    async def send_audio(self, audio: bytes):
        """Send audio chunk for transcription (non-blocking)."""
        if audio and self._connection:
            from deepgram.extensions.types.sockets import ListenV1MediaMessage
            await self._connection.send_media(ListenV1MediaMessage(data=audio))

    def _handle_message(self, message):
        """Process transcript and utterance end events."""
        msg_type = getattr(message, "type", None)

        if msg_type == "Results":
            channel = getattr(message, "channel", None)
            if channel and channel.alternatives:
                text = channel.alternatives[0].transcript
                is_final = getattr(message, "is_final", False)
                if text and self._on_transcript:
                    asyncio.create_task(self._on_transcript(text, is_final))

        elif msg_type == "UtteranceEnd":
            # Silence detected - user finished speaking
            if self._on_utterance_end:
                asyncio.create_task(self._on_utterance_end())

        elif msg_type == "SpeechStarted":
            # VAD: User started speaking (Enterprise tier)
            # Use for barge-in / interruption handling
            pass
```

---

## Core Pattern: Groq LLM (Streaming)

```python
"""
Groq LLM for ultra-low latency (~220ms TTFB).
CRITICAL: Never use OpenAI. Always use Groq.
"""

from groq import AsyncGroq

class GroqVoiceLLM:
    """Groq LLM optimized for voice applications."""

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",  # Fastest
        max_tokens: int = 150,                 # Short for voice
        temperature: float = 0.7
    ):
        self.client = AsyncGroq()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.system_prompt = (
            "You are a helpful voice assistant. "
            "Keep responses concise (2-3 sentences max). "
            "Speak naturally as if in a phone conversation."
        )

    async def generate(self, user_input: str) -> str:
        """Generate response (non-streaming)."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    async def generate_stream(self, user_input: str):
        """Streaming generation for lowest TTFB."""
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content  # Pipe directly to TTS
```

---

## Core Pattern: Cartesia TTS (57 Emotions)

```python
"""
Cartesia Sonic-3 TTS with emotion controls.
~90ms TTFB with streaming audio.
"""

from cartesia import AsyncCartesia

# All 57 valid emotions for Sonic-3
VALID_EMOTIONS = {
    # Positive High-Energy
    "happy", "excited", "enthusiastic", "elated", "triumphant", "amazed",
    # Positive Calm
    "content", "peaceful", "calm", "grateful", "affectionate",
    # Professional
    "neutral", "confident", "determined", "contemplative",
    # Hospitality-optimized
    "sympathetic", "apologetic", "curious",
}

# Emotion presets by scenario
EMOTION_PRESETS = {
    "greeting": "excited",
    "confirmation": "grateful",
    "info": "calm",
    "complaint": "sympathetic",
    "farewell": "grateful",
    "apology": "apologetic",
}

class CartesiaTTSProvider:
    """Cartesia Sonic-3 TTS with emotion support."""

    # Voice presets (bilingual)
    VOICE_PRESETS = {
        "en": "a0e99841-438c-4a64-b679-ae501e7d6091",  # Warm female English
        "es": "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",  # Mexican Woman
    }

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._client = None

    async def synthesize_stream(
        self,
        text: str,
        language: str = "en",
        emotion: str = "neutral",
        speed: float = 1.0
    ):
        """Stream synthesized audio chunks."""
        if not text.strip():
            return

        if not self._client:
            self._client = AsyncCartesia(api_key=self._api_key)

        voice_id = self.VOICE_PRESETS.get(language, self.VOICE_PRESETS["en"])

        # Sonic-3 uses generation_config for emotion/speed
        generation_config = {"speed": speed}
        if emotion in VALID_EMOTIONS:
            generation_config["emotion"] = emotion

        response = await self._client.tts.sse(
            model_id="sonic-3",
            transcript=text,
            voice_id=voice_id,
            output_format={
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 8000,  # Telephony
            },
            language=language,
            generation_config=generation_config,
        )

        async for chunk in response:
            if hasattr(chunk, "audio") and chunk.audio:
                yield chunk.audio
```

---

## Core Pattern: Twilio Media Streams

```python
"""
Twilio Media Streams WebSocket for real-time bidirectional audio.
PRO/ENTERPRISE tier only.
"""

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
import json
import base64
import asyncio

app = FastAPI()

@app.post("/voice/incoming")
async def incoming_call(request: Request):
    """Route incoming call to Media Streams WebSocket."""
    form_data = await request.form()
    from_number = form_data.get("From")

    # Auto-detect language from caller country code
    language = "es" if from_number.startswith("+52") else "en"

    response = VoiceResponse()
    connect = Connect()
    stream = Stream(url=f"wss://your-app.com/voice/stream?lang={language}")
    connect.append(stream)
    response.append(connect)

    return Response(content=str(response), media_type="application/xml")


@app.websocket("/voice/stream")
async def media_stream(websocket: WebSocket, lang: str = "en"):
    """WebSocket handler for Twilio Media Streams."""
    await websocket.accept()

    stream_sid = None
    stt_provider = DeepgramSTTProvider(os.getenv("DEEPGRAM_API_KEY"))
    llm = GroqVoiceLLM()
    tts_provider = CartesiaTTSProvider(os.getenv("CARTESIA_API_KEY"))

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            event = data.get("event")

            if event == "start":
                stream_sid = data["start"]["streamSid"]
                await stt_provider.connect(language=f"{lang}-US")

                # Send greeting
                greeting = "Hello! How can I help you today?"
                if lang == "es":
                    greeting = "Hola! En que puedo ayudarle hoy?"

                async for audio in tts_provider.synthesize_stream(greeting, lang, "excited"):
                    await send_audio(websocket, stream_sid, audio)

            elif event == "media":
                # Incoming audio from caller
                audio = base64.b64decode(data["media"]["payload"])
                await stt_provider.send_audio(audio)

            elif event == "stop":
                break

    finally:
        await stt_provider.disconnect()


async def send_audio(websocket: WebSocket, stream_sid: str, audio: bytes):
    """Send audio chunk back to Twilio."""
    # Convert PCM to mu-law for Twilio
    import audioop
    mulaw = audioop.lin2ulaw(audio, 2)

    payload = base64.b64encode(mulaw).decode("utf-8")
    await websocket.send_text(json.dumps({
        "event": "media",
        "streamSid": stream_sid,
        "media": {"payload": payload}
    }))


async def send_clear(websocket: WebSocket, stream_sid: str):
    """Clear audio queue for barge-in support."""
    await websocket.send_text(json.dumps({
        "event": "clear",
        "streamSid": stream_sid
    }))
```

---

## Bilingual Support (Spanish/English)

### Auto-Detection from Phone Number

```python
def get_language_from_caller(caller_number: str) -> str:
    """Detect language from caller's country code."""
    if not caller_number:
        return "es"  # Default to Spanish (majority market)

    if caller_number.startswith("+52"):
        return "es"  # Mexico
    elif caller_number.startswith("+1"):
        return "en"  # US/Canada
    else:
        return "es"  # International - default Spanish
```

### Bilingual Voice Prompts

```python
BILINGUAL_GREETINGS = {
    "hotel": {
        "en": "Thank you for calling! I'm your virtual concierge. How may I assist you?",
        "es": "Gracias por llamar! Soy su conserje virtual. En que puedo servirle?"
    },
    "restaurant": {
        "en": "Thank you for calling! How can I help with your reservation?",
        "es": "Gracias por llamar! En que puedo ayudarle con su reservacion?"
    },
}

# Spanish formality: Always use "usted" for respect
# English: Friendly, professional, direct
```

---

## Voice Prompt Engineering

### 7-Section Template

```python
VOICE_PROMPT_TEMPLATE = """
# Role
You are {{agent_name}}, a bilingual voice assistant for {{business_name}}.

# Tone & Style
- Keep responses to 2-3 sentences maximum for phone clarity
- NEVER use bullet points, numbered lists, or markdown
- Spell out emails: "john at company dot com"
- Speak phone numbers with pauses: "five one two... eight seven seven..."
- For Spanish: Use "usted" for formal respect

# Guardrails
- Never make up information you don't have
- If caller requests human transfer, comply immediately
- If 3+ failed attempts, offer human transfer
- Respond in the same language the caller uses

# Error Handling
If you misunderstand:
- English: "I want to make sure I got that right. Did you say [repeat back]?"
- Spanish: "Quiero asegurarme de entender bien. Dijo [repetir]?"

# Escalation Triggers
Transfer to human when:
- Caller explicitly requests human assistance
- Complaint or dispute arises
- 3+ failed attempts to understand caller
"""
```

---

## Latency Monitoring

```python
import time
from dataclasses import dataclass

@dataclass
class TurnLatency:
    """Latency metrics for a single turn."""
    stt_ms: int
    llm_ttfb_ms: int
    tts_ttfa_ms: int
    total_ms: int

class LatencyTracker:
    """Track and alert on latency violations."""

    def __init__(self, target_ms: int = 600):
        self._target_ms = target_ms
        self._latencies = []

    def record(self, stt_ms: int, llm_ms: int, tts_ms: int):
        total = stt_ms + llm_ms + tts_ms
        self._latencies.append(total)

        if total > self._target_ms * 1.5:
            print(f"LATENCY VIOLATION: {total}ms (target: {self._target_ms}ms)")

        return TurnLatency(stt_ms, llm_ms, tts_ms, total)

    def get_average(self) -> float:
        return sum(self._latencies) / len(self._latencies) if self._latencies else 0
```

---

## Reference Files Index

| File | Purpose |
|------|---------|
| `reference/deepgram-setup.md` | Deepgram Nova-3 STT streaming setup |
| `reference/groq-voice-llm.md` | Groq LLM for ultra-low latency |
| `reference/cartesia-tts.md` | Cartesia Sonic-3 with 57 emotions |
| `reference/twilio-webhooks.md` | Twilio Media Streams patterns |
| `reference/latency-optimization.md` | Sub-500ms optimization techniques |
| `reference/voice-prompts.md` | Voice-optimized prompt engineering |

---

## Environment Variables

```bash
# Required API Keys (NEVER OpenAI)
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=gsk_xxxxxxxxxxxx
CARTESIA_API_KEY=your_cartesia_key

# Twilio (for telephony)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+15551234567

# Optional fallbacks
ANTHROPIC_API_KEY=sk-ant-xxxxx
CEREBRAS_API_KEY=csk_xxxxx

# Application
BASE_URL=your-app.railway.app
```

---

## Integration Notes

- **Pairs with**: `groq-inference-skill` (LLM patterns), `langgraph-agents-skill` (orchestration)
- **Projects**: VozLux, SolarVoice-AI, langgraph-voice-agents
- **Constraint**: **NO OPENAI** - Use Groq for LLM, never `from openai import OpenAI`
- **Target**: Sub-500ms total latency (STT + LLM + TTS)

---

## Quick Reference Card

```
STACK:
  STT: Deepgram Nova-3 (~150ms) - from deepgram import DeepgramClient
  LLM: Groq llama-3.1-8b-instant (~220ms) - from groq import Groq
  TTS: Cartesia Sonic-3 (~90ms) - from cartesia import AsyncCartesia

NEVER:
  from openai import OpenAI  # FORBIDDEN

LATENCY TARGETS:
  Free/Starter: 2500-3000ms (TwiML)
  Pro: 600ms (Media Streams)
  Enterprise: 400ms (Full streaming + barge-in)

BILINGUAL:
  +52 -> Spanish (es)
  +1 -> English (en)
  Default -> Spanish

EMOTIONS (Sonic-3):
  greeting -> excited
  confirmation -> grateful
  complaint -> sympathetic
  info -> calm
```
