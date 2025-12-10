# RunPod Troubleshooting

## Common Issues

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce MAX_MODEL_LEN, enable quantization |
| Model not loading | Check HF_TOKEN, verify model exists |
| Slow inference | Increase GPU_MEMORY_UTILIZATION to 0.95 |
| Worker timeout | Increase idle_timeout, check model size |
| Connection refused | Check endpoint status, wait for worker spin-up |
| Rate limited | Implement exponential backoff |

## Health Check

```python
async def health_check(endpoint_id: str) -> dict:
    response = await runpod.health(endpoint_id)
    return {
        "status": response.status,
        "workers_ready": response.workers.ready,
        "queue_depth": response.queue.depth,
        "avg_latency_ms": response.metrics.avg_latency
    }
```

## CUDA Memory Issues

**Symptoms:** `CUDA out of memory` errors

**Solutions:**
1. Reduce `MAX_MODEL_LEN` (e.g., 4096 instead of 8192)
2. Enable quantization: `QUANTIZATION=AWQ`
3. Use larger GPU (A6000 → A100)
4. Lower `GPU_MEMORY_UTILIZATION` (0.9 instead of 0.95)

## Model Loading Issues

**Symptoms:** Model fails to load, timeout on startup

**Checklist:**
1. Verify `HF_TOKEN` is set for gated models (Llama, etc.)
2. Check model name spelling exactly matches HuggingFace
3. Ensure container disk is large enough for model
4. Check RunPod dashboard for error logs

## Slow Inference

**Symptoms:** Requests taking 10+ seconds

**Checklist:**
1. Increase `GPU_MEMORY_UTILIZATION` to 0.95
2. Check if workers are scaled to 0 (cold start)
3. Increase `idle_timeout` to avoid constant restarts
4. Use quantized models (AWQ/GPTQ)
5. Check network latency to RunPod region

## Worker Management

### Cold Start
Workers at 0 take 30-60s to spin up. Options:
- Set `min_workers=1` for always-on (costs money)
- Implement client-side retry with backoff
- Pre-warm before expected usage

### Worker Stuck
```python
# Force restart via API
runpod.endpoint(endpoint_id).purge_queue()
```

## Cost Monitoring

```python
class CostController:
    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.spent_today = 0.0

    async def can_deploy(self, estimated_cost: float) -> bool:
        if self.spent_today + estimated_cost > self.daily_budget:
            return False
        return True
```

## Debugging Tips

1. **Check RunPod Dashboard** - Real-time logs and metrics
2. **Use `runsync`** - Easier to debug than async
3. **Start small** - Test with A4000 before A100
4. **Monitor costs** - Set budget alerts in RunPod
