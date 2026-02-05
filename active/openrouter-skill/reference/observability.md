# Observability for OpenRouter

Monitoring, logging, and tracing patterns for Chinese LLM deployments.

## OpenRouter Broadcast Connections

OpenRouter can automatically forward telemetry to observability platforms:

### Langfuse Integration

```bash
# Configure in OpenRouter dashboard
# Settings > Broadcast Connections > Add Langfuse

# Or via API headers
```

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        # Langfuse will receive traces via OpenRouter broadcast
        "X-Title": "Production App"
    }
)
```

### Direct Langfuse Integration

For more control, integrate Langfuse directly:

```python
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI
import os

# Langfuse callback handler
langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Use with callbacks
response = llm.invoke(
    "Hello, world!",
    config={"callbacks": [langfuse_handler]}
)

# Trace will include:
# - Model used
# - Token counts
# - Latency
# - Input/output
```

### With Tracing Context

```python
from langfuse.callback import CallbackHandler

def traced_invoke(
    llm,
    prompt: str,
    trace_name: str,
    user_id: str = None,
    metadata: dict = None
) -> str:
    """Invoke LLM with full tracing context."""

    handler = CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        trace_name=trace_name,
        user_id=user_id,
        metadata=metadata or {}
    )

    response = llm.invoke(prompt, config={"callbacks": [handler]})

    # Flush to ensure trace is sent
    handler.flush()

    return response.content


# Usage with context
result = traced_invoke(
    llm,
    "Explain recursion",
    trace_name="explain-concept",
    user_id="user-123",
    metadata={"feature": "education", "difficulty": "beginner"}
)
```

---

## Cost Tracking

### Token-Based Cost Tracking

```python
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class UsageEvent:
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float

class CostTrackingHandler(BaseCallbackHandler):
    """Track costs across all LLM calls."""

    PRICING = {
        "deepseek/deepseek-chat": (0.27, 1.10),  # per million
        "deepseek/deepseek-coder": (0.14, 0.28),
        "qwen/qwen-2.5-7b-instruct": (0.09, 0.09),
        "qwen/qwen-2.5-72b-instruct": (0.35, 0.70),
        "qwen/qwen-2-vl-72b-instruct": (0.40, 0.40),
        "qwen/qwq-32b": (0.15, 0.40),
    }

    def __init__(self):
        self.events = []

    def on_llm_end(self, response, **kwargs):
        """Called when LLM completes."""
        # Extract token usage from response
        if hasattr(response, 'llm_output') and response.llm_output:
            usage = response.llm_output.get('token_usage', {})
            model = response.llm_output.get('model_name', 'unknown')

            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)

            # Calculate cost
            cost = self._calculate_cost(model, prompt_tokens, completion_tokens)

            event = UsageEvent(
                timestamp=datetime.now(),
                model=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                estimated_cost=cost
            )
            self.events.append(event)

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        if model not in self.PRICING:
            return 0.0
        input_price, output_price = self.PRICING[model]
        return (
            (input_price * prompt_tokens / 1_000_000) +
            (output_price * completion_tokens / 1_000_000)
        )

    def get_total_cost(self) -> float:
        return sum(e.estimated_cost for e in self.events)

    def get_summary(self) -> dict:
        return {
            "total_requests": len(self.events),
            "total_tokens": sum(e.total_tokens for e in self.events),
            "total_cost": self.get_total_cost(),
            "by_model": self._group_by_model()
        }

    def _group_by_model(self) -> dict:
        result = {}
        for event in self.events:
            if event.model not in result:
                result[event.model] = {"requests": 0, "tokens": 0, "cost": 0.0}
            result[event.model]["requests"] += 1
            result[event.model]["tokens"] += event.total_tokens
            result[event.model]["cost"] += event.estimated_cost
        return result


# Usage
cost_handler = CostTrackingHandler()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Make some calls
response = llm.invoke("Hello", config={"callbacks": [cost_handler]})
response = llm.invoke("Explain Python", config={"callbacks": [cost_handler]})

# Check costs
summary = cost_handler.get_summary()
print(f"Total cost: ${summary['total_cost']:.4f}")
print(f"Total tokens: {summary['total_tokens']}")
```

---

## Structured Logging

### JSON Logging Pattern

```python
import logging
import json
from datetime import datetime
from typing import Any

class StructuredLogger:
    """Structured JSON logging for LLM interactions."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, event: str, **data: Any):
        """Log structured event."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            **data
        }
        self.logger.info(json.dumps(log_entry))

    def log_request(
        self,
        model: str,
        prompt_preview: str,
        tokens_estimate: int
    ):
        """Log LLM request."""
        self.log(
            "llm_request",
            model=model,
            prompt_preview=prompt_preview[:100],
            tokens_estimate=tokens_estimate
        )

    def log_response(
        self,
        model: str,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float
    ):
        """Log LLM response."""
        self.log(
            "llm_response",
            model=model,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost
        )

    def log_error(self, model: str, error: str, **context):
        """Log LLM error."""
        self.log(
            "llm_error",
            model=model,
            error=error,
            **context
        )


# Usage
logger = StructuredLogger("openrouter")

logger.log_request(
    model="deepseek/deepseek-chat",
    prompt_preview="Explain quantum computing...",
    tokens_estimate=500
)

logger.log_response(
    model="deepseek/deepseek-chat",
    latency_ms=1234.5,
    prompt_tokens=100,
    completion_tokens=400,
    cost=0.00047
)
```

---

## Performance Metrics

### Latency Tracking

```python
import time
from dataclasses import dataclass, field
from statistics import mean, median, stdev
from typing import List

