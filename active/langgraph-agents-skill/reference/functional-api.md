# Functional API Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Simpler workflows, prefer decorators over explicit graph construction

## When to Use Functional API vs Graph API

| Criteria | Functional API | Graph API |
|----------|---------------|-----------|
| **Learning curve** | Lower (familiar decorators) | Higher (explicit graph concepts) |
| **Workflow complexity** | Simple to moderate | Moderate to complex |
| **Parallel execution** | Built-in with multiple @task calls | Requires explicit Send/parallel nodes |
| **State management** | Implicit through return values | Explicit TypedDict state |
| **Best for** | Linear flows, task pipelines | Complex routing, conditional edges |

**Rule of thumb**: Start with Functional API. Graduate to Graph API when you need conditional routing or complex state merging.

---

## Core Decorators

### @task - Durable Task Units

```python
from langgraph.func import task

@task
def research(query: str) -> str:
    """Research task with automatic checkpointing."""
    # LLM call, API fetch, etc.
    return f"Research results for: {query}"

@task
def synthesize(research: str, tone: str) -> str:
    """Synthesis depends on research completing first."""
    return f"Synthesized ({tone}): {research}"
```

**Key behaviors**:
- Tasks are checkpointed automatically
- Calling `.result()` blocks until completion
- Multiple task calls without `.result()` run in parallel

### @entrypoint - Workflow Entry

```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver

@task
def step_one(data: str) -> str:
    return f"Processed: {data}"

@task
def step_two(result: str) -> str:
    return f"Final: {result}"

@entrypoint(checkpointer=InMemorySaver())
def my_workflow(input_data: str) -> dict:
    """Main workflow with persistence."""
    r1 = step_one(input_data).result()
    r2 = step_two(r1).result()
    return {"output": r2}

# Invoke
result = my_workflow("hello")
```

---

## Parallel Execution

```python
from langgraph.func import entrypoint, task

@task
def fetch_source_a(query: str) -> str:
    return f"Source A: {query}"

@task
def fetch_source_b(query: str) -> str:
    return f"Source B: {query}"

@entrypoint(checkpointer=InMemorySaver())
def parallel_research(query: str) -> dict:
    # Start both tasks without blocking
    task_a = fetch_source_a(query)
    task_b = fetch_source_b(query)

    # Now block for both results
    result_a = task_a.result()
    result_b = task_b.result()

    return {"sources": [result_a, result_b]}
```

**Parallel pattern**: Call multiple `@task` functions, then call `.result()` on each.

---

## Human-in-the-Loop with Functional API

```python
from langgraph.func import entrypoint, task
from langgraph.types import interrupt

@task
def prepare_action(data: str) -> dict:
    return {"action": "deploy", "target": data}

@entrypoint(checkpointer=InMemorySaver())
def approval_workflow(data: str) -> dict:
    action = prepare_action(data).result()

    # Pause for human approval
    approval = interrupt({
        "question": f"Approve {action['action']} to {action['target']}?",
        "options": ["approve", "reject"]
    })

    if approval == "approve":
        return {"status": "deployed", "target": action["target"]}
    else:
        return {"status": "cancelled"}

# First invocation pauses at interrupt()
result = approval_workflow.invoke("production", config={"configurable": {"thread_id": "123"}})

# Resume with approval
result = approval_workflow.invoke(
    Command(resume="approve"),
    config={"configurable": {"thread_id": "123"}}
)
```

---

## Durable Execution

### Durability Modes

Control checkpoint write overhead vs crash safety:

| Mode | Behavior | Trade-off |
|------|----------|-----------|
| `"exit"` | Persists only at completion | Best performance |
| `"async"` | Async writes between steps | Balanced; minor crash risk |
| `"sync"` | Sync writes before each step | Highest safety |

### Failure and Resume

When a workflow crashes mid-execution:
1. Runtime identifies the last completed `@task` checkpoint
2. All completed tasks return cached results (no re-execution)
3. Execution resumes from the first incomplete task

