# MCP Integration Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Using Model Context Protocol tools with LangGraph agents

## Overview

MCP (Model Context Protocol) standardizes tool interfaces. LangChain's `langchain-mcp-adapters` package bridges MCP servers with LangChain/LangGraph agents.

---

## MultiServerMCPClient

The primary interface for connecting to MCP servers:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

# Configuration-based initialization (langchain-mcp-adapters 0.1.0+)
async with MultiServerMCPClient(
    {
        "local_tools": {
            "transport": "stdio",
            "command": "python",
            "args": ["./mcp_server.py"]
        },
        "remote_tools": {
            "transport": "streamable-http",
            "url": "https://mcp.example.com/mcp"
        }
    }
) as client:
    tools = await client.get_tools()
```

Note: The `client.add_server()` pattern is deprecated. Use dict-config with `async with` context manager instead.

---

## Transport Mechanisms

### stdio (Local Process)

```python
async with MultiServerMCPClient(
    {
        "file_tools": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@anthropic/mcp-server-files"]
        }
    }
) as client:
    tools = await client.get_tools()
```

- Spawns local process
- Communicates via stdin/stdout
- Best for: Local development, single-machine deployment

### streamable-http (Remote Server)

```python
async with MultiServerMCPClient(
    {
        "api_tools": {
            "transport": "streamable-http",
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": "Bearer ${API_KEY}"}
        }
    }
) as client:
    tools = await client.get_tools()
```

- Connects to HTTP endpoint with streaming support
- Best for: Distributed systems, shared tool servers
- Note: `"sse"` transport is deprecated in the MCP spec; use `"streamable-http"` instead

---

## Using MCP Tools with Agents

### With create_react_agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient

model = ChatAnthropic(model="claude-sonnet-4-6")

async with MultiServerMCPClient(
    {"tools": {"transport": "stdio", "command": "python", "args": ["./mcp_tools.py"]}}
) as client:
    tools = await client.get_tools()

    # Create agent with MCP tools
    agent = create_react_agent(model, tools=tools)

    # Invoke
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Read the config.json file"}]
    })
```

### With Graph API

```python
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Get MCP tools (inside async with block)
tools = await client.get_tools()

# Create tool node
tool_node = ToolNode(tools)

# Add to graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("agent", should_use_tool, {
    "tools": "tools",
    "end": END
})
workflow.add_edge("tools", "agent")
```

---

## Tool Composition

### Combining MCP with Native Tools

```python
from langchain_core.tools import tool

# Native LangChain tool
@tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# MCP tools
mcp_tools = await client.get_tools()

# Combine
all_tools = [calculate_sum] + mcp_tools

agent = create_react_agent(model, tools=all_tools)
```

### Filtering MCP Tools

```python
# Get all tools
all_mcp_tools = await client.get_tools()

# Filter to specific tools
allowed_tools = ["read_file", "write_file", "search"]
filtered_tools = [t for t in all_mcp_tools if t.name in allowed_tools]

agent = create_react_agent(model, tools=filtered_tools)
```

---

## Server Management

### Lifecycle Management

```python
async with MultiServerMCPClient(
    {"tools": {"transport": "stdio", "command": "python", "args": ["./server.py"]}}
) as client:
    tools = await client.get_tools()

    # Use tools...
    result = agent.invoke(...)

# Servers automatically cleaned up on context exit
```

### Error Handling

```python
try:
    async with MultiServerMCPClient(
        {"unreliable": {"transport": "streamable-http", "url": "https://flaky.example.com/mcp"}}
    ) as client:
        tools = await client.get_tools()
except Exception as e:
    # Fallback to local tools
    tools = [local_fallback_tool]
```

---

## Common MCP Servers

### File Operations
```python
async with MultiServerMCPClient(
    {"files": {"transport": "stdio", "command": "npx", "args": ["-y", "@anthropic/mcp-server-files", "/allowed/path"]}}
) as client:
    tools = await client.get_tools()
```

### Web Search
```python
async with MultiServerMCPClient(
    {"brave": {"transport": "stdio", "command": "npx", "args": ["-y", "@anthropic/mcp-server-brave"],
               "env": {"BRAVE_API_KEY": os.environ["BRAVE_API_KEY"]}}}
) as client:
    tools = await client.get_tools()
```

### Database
```python
async with MultiServerMCPClient(
    {"postgres": {"transport": "stdio", "command": "npx", "args": ["-y", "@anthropic/mcp-server-postgres"],
                  "env": {"DATABASE_URL": os.environ["DATABASE_URL"]}}}
) as client:
    tools = await client.get_tools()
```

### GitHub
```python
async with MultiServerMCPClient(
    {"github": {"transport": "stdio", "command": "npx", "args": ["-y", "@anthropic/mcp-server-github"],
                "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]}}}
) as client:
    tools = await client.get_tools()
```

---

## Production Patterns

### Connection Pooling

```python
SERVER_CONFIG = {
    "files": {"transport": "stdio", "command": "python", "args": ["./file_server.py"]},
    "search": {"transport": "streamable-http", "url": "https://search.example.com/mcp"},
}

# Reuse config across calls; create new context per request to ensure clean lifecycle
async def get_mcp_tools():
    async with MultiServerMCPClient(SERVER_CONFIG) as client:
        return await client.get_tools()

# Usage
tools = await get_mcp_tools()
```

### Environment-Based Configuration

```python
import os

MCP_CONFIG = {
    "development": {
        "files": {"transport": "stdio", "command": "python", "args": ["./dev_server.py"]},
    },
    "production": {
        "files": {"transport": "streamable-http", "url": os.environ.get("MCP_FILES_URL")},
    }
}

env = os.environ.get("ENVIRONMENT", "development")
server_config = MCP_CONFIG[env]

async with MultiServerMCPClient(server_config) as client:
    tools = await client.get_tools()
```

---

## Best Practices

1. **Use context managers**: `async with MultiServerMCPClient({...})` ensures proper lifecycle and cleanup
2. **Dict-config pattern**: Pass server config to the constructor — do not use deprecated `add_server()`
3. **Use `get_tools()`**: The method is `await client.get_tools()`, not `get_langchain_tools()`
4. **Filter tools**: Only expose tools the agent needs to reduce token usage
5. **Handle failures**: MCP servers can fail; have fallback strategies with native LangChain tools
6. **Use `streamable-http`**: SSE transport is deprecated in the MCP spec
7. **Environment isolation**: Different server configs for dev/prod

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server won't start | Check command path, permissions, dependencies |
| Tool not found | Verify server exposes tool, check `get_tools()` output |
| Connection timeout | Increase timeout, check network, verify URL |
| Auth failures | Check API keys in env vars, verify headers |
