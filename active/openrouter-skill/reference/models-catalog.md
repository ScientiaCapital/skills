# OpenRouter Chinese LLM Catalog

Complete reference for Chinese and open-source models available through OpenRouter.

## DeepSeek Family

### deepseek/deepseek-chat (V3)
- **Best For**: General reasoning, analysis, conversations
- **Context**: 64K tokens
- **Cost**: $0.27/$1.10 per 1M tokens (input/output)
- **Capabilities**: Text, tool calling, JSON mode
- **Notes**: Best general-purpose Chinese model, comparable to GPT-4

### deepseek/deepseek-coder
- **Best For**: Code generation, debugging, technical docs
- **Context**: 128K tokens
- **Cost**: $0.14/$0.28 per 1M tokens
- **Capabilities**: Text, code specialist
- **Notes**: Trained specifically on code, excellent for programming tasks

### deepseek/deepseek-r1
- **Best For**: Complex reasoning, math, logic problems
- **Context**: 64K tokens
- **Cost**: $0.55/$2.19 per 1M tokens
- **Capabilities**: Reasoning traces, extended thinking
- **Notes**: Shows reasoning process, best for hard problems

### deepseek/deepseek-r1-distill-qwen-32b
- **Best For**: Reasoning at lower cost
- **Context**: 64K tokens
- **Cost**: $0.15/$0.40 per 1M tokens
- **Capabilities**: Reasoning, distilled from R1
- **Notes**: Good balance of reasoning ability and cost

---

## Qwen Family (Alibaba)

### qwen/qwen-2.5-72b-instruct
- **Best For**: Complex analysis, long documents
- **Context**: 128K tokens
- **Cost**: $0.35/$0.70 per 1M tokens
- **Capabilities**: Text, tool calling, JSON mode
- **Notes**: Alibaba's flagship text model

### qwen/qwen-2.5-7b-instruct
- **Best For**: Fast, cheap tasks, high throughput
- **Context**: 32K tokens
- **Cost**: $0.09/$0.09 per 1M tokens
- **Capabilities**: Text, tool calling
- **Notes**: Best value for simple tasks

### qwen/qwen-2-vl-72b-instruct
- **Best For**: Vision tasks, charts, documents
- **Context**: 32K tokens
- **Cost**: $0.40/$0.40 per 1M tokens
- **Capabilities**: Vision, text, image analysis
- **Notes**: Excellent for chart interpretation, document analysis

### qwen/qwen3-vl-30b
- **Best For**: Vision tasks at lower cost
- **Context**: 32K tokens
- **Cost**: $0.08/$0.50 per 1M tokens
- **Capabilities**: Vision, text
- **Notes**: Newer vision model, good price/performance

### qwen/qwq-32b
- **Best For**: Deep reasoning, complex problems
- **Context**: 32K tokens
- **Cost**: $0.15/$0.40 per 1M tokens
- **Capabilities**: Reasoning traces (thinking model)
- **Notes**: Shows reasoning process like o1, excellent for math/logic

---

## Other Chinese Models

### moonshot/moonshot-v1-128k
- **Best For**: Very long documents, book analysis
- **Context**: 128K tokens
- **Cost**: $0.55/$0.55 per 1M tokens
- **Capabilities**: Text, ultra-long context
- **Notes**: Best for documents that need full context

### yi/yi-lightning
- **Best For**: Fast inference, simple tasks
- **Context**: 16K tokens
- **Cost**: $0.10/$0.10 per 1M tokens
- **Capabilities**: Text
- **Notes**: 01.AI's fast model, good for high-throughput

### zhipu/glm-4-plus
- **Best For**: Chinese language tasks
- **Context**: 128K tokens
- **Cost**: $0.50/$0.50 per 1M tokens
- **Capabilities**: Text, Chinese-optimized
- **Notes**: Strong for Chinese content generation

---

## Model Variants

OpenRouter offers several model variants:

