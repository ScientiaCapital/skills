# Deployment Patterns for LangGraph

Application structure, local development, and production deployment patterns.

---

## Application Structure

### Recommended Project Layout

```
my-agent/
├── agent.py              # Graph/agent definition
├── tools.py              # Tool implementations
├── state.py              # State schema definitions
├── langgraph.json        # LangGraph Platform config
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (gitignored)
├── tests/
│   ├── conftest.py
│   ├── test_agent.py
│   └── test_tools.py
└── skills/               # Optional: agent sub-skills
    └── researcher/
        └── SKILL.md
```

### `langgraph.json` Configuration

```json
{
  "dependencies": ["requirements.txt"],
  "graphs": {
    "my_agent": "agent.py:graph",
    "researcher": "agent.py:researcher_graph"
  },
  "env": ".env",
  "dockerfile_lines": [
    "RUN apt-get update && apt-get install -y libpq-dev"
  ]
}
```

Multiple graphs can be exposed from the same project — each gets its own `assistant_id`.

---

## LangGraph Local Server

### Setup and Launch

```bash
# Install CLI with in-memory persistence support
pip install "langgraph-cli[inmem]"

# Launch dev server (requires Python >= 3.11)
langgraph dev

# Server runs at http://127.0.0.1:2024
# API docs at http://127.0.0.1:2024/docs
# Studio UI at https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**Note**: Local server uses in-memory persistence — state is lost on restart, not for production.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/runs/stream` | POST | Stream agent execution |
| `/threads` | POST | Create new thread |
| `/threads/{id}/state` | GET | Get current thread state |
| `/threads/{id}/history` | GET | Get full state history |
| `/assistants` | GET | List available agents |
| `/health` | GET | Health check |

### Python Client SDK

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://127.0.0.1:2024")

# Create a thread (persistent conversation)
thread = client.threads.create()

# Stream agent execution
for chunk in client.runs.stream(
    thread_id=thread["thread_id"],
    assistant_id="my_agent",
    input={"messages": [{"role": "user", "content": "Hello"}]},
    stream_mode="updates",
):
    print(chunk)

# Retrieve final state
state = client.threads.get_state(thread_id=thread["thread_id"])
print(state["values"]["messages"][-1]["content"])
```

**Async:** Use `get_client()` instead of `get_sync_client()` — same API with `await`.

---

## LangGraph Platform (Production)

### Deployment via LangSmith

1. Push code to GitHub (public or private repo)
2. Connect repo in LangSmith → **Deployments** → **New Deployment**
3. Set environment variables in the deployment config
4. Deployment builds a container and starts in ~15 minutes

### API Access

```python
import httpx

API_URL = "https://your-deployment.langsmith.com"
API_KEY = "ls_..."

# Streaming request
with httpx.stream(
    "POST",
    f"{API_URL}/runs/stream",
    headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
    json={
        "assistant_id": "my_agent",
        "input": {"messages": [{"role": "user", "content": "Hello"}]},
        "stream_mode": ["updates", "messages"],
    },
    timeout=60.0,
) as response:
    for line in response.iter_lines():
        if line:
            print(line)
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Python dependencies — cached layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000
CMD ["langgraph", "up", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose — Full Stack

```yaml
services:
  agent:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    environment:
      DATABASE_URL: "postgresql://agent:${POSTGRES_PASSWORD}@postgres:5432/langgraph"
      REDIS_URL: "redis://redis:6379"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: langgraph
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agent -d langgraph"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
```

---

## Checkpointer Selection

| Checkpointer | Use Case | Setup |
|-------------|----------|-------|
| `InMemorySaver` | Testing, local dev | No dependencies |
| `PostgresSaver` | Production, durable state | `pip install langgraph-checkpoint-postgres` |
| `RedisSaver` | High-throughput, ephemeral | `pip install langgraph-checkpoint-redis` |

### PostgreSQL Checkpointer (Production)

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Synchronous (FastAPI, Flask)
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://agent:password@host:5432/langgraph"
)

graph = build_graph(checkpointer=checkpointer)
```

### Async PostgreSQL Checkpointer

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import asyncpg

async def build_production_graph():
    pool = await asyncpg.create_pool(
        "postgresql://agent:password@host:5432/langgraph",
        min_size=5,
        max_size=20,
    )
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()  # Creates tables if needed
    return build_graph(checkpointer=checkpointer)
```

### Redis for High-Throughput

```python
from langgraph.checkpoint.redis import RedisSaver

checkpointer = RedisSaver.from_conn_string("redis://localhost:6379")
graph = build_graph(checkpointer=checkpointer)
```

---

## Scaling Patterns

### Worker Pools

For high concurrency, run multiple agent workers behind a load balancer:

- Each worker maintains its own connection pool to the checkpointer
- Thread IDs ensure state consistency — the same thread always reads its own state
- Use Redis for cross-worker coordination (distributed locks, rate limiting)

```python
# gunicorn config for multiple workers
# gunicorn.conf.py
workers = 4             # CPU-bound: num_cores. IO-bound: num_cores * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
timeout = 120           # Long enough for multi-step agents
keepalive = 5
```

### Rate Limiting

```python
from fastapi import FastAPI, Request, HTTPException
import time
from collections import defaultdict

app = FastAPI()

# Simple in-process rate limiter — use Redis for multi-worker
_request_counts: dict = defaultdict(list)
RATE_LIMIT = 10  # requests per minute

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    user_id = request.headers.get("X-User-Id", "anonymous")
    now = time.time()
    window = [t for t in _request_counts[user_id] if now - t < 60]
    if len(window) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    _request_counts[user_id] = window + [now]
    return await call_next(request)
```

---

## Production Checklist

| Category | Check |
|----------|-------|
| Persistence | PostgreSQL checkpointer (not in-memory) |
| Config | Environment variables for all secrets |
| Reliability | Health check endpoint responding |
| Security | Rate limiting on all agent API endpoints |
| Security | Authentication/authorization enforced |
| Observability | LangSmith tracing enabled with project name |
| Cost | Budget alerts configured |
| Ops | Error alerting (PagerDuty, Slack, etc.) |
| Ops | Trace sampling configured for high-volume |
| Ops | Database backup strategy in place |
| Ops | Graceful shutdown handling (SIGTERM) |
| Scaling | Connection pooling on checkpointer |
