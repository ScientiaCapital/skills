# GROQ Models Catalog

Complete reference for all GROQ API models (December 2025).

---

## Text-to-Text Models

### Llama 4 Models (Latest - Meta)

| Model | Context | Capabilities | Pricing ($/1M) |
|-------|---------|--------------|----------------|
| `meta-llama/llama-4-scout-17b-16e-instruct` | 128K | Text, Vision, Tools | $0.59/$0.79 |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | 128K | Text, Vision, Tools, Reasoning | $0.59/$0.79 |

**Llama 4 Scout**: Best for vision/OCR, supports up to 5 images per request
**Llama 4 Maverick**: Best for reasoning with 128 experts

### Llama 3.3 & 3.1 Models

| Model | Context | Capabilities | Pricing ($/1M) |
|-------|---------|--------------|----------------|
| `llama-3.3-70b-versatile` | 128K | Text, Tools, JSON mode | $0.59/$0.79 |
| `llama-3.1-8b-instant` | 128K | Text, Tools, JSON mode | $0.05/$0.08 |
| `llama-3.1-70b-versatile` | 128K | Text, Tools, JSON mode | $0.59/$0.79 |

**llama-3.3-70b**: Best all-around model
**llama-3.1-8b**: Ultra-fast, cheapest for simple tasks

### Other Text Models

| Model | Context | Use Case | Pricing ($/1M) |
|-------|---------|----------|----------------|
| `gemma2-9b-it` | 8K | Instruction following | $0.20/$0.20 |
| `qwen/qwen3-32b` | 32K | Multilingual, Chinese | $0.35/$0.55 |
| `llama-guard-3-8b` | 8K | Content moderation | $0.20/$0.20 |

---

## Speech-to-Text Models (Whisper)

> **Note:** Whisper on GROQ is an open-source model hosted on **GROQ hardware** - NOT OpenAI's API.

| Model | Languages | Speed | Pricing |
|-------|-----------|-------|---------|
| `whisper-large-v3` | 100+ | Standard | $0.111/hr |
| `whisper-large-v3-turbo` | 100+ | 3-5x faster | $0.04/hr |
| `distil-whisper-large-v3-en` | English only | 6x faster | $0.02/hr |

**Audio Formats**: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
**Max File Size**: 25MB

---

## Text-to-Speech Models

| Model | Voices | Pricing |
|-------|--------|---------|
| `playai-tts` | Fritz-PlayAI, Arista-PlayAI | $15/1M chars |

---

## Compound Models (Built-in Tools)

| Model | Built-in Tools | Use Case |
|-------|----------------|----------|
| `compound-beta` | web_search, code_execution | Agentic workflows |

---

## Model Selection Guide

### By Use Case

| Use Case | Recommended Model |
|----------|-------------------|
| Low-latency chat | `llama-3.1-8b-instant` |
| High-quality chat | `llama-3.3-70b-versatile` |
| Vision + text | `meta-llama/llama-4-scout-17b-16e-instruct` |
| Complex reasoning | `meta-llama/llama-4-maverick-17b-128e-instruct` |
| Audio transcription (fast) | `whisper-large-v3-turbo` |
| Audio transcription (accurate) | `whisper-large-v3` |
| Content moderation | `llama-guard-3-8b` |
| Budget-friendly | `llama-3.1-8b-instant` |

### By Priority

| Priority | Model | Notes |
|----------|-------|-------|
| Speed | `llama-3.1-8b-instant` | Fastest inference |
| Quality | `llama-3.3-70b-versatile` | Best all-around |
| Vision | `llama-4-scout-17b-16e` | Up to 5 images |
| Cost | `llama-3.1-8b-instant` | $0.05/$0.08 per 1M |

---

## Model Capabilities Matrix

| Model | Text | Vision | Audio | Tools | JSON | Reasoning |
|-------|------|--------|-------|-------|------|-----------|
| llama-4-scout-17b-16e | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| llama-4-maverick-17b-128e | ✅ | ✅ | ❌ | ✅ | ✅ | ✅✅ |
| llama-3.3-70b-versatile | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| llama-3.1-8b-instant | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ |
| whisper-large-v3 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| compound-beta | ✅ | ❌ | ❌ | ✅✅ | ✅ | ✅ |

---

## Rate Limits

| Tier | Requests/min | Tokens/day |
|------|--------------|------------|
| Free | 30 | 500,000 |
| Paid | 100+ | Unlimited |

---

## NO OPENAI

All models are accessed via GROQ's Python SDK:

```python
from groq import Groq  # Never: from openai import OpenAI

client = Groq(api_key="gsk_...")
```
