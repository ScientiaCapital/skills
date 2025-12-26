# Monitoring & Health Checks - Complete Guide

Comprehensive monitoring, logging, and observability for RunPod deployments.

## Health Check Implementation

### Basic Health Check

```python
import runpod

async def check_endpoint_health(endpoint_id: str) -> dict:
    """Basic health check for RunPod endpoint."""
    endpoint = runpod.Endpoint(endpoint_id)

    try:
        health = await endpoint.health()

        return {
            "status": "healthy" if health.status == "READY" else "degraded",
            "workers_ready": health.workers.ready,
            "workers_running": health.workers.running,
            "queue_depth": health.queue.in_queue,
            "healthy": health.status == "READY"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "healthy": False
        }
```

### Comprehensive Health Check

```python
import runpod
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class HealthStatus:
    healthy: bool
    status: str
    workers_ready: int
    workers_running: int
    workers_pending: int
    workers_throttled: int
    queue_depth: int
    queue_in_progress: int
    avg_latency_ms: Optional[float]
    p95_latency_ms: Optional[float]
    success_rate: Optional[float]
    cold_start_time_ms: Optional[float]
    requests_per_minute: Optional[float]
    last_check: float

async def comprehensive_health_check(endpoint_id: str) -> HealthStatus:
    """Full health assessment with metrics."""
    endpoint = runpod.Endpoint(endpoint_id)

    try:
        health = await endpoint.health()

        return HealthStatus(
            healthy=health.status == "READY",
            status=health.status,
            workers_ready=health.workers.ready,
            workers_running=health.workers.running,
            workers_pending=health.workers.pending,
            workers_throttled=health.workers.throttled,
            queue_depth=health.queue.in_queue,
            queue_in_progress=health.queue.in_progress,
            avg_latency_ms=health.metrics.avg_execution_time,
            p95_latency_ms=health.metrics.p95_execution_time,
            success_rate=health.metrics.success_rate,
            cold_start_time_ms=health.metrics.avg_cold_start_time,
            requests_per_minute=health.metrics.requests_per_minute,
            last_check=time.time()
        )

    except Exception as e:
        return HealthStatus(
            healthy=False,
            status=f"ERROR: {str(e)}",
            workers_ready=0,
            workers_running=0,
            workers_pending=0,
            workers_throttled=0,
            queue_depth=0,
            queue_in_progress=0,
            avg_latency_ms=None,
            p95_latency_ms=None,
            success_rate=None,
            cold_start_time_ms=None,
            requests_per_minute=None,
            last_check=time.time()
        )
```

---

## GraphQL Monitoring

### Get Endpoint Metrics

```python
import requests
from typing import Optional

def get_endpoint_metrics_graphql(api_key: str, endpoint_id: str) -> dict:
    """Get detailed endpoint metrics via GraphQL."""
    query = """
    query getEndpoint($id: String!) {
        endpoint(id: $id) {
            id
            name
            status
            templateId
            workersMin
            workersMax
            idleTimeout
            gpuType
            createdAt
            updatedAt

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
                retried
            }

            metrics {
                requestsPerMinute
                requestsTotal
                avgExecutionTimeMs
                p50ExecutionTimeMs
                p95ExecutionTimeMs
                p99ExecutionTimeMs
                avgColdStartTimeMs
                successRate
                errorRate
            }
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": {"id": endpoint_id}},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL error: {data['errors']}")

    return data["data"]["endpoint"]


def get_all_endpoints(api_key: str) -> list:
    """List all endpoints with basic metrics."""
    query = """
    query getEndpoints {
        myself {
            serverlessDiscount
            endpoints {
                id
                name
                status
                workersMin
                workersMax
                workers {
                    ready
                    running
                }
                queue {
                    inQueue
                    inProgress
                }
            }
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()["data"]["myself"]["endpoints"]
```

### Get Pod Status

