# Technical Research Reference

Comprehensive guide for framework evaluation, LLM selection, API integration, and MCP discovery.

---

## Framework Comparison Template

### Comparison Overview

```yaml
comparison:
  use_case: ""
  date: ""
  decision_needed_by: ""
  stakeholders: []

  requirements:
    must_have: []
    nice_to_have: []
    constraints: []
```

---

### Framework Profiles

#### Framework A: [Name]

```yaml
basics:
  name: ""
  url: ""
  github: ""
  stars: 0
  last_release: ""
  license: ""

maturity:
  age_years: 0
  production_users: []  # Known companies
  stability: ""  # alpha, beta, stable, mature

community:
  discord_members: 0
  github_contributors: 0
  stackoverflow_questions: 0

documentation:
  quality: ""  # 1-5
  examples: ""  # 1-5
  api_reference: ""  # 1-5
  tutorials: ""  # 1-5
```

---

### Feature Comparison Matrix

| Feature | Framework A | Framework B | Weight |
|---------|-------------|-------------|--------|
| [Feature 1] | [check] / [warn] / [x] | [check] / [warn] / [x] | HIGH |
| [Feature 2] | [check] / [warn] / [x] | [check] / [warn] / [x] | MED |
| [Feature 3] | [check] / [warn] / [x] | [check] / [warn] / [x] | LOW |

**Legend:**
- [check] Full support (native, well-documented)
- [warn] Partial support (possible but difficult, plugin required)
- [x] Not supported

---

### Technical Evaluation

#### Installation & Setup

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| pip install works | | |
| M1 Mac compatible | | |
| Dependencies clean | | |
| Setup time | | |

#### Code Quality

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Type hints | | |
| Async support | | |
| Error messages | | |
| Debugging ease | | |

#### Performance

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Startup time | | |
| Memory usage | | |
| Throughput | | |
| Latency | | |

---

### Integration Assessment

#### With Our Stack

| Integration | Framework A | Framework B |
|-------------|-------------|-------------|
| Supabase | | |
| RunPod | | |
| Vercel | | |
| MCP servers | | |
| LangGraph | | |

#### API/SDK Quality

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Python SDK | | |
| REST API | | |
| WebSocket | | |
| Streaming | | |

---

### Risk Assessment

#### Framework A Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | LOW/MED/HIGH | LOW/MED/HIGH | |

#### Framework B Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

---

### Cost Analysis

```yaml
framework_a:
  licensing: ""  # Free, paid, usage-based
  hosting_cost: ""
  development_time: ""
  maintenance_burden: ""
  total_estimate: ""

framework_b:
  licensing: ""
  hosting_cost: ""
  development_time: ""
  maintenance_burden: ""
  total_estimate: ""
```

---

### Proof of Concept Results

#### Framework A PoC

```yaml
poc:
  goal: ""
  time_spent: ""
  outcome: ""  # success, partial, failure

  what_worked: []
  what_didnt: []
  surprises: []

  code_sample: |
    # Key code that worked or didn't
```

---

### Decision Matrix

| Criteria | Weight | Framework A | Framework B |
|----------|--------|-------------|-------------|
| Feature completeness | 25% | /10 | /10 |
| Ease of use | 20% | /10 | /10 |
| Performance | 15% | /10 | /10 |
| Community/support | 15% | /10 | /10 |
| Integration fit | 15% | /10 | /10 |
| Cost | 10% | /10 | /10 |
| **Weighted Total** | 100% | **/10** | **/10** |

---

### Recommendation

```yaml
recommendation:
  winner: ""
  confidence: ""  # high, medium, low

  primary_reasons:
    - ""
    - ""
    - ""

  concerns:
    - ""

  next_steps:
    - ""
    - ""

  fallback_plan: ""
```

---

## LLM Evaluation Checklist

### Provider Evaluation Template

