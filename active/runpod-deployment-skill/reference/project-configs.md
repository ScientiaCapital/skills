# Project-Specific Configs

## ThetaRoom (Trading Inference)

```python
THETAROOM_CONFIG = DeploymentConfig(
    name="thetaroom-inference",
    gpu_type="NVIDIA RTX A4000",
    gpu_count=1,
    container_disk_gb=25,
    min_workers=0,
    max_workers=2,
    idle_timeout=60,
    environment_vars={
        "MODEL_NAME": "all-MiniLM-L6-v2",
        "VECTOR_DIMENSIONS": "1536",
        "BATCH_SIZE": "100",
        "CACHE_TTL": "3600"
    }
)
```

**Use case:** Embeddings for trading signal vectorization

## Sales-Agent (Batch Processing)

```python
SALES_AGENT_CONFIG = DeploymentConfig(
    name="sales-agent-inference",
    gpu_type="NVIDIA RTX A4000",
    gpu_count=1,
    container_disk_gb=20,
    min_workers=0,
    max_workers=3,
    idle_timeout=30,
    environment_vars={
        "MODEL_NAME": "Qwen/Qwen2.5-7B-Instruct",
        "MAX_BATCH_SIZE": "10",
        "MAX_CONCURRENT": "3"
    }
)
```

**Use case:** Lead qualification, sequence generation

## Unsloth Fine-Tuning

```python
UNSLOTH_CONFIG = DeploymentConfig(
    name="unsloth-finetune",
    gpu_type="NVIDIA H100",  # or A100
    gpu_count=1,
    container_disk_gb=50,
    min_workers=0,
    max_workers=1,
    idle_timeout=300,  # Longer for training
    environment_vars={
        "UNSLOTH_VERSION": "2024.11",
        "TORCH_VERSION": "2.4.0",
        "CUDA_VERSION": "12.4"
    }
)
```

**Use case:** LoRA fine-tuning with 2x memory efficiency

## Config Template

```python
from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    name: str
    gpu_type: str = "NVIDIA RTX A4000"
    gpu_count: int = 1
    container_disk_gb: int = 25
    min_workers: int = 0
    max_workers: int = 3
    idle_timeout: int = 30  # seconds
    environment_vars: dict = None
```

## Scale-to-Zero Settings

| Project | idle_timeout | Reason |
|---------|-------------|--------|
| ThetaRoom | 60s | Interactive queries |
| Sales-Agent | 30s | Batch processing |
| Unsloth | 300s | Long training jobs |
