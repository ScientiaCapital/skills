# Serverless Workers - Deep Dive

Complete reference for RunPod serverless worker development.

## Handler Function Architecture

### Basic Handler Structure

```python
import runpod

def handler(job):
    """
    Core handler function - entry point for all requests.

    Args:
        job (dict): Job object containing:
            - id (str): Unique job identifier
            - input (dict): User-provided input data

    Returns:
        dict: Result to return to client
        generator: For streaming responses
    """
    job_id = job["id"]
    job_input = job["input"]

    # Process request
    result = process(job_input)

    return {"output": result}

# Start the worker
runpod.serverless.start({"handler": handler})
```

### Handler Lifecycle

```
Request → Queue → Worker Allocation → Handler Execution → Response
                        ↓
                  Cold Start (if no workers ready)
                  30-60s for model loading
```

---

## Streaming Responses

### Generator Pattern

For real-time streaming (LLMs, TTS, progressive results):

```python
import runpod

def handler(job):
    """Streaming handler using generator."""
    job_input = job["input"]
    prompt = job_input.get("prompt", "")

    def stream_tokens():
        for token in model.generate_stream(prompt):
            yield {
                "token": token,
                "finished": False
            }
        yield {
            "token": "",
            "finished": True,
            "usage": {"tokens": token_count}
        }

    return stream_tokens()

runpod.serverless.start({
    "handler": handler,
    "return_aggregate_stream": True  # Aggregate all yields into final response
})
```

### Client-Side Streaming

```python
import runpod

# Initialize client
runpod.api_key = os.environ["RUNPOD_API_KEY"]

# Start streaming request
endpoint = runpod.Endpoint("your-endpoint-id")
job = endpoint.run({"prompt": "Write a story about..."})

# Stream results as they arrive
for chunk in job.stream():
    output = chunk.get("output", {})
    token = output.get("token", "")
    print(token, end="", flush=True)

    if output.get("finished"):
        break

# Get final aggregated result
final = job.output()
```

### Streaming with Metadata

```python
def handler(job):
    """Stream with progress metadata."""
    job_input = job["input"]
    items = job_input.get("items", [])
    total = len(items)

    def process_stream():
        for i, item in enumerate(items):
            result = process_item(item)
            yield {
                "result": result,
                "progress": (i + 1) / total * 100,
                "remaining": total - i - 1,
                "finished": i == total - 1
            }

    return process_stream()
```

---

## Progress Updates

### Long-Running Jobs

For jobs that take time (training, batch processing):

```python
import runpod

def handler(job):
    """Handler with progress updates for long-running jobs."""
    job_input = job["input"]
    items = job_input.get("items", [])
    total = len(items)
    results = []

    for i, item in enumerate(items):
        # Process item
        result = process(item)
        results.append(result)

        # Update progress (0-100 percentage)
        progress = int((i + 1) / total * 100)
        runpod.serverless.progress_update(job, progress)

    return {
        "results": results,
        "total_processed": total
    }

runpod.serverless.start({"handler": handler})
```

### Progress with Status Messages

```python
def handler(job):
    """Progress updates with status messages."""
    job_id = job["id"]
    job_input = job["input"]

    # Stage 1: Preprocessing
    runpod.serverless.progress_update(job, 10, "Preprocessing input...")
    preprocessed = preprocess(job_input)

    # Stage 2: Inference
    runpod.serverless.progress_update(job, 30, "Running inference...")
    inference_result = model.predict(preprocessed)

    # Stage 3: Postprocessing
    runpod.serverless.progress_update(job, 80, "Postprocessing results...")
    final_result = postprocess(inference_result)

    # Complete
    runpod.serverless.progress_update(job, 100, "Complete")

    return {"result": final_result}
```

### Client-Side Progress Polling

