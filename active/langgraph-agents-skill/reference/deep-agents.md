# Deep Agents Framework Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Building production agent systems with file management, persistence, and skills

## Overview

Deep Agents is a production-ready framework built on LangGraph that provides:
- **Harness**: Pre-configured agent with 6 built-in tools
- **Backends**: Flexible storage (ephemeral, persistent, composite)
- **Middleware**: TodoList, Filesystem, SubAgent capabilities
- **Skills**: Directory-based skill loading

---

## Harness Pattern

The harness is a complete agent setup with built-in tools:

```python
from deep_agents import create_deep_agent
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-opus-4-6")

agent = create_deep_agent(
    model=model,
    system_prompt="You are a helpful assistant.",
    interrupt_on=["deploy", "delete"],  # HITL for dangerous ops
    skills_dirs=["./skills/"]
)

# Invoke
result = agent.invoke({
    "messages": [{"role": "user", "content": "Create a new project structure"}]
})
```

### Built-in Tools (6)

| Tool | Purpose |
|------|---------|
| `read_file` | Read files from configured backends |
| `write_file` | Write/update files |
| `list_directory` | List directory contents |
| `search_files` | Search for patterns in files |
| `execute_command` | Run shell commands (sandboxed) |
| `web_search` | Search the web for information |

---

### Full API Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `BaseChatModel` | required | LLM instance (ChatAnthropic, ChatGroq, etc.) |
| `system_prompt` | `str` | `None` | System message for the agent |
| `tools` | `list[BaseTool]` | `[]` | Additional tools beyond built-in 6 |
| `backend` | `BackendProtocol` | `StateBackend()` | Storage backend configuration |
| `middleware` | `list[AgentMiddleware]` | `[]` | Middleware stack |
| `interrupt_on` | `dict[str, bool]` | `{}` | Tool-level HITL configuration |
| `checkpointer` | `BaseCheckpointSaver` | `None` | Persistence backend |
| `store` | `BaseStore` | `None` | Long-term cross-thread memory |
| `skills_dirs` | `list[str]` | `[]` | Directories to scan for skills |
| `memory` | `list[str]` | `[]` | Paths to AGENTS.md files (always loaded) |
| `subagents` | `list[SubAgent]` | `[]` | Subagent configurations |
| `name` | `str` | `"deep-agent"` | Agent name (for tracing/logging) |

---

## Backend Configurations

Backends control where agent data lives:

### StateBackend (Ephemeral)

```python
from deep_agents.backends import StateBackend

backend = StateBackend()  # Data lives in workflow state only
```

- Data lost when workflow completes
- Good for: Scratch space, temporary processing

### StoreBackend (Persistent)

```python
from deep_agents.backends import StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()  # Or Redis, PostgreSQL
backend = StoreBackend(store=store, namespace="project_123")
```

- Data persists across invocations
- Good for: Long-term memory, project files

### FilesystemBackend (Local Disk)

```python
from deep_agents.backends import FilesystemBackend

backend = FilesystemBackend(root_path="/tmp/agent_workspace")
```

- Direct filesystem access
- Good for: Development, local file operations

### CompositeBackend (Production Pattern)

```python
from deep_agents.backends import CompositeBackend, StateBackend, StoreBackend

backend = CompositeBackend({
    "/workspace/": StateBackend(),      # Ephemeral scratch space
    "/memories/": StoreBackend(),       # Persistent long-term
    "/outputs/": FilesystemBackend()    # Direct file output
})
```

**Path routing**: Agent sees unified filesystem, backend routes by path prefix.

---

## Middleware Stack

### TodoList Middleware

Gives agent task tracking capabilities:

```python
from deep_agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model=model,
    middleware=[TodoListMiddleware()]
)

# Agent can now:
# - Create todos: {"action": "create_todo", "task": "Research competitors"}
# - Update status: {"action": "update_todo", "id": 1, "status": "done"}
# - List todos: {"action": "list_todos"}
```

### Filesystem Middleware

Enhanced file operations with validation:

```python
from deep_agents.middleware import FilesystemMiddleware

agent = create_deep_agent(
    model=model,
    middleware=[
        FilesystemMiddleware(
            allowed_extensions=[".py", ".md", ".json"],
            max_file_size=1_000_000,  # 1MB limit
            blocked_paths=["/etc", "/root"]
        )
    ]
)
```

### SubAgent Middleware

Spawn child agents for parallel work:

```python
from deep_agents.middleware import SubAgentMiddleware

agent = create_deep_agent(
    model=model,
    middleware=[
        SubAgentMiddleware(
            max_concurrent=5,
            timeout_seconds=300
        )
    ]
)

# Agent can spawn: {"action": "spawn_agent", "task": "Research X", "type": "researcher"}
```

---

## Skills Integration

### Skills Progressive Disclosure

Deep Agents loads skills using a two-phase approach:

1. **Frontmatter scan**: Read only YAML frontmatter to check relevance
2. **Full load**: Read complete SKILL.md only when skill matches current task

```
skills/
└── skill-name/
    ├── SKILL.md          # Required — frontmatter + instructions
    ├── script.py         # Optional — executable scripts
    └── reference-docs/   # Optional — deep-dive references
```

**SKILL.md frontmatter (required fields):**
```yaml
---
name: "my-skill"
description: "Max 1,024 chars — used for relevance matching"
---
```

**Source precedence:** Later sources override earlier (last-wins).

**Skills vs tools vs memory:**
- Skills: bundled capabilities with contextual instructions (loaded on-demand)
- Tools: atomic actions the agent can call
- Memory (AGENTS.md): persistent context, always loaded every invocation