| Suffix | Description | Example |
|--------|-------------|---------|
| `:free` | Free tier (rate limited) | `deepseek/deepseek-chat:free` |
| `:nitro` | Faster inference | `qwen/qwen-2.5-72b-instruct:nitro` |
| `:extended` | Extended context | Model-specific |
| `:online` | Web search enabled | Provider-specific |

---

## Capabilities Matrix

| Model | Text | Vision | Tools | JSON | Reasoning | Long Context |
|-------|------|--------|-------|------|-----------|--------------|
| deepseek-chat | ✅ | ❌ | ✅ | ✅ | ⭐ | 64K |
| deepseek-coder | ✅ | ❌ | ✅ | ✅ | ⭐ | 128K |
| deepseek-r1 | ✅ | ❌ | ❌ | ✅ | ⭐⭐⭐ | 64K |
| qwen-2.5-72b | ✅ | ❌ | ✅ | ✅ | ⭐⭐ | 128K |
| qwen-2.5-7b | ✅ | ❌ | ✅ | ✅ | ⭐ | 32K |
| qwen-2-vl-72b | ✅ | ✅ | ✅ | ✅ | ⭐⭐ | 32K |
| qwq-32b | ✅ | ❌ | ❌ | ✅ | ⭐⭐⭐ | 32K |
| moonshot-128k | ✅ | ❌ | ❌ | ❌ | ⭐ | 128K |

Legend: ⭐ = Basic, ⭐⭐ = Good, ⭐⭐⭐ = Excellent

---

## Model Selection by Task

```python
MODEL_BY_TASK = {
    # Text tasks
    "chat": "deepseek/deepseek-chat",
    "analysis": "deepseek/deepseek-chat",
    "summarization": "qwen/qwen-2.5-7b-instruct",

    # Code tasks
    "code_generation": "deepseek/deepseek-coder",
    "code_review": "deepseek/deepseek-coder",
    "debugging": "deepseek/deepseek-coder",

    # Reasoning tasks
    "math": "qwen/qwq-32b",
    "logic": "qwen/qwq-32b",
    "complex_reasoning": "deepseek/deepseek-r1",

    # Vision tasks
    "image_analysis": "qwen/qwen-2-vl-72b-instruct",
    "chart_reading": "qwen/qwen-2-vl-72b-instruct",
    "document_ocr": "qwen/qwen-2-vl-72b-instruct",

    # Long context
    "long_document": "moonshot/moonshot-v1-128k",
    "book_analysis": "moonshot/moonshot-v1-128k",

    # High throughput
    "batch_processing": "qwen/qwen-2.5-7b-instruct",
    "simple_classification": "yi/yi-lightning",

    # Unknown
    "auto": "openrouter/auto",
}
```

---

## Pricing Quick Reference

| Tier | Models | Input Cost | Output Cost | Use Case |
|------|--------|------------|-------------|----------|
| **Budget** | qwen-2.5-7b, yi-lightning | $0.09-0.10 | $0.09-0.10 | Simple tasks, high volume |
| **Standard** | deepseek-chat, qwen-2.5-72b | $0.27-0.35 | $0.70-1.10 | General analysis |
| **Vision** | qwen-2-vl-72b | $0.40 | $0.40 | Image/chart analysis |
| **Reasoning** | qwq-32b, deepseek-r1 | $0.15-0.55 | $0.40-2.19 | Complex problems |
| **Long Context** | moonshot-128k | $0.55 | $0.55 | Full document analysis |

---

## Getting Model Info via API

```python
import httpx

# List all models
response = httpx.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)
models = response.json()["data"]

# Filter Chinese models
chinese_providers = ["deepseek", "qwen", "moonshot", "yi", "zhipu", "glm"]
chinese_models = [
    m for m in models
    if any(p in m["id"] for p in chinese_providers)
]

for model in chinese_models:
    print(f"{model['id']}: ${model['pricing']['prompt']}/1K input")
```