```yaml
provider:
  name: ""
  website: ""
  api_docs: ""
  status_page: ""

models_available:
  - name: ""
    context_window: 0
    input_cost_per_1m: 0.00
    output_cost_per_1m: 0.00

access:
  signup_process: ""  # instant, waitlist, enterprise
  api_key_type: ""  # simple key, OAuth, etc.
  rate_limits: ""

evaluated_date: ""
verdict: ""  # USE, MAYBE, SKIP
```

---

### Tim's Approved Providers

#### Tier 1: Primary (Use Freely)

| Provider | Best For | Access Via |
|----------|----------|------------|
| Anthropic | Complex reasoning, code | Direct API |
| Google | Multimodal, long context | Direct API |
| OpenRouter | Cost optimization | API gateway |

#### Tier 2: Specialized (Use Cases)

| Provider | Best For | Access Via |
|----------|----------|------------|
| DeepSeek | Bulk processing, code | OpenRouter |
| Qwen | Chinese content, cost | OpenRouter |
| Voyage | Embeddings | Direct API |
| Cohere | Embeddings, rerank | Direct API |

#### Tier 3: Local (Privacy/Cost)

| Provider | Best For | Access Via |
|----------|----------|------------|
| Ollama | Development, private | Local |
| LM Studio | Testing | Local |

#### Forbidden

| Provider | Reason |
|----------|--------|
| OpenAI | Policy decision |
| Azure OpenAI | Same |

---

### Cost Analysis Framework

#### Cost Per Task Type

```yaml
task_costs:
  simple_classification:
    tokens_typical: 500
    best_model: "deepseek-chat"
    cost_per_1000_tasks: "$0.07"

  summarization:
    tokens_typical: 2000
    best_model: "deepseek-chat"
    cost_per_1000_tasks: "$0.28"

  complex_reasoning:
    tokens_typical: 4000
    best_model: "claude-sonnet"
    cost_per_1000_tasks: "$12.00"

  code_generation:
    tokens_typical: 3000
    best_model: "claude-sonnet"
    cost_per_1000_tasks: "$9.00"

  embeddings:
    tokens_typical: 500
    best_model: "voyage-3"
    cost_per_1000_tasks: "$0.05"
```

#### Monthly Cost Projection

```python
def estimate_monthly_cost(tasks: dict) -> float:
    """
    tasks = {
        'simple_classification': 10000,
        'summarization': 5000,
        'complex_reasoning': 1000,
        'code_generation': 500,
        'embeddings': 50000
    }
    """
    rates = {
        'simple_classification': 0.00007,
        'summarization': 0.00028,
        'complex_reasoning': 0.012,
        'code_generation': 0.009,
        'embeddings': 0.00005
    }
    return sum(tasks[k] * rates[k] for k in tasks)
```

---

### Capability Evaluation

#### Reasoning Quality Test

```yaml
test_prompts:
  logic:
    prompt: "If all A are B, and all B are C, what can we conclude about A and C?"
    expected: "All A are C (transitive property)"

  math:
    prompt: "What is 17 * 23? Show your work."
    expected: "391 with clear steps"

  code:
    prompt: "Write a Python function to find the nth Fibonacci number using memoization."
    expected: "Correct implementation with @lru_cache or manual memo dict"

  analysis:
    prompt: "Given [complex scenario], what are the trade-offs?"
    expected: "Structured analysis with multiple perspectives"
```

#### Instruction Following Test

```yaml
tests:
  format_compliance:
    prompt: "Respond in JSON format with keys: name, age, city"
    check: "Valid JSON, correct keys"

  length_control:
    prompt: "Explain X in exactly 3 sentences."
    check: "Exactly 3 sentences"

  constraint_respect:
    prompt: "List 5 items, no more, no less"
    check: "Exactly 5 items"
```

---

### Integration Checklist

#### API Quality

- [ ] REST API available
- [ ] Python SDK official/maintained
- [ ] Streaming support
- [ ] Function calling / tools
- [ ] JSON mode
- [ ] Batch API available

#### Reliability

- [ ] Status page exists
- [ ] SLA published
- [ ] Historical uptime >99%
- [ ] Rate limit headers clear
- [ ] Error messages helpful

#### Developer Experience

