# Tool Calling with OpenRouter Chinese LLMs

Patterns for function calling with Chinese models through OpenRouter.

## Supported Models for Tool Calling

| Model | Tool Calling | Parallel Tools | Notes |
|-------|-------------|----------------|-------|
| `deepseek/deepseek-chat` | ✅ | ✅ | Best overall for tools |
| `deepseek/deepseek-coder` | ✅ | ✅ | Good for code-related tools |
| `qwen/qwen-2.5-72b-instruct` | ✅ | ✅ | Strong tool following |
| `qwen/qwen-2.5-7b-instruct` | ✅ | ⚠️ Limited | May miss some calls |
| `qwen/qwen-2-vl-72b-instruct` | ✅ | ⚠️ Limited | Vision + tools |
| `qwen/qwq-32b` | ❌ | ❌ | Reasoning model, no tools |
| `moonshot/moonshot-v1-128k` | ❌ | ❌ | Text only |

---

## Basic Tool Definition

### Using @tool Decorator

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os

@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather for a location.

    Args:
        location: City name or coordinates
        unit: Temperature unit - 'celsius' or 'fahrenheit'
    """
    # Mock implementation
    return f"Weather in {location}: 22°{unit[0].upper()}, sunny"

@tool
def search_products(
    query: str,
    category: str = "all",
    max_price: float = None
) -> str:
    """Search product database.

    Args:
        query: Search terms
        category: Product category filter
        max_price: Maximum price filter
    """
    return f"Found 10 products matching '{query}' in {category}"

# Create LLM with tools
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

llm_with_tools = llm.bind_tools([get_weather, search_products])
```

### Using Pydantic Models

```python
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class WeatherInput(BaseModel):
    """Input for weather lookup."""
    location: str = Field(description="City name or coordinates")
    unit: str = Field(default="celsius", description="Temperature unit")

def get_weather_impl(location: str, unit: str = "celsius") -> str:
    return f"Weather in {location}: 22°{unit[0].upper()}"

weather_tool = StructuredTool.from_function(
    func=get_weather_impl,
    name="get_weather",
    description="Get current weather for a location",
    args_schema=WeatherInput
)

llm_with_tools = llm.bind_tools([weather_tool])
```

---

## Tool Choice Parameter

Control when and how tools are called:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Auto: Model decides whether to use tools (default)
llm_auto = llm.bind_tools(tools, tool_choice="auto")

# Required: Model must use at least one tool
llm_required = llm.bind_tools(tools, tool_choice="required")

# None: Model cannot use tools (for this request)
llm_none = llm.bind_tools(tools, tool_choice="none")

# Specific: Force a specific tool
llm_specific = llm.bind_tools(tools, tool_choice={"type": "function", "function": {"name": "get_weather"}})
```

---

## Handling Tool Calls

### Basic Pattern

```python
from langchain_core.messages import HumanMessage, ToolMessage

# Initial request
response = llm_with_tools.invoke([
    HumanMessage(content="What's the weather in Tokyo and London?")
])

# Check for tool calls
if response.tool_calls:
    # Build tool results
    tool_results = []
    for call in response.tool_calls:
        # Execute tool
        if call["name"] == "get_weather":
            result = get_weather.invoke(call["args"])
        elif call["name"] == "search_products":
            result = search_products.invoke(call["args"])

        tool_results.append(
            ToolMessage(content=result, tool_call_id=call["id"])
        )

    # Get final response with tool results
    final_response = llm_with_tools.invoke([
        HumanMessage(content="What's the weather in Tokyo and London?"),
        response,  # Assistant message with tool calls
        *tool_results  # Tool results
    ])

    print(final_response.content)
```

### Automated Tool Execution

```python
from langgraph.prebuilt import create_react_agent

# Create agent that automatically handles tool calls
agent = create_react_agent(
    model=llm,
    tools=[get_weather, search_products]
)

# Run agent
result = agent.invoke({
    "messages": [("user", "What's the weather in Tokyo?")]
})

# Agent automatically:
# 1. Calls get_weather tool
# 2. Receives result
# 3. Formulates final response
print(result["messages"][-1].content)
```

---

## Parallel Tool Calling

Some models support calling multiple tools simultaneously:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

llm_with_tools = llm.bind_tools([get_weather, search_products])

# Request that needs multiple tools
response = llm_with_tools.invoke([
    HumanMessage(content="What's the weather in Tokyo and also search for umbrellas")
])

# Model may return multiple tool calls
for call in response.tool_calls:
    print(f"Tool: {call['name']}, Args: {call['args']}")

# Output might be:
# Tool: get_weather, Args: {'location': 'Tokyo'}
# Tool: search_products, Args: {'query': 'umbrellas'}
```

---

## Complex Tool Schemas

### Nested Objects

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.tools import tool

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class CreateOrderInput(BaseModel):
    customer_id: str = Field(description="Customer identifier")
    items: List[OrderItem] = Field(description="List of items to order")
    shipping_address: Address = Field(description="Shipping address")
    express_shipping: bool = Field(default=False, description="Use express shipping")

@tool(args_schema=CreateOrderInput)
def create_order(
    customer_id: str,
    items: List[dict],
    shipping_address: dict,
    express_shipping: bool = False
) -> str:
    """Create a new order for a customer."""
    total = sum(item["quantity"] * item["price"] for item in items)
    return f"Order created for {customer_id}. Total: ${total:.2f}"
```

### Enum Constraints

```python
from enum import Enum
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Category(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"

class CreateTicketInput(BaseModel):
    title: str = Field(description="Ticket title")
    description: str = Field(description="Detailed description")
    priority: Priority = Field(description="Ticket priority level")
    category: Category = Field(description="Ticket category")

@tool(args_schema=CreateTicketInput)
def create_ticket(
    title: str,
    description: str,
    priority: Priority,
    category: Category
) -> str:
    """Create a support ticket."""
    return f"Ticket '{title}' created with {priority.value} priority"
```

---

## Error Handling for Tools

### Graceful Fallback

```python
from langchain_core.messages import HumanMessage, AIMessage

def invoke_with_tool_fallback(
    llm_with_tools,
    llm_without_tools,
    messages: list
) -> str:
    """Try with tools, fall back to plain LLM on failure."""
    try:
        response = llm_with_tools.invoke(messages)

        if response.tool_calls:
            # Handle tool calls...
            pass

        return response.content

    except Exception as e:
        # Model doesn't support tools, use plain completion
        print(f"Tool calling failed: {e}, falling back to plain LLM")
        return llm_without_tools.invoke(messages).content
```

### Tool Execution Error Handling

```python
from langchain_core.messages import ToolMessage

def execute_tool_safely(tool_name: str, args: dict, tools: dict) -> str:
    """Execute tool with error handling."""
    if tool_name not in tools:
        return f"Error: Unknown tool '{tool_name}'"

    try:
        tool = tools[tool_name]
        return tool.invoke(args)
    except TypeError as e:
        return f"Error: Invalid arguments for {tool_name}: {e}"
    except Exception as e:
        return f"Error executing {tool_name}: {e}"

# Usage in tool call loop
tools_map = {"get_weather": get_weather, "search_products": search_products}

for call in response.tool_calls:
    result = execute_tool_safely(call["name"], call["args"], tools_map)
    tool_messages.append(
        ToolMessage(content=result, tool_call_id=call["id"])
    )
```

---

## Best Practices

1. **Clear Tool Descriptions**
   - Write detailed docstrings
   - Explain when the tool should be used
   - Document all parameters

2. **Model Selection**
   - Use `deepseek/deepseek-chat` for reliable tool calling
   - Avoid reasoning models (qwq-32b) for tools
   - Test tool support before production

3. **Error Handling**
   - Always handle tool execution errors
   - Return meaningful error messages
   - Implement fallbacks for unsupported models

4. **Schema Design**
   - Use Pydantic for complex inputs
   - Add Field descriptions
   - Use enums for constrained values

5. **Testing**
   - Test each tool independently
   - Test tool combinations
   - Verify parallel calling works