```python
def get_pod_status_graphql(api_key: str, pod_id: Optional[str] = None) -> dict:
    """Get status of pods."""
    if pod_id:
        query = """
        query getPod($id: String!) {
            pod(input: {podId: $id}) {
                id
                name
                runtime
                imageName
                gpuCount
                gpuType
                desiredStatus
                machineId
                uptimeSeconds
                costPerHr
                memoryInGb
                vcpuCount
            }
        }
        """
        variables = {"id": pod_id}
    else:
        query = """
        query getMyPods {
            myself {
                pods {
                    id
                    name
                    desiredStatus
                    gpuType
                    gpuCount
                    uptimeSeconds
                    costPerHr
                }
            }
        }
        """
        variables = {}

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()["data"]
```

### Get Usage and Billing

```python
def get_usage_graphql(api_key: str) -> dict:
    """Get account usage and billing info."""
    query = """
    query getUsage {
        myself {
            id
            email
            currentSpendPerHr
            clientBalance
            serverlessDiscount
            savingsPlans {
                planType
                startTime
                endTime
            }
        }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        json={"query": query},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()["data"]["myself"]
```

---

## Logging Best Practices

### Structured Logging

```python
import logging
import json
import sys
from datetime import datetime
from typing import Any

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields
        if hasattr(record, "job_id"):
            log_data["job_id"] = record.job_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging():
    """Configure structured logging."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger("runpod_worker")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


logger = setup_logging()
```

### Handler with Logging

```python
import runpod
import time
from datetime import datetime

logger = setup_logging()

def handler(job):
    """Handler with comprehensive logging."""
    job_id = job["id"]
    job_input = job["input"]
    start_time = time.time()

    # Log job start
    logger.info(
        "Job started",
        extra={
            "extra": {
                "job_id": job_id,
                "input_keys": list(job_input.keys()),
                "input_size_bytes": len(json.dumps(job_input))
            }
        }
    )

    try:
        # Processing
        result = process(job_input)

        # Log success
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "Job completed",
            extra={
                "extra": {
                    "job_id": job_id,
                    "duration_ms": round(duration_ms, 2),
                    "output_size_bytes": len(json.dumps(result))
                }
            }
        )

        return result

    except Exception as e:
        # Log failure
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            f"Job failed: {str(e)}",
            extra={
                "extra": {
                    "job_id": job_id,
                    "duration_ms": round(duration_ms, 2),
                    "error_type": type(e).__name__
                }
            },
            exc_info=True
        )
        raise

runpod.serverless.start({"handler": handler})
```

---

## Metrics Collection

### Custom Metrics Class

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
import statistics

