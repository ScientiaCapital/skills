# FP8 Reinforcement Learning

Ultra-efficient GRPO training using 8-bit floating point precision.

## Benefits

| Metric | Improvement |
|--------|-------------|
| RL inference speed | 1.4x faster via vLLM |
| VRAM usage | 60% less (~30GB savings for 32B) |
| Context length | 2x longer vs BF16/FP16 |
| GPU support | RTX 40/50 series, H100, H200, B200 |

## Installation

```bash
# Upgrade Unsloth with FP8 support
pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth unsloth_zoo

# Install FP8 dependencies (RTX 40+ / datacenter GPUs)
pip install --pre torchao fbgemm-gpu fbgemm-gpu-genai
```

## Basic FP8 Training

```python
import os
# CRITICAL: Enable shared memory between training and vLLM inference
os.environ['UNSLOTH_VLLM_STANDBY'] = "1"

from unsloth import FastLanguageModel
from trl import GRPOConfig, GRPOTrainer

# Load model in FP8
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B",
    max_seq_length=2048,
    load_in_fp8=True,       # Enable FP8 weights
    fast_inference=True,     # Enable vLLM backend
    max_lora_rank=64,
    gpu_memory_utilization=0.6,
)

# Configure LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=64,
    use_gradient_checkpointing="unsloth",
)

# Train with GRPO
trainer = GRPOTrainer(
    model=model,
    args=GRPOConfig(
        num_generations=4,
        beta=0.04,
        learning_rate=5e-6,
        max_completion_length=512,
    ),
    train_dataset=dataset,
    reward_funcs=[correctness_reward, format_reward],
)
trainer.train()
```

## Memory Architecture

FP8 training shares weights between training and vLLM inference:

```
┌─────────────────────────────────────────────────────┐
│                    GPU VRAM                          │
├─────────────────────────────────────────────────────┤
│  FP8 Weights (shared between training & inference)  │
├─────────────────────────────────────────────────────┤
│  LoRA Adapters                                       │
├─────────────────────────────────────────────────────┤
│  Optimizer States                                    │
├─────────────────────────────────────────────────────┤
│  Activations + Gradients                             │
└─────────────────────────────────────────────────────┘

With UNSLOTH_VLLM_STANDBY=1:
- No duplicate model copies
- 30%+ additional memory savings
- Single FP8 copy at any time
```

## FP8 Scaling Types

Three quantization granularities available:

| Type | Accuracy | Throughput | Use Case |
|------|----------|------------|----------|
| Block-wise | Best (62.37% MMLU Pro) | Balanced | Default recommendation |
| Per-Channel | Good | Highest (13,963 tok/s) | Maximum speed |
| Per-Tensor | Lower | Medium | Memory-constrained |

## Pre-Quantized FP8 Models

Ready-to-use FP8 models on HuggingFace:

```python
# Qwen3 Series
"unsloth/Qwen3-0.6B"
"unsloth/Qwen3-4B"
"unsloth/Qwen3-8B"
"unsloth/Qwen3-32B"

# Llama Series
"unsloth/Llama-3.1-8B-Instruct"
"unsloth/Llama-3.2-3B-Instruct"
"unsloth/Llama-3.3-70B-Instruct"

# Gemma Series
"unsloth/Gemma-3-4B"
"unsloth/Gemma-3-27B"
```

## VRAM Requirements (FP8 vs BF16)

| Model | BF16 VRAM | FP8 VRAM | Savings |
|-------|-----------|----------|---------|
| Qwen3-8B | 24GB | 10GB | 58% |
| Qwen3-32B | 80GB | 32GB | 60% |
| Llama-3.1-8B | 24GB | 10GB | 58% |
| Llama-3.3-70B | 160GB | 64GB | 60% |

## Troubleshooting

**"FP8 not supported" error:**
- Requires RTX 40xx/50xx or datacenter GPU (H100+)
- Install fbgemm-gpu-genai: `pip install --pre fbgemm-gpu-genai`

**OOM during training:**
- Reduce `gpu_memory_utilization` to 0.5
- Reduce `num_generations` to 2
- Enable `use_gradient_checkpointing="unsloth"`

**Poor training quality:**
- FP8 is for memory efficiency, not speed alone
- If quality degrades, try block-wise scaling (default)
- Compare final loss with BF16 baseline

## When to Use FP8

| Scenario | Use FP8? |
|----------|----------|
| Training 7B+ models on 24GB GPU | Yes |
| Need 2x context length | Yes |
| Memory-constrained cloud GPUs | Yes |
| Older GPUs (RTX 30xx) | No |
| Maximum training quality critical | Consider BF16 |
