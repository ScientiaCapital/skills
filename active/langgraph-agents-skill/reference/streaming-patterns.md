# Streaming Patterns Reference

**Level**: Deep-Dive (Level 3)
**When to load**: Implementing real-time output, progress tracking, or debugging workflows

## Overview

LangGraph supports 5 streaming modes for different use cases:
- **values**: Full state after each step
- **updates**: Delta changes per node
- **messages**: LLM tokens as they generate
- **custom**: Application-defined events
- **debug**: Internal execution details

---

## Streaming Modes

### values - Full State Snapshots

```python
for state in graph.stream(inputs, stream_mode="values"):
    print(f"Full state: {state}")
    # {'messages': [...], 'next_agent': 'researcher', ...}
```

**Use when**: Need complete state at each step, debugging state evolution.

### updates - Node Output Deltas

```python
for update in graph.stream(inputs, stream_mode="updates"):
    node_name = list(update.keys())[0]
    node_output = update[node_name]
    print(f"{node_name} produced: {node_output}")
    # researcher: {'findings': 'New research...'}
```

**Use when**: Tracking which node produced what, partial updates to UI.

### messages - Token-by-Token LLM Output

```python
async for event in graph.astream(inputs, stream_mode="messages"):
    if hasattr(event, 'content'):
        print(event.content, end="", flush=True)
```

**Use when**: Showing LLM responses as they generate (chat UX).

### custom - Application Events

```python
from langgraph.types import StreamWriter

def my_node(state: State, writer: StreamWriter) -> dict:
    writer({"event": "starting", "progress": 0})

    # Do work...
    writer({"event": "processing", "progress": 50})

    # More work...
    writer({"event": "complete", "progress": 100})

    return {"result": "done"}

# Consume custom events
for event in graph.stream(inputs, stream_mode="custom"):
    if event.get("event") == "processing":
        update_progress_bar(event["progress"])
```

**Use when**: Progress tracking, custom UI updates, logging milestones.

### debug - Execution Internals

```python
for event in graph.stream(inputs, stream_mode="debug"):
    print(f"[DEBUG] {event}")
    # Includes: node entry/exit, edge traversal, checkpoint saves
```

**Use when**: Debugging workflow issues, understanding execution order.

---

## Combined Streaming

Stream multiple modes simultaneously:

```python
async for event in graph.astream(
    inputs,
    stream_mode=["updates", "messages", "custom"]
):
    if "updates" in event:
        handle_node_update(event["updates"])
    elif "messages" in event:
        handle_llm_token(event["messages"])
    elif "custom" in event:
        handle_custom_event(event["custom"])
```

---

## Custom Streaming with get_stream_writer

### Within Graph Nodes

```python
from langgraph.types import get_stream_writer

def research_node(state: State) -> dict:
    writer = get_stream_writer()

    # Stream progress events
    writer({"type": "status", "message": "Starting research..."})

    for i, source in enumerate(state["sources"]):
        result = fetch_source(source)
        writer({
            "type": "progress",
            "current": i + 1,
            "total": len(state["sources"]),
            "source": source
        })

    writer({"type": "status", "message": "Research complete"})
    return {"findings": results}
```

### Consuming Custom Events

```python
async def process_with_progress(inputs):
    progress_events = []

    async for event in graph.astream(inputs, stream_mode="custom"):
        if event.get("type") == "progress":
            progress_events.append(event)
            yield {"progress": event["current"] / event["total"]}
        elif event.get("type") == "status":
            yield {"status": event["message"]}
```

---

## Subgraph Streaming

Stream from nested workflows:

```python
from langgraph.types import StreamWriter

# Subgraph streams its own events
subgraph = create_research_graph()

def parent_node(state: State, writer: StreamWriter) -> dict:
    # Forward subgraph streams to parent
    for event in subgraph.stream(
        {"query": state["query"]},
        stream_mode="custom"
    ):
        writer({"subgraph": "research", **event})

    return {"research_complete": True}
```

---

## Async Streaming Patterns

### WebSocket Integration

```python
from fastapi import WebSocket

async def websocket_endpoint(websocket: WebSocket, inputs: dict):
    await websocket.accept()

    async for event in graph.astream(inputs, stream_mode=["updates", "custom"]):
        await websocket.send_json(event)

    await websocket.close()
```

### Server-Sent Events (SSE)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def stream_workflow(query: str):
    async def event_generator():
        async for event in graph.astream(
            {"query": query},
            stream_mode="custom"
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

---

## Production Patterns

### Progress Tracking

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProgressEvent:
    step: str
    progress: float  # 0.0 - 1.0
    message: str
    metadata: Optional[dict] = None

def tracked_node(state: State) -> dict:
    writer = get_stream_writer()

    steps = ["fetch", "process", "validate", "complete"]
    for i, step in enumerate(steps):
        writer(ProgressEvent(
            step=step,
            progress=(i + 1) / len(steps),
            message=f"Executing {step}..."
        ).__dict__)

        execute_step(step, state)

    return {"status": "complete"}
```

### Error Streaming

```python
def safe_node(state: State) -> dict:
    writer = get_stream_writer()

    try:
        result = risky_operation(state)
        writer({"type": "success", "result": result})
        return {"output": result}
    except Exception as e:
        writer({
            "type": "error",
            "error": str(e),
            "recoverable": isinstance(e, RecoverableError)
        })
        raise
```

### Rate-Limited Streaming

```python
import asyncio
from collections import deque

class RateLimitedWriter:
    def __init__(self, writer: StreamWriter, min_interval: float = 0.1):
        self.writer = writer
        self.min_interval = min_interval
        self.last_write = 0
        self.buffer = deque(maxlen=10)

    def __call__(self, event: dict):
        now = asyncio.get_event_loop().time()
        if now - self.last_write >= self.min_interval:
            self.writer(event)
            self.last_write = now
        else:
            self.buffer.append(event)
```

---

## Best Practices

1. **Choose the right mode**: `updates` for UI, `messages` for chat, `custom` for progress
2. **Buffer high-frequency events**: Don't overwhelm clients with too many updates
3. **Structure custom events**: Use consistent schema for custom events
4. **Handle disconnects**: Clean up resources if client disconnects mid-stream
5. **Log debug events**: Stream debug mode to logging, not to users
6. **Combine modes sparingly**: More modes = more data; be selective

---

## Mode Selection Guide

| Use Case | Mode(s) | Why |
|----------|---------|-----|
| Chat interface | `messages` | Token-by-token display |
| Progress bar | `custom` | Fine-grained progress events |
| Debug panel | `debug` + `updates` | Full execution visibility |
| State inspector | `values` | See complete state evolution |
| Multi-agent dashboard | `updates` + `custom` | Track each agent's work |
