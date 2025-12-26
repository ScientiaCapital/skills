# Templates Reference - Dockerfile & Configuration Patterns

Production-ready templates for RunPod deployments.

## Dockerfile Patterns

### Basic Python Handler

```dockerfile
# Dockerfile for basic Python handler
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY handler.py .
COPY src/ ./src/

# Run handler
CMD ["python", "-u", "handler.py"]
```

### With Model Pre-Download

```dockerfile
# Dockerfile with pre-downloaded model (faster cold starts, larger image)
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build arguments for model download
ARG HF_TOKEN
ARG MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"

# Pre-download model (cached in image)
RUN python -c "import os; os.environ['HF_TOKEN']='${HF_TOKEN}'; \
    from transformers import AutoTokenizer, AutoModelForCausalLM; \
    AutoTokenizer.from_pretrained('${MODEL_NAME}', token='${HF_TOKEN}'); \
    AutoModelForCausalLM.from_pretrained('${MODEL_NAME}', token='${HF_TOKEN}', torch_dtype='auto')"

COPY handler.py .

CMD ["python", "-u", "handler.py"]
```

### vLLM Optimized

```dockerfile
# Dockerfile for vLLM deployment
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

# Install vLLM and dependencies
RUN pip install --no-cache-dir \
    vllm>=0.4.0 \
    runpod \
    ray \
    transformers \
    accelerate

# Copy handler
COPY handler.py .

# vLLM environment defaults
ENV VLLM_ATTENTION_BACKEND=FLASH_ATTN

CMD ["python", "-u", "handler.py"]
```

### Multi-Stage Build (Smaller Image)

```dockerfile
# Multi-stage build for smaller final image
# Stage 1: Build dependencies
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04 as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# Stage 2: Runtime image
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-runtime-ubuntu22.04

WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local/lib/python3.10/dist-packages

# Copy application
COPY handler.py .
COPY src/ ./src/

CMD ["python", "-u", "handler.py"]
```

### With Network Volume

```dockerfile
# Dockerfile for use with network volumes
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

# Models loaded from network volume at runtime
ENV MODEL_CACHE_DIR=/runpod-volume/models

CMD ["python", "-u", "handler.py"]
```

---

## runpod.toml Configuration

### Basic Configuration

```toml
# runpod.toml - Basic serverless endpoint

[project]
name = "my-inference-endpoint"
base_image = "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04"
gpu_types = ["NVIDIA GeForce RTX 4090", "NVIDIA RTX A5000"]
gpu_count = 1

[deploy]
workers_min = 0
workers_max = 5
idle_timeout = 60

[env]
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
MAX_TOKENS = "2048"

[build]
include = ["handler.py", "requirements.txt", "src/"]
```

### Production Configuration

```toml
# runpod.toml - Production deployment

[project]
name = "production-inference"
base_image = "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04"
gpu_types = ["NVIDIA A100 80GB PCIe", "NVIDIA A100 40GB PCIe"]
gpu_count = 1
volume_mount_path = "/runpod-volume"

[deploy]
workers_min = 1          # Always warm for production
workers_max = 10
idle_timeout = 120
scaler_type = "QUEUE_DELAY"
scaler_value = 2          # Target 2s queue delay

[env]
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
MAX_MODEL_LEN = "8192"
GPU_MEMORY_UTILIZATION = "0.95"
TENSOR_PARALLEL_SIZE = "1"
# HF_TOKEN injected from secrets

[build]
include = ["handler.py", "requirements.txt", "src/", "configs/"]

[secrets]
HF_TOKEN = "env:HF_TOKEN"
```

### Multi-GPU Configuration

```toml
# runpod.toml - Multi-GPU for large models

[project]
name = "70b-inference"
base_image = "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04"
gpu_types = ["NVIDIA A100 80GB PCIe"]
gpu_count = 2             # Two A100s for 70B model

[deploy]
workers_min = 0
workers_max = 2
idle_timeout = 300        # Longer timeout for expensive setup

[env]
MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct"
TENSOR_PARALLEL_SIZE = "2"
MAX_MODEL_LEN = "16384"
GPU_MEMORY_UTILIZATION = "0.95"
QUANTIZATION = "awq"

[build]
include = ["handler.py", "requirements.txt"]
```

