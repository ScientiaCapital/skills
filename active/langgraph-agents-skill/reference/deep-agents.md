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

model = ChatAnthropic(model="claude-opus-4-5-20251101")

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

Deep Agents works best with Anthropic models:

```python
from langchain_anthropic import ChatAnthropic

# Production config
model = ChatAnthropic(
    model="claude-opus-4-5-20251101",  # Or claude-sonnet-4-5-20250929
    max_tokens=4096,
    temperature=0.7,
    # Extended thinking for complex reasoning
    extra_headers={"anthropic-beta": "extended-thinking-2025-04-16"}
)

agent = create_deep_agent(model=model)
```

### Model Selection by Task

```python
# Complex reasoning / architecture
opus = ChatAnthropic(model="claude-opus-4-5-20251101")

# Fast execution / simple tasks
sonnet = ChatAnthropic(model="claude-sonnet-4-5-20250929")

# Route by task complexity
model = opus if task.requires_deep_reasoning else sonnet
```

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
backend = CompositeBackend({
    "/scratch/": StateBackend(),
    "/memories/": StoreBackend(store=RedisStore(url="redis://localhost:6379")),
})

# Model
model = ChatAnthropic(model="claude-opus-4-5-20251101")

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
