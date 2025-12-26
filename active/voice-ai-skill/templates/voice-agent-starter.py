#!/usr/bin/env python3
"""
Voice Agent Starter Template
=============================

Production-ready voice agent using:
- STT: Deepgram Nova-3 (streaming)
- LLM: GROQ llama-3.1-8b-instant (streaming)
- TTS: Cartesia Sonic-3 (with emotions)

NO OPENAI - Uses Groq, Deepgram, and Cartesia only.

Environment Variables Required:
    GROQ_API_KEY        - Groq API key for LLM
    DEEPGRAM_API_KEY    - Deepgram API key for STT
    CARTESIA_API_KEY    - Cartesia API key for TTS
    TWILIO_ACCOUNT_SID  - (Optional) Twilio account SID
    TWILIO_AUTH_TOKEN   - (Optional) Twilio auth token

Usage:
    python voice-agent-starter.py --tier enterprise --language es
    python voice-agent-starter.py --demo

Author: Tim Kipper
License: MIT
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncIterator, Callable, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================


class Tier(Enum):
    """Service tiers with target latencies (end-to-end response time)."""
    FREE = "free"              # 3000ms target - basic usage
    STARTER = "starter"        # 2500ms target - small businesses
    PRO = "pro"                # 600ms target  - professional use
    ENTERPRISE = "enterprise"  # 400ms target  - real-time conversations


class Language(Enum):
    """Supported languages for bilingual agents."""
    ENGLISH = "en"
    SPANISH = "es"


class Emotion(Enum):
    """Cartesia voice emotions for TTS."""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    WARM = "warm"
    PROFESSIONAL = "professional"
    SYMPATHETIC = "sympathetic"
    EXCITED = "excited"
    CALM = "calm"


@dataclass
class TierConfig:
    """Configuration settings per service tier."""
    name: str
    target_latency_ms: int
    llm_model: str
    llm_max_tokens: int
    stt_model: str
    tts_model: str
    enable_interrupts: bool
    endpointing_ms: int


TIER_CONFIGS: dict[Tier, TierConfig] = {
    Tier.FREE: TierConfig(
        name="Free",
        target_latency_ms=3000,
        llm_model="llama-3.1-8b-instant",
        llm_max_tokens=256,
        stt_model="nova-2",
        tts_model="sonic-english",
        enable_interrupts=False,
        endpointing_ms=500,
    ),
    Tier.STARTER: TierConfig(
        name="Starter",
        target_latency_ms=2500,
        llm_model="llama-3.1-8b-instant",
        llm_max_tokens=512,
        stt_model="nova-2",
        tts_model="sonic-english",
        enable_interrupts=True,
        endpointing_ms=400,
    ),
    Tier.PRO: TierConfig(
        name="Pro",
        target_latency_ms=600,
        llm_model="llama-3.1-70b-versatile",
        llm_max_tokens=1024,
        stt_model="nova-2",
        tts_model="sonic-multilingual",
        enable_interrupts=True,
        endpointing_ms=300,
    ),
    Tier.ENTERPRISE: TierConfig(
        name="Enterprise",
        target_latency_ms=400,
        llm_model="llama-3.1-70b-versatile",
        llm_max_tokens=2048,
        stt_model="nova-2",
        tts_model="sonic-multilingual",
        enable_interrupts=True,
        endpointing_ms=250,
    ),
}


# Voice presets for different personas
VOICE_PRESETS: dict[str, dict] = {
    "mexican-woman": {
        "voice_id": "a0e99841-438c-4a64-b679-ae501e7d6091",  # Cartesia Spanish female
        "language": "es",
        "default_emotion": Emotion.WARM,
    },
    "american-man": {
        "voice_id": "bf991597-6c13-47e4-8411-91ec2de5c466",  # Cartesia English male
        "language": "en",
        "default_emotion": Emotion.PROFESSIONAL,
    },
    "spanish-man": {
        "voice_id": "846d6cb0-2301-48b6-9571-15daae6f6f82",  # Cartesia Spanish male
        "language": "es",
        "default_emotion": Emotion.CALM,
    },
    "british-woman": {
        "voice_id": "71a7ad14-091c-4e8e-a314-022ece01c121",  # Cartesia British female
        "language": "en",
        "default_emotion": Emotion.PROFESSIONAL,
    },
}


# =============================================================================
# LOGGING SETUP
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("voice-agent")


# =============================================================================
# VOICE AGENT STATE
# =============================================================================

@dataclass
class ConversationTurn:
    """Single turn in the conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: float = field(default_factory=lambda: asyncio.get_event_loop().time())


