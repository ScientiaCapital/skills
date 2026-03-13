# Guardrails for LangGraph Agents

Patterns for input validation, output filtering, and safety controls in agent systems.

---

## Input Guardrails

### PII Detection

```python
import re

def redact_pii(text: str) -> str:
    """Redact common PII patterns from text."""
    patterns = {
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': '[EMAIL_REDACTED]',
        r'\b\d{3}-\d{2}-\d{4}\b': '[SSN_REDACTED]',
        r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b': '[CARD_REDACTED]',
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b': '[PHONE_REDACTED]',
    }
    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text)
    return text

# Use as input guard node or wrap around tool inputs
```

### Prompt Injection Detection

```python
from langchain_core.tools import tool

@tool
def validate_input(user_input: str) -> dict:
    """Check user input for injection attempts."""
    suspicious_patterns = [
        "ignore previous instructions",
        "you are now",
        "system prompt",
        "forget everything",
    ]
    for pattern in suspicious_patterns:
        if pattern.lower() in user_input.lower():
            return {"safe": False, "reason": f"Suspicious pattern: {pattern}"}
    return {"safe": True}
```

### Complexity Limits

```python
# Prevent runaway agents via recursion_limit in config
config = {
    "recursion_limit": 25,  # Max graph steps before stopping (default: 25)
    "configurable": {"thread_id": "user-123"},
}
result = graph.invoke(input_data, config=config)

# For finer control, track calls in state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tool_call_count: int

def tool_limiter_node(state: AgentState) -> dict:
    if state.get("tool_call_count", 0) > 20:
        return {"messages": [AIMessage(content="Tool call limit reached.")]}
    return {"tool_call_count": state.get("tool_call_count", 0) + 1}
```

---

## Output Guardrails

### Format Validation

```python
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent

class StructuredResponse(BaseModel):
    answer: str = Field(description="The main answer")
    confidence: float = Field(ge=0.0, le=1.0)
    sources: list[str] = Field(default_factory=list)

# Force structured output
agent = create_react_agent(
    model, tools,
    response_format=StructuredResponse
)
```

### Sensitive Data Filtering

```python
import re

def filter_output(response: str) -> str:
    """Remove sensitive patterns from agent output."""
    patterns = {
        r'\b\d{3}-\d{2}-\d{4}\b': '[SSN_REDACTED]',          # SSN
        r'\b\d{16}\b': '[CARD_REDACTED]',                       # Credit card
        r'(?i)api[_-]?key\s*[:=]\s*\S+': '[API_KEY_REDACTED]', # API keys
    }
    for pattern, replacement in patterns.items():
        response = re.sub(pattern, replacement, response)
    return response
```

---

## Tripwire Guardrails

### Budget Exceeded

```python
from langgraph.types import Command
from langchain_core.messages import AIMessage

class BudgetGuardrail:
    def __init__(self, max_cost_usd: float):
        self.max_cost = max_cost_usd
        self.total_cost = 0.0

    def track(self, usage_metadata: dict) -> None:
        input_tokens = usage_metadata.get("input_tokens", 0)
        output_tokens = usage_metadata.get("output_tokens", 0)
        # Claude Sonnet 4.6 pricing
        self.total_cost += (input_tokens * 3e-6) + (output_tokens * 15e-6)

    def check(self) -> None:
        if self.total_cost > self.max_cost:
            raise RuntimeError(
                f"Budget exceeded: ${self.total_cost:.4f} > ${self.max_cost:.4f}"
            )

# Usage in a node
budget = BudgetGuardrail(max_cost_usd=0.50)

def agent_node(state: AgentState) -> AgentState:
    response = model.invoke(state["messages"])
    budget.track(response.usage_metadata)
    budget.check()  # Raises if over budget
    return {"messages": [response]}
```

### Safety Violation Detection

```python
from langgraph.types import Command
from langchain_core.messages import AIMessage

UNSAFE_SEQUENCES = [
    {"tool": "delete_file", "followed_by": "send_email"},
]

def safety_check_node(state: dict) -> dict | Command:
    """Block unsafe tool sequences. Use as a node before the agent node."""
    messages = state.get("messages", [])
    last_tool_calls = [
        m.tool_calls for m in messages
        if hasattr(m, "tool_calls") and m.tool_calls
    ]
    recent_tools = [tc["name"] for calls in last_tool_calls[-3:] for tc in calls]
    for seq in UNSAFE_SEQUENCES:
        if seq["tool"] in recent_tools and seq["followed_by"] in recent_tools:
            return Command(
                goto="__end__",
                update={
                    "messages": [AIMessage(content="Unsafe tool sequence detected. Stopping.")]
                }
            )
    return {}  # Continue normally
```