```python
import runpod
import time

endpoint = runpod.Endpoint("your-endpoint-id")

# Start async job
job = endpoint.run({"items": large_dataset}, is_async=True)

# Poll for progress
while True:
    status = job.status()

    if status["status"] == "COMPLETED":
        result = job.output()
        break
    elif status["status"] == "FAILED":
        raise Exception(f"Job failed: {status.get('error')}")
    elif status["status"] == "IN_PROGRESS":
        progress = status.get("progress", 0)
        print(f"Progress: {progress}%")

    time.sleep(2)
```

---

## Async Handlers

### Async/Await Pattern

```python
import runpod
import asyncio
import aiohttp

async def async_handler(job):
    """Async handler for concurrent I/O operations."""
    job_input = job["input"]
    urls = job_input.get("urls", [])

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return {"results": results}

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

runpod.serverless.start({"handler": async_handler})
```

### Concurrent Model Calls

```python
import runpod
import asyncio

async def async_handler(job):
    """Concurrent model inference."""
    job_input = job["input"]
    prompts = job_input.get("prompts", [])

    # Run multiple inferences concurrently
    tasks = [infer_async(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)

    return {"results": results}

async def infer_async(prompt):
    """Async wrapper for model inference."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, model.generate, prompt)
```

---

## Error Handling Patterns

### Comprehensive Error Handler

```python
import runpod
import traceback
import torch

def handler(job):
    """Production error handling."""
    job_id = job["id"]

    try:
        job_input = job["input"]

        # Validate input
        validation_error = validate(job_input)
        if validation_error:
            return {
                "error": validation_error,
                "status": "VALIDATION_FAILED",
                "retry": False
            }

        # Process
        result = process(job_input)

        return {
            "output": result,
            "status": "SUCCESS"
        }

    except torch.cuda.OutOfMemoryError:
        # OOM - don't retry, need smaller input
        return {
            "error": "GPU out of memory. Reduce input size or max_tokens.",
            "status": "OOM_ERROR",
            "retry": False
        }

    except TimeoutError:
        # Timeout - may succeed on retry
        return {
            "error": "Request timed out",
            "status": "TIMEOUT",
            "retry": True
        }

    except ConnectionError as e:
        # Network issue - retry
        return {
            "error": f"Connection error: {str(e)}",
            "status": "CONNECTION_ERROR",
            "retry": True
        }

    except Exception as e:
        # Unknown error - log and retry
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "UNKNOWN_ERROR",
            "retry": True
        }

runpod.serverless.start({"handler": handler})
```

### Retry Configuration

```python
# Client-side retry handling
endpoint = runpod.Endpoint("your-endpoint-id")

def run_with_retry(input_data, max_retries=3):
    """Run job with automatic retry."""
    for attempt in range(max_retries):
        try:
            result = endpoint.run_sync(input_data, timeout=120)

            if result.get("retry") == True:
                print(f"Retry requested, attempt {attempt + 1}")
                continue

            return result

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff

    raise Exception("Max retries exceeded")
```

---

## Input Validation

### Schema Validation

```python
from pydantic import BaseModel, validator
from typing import List, Optional

class InferenceInput(BaseModel):
    """Validated input schema."""
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7
    messages: Optional[List[dict]] = None

    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        if v < 1 or v > 4096:
            raise ValueError('max_tokens must be between 1 and 4096')
        return v

    @validator('temperature')
    def validate_temperature(cls, v):
        if v < 0 or v > 2:
            raise ValueError('temperature must be between 0 and 2')
        return v

def handler(job):
    """Handler with Pydantic validation."""
    try:
        validated = InferenceInput(**job["input"])
    except ValueError as e:
        return {"error": str(e), "status": "VALIDATION_ERROR"}

    result = model.generate(
        validated.prompt,
        max_tokens=validated.max_tokens,
        temperature=validated.temperature
    )

    return {"output": result}
```

### Manual Validation

