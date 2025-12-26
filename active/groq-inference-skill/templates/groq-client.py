#!/usr/bin/env python3
"""
GROQ API Quick-Start Template
Fast inference with low latency for chat, vision, audio, and tool use.

Setup:
    pip install groq
    export GROQ_API_KEY=gsk_...

Usage:
    python groq-client.py
"""

import os
from groq import Groq

# Initialize client (reads GROQ_API_KEY from environment)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# =============================================================================
# PATTERN 1: Basic Chat Completion
# =============================================================================
def chat_completion(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Basic chat completion with GROQ's fast inference."""
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=1024,
    )
    return completion.choices[0].message.content


# =============================================================================
# PATTERN 2: Streaming Chat
# =============================================================================
def chat_streaming(prompt: str, model: str = "llama-3.3-70b-versatile"):
    """Stream tokens as they're generated for real-time UX."""
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print()  # Newline at end


# =============================================================================
# PATTERN 3: Vision / Multimodal
# =============================================================================
def analyze_image(image_url: str, question: str = "What's in this image?") -> str:
    """Analyze images with Llama 4 Scout/Maverick."""
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        max_completion_tokens=1024,
    )
    return completion.choices[0].message.content


# =============================================================================
# PATTERN 4: Speech-to-Text (Transcription)
# =============================================================================
def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """Transcribe audio file using Whisper."""
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, audio_file.read()),
            model="whisper-large-v3",
            language=language,
            response_format="text",
        )
    return transcription


# =============================================================================
# PATTERN 5: Text-to-Speech
# =============================================================================
def text_to_speech(text: str, output_path: str = "speech.wav", voice: str = "Fritz-PlayAI"):
    """Generate speech audio from text using PlayAI."""
    response = client.audio.speech.create(
        model="playai-tts",
        voice=voice,
        input=text,
        response_format="wav",
    )
    response.write_to_file(output_path)
    return output_path


# =============================================================================
# PATTERN 6: Tool Use (Function Calling)
# =============================================================================
def chat_with_tools(prompt: str) -> dict:
    """Chat with function calling support."""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice="auto",
    )

    message = completion.choices[0].message
    if message.tool_calls:
        return {
            "tool_calls": [
                {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
                for tc in message.tool_calls
            ]
        }
    return {"content": message.content}


# =============================================================================
# PATTERN 7: Reasoning Models
# =============================================================================
def reasoning_completion(prompt: str, format: str = "parsed") -> dict:
    """Use reasoning models with explicit thinking process."""
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[{"role": "user", "content": prompt}],
        reasoning_format=format,  # parsed, raw, hidden
        max_completion_tokens=2048,
    )
    message = completion.choices[0].message
    return {
        "content": message.content,
        "reasoning": getattr(message, "reasoning", None),
    }


# =============================================================================
# PATTERN 8: Compound (Built-in Tools)
# =============================================================================
def compound_search(query: str) -> dict:
    """Use Compound model with built-in web search."""
    completion = client.chat.completions.create(
        model="compound-beta",
        messages=[{"role": "user", "content": query}],
    )
    message = completion.choices[0].message
    return {
        "content": message.content,
        "executed_tools": getattr(message, "executed_tools", []),
    }


# =============================================================================
# MAIN: Demo all patterns
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("GROQ API Quick-Start Demo")
    print("=" * 60)

    # Test basic chat
    print("\n1. Basic Chat:")
    response = chat_completion("What is GROQ? One sentence.")
    print(f"   {response}")

    # Test streaming (uncomment to run)
    # print("\n2. Streaming Chat:")
    # chat_streaming("Count from 1 to 5 slowly.")

    # Test vision (uncomment with valid image URL)
    # print("\n3. Vision Analysis:")
    # result = analyze_image("https://example.com/image.jpg")
    # print(f"   {result}")

    # Test tool calling
    print("\n4. Tool Calling:")
    result = chat_with_tools("What's the weather in Tokyo?")
    print(f"   {result}")

    # Test reasoning
    print("\n5. Reasoning:")
    result = reasoning_completion("How many r's in strawberry?")
    print(f"   Answer: {result['content']}")
    if result["reasoning"]:
        print(f"   Reasoning: {result['reasoning'][:100]}...")

    # Test compound
    print("\n6. Compound (Web Search):")
    result = compound_search("What's the latest news about GROQ?")
    print(f"   {result['content'][:200]}...")
    if result["executed_tools"]:
        print(f"   Tools used: {len(result['executed_tools'])}")

    print("\n" + "=" * 60)
    print("Demo complete! See reference/ for detailed patterns.")
    print("=" * 60)
