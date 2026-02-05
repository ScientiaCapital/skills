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

## Durable Execution Guarantees

Functional API provides **deterministic replay**:

```python
@task
def non_deterministic_op() -> str:
    # This is checkpointed - replay returns same value
    return str(uuid.uuid4())

@entrypoint(checkpointer=InMemorySaver())
def durable_workflow() -> dict:
    # If workflow crashes after task_1 completes,
    # replay will return the SAME uuid, not generate a new one
    uuid_result = non_deterministic_op().result()
    return {"id": uuid_result}
```

**Implication**: Wrap non-deterministic operations (API calls, timestamps, random values) in `@task` for reliable replay.

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
