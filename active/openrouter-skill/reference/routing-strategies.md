# OpenRouter Routing Strategies

Patterns for intelligent model routing across Chinese LLMs.

## Auto Router

OpenRouter's auto router automatically selects the best model for your prompt:

```python
from langchain_openai import ChatOpenAI

# Let OpenRouter choose (powered by NotDiamond)
llm = ChatOpenAI(
    model="openrouter/auto",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# The response headers include which model was used
# Access via callbacks or response metadata
```

### When to Use Auto Router
- Uncertain about best model for task
- Prototyping and testing
- Variable input types
- Want automatic optimization

### Auto Router Limitations
- Less predictable costs
- May not always pick Chinese models
- No control over model selection

---

## Provider Routing (Extra Body)

Control routing behavior with provider preferences:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    extra_body={
        "provider": {
            # Preferred providers (in order)
            "order": ["DeepSeek", "Together", "Fireworks"],

            # Allow fallback to other providers
            "allow_fallbacks": True,

            # Require model to support these features
            "require_parameters": True,

            # Quantization preferences
            "quantizations": ["bf16", "fp16"],  # Prefer high precision

            # Data policies
            "data_collection": "deny"  # Opt out of training
        }
    }
)
```

### Provider Preferences Options

| Option | Values | Description |
|--------|--------|-------------|
| `order` | Provider names | Preferred provider order |
| `allow_fallbacks` | boolean | Fall back if preferred unavailable |
| `require_parameters` | boolean | Require exact parameter support |
| `quantizations` | list | Acceptable quantization levels |
| `data_collection` | "allow"/"deny" | Data training consent |

---

## Model Fallbacks

Configure automatic failover for reliability:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    extra_body={
        "route": "fallback",
        "models": [
            "deepseek/deepseek-chat",      # Primary
            "qwen/qwen-2.5-72b-instruct",  # First fallback
            "qwen/qwen-2.5-7b-instruct"    # Last resort
        ]
    }
)
```

---

## Custom Task-Based Router

Build your own routing logic:

```python
from enum import Enum
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

class TaskType(str, Enum):
    CHAT = "chat"
    CODE = "code"
    VISION = "vision"
    REASONING = "reasoning"
    LONG_CONTEXT = "long_context"
    FAST = "fast"

class ChineseModelRouter:
    """Routes to optimal Chinese LLM based on task type."""

    TASK_TO_MODEL = {
        TaskType.CHAT: "deepseek/deepseek-chat",
        TaskType.CODE: "deepseek/deepseek-coder",
        TaskType.VISION: "qwen/qwen-2-vl-72b-instruct",
        TaskType.REASONING: "qwen/qwq-32b",
        TaskType.LONG_CONTEXT: "moonshot/moonshot-v1-128k",
        TaskType.FAST: "qwen/qwen-2.5-7b-instruct",
    }

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self._llm_cache = {}

    def get_llm(self, task: TaskType, **kwargs) -> ChatOpenAI:
        """Get LLM for task type with caching."""
        model = self.TASK_TO_MODEL[task]

        cache_key = (model, frozenset(kwargs.items()))
        if cache_key not in self._llm_cache:
            self._llm_cache[cache_key] = ChatOpenAI(
                model=model,
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                **kwargs
            )
        return self._llm_cache[cache_key]

    def detect_task(self, message: str, has_image: bool = False) -> TaskType:
        """Simple task detection heuristic."""
        message_lower = message.lower()

        if has_image:
            return TaskType.VISION

        code_keywords = ["code", "function", "class", "debug", "implement", "python", "javascript"]
        if any(kw in message_lower for kw in code_keywords):
            return TaskType.CODE

        reasoning_keywords = ["prove", "solve", "calculate", "math", "logic", "why"]
        if any(kw in message_lower for kw in reasoning_keywords):
            return TaskType.REASONING

        if len(message) > 10000:  # Long input
            return TaskType.LONG_CONTEXT

        return TaskType.CHAT

    def route(self, message: str, has_image: bool = False, **kwargs):
        """Auto-route message to appropriate model."""
        task = self.detect_task(message, has_image)
        llm = self.get_llm(task, **kwargs)
        return llm.invoke(message)


# Usage
router = ChineseModelRouter()

# Auto-routing
response = router.route("Explain recursion in Python")  # -> deepseek-coder
response = router.route("What is 2+2?")  # -> qwq-32b (reasoning)
response = router.route("Hello, how are you?")  # -> deepseek-chat

# Explicit routing
code_llm = router.get_llm(TaskType.CODE)
vision_llm = router.get_llm(TaskType.VISION)
```

