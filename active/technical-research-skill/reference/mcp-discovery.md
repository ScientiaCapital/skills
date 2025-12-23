# MCP Discovery Guide

## What is MCP?

Model Context Protocol (MCP) enables LLMs to interact with external tools, data sources, and services through a standardized interface.

**Key concepts:**
- **Server:** Provides tools/resources to LLMs
- **Client:** Connects to servers (Claude Desktop, Cursor, etc.)
- **Tools:** Functions the LLM can call
- **Resources:** Data the LLM can read

---

## Discovery Workflow

### Step 1: Check Existing MCP Servers

**Tim's mcp-server-cookbook:**
```
/Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook/
```

**Already configured servers:**
Check `~/.claude/claude_desktop_config.json` for active servers.

### Step 2: Search Official MCP Servers

**Official repository:**
https://github.com/modelcontextprotocol/servers

**Categories:**
- Database (PostgreSQL, SQLite, etc.)
- File systems
- Web/API integrations
- Developer tools

### Step 3: Search Community Servers

**GitHub search queries:**
```
"mcp server" [capability] language:python
"fastmcp" [capability]
"model context protocol" [capability]
```

**Awesome lists:**
- Search for "awesome-mcp" repositories
- Check MCP Discord for recommendations

### Step 4: Evaluate or Build

Decision tree:
```
Found existing server?
├─► Yes, well-maintained → USE IT
├─► Yes, needs updates → FORK & MODIFY
├─► No, but similar exists → ADAPT
└─► No → BUILD WITH FASTMCP
```

---

## MCP Server Evaluation Criteria

### Must-Have

| Criteria | Check |
|----------|-------|
| Python or TypeScript | ☐ |
| Active maintenance (<6 months) | ☐ |
| Clear documentation | ☐ |
| Error handling | ☐ |
| Security considerations | ☐ |

### Nice-to-Have

| Criteria | Check |
|----------|-------|
| Type hints | ☐ |
| Tests included | ☐ |
| Docker support | ☐ |
| Config via env vars | ☐ |
| Async support | ☐ |

### Red Flags

- No updates in >1 year
- No error handling
- Hardcoded credentials
- No documentation
- Depends on deprecated packages

---

## Building with FastMCP

### When to Build

- No existing server for your need
- Existing servers are poorly maintained
- Need custom integration with your stack
- Want tighter control over security

### FastMCP Quickstart

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description of what this tool does."""
    return f"Processed: {param}"

@mcp.resource("resource://my-data")
async def get_my_data() -> str:
    """Returns some data."""
    return "data content"

if __name__ == "__main__":
    mcp.run()
```

### Project Structure

```
my-mcp-server/
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── server.py      # FastMCP server
│       ├── tools.py       # Tool implementations
│       └── resources.py   # Resource implementations
├── tests/
├── pyproject.toml
├── README.md
└── .env.example
```

---

## Common MCP Server Categories

### Data & Databases

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-postgres | PostgreSQL queries | Stable |
| mcp-server-sqlite | SQLite operations | Stable |
| mcp-server-supabase | Supabase integration | Community |

### File Systems

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-filesystem | Local file access | Official |
| mcp-server-gdrive | Google Drive | Community |
| mcp-server-s3 | AWS S3 | Community |

### Web & APIs

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-fetch | HTTP requests | Official |
| mcp-server-brave | Brave search | Official |
| mcp-server-github | GitHub API | Community |

### Developer Tools

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-git | Git operations | Official |
| mcp-server-docker | Container management | Community |
| mcp-server-kubernetes | K8s operations | Community |

---

## Integration with Claude Desktop

### Configuration File Location

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Configuration Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "my_server"],
      "env": {
        "API_KEY": "xxx"
      }
    }
  }
}
```

### Common Patterns

**Python package:**
```json
{
  "server-name": {
    "command": "uvx",
    "args": ["my-mcp-server"]
  }
}
```

**Local development:**
```json
{
  "server-name": {
    "command": "/path/to/venv/bin/python",
    "args": ["-m", "src.server"],
    "cwd": "/path/to/project"
  }
}
```

**With environment variables:**
```json
{
  "server-name": {
    "command": "python",
    "args": ["-m", "server"],
    "env": {
      "DATABASE_URL": "postgres://...",
      "API_KEY": "${API_KEY}"
    }
  }
}
```

---

## Debugging MCP Servers

### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Tools Locally

```python
# test_tools.py
import asyncio
from my_server.tools import my_tool

async def test():
    result = await my_tool("test input")
    print(result)

asyncio.run(test())
```

### Check Server Status

In Claude Desktop:
1. Open Developer Tools
2. Check Console for MCP errors
3. Look for connection issues

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Server not starting | Python path | Use absolute path |
| Tools not showing | Import error | Check logs |
| Timeout errors | Slow operations | Add async, increase timeout |
| Auth failures | Wrong env vars | Check .env loading |

---

## Security Considerations

### Environment Variables

```python
# Good: Load from environment
import os
api_key = os.environ.get("API_KEY")

# Bad: Hardcoded
api_key = "sk-xxx"  # NEVER DO THIS
```

### Input Validation

```python
from pydantic import BaseModel, validator

class ToolInput(BaseModel):
    path: str
    
    @validator('path')
    def validate_path(cls, v):
        if '..' in v or v.startswith('/'):
            raise ValueError("Invalid path")
        return v
```

### Scope Limitation

```python
# Limit file access to specific directories
ALLOWED_DIRS = ["/Users/tmkipper/Desktop/tk_projects"]

def is_allowed_path(path: str) -> bool:
    return any(path.startswith(d) for d in ALLOWED_DIRS)
```

---

## MCP Server Template

```python
"""
My MCP Server
=============

Tools:
- tool_name: Description

Resources:
- resource://name: Description
"""

from fastmcp import FastMCP
from pydantic import BaseModel
import os

# Configuration
class Config(BaseModel):
    api_key: str = os.environ.get("API_KEY", "")

config = Config()
mcp = FastMCP("my-server")

# Tools
@mcp.tool()
async def my_tool(param: str) -> str:
    """
    Description of the tool.
    
    Args:
        param: What this parameter does
        
    Returns:
        What the tool returns
    """
    # Implementation
    return f"Result: {param}"

# Resources
@mcp.resource("resource://config")
async def get_config() -> str:
    """Returns current configuration."""
    return config.model_dump_json()

if __name__ == "__main__":
    mcp.run()
```
