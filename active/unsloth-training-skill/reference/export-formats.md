# Export Formats Guide

GGUF quantization, Ollama deployment, LM Studio, and Dynamic 2.0.

---

## GGUF Quantization Methods

### Quick Reference

| Method | Size | Quality | Use Case |
|--------|------|---------|----------|
| `q4_k_m` | ~4.5 bits | Good | **Default - best balance** |
| `q5_k_m` | ~5.5 bits | Better | Quality over size |
| `q8_0` | 8 bits | Excellent | Near full precision |
| `f16` | 16 bits | Perfect | Maximum quality |
| `q3_k_m` | ~3.5 bits | OK | Extreme compression |
| `q2_k` | ~2.5 bits | Fair | Minimum viable |

### Recommended by Use Case

| Use Case | Method | Reason |
|----------|--------|--------|
| Mobile deployment | `q4_k_m` | Size/quality balance |
| Desktop (8GB VRAM) | `q5_k_m` | Better quality fits |
| Desktop (16GB+ VRAM) | `q8_0` | Near-lossless |
| Ollama local | `q4_k_m` | Fast inference |
| API serving | `f16` or `q8_0` | Maximum quality |

### Save Locally

```python
# Single quantization
model.save_pretrained_gguf(
    "output_gguf",
    tokenizer,
    quantization_method="q4_k_m"
)

# Multiple quantizations
for method in ["q4_k_m", "q8_0"]:
    model.save_pretrained_gguf(
        f"output_{method}",
        tokenizer,
        quantization_method=method
    )
```

### Push to HuggingFace

```python
model.push_to_hub_gguf(
    "username/model-name-gguf",
    tokenizer,
    quantization_method="q4_k_m"
)
```

### Memory Control

```python
# Reduce GPU usage during export (if OOM)
model.save_pretrained_gguf(
    "output_gguf",
    tokenizer,
    quantization_method="q4_k_m",
    maximum_memory_usage=0.5  # Use 50% GPU (default 0.75)
)
```

---

## Ollama Export

### Automatic Export

```python
# Save GGUF
model.save_pretrained_gguf(
    "my_model_gguf",
    tokenizer,
    quantization_method="q4_k_m"
)

# Unsloth auto-generates Modelfile with correct chat template
```

### Modelfile Structure

```dockerfile
FROM ./my_model_gguf/unsloth.Q4_K_M.gguf

TEMPLATE """{{ .System }}
User: {{ .Prompt }}
Assistant: """

PARAMETER temperature 0.7
PARAMETER top_p 0.95
PARAMETER stop "<|im_end|>"
```

### Create and Run

```bash
# Create model in Ollama
ollama create my-model -f Modelfile

# Test inference
ollama run my-model "Hello, how are you?"

# Run as server
ollama serve  # Runs on localhost:11434
```

### Python Usage

```python
import ollama

response = ollama.chat(
    model='my-model',
    messages=[
        {'role': 'user', 'content': 'Explain GRPO in simple terms'}
    ]
)
print(response['message']['content'])
```

### Troubleshooting Ollama

| Issue | Cause | Fix |
|-------|-------|-----|
| Gibberish output | Wrong chat template | Use conversational notebook |
| Infinite loop | Missing EOS token | Check Modelfile PARAMETER stop |
| Poor quality | Wrong quantization | Try q8_0 instead of q4_k_m |

---

## LM Studio Export

### Export GGUF

```python
model.save_pretrained_gguf(
    "my_model_gguf",
    tokenizer,
    quantization_method="q4_k_m"
)
```

### Import Methods

**CLI Import:**
```bash
# Basic import
lms import /path/to/my_model_gguf/unsloth.Q4_K_M.gguf

# With copy (preserve original)
lms import --copy /path/to/model.gguf

# With symbolic link (for external drives)
lms import --symbolic-link /path/to/model.gguf
```

**From HuggingFace:**
```bash
# Via CLI
lms get username/my_model_gguf@Q4_K_M

# Or search in LM Studio Discover tab: "username/my_model_gguf"
```

**Manual Import:**
```
Place files in: ~/.lmstudio/models/publisher/model/model-file.gguf
```

### Configuration

1. Open LM Studio → Chat tab
2. Click model loader → Select imported model
3. Adjust GPU offload layers and context length
4. Configure prompt template to match training

### API Serving

```bash
# Start server
lms server start --port 1234

# Access OpenAI-compatible API
curl http://localhost:1234/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "my_model_gguf",
        "messages": [{"role": "user", "content": "Hello!"}]
    }'
```

### Troubleshooting LM Studio

| Issue | Fix |
|-------|-----|
| Gibberish/repeats | Adjust Prompt Template in settings |
| OOM errors | Reduce context length, use Q4_K_M |
| Slow inference | Increase GPU offload layers |

---

## Dynamic 2.0 GGUFs

### What is Dynamic 2.0?

Unsloth's advanced quantization that selectively quantizes layers based on model architecture:

- **Layer-specific optimization** - Different quantization per layer
- **Universal compatibility** - Works on MoE and non-MoE models
- **High-quality calibration** - 1.5M+ tokens of curated data

### Performance Comparison

| Model | Method | MMLU 5-shot | Size |
|-------|--------|-------------|------|
| Gemma 3 27B | Standard Q4 | 69.5% | 16GB |
| Gemma 3 27B | Dynamic 2.0 Q4 | 71.47% | 16GB |
| Gemma 3 27B | Google QAT | 70.64% | 18GB |

### Available Dynamic 2.0 Models

```
unsloth/Llama-4-Scout-17B-Dynamic-2.0
unsloth/Gemma-3-27B-Dynamic-2.0
unsloth/Qwen3-32B-Dynamic-2.0
unsloth/DeepSeek-V3.1-Dynamic-2.0
```

### Using Dynamic 2.0

Dynamic 2.0 GGUFs are pre-quantized by Unsloth:

```bash
# Download from HuggingFace
huggingface-cli download unsloth/Gemma-3-27B-Dynamic-2.0 \
    --include "*.gguf" \
    --local-dir gemma3-dynamic

# Use with Ollama
ollama create gemma3-dynamic -f Modelfile
```

### KL Divergence Improvement

Dynamic 2.0 reduces KL divergence by ~7.5% compared to standard imatrix quantization, meaning outputs more closely match the original model.