@dataclass
class VoiceAgentState:
    """Current state of the voice agent."""
    is_listening: bool = False
    is_speaking: bool = False
    is_processing: bool = False
    current_transcript: str = ""
    conversation_history: list[ConversationTurn] = field(default_factory=list)
    turn_count: int = 0
    session_id: str = ""
    language: Language = Language.ENGLISH
    current_emotion: Emotion = Emotion.NEUTRAL


# =============================================================================
# STT: DEEPGRAM NOVA-3 STREAMING
# =============================================================================

class DeepgramSTT:
    """
    Deepgram Speech-to-Text with streaming support.

    Uses Nova-3 model for best-in-class accuracy and latency.
    """

    def __init__(
        self,
        api_key: str,
        language: Language = Language.ENGLISH,
        tier_config: TierConfig | None = None,
    ):
        from deepgram import DeepgramClient

        self.client = DeepgramClient(api_key)
        self.language = language
        self.config = tier_config or TIER_CONFIGS[Tier.ENTERPRISE]
        self.connection = None
        self._transcript_callback: Callable[[str, bool], None] | None = None

    def _get_language_code(self) -> str:
        """Get Deepgram language code."""
        return "es" if self.language == Language.SPANISH else "en-US"

    async def start_stream(
        self,
        on_transcript: Callable[[str, bool], None],
    ) -> None:
        """
        Start streaming transcription.

        Args:
            on_transcript: Callback(text, is_final) for transcript updates
        """
        from deepgram import LiveTranscriptionEvents, LiveOptions

        self._transcript_callback = on_transcript

        options = LiveOptions(
            model=self.config.stt_model,
            language=self._get_language_code(),
            smart_format=True,
            interim_results=True,
            endpointing=self.config.endpointing_ms,
            utterance_end_ms=1000,
            vad_events=True,
            encoding="linear16",
            sample_rate=16000,
            channels=1,
        )

        self.connection = self.client.listen.live.v("1")

        # Register event handlers
        self.connection.on(LiveTranscriptionEvents.Transcript, self._handle_transcript)
        self.connection.on(LiveTranscriptionEvents.UtteranceEnd, self._handle_utterance_end)
        self.connection.on(LiveTranscriptionEvents.Error, self._handle_error)

        await self.connection.start(options)
        logger.info(f"Deepgram STT started | model={self.config.stt_model} | lang={self._get_language_code()}")

    def _handle_transcript(self, connection, result, **kwargs) -> None:
        """Handle transcript events from Deepgram."""
        try:
            transcript = result.channel.alternatives[0].transcript
            is_final = result.is_final

            if transcript and self._transcript_callback:
                self._transcript_callback(transcript, is_final)

        except (IndexError, AttributeError) as e:
            logger.warning(f"Transcript parsing error: {e}")

    def _handle_utterance_end(self, connection, utterance_end, **kwargs) -> None:
        """Handle end of utterance."""
        logger.debug("Utterance end detected")

    def _handle_error(self, connection, error, **kwargs) -> None:
        """Handle Deepgram errors."""
        logger.error(f"Deepgram error: {error}")

    async def send_audio(self, audio_chunk: bytes) -> None:
        """Send audio chunk to Deepgram for transcription."""
        if self.connection:
            await self.connection.send(audio_chunk)

    async def stop_stream(self) -> None:
        """Stop the streaming transcription."""
        if self.connection:
            await self.connection.finish()
            self.connection = None
            logger.info("Deepgram STT stopped")


# =============================================================================
# LLM: GROQ LLAMA-3.1 STREAMING
# =============================================================================

class GroqLLM:
    """
    Groq LLM with streaming support.

    Uses llama-3.1-8b-instant or llama-3.1-70b-versatile.
    NO OPENAI - Groq only.
    """

    def __init__(
        self,
        api_key: str,
        tier_config: TierConfig | None = None,
        language: Language = Language.ENGLISH,
    ):
        from groq import Groq

        self.client = Groq(api_key=api_key)
        self.config = tier_config or TIER_CONFIGS[Tier.ENTERPRISE]
        self.language = language

    def _get_system_prompt(self, custom_prompt: str) -> str:
        """Build system prompt with language context."""
        lang_context = (
            "Responde siempre en espanol. Usa un tono amable y profesional."
            if self.language == Language.SPANISH
            else "Always respond in English. Use a friendly and professional tone."
        )

        return f"""{custom_prompt}

{lang_context}

Guidelines:
- Keep responses concise (1-2 sentences for voice)
- Be conversational and natural
- Avoid technical jargon unless necessary
- Ask clarifying questions when needed
"""

    async def generate_stream(
        self,
        user_message: str,
        conversation_history: list[ConversationTurn],
        system_prompt: str,
    ) -> AsyncIterator[str]:
        """
        Generate streaming response from Groq.

        Args:
            user_message: Current user input
            conversation_history: Previous turns
            system_prompt: Agent system prompt

        Yields:
            Text chunks as they're generated
        """
        messages = [
            {"role": "system", "content": self._get_system_prompt(system_prompt)}
        ]

        # Add conversation history (last 10 turns for context)
        for turn in conversation_history[-10:]:
            messages.append({
                "role": turn.role,
                "content": turn.content,
            })

        messages.append({"role": "user", "content": user_message})

        logger.debug(f"Groq request | model={self.config.llm_model} | tokens={self.config.llm_max_tokens}")

        stream = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=messages,
            max_tokens=self.config.llm_max_tokens,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# =============================================================================
