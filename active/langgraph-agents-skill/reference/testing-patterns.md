# Testing Patterns for LangGraph

Strategies for unit testing, integration testing, and CI/CD for graph-based agent systems.

---

## Unit Testing Graph Nodes

### Mock LLM Responses

```python
import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage, HumanMessage

def test_agent_node_routes_correctly():
    """Test that agent node produces correct routing decision."""
    mock_model = MagicMock()
    mock_model.invoke.return_value = AIMessage(
        content="I'll research this topic.",
        tool_calls=[{
            "name": "search",
            "args": {"query": "LangGraph"},
            "id": "call_1"
        }]
    )

    state = {"messages": [HumanMessage(content="Research LangGraph")]}
    result = agent_node(state, model=mock_model)

    assert result["messages"][-1].tool_calls[0]["name"] == "search"
    mock_model.invoke.assert_called_once()
```

### Test State Transformations

```python
def test_reduce_node_aggregates():
    """Test that reduce node properly aggregates parallel results."""
    state = {
        "results": [
            {"source": "A", "data": "result_a"},
            {"source": "B", "data": "result_b"},
        ]
    }
    result = reduce_node(state)
    assert len(result["final_results"]) == 2
    assert result["final_results"][0]["source"] == "A"

def test_node_returns_correct_keys():
    """Verify node output contains required state keys."""
    state = {"messages": [HumanMessage(content="test")], "context": ""}
    result = enrichment_node(state)
    assert "context" in result
    assert isinstance(result["context"], str)
```

---

## Integration Testing Full Graphs

### Fresh Checkpointer Per Test

```python
from langgraph.checkpoint.memory import InMemorySaver
import pytest

@pytest.fixture
def graph():
    """Create fresh graph with clean checkpointer per test."""
    checkpointer = InMemorySaver()
    return build_my_graph(checkpointer=checkpointer)

def test_full_workflow(graph):
    config = {"configurable": {"thread_id": "test-1"}}
    result = graph.invoke(
        {"messages": [HumanMessage(content="Hello")]},
        config=config
    )
    assert len(result["messages"]) >= 2
    assert result["messages"][-1].type == "ai"
```

### Interrupt/Resume Cycles

```python
from langgraph.types import Command

def test_approval_flow(graph):
    config = {"configurable": {"thread_id": "test-approval"}}

    # First invocation should trigger interrupt at approval node
    result = graph.invoke(
        {"messages": [HumanMessage(content="Deploy to prod")]},
        config=config
    )

    # Verify the graph paused awaiting approval
    state = graph.get_state(config)
    assert "approval" in state.next

    # Resume with approval signal
    final = graph.invoke(Command(resume="approve"), config=config)
    assert final["status"] == "deployed"

def test_rejection_flow(graph):
    config = {"configurable": {"thread_id": "test-rejection"}}

    graph.invoke(
        {"messages": [HumanMessage(content="Delete all records")]},
        config=config
    )

    final = graph.invoke(Command(resume="reject"), config=config)
    assert final["status"] == "cancelled"
```

---

## Snapshot Testing State Transitions

### Golden Snapshots

```python
import json
from pathlib import Path

SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"

def save_snapshot(name: str, data: list) -> None:
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    (SNAPSHOTS_DIR / f"{name}.json").write_text(json.dumps(data, indent=2))

def load_snapshot(name: str) -> list:
    return json.loads((SNAPSHOTS_DIR / f"{name}.json").read_text())

def test_state_transitions_match_snapshot(graph):
    """Compare state evolution against known-good snapshot."""
    config = {"configurable": {"thread_id": "snapshot-test"}}

    graph.invoke(
        {"messages": [HumanMessage(content="test input")]},
        config=config
    )

    history = list(graph.get_state_history(config))
    transitions = [
        {"step": s.metadata.get("step"), "next": sorted(list(s.next))}
        for s in history
    ]

    snapshot_name = "state_transitions_v1"
    if not (SNAPSHOTS_DIR / f"{snapshot_name}.json").exists():
        save_snapshot(snapshot_name, transitions)
        pytest.skip("Snapshot created — re-run to compare")

    expected = load_snapshot(snapshot_name)
    assert transitions == expected, "State transitions changed — update snapshot if intentional"
```

---

## Mock Tool Execution

```python
@pytest.fixture
def mock_tools():
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """Mock search returning predictable results."""
        return f"Mock results for: {query}"

    @tool
    def get_weather(city: str) -> str:
        """Mock weather tool."""
        return f"Sunny, 72F in {city}"

    return [search, get_weather]

def test_agent_uses_tools(mock_tools, mock_model):
    from langgraph.prebuilt import create_react_agent

    graph = create_react_agent(mock_model, tools=mock_tools)
    result = graph.invoke({
        "messages": [HumanMessage(content="Search for LangGraph tutorials")]
    })

    tool_messages = [m for m in result["messages"] if m.type == "tool"]
    assert len(tool_messages) >= 1
    assert "Mock results" in tool_messages[0].content
```