### Unauthorized Tool Call

```python
TOOL_ALLOWLIST = {"search", "calculator", "read_file"}
TOOL_BLOCKLIST = {"delete_file", "send_email", "execute_code"}

def enforce_tool_policy(tool_calls: list[dict]) -> list[dict]:
    """Filter tool calls against allowlist/blocklist."""
    approved = []
    for call in tool_calls:
        name = call.get("name", "")
        if name in TOOL_BLOCKLIST:
            raise PermissionError(f"Tool '{name}' is blocked by policy")
        if TOOL_ALLOWLIST and name not in TOOL_ALLOWLIST:
            raise PermissionError(f"Tool '{name}' is not in the allowlist")
        approved.append(call)
    return approved
```

---

## Guardrail Composition

### Multi-Layer Defense as Graph Nodes

Compose guardrails as a pipeline of graph nodes for full traceability:

```python
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt

def pii_guard_node(state: AgentState) -> dict:
    """Layer 1: Sanitize PII from input."""
    last = state["messages"][-1].content if state["messages"] else ""
    clean = redact_pii(last)  # From redact_pii() above
    if clean != last:
        return {"messages": [HumanMessage(content=clean)]}
    return {}

def safety_guard_node(state: AgentState) -> dict:
    """Layer 2: Block unsafe content."""
    last = state["messages"][-1].content if state["messages"] else ""
    blocked = ["<script>", "DROP TABLE", "rm -rf"]
    if any(b.lower() in last.lower() for b in blocked):
        return {"messages": [AIMessage(content="I cannot process this request.")]}
    return {}

def hitl_guard_node(state: AgentState) -> dict:
    """Layer 3: Human approval for destructive ops."""
    last = state["messages"][-1]
    if hasattr(last, "tool_calls"):
        dangerous = {"delete_file", "send_email", "execute_code"}
        for tc in last.tool_calls:
            if tc["name"] in dangerous:
                approval = interrupt({"action": tc["name"], "args": tc["args"]})
                if not approval.get("approved"):
                    return {"messages": [AIMessage(content="Action rejected by human.")]}
    return {}
```

### Short-Circuit Pattern

Use conditional edges to skip remaining nodes on failure:

```python
def route_after_safety(state: AgentState) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and "cannot process" in last.content:
        return END  # Short-circuit — skip agent execution
    return "agent"

workflow.add_conditional_edges("safety_guard", route_after_safety)
```

---

## Integration with LangGraph

### Guardrails as Graph Nodes

Wrapping guardrails as first-class nodes gives full visibility in traces:

```python
from langgraph.graph import StateGraph, END, add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage

class GuardedState(TypedDict):
    messages: Annotated[list, add_messages]
    input_valid: bool
    output_valid: bool

def input_validation_node(state: GuardedState) -> dict:
    last = state["messages"][-1].content if state["messages"] else ""
    safe = all(p not in last.lower() for p in ["ignore previous", "system prompt"])
    return {"input_valid": safe}

def output_validation_node(state: GuardedState) -> dict:
    last = state["messages"][-1].content if state["messages"] else ""
    clean = filter_output(last)  # From filter_output() above
    return {"output_valid": clean == last, "messages": [AIMessage(content=clean)]}

def error_handler_node(state: GuardedState) -> dict:
    return {"messages": [AIMessage(content="Request could not be processed safely.")]}

def agent_node(state: GuardedState) -> dict:
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# Wire the graph
workflow = StateGraph(GuardedState)
workflow.add_node("input_guard", input_validation_node)
workflow.add_node("agent", agent_node)
workflow.add_node("output_guard", output_validation_node)
workflow.add_node("error", error_handler_node)

workflow.set_entry_point("input_guard")
workflow.add_conditional_edges(
    "input_guard",
    lambda s: "agent" if s["input_valid"] else "error"
)
workflow.add_edge("agent", "output_guard")
workflow.add_conditional_edges(
    "output_guard",
    lambda s: END if s["output_valid"] else "agent"
)
workflow.add_edge("error", END)
```

---

## Production Checklist

| Category | Check |
|----------|-------|
| Input | PII detection on all user inputs |
| Input | Prompt injection detection |
| Limits | Model call limit prevents infinite loops |
| Limits | Tool call limit prevents excessive API usage |
| Output | Output filtered for sensitive data leakage |
| Output | Structured output validation where applicable |
| Budget | Hard budget stop with cost tracking |
| Safety | Human-in-the-loop for destructive operations |
| Ops | All guardrail triggers logged for monitoring |
| Ops | Alerts on guardrail trigger rate spikes |
