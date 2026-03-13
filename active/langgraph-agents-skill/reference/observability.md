# Observability for LangGraph Agents

Tracing, monitoring, evaluation, and debugging patterns for production agent systems.

---

## LangSmith Tracing

### Zero-Config Setup

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "ls_..."
os.environ["LANGSMITH_PROJECT"] = "my-agent-prod"

# All LangGraph operations auto-trace — no code changes needed
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools)  # Traces automatically
```

### Selective Tracing

```python
from langsmith import tracing_context

# Enable tracing for specific blocks only
with tracing_context(project_name="debug-session"):
    result = agent.invoke(input_data)

# Disable tracing temporarily (e.g., health checks, test runs)
with tracing_context(enabled=False):
    result = agent.invoke(input_data)  # Not traced
```

### Run Metadata and Tags

```python
config = {
    "configurable": {"thread_id": "user-123"},
    "tags": ["production", "v2"],
    "metadata": {
        "user_id": "user-123",
        "session_type": "customer-support",
        "cost_tier": "standard",
        "deployment": "us-east-1",
    }
}
result = agent.invoke(input_data, config=config)
# Filter by tags/metadata in LangSmith dashboard
# Drill down to specific user sessions from support tickets
```

### `@traceable` Decorator

```python
from langsmith import traceable

@traceable(name="custom_retrieval", tags=["rag", "vector-search"])
def retrieve_documents(query: str, k: int = 5) -> list[str]:
    """Custom retrieval function traced in LangSmith."""
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

@traceable(name="reranker", run_type="chain")
def rerank_results(query: str, docs: list[str]) -> list[str]:
    """Reranking step traced as a child span."""
    # ... reranking logic
    return docs
```

---

## Custom Metrics

### Token Usage Tracking

```python
from langchain_core.callbacks import UsageMetadataCallbackHandler

handler = UsageMetadataCallbackHandler()
result = agent.invoke(input_data, config={"callbacks": [handler]})

total_input = sum(u.input_tokens for u in handler.usage_metadata)
total_output = sum(u.output_tokens for u in handler.usage_metadata)
cost = (total_input * 3e-6) + (total_output * 15e-6)  # Claude Sonnet 4.6

print(f"Tokens — in: {total_input}, out: {total_output}, cost: ${cost:.4f}")
```

### Latency and Error Tracking

```python
import time
from langchain_core.callbacks.base import BaseCallbackHandler

class AgentMetricsHandler(BaseCallbackHandler):
    """Track latency, errors, and tool calls across agent runs."""

    def __init__(self):
        self.node_timings: dict[str, list[float]] = {}
        self._start_times: dict[str, float] = {}
        self.total_runs = 0
        self.errors = 0
        self.tool_calls = 0

    def on_chain_start(self, serialized: dict, inputs: dict, **kwargs) -> None:
        name = serialized.get("name", "unknown")
        self._start_times[name] = time.perf_counter()
        self.total_runs += 1

    def on_chain_end(self, outputs: dict, **kwargs) -> None:
        for name, start in list(self._start_times.items()):
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.node_timings.setdefault(name, []).append(elapsed_ms)
            del self._start_times[name]
            break

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        self.errors += 1

    def on_tool_start(self, *args, **kwargs) -> None:
        self.tool_calls += 1

    @property
    def error_rate(self) -> float:
        return self.errors / self.total_runs if self.total_runs else 0.0

metrics = AgentMetricsHandler()
result = graph.invoke(input_data, config={"callbacks": [metrics]})
print(f"Error rate: {metrics.error_rate:.1%}, Tool calls: {metrics.tool_calls}")
```

---

## Evaluation

### LangSmith Evaluators

```python
from langsmith import Client, evaluate

client = Client()

# Build evaluation dataset once
dataset = client.create_dataset("agent-qa-v2")
client.create_examples(
    inputs=[
        {"query": "What is LangGraph?"},
        {"query": "How does state persistence work?"},
    ],
    outputs=[
        {"answer": "LangGraph is a framework for building stateful multi-actor agents"},
        {"answer": "State persistence is handled by checkpointers like PostgresSaver"},
    ],
    dataset_id=dataset.id
)

# Run evaluation experiment
results = evaluate(
    agent.invoke,
    data=dataset,
    evaluators=["correctness", "helpfulness"],
    experiment_prefix="v2-upgrade",
    max_concurrency=4,
)
print(results.to_pandas()[["correctness", "helpfulness"]].mean())
```

### Custom Evaluators

```python
from langsmith.schemas import Run, Example

def tool_usage_evaluator(run: Run, example: Example) -> dict:
    """Score whether agent used the expected tools."""
    messages = run.outputs.get("messages", [])
    tool_messages = [m for m in messages if getattr(m, "type", "") == "tool"]
    used_tools = {m.name for m in tool_messages if hasattr(m, "name")}

    expected_tools = set(example.outputs.get("expected_tools", []))
    if not expected_tools:
        return {"key": "tool_usage", "score": 1.0}

    coverage = len(used_tools & expected_tools) / len(expected_tools)
    return {
        "key": "tool_usage",
        "score": coverage,
        "comment": f"Used: {used_tools}, Expected: {expected_tools}",
    }

