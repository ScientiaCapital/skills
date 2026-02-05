# Cost Optimization for OpenRouter

Strategies to minimize costs while maximizing performance with Chinese LLMs.

## Cost Comparison: Chinese vs Western Models

| Task | Western Model | $/1M tokens | Chinese Model | $/1M tokens | Savings |
|------|--------------|-------------|---------------|-------------|---------|
| General Chat | GPT-4o | $5.00/$15.00 | DeepSeek Chat | $0.27/$1.10 | **95%** |
| Code Gen | Claude Sonnet 4 | $3.00/$15.00 | DeepSeek Coder | $0.14/$0.28 | **98%** |
| Vision | GPT-4o | $5.00/$15.00 | Qwen-VL-72B | $0.40/$0.40 | **97%** |
| Fast Tasks | GPT-4o-mini | $0.15/$0.60 | Qwen-7B | $0.09/$0.09 | **75%** |
| Reasoning | Claude Opus 4 | $15.00/$75.00 | QwQ-32B | $0.15/$0.40 | **99%** |
| Long Context | GPT-4-128K | $10.00/$30.00 | Moonshot-128K | $0.55/$0.55 | **98%** |

---

## Tiered Routing Strategy

Route simple tasks to cheap models, complex tasks to capable models:

```python
from enum import Enum
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
import os

class CostTier(str, Enum):
    BUDGET = "budget"      # $0.09-0.10/M - Simple tasks
    STANDARD = "standard"  # $0.27-0.35/M - General tasks
    PREMIUM = "premium"    # $0.40-0.55/M - Complex tasks
    REASONING = "reasoning"  # Variable - Hard problems

@dataclass
class TierConfig:
    model: str
    max_tokens: int
    temperature: float

TIER_CONFIGS = {
    CostTier.BUDGET: TierConfig(
        model="qwen/qwen-2.5-7b-instruct",
        max_tokens=1000,
        temperature=0.3
    ),
    CostTier.STANDARD: TierConfig(
        model="deepseek/deepseek-chat",
        max_tokens=2000,
        temperature=0.7
    ),
    CostTier.PREMIUM: TierConfig(
        model="qwen/qwen-2.5-72b-instruct",
        max_tokens=4000,
        temperature=0.7
    ),
    CostTier.REASONING: TierConfig(
        model="qwen/qwq-32b",
        max_tokens=8000,
        temperature=0.2
    ),
}

class TieredRouter:
    """Route requests to appropriate cost tier."""

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"

    def classify_complexity(self, prompt: str) -> CostTier:
        """Classify prompt complexity for routing."""
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())

        # Reasoning indicators
        reasoning_keywords = [
            "prove", "derive", "solve", "calculate", "logic",
            "step by step", "explain why", "mathematical"
        ]
        if any(kw in prompt_lower for kw in reasoning_keywords):
            return CostTier.REASONING

        # Premium indicators
        premium_keywords = [
            "analyze deeply", "comprehensive", "detailed analysis",
            "complex", "nuanced", "compare and contrast"
        ]
        if any(kw in prompt_lower for kw in premium_keywords) or word_count > 500:
            return CostTier.PREMIUM

        # Budget indicators
        budget_keywords = [
            "summarize briefly", "yes or no", "simple",
            "quick", "short answer", "tldr"
        ]
        if any(kw in prompt_lower for kw in budget_keywords) or word_count < 50:
            return CostTier.BUDGET

        return CostTier.STANDARD

    def get_llm(self, tier: CostTier) -> ChatOpenAI:
        """Get LLM for specified tier."""
        config = TIER_CONFIGS[tier]
        return ChatOpenAI(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url
        )

    def route(self, prompt: str, force_tier: CostTier = None):
        """Route prompt to appropriate tier."""
        tier = force_tier or self.classify_complexity(prompt)
        llm = self.get_llm(tier)
        return llm.invoke(prompt), tier


# Usage
router = TieredRouter()

# Auto-routing
response, tier = router.route("What is 2+2?")  # -> BUDGET
response, tier = router.route("Analyze the economic implications of AI")  # -> PREMIUM

# Force specific tier
response, _ = router.route("Hello", force_tier=CostTier.STANDARD)
```

