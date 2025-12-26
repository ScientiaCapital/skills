# Cost Optimization - Complete Guide

Strategies for minimizing GPU costs while maintaining performance.

## Core Optimization Strategies

### 1. Scale-to-Zero

The most impactful cost saving: pay only for actual compute.

```python
# Aggressive scale-to-zero configuration
endpoint_config = {
    "workers_min": 0,          # No idle workers
    "workers_max": 5,          # Can scale up for bursts
    "idle_timeout": 15,        # Scale down quickly after idle
    "scaler_type": "QUEUE_DELAY",
    "scaler_value": 3          # Allow 3s queue delay
}
```

**Trade-offs:**
| Config | Cold Start | Cost | Best For |
|--------|------------|------|----------|
| workers_min=0, idle_timeout=15 | 30-60s | Lowest | Occasional use |
| workers_min=0, idle_timeout=60 | 30-60s | Low | Bursty traffic |
| workers_min=1, idle_timeout=60 | 0s | Medium | Production APIs |
| workers_min=2+ | 0s | Higher | High traffic |

### 2. GPU Right-Sizing

Don't overprovision - use the smallest GPU that meets requirements.

```python
def estimate_gpu_requirement(model_size_b: float, quantized: bool = False) -> str:
    """Select minimum GPU for model."""
    # VRAM estimation
    if quantized:
        vram_needed = model_size_b * 1.2  # 4-bit
    else:
        vram_needed = model_size_b * 2.2  # FP16

    if vram_needed <= 14:
        return "RTX_A4000"    # 16GB, $0.36/hr
    elif vram_needed <= 22:
        return "RTX_4090"     # 24GB, $0.44/hr
    elif vram_needed <= 44:
        return "RTX_A6000"    # 48GB, $0.79/hr
    elif vram_needed <= 76:
        return "A100_80GB"    # 80GB, $1.89/hr
    else:
        return "H100_80GB"    # 80GB, $4.69/hr


# Example: 7B model
# Unquantized: 7 * 2.2 = 15.4GB -> RTX 4090 ($0.44/hr)
# Quantized: 7 * 1.2 = 8.4GB -> RTX A4000 ($0.36/hr)
# Savings: 18% just from quantization + right-sizing
```

### 3. Quantization

Reduce model size to use cheaper GPUs.

```python
# 4-bit quantization reduces VRAM by ~60%
env_vars = {
    "MODEL_NAME": "meta-llama/Llama-3.1-70B-Instruct",
    "QUANTIZATION": "AWQ",
    "GPU_MEMORY_UTILIZATION": 0.95
}

# Cost comparison for 70B model:
# - FP16 on 2x A100 80GB: $3.78/hr
# - AWQ on 1x A100 80GB:  $1.89/hr
# - AWQ on 2x RTX A6000:  $1.58/hr (if fits)
# Savings: 50-58%
```

### 4. Batch Processing

Maximize GPU utilization with batching.

```python
def batch_inference_handler(job):
    """Process multiple requests in single GPU pass."""
    job_input = job["input"]
    requests = job_input.get("requests", [])

    # Optimal batch size depends on model and VRAM
    batch_size = min(len(requests), 8)

    results = []
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]

        # Single batched forward pass
        batch_results = model.generate_batch(batch)
        results.extend(batch_results)

    return {"results": results}

# Client-side batching
def batch_requests(requests: list, batch_size: int = 10):
    """Collect requests and send as batch."""
    batched_response = endpoint.run_sync({
        "requests": requests
    })
    return batched_response["results"]
```

---

## Cost Calculation

### Estimate Monthly Costs