---

## Cost-Aware Router

Route based on budget constraints:

```python
from dataclasses import dataclass
from typing import Dict
import os

@dataclass
class ModelCost:
    input_per_million: float
    output_per_million: float

    @property
    def avg_cost(self) -> float:
        return (self.input_per_million + self.output_per_million) / 2

class CostAwareRouter:
    """Routes to models based on budget constraints."""

    COSTS: Dict[str, ModelCost] = {
        # Budget tier
        "qwen/qwen-2.5-7b-instruct": ModelCost(0.09, 0.09),
        "yi/yi-lightning": ModelCost(0.10, 0.10),

        # Standard tier
        "deepseek/deepseek-chat": ModelCost(0.27, 1.10),
        "deepseek/deepseek-coder": ModelCost(0.14, 0.28),
        "qwen/qwen-2.5-72b-instruct": ModelCost(0.35, 0.70),

        # Premium tier
        "qwen/qwen-2-vl-72b-instruct": ModelCost(0.40, 0.40),
        "qwen/qwq-32b": ModelCost(0.15, 0.40),
        "moonshot/moonshot-v1-128k": ModelCost(0.55, 0.55),
        "deepseek/deepseek-r1": ModelCost(0.55, 2.19),
    }

    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.spent_today = 0.0

    def get_model_for_budget(
        self,
        preferred: str,
        estimated_tokens: int = 1000
    ) -> str:
        """Get best model within budget constraints."""
        budget_remaining = self.daily_budget - self.spent_today

        # If budget low, force cheapest model
        if budget_remaining < 1.0:
            return "qwen/qwen-2.5-7b-instruct"

        # Calculate estimated cost for preferred model
        if preferred in self.COSTS:
            cost = self.COSTS[preferred]
            estimated_cost = (
                (cost.input_per_million * estimated_tokens / 1_000_000) +
                (cost.output_per_million * estimated_tokens / 1_000_000)
            )

            if estimated_cost < budget_remaining * 0.1:  # Use max 10% per request
                return preferred

        # Fall back to cheaper alternative
        sorted_by_cost = sorted(
            self.COSTS.items(),
            key=lambda x: x[1].avg_cost
        )
        return sorted_by_cost[0][0]

    def track_usage(self, model: str, input_tokens: int, output_tokens: int):
        """Track actual usage for budget management."""
        if model in self.COSTS:
            cost = self.COSTS[model]
            actual_cost = (
                (cost.input_per_million * input_tokens / 1_000_000) +
                (cost.output_per_million * output_tokens / 1_000_000)
            )
            self.spent_today += actual_cost


# Usage
cost_router = CostAwareRouter(daily_budget=5.0)

# Get model within budget
model = cost_router.get_model_for_budget(
    preferred="deepseek/deepseek-chat",
    estimated_tokens=2000
)

# Track after use
cost_router.track_usage(model, input_tokens=500, output_tokens=1500)
```

---

## LangGraph Router Node

Integrate routing into LangGraph workflows:

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class RouterState(TypedDict):
    message: str
    has_image: bool
    model: str
    response: str

def route_node(state: RouterState) -> RouterState:
    """Route to appropriate model."""
    router = ChineseModelRouter()
    task = router.detect_task(state["message"], state["has_image"])
    return {"model": router.TASK_TO_MODEL[task]}

def execute_node(state: RouterState) -> RouterState:
    """Execute with selected model."""
    llm = ChatOpenAI(
        model=state["model"],
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    response = llm.invoke(state["message"])
    return {"response": response.content}

# Build graph
graph = StateGraph(RouterState)
graph.add_node("route", route_node)
graph.add_node("execute", execute_node)
graph.add_edge("route", "execute")
graph.add_edge("execute", END)
graph.set_entry_point("route")

chain = graph.compile()

# Run
result = chain.invoke({
    "message": "Write a Python function to sort a list",
    "has_image": False
})
print(f"Model used: {result['model']}")
print(f"Response: {result['response']}")
```

---

## Routing Best Practices

1. **Cache LLM instances** - Don't recreate for every request
2. **Use fallbacks in production** - Always have a backup model
3. **Track costs** - Monitor budget to avoid surprises
4. **Test routing logic** - Ensure tasks route correctly
5. **Log model selection** - Debug routing decisions
6. **Set timeouts** - Different models have different latencies
