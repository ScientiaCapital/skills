# Groq LLM for Voice AI Pipelines

Reference patterns extracted from VozLux production codebase for ultra-low latency voice AI.

## Overview

Groq provides the fastest inference via custom LPU (Language Processing Unit) hardware, achieving ~220ms TTFB (Time To First Byte). This makes it ideal for real-time voice applications targeting <500ms total latency.

**CRITICAL: Never use OpenAI. Always use `from groq import Groq`.**

---

## Provider Priority for Voice Applications

For voice AI, prioritize providers by latency:

```
1. GROQ (~220ms TTFB) - Fastest, use for voice-critical paths
2. Cerebras (~200ms TTFT) - Ultra-fast alternative
3. OpenRouter (variable) - Cost-effective fallback
4. Claude/Anthropic (variable) - High quality, higher latency
```

---

## GroqLLM Class Implementation

```python
"""
Groq LLM for ultra-low latency voice AI pipelines.

CRITICAL: Never use OpenAI. Use Groq for voice applications.
"""

import os
import json
import httpx
from typing import Optional, AsyncGenerator


class GroqLLM:
    """
    Groq LLM using OpenAI-compatible API for ultra-low latency (~220ms TTFB).

    Groq provides the fastest inference via their custom LPU hardware,
    ideal for real-time voice applications targeting <500ms total latency.

    Recommended models:
    - llama-3.1-8b-instant: Fastest, optimized for speed (~220ms)
    - llama-3.3-70b-versatile: High quality, still fast (~300ms)
    - mixtral-8x7b-32768: Good balance of quality/speed (~280ms)

    Args:
        model: Model identifier (default: "llama-3.1-8b-instant")
        temperature: Sampling temperature 0.0-1.0 (default: 0.7)
        max_tokens: Maximum tokens to generate (default: 150 for voice)

    Examples:
        >>> llm = GroqLLM(model="llama-3.1-8b-instant", temperature=0.3)
        >>> response = await llm.generate("Hello, how are you?")
    """

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        max_tokens: int = 150  # Short for voice responses
    ):
        """Initialize Groq LLM with API credentials and model config."""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set. Get key at: https://console.groq.com/keys")

        self.base_url = "https://api.groq.com/openai/v1"
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def _call_api(self, messages: list[dict], stream: bool = False) -> str:
        """
        Call Groq API with messages and return response.

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response

        Returns:
            Generated text response

        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": stream
                },
                timeout=10.0  # 10s timeout for voice responsiveness
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate response from prompt.

        Args:
            prompt: User prompt/question
            system_prompt: Optional system message for context

        Returns:
            Generated text response
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return await self._call_api(messages)

    async def agenerate_stream(
        self,
        prompt: str,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate response with streaming for lower TTFB.

        Streaming is critical for voice: start TTS synthesis
        as soon as first tokens arrive.

        Yields:
            Text chunks as they arrive
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": True
                },
                timeout=30.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and "DONE" not in line:
                        try:
                            data = json.loads(line[6:])
                            content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass
```

---

## Model Selection for Voice

### Speed-Optimized Models

| Model | TTFB | Use Case |
|-------|------|----------|
| `llama-3.1-8b-instant` | ~220ms | **Default for voice** - fastest response |
| `llama-3.3-70b-versatile` | ~300ms | Complex queries needing better reasoning |
| `mixtral-8x7b-32768` | ~280ms | Long context windows (32k tokens) |

### Voice-Specific Settings

```python
# Voice-optimized defaults
VOICE_LLM_CONFIG = {
    "model": "llama-3.1-8b-instant",  # Fastest model
    "temperature": 0.7,                # Consistent but natural
    "max_tokens": 150,                 # Short responses for voice
    "timeout": 10.0,                   # Fast fail for voice UX
}

# For complex queries (booking confirmations, etc.)
COMPLEX_LLM_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.3,               # More consistent
    "max_tokens": 250,                # Allow longer responses
    "timeout": 15.0,
}
```

---

## LLM Factory Pattern

