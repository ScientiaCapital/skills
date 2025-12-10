# Cost Optimization for LangGraph Agents

Strategies to minimize LLM costs in production agent systems.

## Provider Routing by Task Complexity

Route requests to cost-effective providers based on task difficulty:

```python
from typing import Literal

ProviderType = Literal["ollama", "deepseek", "groq", "claude-haiku", "claude-sonnet"]

class TaskRouter:
    """Route tasks to providers based on complexity and cost."""

    def __init__(self):
        self.provider_costs = {
            "ollama": 0.0,           # Free, local (Qwen, Llama)
            "groq": 0.05,            # $0.05/1M tokens (Llama 3.1)
            "deepseek": 0.14,        # $0.14/1M tokens
            "claude-haiku": 0.25,    # $0.25/1M tokens
            "claude-sonnet": 3.0,    # $3/1M tokens
        }

    def select_provider(self, complexity: int, requires_reasoning: bool) -> ProviderType:
        """Select cheapest provider for task complexity (1-10 scale)."""
        if complexity <= 3:
            return "ollama"          # Simple tasks: local models
        elif complexity <= 5:
            return "groq"            # Medium tasks: fast inference
        elif complexity <= 7:
            return "deepseek"        # Complex tasks: reasoning
        elif requires_reasoning:
            return "claude-sonnet"   # Advanced reasoning needed
        else:
            return "claude-haiku"    # General complex tasks
```

## Response Caching

Cache expensive LLM responses to avoid redundant API calls:

```python
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

class ResponseCache:
    """Cache LLM responses with TTL management."""

    def __init__(self, ttl_hours: int = 24):
        self.cache: dict[str, tuple[str, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)

    def _generate_key(self, prompt: str, provider: str, temperature: float) -> str:
        """Generate cache key from request parameters."""
        payload = f"{provider}:{temperature}:{prompt}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def get(self, prompt: str, provider: str, temperature: float) -> Optional[str]:
        """Retrieve cached response if valid."""
        key = self._generate_key(prompt, provider, temperature)
        if key in self.cache:
            response, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return response
            del self.cache[key]  # Expired
        return None

    def set(self, prompt: str, provider: str, temperature: float, response: str):
        """Cache response with timestamp."""
        key = self._generate_key(prompt, provider, temperature)
        self.cache[key] = (response, datetime.now())
```

## Token Budget Management

Enforce cost limits at agent and system levels:

```python
class CostController:
    """Track and enforce LLM cost budgets."""

    def __init__(self, daily_budget: float = 10.0, alert_threshold: float = 0.8):
        self.daily_budget = daily_budget
        self.alert_threshold = alert_threshold
        self.spent_today = 0.0
        self.agent_costs: dict[str, float] = {}

    def estimate_cost(self, tokens: int, provider: str) -> float:
        """Estimate cost for token count and provider."""
        costs_per_million = {
            "ollama": 0.0,
            "groq": 0.05,
            "deepseek": 0.14,
            "claude-haiku": 0.25,
            "claude-sonnet": 3.0,
        }
        return (tokens / 1_000_000) * costs_per_million.get(provider, 0.0)

    async def can_execute(self, agent_name: str, estimated_tokens: int, provider: str) -> bool:
        """Check if request fits within budget."""
        cost = self.estimate_cost(estimated_tokens, provider)

        if self.spent_today + cost > self.daily_budget:
            return False  # Budget exceeded

        if self.spent_today + cost > self.daily_budget * self.alert_threshold:
            print(f"⚠️ Alert: {(self.spent_today/self.daily_budget)*100:.1f}% of daily budget used")

        return True

    def record_usage(self, agent_name: str, tokens: int, provider: str):
        """Record actual token usage and cost."""
        cost = self.estimate_cost(tokens, provider)
        self.spent_today += cost
        self.agent_costs[agent_name] = self.agent_costs.get(agent_name, 0.0) + cost

    def get_report(self) -> dict:
        """Generate cost report."""
        return {
            "daily_spent": self.spent_today,
            "daily_budget": self.daily_budget,
            "utilization": f"{(self.spent_today/self.daily_budget)*100:.1f}%",
            "by_agent": self.agent_costs,
            "remaining": self.daily_budget - self.spent_today,
        }
```

## Cost Monitoring in LangGraph

Integrate cost tracking into your agent graph:

```python
from langgraph.graph import StateGraph
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama

# Provider initialization (NO OPENAI)
PROVIDERS = {
    "claude-haiku": ChatAnthropic(model="claude-3-5-haiku-20241022"),
    "claude-sonnet": ChatAnthropic(model="claude-sonnet-4-20250514"),
    "groq": ChatGroq(model="llama-3.3-70b-versatile"),
    "ollama": ChatOllama(model="qwen2.5:7b"),
}

async def call_llm(prompt: str, provider: str):
    """Call LLM by provider name."""
    llm = PROVIDERS.get(provider, PROVIDERS["claude-haiku"])
    return await llm.ainvoke([{"role": "user", "content": prompt}])

def create_cost_aware_graph(cost_controller: CostController):
    graph = StateGraph(AgentState)

    async def cost_tracked_node(state: AgentState):
        """Node wrapper with cost tracking."""
        agent_name = state["current_agent"]
        prompt = state["messages"][-1].content
        estimated_tokens = len(prompt.split()) * 1.5  # Rough estimate

        # Check budget before execution
        provider = state.get("provider", "claude-haiku")
        if not await cost_controller.can_execute(agent_name, estimated_tokens, provider):
            return {**state, "error": "Budget exceeded"}

        # Execute agent logic
        response = await call_llm(prompt, provider)

        # Record actual usage
        actual_tokens = response.usage.total_tokens
        cost_controller.record_usage(agent_name, actual_tokens, provider)

        return {**state, "messages": state["messages"] + [response]}

    return graph
```

## Best Practices

1. **Use local models for simple tasks**: Classification, extraction, templating
2. **Cache aggressively**: Identical prompts, embeddings, search results
3. **Batch requests**: Group similar tasks to reduce overhead
4. **Monitor per-agent costs**: Identify expensive agents for optimization
5. **Set hard budget limits**: Prevent runaway costs in production
6. **Use structured outputs**: Reduce token waste from retry parsing
7. **Implement fallbacks**: Downgrade to cheaper models on budget pressure