```python
class CostEstimator:
    """Estimate RunPod costs based on usage patterns."""

    GPU_RATES = {
        "RTX_4090": 0.44,
        "RTX_A4000": 0.36,
        "RTX_A5000": 0.47,
        "RTX_A6000": 0.79,
        "A100_40GB": 1.64,
        "A100_80GB": 1.89,
        "H100_80GB": 4.69,
    }

    def estimate_serverless_cost(
        self,
        gpu_type: str,
        daily_requests: int,
        avg_processing_time_s: float,
        cold_start_frequency: str = "hourly"  # hourly, daily, rarely
    ) -> dict:
        """Estimate monthly serverless costs."""

        hourly_rate = self.GPU_RATES.get(gpu_type, 1.0)

        # Compute time
        daily_compute_s = daily_requests * avg_processing_time_s
        daily_compute_hours = daily_compute_s / 3600
        monthly_compute_hours = daily_compute_hours * 30

        # Cold start overhead
        cold_start_s = 45  # Average cold start time
        cold_starts_per_day = {
            "hourly": 24,
            "daily": 1,
            "rarely": 0.1
        }[cold_start_frequency]

        daily_cold_start_hours = (cold_starts_per_day * cold_start_s) / 3600
        monthly_cold_start_hours = daily_cold_start_hours * 30

        total_hours = monthly_compute_hours + monthly_cold_start_hours
        total_cost = total_hours * hourly_rate

        return {
            "gpu_type": gpu_type,
            "hourly_rate": hourly_rate,
            "monthly_compute_hours": round(monthly_compute_hours, 2),
            "monthly_cold_start_hours": round(monthly_cold_start_hours, 2),
            "total_hours": round(total_hours, 2),
            "monthly_cost": round(total_cost, 2)
        }


# Example calculations
estimator = CostEstimator()

# Light usage: 100 requests/day, 5s each, hourly cold starts
light = estimator.estimate_serverless_cost(
    "RTX_4090", 100, 5.0, "hourly"
)
# ~$12/month

# Medium usage: 1000 requests/day, 3s each, rare cold starts
medium = estimator.estimate_serverless_cost(
    "RTX_4090", 1000, 3.0, "rarely"
)
# ~$11/month

# Heavy usage: 10000 requests/day, 2s each
heavy = estimator.estimate_serverless_cost(
    "RTX_4090", 10000, 2.0, "rarely"
)
# ~$73/month
```

### Compare Self-Hosted vs API

```python
def compare_costs(
    monthly_requests: int,
    avg_tokens_per_request: int,
    self_hosted_config: dict
) -> dict:
    """Compare self-hosted RunPod vs commercial API costs."""

    # Commercial API costs (per 1M tokens)
    api_costs = {
        "gpt-4": 30.00,
        "gpt-4-turbo": 10.00,
        "claude-3-opus": 15.00,
        "claude-3-sonnet": 3.00,
        "deepseek-api": 0.14,
    }

    # Calculate API cost
    total_tokens = monthly_requests * avg_tokens_per_request
    millions_of_tokens = total_tokens / 1_000_000

    api_monthly = {
        name: millions_of_tokens * cost
        for name, cost in api_costs.items()
    }

    # Self-hosted cost (from config)
    self_hosted_monthly = self_hosted_config["monthly_cost"]
    self_hosted_per_m_tokens = self_hosted_monthly / millions_of_tokens if millions_of_tokens > 0 else 0

    return {
        "total_tokens": total_tokens,
        "self_hosted": {
            "monthly_cost": self_hosted_monthly,
            "per_m_tokens": round(self_hosted_per_m_tokens, 4)
        },
        "api_costs": {
            name: {"monthly": round(cost, 2)}
            for name, cost in api_monthly.items()
        },
        "savings_vs_gpt4": round(api_monthly["gpt-4"] - self_hosted_monthly, 2),
        "savings_percent_vs_gpt4": round((1 - self_hosted_monthly / api_monthly["gpt-4"]) * 100, 1) if api_monthly["gpt-4"] > 0 else 0
    }


# Example: 100k requests/month, 500 tokens each
comparison = compare_costs(
    100_000,
    500,
    {"monthly_cost": 50}  # $50/month on RunPod
)
# Self-hosted: $50/month, ~$1/M tokens
# GPT-4: $1,500/month
# Savings: $1,450/month (97%)
```

---

## Budget Controls

### Real-Time Cost Tracking

