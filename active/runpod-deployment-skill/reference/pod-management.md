# Pod Management - Complete Reference

Comprehensive guide to RunPod GPU types, pricing, and pod lifecycle management.

## GPU Types and Specifications

### Consumer GPUs

| GPU | VRAM | CUDA Cores | Tensor Cores | FP16 TFLOPS | Best For |
|-----|------|------------|--------------|-------------|----------|
| RTX 3090 | 24GB | 10496 | 328 | 35.6 | Budget inference |
| RTX 4080 | 16GB | 9728 | 304 | 48.7 | Small models |
| RTX 4090 | 24GB | 16384 | 512 | 82.6 | 7B-8B inference |

### Professional GPUs

| GPU | VRAM | CUDA Cores | Tensor Cores | FP16 TFLOPS | Best For |
|-----|------|------------|--------------|-------------|----------|
| RTX A4000 | 16GB | 6144 | 192 | 19.2 | Embeddings, small |
| RTX A5000 | 24GB | 8192 | 256 | 27.8 | 7B models |
| RTX A6000 | 48GB | 10752 | 336 | 38.7 | 13B-30B models |
| A40 | 48GB | 10752 | 336 | 37.4 | Training, inference |

### Data Center GPUs

| GPU | VRAM | Architecture | FP16 TFLOPS | Best For |
|-----|------|--------------|-------------|----------|
| A100 40GB | 40GB | Ampere | 312 | 30B production |
| A100 80GB | 80GB | Ampere | 312 | 70B models |
| H100 80GB | 80GB | Hopper | 989 | Training, 70B+ |
| H200 141GB | 141GB | Hopper | 989 | Largest models |

---

## Pricing (December 2024)

### Serverless Pricing (Per-Second Billing)

| GPU | On-Demand/hr | Spot/hr | Effective $/1M tokens* |
|-----|--------------|---------|------------------------|
| RTX 4090 | $0.44 | $0.18 | ~$0.003 |
| RTX A4000 | $0.36 | $0.14 | ~$0.002 |
| RTX A5000 | $0.47 | $0.19 | ~$0.003 |
| RTX A6000 | $0.79 | $0.32 | ~$0.005 |
| A100 40GB | $1.64 | $0.66 | ~$0.008 |
| A100 80GB | $1.89 | $0.76 | ~$0.010 |
| H100 80GB | $4.69 | $1.88 | ~$0.015 |
| H200 141GB | $5.99 | $2.40 | ~$0.020 |

*Estimated based on typical throughput for 7B model

### Pod Pricing (Hourly)

| GPU | On-Demand/hr | Spot/hr |
|-----|--------------|---------|
| RTX 4090 | $0.44 | $0.18 |
| A100 80GB | $1.89 | $0.76 |
| H100 80GB | $4.69 | $1.88 |
| H100 SXM5 | $5.49 | $2.20 |

---

## Spot vs On-Demand

### When to Use Spot Instances

**Good for Spot:**
- Training with checkpointing
- Batch processing
- Non-real-time inference
- Development/testing
- Any interruptible workload

**Not Good for Spot:**
- Production API endpoints
- Real-time inference
- User-facing applications
- Time-critical workloads

### Handling Spot Interruptions

```python
import signal
import sys

def graceful_shutdown(signum, frame):
    """Handle spot instance termination."""
    print("Received shutdown signal, saving checkpoint...")
    save_checkpoint()
    cleanup_resources()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
```

### Training with Spot Instances

```python
import os

class CheckpointManager:
    """Manage training checkpoints for spot instances."""

    def __init__(self, checkpoint_dir="/runpod-volume/checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save(self, model, optimizer, epoch, step):
        """Save checkpoint to persistent volume."""
        path = f"{self.checkpoint_dir}/checkpoint_{epoch}_{step}.pt"
        torch.save({
            'epoch': epoch,
            'step': step,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, path)
        print(f"Checkpoint saved: {path}")

    def load_latest(self):
        """Resume from latest checkpoint."""
        checkpoints = sorted(os.listdir(self.checkpoint_dir))
        if not checkpoints:
            return None
        latest = os.path.join(self.checkpoint_dir, checkpoints[-1])
        return torch.load(latest)
```

---

## Creating Pods

### Via Python SDK