```python
"""
Factory for creating LLM instances with provider priority.

Provider priority for voice applications:
1. Groq (fastest) - ~220ms TTFB
2. Cerebras - ~200ms TTFT
3. OpenRouter - variable latency
4. Anthropic - high quality, higher latency
"""

import os
from typing import Optional


class LLMFactory:
    """Factory for creating LLM instances optimized for voice."""

    @staticmethod
    def get_available_provider() -> str:
        """
        Get the name of an available LLM provider.

        Prioritizes by latency for voice applications.
        NEVER returns OpenAI.

        Returns:
            "groq", "cerebras", "openrouter", "anthropic", or "none"
        """
        # Prioritize by latency for voice applications:
        # 1. Groq LPU (~220ms TTFB) - fastest for voice
        if os.getenv("GROQ_API_KEY"):
            return "groq"

        # 2. Cerebras (~200ms TTFT)
        if os.getenv("CEREBRAS_API_KEY"):
            return "cerebras"

        # 3. OpenRouter (variable latency, cost-effective)
        if os.getenv("OPENROUTER_API_KEY"):
            return "openrouter"

        # 4. Anthropic (high quality, higher latency)
        if os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"

        return "none"

    @staticmethod
    def create_groq_llm(
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        max_tokens: int = 150
    ) -> "GroqLLM":
        """
        Create Groq LLM instance for ultra-low latency inference.

        Groq provides ~220ms TTFB via custom LPU hardware,
        ideal for real-time voice applications targeting <500ms total.

        Recommended models for voice:
        - llama-3.1-8b-instant: Fastest, optimized for speed
        - llama-3.3-70b-versatile: High quality, still fast
        - mixtral-8x7b-32768: Good balance

        Args:
            model: Model identifier (default: "llama-3.1-8b-instant")
            temperature: Sampling temperature 0.0-1.0 (default: 0.7)
            max_tokens: Maximum tokens to generate (default: 150)

        Returns:
            Configured GroqLLM instance

        Raises:
            ValueError: If GROQ_API_KEY not set
        """
        return GroqLLM(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    @staticmethod
    def create_voice_llm() -> "GroqLLM":
        """
        Create LLM optimized for voice applications.

        Returns Groq with voice-optimized settings:
        - llama-3.1-8b-instant model (fastest)
        - 150 max tokens (short voice responses)
        - 10s timeout (fast fail for voice UX)

        Returns:
            GroqLLM configured for voice
        """
        provider = LLMFactory.get_available_provider()

        if provider == "groq":
            return GroqLLM(
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=150
            )
        elif provider == "cerebras":
            # Fallback to Cerebras if Groq unavailable
            return CerebrasLLM(
                model="llama3.1-8b",
                temperature=0.7,
                max_tokens=150
            )
        else:
            raise ValueError(
                "No low-latency LLM provider available. "
                "Set GROQ_API_KEY or CEREBRAS_API_KEY in .env file."
            )
```

---

## Using Groq SDK Directly

For more control, use the official Groq SDK:

```python
"""
Using official Groq SDK for voice applications.

Install: pip install groq
"""

from groq import Groq, AsyncGroq
import os


# Synchronous client
def generate_sync(prompt: str) -> str:
    """Synchronous generation (not recommended for voice)."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
    )

    return response.choices[0].message.content


# Async client (recommended for voice)
async def generate_async(prompt: str, system_prompt: str = None) -> str:
    """Async generation for voice pipelines."""
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=150,
    )

    return response.choices[0].message.content


# Streaming (best for voice - start TTS as tokens arrive)
async def generate_stream(prompt: str, system_prompt: str = None):
    """Streaming generation for lowest TTFB."""
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

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

---

## Voice Pipeline Integration

```python
"""
Integrating Groq LLM into voice pipeline.

Flow: STT (~150ms) -> LLM (~220ms) -> TTS (~90ms) = ~460ms total
"""

import asyncio
from typing import AsyncGenerator


class VoiceLLMProcessor:
    """
    Voice-optimized LLM processor with streaming.

    Uses Groq for ultra-low latency inference.
    """

    def __init__(self, llm: GroqLLM = None):
        self.llm = llm or GroqLLM(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=150
        )
        self.system_prompt = (
            "You are a helpful voice assistant. "
            "Keep responses concise and conversational. "
            "Speak naturally as if in a phone conversation."
        )

    async def process(self, user_input: str) -> str:
        """
        Process user input and return response.

        For simple responses, non-streaming is fine.
        """
        return await self.llm.generate(
            prompt=user_input,
            system_prompt=self.system_prompt
        )

    async def process_stream(
        self,
        user_input: str
    ) -> AsyncGenerator[str, None]:
        """
        Process user input with streaming for lower TTFB.

        Use this when piping directly to TTS:
        - Start TTS synthesis as tokens arrive
        - Reduces perceived latency
        """
        async for chunk in self.llm.agenerate_stream(
            prompt=user_input,
            system_prompt=self.system_prompt
        ):
            yield chunk

    async def process_with_context(
        self,
        user_input: str,
        conversation_history: list[dict]
    ) -> str:
        """
        Process with conversation history for context.

        Keeps history short to minimize latency.
        """
        # Build messages with history (limit to last 10 exchanges)
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add recent history (max 20 messages = 10 exchanges)
        recent_history = conversation_history[-20:]
        messages.extend(recent_history)

        # Add current input
        messages.append({"role": "user", "content": user_input})

        return await self.llm._call_api(messages)
```

---

## Environment Variables

```bash
# .env file
# CRITICAL: Never use OPENAI_API_KEY

# Primary: Groq (fastest for voice)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Fallback: Cerebras
CEREBRAS_API_KEY=csk_xxxxxxxxxxxxxxxxxxxxx

# Cost-effective alternative: OpenRouter
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# High quality fallback: Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

---

## Key Takeaways

1. **Always use Groq for voice** - ~220ms TTFB is the fastest available
2. **Use `llama-3.1-8b-instant`** - Optimized for speed, sufficient quality for voice
3. **Keep `max_tokens` low** - 150 tokens is ideal for conversational responses
4. **Use streaming** - Pipe tokens to TTS as they arrive for lower perceived latency
5. **Never use OpenAI** - Use `from groq import Groq` instead
6. **Short timeouts** - 10s for voice, fail fast for better UX
7. **Limit context** - Keep conversation history short to minimize latency
