# API Integration Patterns

## Common Integration Architectures

### Pattern 1: Direct API Call

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

### Pattern 2: SDK Wrapper

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

### Pattern 3: Multi-Provider Router

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

### Pattern 4: Queue-Based Processing

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

## Error Handling Patterns

### Retry with Exponential Backoff

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

### Circuit Breaker

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

## Rate Limiting Patterns

### Token Bucket

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

### Sliding Window

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

## Caching Patterns

### Response Cache

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

### Semantic Cache (with embeddings)

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

## Webhook Patterns

### Webhook Receiver

```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

@app.post("/webhook/{provider}")
async def receive_webhook(provider: str, request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature")
    
    if not verify_signature(body, signature, provider):
        raise HTTPException(status_code=401)
        
    payload = await request.json()
    await process_webhook(provider, payload)
    return {"status": "ok"}

def verify_signature(body: bytes, signature: str, provider: str) -> bool:
    secret = get_webhook_secret(provider)
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)
```

---

## Configuration Management

### Environment-Based Config

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

### Feature Flags

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
