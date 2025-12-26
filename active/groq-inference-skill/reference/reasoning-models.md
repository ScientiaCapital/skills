# GROQ Reasoning Models

Complete guide for GROQ's reasoning-capable models with extended thinking.

---

## Supported Reasoning Models

| Model | Use Case |
|-------|----------|
| `meta-llama/llama-4-maverick-17b-128e-instruct` | Complex reasoning, thinking models |
| `qwen/qwen3-32b` | Structured reasoning, multilingual |

---

## Configuration Parameters

### reasoning_format

Controls how reasoning is returned in the response.

| Value | Behavior | Use Case |
|-------|----------|----------|
| `"parsed"` | Reasoning in `message.reasoning` field | Debugging, analysis |
| `"raw"` | Reasoning in `<think>` tags in content | Full transparency |
| `"hidden"` | Only final answer, no reasoning | Production, end-users |

---

## Examples

### Parsed Format with Separate Reasoning

```python
from groq import Groq

client = Groq(api_key="gsk_...")

response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {"role": "user", "content": "How many r's in strawberry?"}
    ],
    reasoning_format="parsed"
)

msg = response.choices[0].message

# Access reasoning separately
if hasattr(msg, 'reasoning') and msg.reasoning:
    print("Thinking:", msg.reasoning)

print("Answer:", msg.content)
```

### Hidden Format for Production

```python
# User-facing response - hide reasoning process
response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[{"role": "user", "content": "Recommend a laptop under $2000"}],
    reasoning_format="hidden"  # Only final answer
)

print(response.choices[0].message.content)
```

### Raw Format with <think> Tags

```python
response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[{"role": "user", "content": "Solve: 15% of 240"}],
    reasoning_format="raw"
)

# Reasoning embedded in content with <think> tags
content = response.choices[0].message.content
print(content)
```

**Output:**
```
<think>
15% of 240 means 15/100 × 240 = 0.15 × 240 = 36
</think>

15% of 240 is 36.
```

---

## Streaming with Reasoning

```python
stream = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[{"role": "user", "content": "Analyze this problem"}],
    reasoning_format="raw",  # Best for streaming
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## Best Practices

1. **Development:** Use `reasoning_format="parsed"` for debugging
2. **Production:** Use `reasoning_format="hidden"` to save tokens
3. **Complex Problems:** Reasoning models excel at multi-step analysis
4. **Simple Tasks:** Use non-reasoning models (llama-3.3-70b) for cost efficiency

---

## When to Use Reasoning Models

| Task Type | Use Reasoning? |
|-----------|---------------|
| Math problems | ✅ Yes |
| Logic puzzles | ✅ Yes |
| Step-by-step analysis | ✅ Yes |
| Simple Q&A | ❌ No (use llama-3.3-70b) |
| Classification | ❌ No (use llama-3.1-8b) |

---

## NO OPENAI

```python
from groq import Groq  # Never: from openai import OpenAI
```
