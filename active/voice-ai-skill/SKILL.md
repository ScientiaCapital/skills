---
name: voice-ai-skill
description: |
  Builds voice AI agents and conversational systems using Cartesia, Deepgram, AssemblyAI,
  Twilio, and ElevenLabs. Covers speech-to-text, text-to-speech, telephony integration,
  and voice agent architectures. Use when building voice bots, phone agents, or real-time
  voice applications. Triggers: "voice agent", "voice AI", "speech-to-text", "text-to-speech",
  "Twilio", "Deepgram", "Cartesia", "phone bot", "IVR", "conversational AI", "voice bot".
---

# Voice AI Skill

Building voice agents with Cartesia, Deepgram, AssemblyAI, Twilio, and ElevenLabs.

## Quick Reference

| Component | Primary | Fallback | Use Case |
|-----------|---------|----------|----------|
| STT (Speech-to-Text) | Deepgram | AssemblyAI | Real-time transcription |
| TTS (Text-to-Speech) | Cartesia | ElevenLabs | Voice synthesis |
| Telephony | Twilio | - | Phone calls, SMS |
| Orchestration | LangGraph | - | Conversation flow |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Voice Agent Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User ──[Phone]──► Twilio ──[WebSocket]──► Voice Server    │
│                                                              │
│   Voice Server:                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │  Audio In ──► Deepgram STT ──► Text                  │  │
│   │                                  │                    │  │
│   │                                  ▼                    │  │
│   │                          LLM (Claude/DeepSeek)        │  │
│   │                                  │                    │  │
│   │                                  ▼                    │  │
│   │  Audio Out ◄── Cartesia TTS ◄── Response Text        │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Provider Configurations

### Deepgram (Primary STT)

```python
# Deepgram real-time transcription
from deepgram import DeepgramClient, LiveTranscriptionEvents

DEEPGRAM_CONFIG = {
    "model": "nova-2",           # Best accuracy
    "language": "en-US",
    "smart_format": True,        # Punctuation, formatting
    "interim_results": True,     # Streaming partial results
    "endpointing": 300,          # ms of silence = end of speech
    "utterance_end_ms": 1000,    # Final utterance detection
    "vad_events": True,          # Voice activity detection
    "encoding": "linear16",
    "sample_rate": 16000,
}

async def setup_deepgram():
    client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])
    connection = client.listen.live.v("1")

    connection.on(LiveTranscriptionEvents.Transcript, handle_transcript)
    connection.on(LiveTranscriptionEvents.UtteranceEnd, handle_utterance_end)

    await connection.start(DEEPGRAM_CONFIG)
    return connection
```

### AssemblyAI (Fallback STT)

```python
# AssemblyAI real-time transcription
import assemblyai as aai

ASSEMBLYAI_CONFIG = {
    "sample_rate": 16000,
    "encoding": aai.AudioEncoding.pcm_s16le,
    "word_boost": ["Coperniq", "solar", "MEP"],  # Domain terms
}

def on_data(transcript: aai.RealtimeTranscript):
    if transcript.text:
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            handle_final_transcript(transcript.text)
        else:
            handle_partial_transcript(transcript.text)

transcriber = aai.RealtimeTranscriber(
    sample_rate=16000,
    on_data=on_data,
    on_error=on_error,
)
```

### Cartesia (Primary TTS)

```python
# Cartesia text-to-speech
from cartesia import Cartesia

CARTESIA_CONFIG = {
    "model_id": "sonic-english",      # Fast, natural
    "voice_id": "voice_id_here",      # Custom or preset
    "output_format": {
        "container": "raw",
        "encoding": "pcm_s16le",
        "sample_rate": 24000,
    },
    "language": "en",
}

client = Cartesia(api_key=os.environ["CARTESIA_API_KEY"])

async def synthesize_speech(text: str):
    """Stream TTS audio chunks"""
    for chunk in client.tts.bytes(
        model_id=CARTESIA_CONFIG["model_id"],
        voice_id=CARTESIA_CONFIG["voice_id"],
        transcript=text,
        output_format=CARTESIA_CONFIG["output_format"],
    ):
        yield chunk
```

### ElevenLabs (Fallback TTS)

```python
# ElevenLabs text-to-speech
from elevenlabs import generate, stream

ELEVENLABS_CONFIG = {
    "voice": "Rachel",            # Or custom voice ID
    "model": "eleven_turbo_v2",   # Low latency
    "output_format": "pcm_16000", # For telephony
}

def synthesize_elevenlabs(text: str):
    audio = generate(
        text=text,
        voice=ELEVENLABS_CONFIG["voice"],
        model=ELEVENLABS_CONFIG["model"],
    )
    return audio
```

### Twilio (Telephony)

```python
# Twilio Voice webhook handler
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

@app.route("/voice/incoming", methods=["POST"])
def handle_incoming_call():
    """Handle incoming Twilio call"""
    response = VoiceResponse()

    # Connect to media stream for real-time audio
    connect = Connect()
    stream = Stream(url=f"wss://{HOST}/voice/stream")
    stream.parameter(name="caller", value=request.form.get("From"))
    connect.append(stream)
    response.append(connect)

    return str(response)

@app.websocket("/voice/stream")
async def voice_stream(websocket):
    """WebSocket handler for Twilio media stream"""
    async for message in websocket:
        data = json.loads(message)

        if data["event"] == "media":
            # Audio from caller
            audio = base64.b64decode(data["media"]["payload"])
            await process_audio(audio)

        elif data["event"] == "start":
            stream_sid = data["start"]["streamSid"]
            # Initialize session

        elif data["event"] == "stop":
            # Call ended
            pass
```

