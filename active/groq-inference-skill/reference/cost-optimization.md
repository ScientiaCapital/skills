# GROQ Cost Optimization

Complete guide for optimizing GROQ inference costs.

---

## Pricing Matrix (December 2025)

### Text Models

| Model | Input ($/1M) | Output ($/1M) | Use Case |
|-------|--------------|---------------|----------|
| llama-3.3-70b-versatile | $0.59 | $0.79 | General purpose |
| llama-3.1-8b-instant | $0.05 | $0.08 | Simple tasks, fastest |
| llama-3.1-70b-versatile | $0.59 | $0.79 | General purpose |
| gemma2-9b-it | $0.20 | $0.20 | Instruction following |

### Speech Models

| Model | Pricing | Use Case |
|-------|---------|----------|
| whisper-large-v3 | $0.111/hour | High accuracy |
| whisper-large-v3-turbo | $0.04/hour | Fast transcription |

---

## Strategy 1: Model Selection by Task

```python
def select_model(task_type: str, complexity: str):
    """Route to cost-optimal model"""

    if task_type == "classification":
        return "llama-3.1-8b-instant"  # $0.05/$0.08

    if task_type == "summarization":
        return "llama-3.1-8b-instant"  # $0.05/$0.08

    if task_type == "reasoning":
        return "llama-3.3-70b-versatile"  # $0.59/$0.79

    # Default
    return "llama-3.1-8b-instant"
```

---

## Strategy 2: Response Caching

```python
import hashlib

response_cache = {}

def cached_completion(prompt: str, model: str = "llama-3.1-8b-instant"):
    """Cache responses for identical prompts"""

    cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

    if cache_key in response_cache:
        return response_cache[cache_key]  # Free!

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    response_cache[cache_key] = result

    return result
```

---

## Strategy 3: Context Truncation

```python
def truncate_context(messages: list, max_tokens: int = 4000):
    """Keep context under limit to avoid high token costs"""

    def estimate_tokens(text: str):
        return len(text) // 4

    total_tokens = sum(estimate_tokens(m["content"]) for m in messages)

    if total_tokens > max_tokens:
        system = [m for m in messages if m["role"] == "system"]
        recent = messages[-5:]
        return system + recent

    return messages
```

---

## Strategy 4: Provider Routing

Route to GROQ for speed, Claude for quality (NO OpenAI).

```python
from groq import Groq
from anthropic import Anthropic

groq_client = Groq(api_key="gsk_...")
claude_client = Anthropic(api_key="sk-ant-...")

def smart_route(prompt: str, priority: str):
    """Route to GROQ for speed, Claude for quality"""

    if priority == "speed":
        return groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content

    elif priority == "quality":
        return claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

    # Balanced
    return groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
```

---

## Strategy 5: Whisper Cost Optimization

```python
def transcribe_cost_effective(audio_file: str, language: str = None):
    """Use appropriate Whisper model for cost/speed trade-off"""

    # Fast transcription needed
    if need_speed:
        model = "whisper-large-v3-turbo"  # $0.04/hr
    else:
        model = "whisper-large-v3"        # $0.111/hr

    with open(audio_file, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model=model,
            file=f,
            language=language
        )

    return transcription.text
```

---

## Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.total_cost = 0.0
        self.pricing = {
            "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
            "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        }

    def track(self, response, model: str):
        usage = response.usage
        input_cost = (usage.prompt_tokens / 1_000_000) * self.pricing[model]["input"]
        output_cost = (usage.completion_tokens / 1_000_000) * self.pricing[model]["output"]
        self.total_cost += (input_cost + output_cost)
        return {"cost": input_cost + output_cost}

    def report(self):
        return f"Total cost: ${self.total_cost:.4f}"
```

---

## Summary: Cost Hierarchy

| Strategy | Savings | Effort |
|----------|---------|--------|
| Model selection (8b vs 70b) | 90% | Low |
| Response caching | Up to 100% | Medium |
| Context truncation | 30-50% | Low |
| Provider routing | Variable | High |

---

## NO OPENAI

```python
from groq import Groq       # Speed
from anthropic import Anthropic  # Quality

# NEVER:
# from openai import OpenAI  ❌
```
