---
name: runpod-deployment-skill
version: 1.0.0
description: |
  RunPod serverless and pod deployment patterns for GPU-accelerated AI workloads.
  Use when deploying ML models, setting up vLLM inference endpoints, configuring
  serverless GPU workers, or managing RunPod infrastructure. Triggers: "deploy to RunPod",
  "GPU serverless", "vLLM endpoint", "A100 deployment", "scale to zero", "RunPod worker".
  Note: M1 Mac requires GitHub Actions for Docker builds (no local build).
---

# RunPod Deployment Skill

GPU deployment patterns for AI/ML workloads.

## M1 Mac Deployment (IMPORTANT)

**Cannot build Docker images locally on M1** - ARM architecture incompatible with RunPod's x86 GPUs.

**Solution: GitHub Actions builds the image for you.**

```bash
# 1. Push code to GitHub (no local docker build)
git add . && git commit -m "Deploy to RunPod" && git push

# 2. GitHub Actions builds x86 image and deploys
# See reference/cicd.md for workflow
```

This is the standard workflow for M1 Macs - let CI/CD handle the build.

## Quick Reference

### GPU Selection Guide

| Use Case | GPU | VRAM | Cost/hr |
|----------|-----|------|---------|
| 3B-7B models | RTX A5000 | 24GB | ~$0.50 |
| 8B-13B models | RTX A6000 | 48GB | ~$0.80 |
| 30B+ models | A100 | 80GB | ~$2.50 |
| Fine-tuning | H100 | 80GB | ~$3.59 |
| Embeddings | RTX A4000 | 16GB | ~$0.35 |

### Serverless Pricing

- Per-second billing
- Scale to 0 when idle
- H200: $3.59/hour

## Deployment Pattern

```python
@dataclass
class DeploymentConfig:
    name: str
    gpu_type: str = "NVIDIA RTX A4000"
    gpu_count: int = 1
    container_disk_gb: int = 25
    min_workers: int = 0      # Scale to zero
    max_workers: int = 3
    idle_timeout: int = 30    # seconds
    environment_vars: dict = None
```

```python
class RunPodManager:
    async def deploy_serverless(self, config: DeploymentConfig):
        endpoint = await runpod.create_endpoint(
            name=config.name,
            gpu_ids=[config.gpu_type],
            workers_min=config.min_workers,
            workers_max=config.max_workers,
            idle_timeout=config.idle_timeout,
            env=config.environment_vars
        )
        return endpoint
```

## Cost Optimization

```python
def select_gpu_tier(task_complexity: int) -> str:
    if task_complexity <= 3:
        return "RTX_A4000"     # $0.35/hr - embeddings
    elif task_complexity <= 6:
        return "RTX_A6000"     # $0.80/hr - 8B-13B models
    else:
        return "A100_80GB"     # $2.50/hr - large models
```

**Scale-to-Zero Settings:**
| Use Case | idle_timeout |
|----------|-------------|
| Interactive | 60s |
| Batch processing | 30s |
| Training | 300s |

## Integration Notes

- **Pairs with:** trading-signals-skill (model serving)
- **Pairs with:** sales-outreach-skill (LLM agents)
- **Projects:** ThetaRoom, sales-agent, Unsloth

## Reference Files

- `reference/vllm-setup.md` - Environment vars, supported models, benchmarks
- `reference/project-configs.md` - ThetaRoom, sales-agent, Unsloth configs
- `reference/cicd.md` - GitHub Actions, deploy scripts, MCP integration
- `reference/troubleshooting.md` - Common issues, health checks