```python
import asyncio
from datetime import datetime, timedelta

class CostController:
    """Real-time cost monitoring and enforcement."""

    def __init__(
        self,
        daily_budget: float = 50.0,
        alert_threshold: float = 0.8,
        gpu_rate: float = 0.44
    ):
        self.daily_budget = daily_budget
        self.alert_threshold = alert_threshold
        self.gpu_rate = gpu_rate
        self.spent_today = 0.0
        self.day_start = datetime.now().date()

    def _reset_if_new_day(self):
        """Reset counter on new day."""
        today = datetime.now().date()
        if today > self.day_start:
            self.spent_today = 0.0
            self.day_start = today

    async def track_job(self, duration_s: float) -> dict:
        """Track job cost and enforce budget."""
        self._reset_if_new_day()

        job_cost = (duration_s / 3600) * self.gpu_rate
        self.spent_today += job_cost

        result = {
            "job_cost": round(job_cost, 6),
            "daily_spent": round(self.spent_today, 4),
            "daily_remaining": round(self.daily_budget - self.spent_today, 4),
            "budget_used_percent": round(self.spent_today / self.daily_budget * 100, 1)
        }

        # Alert at threshold
        if self.spent_today >= self.daily_budget * self.alert_threshold:
            result["alert"] = f"Approaching budget: ${self.spent_today:.2f} of ${self.daily_budget:.2f}"
            await self._send_alert(result["alert"])

        # Hard stop at budget
        if self.spent_today >= self.daily_budget:
            result["budget_exceeded"] = True
            await self._shutdown_workers()
            raise BudgetExceededError(f"Daily budget of ${self.daily_budget} exceeded")

        return result

    async def _send_alert(self, message: str):
        """Send alert (implement your notification method)."""
        print(f"ALERT: {message}")
        # Could send to Slack, email, etc.

    async def _shutdown_workers(self):
        """Scale workers to zero when budget exceeded."""
        print("Scaling to zero due to budget exceeded")
        # runpod.Endpoint(endpoint_id).update(workers_min=0, workers_max=0)


# Usage in handler
cost_controller = CostController(daily_budget=100.0, gpu_rate=0.44)

def handler(job):
    start = time.time()
    try:
        result = process(job["input"])
        return result
    finally:
        duration = time.time() - start
        asyncio.run(cost_controller.track_job(duration))
```

### Budget-Aware Deployment

```python
class BudgetAwareDeployment:
    """Deploy with automatic budget limits."""

    def __init__(self, monthly_budget: float):
        self.monthly_budget = monthly_budget
        self.daily_budget = monthly_budget / 30

    def get_safe_config(self, gpu_type: str) -> dict:
        """Calculate safe worker limits based on budget."""
        hourly_rate = CostEstimator.GPU_RATES.get(gpu_type, 1.0)

        # Max hours per day within budget
        max_hours_per_day = self.daily_budget / hourly_rate

        # Conservative: assume 50% utilization
        # Max workers = hours / (24 * utilization)
        max_workers = int(max_hours_per_day / (24 * 0.5))
        max_workers = max(1, min(max_workers, 10))  # Clamp 1-10

        return {
            "gpu_type": gpu_type,
            "workers_min": 0,
            "workers_max": max_workers,
            "idle_timeout": 30,
            "daily_budget": round(self.daily_budget, 2),
            "max_daily_hours": round(max_hours_per_day, 1)
        }


# Example: $100/month budget
budget_deploy = BudgetAwareDeployment(100)
config = budget_deploy.get_safe_config("RTX_4090")
# {
#   "gpu_type": "RTX_4090",
#   "workers_max": 3,
#   "daily_budget": 3.33,
#   "max_daily_hours": 7.6
# }
```

---

## Spot Instance Strategies

### When to Use Spot

```python
def should_use_spot(use_case: str) -> tuple[bool, str]:
    """Determine if spot instances are appropriate."""

    spot_friendly = {
        "training": (True, "Training can checkpoint and resume"),
        "batch_processing": (True, "Batch jobs are interruptible"),
        "development": (True, "Dev work doesn't need guaranteed uptime"),
        "fine_tuning": (True, "Fine-tuning should use checkpoints"),
        "embeddings_batch": (True, "Batch embeddings can be retried"),
    }

    spot_unfriendly = {
        "production_api": (False, "User-facing needs reliability"),
        "real_time_inference": (False, "Interruptions cause failures"),
        "streaming_response": (False, "Can't resume mid-stream"),
        "demo": (False, "Demos should be reliable"),
    }

    if use_case in spot_friendly:
        return spot_friendly[use_case]
    elif use_case in spot_unfriendly:
        return spot_unfriendly[use_case]
    else:
        return (True, "Default to spot for cost savings")


# Spot pricing comparison
spot_savings = {
    "RTX_4090": {"on_demand": 0.44, "spot": 0.18, "savings": "59%"},
    "A100_80GB": {"on_demand": 1.89, "spot": 0.76, "savings": "60%"},
    "H100_80GB": {"on_demand": 4.69, "spot": 1.88, "savings": "60%"},
}
```

