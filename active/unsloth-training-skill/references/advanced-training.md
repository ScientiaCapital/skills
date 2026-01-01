# Advanced Training Techniques

500K context, packing, checkpointing, and continued pretraining.

---

## 3x Faster Training with Packing

### What is Packing?

Packing combines multiple shorter sequences into a single tensor, eliminating padding waste. Traditional batching pads all sequences to match the longest, wasting compute on padding tokens.

```
Traditional (50% waste):
[Token Token Token PAD PAD PAD PAD PAD]
[Token Token Token Token Token PAD PAD PAD]

Packed (95%+ utilization):
[Token Token Token | Token Token Token Token Token]
```

### Performance Gains

| Dataset Distribution | Speedup |
|---------------------|---------|
| 50% short, 50% long | 2x |
| 80% short, 20% long | 5x |
| Mixed conversation | 2-3x |

### Enable Packing

**Automatic (Default):**
```bash
# Just update Unsloth - padding-free mode is automatic
pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth
```

**Explicit Packing:**
```python
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        per_device_train_batch_size=1,
        max_length=4096,
        packing=True,  # Enable explicit packing
    ),
)
trainer.train()
```

### Key Points

- Works with all attention backends (Flash Attention 3, xFormers, SDPA)
- Compatible with full fine-tuning, LoRA, pretraining, and RL
- Dataset row count shrinks as sequences combine
- Use `packing=False` for identical loss curves to unpacked

---

## 500K Context Length Training

Train on ultra-long sequences with three key technologies.

### 1. Fused & Chunked Cross-Entropy Loss

Processes logits in chunks instead of computing entire sequences at once:

```python
# Enable automatically in Unsloth
# Results: 60% lower VRAM, 3.2x longer contexts
```

### 2. Enhanced Gradient Checkpointing

Activation offloading with only 0.1% training overhead:

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    use_gradient_checkpointing="unsloth",  # Enable offloading
)
```

### 3. Tiled MLP

For maximum context on limited VRAM:

```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B",
    max_seq_length=500000,
    unsloth_tiled_mlp=True,  # Enable tiled MLP
)
```

### Context Length by Hardware

| GPU | Standard | With Tiled MLP |
|-----|----------|----------------|
| A100 40GB | 80K | 290K |
| H100 80GB | 160K | 500K+ |
| B200 192GB | 400K | 750K+ |

### Trade-offs

- Tiled MLP adds ~1.3x step time
- Use only when you need >100K context
- Memory savings outweigh speed cost for long sequences

---

## Checkpoint Resumption

Save and resume training progress.

### Enable Checkpointing

```python
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="checkpoints",
        save_strategy="steps",
        save_steps=100,           # Save every 100 steps
        save_total_limit=3,       # Keep last 3 checkpoints
    ),
)
trainer.train()
```

### Resume Training

```python
# Resume from latest checkpoint
trainer.train(resume_from_checkpoint=True)

# Resume from specific checkpoint
trainer.train(resume_from_checkpoint="checkpoints/checkpoint-500")
```

### With Weights & Biases

```python
import wandb

# Login
wandb.login(key="your_key")

# Initialize run
run = wandb.init(project="unsloth-training")

# Resume from W&B artifact
artifact = run.use_artifact('username/project/run-id:latest', type='model')
artifact_dir = artifact.download()
trainer.train(resume_from_checkpoint=artifact_dir)
```

### Early Stopping

```python
from transformers import EarlyStoppingCallback

trainer = SFTTrainer(
    model=model,
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=3,      # Stop after 3 non-improving evals
            early_stopping_threshold=0.01,  # Minimum improvement
        )
    ],
)
```

---

## Continued Pretraining

Teach models new domains or languages.

### When to Use

| Scenario | Use Continued Pretraining? |
|----------|---------------------------|
| New language (e.g., Turkish) | Yes |
| Domain knowledge (law, medicine) | Yes |
| Better instruction following | No (use SFT) |
| Reasoning improvement | No (use GRPO) |

### Basic Setup

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.1-8B",  # Base model, not Instruct
    max_seq_length=4096,
)

# Use text completion format
trainer = SFTTrainer(
    model=model,
    train_dataset=raw_text_dataset,  # Plain text, not conversations
    args=SFTConfig(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=1e-5,
        num_train_epochs=1,
        packing=True,  # Essential for efficiency
    ),
)
trainer.train()
```

### Fine-tuning Embeddings

For best results, also train embedding layers:

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
        "lm_head",        # Output layer
        "embed_tokens",   # Input embeddings
    ],
    use_gradient_checkpointing="unsloth",
)
```

### Differentiated Learning Rates

```python
# Embedding layers should train slower
embedding_learning_rate = 5e-6   # 2-10x smaller than base
base_learning_rate = 5e-5
```

### Data Format

For continued pretraining, use raw text:

```python
dataset = [
    {"text": "Long domain document 1..."},
    {"text": "Long domain document 2..."},
    # ...
]
```
