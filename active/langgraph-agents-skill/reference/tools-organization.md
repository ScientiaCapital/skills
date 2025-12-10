# Tools Organization - LangGraph Agents

## Level 3 Reference: Tool Architecture Patterns

This guide shows how to organize LangGraph tools into modular, testable components using patterns from production agent systems.

---

## Modular File Structure

### Domain-Based Organization
```
tools/
├── __init__.py           # Export all tool collections
├── research.py           # Web search, knowledge retrieval
├── data.py              # Database, file operations
├── communication.py     # Email, Slack, webhooks
└── analysis.py          # LLM-based processing
```

### Collection Functions Pattern
```python
# tools/research.py
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults

def create_research_tools() -> list:
    """Factory function for research tools"""
    return [
        tavily_search(),
        wikipedia_lookup(),
        arxiv_search()
    ]

@tool
def tavily_search(query: str) -> str:
    """Search the web for current information"""
    search = TavilySearchResults(max_results=3)
    return search.invoke({"query": query})
```

---

## Tool Decorator Patterns

### Basic Tool
```python
@tool
def fetch_user_data(user_id: str) -> dict:
    """Retrieve user profile from database

    Args:
        user_id: Unique user identifier
    """
    # Implementation
    return {"id": user_id, "name": "..."}
```

### Content and Artifact Response
```python
@tool(response_format="content_and_artifact")
def analyze_sales_data(query: str) -> tuple[str, dict]:
    """Analyze sales data and return summary + full results

    Returns:
        tuple: (human_readable_summary, structured_data)
    """
    # Replace with your SQL/database library
    results = run_sql_query(query)  # e.g., sqlalchemy, psycopg2
    summary = f"Found {len(results)} sales records"
    artifact = {"rows": results, "total": sum(r['amount'] for r in results)}
    return summary, artifact
```

### Async Tools
```python
@tool
async def send_email(to: str, subject: str, body: str) -> str:
    """Send email notification (async)"""
    # Replace EmailClient with your async email library (e.g., aiosmtplib)
    async with EmailClient() as client:
        await client.send(to=to, subject=subject, body=body)
    return f"Email sent to {to}"
```

---

## Testing Tools

### Unit Test Pattern
```python
# tests/test_tools.py
import pytest
from tools.research import tavily_search

def test_tavily_search():
    result = tavily_search.invoke({"query": "LangGraph tutorial"})
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_async_tool():
    result = await send_email.ainvoke({
        "to": "test@example.com",
        "subject": "Test",
        "body": "Test message"
    })
    assert "sent" in result.lower()
```

### Mock External Services
```python
from unittest.mock import patch, MagicMock

def test_tool_with_api_call():
    with patch('tools.research.TavilySearchResults') as mock_tavily:
        mock_tavily.return_value.invoke.return_value = "Mocked results"
        result = tavily_search.invoke({"query": "test"})
        assert result == "Mocked results"
```

---

## Best Practices

### 1. Naming Conventions
- **Verbs for actions**: `send_email`, `fetch_data`, `analyze_report`
- **Clear scope**: `search_arxiv_papers` not just `search`
- **Domain prefix**: `sql_query_database`, `slack_post_message`

### 2. Error Handling
```python
import requests
from langchain_core.tools import tool

@tool
def safe_api_call(endpoint: str) -> str:
    """Call external API with error handling"""
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        return "Error: API request timed out"
    except requests.RequestException as e:
        return f"Error: {str(e)}"
```

### 3. Tool Documentation
```python
@tool
def calculate_roi(investment: float, returns: float, years: int) -> dict:
    """Calculate return on investment metrics

    Args:
        investment: Initial investment amount (USD)
        returns: Total returns (USD)
        years: Investment period in years

    Returns:
        dict with keys: roi_percentage, annualized_return, profit

    Example:
        >>> calculate_roi(10000, 15000, 3)
        {'roi_percentage': 50.0, 'annualized_return': 14.47, 'profit': 5000}
    """
    profit = returns - investment
    roi = (profit / investment) * 100
    annualized = ((returns / investment) ** (1/years) - 1) * 100
    return {"roi_percentage": roi, "annualized_return": annualized, "profit": profit}
```

### 4. Tool Registry Pattern
```python
# tools/__init__.py
from .research import create_research_tools
from .data import create_data_tools
from .communication import create_communication_tools

def get_all_tools() -> list:
    """Get all available tools"""
    return [
        *create_research_tools(),
        *create_data_tools(),
        *create_communication_tools()
    ]

def get_tools_for_agent(agent_type: str) -> list:
    """Get tools for specific agent role"""
    tool_map = {
        "researcher": create_research_tools(),
        "analyst": create_data_tools(),
        "communicator": create_communication_tools()
    }
    return tool_map.get(agent_type, [])
```

---

## Related References
- `graph-architecture.md` - How to attach tools to graph nodes
- `agent-state-management.md` - Passing tool results through state