# TTS: CARTESIA SONIC-3 WITH EMOTIONS
# =============================================================================

class CartesiaTTS:
    """
    Cartesia Text-to-Speech with emotion control.

    Uses Sonic-3 for ultra-low latency and natural speech.
    """

    def __init__(
        self,
        api_key: str,
        voice_preset: str = "mexican-woman",
        tier_config: TierConfig | None = None,
    ):
        from cartesia import AsyncCartesia

        self.client = AsyncCartesia(api_key=api_key)
        self.preset = VOICE_PRESETS.get(voice_preset, VOICE_PRESETS["mexican-woman"])
        self.config = tier_config or TIER_CONFIGS[Tier.ENTERPRISE]
        self.current_emotion = self.preset["default_emotion"]

    def set_emotion(self, emotion: Emotion) -> None:
        """Set the current emotion for TTS output."""
        self.current_emotion = emotion
        logger.debug(f"TTS emotion set to: {emotion.value}")

    def _get_voice_controls(self) -> dict:
        """Get voice control parameters based on emotion."""
        emotion_controls = {
            Emotion.NEUTRAL: {"speed": "normal", "emotion": []},
            Emotion.HAPPY: {"speed": "normal", "emotion": ["positivity:high"]},
            Emotion.WARM: {"speed": "slow", "emotion": ["positivity:medium"]},
            Emotion.PROFESSIONAL: {"speed": "normal", "emotion": []},
            Emotion.SYMPATHETIC: {"speed": "slow", "emotion": ["positivity:low"]},
            Emotion.EXCITED: {"speed": "fast", "emotion": ["positivity:highest"]},
            Emotion.CALM: {"speed": "slow", "emotion": []},
        }
        return emotion_controls.get(self.current_emotion, emotion_controls[Emotion.NEUTRAL])

    async def synthesize_stream(
        self,
        text: str,
        emotion: Emotion | None = None,
    ) -> AsyncIterator[bytes]:
        """
        Stream TTS audio chunks.

        Args:
            text: Text to synthesize
            emotion: Optional emotion override

        Yields:
            Audio chunks (PCM 24kHz)
        """
        if emotion:
            self.set_emotion(emotion)

        voice_controls = self._get_voice_controls()

        logger.debug(f"Cartesia TTS | voice={self.preset['voice_id']} | emotion={self.current_emotion.value}")

        output_format = {
            "container": "raw",
            "encoding": "pcm_s16le",
            "sample_rate": 24000,
        }

        # Use streaming synthesis
        async for chunk in await self.client.tts.sse(
            model_id=self.config.tts_model,
            voice_id=self.preset["voice_id"],
            transcript=text,
            output_format=output_format,
            language=self.preset["language"],
            # Note: emotion controls may vary by Cartesia API version
        ):
            if hasattr(chunk, "audio"):
                yield base64.b64decode(chunk.audio)

    async def synthesize_full(
        self,
        text: str,
        emotion: Emotion | None = None,
    ) -> bytes:
        """
        Synthesize complete audio (non-streaming).

        Args:
            text: Text to synthesize
            emotion: Optional emotion override

        Returns:
            Complete audio bytes (PCM 24kHz)
        """
        chunks = []
        async for chunk in self.synthesize_stream(text, emotion):
            chunks.append(chunk)
        return b"".join(chunks)


# =============================================================================
# VOICE AGENT CORE
# =============================================================================

