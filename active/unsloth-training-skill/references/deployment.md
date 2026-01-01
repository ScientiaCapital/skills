# Deployment Guide

Docker setup, vLLM serving, LoRA hot-swapping, and SGLang integration.

---

## Docker Fine-tuning

### Official Image

```bash
# Pull official Unsloth image
docker pull unsloth/unsloth

# Run with GPU support
docker run -d \
  -e JUPYTER_PASSWORD="mypassword" \
  -p 8888:8888 \
  -p 2222:22 \
  -v $(pwd)/work:/workspace/work \
  --gpus all \
  unsloth/unsloth
```

Access Jupyter Lab at `http://localhost:8888`

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `JUPYTER_PASSWORD` | Lab access | `unsloth` |
| `JUPYTER_PORT` | Internal port | `8888` |
| `SSH_KEY` | Public key auth | None |
| `USER_PASSWORD` | Sudo password | `unsloth` |

### Advanced Configuration

```bash
docker run -d \
  -e JUPYTER_PORT=8000 \
  -e JUPYTER_PASSWORD="secure_password" \
  -e "SSH_KEY=$(cat ~/.ssh/id_rsa.pub)" \
  -e USER_PASSWORD="sudo_password" \
  -p 8000:8000 \
  -p 2222:22 \
  -v $(pwd)/work:/workspace/work \
  -v $(pwd)/models:/workspace/models \
  --gpus all \
  --shm-size 16g \
  unsloth/unsloth
```

### Container Directories

- `/workspace/work/` - Your mounted work directory
- `/workspace/unsloth-notebooks/` - Pre-built training examples
- `/home/unsloth/` - User home directory

---

## vLLM Engine Arguments

### Memory Management

```bash
vllm serve unsloth/Qwen3-8B \
    --gpu-memory-utilization 0.95 \    # Use 95% GPU memory (default 0.9)
    --max-model-len 32768 \             # Reduce to save memory
    --swap-space 8 \                    # CPU offload buffer (GB)
    --dtype bfloat16                    # Or auto, float16
```

### FP8 Quantization (50% Memory Reduction)

```bash
vllm serve unsloth/Llama-3.1-8B-Instruct \
    --quantization fp8 \                # Enable FP8 weights
    --kv-cache-dtype fp8 \              # FP8 KV cache
    --gpu-memory-utilization 0.95
```

### Multi-GPU (Tensor Parallelism)

```bash
# 2-GPU setup
vllm serve unsloth/Qwen3-32B \
    --tensor-parallel-size 2 \          # Split across 2 GPUs
    --gpu-memory-utilization 0.9

# 4-GPU with pipeline parallelism
vllm serve unsloth/Llama-3.3-70B-Instruct \
    --tensor-parallel-size 4 \
    --pipeline-parallel-size 1
```

### LoRA Serving

```bash
vllm serve unsloth/Llama-3.1-8B-Instruct \
    --enable-lora \                     # Enable LoRA adapters
    --max-loras 4 \                     # Up to 4 concurrent adapters
    --max-lora-rank 64 \                # Maximum LoRA rank
    --lora-modules adapter1=/path/to/lora1 adapter2=/path/to/lora2
```

### All Important Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--port` | API port | 8000 |
| `--api-key` | Auth password | None |
| `--seed` | Random seed | 0 |
| `--enforce-eager` | Disable compilation | False |
| `--disable-log-stats` | Suppress logs | False |
| `--tokenizer` | Custom tokenizer | Model default |
| `--hf-token` | HF authentication | None |

---

## LoRA Hot-Swapping

Load and swap LoRA adapters at runtime without server restart.

### Enable Hot-Swapping

```bash
# Set environment variable
export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True

# Start server with LoRA enabled
vllm serve unsloth/Llama-3.1-8B-Instruct \
    --quantization fp8 \
    --kv-cache-dtype fp8 \
    --gpu-memory-utilization 0.8 \
    --max-model-len 65536 \
    --enable-lora \
    --max-loras 4 \
    --max-lora-rank 64
```

### Load Adapter

```bash
curl -X POST http://localhost:8000/v1/load_lora_adapter \
    -H "Content-Type: application/json" \
    -d '{
        "lora_name": "sales_agent",
        "lora_path": "/workspace/adapters/sales_lora"
    }'
```

### Use Adapter in Request

```bash
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "sales_agent",
        "messages": [{"role": "user", "content": "Hello!"}]
    }'
```

### Unload Adapter

```bash
curl -X POST http://localhost:8000/v1/unload_lora_adapter \
    -H "Content-Type: application/json" \
    -d '{"lora_name": "sales_agent"}'
```

### After Unsloth Training

```python
# Save adapter after training
model.save_pretrained("trained_lora")
tokenizer.save_pretrained("trained_lora")

# Load into running vLLM server
# POST /v1/load_lora_adapter with path to trained_lora/
```

---

## SGLang Integration

Alternative to vLLM with competitive performance.

### Installation

```bash
# Install dependencies
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install uv && uv pip install "sglang" && uv pip install unsloth

# Or use Docker
docker run --gpus all --shm-size 32g lmsysorg/sglang:latest
```

### Deploy Model

```bash
# Start server
python3 -m sglang.launch_server \
    --model-path unsloth/Llama-3.2-1B-Instruct \
    --host 0.0.0.0 \
    --port 30000

# With FP8 quantization
python3 -m sglang.launch_server \
    --model-path unsloth/Qwen3-8B \
    --quantization fp8 \
    --kv-cache-dtype fp8_e4m3 \
    --host 0.0.0.0 \
    --port 30000
```

### Deploy Fine-tuned Model

```python
# After training, save merged model
model.save_pretrained_merged(
    "finetuned_model",
    tokenizer,
    save_method="merged_16bit"
)
```

```bash
# Serve with SGLang
python -m sglang.launch_server \
    --model-path finetuned_model \
    --host 0.0.0.0 \
    --port 30002
```

### API Access

SGLang provides OpenAI-compatible API:

```python
from openai import OpenAI  # OpenAI client format, NOT OpenAI server

client = OpenAI(base_url="http://localhost:30000/v1", api_key="none")
response = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Performance Comparison

| Server | gpt-oss-20b Output Tokens/s | First Token Latency |
|--------|----------------------------|---------------------|
| SGLang | ~2,562 | 0.40-0.42s |
| vLLM | ~2,400 | 0.45-0.50s |

### Troubleshooting

```bash
# Clear Flashinfer cache if errors occur
rm -rf ~/.cache/flashinfer
```
