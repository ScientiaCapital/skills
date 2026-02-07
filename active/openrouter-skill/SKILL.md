---
name: "openrouter-skill"
description: "Orchestrate Chinese LLMs (DeepSeek, Qwen, Yi, Moonshot) through OpenRouter API with LangChain. Use when: openrouter, chinese llm, deepseek, qwen, moonshot, yi model, model routing, auto router, llm orchestration."
---

<objective>
Enable intelligent routing to Chinese/open-source LLMs through OpenRouter's unified API. Provides model selection guidance, cost optimization, and production patterns for LangChain/LangGraph integration.
</objective>

<quick_start>

## 1. Basic LangChain Setup

```python
from langchain_openai import ChatOpenAI
import os

# Any OpenRouter model works with ChatOpenAI
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-app.com",  # Optional but recommended
        "X-Title": "Your App Name"
    }
)

response = llm.invoke("Explain quantum computing in simple terms")
```

## 2. Vision Analysis (Charts, Documents)

```python
from langchain_core.messages import HumanMessage
import base64

llm = ChatOpenAI(
    model="qwen/qwen-2-vl-72b-instruct",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# From URL
response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": "Analyze this chart and identify key trends"},
        {"type": "image_url", "image_url": {"url": "https://example.com/chart.png"}}
    ])
])

# From base64
with open("chart.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": "What does this chart show?"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
    ])
])
```

## 3. Auto-Routing (Let OpenRouter Choose)

```python
# OpenRouter's Auto model selects the best model for your prompt
llm = ChatOpenAI(
    model="openrouter/auto",  # Powered by NotDiamond
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)
```

</quick_start>

<success_criteria>
- OpenRouter API key configured and authenticated
- Model selection follows the decision tree (vision -> Qwen-VL, code -> DeepSeek Coder, etc.)
- LangChain ChatOpenAI integration working with correct base URL and headers
- Cost savings of 60-97% vs Western model equivalents for comparable quality
- Fallback chain configured for production reliability
</success_criteria>

<core_concepts>

## Model Selection Decision Tree

```
Task Type
│
├─ Vision/Charts ──────────> qwen/qwen-2-vl-72b-instruct ($0.40/M)
├─ Code Generation ────────> deepseek/deepseek-coder ($0.14/$0.28)
├─ Deep Reasoning ─────────> qwen/qwq-32b ($0.15/$0.40)
├─ Long Documents ─────────> moonshot/moonshot-v1-128k ($0.55/M)
├─ Fast/Cheap Tasks ───────> qwen/qwen-2.5-7b-instruct ($0.09/M)
├─ General Analysis ───────> deepseek/deepseek-chat ($0.27/$1.10)
└─ Unknown/Auto ───────────> openrouter/auto
```

## Top Chinese LLMs

| Model | Best For | Cost ($/1M tokens) |
|-------|----------|-------------------|
| `deepseek/deepseek-chat` | General reasoning, analysis | $0.27 in / $1.10 out |
| `deepseek/deepseek-coder` | Code generation | $0.14 / $0.28 |
| `qwen/qwen-2-vl-72b-instruct` | Vision, charts | $0.40 / $0.40 |
| `qwen/qwen-2.5-7b-instruct` | Fast, cheap tasks | $0.09 / $0.09 |
| `qwen/qwq-32b` | Deep reasoning | $0.15 / $0.40 |
| `moonshot/moonshot-v1-128k` | Long context (128K) | $0.55 / $0.55 |

## Cost Comparison vs Western Models

| Task | Western Model | Cost | Chinese Model | Cost | Savings |
|------|--------------|------|---------------|------|---------|
| Chat | GPT-4o | $5.00/$15.00 | DeepSeek Chat | $0.27/$1.10 | **95%** |
| Code | Claude Sonnet | $3.00/$15.00 | DeepSeek Coder | $0.14/$0.28 | **95%** |
| Vision | GPT-4o | $5.00/$15.00 | Qwen-VL | $0.40/$0.40 | **97%** |
| Fast | GPT-4o-mini | $0.15/$0.60 | Qwen-7B | $0.09/$0.09 | **60%** |

## LangGraph Multi-Model Factory

```python
from enum import Enum
from langchain_openai import ChatOpenAI
import os

class ChineseModel(str, Enum):
    DEEPSEEK_CHAT = "deepseek/deepseek-chat"
    DEEPSEEK_CODER = "deepseek/deepseek-coder"
    QWEN_VL = "qwen/qwen-2-vl-72b-instruct"
    QWEN_FAST = "qwen/qwen-2.5-7b-instruct"
    QWQ_REASONING = "qwen/qwq-32b"
    MOONSHOT_LONG = "moonshot/moonshot-v1-128k"
    AUTO = "openrouter/auto"

def create_llm(model: ChineseModel, **kwargs) -> ChatOpenAI:
    """Factory for OpenRouter LLMs with sensible defaults."""
    return ChatOpenAI(
        model=model.value,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": os.getenv("APP_URL", "http://localhost"),
            "X-Title": os.getenv("APP_NAME", "LangChain App")
        },
        **kwargs
    )

# Usage
chat_llm = create_llm(ChineseModel.DEEPSEEK_CHAT)
vision_llm = create_llm(ChineseModel.QWEN_VL)
fast_llm = create_llm(ChineseModel.QWEN_FAST, temperature=0)
```

## Environment Setup

```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-...
APP_URL=https://your-app.com      # For attribution (optional)
APP_NAME=Your App Name            # For attribution (optional)
```

</core_concepts>

<routing>
For detailed information, see:

- `reference/models-catalog.md` - Complete model listing with capabilities
- `reference/routing-strategies.md` - Auto, provider, and custom routing
- `reference/langchain-integration.md` - LangChain/LangGraph patterns
- `reference/cost-optimization.md` - Budget management and caching
- `reference/tool-calling.md` - Function calling patterns
- `reference/multimodal.md` - Vision, PDF, audio support
- `reference/observability.md` - Monitoring and tracing
</routing>

<checklist>
When implementing OpenRouter integration:

- [ ] Set OPENROUTER_API_KEY environment variable
- [ ] Choose appropriate model for task type (see decision tree)
- [ ] Use ChatOpenAI with openai_api_base="https://openrouter.ai/api/v1"
- [ ] Add HTTP-Referer and X-Title headers for attribution
- [ ] Consider cost implications (Chinese models are 10-100x cheaper)
- [ ] Enable streaming for chat interfaces
- [ ] Implement fallback chain for production reliability
- [ ] Set up cost tracking/budget limits
</checklist>