Skills are loaded from directories:

```
./skills/
  researcher/
    SKILL.md        # Instructions for this skill
    prompts.yaml    # Optional prompt templates
  writer/
    SKILL.md
```

```python
agent = create_deep_agent(
    model=model,
    skills_dirs=["./skills/"],
    active_skills=["researcher", "writer"]  # Optional: limit active skills
)
```

### Skill Discovery

Agent sees available skills and can invoke them:
```python
# Agent has access to skill_invoke tool
{"tool": "skill_invoke", "skill": "researcher", "input": "Find LangGraph patterns"}
```

---

## Subagent Configuration

Two subagent types for context quarantine — parent receives only final result:

```python
from deep_agents import CompiledSubAgent

# Dict-based subagent (simple)
research_subagent = {
    "name": "research-agent",
    "description": "In-depth research using web search",
    "system_prompt": "You are a thorough researcher...",
    "tools": [internet_search],
    "model": "claude-sonnet-4-6",
}

# CompiledSubAgent (complex LangGraph workflows)
custom_subagent = CompiledSubAgent(
    name="data-analyzer",
    description="Analyze datasets with custom pipeline",
    runnable=custom_compiled_graph
)

agent = create_deep_agent(
    model=model,
    subagents=[research_subagent, custom_subagent]
)
```

**Inheritance rules:**
- Custom subagents do NOT inherit parent's skills — specify `skills=` explicitly
- The default "general-purpose" subagent DOES inherit parent's skills/tools/model
- Override the default by including `name="general-purpose"` in subagents list

**Identify calling agent in tools:**
```python
agent_name = config.get("metadata", {}).get("lc_agent_name")
```

---

## Interrupt Patterns (HITL)

### Declarative Interrupts

```python
agent = create_deep_agent(
    model=model,
    interrupt_on=[
        "deploy",           # Pause on deploy actions
        "delete",           # Pause on delete actions
        "purchase",         # Pause on purchase actions
        {"pattern": "*.env"}  # Pause on .env file writes
    ]
)
```

### Handling Interrupts

```python
from langgraph.types import Command

# First invocation hits interrupt
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Deploy to production"}]},
    config={"configurable": {"thread_id": "abc"}}
)
# result["interrupt"] contains the pending action

# Resume with approval
result = agent.invoke(
    Command(resume={"approved": True}),
    config={"configurable": {"thread_id": "abc"}}
)
```

---

## Anthropic Provider Configuration

See `base-agent-architecture.md` for full provider setup. Quick reference:

| Model | Use Case |
|-------|---------|
| `claude-opus-4-6` | Complex reasoning, architecture decisions |
| `claude-sonnet-4-6` | Fast execution, general tasks |
| `claude-haiku-4-5` | Simple classification, extraction |

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    # Note: Extended thinking is now GA in Claude 4 models;
    # beta header only needed for older API versions
    # extra_headers={"anthropic-beta": "extended-thinking-2025-04-16"}
)
```

---

## Long-Term Memory via Store

Use `CompositeBackend` to route `/memories/` to a persistent `StoreBackend`:

```python
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore  # Dev
# from langgraph.store.postgres import PostgresStore  # Production

backend = CompositeBackend(
    default=StateBackend(runtime),
    routes={"/memories/": StoreBackend(runtime)}
)

agent = create_deep_agent(
    model=model,
    store=InMemoryStore(),  # or PostgresStore.from_conn_string(...)
    backend=make_backend,
    checkpointer=MemorySaver()
)
```

**Production stores:**

| Store | Package | Use Case |
|-------|---------|----------|
| `InMemoryStore` | `langgraph` | Dev/testing only |
| `PostgresStore` | `langgraph-checkpoint-postgres` | Production |
| `RedisStore` | `langgraph-checkpoint-redis` | High-throughput; `# pip install langgraph-checkpoint-redis` |

---

## Production Checklist

- [ ] Use CompositeBackend for path-based routing
- [ ] Enable interrupt_on for destructive operations
- [ ] Set max_concurrent limits on SubAgentMiddleware
- [ ] Validate file extensions with FilesystemMiddleware
- [ ] Use persistent store (Redis/PostgreSQL) for StoreBackend
- [ ] Configure skills_dirs for reusable capabilities
- [ ] Add timeout handling for long-running operations

---

## Full Example

```python
from deep_agents import create_deep_agent
from deep_agents.backends import CompositeBackend, StateBackend, StoreBackend
from deep_agents.middleware import TodoListMiddleware, SubAgentMiddleware
from langchain_anthropic import ChatAnthropic
from langgraph.store.redis import RedisStore

# Production backend
store = RedisStore.from_conn_string("redis://localhost:6379")
# await store.setup()  # Required for Redis/Postgres stores

backend = CompositeBackend({
    "/scratch/": StateBackend(),
    "/memories/": StoreBackend(store=store),
})

# Model
model = ChatAnthropic(model="claude-opus-4-6")

# Create agent
agent = create_deep_agent(
    model=model,
    backend=backend,
    middleware=[
        TodoListMiddleware(),
        SubAgentMiddleware(max_concurrent=3)
    ],
    interrupt_on=["deploy", "delete", "purchase"],
    skills_dirs=["./skills/"],
    system_prompt="You are a senior engineer. Break down complex tasks."
)

# Run with persistence
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Build a REST API for user management"}]},
    config={"configurable": {"thread_id": "project_api_001"}}
)
```