### Cost-Optimized Configuration

```toml
# runpod.toml - Cost-optimized deployment

[project]
name = "budget-inference"
base_image = "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04"
gpu_types = ["NVIDIA RTX A4000", "NVIDIA RTX A5000", "NVIDIA GeForce RTX 4090"]
gpu_count = 1

[deploy]
workers_min = 0           # Scale to zero
workers_max = 3
idle_timeout = 15         # Aggressive scale-down
scaler_type = "QUEUE_DELAY"
scaler_value = 5          # Allow some queue delay for cost savings

[env]
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
QUANTIZATION = "awq"      # Quantize for smaller GPU
MAX_MODEL_LEN = "4096"

[build]
include = ["handler.py", "requirements.txt"]
```

---

## requirements.txt Templates

### Basic LLM Inference

```
# requirements.txt - Basic LLM
runpod>=1.6.0
torch>=2.1.0
transformers>=4.36.0
accelerate>=0.25.0
safetensors>=0.4.0
sentencepiece>=0.1.99
```

### vLLM Deployment

```
# requirements.txt - vLLM
runpod>=1.6.0
vllm>=0.4.0
ray>=2.9.0
transformers>=4.36.0
accelerate>=0.25.0
```

### Embeddings

```
# requirements.txt - Embeddings
runpod>=1.6.0
torch>=2.1.0
sentence-transformers>=2.3.0
transformers>=4.36.0
numpy>=1.24.0
```

### Vision Models

```
# requirements.txt - Vision
runpod>=1.6.0
torch>=2.1.0
transformers>=4.36.0
accelerate>=0.25.0
Pillow>=10.0.0
timm>=0.9.0
```

### Audio/Voice

```
# requirements.txt - Audio
runpod>=1.6.0
torch>=2.1.0
transformers>=4.36.0
TTS>=0.21.0
soundfile>=0.12.0
numpy>=1.24.0
```

### Full Stack (Kitchen Sink)

```
# requirements.txt - Full stack
runpod>=1.6.0
torch>=2.1.0
transformers>=4.36.0
accelerate>=0.25.0
vllm>=0.4.0
sentence-transformers>=2.3.0
safetensors>=0.4.0
pydantic>=2.0.0
aiohttp>=3.9.0
numpy>=1.24.0
```

---

## GitHub Actions Workflow

### Complete CI/CD Template

```yaml
# .github/workflows/deploy-runpod.yml
name: Deploy to RunPod

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=raw,value=latest

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64
          build-args: |
            HF_TOKEN=${{ secrets.HF_TOKEN }}

      - name: Install runpodctl
        run: |
          wget -qO- https://github.com/runpod/runpodctl/releases/latest/download/runpodctl-linux-amd64 -O runpodctl
          chmod +x runpodctl
          sudo mv runpodctl /usr/local/bin/

      - name: Deploy to RunPod
        env:
          RUNPOD_API_KEY: ${{ secrets.RUNPOD_API_KEY }}
        run: |
          runpodctl project deploy \
            --name ${{ github.event.repository.name }} \
            --image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

      - name: Notify deployment
        if: success()
        run: |
          echo "Deployment successful!"
          echo "Image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest"
```

### Simplified Workflow (No Docker Build)

```yaml
# .github/workflows/deploy-simple.yml
name: Deploy to RunPod (Simple)

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install runpodctl
        run: |
          wget -qO- https://github.com/runpod/runpodctl/releases/latest/download/runpodctl-linux-amd64 -O runpodctl
          chmod +x runpodctl
          sudo mv runpodctl /usr/local/bin/

      - name: Deploy
        env:
          RUNPOD_API_KEY: ${{ secrets.RUNPOD_API_KEY }}
        run: |
          runpodctl project deploy \
            --name ${{ github.event.repository.name }} \
            --gpu-type "NVIDIA RTX A4000" \
            --min-workers 0 \
            --max-workers 3 \
            --idle-timeout 60
```

---

