# GROQ Audio & Speech

Complete guide for GROQ's audio capabilities: STT (Whisper) and TTS (PlayAI).

---

## Speech-to-Text (Whisper)

> **IMPORTANT:** Whisper on GROQ runs on **GROQ hardware** - it is NOT calling OpenAI's API.
> Whisper is an open-source model that GROQ hosts for fast inference.

### Available Models

| Model | Languages | Speed | Pricing | Use Case |
|-------|-----------|-------|---------|----------|
| `whisper-large-v3` | 100+ | Standard | $0.111/hr | High accuracy |
| `whisper-large-v3-turbo` | 100+ | 3-5x faster | $0.04/hr | Real-time |
| `distil-whisper-large-v3-en` | English | 6x faster | $0.02/hr | English-only |

### Supported Audio Formats
flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm

### Max File Size
25MB

---

## Transcription Examples

### Basic Transcription

```python
from groq import Groq

client = Groq(api_key="gsk_...")

def transcribe(audio_path: str, language: str = "en") -> str:
    """Transcribe audio file"""
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",  # GROQ-hosted, NOT OpenAI
            language=language,
            response_format="text"
        )
    return result
```

### With Timestamps (verbose_json)

```python
def transcribe_with_timestamps(audio_path: str) -> dict:
    """Transcribe with word-level timestamps"""
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )
    return {
        "text": result.text,
        "segments": result.segments,
        "words": result.words
    }
```

### Translation (Any Language → English)

```python
def translate_to_english(audio_path: str) -> str:
    """Translate audio to English text"""
    with open(audio_path, "rb") as f:
        result = client.audio.translations.create(
            file=f,
            model="whisper-large-v3"
        )
    return result.text
```

### Fast Transcription (Turbo)

```python
def fast_transcribe(audio_path: str) -> str:
    """3-5x faster transcription for real-time use"""
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",  # Faster
            response_format="text"
        )
    return result
```

---

## Text-to-Speech (PlayAI)

### Available Voices
- `Fritz-PlayAI` - Neutral male voice
- `Arista-PlayAI` - Warm female voice

### Basic TTS

```python
def text_to_speech(text: str, output_path: str = "output.wav"):
    """Generate speech from text"""
    response = client.audio.speech.create(
        model="playai-tts",
        voice="Fritz-PlayAI",
        input=text,
        response_format="wav"
    )
    response.write_to_file(output_path)
    return output_path
```

### Streaming TTS

```python
def stream_tts(text: str):
    """Stream TTS audio chunks for real-time playback"""
    with client.audio.speech.with_streaming_response.create(
        model="playai-tts",
        voice="Fritz-PlayAI",
        input=text,
        response_format="wav"
    ) as response:
        for chunk in response.iter_bytes(1024):
            yield chunk
```

---

## Alternative Audio Providers

### STT Alternatives (if non-Whisper preferred)

| Provider | Strength | Install |
|----------|----------|---------|
| **Deepgram** | Real-time streaming, lowest latency | `pip install deepgram-sdk` |
| **AssemblyAI** | High accuracy, speaker diarization | `pip install assemblyai` |

### TTS Alternatives (beyond PlayAI)

| Provider | Strength | Install |
|----------|----------|---------|
| **Cartesia** | Ultra-low latency, emotional control | `pip install cartesia` |
| **ElevenLabs** | Most natural voices, voice cloning | `pip install elevenlabs` |
| **Deepgram** | Fast, cost-effective | `pip install deepgram-sdk` |

See `voice-ai-skill` for integration patterns with these providers.

---

## Voice Agent Pattern

Combine STT + LLM + TTS for voice agents:

```python
import asyncio

async def voice_agent_turn(audio_input_path: str) -> str:
    """Process one turn of voice conversation"""

    # 1. STT - Transcribe user audio
    with open(audio_input_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",  # Fast
            response_format="text"
        )

    user_text = transcription

    # 2. LLM - Generate response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Fast
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": user_text}
        ]
    )

    assistant_text = response.choices[0].message.content

    # 3. TTS - Generate audio response
    audio_response = client.audio.speech.create(
        model="playai-tts",
        voice="Fritz-PlayAI",
        input=assistant_text,
        response_format="wav"
    )

    output_path = "response.wav"
    audio_response.write_to_file(output_path)

    return output_path
```

---

## Cost Optimization

```python
def transcribe_cost_effective(audio_path: str, language: str = None):
    """Select model based on requirements"""

    # English-only and speed critical
    if language == "en" and need_speed:
        model = "distil-whisper-large-v3-en"  # $0.02/hr

    # Any language, speed critical
    elif need_speed:
        model = "whisper-large-v3-turbo"      # $0.04/hr

    # Best accuracy
    else:
        model = "whisper-large-v3"            # $0.111/hr

    with open(audio_path, "rb") as f:
        return client.audio.transcriptions.create(
            file=f,
            model=model,
            language=language,
            response_format="text"
        )
```

---

## Best Practices

1. **STT Model Selection**: Use turbo for real-time, large-v3 for accuracy
2. **File Size**: Chunk large files to stay under 25MB limit
3. **Language Hint**: Provide `language` parameter for better accuracy
4. **Streaming TTS**: Use for real-time voice applications
5. **Alternative Providers**: Consider Deepgram/Cartesia for ultra-low latency

---

## NO OPENAI

Whisper is open-source. GROQ hosts it on their hardware:

```python
from groq import Groq  # Never: from openai import OpenAI

# This is NOT calling OpenAI's API
result = client.audio.transcriptions.create(
    model="whisper-large-v3",  # GROQ-hosted open-source model
    file=audio_file
)
```
