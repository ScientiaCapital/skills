# Agent Orchestration Patterns

Three proven patterns for coordinating multiple agents in LangGraph systems.

---

## 1. Supervisor Pattern

**When to use**: Clear hierarchy, centralized control, deterministic routing.

**Best for**: Customer support escalation, document processing pipelines, approval workflows.

### Implementation

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Initialize model
model = ChatAnthropic(model="claude-sonnet-4-6")

# Define specialized agents
research_agent = create_react_agent(model, tools=research_tools, prompt="Research specialist")
writer_agent = create_react_agent(model, tools=writer_tools, prompt="Content writer")
reviewer_agent = create_react_agent(model, tools=review_tools, prompt="Quality reviewer")

# Create supervisor with centralized routing
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
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.prebuilt import create_react_agent

# Create handoff tools
handoff_to_bob = create_handoff_tool(agent_name="Bob", description="Transfer to Bob for Python tasks")
handoff_to_alice = create_handoff_tool(agent_name="Alice", description="Transfer to Alice for SQL tasks")

# Create peer agents with handoff capabilities
alice = create_react_agent(
    model,
    tools=[query_db, handoff_to_bob],
    prompt="You are Alice, a SQL expert. Hand off to Bob for Python tasks."
)

bob = create_react_agent(
    model,
    tools=[execute_code, handoff_to_alice],
    prompt="You are Bob, a Python expert. Hand off to Alice for SQL tasks."
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

Agents use `create_handoff_tool` from `langgraph_swarm` to transfer control. Handoff tools return a `Command` that updates the active agent in state and passes a `ToolMessage` with context. State passes seamlessly between peers without a central coordinator.

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
| **Handoff** | Sequential | Medium | Low | Pipeline chains, escalation flows |
| **Router** | Dispatch | Medium | Low | Classify-and-route workflows |
| **Skills** | On-demand | High | Low | Progressive disclosure of capabilities |
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

# fan_out returns Send objects that route directly to process_item
# No edge needed from fan_out — Send handles routing
workflow.add_edge("process_item", "reduce")
workflow.set_entry_point("fan_out")
```

---

## 6. Handoff Pattern

**When to use**: Sequential workflows where one agent must complete before the next begins, with precondition validation.

**Best for**: Multi-step pipelines, agent specialization chains, escalation workflows.

### Implementation

```python
from langgraph_swarm import create_handoff_tool
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

# Create handoff tool with precondition description
handoff_to_reviewer = create_handoff_tool(
    agent_name="reviewer",
    description="Transfer to reviewer only after analysis is complete"
)

# Analyst agent hands off when done
analyst = create_react_agent(
    model,
    tools=[analyze_data, handoff_to_reviewer],
    prompt="Analyze data thoroughly, then hand off to reviewer."
)

# Reviewer receives control via handoff
reviewer = create_react_agent(
    model,
    tools=[approve_result, request_revision],
    prompt="Review the analyst's findings and approve or request revision."
)
```

### When Handoffs vs Swarm

- **Handoff**: Sequential, one agent active at a time, precondition checks enforced via tool descriptions. Use for linear pipelines where order matters.
- **Swarm**: Parallel-capable, multiple agents can be active, peer-to-peer. Use for exploratory workflows without a fixed sequence.

---

## 7. Router Pattern

**When to use**: Classify input then dispatch to a specialist, with optional synthesis. No iterative decision-making needed.

**Best for**: Intent routing, domain triage, fan-out to specialists.

### Implementation

```python
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from typing import Literal

def classifier_node(state: State) -> Command[Literal["sql_agent", "python_agent", "general_agent"]]:
    """Classify intent and route to the right specialist."""
    intent = llm.invoke(f"Classify this task: {state['task']}. Reply with: sql, python, or general")
    route_map = {"sql": "sql_agent", "python": "python_agent", "general": "general_agent"}
    return Command(
        update={"intent": intent.content},
        goto=route_map.get(intent.content.strip(), "general_agent")
    )

# Parallel routing with Send
from langgraph.types import Send

def parallel_router(state: State) -> list[Send]:
    """Route to multiple specialists simultaneously."""
    return [
        Send("sql_agent", {**state, "focus": "data"}),
        Send("python_agent", {**state, "focus": "logic"})
    ]

workflow = StateGraph(State)
workflow.add_node("classify", classifier_node)
workflow.add_node("sql_agent", sql_agent_node)
workflow.add_node("python_agent", python_agent_node)
workflow.add_node("general_agent", general_agent_node)
workflow.set_entry_point("classify")
```

---

## 8. Skills-Based Multi-Agent

**When to use**: Progressive disclosure of capabilities. Load specialized prompts and tools on demand rather than giving every agent access to everything.

**Best for**: Large tool libraries, cost reduction, composable agent capabilities.

### Implementation

```python
from langgraph.prebuilt import create_react_agent

SKILL_REGISTRY = {
    "sql": {"tools": [run_sql, explain_query], "prompt": "You are a SQL specialist."},
    "python": {"tools": [execute_code, lint_code], "prompt": "You are a Python specialist."},
    "research": {"tools": [web_search, summarize], "prompt": "You are a research specialist."},
}

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialist skill set for the current task."""
    if skill_name not in SKILL_REGISTRY:
        return f"Unknown skill: {skill_name}. Available: {list(SKILL_REGISTRY.keys())}"
    skill = SKILL_REGISTRY[skill_name]
    # Dynamically bind tools to the agent for this turn
    return f"Skill '{skill_name}' loaded. Prompt: {skill['prompt']}"

# Base agent with skill-loading capability
base_agent = create_react_agent(
    model,
    tools=[load_skill, *base_tools],
    prompt="You have access to specialized skills. Load the appropriate skill before proceeding."
)
```

This pattern is lighter-weight than spawning full subagents: the base agent selects and applies skill context within a single execution rather than delegating to separate processes.