## Deploy Scripts

### Bash Deploy Script

```bash
#!/bin/bash
# deploy.sh - Deploy to RunPod

set -e

PROJECT_NAME=${1:-$(basename $(pwd))}
GPU_TYPE=${2:-"NVIDIA RTX A4000"}
MIN_WORKERS=${3:-0}
MAX_WORKERS=${4:-3}
IDLE_TIMEOUT=${5:-60}

echo "=== RunPod Deployment ==="
echo "Project: $PROJECT_NAME"
echo "GPU: $GPU_TYPE"
echo "Workers: $MIN_WORKERS - $MAX_WORKERS"
echo "Idle Timeout: ${IDLE_TIMEOUT}s"

# Check for API key
if [ -z "$RUNPOD_API_KEY" ]; then
    echo "Error: RUNPOD_API_KEY not set"
    exit 1
fi

# Deploy
runpodctl project deploy \
    --name "$PROJECT_NAME" \
    --gpu-type "$GPU_TYPE" \
    --min-workers $MIN_WORKERS \
    --max-workers $MAX_WORKERS \
    --idle-timeout $IDLE_TIMEOUT

echo "=== Deployment Complete ==="
```

### Python Deploy Script

```python
#!/usr/bin/env python3
"""deploy.py - Deploy to RunPod with validation."""

import os
import sys
import argparse
import runpod

def deploy(config: dict):
    """Deploy endpoint with configuration."""
    runpod.api_key = os.environ.get("RUNPOD_API_KEY")

    if not runpod.api_key:
        print("Error: RUNPOD_API_KEY not set")
        sys.exit(1)

    print(f"Deploying {config['name']}...")

    endpoint = runpod.Endpoint.create(
        name=config["name"],
        template_id=config.get("template_id"),
        gpu_type_ids=config["gpu_types"],
        workers_min=config.get("workers_min", 0),
        workers_max=config.get("workers_max", 3),
        idle_timeout=config.get("idle_timeout", 60),
        gpu_count=config.get("gpu_count", 1)
    )

    print(f"Endpoint created: {endpoint.id}")
    return endpoint


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--gpu-type", default="NVIDIA RTX A4000")
    parser.add_argument("--min-workers", type=int, default=0)
    parser.add_argument("--max-workers", type=int, default=3)
    parser.add_argument("--idle-timeout", type=int, default=60)

    args = parser.parse_args()

    config = {
        "name": args.name,
        "gpu_types": [args.gpu_type],
        "workers_min": args.min_workers,
        "workers_max": args.max_workers,
        "idle_timeout": args.idle_timeout
    }

    deploy(config)
```

---

## MCP Server Configuration

### Claude Desktop Integration

```json
{
  "mcpServers": {
    "runpod": {
      "command": "npx",
      "args": ["-y", "@runpod/mcp-server"],
      "env": {
        "RUNPOD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Example MCP Commands

```
# Natural language control via MCP
"Create a RunPod serverless endpoint for embeddings using RTX A4000"
"Deploy my vLLM endpoint with A100 and 8GB RAM"
"Scale the inference endpoint to handle 1000 requests per minute"
"Show me current GPU usage and costs"
"Stop all idle workers on my endpoints"
```

---

## Environment Templates

### Development

```bash
# .env.development
RUNPOD_API_KEY=your-dev-key
MODEL_NAME=Qwen/Qwen2.5-0.5B  # Small model for testing
MAX_TOKENS=512
GPU_TYPE=NVIDIA RTX A4000
LOG_LEVEL=DEBUG
```

### Production

```bash
# .env.production
RUNPOD_API_KEY=your-prod-key
MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
HF_TOKEN=hf_xxx
MAX_TOKENS=2048
GPU_MEMORY_UTILIZATION=0.95
MAX_MODEL_LEN=8192
LOG_LEVEL=INFO
```

### Testing

```bash
# .env.test
RUNPOD_API_KEY=your-test-key
MODEL_NAME=Qwen/Qwen2.5-0.5B
MAX_TOKENS=100
MOCK_INFERENCE=true
LOG_LEVEL=DEBUG
```