@dataclass
class MetricsCollector:
    """Collect and aggregate metrics."""

    # Counters
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0

    # Latency tracking
    latencies_ms: List[float] = field(default_factory=list)

    # Token tracking
    total_tokens_in: int = 0
    total_tokens_out: int = 0

    # Timestamps
    start_time: datetime = field(default_factory=datetime.now)

    def record_request(
        self,
        success: bool,
        latency_ms: float,
        tokens_in: int = 0,
        tokens_out: int = 0
    ):
        """Record a request."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        self.latencies_ms.append(latency_ms)
        self.total_tokens_in += tokens_in
        self.total_tokens_out += tokens_out

    def get_stats(self) -> Dict:
        """Get aggregated statistics."""
        runtime_seconds = (datetime.now() - self.start_time).total_seconds()

        stats = {
            "runtime_seconds": round(runtime_seconds, 1),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.successful_requests / max(self.total_requests, 1) * 100, 2),
            "requests_per_minute": round(self.total_requests / max(runtime_seconds / 60, 1), 2),
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
        }

        if self.latencies_ms:
            sorted_latencies = sorted(self.latencies_ms)
            stats["latency"] = {
                "avg_ms": round(statistics.mean(self.latencies_ms), 2),
                "p50_ms": round(sorted_latencies[len(sorted_latencies) // 2], 2),
                "p95_ms": round(sorted_latencies[int(len(sorted_latencies) * 0.95)], 2),
                "p99_ms": round(sorted_latencies[int(len(sorted_latencies) * 0.99)], 2),
                "min_ms": round(min(self.latencies_ms), 2),
                "max_ms": round(max(self.latencies_ms), 2),
            }

        return stats


# Global metrics collector
metrics = MetricsCollector()

def handler(job):
    start = time.time()
    try:
        result = process(job["input"])

        latency_ms = (time.time() - start) * 1000
        metrics.record_request(
            success=True,
            latency_ms=latency_ms,
            tokens_in=result.get("tokens_in", 0),
            tokens_out=result.get("tokens_out", 0)
        )

        return result

    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        metrics.record_request(success=False, latency_ms=latency_ms)
        raise
```

---

## Alerting

### Threshold-Based Alerts

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Optional
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    severity: AlertSeverity
    message: str
    metric: str
    value: float
    threshold: float
    timestamp: float

class AlertManager:
    """Manage alerts based on metric thresholds."""

    def __init__(self, notification_callback: Optional[Callable] = None):
        self.thresholds = {
            "queue_depth": {"warning": 10, "critical": 50},
            "error_rate": {"warning": 0.05, "critical": 0.10},
            "latency_p95_ms": {"warning": 5000, "critical": 10000},
            "workers_throttled": {"warning": 1, "critical": 3},
        }
        self.notification_callback = notification_callback
        self.active_alerts = {}

    async def check_metrics(self, metrics: dict):
        """Check metrics against thresholds and generate alerts."""
        alerts = []

        for metric, value in metrics.items():
            if metric not in self.thresholds:
                continue

            thresholds = self.thresholds[metric]

            if value >= thresholds.get("critical", float("inf")):
                alert = Alert(
                    severity=AlertSeverity.CRITICAL,
                    message=f"{metric} is critical: {value}",
                    metric=metric,
                    value=value,
                    threshold=thresholds["critical"],
                    timestamp=time.time()
                )
                alerts.append(alert)

            elif value >= thresholds.get("warning", float("inf")):
                alert = Alert(
                    severity=AlertSeverity.WARNING,
                    message=f"{metric} is elevated: {value}",
                    metric=metric,
                    value=value,
                    threshold=thresholds["warning"],
                    timestamp=time.time()
                )
                alerts.append(alert)

        # Send notifications
        for alert in alerts:
            if self.notification_callback:
                await self.notification_callback(alert)
            self.active_alerts[alert.metric] = alert

        return alerts

    async def run_monitoring_loop(self, endpoint_id: str, interval_seconds: int = 60):
        """Continuous monitoring loop."""
        while True:
            try:
                health = await comprehensive_health_check(endpoint_id)

                metrics = {
                    "queue_depth": health.queue_depth,
                    "error_rate": 1 - (health.success_rate or 1),
                    "latency_p95_ms": health.p95_latency_ms or 0,
                    "workers_throttled": health.workers_throttled,
                }

                alerts = await self.check_metrics(metrics)

                if alerts:
                    for alert in alerts:
                        print(f"[{alert.severity.value.upper()}] {alert.message}")

            except Exception as e:
                print(f"Monitoring error: {e}")

            await asyncio.sleep(interval_seconds)
```

### Slack Notification

```python
import aiohttp

async def send_slack_alert(alert: Alert, webhook_url: str):
    """Send alert to Slack."""
    color = {
        AlertSeverity.INFO: "#36a64f",
        AlertSeverity.WARNING: "#ffcc00",
        AlertSeverity.CRITICAL: "#ff0000"
    }[alert.severity]

    payload = {
        "attachments": [{
            "color": color,
            "title": f"RunPod Alert: {alert.severity.value.upper()}",
            "text": alert.message,
            "fields": [
                {"title": "Metric", "value": alert.metric, "short": True},
                {"title": "Value", "value": str(alert.value), "short": True},
                {"title": "Threshold", "value": str(alert.threshold), "short": True},
            ],
            "ts": int(alert.timestamp)
        }]
    }

    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)
```

---

## Dashboard Data

### Metrics API Endpoint

```python
from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/metrics")
async def get_metrics():
    """Endpoint for monitoring dashboard."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "worker_metrics": metrics.get_stats(),
        "active_alerts": [
            {
                "severity": a.severity.value,
                "message": a.message,
                "metric": a.metric
            }
            for a in alert_manager.active_alerts.values()
        ]
    }