- [ ] Quick start guide
- [ ] API playground
- [ ] SDK well-typed
- [ ] Examples in docs
- [ ] Active Discord/support

---

### Model Selection Decision Tree

```
START: What's the task?
│
├──► Complex reasoning / Analysis
│   └──► Claude Sonnet (or Gemini Pro)
│
├──► Code generation / Review
│   └──► Claude Sonnet (or DeepSeek Coder)
│
├──► Bulk text processing
│   └──► Is accuracy critical?
│       ├──► Yes ──► Claude Haiku
│       └──► No ──► DeepSeek V3
│
├──► Embeddings
│   └──► Voyage-3 (or Cohere)
│
├──► Multimodal (images)
│   └──► Claude Sonnet or Gemini Pro
│
├──► Long context (>100k)
│   └──► Gemini Pro (1M context)
│
├──► Local / Private
│   └──► Ollama + Qwen 2.5
│
└──► Cost is primary concern
    └──► DeepSeek V3 via OpenRouter
```

---

### Provider Deep Dives

#### Anthropic (Claude)

```yaml
strengths:
  - Best reasoning quality
  - Excellent instruction following
  - Strong code generation
  - Good at saying "I don't know"

weaknesses:
  - Higher cost than Chinese LLMs
  - No fine-tuning (yet)
  - Rate limits can be tight

best_for:
  - Complex analysis
  - Code review/generation
  - Agentic workflows
  - Customer-facing applications

cost_optimization:
  - Use Haiku for simple tasks
  - Batch API for bulk (50% off)
  - Cache system prompts
```

#### DeepSeek (via OpenRouter)

```yaml
strengths:
  - 90%+ cost savings vs Claude
  - Good code generation
  - Fast inference
  - Generous rate limits

weaknesses:
  - Slightly lower reasoning
  - Less reliable on edge cases
  - Smaller context window

best_for:
  - Bulk processing
  - Code generation (routine)
  - Classification tasks
  - Cost-sensitive pipelines

cost_optimization:
  - Already cheap
  - Use V3 for quality/cost balance
```

#### Google (Gemini)

```yaml
strengths:
  - Massive context (1M tokens)
  - Strong multimodal
  - Good reasoning
  - Competitive pricing

weaknesses:
  - API can be flaky
  - SDK less mature than Anthropic
  - Safety filters aggressive

best_for:
  - Long document analysis
  - Multimodal tasks
  - When 200k context isn't enough

cost_optimization:
  - Use Flash for simple tasks
  - Pro for complex reasoning
```

---

## API Integration Patterns

### Common Integration Architectures

#### Pattern 1: Direct API Call

```python
# Simplest pattern - direct HTTP request
import httpx

async def call_api(endpoint: str, payload: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            json=payload,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
```

**Use when:**
- Simple, infrequent calls
- No retry logic needed
- Single endpoint

#### Pattern 2: SDK Wrapper

```python
# Wrap SDK for consistent interface
from anthropic import Anthropic

class LLMClient:
    def __init__(self):
        self.client = Anthropic()

    async def complete(self, prompt: str, model: str = "claude-sonnet-4-20250514") -> str:
        response = await self.client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

**Use when:**
- SDK is well-maintained
- Need type hints
- Want automatic retries

#### Pattern 3: Multi-Provider Router

```python
# Route to different providers based on task
from enum import Enum

class Provider(Enum):
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"

class LLMRouter:
    def __init__(self):
        self.providers = {
            Provider.ANTHROPIC: AnthropicClient(),
            Provider.DEEPSEEK: OpenRouterClient("deepseek"),
            Provider.GEMINI: GeminiClient(),
        }

    async def complete(
        self,
        prompt: str,
        task_type: str = "general"
    ) -> str:
        provider = self._select_provider(task_type)
        return await self.providers[provider].complete(prompt)

    def _select_provider(self, task_type: str) -> Provider:
        routing = {
            "complex_reasoning": Provider.ANTHROPIC,
            "bulk_processing": Provider.DEEPSEEK,
            "long_context": Provider.GEMINI,
        }
        return routing.get(task_type, Provider.ANTHROPIC)