### Spot with Fallback

```python
class SpotWithFallback:
    """Use spot instances with on-demand fallback."""

    def __init__(self, endpoint_id_spot: str, endpoint_id_ondemand: str):
        self.spot = runpod.Endpoint(endpoint_id_spot)
        self.ondemand = runpod.Endpoint(endpoint_id_ondemand)

    async def run(self, input_data: dict, timeout: int = 120):
        """Try spot first, fall back to on-demand."""
        try:
            # Try spot first (cheaper)
            result = await self.spot.run_sync(input_data, timeout=timeout)
            return {"result": result, "instance_type": "spot"}

        except (TimeoutError, SpotInterruptionError):
            # Fall back to on-demand
            result = await self.ondemand.run_sync(input_data, timeout=timeout)
            return {"result": result, "instance_type": "on_demand"}
```

---

## Optimization Checklist

### Immediate Wins

- [ ] Enable scale-to-zero (workers_min=0)
- [ ] Set aggressive idle_timeout (15-30s)
- [ ] Use quantization (AWQ/GPTQ) when acceptable
- [ ] Right-size GPU to model requirements
- [ ] Use spot instances for non-production

### Medium-Term Optimization

- [ ] Implement request batching
- [ ] Cache frequent embeddings
- [ ] Optimize model loading time
- [ ] Use network volumes for model caching
- [ ] Set up cost alerts

### Long-Term Cost Reduction

- [ ] Train smaller distilled models
- [ ] Implement request deduplication
- [ ] Use speculative decoding
- [ ] Consider reserved capacity for stable workloads
- [ ] Multi-tier routing (fast/slow based on need)

---

## Cost Optimization Patterns

### Request Caching

```python
import hashlib
import json
from functools import lru_cache

class CachedEndpoint:
    """Cache identical requests to reduce GPU calls."""

    def __init__(self, endpoint_id: str, cache_size: int = 1000):
        self.endpoint = runpod.Endpoint(endpoint_id)
        self._cache = {}
        self.cache_size = cache_size
        self.cache_hits = 0
        self.cache_misses = 0

    def _cache_key(self, input_data: dict) -> str:
        """Generate cache key from input."""
        serialized = json.dumps(input_data, sort_keys=True)
        return hashlib.md5(serialized.encode()).hexdigest()

    async def run(self, input_data: dict) -> dict:
        """Run with caching."""
        key = self._cache_key(input_data)

        if key in self._cache:
            self.cache_hits += 1
            return {"result": self._cache[key], "cached": True}

        self.cache_misses += 1
        result = await self.endpoint.run_sync(input_data)

        # Add to cache (evict oldest if full)
        if len(self._cache) >= self.cache_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = result

        return {"result": result, "cached": False}

    def stats(self) -> dict:
        """Cache statistics."""
        total = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total if total > 0 else 0
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": f"{hit_rate:.1%}",
            "estimated_savings": f"${self.cache_hits * 0.001:.2f}"  # Rough estimate
        }
```

### Multi-Tier Routing

```python
class MultiTierRouter:
    """Route requests to appropriate GPU tier."""

    def __init__(self):
        self.endpoints = {
            "small": runpod.Endpoint("small-endpoint-id"),   # RTX A4000
            "medium": runpod.Endpoint("medium-endpoint-id"), # RTX 4090
            "large": runpod.Endpoint("large-endpoint-id"),   # A100
        }

    def route(self, input_data: dict) -> str:
        """Determine appropriate tier based on request."""
        # Simple routing based on input size
        prompt_length = len(input_data.get("prompt", ""))
        max_tokens = input_data.get("max_tokens", 512)

        total_tokens = prompt_length / 4 + max_tokens  # Rough estimate

        if total_tokens < 1000:
            return "small"
        elif total_tokens < 4000:
            return "medium"
        else:
            return "large"

    async def run(self, input_data: dict) -> dict:
        """Route and run request."""
        tier = self.route(input_data)
        endpoint = self.endpoints[tier]
        result = await endpoint.run_sync(input_data)
        return {"result": result, "tier": tier}
```