```python
import runpod

runpod.api_key = os.environ["RUNPOD_API_KEY"]

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
print(f"Endpoint created: {endpoint.id}")

# Create on-demand GPU pod
pod = runpod.create_pod(
    name="training-pod",
    image_name="runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04",
    gpu_type_id="NVIDIA A100 80GB PCIe",
    gpu_count=2,
    volume_in_gb=100,
    container_disk_in_gb=50,
    env={
        "HF_TOKEN": os.environ["HF_TOKEN"],
        "WANDB_API_KEY": os.environ["WANDB_API_KEY"]
    }
)
print(f"Pod created: {pod['id']}")
```

### Via GraphQL API

```python
import requests

def create_pod_graphql(config: dict) -> dict:
    """Create pod using GraphQL for full control."""
    query = """
    mutation createPod($input: PodFindAndDeployOnDemandInput!) {
        podFindAndDeployOnDemand(input: $input) {
            id
            name
            imageName
            gpuCount
            volumeInGb
            containerDiskInGb
            ports
            env {
                key
                value
            }
        }
    }
    """

    variables = {
        "input": {
            "name": config["name"],
            "imageName": config["image"],
            "gpuTypeId": config["gpu_type"],
            "gpuCount": config.get("gpu_count", 1),
            "volumeInGb": config.get("volume_gb", 50),
            "containerDiskInGb": config.get("disk_gb", 25),
            "ports": config.get("ports", "8080/http"),
            "startSsh": config.get("ssh", True),
            "env": [
                {"key": k, "value": v}
                for k, v in config.get("env", {}).items()
            ]
        }
    }

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config['api_key']}"}
    )

    return response.json()["data"]["podFindAndDeployOnDemand"]


# Example usage
pod = create_pod_graphql({
    "api_key": os.environ["RUNPOD_API_KEY"],
    "name": "my-training-pod",
    "image": "runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04",
    "gpu_type": "NVIDIA A100 80GB PCIe",
    "gpu_count": 2,
    "volume_gb": 200,
    "disk_gb": 50,
    "env": {
        "HF_TOKEN": "your-token",
        "WANDB_API_KEY": "your-key"
    }
})
```

### Via CLI

```bash
# Create serverless endpoint
runpodctl project deploy \
    --name my-endpoint \
    --gpu-type "NVIDIA RTX A4000" \
    --min-workers 0 \
    --max-workers 5 \
    --idle-timeout 60

# Create GPU pod
runpodctl create pod \
    --name training-pod \
    --image runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel \
    --gpu-type "NVIDIA A100 80GB PCIe" \
    --gpu-count 2 \
    --volume-size 100 \
    --container-disk 50
```

---

## Pod Lifecycle Management

### Stopping and Starting Pods

```python
import runpod

# Stop pod (preserves data)
runpod.stop_pod(pod_id="your-pod-id")

# Start stopped pod
runpod.resume_pod(pod_id="your-pod-id")

# Terminate pod (destroys everything)
runpod.terminate_pod(pod_id="your-pod-id")
```

### GraphQL Pod Operations

```python
def stop_pod_graphql(api_key: str, pod_id: str):
    """Stop a running pod."""
    query = """
    mutation stopPod($input: PodStopInput!) {
        podStop(input: $input) {
            id
            desiredStatus
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={
            "query": query,
            "variables": {"input": {"podId": pod_id}}
        },
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()


def terminate_pod_graphql(api_key: str, pod_id: str):
    """Terminate and delete a pod."""
    query = """
    mutation terminatePod($input: PodTerminateInput!) {
        podTerminate(input: $input)
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={
            "query": query,
            "variables": {"input": {"podId": pod_id}}
        },
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()
```

---

## Network Volumes

### Creating Persistent Volumes

```python
def create_network_volume(api_key: str, name: str, size_gb: int, region: str = "US"):
    """Create a persistent network volume."""
    query = """
    mutation createNetworkVolume($input: CreateNetworkVolumeInput!) {
        createNetworkVolume(input: $input) {
            id
            name
            size
            dataCenterId
        }
    }
    """

    variables = {
        "input": {
            "name": name,
            "size": size_gb,
            "dataCenterId": region
        }
    }

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()
```

### Mounting Volumes

```python
# When creating pod, attach network volume
pod = runpod.create_pod(
    name="training-pod",
    image_name="runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel",
    gpu_type_id="NVIDIA A100 80GB PCIe",
    network_volume_id="your-volume-id",
    volume_mount_path="/workspace"  # Mounted at this path
)

# In handler, access at mount path
def handler(job):
    # Models and data persist here
    model_path = "/workspace/models/my-model"
    ...
```

