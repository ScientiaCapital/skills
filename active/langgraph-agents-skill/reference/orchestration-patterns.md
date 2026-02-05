# Agent Orchestration Patterns

Three proven patterns for coordinating multiple agents in LangGraph systems.

---

## 1. Supervisor Pattern

**When to use**: Clear hierarchy, centralized control, deterministic routing.

**Best for**: Customer support escalation, document processing pipelines, approval workflows.

### Implementation

```python
from langgraph.prebuilt import create_supervisor
from langchain_anthropic import ChatAnthropic

# Define specialized agents
research_agent = create_agent(model, research_tools, "Research specialist")
writer_agent = create_agent(model, writer_tools, "Content writer")
reviewer_agent = create_agent(model, review_tools, "Quality reviewer")

# Create supervisor with centralized routing
model = ChatAnthropic(model="claude-sonnet-4-5-20250929")
supervisor_graph = create_supervisor(
    agents=[research_agent, writer_agent, reviewer_agent],
    model=model
)

# Supervisor decides which agent handles each step
result = supervisor_graph.invoke({
    "messages": [("user", "Write article about LangGraph patterns")]
})
```

### Routing Logic

The supervisor uses LLM function binding to route tasks:
- Analyzes incoming message/state
- Selects appropriate agent via tool call
- Aggregates responses before next routing decision

### Termination

Set explicit end conditions:
```python
if response.tool_calls and response.tool_calls[0]["name"] == "FINISH":
    return END
```

---

## 2. Swarm Pattern

**When to use**: Peer collaboration, dynamic handoffs, exploratory workflows.

**Best for**: Multi-specialist consultation, creative brainstorming, adaptive problem-solving.

### Implementation

```python
from langgraph.prebuilt import create_swarm

# Define peer agents with handoff capabilities
alice = Agent(
    name="Alice",
    instructions="SQL expert. Hand off to Bob for Python.",
    tools=[query_db, handoff_to_bob]
)

bob = Agent(
    name="Bob",
    instructions="Python expert. Hand off to Alice for SQL.",
    tools=[execute_code, handoff_to_alice]
)

# Create swarm with peer-to-peer coordination
swarm_graph = create_swarm(
    agents=[alice, bob],
    default_active_agent="Alice"
)

# Agents decide when to hand off to peers
result = swarm_graph.invoke({
    "messages": [("user", "Query DB then visualize with Python")]
})
```

### Handoff Mechanism

Agents use handoff tools to transfer control:
```python
def handoff_to_bob(reason: str):
    """Transfer task to Bob with context"""
    return {"active_agent": "Bob", "context": reason}
```

State passes seamlessly between peers without central coordinator.

---

## 3. Master Orchestrator Pattern

**When to use**: Complex workflows, learning systems, adaptive routing.

**Best for**: Multi-phase projects, evolving strategies, performance optimization.

### Implementation

```python
from langgraph.graph import StateGraph, END

class MasterOrchestrator:
    def __init__(self, agents: dict):
        self.agents = agents
        self.performance_metrics = {}

    async def route(self, state: dict) -> str:
        """Intelligent routing based on task complexity and agent performance"""
        complexity = self.assess_complexity(state["task"])

        if complexity == "simple":
            return "fast_agent"
        elif complexity == "research":
            return "deep_research_agent"
        else:
            # Select best performing agent for this task type
            return self.select_best_agent(state["task_type"])

    def assess_complexity(self, task: str) -> str:
        """Analyze task requirements"""
        # Custom logic: token count, keyword analysis, etc.
        return "simple" if len(task.split()) < 20 else "research"

    def select_best_agent(self, task_type: str) -> str:
        """Choose agent based on historical performance"""
        best_agent = max(
            self.performance_metrics.get(task_type, {}),
            key=lambda x: x[1],
            default=("default_agent", 0)
        )
        return best_agent[0]

# Build graph with custom routing
workflow = StateGraph(State)
orchestrator = MasterOrchestrator(agents={...})

workflow.add_node("route", orchestrator.route)
workflow.add_conditional_edges("route", lambda s: s["next_agent"])
```

### Workflow Composition

Chain multiple agents with conditional logic:
```python
workflow.add_edge("research_agent", "synthesis_agent")
workflow.add_conditional_edges(
    "synthesis_agent",
    lambda s: "review_agent" if s["needs_review"] else END
)
```

---

## Decision Matrix

| Pattern | Control | Flexibility | Complexity | Best Use Case |
|---------|---------|-------------|------------|---------------|
| **Supervisor** | Centralized | Low | Low | Linear workflows, clear hierarchy |
| **Swarm** | Distributed | High | Medium | Peer collaboration, dynamic tasks |
| **Master Orchestrator** | Custom | Very High | High | Learning systems, adaptive routing |

