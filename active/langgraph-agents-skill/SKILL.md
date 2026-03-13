---
name: "langgraph-agents"
description: "Multi-agent systems with LangGraph - supervisor/swarm/handoff/router patterns, state coordination, Deep Agents, guardrails, testing, observability, deployment. Use when building multi-agent workflows, coordinating agents, or need cost-optimized orchestration. Uses Claude, DeepSeek, Gemini (no OpenAI)."
---

<objective>
Build production-grade multi-agent systems with LangGraph using supervisor, swarm, handoff, router, or master patterns. Enables cost-optimized orchestration with multi-provider routing (Claude, DeepSeek, Gemini - NO OpenAI), guardrails, durable execution, observability, and scalable agent coordination.
</objective>

<quick_start>
**State schema (foundation):**
```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]  # Auto-merge
    next_agent: str  # For handoffs
```

**Pattern selection:**
| Pattern | When | Agents |
|---------|------|--------|
| Supervisor | Clear hierarchy | 3-10 |
| Swarm | Peer collaboration | 5-15 |
| Handoff | Sequential pipeline | 2-5 |
| Router | Classify and dispatch | 2-10 |
| Master | Learning systems | 10-30+ |

**API choice:** Graph API (explicit nodes/edges) vs Functional API (`@entrypoint`/`@task` decorators)

**Key packages:** `pip install langchain langgraph langgraph-supervisor langgraph-swarm langchain-mcp-adapters`
</quick_start>

<success_criteria>
Multi-agent system is successful when:
- State uses `Annotated[..., add_messages]` for proper message merging
- Termination conditions prevent infinite loops
- Routing uses conditional edges (not hardcoded paths) OR Functional API tasks
- Cost optimization: simple tasks → cheaper models (DeepSeek)
- Complex reasoning → quality models (Claude)
- NO OpenAI used anywhere
- Checkpointers enabled for context preservation
- Human-in-the-loop: interrupt() for approval workflows
- Guardrails: PII detection, budget limits, call limits
- MCP tools standardized via MultiServerMCPClient when appropriate
- Observability: LangSmith tracing enabled in production
</success_criteria>

<core_content>
Production-tested patterns for building scalable, cost-optimized multi-agent systems with LangGraph and LangChain.

## When to Use This Skill

**Symptoms:**
- "State not updating correctly between agents"
- "Agents not coordinating properly"
- "LLM costs spiraling out of control"
- "Need to choose between supervisor vs swarm vs handoff patterns"
- "Unclear how to structure agent state schemas"
- "Agents losing context or repeating work"
- "Need guardrails for PII, budget, or safety"
- "How to test agent graphs"
- "Need durable execution with crash recovery"
- "Setting up LangSmith tracing / observability"
- "Deploying LangGraph to production"

**Use Cases:**
- Multi-agent systems with 3+ specialized agents
- Complex workflows requiring orchestration
- Cost-sensitive production deployments
- Self-learning or adaptive agent systems
- Enterprise applications with multiple LLM providers

## Quick Reference: Orchestration Pattern Selection

| Pattern | Use When | Complexity | Reference |
|---------|----------|------------|-----------|
| **Supervisor** | Clear hierarchy, centralized routing | Low-Medium | `reference/orchestration-patterns.md` |
| **Swarm** | Peer collaboration, dynamic handoffs | Medium | `reference/orchestration-patterns.md` |
| **Handoff** | Sequential pipelines, escalation | Low | `reference/orchestration-patterns.md` |
| **Router** | Classify-and-dispatch, fan-out | Low | `reference/orchestration-patterns.md` |
| **Skills** | Progressive disclosure, on-demand | Low | `reference/orchestration-patterns.md` |
| **Master** | Learning systems, complex workflows | High | `reference/orchestration-patterns.md` |

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

### 2. Multi-Provider Configuration (via lang-core)
```python
# Use lang-core for unified provider access (NO OPENAI)
from lang_core.providers import get_llm_for_task, LLMPriority

llm_cheap = get_llm_for_task(priority=LLMPriority.COST)     # DeepSeek
llm_smart = get_llm_for_task(priority=LLMPriority.QUALITY)  # Claude
llm_fast = get_llm_for_task(priority=LLMPriority.SPEED)     # Cerebras
llm_local = get_llm_for_task(priority=LLMPriority.LOCAL)    # Ollama
```
**Deep dive:** `reference/base-agent-architecture.md`, `reference/cost-optimization.md`

### 3. Supervisor Pattern
```python
from langgraph_supervisor import create_supervisor  # pip install langgraph-supervisor
from langgraph.prebuilt import create_react_agent

research_agent = create_react_agent(model, tools=research_tools, prompt="Research specialist")
writer_agent = create_react_agent(model, tools=writer_tools, prompt="Content writer")

supervisor = create_supervisor(agents=[research_agent, writer_agent], model=model)
result = supervisor.invoke({"messages": [("user", "Write article about LangGraph")]})
```