---

## Multi-GPU Configuration

### Tensor Parallelism

For models too large for single GPU:

```python
# Environment for multi-GPU
env_vars = {
    "MODEL_NAME": "meta-llama/Llama-3.1-70B-Instruct",
    "TENSOR_PARALLEL_SIZE": "2",  # Split across 2 GPUs
    "MAX_MODEL_LEN": "16384"
}

# Create with multiple GPUs
endpoint = runpod.Endpoint.create(
    name="70b-inference",
    template_id="vllm-template",
    gpu_type_ids=["NVIDIA A100 80GB PCIe"],
    gpu_count=2,  # 2x A100 for 70B
    workers_min=0,
    workers_max=2
)
```

### Multi-GPU Training

```python
import torch.distributed as dist
import os

def setup_distributed():
    """Initialize distributed training."""
    rank = int(os.environ.get("RANK", 0))
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    local_rank = int(os.environ.get("LOCAL_RANK", 0))

    dist.init_process_group(
        backend="nccl",
        init_method="env://",
        world_size=world_size,
        rank=rank
    )

    torch.cuda.set_device(local_rank)

    return rank, world_size, local_rank
```

---

## Region Selection

### Available Regions

| Region | Code | Latency From |
|--------|------|--------------|
| US East | US-EAST | East Coast, Europe |
| US West | US-WEST | West Coast, Asia |
| EU | EU | Europe, Middle East |
| APAC | APAC | Asia Pacific |

### Selecting Region

```python
# Via GraphQL
def list_gpu_availability(api_key: str):
    """List available GPUs by region."""
    query = """
    query getGpuTypes {
        gpuTypes {
            id
            displayName
            memoryInGb
            secureCloud
            communityCloud
            lowestPrice {
                minimumBidPrice
                uninterruptablePrice
            }
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()["data"]["gpuTypes"]
```

---

## GPU Selection Guide

### By Model Size

```python
def select_gpu_for_model(
    model_size_b: float,
    quantization: str = None,
    multi_gpu: bool = False
) -> dict:
    """Select optimal GPU configuration for model size."""

    # Approximate VRAM requirements
    if quantization == "AWQ" or quantization == "GPTQ":
        vram_needed = model_size_b * 1.2  # 4-bit quantization
    elif quantization == "INT8":
        vram_needed = model_size_b * 1.5  # 8-bit quantization
    else:
        vram_needed = model_size_b * 2.2  # FP16

    # GPU selection based on VRAM
    if vram_needed <= 16:
        return {
            "gpu": "NVIDIA RTX A4000",
            "count": 1,
            "cost_hr": 0.36
        }
    elif vram_needed <= 24:
        return {
            "gpu": "NVIDIA GeForce RTX 4090",
            "count": 1,
            "cost_hr": 0.44
        }
    elif vram_needed <= 48:
        return {
            "gpu": "NVIDIA RTX A6000",
            "count": 1,
            "cost_hr": 0.79
        }
    elif vram_needed <= 80:
        return {
            "gpu": "NVIDIA A100 80GB PCIe",
            "count": 1,
            "cost_hr": 1.89
        }
    elif vram_needed <= 160:
        return {
            "gpu": "NVIDIA A100 80GB PCIe",
            "count": 2,
            "cost_hr": 3.78
        }
    else:
        return {
            "gpu": "NVIDIA H100 80GB HBM3",
            "count": 2,
            "cost_hr": 9.38
        }


# Examples
print(select_gpu_for_model(7))   # 7B model -> RTX 4090
print(select_gpu_for_model(13))  # 13B model -> A6000
print(select_gpu_for_model(70))  # 70B model -> A100 80GB
print(select_gpu_for_model(70, quantization="AWQ"))  # 70B quantized -> A100 80GB
```

### By Use Case

| Use Case | Recommended GPU | Reason |
|----------|-----------------|--------|
| Embeddings | RTX A4000 | Low VRAM, cost effective |
| 7B inference | RTX 4090 | Best perf/cost |
| 13B inference | RTX A6000 | 48GB VRAM |
| 30B inference | A100 40GB | Production grade |
| 70B inference | A100 80GB | Large VRAM |
| Fine-tuning 7B | RTX A6000 | Needs headroom |
| Fine-tuning 13B+ | A100 80GB | Large VRAM for gradients |
| Training | H100 | Maximum performance |
