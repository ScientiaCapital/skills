---
name: langgraph-agents-skill
description: Use when building multi-agent systems with LangGraph/LangChain and encountering state coordination issues, orchestration pattern decisions, or cost optimization needs across LLM providers. Applies patterns from production systems with 20+ agents including supervisor/swarm/master orchestration, state schema design, multi-provider routing, and context engineering.
---

# LangGraph Multi-Agent Systems

Production-tested patterns for building scalable, cost-optimized multi-agent systems with LangGraph and LangChain.

## When to Use This Skill

**Symptoms:**
- "State not updating correctly between agents"
- "Agents not coordinating properly"
- "LLM costs spiraling out of control"
- "Need to choose between supervisor vs swarm patterns"
- "Unclear how to structure agent state schemas"
- "Agents losing context or repeating work"

**Use Cases:**
- Multi-agent systems with 3+ specialized agents
- Complex workflows requiring orchestration
- Cost-sensitive production deployments
- Self-learning or adaptive agent systems
- Enterprise applications with multiple LLM providers

## Quick Reference: Orchestration Pattern Selection

| Pattern | Use When | Agent Count | Complexity | Reference |
|---------|----------|-------------|------------|-----------|
| **Supervisor** | Clear hierarchy, centralized routing | 3-10 | Low-Medium | `reference/orchestration-patterns.md` |
| **Swarm** | Peer collaboration, dynamic handoffs | 5-15 | Medium | `reference/orchestration-patterns.md` |
| **Master** | Learning systems, complex workflows | 10-30+ | High | `reference/orchestration-patterns.md` |

## Core Patterns

### 1. State Schema (Foundation)
```python
from typing import TypedDict, Annotated, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]  # Auto-merge
    agent_type: str
    metadata: Dict[str, Any]
    next_agent: str  # For handoffs
```
**Deep dive:** `reference/state-schemas.md` (reducers, annotations, multi-level state)

### 2. Multi-Provider Configuration
```python
# Route by complexity/cost (NO OPENAI)
llm_config = {
    "cheap": ChatGroq(model="llama-3.1-8b"),       # Simple tasks
    "smart": ChatAnthropic(model="claude-sonnet"),  # Complex reasoning
    "fast": ChatCerebras(model="llama-3.3-70b")    # High throughput
}
```
**Deep dive:** `reference/base-agent-architecture.md`, `reference/cost-optimization.md`

### 3. Tool Organization
```python
# Modular, testable tools
def create_agent_with_tools(llm, tools: list):
    return create_react_agent(llm, tools, state_modifier=state_modifier)

# Group by domain
research_tools = [tavily_search, wikipedia]
data_tools = [sql_query, csv_reader]
```
**Deep dive:** `reference/tools-organization.md`

### 4. Supervisor Pattern (Centralized)
```python
members = ["researcher", "writer", "reviewer"]
system_prompt = f"Route to: {members}. Return 'FINISH' when done."
supervisor_chain = prompt | llm.bind_functions([route_function])
```

### 5. Swarm Pattern (Distributed)
```python
# Agents hand off directly
def agent_node(state):
    result = agent.invoke(state)
    return {"messages": [result], "next_agent": determine_next(result)}

workflow.add_conditional_edges("agent_a", route_to_next, {
    "agent_b": "agent_b", "agent_c": "agent_c", "end": END
})
```

## Reference Files (Deep Dives)

- **`reference/state-schemas.md`** - TypedDict, Annotated reducers, multi-level state
- **`reference/base-agent-architecture.md`** - Multi-provider setup, agent templates
- **`reference/tools-organization.md`** - Modular tool design, testing patterns
- **`reference/orchestration-patterns.md`** - Supervisor vs swarm vs master (decision matrix)
- **`reference/context-engineering.md`** - Memory compaction, just-in-time loading
- **`reference/cost-optimization.md`** - Provider routing, caching, token budgets

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| State not updating | Add `Annotated[..., add_messages]` reducer |
| Infinite loops | Add termination condition in conditional edges |
| High costs | Route simple tasks to cheaper models |
| Context loss | Use checkpointers or memory systems |