```python
def validate_input(job_input: dict) -> tuple[bool, str]:
    """Manual input validation."""
    if not job_input:
        return False, "Empty input"

    # Required fields
    if "prompt" not in job_input and "messages" not in job_input:
        return False, "Either 'prompt' or 'messages' required"

    # Type checks
    if "max_tokens" in job_input:
        if not isinstance(job_input["max_tokens"], int):
            return False, "max_tokens must be integer"
        if job_input["max_tokens"] > 4096:
            return False, "max_tokens exceeds limit of 4096"

    # Content checks
    prompt = job_input.get("prompt", "")
    if len(prompt) > 100000:
        return False, "prompt exceeds 100k character limit"

    return True, ""
```

---

## Startup Configuration

### Model Loading at Startup

```python
import runpod
import os
import time

# Load BEFORE handler definition for warm workers
print("Loading model...")
start = time.time()

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print(f"Model loaded in {time.time() - start:.2f}s")

def handler(job):
    """Handler uses pre-loaded model."""
    # model is already in GPU memory
    ...

runpod.serverless.start({"handler": handler})
```

### Startup Options

```python
runpod.serverless.start({
    "handler": handler,

    # Aggregate streaming yields into final response
    "return_aggregate_stream": True,

    # Custom settings (if supported)
    "refresh_worker": False,  # Keep worker hot between jobs
})
```

---

## Testing Locally

### Local Testing Script

```python
#!/usr/bin/env python3
"""Test handler locally before deploying."""

import json
import os

# Set test environment
os.environ["MODEL_NAME"] = "Qwen/Qwen2.5-0.5B"  # Small model for testing
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Import handler after setting environment
from handler import handler

# Test cases
test_cases = [
    {
        "id": "test-1",
        "input": {
            "prompt": "Hello, world!",
            "max_tokens": 50
        }
    },
    {
        "id": "test-2",
        "input": {
            "messages": [
                {"role": "user", "content": "What is 2+2?"}
            ],
            "max_tokens": 100
        }
    }
]

for test in test_cases:
    print(f"\n=== Test: {test['id']} ===")
    result = handler(test)
    print(json.dumps(result, indent=2))
```

### Mock RunPod for Testing

```python
import unittest
from unittest.mock import patch, MagicMock

class TestHandler(unittest.TestCase):
    def test_basic_inference(self):
        """Test basic inference flow."""
        job = {
            "id": "test-123",
            "input": {"prompt": "Test prompt", "max_tokens": 50}
        }

        result = handler(job)

        self.assertIn("output", result)
        self.assertNotIn("error", result)

    def test_validation_error(self):
        """Test input validation."""
        job = {
            "id": "test-456",
            "input": {}  # Missing required fields
        }

        result = handler(job)

        self.assertIn("error", result)
        self.assertEqual(result["status"], "VALIDATION_ERROR")

    def test_oom_handling(self):
        """Test OOM error handling."""
        with patch('handler.model.generate') as mock_gen:
            mock_gen.side_effect = torch.cuda.OutOfMemoryError()

            job = {"id": "test-789", "input": {"prompt": "Test"}}
            result = handler(job)

            self.assertEqual(result["status"], "OOM_ERROR")
            self.assertEqual(result["retry"], False)
```

---

## Best Practices

### Performance Optimization

1. **Load models outside handler** - Avoid cold start on every request
2. **Use appropriate batch sizes** - Balance throughput vs latency
3. **Enable torch.compile** - JIT compilation for faster inference
4. **Use float16/bfloat16** - Half precision for 2x speed

### Memory Management

```python
import gc
import torch

def handler(job):
    try:
        result = process(job["input"])
        return result
    finally:
        # Clear CUDA cache after each job
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
```

### Logging Standards

```python
import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def handler(job):
    job_id = job["id"]
    start = datetime.now()

    logger.info(f"Job started: {job_id}")

    try:
        result = process(job["input"])
        duration = (datetime.now() - start).total_seconds()
        logger.info(f"Job completed: {job_id} in {duration:.2f}s")
        return result

    except Exception as e:
        logger.error(f"Job failed: {job_id} - {str(e)}")
        raise
```