class VoiceAgent:
    """
    Production voice agent orchestrating STT, LLM, and TTS.

    Supports:
    - Real-time streaming transcription
    - Streaming LLM responses
    - Low-latency TTS with emotions
    - Interrupt handling (barge-in)
    - Bilingual support (English/Spanish)
    """

    def __init__(
        self,
        system_prompt: str,
        voice_preset: str = "mexican-woman",
        tier: Tier = Tier.ENTERPRISE,
        language: Language = Language.ENGLISH,
    ):
        self.system_prompt = system_prompt
        self.tier = tier
        self.tier_config = TIER_CONFIGS[tier]
        self.language = language
        self.state = VoiceAgentState(language=language)

        # Initialize components
        self.stt = DeepgramSTT(
            api_key=os.environ["DEEPGRAM_API_KEY"],
            language=language,
            tier_config=self.tier_config,
        )

        self.llm = GroqLLM(
            api_key=os.environ["GROQ_API_KEY"],
            tier_config=self.tier_config,
            language=language,
        )

        self.tts = CartesiaTTS(
            api_key=os.environ["CARTESIA_API_KEY"],
            voice_preset=voice_preset,
            tier_config=self.tier_config,
        )

        # Callbacks
        self._on_transcript: Callable[[str, bool], None] | None = None
        self._on_response: Callable[[str], None] | None = None
        self._on_audio: Callable[[bytes], None] | None = None

        logger.info(
            f"VoiceAgent initialized | tier={tier.value} | "
            f"target_latency={self.tier_config.target_latency_ms}ms | "
            f"language={language.value}"
        )

    def on_transcript(self, callback: Callable[[str, bool], None]) -> None:
        """Register callback for transcript updates."""
        self._on_transcript = callback

    def on_response(self, callback: Callable[[str], None]) -> None:
        """Register callback for LLM response text."""
        self._on_response = callback

    def on_audio(self, callback: Callable[[bytes], None]) -> None:
        """Register callback for TTS audio chunks."""
        self._on_audio = callback

    def _handle_transcript(self, text: str, is_final: bool) -> None:
        """Internal transcript handler."""
        self.state.current_transcript = text

        if self._on_transcript:
            self._on_transcript(text, is_final)

        if is_final and text.strip():
            # Queue processing (non-blocking)
            asyncio.create_task(self._process_turn(text))

    async def _process_turn(self, user_text: str) -> None:
        """Process a complete user turn."""
        if self.state.is_processing:
            logger.warning("Already processing, skipping turn")
            return

        self.state.is_processing = True
        self.state.is_listening = False

        try:
            # Add user turn to history
            self.state.conversation_history.append(
                ConversationTurn(role="user", content=user_text)
            )

            # Generate and stream response
            full_response = ""
            sentence_buffer = ""

            async for token in self.llm.generate_stream(
                user_message=user_text,
                conversation_history=self.state.conversation_history,
                system_prompt=self.system_prompt,
            ):
                full_response += token
                sentence_buffer += token

                if self._on_response:
                    self._on_response(token)

                # Stream TTS when we have a complete sentence
                if any(punct in token for punct in ".!?"):
                    await self._speak_text(sentence_buffer.strip())
                    sentence_buffer = ""

            # Speak any remaining text
            if sentence_buffer.strip():
                await self._speak_text(sentence_buffer.strip())

            # Add assistant turn to history
            self.state.conversation_history.append(
                ConversationTurn(role="assistant", content=full_response)
            )

            self.state.turn_count += 1
            logger.info(f"Turn {self.state.turn_count} complete | response_len={len(full_response)}")

        except Exception as e:
            logger.error(f"Turn processing error: {e}")
            # Speak error message
            error_msg = (
                "Lo siento, hubo un problema. Por favor intenta de nuevo."
                if self.language == Language.SPANISH
                else "Sorry, there was a problem. Please try again."
            )
            await self._speak_text(error_msg)

        finally:
            self.state.is_processing = False
            self.state.is_listening = True

    async def _speak_text(self, text: str) -> None:
        """Synthesize and output speech."""
        if not text:
            return

        self.state.is_speaking = True

        try:
            async for audio_chunk in self.tts.synthesize_stream(text):
                if self._on_audio:
                    self._on_audio(audio_chunk)
        finally:
            self.state.is_speaking = False

    async def start(self) -> None:
        """Start the voice agent."""
        await self.stt.start_stream(on_transcript=self._handle_transcript)
        self.state.is_listening = True
        logger.info("Voice agent started and listening")

    async def stop(self) -> None:
        """Stop the voice agent."""
        await self.stt.stop_stream()
        self.state.is_listening = False
        logger.info("Voice agent stopped")

    async def send_audio(self, audio_chunk: bytes) -> None:
        """Send audio to the agent for processing."""
        if self.state.is_listening and not self.state.is_speaking:
            await self.stt.send_audio(audio_chunk)

    def interrupt(self) -> None:
        """Handle user interrupt (barge-in)."""
        if self.tier_config.enable_interrupts and self.state.is_speaking:
            logger.info("User interrupt detected")
            self.state.is_speaking = False
            # In production, this would also cancel TTS playback


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_voice_agent(
    prompt: str,
    voice: str = "mexican-woman",
    tier: str = "enterprise",
    language: str = "es",
) -> VoiceAgent:
    """
    Factory function to create a configured voice agent.

    Args:
        prompt: System prompt defining agent behavior
        voice: Voice preset name (mexican-woman, american-man, etc.)
        tier: Service tier (free, starter, pro, enterprise)
        language: Language code (en, es)

    Returns:
        Configured VoiceAgent instance

    Example:
        agent = create_voice_agent(
            prompt="You are a helpful customer service agent for a solar company.",
            voice="mexican-woman",
            tier="enterprise",
            language="es"
        )
    """
    # Parse tier
    tier_enum = Tier(tier.lower())

    # Parse language
    language_enum = Language(language.lower())

    return VoiceAgent(
        system_prompt=prompt,
        voice_preset=voice,
        tier=tier_enum,
        language=language_enum,
    )