---

## Testing Multi-Agent Coordination

### Partial Execution with `interrupt_after`

`interrupt_after` is a **compile-time** parameter — set it when building the graph, not at invoke time:

```python
@pytest.fixture
def routing_graph():
    """Graph compiled with interrupt to pause after supervisor node."""
    checkpointer = InMemorySaver()
    graph = build_my_graph(checkpointer=checkpointer)
    # Compile with interrupt_after to pause after supervisor decides
    return graph.compile(interrupt_after=["supervisor"], checkpointer=checkpointer)

def test_supervisor_routes_to_researcher(routing_graph):
    """Test supervisor routing without executing the full pipeline."""
    config = {"configurable": {"thread_id": "routing-test"}}

    routing_graph.invoke(
        {"messages": [HumanMessage(content="Research LangGraph")]},
        config=config,
    )

    state = routing_graph.get_state(config)
    assert "researcher" in state.next

def test_supervisor_routes_to_coder(routing_graph):
    config = {"configurable": {"thread_id": "routing-coder"}}

    routing_graph.invoke(
        {"messages": [HumanMessage(content="Write a Python function")]},
        config=config,
    )

    state = routing_graph.get_state(config)
    assert "coder" in state.next
```

### Positioned Execution with `update_state`

```python
def test_reviewer_with_preset_state(graph):
    """Start execution from a specific node with preset state."""
    config = {"configurable": {"thread_id": "positioned-test"}}

    # Seed state as if researcher just completed
    graph.update_state(
        config,
        values={"research_output": "pre-computed research data about LangGraph"},
        as_node="researcher"  # Pretend this came from researcher node
    )

    # Execute from reviewer onward
    result = graph.invoke(None, config=config)
    assert "review" in result.get("status", "")

def test_skip_to_output_formatter(graph):
    """Skip expensive processing by injecting state."""
    config = {"configurable": {"thread_id": "skip-test"}}

    graph.update_state(
        config,
        values={
            "raw_data": [1, 2, 3],
            "analysis_complete": True,
        },
        as_node="analyzer"
    )

    result = graph.invoke(None, config=config)
    assert "formatted_output" in result
```

---

## CI/CD Integration

### Pytest Configuration

```python
# conftest.py
import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

@pytest.fixture(scope="session")
def cheap_model():
    """Use a fast/cheap model for CI integration tests."""
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(model="claude-haiku-4-5", max_tokens=256)

@pytest.fixture
def mock_model():
    """Fully mocked model — no API calls."""
    model = MagicMock()
    model.invoke.return_value = AIMessage(content="Mock response")
    model.bind_tools.return_value = model
    return model
```

```ini
# pytest.ini
[pytest]
markers =
    slow: marks tests that make real LLM API calls (deselect with -m "not slow")
    snapshot: marks snapshot comparison tests
    integration: marks full-graph integration tests

# Run only fast unit tests in CI pre-commit:
# pytest -m "not slow and not integration"
```

### Cost Budgets for Test Suites

```python
# conftest.py
from langchain_core.callbacks import UsageMetadataCallbackHandler

MAX_SUITE_COST_USD = 0.50

@pytest.fixture(scope="session", autouse=True)
def cost_tracker():
    handler = UsageMetadataCallbackHandler()
    yield handler

    total_input = sum(u.input_tokens for u in handler.usage_metadata)
    total_output = sum(u.output_tokens for u in handler.usage_metadata)
    total_cost = (total_input * 3e-6) + (total_output * 15e-6)

    print(f"\nTest suite cost: ${total_cost:.4f}")
    if total_cost > MAX_SUITE_COST_USD:
        pytest.fail(
            f"Test suite exceeded cost budget: ${total_cost:.4f} > ${MAX_SUITE_COST_USD}"
        )
```

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Agent Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -m "not slow" --tb=short

  integration-tests:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -m "integration" --tb=short
```

---

## Best Practices

| Practice | Reason |
|----------|--------|
| Fresh `InMemorySaver` per test | Prevents state bleed between tests |
| Mock LLMs for unit tests | Fast, deterministic, free |
| Real models only in integration tests | Cost control |
| Compile with `interrupt_after` for partial execution | Test routing without full pipeline |
| `update_state` + `as_node` for positioned tests | Skip to specific nodes cheaply |
| Snapshot tests for regressions | Catch unexpected state transition changes |
| Cost budgets in CI | Prevent accidental expensive runs |
| Separate pytest markers | Granular test selection per environment |