---

## Prompt Caching

OpenRouter supports prompt caching for reduced costs on repeated prefixes:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

# Enable caching via extra headers
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    extra_body={
        "provider": {
            "allow_fallbacks": False  # Stay on same provider for cache hits
        }
    }
)

# Large system prompt gets cached after first request
SYSTEM_PROMPT = """You are an expert financial analyst...
[Large static system prompt - 2000+ tokens]
"""

def analyze_with_cached_context(query: str) -> str:
    """Query with cached system prompt."""
    return llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),  # Cached after first call
        HumanMessage(content=query)  # Only this varies
    ]).content

# First call: Full cost
# Subsequent calls: ~90% cheaper for cached prefix
result1 = analyze_with_cached_context("Analyze AAPL stock")
result2 = analyze_with_cached_context("Analyze GOOGL stock")  # Cache hit!
```

### Models with Caching Support
- DeepSeek (all models)
- Qwen (most models)
- OpenAI models via OpenRouter
- Anthropic models via OpenRouter

---

## Budget Monitoring

```python
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List
import os

@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float

@dataclass
class BudgetMonitor:
    """Track and limit API spending."""

    daily_budget: float = 10.0
    monthly_budget: float = 200.0
    alert_threshold: float = 0.8  # Alert at 80% usage

    _usage: List[UsageRecord] = field(default_factory=list)

    PRICING = {
        "qwen/qwen-2.5-7b-instruct": (0.09, 0.09),
        "deepseek/deepseek-chat": (0.27, 1.10),
        "deepseek/deepseek-coder": (0.14, 0.28),
        "qwen/qwen-2.5-72b-instruct": (0.35, 0.70),
        "qwen/qwen-2-vl-72b-instruct": (0.40, 0.40),
        "qwen/qwq-32b": (0.15, 0.40),
        "moonshot/moonshot-v1-128k": (0.55, 0.55),
    }

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a request."""
        if model not in self.PRICING:
            return 0.0  # Unknown model, can't calculate

        input_price, output_price = self.PRICING[model]
        return (
            (input_price * input_tokens / 1_000_000) +
            (output_price * output_tokens / 1_000_000)
        )

    def record_usage(self, model: str, input_tokens: int, output_tokens: int):
        """Record API usage."""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        record = UsageRecord(
            timestamp=datetime.now(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost
        )
        self._usage.append(record)

        # Check alerts
        daily = self.get_daily_spend()
        if daily >= self.daily_budget * self.alert_threshold:
            print(f"⚠️ Daily budget alert: ${daily:.4f} / ${self.daily_budget}")

    def get_daily_spend(self, target_date: date = None) -> float:
        """Get total spend for a specific day."""
        target = target_date or date.today()
        return sum(
            r.cost for r in self._usage
            if r.timestamp.date() == target
        )

    def get_monthly_spend(self) -> float:
        """Get total spend for current month."""
        now = datetime.now()
        return sum(
            r.cost for r in self._usage
            if r.timestamp.year == now.year and r.timestamp.month == now.month
        )

    def can_afford(self, estimated_tokens: int = 1000) -> bool:
        """Check if we can afford another request."""
        # Estimate using cheapest model cost
        estimated_cost = 0.09 * estimated_tokens * 2 / 1_000_000
        return self.get_daily_spend() + estimated_cost < self.daily_budget

    def get_usage_report(self) -> Dict:
        """Generate usage report."""
        today_usage = [r for r in self._usage if r.timestamp.date() == date.today()]

        model_breakdown = {}
        for record in today_usage:
            if record.model not in model_breakdown:
                model_breakdown[record.model] = {"requests": 0, "cost": 0.0}
            model_breakdown[record.model]["requests"] += 1
            model_breakdown[record.model]["cost"] += record.cost

        return {
            "daily_spend": self.get_daily_spend(),
            "daily_budget": self.daily_budget,
            "daily_remaining": self.daily_budget - self.get_daily_spend(),
            "monthly_spend": self.get_monthly_spend(),
            "monthly_budget": self.monthly_budget,
            "model_breakdown": model_breakdown
        }


# Usage
monitor = BudgetMonitor(daily_budget=5.0)

# After each API call
monitor.record_usage("deepseek/deepseek-chat", input_tokens=500, output_tokens=1000)

# Check before expensive operation
if monitor.can_afford(estimated_tokens=5000):
    # proceed with request
    pass

# Get report
report = monitor.get_usage_report()
print(f"Daily spend: ${report['daily_spend']:.4f} / ${report['daily_budget']}")
```

---

## Token Optimization

### Prompt Compression

```python
from langchain_core.messages import HumanMessage, SystemMessage

def compress_prompt(prompt: str, max_chars: int = 2000) -> str:
    """Compress prompt while preserving meaning."""
    if len(prompt) <= max_chars:
        return prompt

    # Remove extra whitespace
    prompt = " ".join(prompt.split())

    # Truncate with indicator
    if len(prompt) > max_chars:
        return prompt[:max_chars-50] + "\n\n[Content truncated for brevity]"

    return prompt

def efficient_system_prompt(base_prompt: str) -> str:
    """Create token-efficient system prompt."""
    # Remove verbose phrases
    replacements = [
        ("I want you to", ""),
        ("Please", ""),
        ("Could you", ""),
        ("I would like you to", ""),
        ("It's important that", ""),
    ]

    result = base_prompt
    for old, new in replacements:
        result = result.replace(old, new)

    return result.strip()
```

### Response Length Control

```python
from langchain_openai import ChatOpenAI

# Control output length for cost savings
cheap_llm = ChatOpenAI(
    model="qwen/qwen-2.5-7b-instruct",
    max_tokens=500,  # Limit output
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Add explicit length instruction
response = cheap_llm.invoke(
    "Summarize this article in 2-3 sentences: [article text]"
)
```

---

## Response Caching

Cache responses to avoid duplicate API calls:

```python
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta

class ResponseCache:
    """File-based cache for LLM responses."""

    def __init__(self, cache_dir: str = ".llm_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_key(self, model: str, prompt: str) -> str:
        """Generate cache key."""
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get(self, model: str, prompt: str) -> str | None:
        """Get cached response if valid."""
        key = self._get_key(model, prompt)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        data = json.loads(cache_file.read_text())
        cached_time = datetime.fromisoformat(data["timestamp"])

        if datetime.now() - cached_time > self.ttl:
            cache_file.unlink()  # Expired
            return None

        return data["response"]

    def set(self, model: str, prompt: str, response: str):
        """Cache a response."""
        key = self._get_key(model, prompt)
        cache_file = self.cache_dir / f"{key}.json"

        data = {
            "model": model,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        cache_file.write_text(json.dumps(data))


def cached_invoke(llm, prompt: str, cache: ResponseCache) -> str:
    """Invoke LLM with caching."""
    model = llm.model_name

    # Check cache
    cached = cache.get(model, prompt)
    if cached:
        return cached

    # Call API
    response = llm.invoke(prompt).content

    # Cache result
    cache.set(model, prompt, response)

    return response


# Usage
cache = ResponseCache(ttl_hours=48)
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# First call: API request
response1 = cached_invoke(llm, "What is Python?", cache)

# Second call: Cache hit (free!)
response2 = cached_invoke(llm, "What is Python?", cache)
```

---

## Cost Optimization Checklist

1. **Model Selection**
   - [ ] Use cheapest model that meets quality requirements
   - [ ] Reserve premium models for complex tasks
   - [ ] Consider free tiers for development/testing

2. **Request Optimization**
   - [ ] Compress long prompts
   - [ ] Set appropriate max_tokens
   - [ ] Use efficient system prompts
   - [ ] Batch similar requests

3. **Caching**
   - [ ] Enable provider-side prompt caching
   - [ ] Implement response caching for repeated queries
   - [ ] Cache static context separately

4. **Monitoring**
   - [ ] Track daily/monthly spend
   - [ ] Set budget alerts
   - [ ] Monitor per-model costs
   - [ ] Review usage patterns weekly

5. **Architecture**
   - [ ] Implement tiered routing
   - [ ] Use fast models for classification/routing
   - [ ] Only call expensive models when necessary