### 4. Swarm Pattern
```python
from langgraph_swarm import create_swarm, create_handoff_tool  # pip install langgraph-swarm

handoff_to_bob = create_handoff_tool(agent_name="Bob", description="Transfer for Python tasks")
alice = create_react_agent(model, tools=[query_db, handoff_to_bob], prompt="SQL expert")
bob = create_react_agent(model, tools=[execute_code], prompt="Python expert")

swarm = create_swarm(agents=[alice, bob], default_active_agent="Alice")
```

### 5. Functional API (Alternative to Graph)
```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver

@task
def research(query: str) -> str:
    return f"Results for: {query}"

@entrypoint(checkpointer=InMemorySaver())
def workflow(query: str) -> dict:
    result = research(query).result()
    return {"output": result}
```
**Deep dive:** `reference/functional-api.md` (durable execution, time travel, testing)

### 6. MCP Tool Integration
```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient(
    {"tools": {"transport": "stdio", "command": "python", "args": ["./mcp_server.py"]}}
) as client:
    tools = await client.get_tools()
    agent = create_react_agent(model, tools=tools)
```
**Deep dive:** `reference/mcp-integration.md`

### 7. Deep Agents Framework (Production)
```python
from deep_agents import create_deep_agent
from deep_agents.backends import CompositeBackend, StateBackend, StoreBackend

backend = CompositeBackend({
    "/workspace/": StateBackend(),      # Ephemeral
    "/memories/": StoreBackend()        # Persistent
})
agent = create_deep_agent(
    model=ChatAnthropic(model="claude-opus-4-6"),
    backend=backend,
    interrupt_on=["deploy", "delete"],
    skills_dirs=["./skills/"]
)
```
**Deep dive:** `reference/deep-agents.md` (subagents, skills, long-term memory)

### 8. Guardrails
```python
# Recursion limit prevents runaway agents (default: 25 steps)
config = {"recursion_limit": 25, "configurable": {"thread_id": "user-123"}}
result = graph.invoke(input_data, config=config)

# Add guardrail nodes for PII, safety checks, HITL — see reference
```
**Deep dive:** `reference/guardrails.md` (input/output validation, tripwires, graph-node guardrails)

## Reference Files (14 Deep Dives)

**Architecture:**
- **`reference/state-schemas.md`** - TypedDict, Annotated reducers, multi-level state
- **`reference/base-agent-architecture.md`** - Multi-provider setup, agent templates
- **`reference/tools-organization.md`** - Modular tool design, InjectedState/InjectedStore

**Orchestration:**
- **`reference/orchestration-patterns.md`** - Supervisor, swarm, handoff, router, skills, master, HITL
- **`reference/context-engineering.md`** - Three context types, memory compaction, Anthropic best practices
- **`reference/cost-optimization.md`** - Provider routing, caching, token budgets, fallback chains

**APIs:**
- **`reference/functional-api.md`** - @entrypoint/@task, durable execution, time travel, testing
- **`reference/mcp-integration.md`** - MultiServerMCPClient, async context manager, tool composition
- **`reference/deep-agents.md`** - Harness, backends, subagents, skills, long-term memory
- **`reference/streaming-patterns.md`** - 5 streaming modes, v2 format, custom streaming

**Production:**
- **`reference/guardrails.md`** - PII detection, prompt injection, budget tripwires, output filtering
- **`reference/testing-patterns.md`** - Unit/integration testing, mocking, snapshot tests, CI/CD
- **`reference/observability.md`** - LangSmith tracing, custom metrics, evaluation, monitoring
- **`reference/deployment-patterns.md`** - App structure, local server, LangGraph Platform, Docker

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| State not updating | Add `Annotated[..., add_messages]` reducer |
| Infinite loops | Add termination condition or set `recursion_limit` in config |
| High costs | Route simple tasks to cheaper models; use fallback chains |
| Context loss | Use checkpointers or memory systems |
| Wrong imports | `create_supervisor` from `langgraph_supervisor`, not `langgraph.prebuilt` |
| Wrong imports | `create_swarm` from `langgraph_swarm`, not `langgraph.prebuilt` |
| MCP API mismatch | Use `await client.get_tools()`, not `get_langchain_tools()` |
| PII leakage | Add PII redaction guard node (see `reference/guardrails.md`) |
| No observability | Set `LANGSMITH_TRACING=true` for zero-config tracing |
| Fragile agents | Add guardrails: call limits, budget tripwires, structured output |

## lang-core Integration

For production deployments, use **lang-core** for:
- **Middleware**: Cost tracking, budget enforcement, retry, caching, PII safety
- **LangSmith**: Unified tracing with `@traced_agent` decorators
- **Providers**: Auto-selection via `get_llm_for_task(priority=...)`
- **Celery**: Background agent execution with progress tracking
- **Redis**: Distributed locks, rate limiting, event pub/sub

```python
from lang_core import traced_agent, get_llm_for_task, LLMPriority
from lang_core.middleware import budget_enforcement_middleware

@traced_agent("QualificationAgent", tags=["sales"])
async def run_qualification(data):
    llm = get_llm_for_task(priority=LLMPriority.SPEED)
    # ... agent logic
```
