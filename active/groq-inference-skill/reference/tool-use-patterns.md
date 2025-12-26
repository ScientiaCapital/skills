# GROQ Tool Use Patterns

Complete guide for GROQ's tool/function calling capabilities.

---

## 1. Built-In Tools (Server-Side)

GROQ's compound models provide pre-integrated tools that execute server-side.

### Available Built-In Tools

| Tool | Description | Models |
|------|-------------|--------|
| `web_search` | Real-time web search | compound-beta |
| `code_interpreter` | Execute Python code | compound-beta |
| `visit_website` | Fetch webpage content | compound-beta |

### Configuration

```python
from groq import Groq

client = Groq(api_key="gsk_...")

response = client.chat.completions.create(
    model="compound-beta",
    messages=[{"role": "user", "content": "Search for GROQ news"}],
)

# Check executed tools
if hasattr(response.choices[0].message, 'executed_tools'):
    for tool in response.choices[0].message.executed_tools:
        print(f"Tool: {tool.name}, Result: {tool.result}")
```

---

## 2. Local Tool Calling (Function Calling)

Traditional function calling pattern where tools execute client-side.

### Tool Definition Schema

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]
```

### tool_choice Parameter

| Value | Behavior |
|-------|----------|
| `"auto"` | Model decides whether to use tools (default) |
| `"required"` | Model MUST use at least one tool |
| `"none"` | Model cannot use tools |
| `{"type": "function", "function": {"name": "get_weather"}}` | Force specific function |

### Complete Python Example

```python
from groq import Groq
import json

client = Groq(api_key="gsk_...")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City, e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

def get_current_weather(location: str, unit: str = "fahrenheit"):
    """Mock weather function"""
    return json.dumps({"location": location, "temperature": "72", "unit": unit})

# Step 1: Initial request
messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Step 2: Handle tool calls
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    messages.append(response_message)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        if function_name == "get_current_weather":
            function_response = get_current_weather(
                location=function_args.get("location"),
                unit=function_args.get("unit", "fahrenheit")
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response,
            })

    # Step 3: Get final response
    second_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    print(second_response.choices[0].message.content)
else:
    print(response_message.content)
```

### Handling Tool Results

**Critical:** Use `role: "tool"` (not "function") for tool results:

```python
messages.append({
    "role": "tool",              # Not "function"
    "tool_call_id": tool_call.id,
    "name": function_name,
    "content": function_response
})
```

---

## Model Support Matrix

| Model | Built-In Tools | Local Tools | Parallel Calls |
|-------|----------------|-------------|----------------|
| compound-beta | ✅ | ❌ | ✅ |
| llama-3.3-70b | ❌ | ✅ | ✅ |
| llama-3.1-70b | ❌ | ✅ | ✅ |
| llama-3.1-8b | ❌ | ✅ | ✅ |

---

## Pattern Selection Guide

### Use Built-In Tools When:
- You need web search or code execution
- You want zero implementation overhead
- You're using compound-beta

### Use Local Tool Calling When:
- Tools access local resources (files, credentials)
- You need full control over execution
- You're building agentic workflows

---

## Best Practices

1. **Tool Descriptions**: Be specific - helps model choose correct tool
2. **Parameter Validation**: Always validate args before execution
3. **Error Responses**: Return structured errors as tool results
4. **Security**: Validate and sanitize all tool inputs

---

## NO OPENAI

```python
from groq import Groq  # Never: from openai import OpenAI
```
