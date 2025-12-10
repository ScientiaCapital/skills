# vLLM Serverless Setup

## Environment Variables

```bash
# Required
MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
HF_TOKEN=hf_xxx  # For gated models

# Performance tuning
TENSOR_PARALLEL_SIZE=1      # Multi-GPU: set to GPU count
MAX_MODEL_LEN=8192
GPU_MEMORY_UTILIZATION=0.95

# Quantization (optional)
QUANTIZATION=AWQ  # or GPTQ

# Troubleshooting
ENFORCE_EAGER=true  # If CUDA errors occur
```

## Supported Models

- Llama 3/3.1/3.2
- Mistral/Mixtral
- Qwen/Qwen2
- Gemma/Gemma2
- Phi-4
- DeepSeek

## API Endpoints

```python
# RunPod Native API
POST https://api.runpod.ai/v2/{endpoint_id}/run
POST https://api.runpod.ai/v2/{endpoint_id}/runsync

# OpenAI-Compatible API
POST https://api.runpod.ai/v2/{endpoint_id}/openai/v1/chat/completions
```

## Client Code

```python
import runpod

runpod.api_key = os.environ["RUNPOD_API_KEY"]

# Async inference
response = runpod.run(
    endpoint_id="your-endpoint-id",
    input={
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 500,
        "temperature": 0.7
    }
)

# Sync inference (waits for result)
response = runpod.run_sync(
    endpoint_id="your-endpoint-id",
    input={"prompt": "Hello", "max_tokens": 100}
)
```

## Performance Benchmarks

| Model | GPU | Tokens/sec | Cost/1M tokens |
|-------|-----|------------|----------------|
| Qwen2-7B | A4000 | 25-35 | ~$0.003 |
| Llama-3-8B | A6000 | 30-45 | ~$0.004 |
| Mistral-7B | A4000 | 28-38 | ~$0.003 |
| Phi-4-mini | A4000 | 40-50 | ~$0.002 |

**Compare to API costs:**
- GPT-4: $30/1M tokens
- Claude: $15/1M tokens
- DeepSeek API: $0.14/1M tokens
- **Self-hosted: ~$0.003/1M tokens (200x savings)**