@app.get("/health")
async def health():
    """Health endpoint for load balancers."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def ready():
    """Readiness check."""
    # Check if model is loaded, dependencies available, etc.
    if model_loaded:
        return {"status": "ready"}
    return {"status": "not_ready"}, 503
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Define metrics
REQUEST_COUNT = Counter(
    'runpod_requests_total',
    'Total number of requests',
    ['status']
)

REQUEST_LATENCY = Histogram(
    'runpod_request_latency_seconds',
    'Request latency in seconds',
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

WORKERS_READY = Gauge(
    'runpod_workers_ready',
    'Number of ready workers'
)

QUEUE_DEPTH = Gauge(
    'runpod_queue_depth',
    'Number of requests in queue'
)

def handler(job):
    """Handler with Prometheus metrics."""
    with REQUEST_LATENCY.time():
        try:
            result = process(job["input"])
            REQUEST_COUNT.labels(status='success').inc()
            return result
        except Exception as e:
            REQUEST_COUNT.labels(status='error').inc()
            raise

@app.get("/metrics/prometheus")
async def prometheus_metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()
```

---

## Log Aggregation

### Viewing Logs

```bash
# Via CLI
runpodctl logs <endpoint_id>

# Via API
curl -H "Authorization: Bearer $RUNPOD_API_KEY" \
  "https://api.runpod.io/v2/<endpoint_id>/logs"
```

### Log Streaming

```python
import websocket
import json

def stream_logs(endpoint_id: str, api_key: str):
    """Stream logs in real-time."""
    ws_url = f"wss://api.runpod.io/v2/{endpoint_id}/logs/stream"

    def on_message(ws, message):
        log = json.loads(message)
        print(f"[{log['timestamp']}] {log['level']}: {log['message']}")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed")

    ws = websocket.WebSocketApp(
        ws_url,
        header={"Authorization": f"Bearer {api_key}"},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()
```

---

## Troubleshooting with Monitoring

### Common Issues Detection

```python
async def diagnose_endpoint(endpoint_id: str) -> dict:
    """Diagnose common endpoint issues."""
    health = await comprehensive_health_check(endpoint_id)

    issues = []
    recommendations = []

    # No workers ready
    if health.workers_ready == 0 and health.workers_running == 0:
        issues.append("No workers available")
        if health.workers_pending > 0:
            recommendations.append("Workers are starting - wait for cold start")
        else:
            recommendations.append("Check if endpoint is active and has available GPUs")

    # High queue depth
    if health.queue_depth > 10:
        issues.append(f"High queue depth: {health.queue_depth}")
        recommendations.append("Consider increasing workers_max")
        recommendations.append("Check if requests are taking too long")

    # Throttled workers
    if health.workers_throttled > 0:
        issues.append(f"Workers throttled: {health.workers_throttled}")
        recommendations.append("GPU availability may be limited")
        recommendations.append("Consider different GPU type or region")

    # High latency
    if health.p95_latency_ms and health.p95_latency_ms > 10000:
        issues.append(f"High P95 latency: {health.p95_latency_ms}ms")
        recommendations.append("Check model size vs GPU VRAM")
        recommendations.append("Consider quantization or smaller model")

    # Low success rate
    if health.success_rate and health.success_rate < 0.95:
        issues.append(f"Low success rate: {health.success_rate:.1%}")
        recommendations.append("Check handler error logs")
        recommendations.append("Validate input data")

    return {
        "status": "healthy" if not issues else "degraded",
        "health": health.__dict__,
        "issues": issues,
        "recommendations": recommendations
    }
```