```python
@task
def fetch_data(url: str) -> dict:
    """If this completes before crash, result is cached."""
    return requests.get(url).json()

@task
def process_data(data: dict) -> dict:
    """If crash happens here, fetch_data won't re-run on resume."""
    return transform(data)

@entrypoint(checkpointer=PostgresSaver.from_conn_string(DB_URL))
def pipeline(url: str) -> dict:
    data = fetch_data(url).result()      # Cached after completion
    result = process_data(data).result()  # Resumes here after crash
    return result
```

### Critical Rules for Durability

1. **All side effects inside `@task`**: Random values, API calls, timestamps
2. **Maintain consistent task order**: Task matching on resume is index-based
3. **Tasks must be idempotent**: They may re-run on resume if incomplete
4. **`@entrypoint` code re-runs**: Only `@task` results are cached

**Implication**: Wrap non-deterministic operations (API calls, timestamps, random values) in `@task` for reliable replay.

---

## Time Travel and Debugging

### State History

Access all checkpoints for a thread:

```python
config = {"configurable": {"thread_id": "my-thread"}}

# List all state snapshots
history = list(workflow.get_state_history(config))
for snapshot in history:
    print(f"Step: {snapshot.metadata['step']}, Next: {snapshot.next}")

# Get current state
current = workflow.get_state(config)
```

### Forking from Historical State

Branch from a past checkpoint with modified state:

```python
# Find desired checkpoint
history = list(workflow.get_state_history(config))
target = history[3]  # 4th checkpoint

# Fork with state modification
fork_config = workflow.update_state(
    target.config,
    values={"query": "modified query"}
)

# Execute from forked state
result = workflow.invoke(None, fork_config)
```

**Warning**: Replay RE-EXECUTES nodes — LLM calls fire again (no caching at node level). Use `@task` for fine-grained caching.

---

## Testing Functional Workflows

### Unit Testing Individual Tasks

```python
import pytest

def test_research_task():
    """Tasks can be tested in isolation."""
    result = research("LangGraph patterns").result()
    assert "LangGraph" in result

def test_parallel_tasks():
    """Test parallel execution returns all results."""
    futures = [fetch_source_a(q) for q in ["a", "b", "c"]]
    results = [f.result() for f in futures]
    assert len(results) == 3
```

### Integration Testing with Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver

def test_interrupt_resume():
    """Test HITL interrupt and resume cycle."""
    checkpointer = InMemorySaver()
    config = {"configurable": {"thread_id": "test-1"}}

    # First invocation — hits interrupt
    result = approval_workflow.invoke("production", config=config)
    assert "__interrupt__" in result

    # Resume with approval
    final = approval_workflow.invoke(
        Command(resume="approve"), config=config
    )
    assert final["status"] == "deployed"
```

---

## Combining with Graph API

Functional API workflows can be nodes in Graph API:

```python
from langgraph.graph import StateGraph
from langgraph.func import entrypoint, task

@task
def research_task(query: str) -> str:
    return f"Research: {query}"

@entrypoint()
def research_subworkflow(query: str) -> dict:
    return {"findings": research_task(query).result()}

# Use as node in larger graph
workflow = StateGraph(AgentState)
workflow.add_node("research", research_subworkflow)
workflow.add_node("synthesis", synthesis_node)
workflow.add_edge("research", "synthesis")
```

---

## Best Practices

1. **Keep tasks focused**: One responsibility per `@task`
2. **Use checkpointer in production**: Always pass `checkpointer` to `@entrypoint`
3. **Handle interrupts**: Use `interrupt()` for human approval, not exceptions
4. **Prefer parallel when possible**: Call multiple tasks before calling `.result()`
5. **Wrap side effects**: Non-deterministic operations belong in `@task`

## Migration from Graph API

| Graph API | Functional API Equivalent |
|-----------|--------------------------|
| `StateGraph(State)` | `@entrypoint(checkpointer=...)` |
| `workflow.add_node("name", fn)` | `@task def name(...)` |
| `workflow.add_edge("a", "b")` | `b(a().result())` |
| `workflow.add_conditional_edges` | Python `if/else` statements |
| `Command(goto="node")` | Return values + Python flow control |