```

**Use when:**
- Multiple LLM providers
- Cost optimization needed
- Different tasks need different models

#### Pattern 4: Queue-Based Processing

```python
# For bulk/async processing
import asyncio
from collections import deque

class BatchProcessor:
    def __init__(self, concurrency: int = 5):
        self.queue = deque()
        self.semaphore = asyncio.Semaphore(concurrency)

    async def process_batch(self, items: list) -> list:
        tasks = [self._process_item(item) for item in items]
        return await asyncio.gather(*tasks)

    async def _process_item(self, item):
        async with self.semaphore:
            return await self.api_call(item)
```

**Use when:**
- Large batch processing
- Rate limit management
- Need progress tracking

---

### Error Handling Patterns

#### Retry with Exponential Backoff

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    *args, **kwargs
) -> T:
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except (httpx.HTTPStatusError, asyncio.TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

#### Circuit Breaker

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure = None
        self.state = "closed"  # closed, open, half-open

    def can_execute(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if datetime.now() - self.last_failure > timedelta(seconds=self.reset_timeout):
                self.state = "half-open"
                return True
            return False
        return True  # half-open

    def record_success(self):
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        self.last_failure = datetime.now()
        if self.failures >= self.threshold:
            self.state = "open"
```

---

### Rate Limiting Patterns

#### Token Bucket

```python
import asyncio
from time import time

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        async with self.lock:
            now = time()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def wait_for_token(self, tokens: int = 1):
        while not await self.acquire(tokens):
            await asyncio.sleep(0.1)
```

#### Sliding Window

```python
from collections import deque
from time import time

class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = deque()

    def can_proceed(self) -> bool:
        now = time()
        # Remove old requests
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
```

---

### Caching Patterns

#### Response Cache

```python
import hashlib
import json
from typing import Optional

class ResponseCache:
    def __init__(self):
        self.cache = {}

    def _hash_request(self, prompt: str, model: str) -> str:
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        key = self._hash_request(prompt, model)
        return self.cache.get(key)

    def set(self, prompt: str, model: str, response: str):
        key = self._hash_request(prompt, model)
        self.cache[key] = response
```

#### Semantic Cache (with embeddings)

```python
import numpy as np
from typing import Optional, Tuple

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.95):
        self.threshold = similarity_threshold
        self.embeddings = []
        self.responses = []

    async def get(self, query_embedding: np.ndarray) -> Optional[str]:
        if not self.embeddings:
            return None

        similarities = [
            np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
            for emb in self.embeddings
        ]

        max_sim = max(similarities)
        if max_sim >= self.threshold:
            idx = similarities.index(max_sim)
            return self.responses[idx]
        return None

    def set(self, embedding: np.ndarray, response: str):
        self.embeddings.append(embedding)
        self.responses.append(response)
```

---

### Configuration Management

#### Environment-Based Config

```python
from pydantic_settings import BaseSettings
from typing import Optional

class APIConfig(BaseSettings):
    anthropic_api_key: str
    openrouter_api_key: str
    google_api_key: Optional[str] = None

    default_model: str = "claude-sonnet-4-20250514"
    default_timeout: int = 30
    max_retries: int = 3

    class Config:
        env_file = ".env"

config = APIConfig()
```

#### Feature Flags

```python
class FeatureFlags:
    def __init__(self):
        self.flags = {
            "use_deepseek_for_bulk": True,
            "enable_caching": True,
            "streaming_enabled": True,
        }

    def is_enabled(self, flag: str) -> bool:
        return self.flags.get(flag, False)
```

---

## MCP Discovery Guide

### What is MCP?

Model Context Protocol (MCP) enables LLMs to interact with external tools, data sources, and services through a standardized interface.

**Key concepts:**
- **Server:** Provides tools/resources to LLMs
- **Client:** Connects to servers (Claude Desktop, Cursor, etc.)
- **Tools:** Functions the LLM can call
- **Resources:** Data the LLM can read