@dataclass
class LatencyTracker:
    """Track latency metrics for LLM calls."""

    measurements: List[float] = field(default_factory=list)

    def record(self, latency_ms: float):
        """Record a latency measurement."""
        self.measurements.append(latency_ms)

    def get_stats(self) -> dict:
        """Get latency statistics."""
        if not self.measurements:
            return {}

        return {
            "count": len(self.measurements),
            "mean_ms": mean(self.measurements),
            "median_ms": median(self.measurements),
            "min_ms": min(self.measurements),
            "max_ms": max(self.measurements),
            "stdev_ms": stdev(self.measurements) if len(self.measurements) > 1 else 0,
            "p95_ms": sorted(self.measurements)[int(len(self.measurements) * 0.95)] if len(self.measurements) >= 20 else None,
            "p99_ms": sorted(self.measurements)[int(len(self.measurements) * 0.99)] if len(self.measurements) >= 100 else None,
        }


def timed_invoke(llm, prompt: str, tracker: LatencyTracker) -> tuple[str, float]:
    """Invoke LLM and track latency."""
    start = time.perf_counter()
    response = llm.invoke(prompt)
    latency_ms = (time.perf_counter() - start) * 1000

    tracker.record(latency_ms)

    return response.content, latency_ms


# Usage
tracker = LatencyTracker()

for i in range(10):
    response, latency = timed_invoke(llm, f"Question {i}", tracker)
    print(f"Request {i}: {latency:.1f}ms")

stats = tracker.get_stats()
print(f"Average latency: {stats['mean_ms']:.1f}ms")
print(f"P95 latency: {stats['p95_ms']:.1f}ms" if stats['p95_ms'] else "")
```

---

## Alerting

### Budget Alerts

```python
from dataclasses import dataclass
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

@dataclass
class AlertConfig:
    daily_budget: float = 10.0
    warning_threshold: float = 0.8  # Alert at 80%
    critical_threshold: float = 0.95  # Alert at 95%
    email_to: str = None

class BudgetAlertManager:
    """Manage budget alerts."""

    def __init__(self, config: AlertConfig):
        self.config = config
        self.alerts_sent = set()

    def check_budget(self, current_spend: float):
        """Check if budget alert should be triggered."""
        budget = self.config.daily_budget

        if current_spend >= budget * self.config.critical_threshold:
            self._send_alert("CRITICAL", current_spend, budget)
        elif current_spend >= budget * self.config.warning_threshold:
            self._send_alert("WARNING", current_spend, budget)

    def _send_alert(self, level: str, spend: float, budget: float):
        """Send alert (deduplicated)."""
        alert_key = f"{level}-{datetime.now().date()}"

        if alert_key in self.alerts_sent:
            return

        self.alerts_sent.add(alert_key)

        message = f"""
{level}: OpenRouter Budget Alert

Current spend: ${spend:.2f}
Daily budget: ${budget:.2f}
Usage: {spend/budget*100:.1f}%

Time: {datetime.now().isoformat()}
"""
        print(message)  # Log to console

        # Send email if configured
        if self.config.email_to:
            self._send_email(level, message)

    def _send_email(self, level: str, message: str):
        """Send email alert."""
        # Implement email sending
        pass


# Usage
alert_manager = BudgetAlertManager(AlertConfig(
    daily_budget=10.0,
    warning_threshold=0.8,
    email_to="alerts@example.com"
))

# After each API call
alert_manager.check_budget(current_spend=8.50)  # 85% - triggers WARNING
```

---

## Dashboard Metrics

### Metrics for Grafana/Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
llm_requests_total = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status']
)

llm_latency_seconds = Histogram(
    'llm_latency_seconds',
    'LLM request latency',
    ['model'],
    buckets=[0.5, 1, 2, 5, 10, 30, 60]
)

llm_tokens_total = Counter(
    'llm_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: prompt or completion
)

llm_cost_dollars = Counter(
    'llm_cost_dollars',
    'Total cost in dollars',
    ['model']
)

llm_daily_budget_remaining = Gauge(
    'llm_daily_budget_remaining',
    'Remaining daily budget in dollars'
)

def record_llm_metrics(
    model: str,
    latency_seconds: float,
    prompt_tokens: int,
    completion_tokens: int,
    cost: float,
    success: bool = True
):
    """Record metrics after LLM call."""
    status = "success" if success else "error"

    llm_requests_total.labels(model=model, status=status).inc()
    llm_latency_seconds.labels(model=model).observe(latency_seconds)
    llm_tokens_total.labels(model=model, type="prompt").inc(prompt_tokens)
    llm_tokens_total.labels(model=model, type="completion").inc(completion_tokens)
    llm_cost_dollars.labels(model=model).inc(cost)

# Start metrics server
start_http_server(8000)  # Metrics at http://localhost:8000/metrics
```

---

## Best Practices

1. **Cost Tracking**
   - Track every API call
   - Set up alerts before hitting limits
   - Review daily/weekly reports

2. **Latency Monitoring**
   - Track P50, P95, P99 latencies
   - Alert on degradation
   - Compare across models

3. **Error Tracking**
   - Log all errors with context
   - Track error rates by model
   - Set up alerts for spikes

4. **Tracing**
   - Use trace IDs across requests
   - Link related LLM calls
   - Include user context when appropriate

5. **Security**
   - Don't log full prompts in production
   - Mask PII in logs
   - Secure observability endpoints
