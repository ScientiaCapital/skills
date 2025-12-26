---
name: runpod-deployment-skill
description: |
  Expert-level RunPod deployment patterns for GPU-accelerated AI workloads.
  Covers serverless workers, pod management, auto-scaling, cost optimization,
  health monitoring, and production model deployment. Use when deploying ML
  models, setting up vLLM/TGI endpoints, configuring serverless GPU workers,
  managing RunPod infrastructure, or optimizing GPU costs.

  Triggers: "deploy to RunPod", "GPU serverless", "vLLM endpoint", "TGI deployment",
  "A100 deployment", "H100 setup", "scale to zero", "RunPod worker", "serverless handler",
  "GPU cost optimization", "model serving", "inference endpoint".

  Note: M1/M2 Mac requires GitHub Actions for Docker builds (ARM incompatible with RunPod x86 GPUs).
---

# RunPod Deployment Skill

Expert-level GPU deployment patterns for production AI/ML workloads.

## Table of Contents

1. [M1 Mac Deployment](#m1-mac-deployment-critical)
2. [GPU Selection Matrix](#gpu-selection-matrix)
3. [Serverless Workers](#serverless-workers)
4. [Pod Management](#pod-management)
5. [Auto-Scaling Configuration](#auto-scaling-configuration)
6. [Cost Optimization](#cost-optimization)
7. [Health Checks & Monitoring](#health-checks--monitoring)
8. [Model Deployment Patterns](#model-deployment-patterns)
9. [Template Creation](#template-creation)
10. [Production Patterns](#production-patterns)
11. [Integration Notes](#integration-notes)

---

## M1 Mac Deployment (CRITICAL)

**Cannot build Docker images locally on M1/M2** - ARM architecture incompatible with RunPod's x86 GPUs.

**Solution: GitHub Actions builds the image for you.**

```bash
# 1. Push code to GitHub (no local docker build)
git add . && git commit -m "Deploy to RunPod" && git push

# 2. GitHub Actions builds x86 image and deploys
# See reference/cicd.md for complete workflow
```

**Never run `docker build` locally for RunPod on Apple Silicon.**

---

## GPU Selection Matrix

### Comprehensive GPU Pricing (December 2024)

| GPU | VRAM | Cost/hr | Best For | Max Model Size |
|-----|------|---------|----------|----------------|
| RTX 4090 | 24GB | $0.44 | 7B-8B inference, embeddings | 13B quantized |
| RTX A4000 | 16GB | $0.36 | Embeddings, small models | 7B quantized |
| RTX A5000 | 24GB | $0.47 | 7B-8B models | 13B quantized |
| RTX A6000 | 48GB | $0.79 | 13B-30B models, fine-tuning | 34B quantized |
| A100 40GB | 40GB | $1.64 | 30B models, production | 40B quantized |
| A100 80GB | 80GB | $1.89 | 70B models, multi-GPU | 70B quantized |
| H100 80GB | 80GB | $4.69 | 70B+ models, training | 70B+ |
| H200 141GB | 141GB | $5.99 | Largest models, training | 120B+ |

### GPU Selection Decision Tree

```python
def select_gpu(model_size_b: float, use_case: str, quantized: bool = False) -> str:
    """Select optimal GPU based on model size and use case."""
    effective_size = model_size_b * (0.5 if quantized else 1.0)

    # Embeddings and small models
    if use_case == "embeddings" or effective_size <= 3:
        return "RTX_A4000"  # $0.36/hr - most cost effective

    # 7B-8B models
    elif effective_size <= 8:
        return "RTX_4090"   # $0.44/hr - best perf/cost for this tier

    # 13B-30B models
    elif effective_size <= 30:
        return "RTX_A6000"  # $0.79/hr - 48GB handles 30B quantized

    # 30B-70B models
    elif effective_size <= 70:
        return "A100_80GB"  # $1.89/hr - production-grade

    # Training or 70B+ inference
    else:
        return "H100_80GB"  # $4.69/hr - maximum performance
```

### Spot Instance Pricing

Spot instances offer 50-80% savings for interruptible workloads:

| GPU | On-Demand | Spot | Savings |
|-----|-----------|------|---------|
| RTX 4090 | $0.44/hr | $0.18/hr | 59% |
| A100 80GB | $1.89/hr | $0.76/hr | 60% |
| H100 80GB | $4.69/hr | $1.88/hr | 60% |

**Use spot for:** Training, batch processing, non-real-time inference

---

## Serverless Workers

### Handler Function Pattern

The core of any RunPod serverless worker:

```python
import runpod

def handler(job):
    """
    Main handler function - receives job, returns result.

    Args:
        job (dict): Contains 'id' and 'input' keys

    Returns:
        dict | generator: Result or streaming generator
    """
    job_input = job["input"]

    # Your inference logic here
    prompt = job_input.get("prompt", "")
    max_tokens = job_input.get("max_tokens", 512)

    result = run_inference(prompt, max_tokens)

    return {"output": result}

# Start the serverless worker
runpod.serverless.start({"handler": handler})
```

### Streaming Responses

For real-time token streaming (LLMs, TTS):

```python
import runpod

def handler(job):
    """Streaming handler using generator pattern."""
    job_input = job["input"]
    prompt = job_input.get("prompt", "")

    # Generator function for streaming
    def generate_tokens():
        for token in model.stream(prompt):
            yield {"token": token, "finished": False}
        yield {"token": "", "finished": True}

    return generate_tokens()

runpod.serverless.start({"handler": handler})
```

**Client-side streaming:**

```python
import runpod

# Start streaming job
job = runpod.Endpoint("endpoint_id").run({
    "prompt": "Write a story"
})

# Stream results
for chunk in job.stream():
    print(chunk["output"]["token"], end="", flush=True)
```

### Progress Updates

For long-running jobs (training, batch processing):

```python
import runpod

def handler(job):
    """Handler with progress updates."""
    items = job["input"]["items"]
    total = len(items)
    results = []

    for i, item in enumerate(items):
        # Process item
        result = process(item)
        results.append(result)

        # Update progress (0-100)
        progress = int((i + 1) / total * 100)
        runpod.serverless.progress_update(job, progress)

    return {"results": results, "processed": total}

runpod.serverless.start({"handler": handler})
```

### Async Handler Pattern

For I/O-bound workloads:

```python
import runpod
import asyncio

async def async_handler(job):
    """Async handler for concurrent operations."""
    job_input = job["input"]
    tasks = job_input.get("tasks", [])

    # Run tasks concurrently
    results = await asyncio.gather(*[
        process_async(task) for task in tasks
    ])

    return {"results": results}

runpod.serverless.start({
    "handler": async_handler
})
```

### Error Handling

Production-grade error handling:

```python
import runpod
import traceback

def handler(job):
    """Handler with comprehensive error handling."""
    try:
        job_input = job["input"]

        # Validate input
        if "prompt" not in job_input:
            return {"error": "Missing required field: prompt", "status": "FAILED"}

        result = run_inference(job_input["prompt"])
        return {"output": result, "status": "COMPLETED"}

    except torch.cuda.OutOfMemoryError:
        return {
            "error": "GPU out of memory - try reducing input size",
            "status": "FAILED",
            "retry": False  # Don't retry OOM errors
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "FAILED",
            "retry": True
        }

runpod.serverless.start({"handler": handler})
```

---

## Pod Management

### Pod Types

**Serverless (Recommended for inference):**
- Scale to zero when idle
- Pay per second of compute
- Auto-scaling built in
- Best for: API endpoints, variable workloads

**On-Demand Pods:**
- Fixed hourly rate
- Always running
- SSH access available
- Best for: Development, long training runs

**Spot Pods:**
- 50-80% cheaper than on-demand
- Can be interrupted
- Best for: Batch processing, training checkpoints

### Creating Pods via API

```python
import runpod

# Create serverless endpoint
endpoint = runpod.Endpoint.create(
    name="my-inference-endpoint",
    template_id="your-template-id",
    gpu_type_ids=["NVIDIA GeForce RTX 4090"],
    workers_min=0,
    workers_max=5,
    idle_timeout=60,
    gpu_count=1
)

# Create on-demand pod
pod = runpod.Pod.create(
    name="training-pod",
    image_name="runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04",
    gpu_type_id="NVIDIA A100 80GB PCIe",
    gpu_count=2,
    volume_in_gb=100,
    container_disk_in_gb=50,
    env={
        "HF_TOKEN": "your-token",
        "WANDB_API_KEY": "your-key"
    }
)
```

### GraphQL API for Advanced Operations

```python
import requests

def create_endpoint_graphql(api_key: str, config: dict) -> dict:
    """Create endpoint using GraphQL for full control."""
    query = """
    mutation createEndpoint($input: EndpointInput!) {
        createEndpoint(input: $input) {
            id
            name
            templateId
            gpuIds
            workersMin
            workersMax
            idleTimeout
        }
    }
    """

    variables = {
        "input": {
            "name": config["name"],
            "templateId": config["template_id"],
            "gpuIds": config["gpu_ids"],
            "workersMin": config.get("workers_min", 0),
            "workersMax": config.get("workers_max", 3),
            "idleTimeout": config.get("idle_timeout", 60),
            "scalerType": config.get("scaler_type", "QUEUE_DELAY"),
            "scalerValue": config.get("scaler_value", 2)
        }
    }

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()
```

---

## Auto-Scaling Configuration

### Scaler Types

**QUEUE_DELAY (Default):**
- Scales based on queue wait time
- Best for: Variable request patterns

**REQUEST_COUNT:**
- Scales based on pending requests
- Best for: Predictable workloads

```python
endpoint_config = {
    "name": "my-endpoint",
    "scaler_type": "QUEUE_DELAY",
    "scaler_value": 2,  # Target 2 seconds queue delay
    "workers_min": 0,
    "workers_max": 10,
    "idle_timeout": 30
}
```

### Auto-Scaling Best Practices

```python
def configure_autoscaling(use_case: str) -> dict:
    """Configure auto-scaling based on use case."""

    configs = {
        "interactive_api": {
            "workers_min": 1,      # Always warm
            "workers_max": 5,
            "idle_timeout": 120,   # 2 min
            "scaler_type": "QUEUE_DELAY",
            "scaler_value": 1      # 1 second target latency
        },
        "batch_processing": {
            "workers_min": 0,
            "workers_max": 20,
            "idle_timeout": 30,
            "scaler_type": "REQUEST_COUNT",
            "scaler_value": 5      # 5 requests per worker
        },
        "cost_optimized": {
            "workers_min": 0,
            "workers_max": 3,
            "idle_timeout": 15,    # Aggressive scale-down
            "scaler_type": "QUEUE_DELAY",
            "scaler_value": 5      # Allow some queue time
        }
    }

    return configs.get(use_case, configs["cost_optimized"])
```

---

## Cost Optimization

### Cost Reduction Strategies

**1. Scale-to-Zero:**
```python
# Most aggressive cost savings
config = {
    "workers_min": 0,
    "idle_timeout": 15,  # Scale down after 15s idle
}
```

**2. GPU Right-Sizing:**
```python
def estimate_monthly_cost(
    gpu_type: str,
    daily_requests: int,
    avg_processing_time_s: float
) -> float:
    """Estimate monthly cost based on usage patterns."""

    gpu_costs = {
        "RTX_4090": 0.44,
        "RTX_A4000": 0.36,
        "RTX_A6000": 0.79,
        "A100_80GB": 1.89,
        "H100_80GB": 4.69
    }

    hourly_rate = gpu_costs.get(gpu_type, 1.0)

    # Calculate compute hours
    daily_compute_hours = (daily_requests * avg_processing_time_s) / 3600
    monthly_compute_hours = daily_compute_hours * 30

    # Add cold start overhead (assume 30s per cold start)
    cold_starts_per_day = 24  # One per hour if scale-to-zero
    cold_start_overhead = (cold_starts_per_day * 30 * 30) / 3600

    total_hours = monthly_compute_hours + cold_start_overhead

    return total_hours * hourly_rate
```

**3. Quantization for Lower GPU Tier:**
```python
# Instead of A100 for 70B model, use A6000 with quantization
env_vars = {
    "MODEL_NAME": "meta-llama/Llama-3.1-70B-Instruct",
    "QUANTIZATION": "AWQ",  # 4-bit quantization
    "GPU_MEMORY_UTILIZATION": 0.95
}
# A6000 ($0.79/hr) instead of A100 ($1.89/hr) = 58% savings
```

**4. Batch Requests:**
```python
def batch_inference(requests: list, batch_size: int = 8) -> list:
    """Batch multiple requests for better GPU utilization."""
    results = []
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        batch_results = model.generate(batch)
        results.extend(batch_results)
    return results
```

### Cost Monitoring

```python
class CostController:
    """Real-time cost monitoring and budget enforcement."""

    def __init__(self, daily_budget: float = 50.0, alert_threshold: float = 0.8):
        self.daily_budget = daily_budget
        self.alert_threshold = alert_threshold
        self.spent_today = 0.0

    async def track_job(self, job_id: str, duration_s: float, gpu_rate: float):
        """Track job cost and enforce budget."""
        job_cost = (duration_s / 3600) * gpu_rate
        self.spent_today += job_cost

        # Alert at threshold
        if self.spent_today >= self.daily_budget * self.alert_threshold:
            await self.send_alert(
                f"Budget alert: ${self.spent_today:.2f} of ${self.daily_budget:.2f}"
            )

        # Hard stop at budget
        if self.spent_today >= self.daily_budget:
            await self.scale_to_zero()
            raise BudgetExceededError(f"Daily budget of ${self.daily_budget} exceeded")

        return job_cost
```

---

## Health Checks & Monitoring

### Health Check Implementation

```python
import runpod

async def health_check(endpoint_id: str) -> dict:
    """Comprehensive health check for RunPod endpoint."""
    endpoint = runpod.Endpoint(endpoint_id)

    health = await endpoint.health()

    return {
        "endpoint_id": endpoint_id,
        "status": health.status,
        "workers": {
            "ready": health.workers.ready,
            "running": health.workers.running,
            "pending": health.workers.pending,
            "throttled": health.workers.throttled
        },
        "queue": {
            "depth": health.queue.in_queue,
            "in_progress": health.queue.in_progress,
            "completed": health.queue.completed
        },
        "metrics": {
            "requests_per_minute": health.metrics.requests_per_minute,
            "avg_execution_time_ms": health.metrics.avg_execution_time,
            "avg_cold_start_time_ms": health.metrics.avg_cold_start_time
        }
    }
```

### GraphQL Monitoring Queries

```python
def get_endpoint_metrics(api_key: str, endpoint_id: str) -> dict:
    """Get detailed endpoint metrics via GraphQL."""
    query = """
    query getEndpoint($id: String!) {
        endpoint(id: $id) {
            id
            name
            status
            workersMin
            workersMax
            gpuType
            createdAt

            workers {
                ready
                running
                pending
                initializing
                throttled
            }

            queue {
                inQueue
                inProgress
                completed
                failed
                cancelled
            }

            metrics {
                requestsPerMinute
                avgExecutionTimeMs
                avgColdStartTimeMs
                p95ExecutionTimeMs
                successRate
            }
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": {"id": endpoint_id}},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()["data"]["endpoint"]
```

### Logging Best Practices

```python
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}'
)
logger = logging.getLogger(__name__)

def handler(job):
    """Handler with structured logging."""
    job_id = job["id"]
    start_time = datetime.now()

    logger.info(json.dumps({
        "event": "job_started",
        "job_id": job_id,
        "input_size": len(str(job["input"]))
    }))

    try:
        result = process(job["input"])

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(json.dumps({
            "event": "job_completed",
            "job_id": job_id,
            "duration_s": duration,
            "output_size": len(str(result))
        }))

        return result

    except Exception as e:
        logger.error(json.dumps({
            "event": "job_failed",
            "job_id": job_id,
            "error": str(e)
        }))
        raise

runpod.serverless.start({"handler": handler})
```

---

## Model Deployment Patterns

### HuggingFace Model Deployment

```python
# Environment variables for HuggingFace models
env_vars = {
    "MODEL_NAME": "meta-llama/Llama-3.1-8B-Instruct",
    "HF_TOKEN": "${HF_TOKEN}",  # For gated models
    "MAX_MODEL_LEN": "8192",
    "GPU_MEMORY_UTILIZATION": "0.95",
    "TENSOR_PARALLEL_SIZE": "1"
}
```

**Handler for HuggingFace models:**

```python
import runpod
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model at startup (outside handler)
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

def handler(job):
    """HuggingFace model inference handler."""
    job_input = job["input"]

    messages = job_input.get("messages", [])
    max_tokens = job_input.get("max_tokens", 512)
    temperature = job_input.get("temperature", 0.7)

    # Format for chat
    prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=temperature > 0
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"response": response}

runpod.serverless.start({"handler": handler})
```

### vLLM Deployment

```python
# vLLM environment configuration
vllm_env = {
    "MODEL_NAME": "meta-llama/Llama-3.1-70B-Instruct",
    "HF_TOKEN": "${HF_TOKEN}",
    "TENSOR_PARALLEL_SIZE": "2",  # For multi-GPU
    "MAX_MODEL_LEN": "16384",
    "GPU_MEMORY_UTILIZATION": "0.95",
    "QUANTIZATION": "awq",  # Optional: AWQ, GPTQ, or None
    "ENFORCE_EAGER": "false"  # Set true if CUDA issues
}
```

**vLLM handler:**

```python
import runpod
from vllm import LLM, SamplingParams

# Initialize vLLM engine at startup
llm = LLM(
    model=os.environ["MODEL_NAME"],
    tensor_parallel_size=int(os.environ.get("TENSOR_PARALLEL_SIZE", 1)),
    gpu_memory_utilization=float(os.environ.get("GPU_MEMORY_UTILIZATION", 0.95)),
    max_model_len=int(os.environ.get("MAX_MODEL_LEN", 8192))
)

def handler(job):
    """vLLM inference handler with OpenAI-compatible interface."""
    job_input = job["input"]

    # OpenAI-compatible parameters
    messages = job_input.get("messages", [])
    max_tokens = job_input.get("max_tokens", 512)
    temperature = job_input.get("temperature", 0.7)
    top_p = job_input.get("top_p", 0.95)

    # Format prompt
    prompt = format_chat_prompt(messages)

    sampling_params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p
    )

    outputs = llm.generate([prompt], sampling_params)
    response = outputs[0].outputs[0].text

    return {
        "choices": [{
            "message": {"role": "assistant", "content": response},
            "finish_reason": "stop"
        }]
    }

runpod.serverless.start({"handler": handler})
```

### Text Generation Inference (TGI)

```python
# TGI environment configuration
tgi_env = {
    "MODEL_ID": "meta-llama/Llama-3.1-8B-Instruct",
    "HUGGING_FACE_HUB_TOKEN": "${HF_TOKEN}",
    "MAX_INPUT_LENGTH": "4096",
    "MAX_TOTAL_TOKENS": "8192",
    "MAX_BATCH_PREFILL_TOKENS": "4096",
    "QUANTIZE": "awq"  # Optional
}
```

### Voice/Audio Model Deployment (VozLux Pattern)

```python
import runpod
import torch
from TTS.api import TTS

# Initialize TTS at startup
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

def handler(job):
    """Voice synthesis handler for VozLux."""
    job_input = job["input"]

    text = job_input["text"]
    speaker_wav = job_input.get("speaker_wav")  # Voice cloning reference
    language = job_input.get("language", "en")

    # Generate audio
    if speaker_wav:
        # Voice cloning
        wav = tts.tts(
            text=text,
            speaker_wav=speaker_wav,
            language=language
        )
    else:
        wav = tts.tts(text=text, language=language)

    # Convert to base64 for transport
    audio_base64 = encode_audio(wav)

    return {"audio": audio_base64, "format": "wav"}

runpod.serverless.start({"handler": handler})
```

### Document Processing (FieldVault Pattern)

```python
import runpod
from transformers import AutoProcessor, AutoModelForVision2Seq
import torch

# Initialize DocVQA model at startup
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large")
model = AutoModelForVision2Seq.from_pretrained(
    "microsoft/Florence-2-large",
    torch_dtype=torch.float16,
    device_map="auto"
)

def handler(job):
    """Document processing handler for FieldVault-AI."""
    job_input = job["input"]

    image_base64 = job_input["image"]
    task = job_input.get("task", "OCR")

    # Decode image
    image = decode_image(image_base64)

    # Process based on task
    if task == "OCR":
        prompt = "<OCR>"
    elif task == "CAPTION":
        prompt = "<CAPTION>"
    elif task == "EXTRACT":
        prompt = f"<DETAILED_CAPTION>{job_input.get('fields', '')}"

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=1024)

    result = processor.decode(outputs[0], skip_special_tokens=True)

    return {"extracted": result}

runpod.serverless.start({"handler": handler})
```

---

## Template Creation

### Dockerfile Pattern

```dockerfile
# Base image with CUDA and Python
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download model (optional, increases image size but faster cold starts)
# RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('your-model')"

# RunPod handler entrypoint
CMD ["python", "-u", "handler.py"]
```

### runpod.toml Configuration

```toml
# runpod.toml - Project configuration

[project]
name = "my-inference-endpoint"
base_image = "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04"
gpu_types = ["NVIDIA GeForce RTX 4090", "NVIDIA RTX A5000"]
gpu_count = 1
volume_mount_path = "/runpod-volume"

[deploy]
workers_min = 0
workers_max = 5
idle_timeout = 60
scaler_type = "QUEUE_DELAY"
scaler_value = 2

[env]
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
MAX_MODEL_LEN = "8192"
GPU_MEMORY_UTILIZATION = "0.95"
# HF_TOKEN = "${HF_TOKEN}"  # Injected from secrets

[build]
include = ["handler.py", "requirements.txt", "src/"]
```

---

## Production Patterns

### Complete Production Worker

```python
#!/usr/bin/env python3
"""Production-ready RunPod serverless worker."""

import os
import time
import logging
import traceback
from typing import Generator, Dict, Any

import runpod
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration from environment
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 2048))
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load model at startup (outside handler for performance)
logger.info(f"Loading model: {MODEL_NAME}")
start_load = time.time()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

logger.info(f"Model loaded in {time.time() - start_load:.2f}s")


def validate_input(job_input: Dict[str, Any]) -> tuple[bool, str]:
    """Validate job input before processing."""
    if not job_input:
        return False, "Empty input"

    if "messages" not in job_input and "prompt" not in job_input:
        return False, "Either 'messages' or 'prompt' required"

    max_tokens = job_input.get("max_tokens", 512)
    if max_tokens > MAX_TOKENS:
        return False, f"max_tokens exceeds limit of {MAX_TOKENS}"

    return True, ""


def generate_response(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.7,
    stream: bool = False
) -> str | Generator:
    """Generate model response."""
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        if stream:
            # Streaming generation
            def token_generator():
                for output in model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=temperature > 0,
                    streamer=True
                ):
                    token = tokenizer.decode(output, skip_special_tokens=True)
                    yield {"token": token, "finished": False}
                yield {"token": "", "finished": True}
            return token_generator()
        else:
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0
            )
            return tokenizer.decode(outputs[0], skip_special_tokens=True)


def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main handler function for RunPod serverless.

    Supports:
    - Chat completion (messages array)
    - Text completion (prompt string)
    - Streaming responses
    - Progress updates for batch processing
    """
    job_id = job["id"]
    job_input = job["input"]

    logger.info(f"Processing job {job_id}")
    start_time = time.time()

    try:
        # Validate input
        valid, error = validate_input(job_input)
        if not valid:
            return {"error": error, "status": "FAILED"}

        # Extract parameters
        messages = job_input.get("messages", [])
        prompt = job_input.get("prompt", "")
        max_tokens = job_input.get("max_tokens", 512)
        temperature = job_input.get("temperature", 0.7)
        stream = job_input.get("stream", False)

        # Format prompt
        if messages:
            prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

        # Generate response
        if stream:
            return generate_response(prompt, max_tokens, temperature, stream=True)
        else:
            response = generate_response(prompt, max_tokens, temperature)

            duration = time.time() - start_time
            logger.info(f"Job {job_id} completed in {duration:.2f}s")

            return {
                "response": response,
                "usage": {
                    "total_time_s": duration,
                    "tokens_generated": len(tokenizer.encode(response))
                }
            }

    except torch.cuda.OutOfMemoryError:
        logger.error(f"Job {job_id}: CUDA OOM")
        return {
            "error": "GPU out of memory. Try reducing max_tokens or input length.",
            "status": "FAILED",
            "retry": False
        }

    except Exception as e:
        logger.error(f"Job {job_id}: {str(e)}\n{traceback.format_exc()}")
        return {
            "error": str(e),
            "status": "FAILED",
            "retry": True
        }


if __name__ == "__main__":
    logger.info("Starting RunPod serverless worker...")
    runpod.serverless.start({
        "handler": handler,
        "return_aggregate_stream": True
    })
```

---

## Integration Notes

### Pairs With Skills

- **trading-signals-skill** - Model serving for trading predictions
- **voice-ai-skill** - VozLux voice synthesis deployment
- **data-analysis-skill** - Large-scale data processing on GPU
- **technical-research-skill** - Embedding generation at scale

### Target Projects

- **VozLux** - Voice inference with XTTS
- **FieldVault-AI** - Document processing with Florence-2
- **Trading models** - Signal prediction serving
- **Sales-Agent** - LLM-powered lead qualification

---

## Reference Files

- `reference/serverless-workers.md` - Handler patterns, streaming, progress updates
- `reference/pod-management.md` - GPU types, spot instances, pricing
- `reference/cost-optimization.md` - Budget controls, right-sizing, quantization
- `reference/monitoring.md` - Health checks, logging, GraphQL queries
- `reference/model-deployment.md` - HuggingFace, vLLM, TGI patterns
- `reference/templates.md` - Dockerfile, runpod.toml configurations
- `reference/vllm-setup.md` - vLLM-specific configuration
- `reference/project-configs.md` - Project-specific deployment configs
- `reference/cicd.md` - GitHub Actions, deployment workflows
- `reference/troubleshooting.md` - Common issues and solutions

---

## Quick Commands

```bash
# Install RunPod CLI
pip install runpod

# Deploy from CLI
runpodctl project deploy --name my-endpoint --gpu-type "NVIDIA RTX 4090"

# Check endpoint health
runpod endpoint health <endpoint_id>

# View logs
runpod endpoint logs <endpoint_id>

# Scale workers
runpod endpoint scale <endpoint_id> --min 1 --max 10
```