---

### Discovery Workflow

#### Step 1: Check Existing MCP Servers

**Tim's mcp-server-cookbook:**
```
/Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook/
```

**Already configured servers:**
Check `~/.claude/claude_desktop_config.json` for active servers.

#### Step 2: Search Official MCP Servers

**Official repository:**
https://github.com/modelcontextprotocol/servers

**Categories:**
- Database (PostgreSQL, SQLite, etc.)
- File systems
- Web/API integrations
- Developer tools

#### Step 3: Search Community Servers

**GitHub search queries:**
```
"mcp server" [capability] language:python
"fastmcp" [capability]
"model context protocol" [capability]
```

**Awesome lists:**
- Search for "awesome-mcp" repositories
- Check MCP Discord for recommendations

#### Step 4: Evaluate or Build

Decision tree:
```
Found existing server?
├──► Yes, well-maintained ──► USE IT
├──► Yes, needs updates ──► FORK & MODIFY
├──► No, but similar exists ──► ADAPT
└──► No ──► BUILD WITH FASTMCP
```

---

### MCP Server Evaluation Criteria

#### Must-Have

| Criteria | Check |
|----------|-------|
| Python or TypeScript | [ ] |
| Active maintenance (<6 months) | [ ] |
| Clear documentation | [ ] |
| Error handling | [ ] |
| Security considerations | [ ] |

#### Nice-to-Have

| Criteria | Check |
|----------|-------|
| Type hints | [ ] |
| Tests included | [ ] |
| Docker support | [ ] |
| Config via env vars | [ ] |
| Async support | [ ] |

#### Red Flags

- No updates in >1 year
- No error handling
- Hardcoded credentials
- No documentation
- Depends on deprecated packages

---

### Building with FastMCP

#### When to Build

- No existing server for your need
- Existing servers are poorly maintained
- Need custom integration with your stack
- Want tighter control over security

#### FastMCP Quickstart

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

#### Project Structure

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

### Common MCP Server Categories

#### Data & Databases

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-postgres | PostgreSQL queries | Stable |
| mcp-server-sqlite | SQLite operations | Stable |
| mcp-server-supabase | Supabase integration | Community |

#### File Systems

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-filesystem | Local file access | Official |
| mcp-server-gdrive | Google Drive | Community |
| mcp-server-s3 | AWS S3 | Community |

#### Web & APIs

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-fetch | HTTP requests | Official |
| mcp-server-brave | Brave search | Official |
| mcp-server-github | GitHub API | Community |

#### Developer Tools

| Server | Purpose | Maturity |
|--------|---------|----------|
| mcp-server-git | Git operations | Official |
| mcp-server-docker | Container management | Community |
| mcp-server-kubernetes | K8s operations | Community |

---

### Integration with Claude Desktop

#### Configuration File Location

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Configuration Format

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

#### Common Patterns

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

### Debugging MCP Servers

#### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Test Tools Locally

```python
# test_tools.py
import asyncio
from my_server.tools import my_tool

async def test():
    result = await my_tool("test input")
    print(result)

asyncio.run(test())
```

#### Check Server Status

In Claude Desktop:
1. Open Developer Tools
2. Check Console for MCP errors
3. Look for connection issues

#### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Server not starting | Python path | Use absolute path |
| Tools not showing | Import error | Check logs |
| Timeout errors | Slow operations | Add async, increase timeout |
| Auth failures | Wrong env vars | Check .env loading |

---

### Security Considerations

#### Environment Variables

```python
# Good: Load from environment
import os
api_key = os.environ.get("API_KEY")

# Bad: Hardcoded
api_key = "sk-xxx"  # NEVER DO THIS
```

#### Input Validation

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

#### Scope Limitation

```python
# Limit file access to specific directories
ALLOWED_DIRS = ["/Users/tmkipper/Desktop/tk_projects"]

def is_allowed_path(path: str) -> bool:
    return any(path.startswith(d) for d in ALLOWED_DIRS)
```

---

### MCP Server Template

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
