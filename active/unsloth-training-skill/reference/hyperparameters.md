# Hyperparameter Reference

## GRPOConfig Complete Reference

```python
GRPOConfig(
    # === CORE GRPO PARAMETERS ===

    num_generations = 4,
    # Number of completions generated per prompt (G in paper)
    # Higher = more stable but slower
    # Range: 2-16, typical: 4-8
    # MUST be >= 2 for GRPO to work

    beta = 0.04,
    # KL divergence penalty coefficient
    # Controls how much model can drift from reference
    # Higher = more constrained, Lower = more exploration
    # Range: 0.001-0.5, typical: 0.01-0.1
    # Start at 0.04, increase if unstable

    max_completion_length = 512,
    # Maximum tokens in generated response
    # Longer = more VRAM, potentially richer reasoning
    # Match to your task requirements

    max_prompt_length = 256,
    # Maximum tokens in input prompt
    # Trim prompts longer than this

    # === LEARNING PARAMETERS ===

    learning_rate = 5e-6,
    # Step size for gradient updates
    # RL needs smaller than SFT (1e-4)
    # Range: 1e-6 to 1e-5
    # Start conservative, increase if learning too slow

    lr_scheduler_type = "cosine",
    # How learning rate decays
    # Options: "constant", "linear", "cosine", "polynomial"
    # "cosine" is most common for RL

    warmup_ratio = 0.1,
    # Fraction of steps for LR warmup
    # Helps stability at start of training

    # === BATCH PARAMETERS ===

    per_device_train_batch_size = 1,
    # Samples per GPU per step
    # Keep low (1-2) for VRAM efficiency
    # Increase gradient_accumulation_steps instead

    gradient_accumulation_steps = 8,
    # Steps to accumulate before update
    # Effective batch = batch_size * accumulation * num_gpus
    # Higher = more stable but slower feedback

    # === CLIPPING PARAMETERS ===

    epsilon = 0.2,
    # PPO clip parameter for policy ratio
    # Prevents too-large policy updates
    # Typical range: 0.1-0.3

    delta = 1.5,
    # Two-sided clipping threshold
    # Enables upper clipping when set
    # Recommended: > 1 + epsilon

    # === LOSS VARIANTS ===

    loss_type = "grpo",
    # Algorithm variant to use:
    # "grpo"    - Original GRPO (default)
    # "dr_grpo" - Dr. GRPO, removes length bias
    # "dapo"    - DAPO, better for long responses
    # "gspo"    - GSPO (Qwen's sequence-level)

    scale_rewards = True,
    # Normalize rewards by std
    # False recommended for Dr. GRPO

    # === LOGGING ===

    logging_steps = 10,
    report_to = "none",  # or "wandb", "tensorboard"
)
```

## Hyperparameter Tuning Guide

### Learning Rate

| Symptom | Action |
|---------|--------|
| Reward not increasing | Increase LR (2x) |
| Reward spiky/unstable | Decrease LR (0.5x) |
| Reward plateaus early | Try cosine schedule |
| Model outputs garbage | Decrease LR significantly |

### Beta (KL Penalty)

| Symptom | Action |
|---------|--------|
| Model diverges/outputs nonsense | Increase beta (2x) |
| Model barely changes behavior | Decrease beta (0.5x) |
| Reward increases then crashes | Increase beta |
| Outputs too similar to base | Decrease beta carefully |

### Num Generations

| VRAM Available | Recommended G | Notes |
|----------------|---------------|-------|
| 8GB | 2 | Minimum viable |
| 16GB | 4 | Good balance |
| 24GB | 6-8 | Better estimates |
| 48GB+ | 8-16 | Research quality |

## Loss Type Selection

| Loss Type | Best For | Key Property |
|-----------|----------|--------------|
| `grpo` | General use | Original algorithm |
| `dr_grpo` | Long outputs | Removes length bias |
| `dapo` | Stable training | Token-level normalization |
| `gspo` | Sequence tasks | Sequence-level importance |

### Dr. GRPO Configuration

```python
GRPOConfig(
    loss_type = "dr_grpo",
    scale_rewards = False,  # Recommended with dr_grpo
)
```

### GSPO Configuration (Qwen-style)

```python
GRPOConfig(
    loss_type = "dr_grpo",
    importance_sampling_level = "sequence",
)
```

## VRAM Optimization

```python
# Maximum memory efficiency
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "...",
    load_in_4bit = True,                    # QLoRA
    fast_inference = True,
    gpu_memory_utilization = 0.5,           # Conservative
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 32,                                 # Lower rank
    use_gradient_checkpointing = "unsloth", # Key for memory
)

training_args = GRPOConfig(
    per_device_train_batch_size = 1,
    gradient_accumulation_steps = 16,       # High accumulation
    num_generations = 2,                    # Minimum G
    max_completion_length = 256,            # Shorter responses
)
```

## SFT Training Parameters

```python
TrainingArguments(
    output_dir = "sft_output",
    per_device_train_batch_size = 2,
    gradient_accumulation_steps = 4,
    num_train_epochs = 3,             # 2-4 epochs typical
    learning_rate = 2e-4,             # Standard for SFT
    warmup_steps = 10,
    logging_steps = 10,
    save_steps = 100,
)
```

## LoRA Configuration

| Rank | Use Case | Training Time |
|------|----------|---------------|
| 16 | Simple format learning, SFT | Fast |
| 32 | Moderate behavior change | Moderate |
| 64 | Complex reasoning (GRPO recommended) | Standard |
| 128 | Maximum adaptation capacity | Slow |

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 64,                       # LoRA rank
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj",      # MLP
    ],
    lora_alpha = 64,              # MUST equal r for balanced scaling
    lora_dropout = 0,             # MUST be 0 for GRPO (Unsloth requirement)
    bias = "none",
    use_gradient_checkpointing = "unsloth",  # 60% less VRAM
)
```
