# LangChain Integration with OpenRouter

Comprehensive patterns for using OpenRouter's Chinese LLMs with LangChain and LangGraph.

## Basic Setup

```python
from langchain_openai import ChatOpenAI
import os

# Environment setup
# OPENROUTER_API_KEY=sk-or-v1-...

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost"),
        "X-Title": os.getenv("APP_NAME", "LangChain App")
    }
)

response = llm.invoke("Hello, how are you?")
print(response.content)
```

---

## Streaming

### Basic Streaming

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    streaming=True
)

# Sync streaming
for chunk in llm.stream("Explain quantum computing"):
    print(chunk.content, end="", flush=True)
```

### Async Streaming

```python
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    streaming=True
)

async def stream_response():
    async for chunk in llm.astream("Explain quantum computing"):
        print(chunk.content, end="", flush=True)

asyncio.run(stream_response())
```

### Streaming with Events

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

async def stream_with_events():
    async for event in llm.astream_events(
        [HumanMessage(content="Write a haiku about coding")],
        version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            print(event["data"]["chunk"].content, end="")

asyncio.run(stream_with_events())
```

---

## Async Patterns

### Concurrent Requests

```python
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen/qwen-2.5-7b-instruct",  # Fast model for parallel
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

async def analyze_multiple(items: list[str]) -> list[str]:
    """Analyze multiple items concurrently."""
    tasks = [llm.ainvoke(f"Summarize: {item}") for item in items]
    responses = await asyncio.gather(*tasks)
    return [r.content for r in responses]

# Usage
items = ["Document 1 text...", "Document 2 text...", "Document 3 text..."]
summaries = asyncio.run(analyze_multiple(items))
```

### Rate-Limited Async

```python
import asyncio
from asyncio import Semaphore
from langchain_openai import ChatOpenAI

async def rate_limited_batch(
    prompts: list[str],
    max_concurrent: int = 5
) -> list[str]:
    """Process prompts with rate limiting."""
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    semaphore = Semaphore(max_concurrent)

    async def process_one(prompt: str) -> str:
        async with semaphore:
            response = await llm.ainvoke(prompt)
            return response.content

    tasks = [process_one(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

---

## LangGraph Agent Factory

```python
from enum import Enum
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import os

class ChineseModel(str, Enum):
    """Available Chinese models via OpenRouter."""
    DEEPSEEK_CHAT = "deepseek/deepseek-chat"
    DEEPSEEK_CODER = "deepseek/deepseek-coder"
    QWEN_VL = "qwen/qwen-2-vl-72b-instruct"
    QWEN_FAST = "qwen/qwen-2.5-7b-instruct"
    QWEN_72B = "qwen/qwen-2.5-72b-instruct"
    QWQ_REASONING = "qwen/qwq-32b"
    MOONSHOT_LONG = "moonshot/moonshot-v1-128k"
    AUTO = "openrouter/auto"


def create_openrouter_llm(
    model: ChineseModel,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    streaming: bool = False,
    **kwargs
) -> ChatOpenAI:
    """Factory for OpenRouter LLMs with sensible defaults."""
    return ChatOpenAI(
        model=model.value,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=streaming,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": os.getenv("APP_URL", "http://localhost"),
            "X-Title": os.getenv("APP_NAME", "LangChain App")
        },
        **kwargs
    )


def create_agent(
    model: ChineseModel,
    tools: list,
    system_message: str = "You are a helpful assistant.",
    **llm_kwargs
):
    """Create a LangGraph ReAct agent with OpenRouter model."""
    llm = create_openrouter_llm(model, **llm_kwargs)
    return create_react_agent(llm, tools, state_modifier=system_message)


# Example usage
@tool
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate a math expression using a parser."""
    # Use a safe math parser library instead of eval
    import ast
    import operator

    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def safe_eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](safe_eval(node.left), safe_eval(node.right))
        else:
            raise ValueError("Unsupported expression")

    tree = ast.parse(expression, mode='eval')
    return str(safe_eval(tree.body))

# Create different agents for different purposes
chat_agent = create_agent(
    ChineseModel.DEEPSEEK_CHAT,
    tools=[search],
    system_message="You are a helpful research assistant."
)

code_agent = create_agent(
    ChineseModel.DEEPSEEK_CODER,
    tools=[calculate],
    system_message="You are a coding assistant."
)

# Run agent
result = chat_agent.invoke({
    "messages": [("user", "What is the capital of France?")]
})
```

---

## Multi-Model Orchestration

### Supervisor Pattern

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
import operator

class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    final_response: str

# Create specialized LLMs
supervisor_llm = create_openrouter_llm(ChineseModel.DEEPSEEK_CHAT, temperature=0)
coder_llm = create_openrouter_llm(ChineseModel.DEEPSEEK_CODER, temperature=0)
analyst_llm = create_openrouter_llm(ChineseModel.QWEN_72B, temperature=0.3)

def supervisor_node(state: SupervisorState) -> SupervisorState:
    """Route to appropriate specialist."""
    last_message = state["messages"][-1].content

    routing_prompt = f"""Analyze this request and decide which specialist should handle it.