### When to Choose Each

**Choose Supervisor if**:
- Clear task hierarchy exists
- Predictable routing logic
- Need centralized monitoring
- Sequential processing preferred

**Choose Swarm if**:
- Agents are domain peers
- Tasks require back-and-forth collaboration
- No clear "leader" agent
- Exploratory workflows

**Choose Master Orchestrator if**:
- Complex decision trees
- Performance tracking needed
- Workflows evolve over time
- Custom routing logic required

### Scalability Considerations

- **Supervisor**: Scales to ~5-10 agents before becoming bottleneck
- **Swarm**: Scales to ~3-5 peers (n² handoff complexity)
- **Master Orchestrator**: Scales to 10+ agents with proper architecture

---

## Combining Patterns

Advanced systems can nest patterns:
```python
# Master orchestrator routes to supervisor sub-graphs
master = MasterOrchestrator({
    "content_team": supervisor_graph,  # Supervisor for writing workflow
    "analysis_team": swarm_graph       # Swarm for data analysis
})
```

Choose the simplest pattern that meets your requirements. Start with Supervisor, graduate to Swarm for peer coordination, use Master Orchestrator only when custom routing logic is essential.

---

## 4. Human-in-the-Loop (HITL) Pattern

**When to use**: Approval workflows, dangerous operations, compliance gates.

**Best for**: Deployment approvals, financial transactions, content moderation.

### Interrupt-Based HITL

```python
from langgraph.types import interrupt, Command
from typing import Literal

def approval_node(state: State) -> Command[Literal["proceed", "cancel"]]:
    """Pause execution for human approval."""
    approval = interrupt({
        "question": "Approve this action?",
        "details": state["pending_action"],
        "options": ["approve", "reject"]
    })

    if approval == "approve":
        return Command(goto="proceed")
    return Command(goto="cancel")

# Build graph with approval gate
workflow = StateGraph(State)
workflow.add_node("prepare", prepare_action)
workflow.add_node("approval", approval_node)
workflow.add_node("proceed", execute_action)
workflow.add_node("cancel", cancel_action)

workflow.add_edge("prepare", "approval")
# Conditional edges handled by Command return
```

### Resuming After Interrupt

```python
from langgraph.types import Command

# First invocation - pauses at interrupt
result = graph.invoke(
    {"messages": [{"role": "user", "content": "Deploy to production"}]},
    config={"configurable": {"thread_id": "deploy_123"}}
)
# result contains interrupt details

# Human reviews and approves...

# Resume with approval
final_result = graph.invoke(
    Command(resume="approve"),
    config={"configurable": {"thread_id": "deploy_123"}}
)
```

### Multiple Approval Gates

```python
def multi_gate_workflow(state: State) -> dict:
    # Gate 1: Manager approval
    manager_approval = interrupt({
        "gate": "manager",
        "question": "Manager approval required"
    })

    if manager_approval != "approve":
        return {"status": "rejected_by_manager"}

    # Gate 2: Compliance check
    compliance_approval = interrupt({
        "gate": "compliance",
        "question": "Compliance review required"
    })

    if compliance_approval != "approve":
        return {"status": "rejected_by_compliance"}

    return {"status": "fully_approved"}
```

### Command Pattern for Combined Updates

```python
from langgraph.types import Command

def routing_node(state: State) -> Command[Literal["agent_a", "agent_b", END]]:
    """Update state AND route in single return."""
    if state["task_type"] == "research":
        return Command(
            update={"assigned_to": "agent_a", "started_at": datetime.now()},
            goto="agent_a"
        )
    elif state["task_type"] == "writing":
        return Command(
            update={"assigned_to": "agent_b"},
            goto="agent_b"
        )
    else:
        return Command(goto=END)
```

---

## 5. Map-Reduce with Send Pattern

**When to use**: Parallel processing of multiple items, fan-out/fan-in workflows.

```python
from langgraph.types import Send

def fan_out_node(state: State) -> list[Send]:
    """Send each item to be processed in parallel."""
    return [
        Send("process_item", {"item": item, "index": i})
        for i, item in enumerate(state["items"])
    ]

def process_item(state: dict) -> dict:
    """Process a single item."""
    return {"result": f"Processed: {state['item']}"}

def reduce_node(state: State) -> dict:
    """Aggregate results from parallel processing."""
    return {"final_results": state["results"]}

# Build map-reduce graph
workflow = StateGraph(State)
workflow.add_node("fan_out", fan_out_node)
workflow.add_node("process_item", process_item)
workflow.add_node("reduce", reduce_node)

workflow.add_conditional_edges("fan_out", lambda _: "process_item")
workflow.add_edge("process_item", "reduce")
```
