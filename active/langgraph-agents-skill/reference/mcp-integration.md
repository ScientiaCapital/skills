# MCP Integration Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Using Model Context Protocol tools with LangGraph agents

## Overview

MCP (Model Context Protocol) standardizes tool interfaces. LangChain's `langchain-mcp-adapters` package bridges MCP servers with LangChain/LangGraph agents.

---

## MultiServerMCPClient

The primary interface for connecting to MCP servers:

```python
from langchain_mcp_adapters import MultiServerMCPClient

# Create client
client = MultiServerMCPClient()

# Add servers
client.add_server(
    name="local_tools",
    transport="stdio",
    command="python",
    args=["./mcp_server.py"]
)

client.add_server(
    name="remote_tools",
    transport="http",
    url="https://mcp.example.com"
)

# Get LangChain-compatible tools
tools = client.get_langchain_tools()
```

---

## Transport Mechanisms

### stdio (Local Process)

```python
client.add_server(
    name="file_tools",
    transport="stdio",
    command="npx",
    args=["-y", "@anthropic/mcp-server-files"]
)
```

- Spawns local process
- Communicates via stdin/stdout
- Best for: Local development, single-machine deployment

### HTTP (Remote Server)

```python
client.add_server(
    name="api_tools",
    transport="http",
    url="https://api.example.com/mcp",
    headers={"Authorization": "Bearer ${API_KEY}"}
)
```

- Connects to HTTP endpoint
- Best for: Distributed systems, shared tool servers

### SSE (Server-Sent Events)

```python
client.add_server(
    name="streaming_tools",
    transport="sse",
    url="https://stream.example.com/mcp"
)
```

- Real-time streaming connection
- Best for: Long-running operations with progress updates

---

## Using MCP Tools with Agents

### With create_react_agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Setup
client = MultiServerMCPClient()
client.add_server("tools", "stdio", command="python", args=["./mcp_tools.py"])
tools = client.get_langchain_tools()

model = ChatAnthropic(model="claude-sonnet-4-5-20250929")

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

# Get MCP tools
tools = client.get_langchain_tools()

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
mcp_tools = client.get_langchain_tools()

# Combine
all_tools = [calculate_sum] + mcp_tools

agent = create_react_agent(model, tools=all_tools)
```

### Filtering MCP Tools

```python
# Get all tools
all_mcp_tools = client.get_langchain_tools()

# Filter to specific tools
allowed_tools = ["read_file", "write_file", "search"]
filtered_tools = [t for t in all_mcp_tools if t.name in allowed_tools]

agent = create_react_agent(model, tools=filtered_tools)
```

---

## Server Management

### Lifecycle Management

```python
async with MultiServerMCPClient() as client:
    client.add_server("tools", "stdio", command="python", args=["./server.py"])
    tools = client.get_langchain_tools()

    # Use tools...
    result = agent.invoke(...)

# Servers automatically cleaned up
```

### Error Handling

```python
try:
    client.add_server("unreliable", "http", url="https://flaky.example.com")
    tools = client.get_langchain_tools()
except MCPConnectionError as e:
    # Fallback to local tools
    tools = [local_fallback_tool]
```

### Health Checks

```python
# Check server status
for server in client.servers:
    status = client.ping(server.name)
    if not status.healthy:
        logger.warning(f"Server {server.name} unhealthy: {status.error}")
```

---

## Common MCP Servers

### File Operations
```python
client.add_server(
    "files",
    "stdio",
    command="npx",
    args=["-y", "@anthropic/mcp-server-files", "/allowed/path"]
)
```

### Web Search
```python
client.add_server(
    "brave",
    "stdio",
    command="npx",
    args=["-y", "@anthropic/mcp-server-brave"],
    env={"BRAVE_API_KEY": os.environ["BRAVE_API_KEY"]}
)
```

### Database
```python
client.add_server(
    "postgres",
    "stdio",
    command="npx",
    args=["-y", "@anthropic/mcp-server-postgres"],
    env={"DATABASE_URL": os.environ["DATABASE_URL"]}
)
```

### GitHub
```python
client.add_server(
    "github",
    "stdio",
    command="npx",
    args=["-y", "@anthropic/mcp-server-github"],
    env={"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]}
)
```

---

## Production Patterns

### Connection Pooling

```python
class MCPToolProvider:
    _instance = None

    @classmethod
    def get_client(cls) -> MultiServerMCPClient:
        if cls._instance is None:
            cls._instance = MultiServerMCPClient()
            cls._setup_servers()
        return cls._instance

    @classmethod
    def _setup_servers(cls):
        cls._instance.add_server("files", "stdio", ...)
        cls._instance.add_server("search", "http", ...)

# Usage
tools = MCPToolProvider.get_client().get_langchain_tools()
```

### Environment-Based Configuration

```python
import os

MCP_CONFIG = {
    "development": {
        "files": {"transport": "stdio", "command": "python", "args": ["./dev_server.py"]},
    },
    "production": {
        "files": {"transport": "http", "url": os.environ.get("MCP_FILES_URL")},
    }
}

env = os.environ.get("ENVIRONMENT", "development")
config = MCP_CONFIG[env]

client = MultiServerMCPClient()
for name, server_config in config.items():
    client.add_server(name, **server_config)
```

---

## Best Practices

1. **Use context managers**: `async with MultiServerMCPClient()` ensures cleanup
2. **Filter tools**: Only expose tools the agent needs
3. **Handle failures**: MCP servers can fail; have fallback strategies
4. **Environment isolation**: Different server configs for dev/prod
5. **Pool connections**: Reuse client instances across invocations
6. **Monitor health**: Implement health checks for remote servers

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server won't start | Check command path, permissions, dependencies |
| Tool not found | Verify server exposes tool, check `get_langchain_tools()` output |
| Connection timeout | Increase timeout, check network, verify URL |
| Auth failures | Check API keys in env vars, verify headers |