Request: {last_message}

Respond with ONLY one of: CODER, ANALYST, DONE
- CODER: For code generation, debugging, technical implementation
- ANALYST: For data analysis, research, writing
- DONE: If the task is complete"""

    response = supervisor_llm.invoke(routing_prompt)
    next_agent = response.content.strip().upper()

    return {"next_agent": next_agent}

def coder_node(state: SupervisorState) -> SupervisorState:
    """Handle coding tasks."""
    last_message = state["messages"][-1].content
    response = coder_llm.invoke(f"Complete this coding task:\n{last_message}")
    return {
        "messages": [response],
        "final_response": response.content
    }

def analyst_node(state: SupervisorState) -> SupervisorState:
    """Handle analysis tasks."""
    last_message = state["messages"][-1].content
    response = analyst_llm.invoke(f"Analyze the following:\n{last_message}")
    return {
        "messages": [response],
        "final_response": response.content
    }

def route_supervisor(state: SupervisorState) -> str:
    """Route based on supervisor decision."""
    next_agent = state.get("next_agent", "DONE")
    if next_agent == "CODER":
        return "coder"
    elif next_agent == "ANALYST":
        return "analyst"
    else:
        return END

# Build graph
graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("coder", coder_node)
graph.add_node("analyst", analyst_node)

graph.add_conditional_edges("supervisor", route_supervisor)
graph.add_edge("coder", END)
graph.add_edge("analyst", END)

graph.set_entry_point("supervisor")
workflow = graph.compile()

# Run
result = workflow.invoke({
    "messages": [HumanMessage(content="Write a Python function to calculate fibonacci")]
})
```

---

## Tool Binding

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import os

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"The weather in {city} is 72°F and sunny."

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the database for records."""
    return f"Found {limit} results for '{query}'"

# Create LLM with tools
llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Bind tools
llm_with_tools = llm.bind_tools([get_weather, search_database])

# Use
response = llm_with_tools.invoke("What's the weather in Tokyo?")

# Check for tool calls
if response.tool_calls:
    for call in response.tool_calls:
        print(f"Tool: {call['name']}, Args: {call['args']}")
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class MovieReview(BaseModel):
    """A movie review."""
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating from 1-10")
    summary: str = Field(description="Brief review summary")
    recommend: bool = Field(description="Whether to recommend")

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

structured_llm = llm.with_structured_output(MovieReview)

review = structured_llm.invoke("Review the movie Inception")
print(f"Title: {review.title}")
print(f"Rating: {review.rating}/10")
print(f"Summary: {review.summary}")
print(f"Recommended: {review.recommend}")
```

---

## Chain Patterns

### Sequential Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Different models for different stages
fast_llm = create_openrouter_llm(ChineseModel.QWEN_FAST, temperature=0.3)
quality_llm = create_openrouter_llm(ChineseModel.DEEPSEEK_CHAT, temperature=0.7)

# Stage 1: Quick analysis
analyze_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a text analyzer. Extract key topics from the text."),
    ("user", "{text}")
])

# Stage 2: Deep synthesis
synthesize_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a writer. Create a compelling summary from these topics."),
    ("user", "Topics: {topics}\n\nOriginal text: {text}")
])

# Build chain
analyze_chain = analyze_prompt | fast_llm | StrOutputParser()
synthesize_chain = synthesize_prompt | quality_llm | StrOutputParser()

def full_pipeline(text: str) -> str:
    topics = analyze_chain.invoke({"text": text})
    summary = synthesize_chain.invoke({"topics": topics, "text": text})
    return summary

# Run
result = full_pipeline("Your long document text here...")
```

---

## Error Handling

```python
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException
import httpx
import time

def create_robust_llm(
    model: str,
    max_retries: int = 3,
    timeout: float = 30.0
) -> ChatOpenAI:
    """Create LLM with retry and timeout handling."""
    return ChatOpenAI(
        model=model,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_retries=max_retries,
        timeout=timeout,
        request_timeout=timeout
    )

def invoke_with_fallback(
    prompt: str,
    primary_model: str = "deepseek/deepseek-chat",
    fallback_model: str = "qwen/qwen-2.5-7b-instruct"
) -> str:
    """Invoke with automatic fallback on failure."""
    try:
        llm = create_robust_llm(primary_model)
        return llm.invoke(prompt).content
    except Exception as e:
        print(f"Primary model failed: {e}, falling back...")
        llm = create_robust_llm(fallback_model)
        return llm.invoke(prompt).content
```

---

## Best Practices

1. **Reuse LLM instances** - Create once, use many times
2. **Use async for batch processing** - Much faster than sequential
3. **Set appropriate timeouts** - Chinese models may have variable latency
4. **Implement fallbacks** - Always have a backup model
5. **Stream long responses** - Better UX for chat interfaces
6. **Bind tools explicitly** - Check model supports tool calling first
7. **Use structured output** - Pydantic ensures type safety
