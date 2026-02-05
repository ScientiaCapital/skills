# State Schemas Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Building state classes, debugging concurrent updates, designing multi-agent state

## Annotated Reducers

### Built-in: add_messages
```python
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

**Behavior**: Merges message lists by ID, deduplicates, preserves order.

### Built-in: operator.add
```python
import operator
from typing import Annotated

class AgentState(TypedDict):
    items: Annotated[list[str], operator.add]  # Concurrent-safe append
    scores: Annotated[list[float], operator.add]
```

**Behavior**: Concatenates lists from parallel branches (e.g., `[1, 2] + [3, 4] = [1, 2, 3, 4]`).

### Custom Reducers
```python
def merge_metadata(existing: dict, new: dict) -> dict:
    """Deep merge with conflict resolution."""
    result = existing.copy()
    for key, value in new.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_metadata(result[key], value)
        else:
            result[key] = value  # New value wins
    return result

class AgentState(TypedDict):
    metadata: Annotated[Dict[str, Any], merge_metadata]
```

## TypedDict Patterns

### total=False for Optional Fields
```python
class BaseAgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    agent_type: str  # Optional - not all agents need this
    lead_id: Optional[int]  # Explicitly optional
    metadata: Dict[str, Any]  # Optional dict
```

**Why**: Allows partial state updates without TypedDict errors.

### Nested State Structures
```python
class ConversationContext(TypedDict):
    topic: str
    sentiment: str
    confidence: float

class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    context: ConversationContext
    history: list[ConversationContext]
```

## Multi-Level State (Inheritance)

```python
# Base state shared by all agents
class BaseAgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    metadata: Dict[str, Any]

# Sales-specific extension
class SalesAgentState(BaseAgentState, total=False):
    lead_id: int
    objections: Annotated[list[str], operator.add]
    sentiment_score: float

# Support-specific extension
class SupportAgentState(BaseAgentState, total=False):
    ticket_id: int
    priority: str
    resolved: bool
```

**Pattern**: Base class defines shared fields, subclasses add agent-specific data.

## Best Practices

### Choose the Right Reducer
- **add_messages**: Always for LangChain messages (handles deduplication)
- **operator.add**: For lists that grow from parallel branches
- **Custom reducer**: For dicts, complex merges, or business logic

### Common Mistakes

❌ **No reducer for concurrent updates**:
```python
class State(TypedDict):
    items: list[str]  # Will cause overwrites in parallel branches!
```

✅ **Use operator.add**:
```python
class State(TypedDict):
    items: Annotated[list[str], operator.add]
```

❌ **Mutable defaults**:
```python
class State(TypedDict):
    metadata: Dict[str, Any] = {}  # Shared across instances!
```

✅ **No defaults in TypedDict, initialize in graph**:
```python
graph.add_node("init", lambda state: {"metadata": {}})
```

### Validation Pattern
```python
from pydantic import BaseModel, field_validator

class ValidatedState(BaseModel):
    messages: list[BaseMessage]
    lead_id: int

    @field_validator('lead_id')
    def validate_lead_id(cls, v):
        if v <= 0:
            raise ValueError("lead_id must be positive")
        return v

# Convert to TypedDict for LangGraph
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    lead_id: int
```

**Use when**: State validation is critical (financial, compliance).

## Multiple State Schemas Pattern

Use different schemas for different graph sections:

### Input/Output Schemas

```python
class InputState(TypedDict):
    """What the graph accepts from external callers."""
    query: str
    user_id: str

class OutputState(TypedDict):
    """What the graph returns to callers."""
    response: str
    confidence: float

class InternalState(TypedDict, total=False):
    """Full internal state - not exposed externally."""
    query: str
    user_id: str
    response: str
    confidence: float
    intermediate_results: list[str]
    agent_reasoning: str

# Build graph with schema separation
workflow = StateGraph(InternalState, input=InputState, output=OutputState)
```

### Private Node State

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    final_answer: str

class ResearchPrivateState(TypedDict):
    """Only visible to research node, not in main state."""
    search_queries: list[str]
    raw_results: list[dict]
    filtered_count: int

def research_node(state: OverallState) -> dict:
    # Use private state internally
    private: ResearchPrivateState = {
        "search_queries": generate_queries(state),
        "raw_results": [],
        "filtered_count": 0
    }

    for query in private["search_queries"]:
        results = search(query)
        private["raw_results"].extend(results)

    # Only return what should update main state
    return {"messages": [summarize(private["raw_results"])]}
```

## Runtime Context Pattern

### Accessing Config in Nodes

```python
from langgraph.config import get_config

def configurable_node(state: State) -> dict:
    """Access runtime configuration."""
    config = get_config()

    # Access thread ID
    thread_id = config.get("configurable", {}).get("thread_id")

    # Access custom config
    user_tier = config.get("configurable", {}).get("user_tier", "free")

    if user_tier == "premium":
        # Use better model, more tokens, etc.
        pass

    return {"processed": True}

# Pass config at runtime
result = graph.invoke(
    {"query": "Hello"},
    config={
        "configurable": {
            "thread_id": "user_123_session_456",
            "user_tier": "premium",
            "max_tokens": 4096
        }
    }
)
```

### Recursion Limit Management

```python
# Set recursion limit to prevent infinite loops
result = graph.invoke(
    inputs,
    config={"recursion_limit": 25}  # Default is 25
)

# Handle recursion limit reached
from langgraph.errors import GraphRecursionError

try:
    result = graph.invoke(inputs, config={"recursion_limit": 10})
except GraphRecursionError:
    # Gracefully handle max depth reached
    return {"error": "Workflow exceeded maximum steps"}
```

### Thread-Scoped State

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

# Each thread_id maintains separate state
result_a = graph.invoke(
    {"messages": [{"role": "user", "content": "Start project A"}]},
    config={"configurable": {"thread_id": "project_a"}}
)

result_b = graph.invoke(
    {"messages": [{"role": "user", "content": "Start project B"}]},
    config={"configurable": {"thread_id": "project_b"}}
)

# Resume project A later
result_a_continued = graph.invoke(
    {"messages": [{"role": "user", "content": "Continue"}]},
    config={"configurable": {"thread_id": "project_a"}}
)
```