def response_length_evaluator(run: Run, example: Example) -> dict:
    """Check that response is within expected length bounds."""
    output = run.outputs.get("messages", [])
    last_content = output[-1].content if output else ""
    min_len = example.outputs.get("min_length", 10)
    max_len = example.outputs.get("max_length", 2000)
    in_bounds = min_len <= len(last_content) <= max_len
    return {"key": "response_length", "score": 1.0 if in_bounds else 0.0}
```

---

## Production Monitoring

### Anomaly Detection

```python
from collections import deque
import statistics

class AnomalyDetector:
    """Simple rolling-window anomaly detector for token usage."""

    def __init__(self, window_size: int = 100, threshold_sigma: float = 3.0):
        self.window = deque(maxlen=window_size)
        self.threshold = threshold_sigma

    def record(self, value: float) -> bool:
        """Returns True if value is anomalous."""
        self.window.append(value)
        if len(self.window) < 10:
            return False  # Not enough data yet
        mean = statistics.mean(self.window)
        stdev = statistics.stdev(self.window)
        if stdev == 0:
            return False
        z_score = abs(value - mean) / stdev
        return z_score > self.threshold

token_anomaly = AnomalyDetector(window_size=200, threshold_sigma=3.0)

def monitored_invoke(graph, input_data: dict, config: dict) -> dict:
    handler = UsageMetadataCallbackHandler()
    result = graph.invoke(input_data, config={**config, "callbacks": [handler]})

    total_tokens = sum(u.input_tokens + u.output_tokens for u in handler.usage_metadata)
    if token_anomaly.record(float(total_tokens)):
        alert(f"Token spike detected: {total_tokens} tokens in single run")

    return result
```

### Quality Degradation Alerts

```python
import schedule  # pip install schedule
import time

def run_quality_check():
    """Scheduled evaluation run — detect quality regressions."""
    results = evaluate(
        agent.invoke,
        data="agent-qa-v2",  # Dataset name
        evaluators=["correctness"],
        experiment_prefix="scheduled-check",
    )
    df = results.to_pandas()
    correctness_mean = df["correctness"].mean()

    QUALITY_THRESHOLD = 0.85
    if correctness_mean < QUALITY_THRESHOLD:
        alert(
            f"Quality regression: correctness={correctness_mean:.2f} "
            f"below threshold {QUALITY_THRESHOLD}"
        )

# Run quality check daily at 6 AM
schedule.every().day.at("06:00").do(run_quality_check)
```

---

## Multi-Provider Observability

### Unified Tracing Across Providers

```python
# All providers trace to same LangSmith project when LANGSMITH_TRACING=true
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

claude = ChatAnthropic(model="claude-sonnet-4-6")   # Traced
groq = ChatGroq(model="llama-3.3-70b-versatile")    # Traced
ollama = ChatOllama(model="qwen2.5:7b")             # Traced

# Compare provider performance in LangSmith dashboard
# Filter traces by model name to benchmark cost vs quality
```

### Provider Comparison Pattern

```python
from langsmith import evaluate

# Run same eval across providers to compare
for model_name, model in [
    ("claude-sonnet-4-6", claude),
    ("llama-3.3-70b", groq),
]:
    agent = create_react_agent(model, tools)
    evaluate(
        agent.invoke,
        data="agent-qa-v2",
        evaluators=["correctness", "helpfulness"],
        experiment_prefix=f"provider-compare-{model_name}",
    )
# Compare results side-by-side in LangSmith Experiments view
```

---

## Debugging Techniques

### Replay a Failing Run

```python
from langsmith import Client

client = Client()

# Pull the exact inputs from a failed run
run = client.read_run("run-uuid-here")
failed_input = run.inputs

# Reproduce locally with full tracing
with tracing_context(project_name="debug-replay"):
    result = agent.invoke(failed_input)
```

### State History Inspection

```python
# Walk the full execution history of a thread
config = {"configurable": {"thread_id": "problematic-thread-id"}}
history = list(graph.get_state_history(config))

for state in reversed(history):
    step = state.metadata.get("step", "?")
    print(f"Step {step}: next={list(state.next)}")
    print(f"  Messages: {len(state.values.get('messages', []))}")
```

---

## Best Practices

| Area | Recommendation |
|------|---------------|
| Tracing | Always trace in production — overhead is ~2-5ms per span |
| Projects | Separate LangSmith projects for dev/staging/prod |
| Tags | Tag by user ID and session type for targeted debugging |
| Evals | Run scheduled evals — catch regressions before users do |
| Alerts | Set up alerts for token spikes, error rate, latency |
| Retention | 30-day trace history balances debuggability and storage |
| Sampling | At high volume (>1000 req/min), sample traces at 10-20% |
| Metadata | Include deployment region and version in run metadata |