## Voice Agent Patterns

### Conversation State Machine

```python
from enum import Enum
from langgraph.graph import StateGraph

class ConversationState(Enum):
    GREETING = "greeting"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    TRANSFERRING = "transferring"
    ENDING = "ending"

class VoiceAgentState(TypedDict):
    state: ConversationState
    transcript: str
    response: str
    context: dict
    turn_count: int

def create_voice_agent():
    workflow = StateGraph(VoiceAgentState)

    workflow.add_node("listen", listen_node)
    workflow.add_node("think", think_node)
    workflow.add_node("speak", speak_node)
    workflow.add_node("route", route_node)

    workflow.add_edge("listen", "think")
    workflow.add_edge("think", "speak")
    workflow.add_conditional_edges("speak", should_continue, {
        "listen": "listen",
        "transfer": "transfer",
        "end": END,
    })

    return workflow.compile()
```

### Interrupt Handling

```python
class InterruptHandler:
    """Handle user interruptions (barge-in)"""

    def __init__(self):
        self.is_speaking = False
        self.current_utterance = None

    async def on_user_speech_start(self):
        """User started talking"""
        if self.is_speaking:
            # Stop TTS immediately
            await self.stop_speaking()
            # Process their input
            self.is_speaking = False

    async def stop_speaking(self):
        """Stop current TTS playback"""
        if self.current_utterance:
            self.current_utterance.cancel()
            # Send stop signal to Twilio
            await self.send_clear_audio()
```

### Turn-Taking Logic

```python
TURN_CONFIG = {
    "endpointing_ms": 300,       # Silence before turn ends
    "max_turn_duration": 30,     # Max seconds per turn
    "interrupt_threshold": 0.5,  # Confidence to allow interrupt
}

async def handle_turn_end(transcript: str, state: VoiceAgentState):
    """Process complete user turn"""

    # Skip empty/noise turns
    if len(transcript.strip()) < 3:
        return state

    # Generate response
    response = await generate_response(transcript, state["context"])

    # Update state
    state["transcript"] = transcript
    state["response"] = response
    state["turn_count"] += 1

    # Speak response
    await speak_response(response)

    return state
```

## Twilio Integration Patterns

### Outbound Calls

```python
from twilio.rest import Client

async def make_outbound_call(to_number: str, context: dict):
    """Initiate outbound voice call"""
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"]
    )

    call = client.calls.create(
        to=to_number,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        url=f"{BASE_URL}/voice/outbound?context={encode(context)}",
        status_callback=f"{BASE_URL}/voice/status",
        status_callback_event=["initiated", "ringing", "answered", "completed"],
    )

    return call.sid
```

### Call Transfer

```python
def transfer_to_human(response: VoiceResponse, department: str):
    """Transfer call to human agent"""
    transfer_numbers = {
        "sales": "+1234567890",
        "support": "+1234567891",
    }

    response.say("Let me transfer you to a specialist.")
    response.dial(transfer_numbers.get(department))

    return response
```

## Latency Optimization

### Target Latencies

```yaml
latency_targets:
  stt_first_result: "<300ms"
  llm_first_token: "<500ms"
  tts_first_audio: "<200ms"
  total_turn_latency: "<1.5s"
```

### Optimization Techniques

```python
# 1. Stream everything
async def optimized_pipeline(audio_chunk):
    # Stream STT results
    async for partial in stt_stream(audio_chunk):
        if partial.is_final:
            # Start LLM immediately
            async for token in llm_stream(partial.text):
                # Stream to TTS immediately
                async for audio in tts_stream(token):
                    yield audio

# 2. Prefetch/warm connections
async def warm_connections():
    """Call on startup"""
    await deepgram_client.ping()
    await cartesia_client.ping()
    await llm_client.ping()

# 3. Use fastest models
MODEL_CONFIG = {
    "stt": "deepgram/nova-2",          # Fastest accurate STT
    "llm": "claude-3-haiku",           # Fast for simple responses
    "tts": "cartesia/sonic-english",   # Sub-200ms first audio
}
```

## Error Handling

```python
class VoiceErrorHandler:
    """Graceful degradation for voice pipeline"""

    async def handle_stt_error(self, error):
        """Fallback to AssemblyAI"""
        logger.error(f"Deepgram error: {error}")
        return await self.assemblyai_transcribe()

    async def handle_tts_error(self, error):
        """Fallback to ElevenLabs"""
        logger.error(f"Cartesia error: {error}")
        return await self.elevenlabs_synthesize()

    async def handle_llm_timeout(self):
        """Use canned response"""
        return "I'm having a moment. Could you repeat that?"

    async def handle_call_quality_issue(self):
        """Audio quality degradation"""
        return "I'm having trouble hearing you. Are you still there?"
```

## Environment Variables

```bash
# Required API Keys
DEEPGRAM_API_KEY=
ASSEMBLYAI_API_KEY=
CARTESIA_API_KEY=
ELEVENLABS_API_KEY=

# Twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# LLM (NO OPENAI)
ANTHROPIC_API_KEY=
DEEPSEEK_API_KEY=
```

## Integration Notes

- **Pairs with**: langgraph-agents-skill (orchestration), sales-outreach-skill (outbound)
- **Projects**: vozlux, solarvoice-ai, langgraph-voice-agents
- **Constraint**: NO OPENAI - use Claude, DeepSeek for LLM backbone

## Reference Files

- `reference/deepgram-setup.md` - Complete Deepgram integration
- `reference/twilio-webhooks.md` - Twilio voice webhook patterns
- `reference/latency-optimization.md` - Sub-second response techniques
- `reference/voice-prompts.md` - Voice-optimized prompt engineering