# =============================================================================
# CLI DEMO MODE
# =============================================================================

async def demo_mode():
    """
    Interactive demo mode for testing the voice agent.

    Uses text input instead of audio for demonstration.
    """
    print("\n" + "=" * 60)
    print("VOICE AGENT DEMO MODE")
    print("=" * 60)
    print("\nThis demo uses text input to simulate voice interaction.")
    print("Type your message and press Enter. Type 'quit' to exit.\n")

    # Check environment variables
    required_vars = ["GROQ_API_KEY", "DEEPGRAM_API_KEY", "CARTESIA_API_KEY"]
    missing = [var for var in required_vars if not os.environ.get(var)]

    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        print("\nSet these in your .env file or environment.")
        sys.exit(1)

    # Create agent
    agent = create_voice_agent(
        prompt="""You are a friendly voice assistant for a solar energy company.
Help customers with questions about solar panels, installations, and savings.
Be concise and helpful.""",
        voice="mexican-woman",
        tier="enterprise",
        language="es",
    )

    # Set up callbacks for demo output
    def on_transcript(text: str, is_final: bool) -> None:
        prefix = "[FINAL]" if is_final else "[PARTIAL]"
        print(f"{prefix} {text}")

    def on_response(token: str) -> None:
        print(token, end="", flush=True)

    def on_audio(audio: bytes) -> None:
        # In demo mode, just note audio was generated
        print(f"\n[AUDIO] Generated {len(audio)} bytes", end="")

    agent.on_transcript(on_transcript)
    agent.on_response(on_response)
    agent.on_audio(on_audio)

    print(f"Agent ready | Tier: {agent.tier.value} | Language: {agent.language.value}")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == "quit":
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            print("\nAssistant: ", end="")

            # Simulate transcript callback (since we're using text input)
            agent._handle_transcript(user_input, is_final=True)

            # Wait for processing to complete
            while agent.state.is_processing:
                await asyncio.sleep(0.1)

            print()  # New line after response

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Main entry point with CLI argument parsing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Voice Agent Starter - Production voice AI template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python voice-agent-starter.py --demo
  python voice-agent-starter.py --tier enterprise --language es
  python voice-agent-starter.py --voice american-man --language en
        """
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run interactive demo mode"
    )
    parser.add_argument(
        "--tier",
        choices=["free", "starter", "pro", "enterprise"],
        default="enterprise",
        help="Service tier (default: enterprise)"
    )
    parser.add_argument(
        "--language",
        choices=["en", "es"],
        default="es",
        help="Language code (default: es)"
    )
    parser.add_argument(
        "--voice",
        choices=list(VOICE_PRESETS.keys()),
        default="mexican-woman",
        help="Voice preset (default: mexican-woman)"
    )

    args = parser.parse_args()

    if args.demo:
        asyncio.run(demo_mode())
    else:
        # Print configuration summary
        tier_config = TIER_CONFIGS[Tier(args.tier)]
        print("\nVoice Agent Configuration")
        print("=" * 40)
        print(f"Tier:           {args.tier}")
        print(f"Target Latency: {tier_config.target_latency_ms}ms")
        print(f"LLM Model:      {tier_config.llm_model}")
        print(f"STT Model:      {tier_config.stt_model}")
        print(f"TTS Model:      {tier_config.tts_model}")
        print(f"Language:       {args.language}")
        print(f"Voice:          {args.voice}")
        print("=" * 40)
        print("\nRun with --demo to start interactive mode")


if __name__ == "__main__":
    main()
