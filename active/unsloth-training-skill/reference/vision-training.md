# Vision Fine-tuning (VLM)

Fine-tune vision-language models with Unsloth.

---

## Supported Models

| Model | Size | Use Case |
|-------|------|----------|
| Qwen3-VL 8B | 8B | General vision Q&A |
| Gemma 3 4B | 4B | Lightweight VLM |
| Llama 3.2 Vision | 11B | Medical imaging, documents |
| Qwen2.5-VL 7B | 7B | Handwriting, LaTeX |
| Pixtral 12B | 12B | General Q&A |

---

## Data Format

Vision datasets use conversation format with image content:

```python
dataset = [
    {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What do you see in this image?"},
                    {"type": "image", "image": image_bytes_or_path}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "I see a cat sitting on a windowsill."}
                ]
            }
        ]
    }
]
```

### From HuggingFace Dataset

```python
from datasets import load_dataset

# Load vision dataset
dataset = load_dataset("username/vision-dataset")

# Format for Unsloth
def format_vision(example):
    return {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": example["question"]},
                    {"type": "image", "image": example["image"]}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": example["answer"]}]
            }
        ]
    }

dataset = dataset.map(format_vision)
```

---

## Training Setup

```python
from unsloth import FastVisionModel
from trl import SFTTrainer, SFTConfig
from unsloth import UnslothVisionDataCollator

# Load vision model
model, tokenizer = FastVisionModel.from_pretrained(
    model_name="unsloth/Qwen2-VL-7B-Instruct",
    max_seq_length=4096,
    load_in_4bit=True,
)

# Configure LoRA for vision + language
model = FastVisionModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    finetune_vision_layers=True,      # Vision encoder
    finetune_language_layers=True,    # Language model
    finetune_attention_modules=True,  # Attention
    finetune_mlp_modules=True,        # MLP layers
)

# Data collator handles image preprocessing
data_collator = UnslothVisionDataCollator(
    tokenizer=tokenizer,
    max_seq_length=4096,
)

# Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    data_collator=data_collator,
    args=SFTConfig(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        num_train_epochs=3,
    ),
)
trainer.train()
```

---

## Layer Configuration

Control which layers to fine-tune:

```python
model = FastVisionModel.get_peft_model(
    model,
    r=16,

    # Vision encoder - expensive but important for domain shift
    finetune_vision_layers=True,

    # Language model - always recommended
    finetune_language_layers=True,

    # Attention - usually yes
    finetune_attention_modules=True,

    # MLP - can skip if memory-constrained
    finetune_mlp_modules=True,
)
```

### Configuration by Use Case

| Use Case | Vision | Language | Attention | MLP |
|----------|--------|----------|-----------|-----|
| New image domain | Yes | Yes | Yes | Yes |
| Same domain, new task | No | Yes | Yes | Yes |
| Quick adaptation | No | Yes | Yes | No |

---

## Image Preprocessing

The `UnslothVisionDataCollator` handles:

- Automatic resizing (300-1000px recommended)
- Patch size alignment
- Sequence length management

```python
data_collator = UnslothVisionDataCollator(
    tokenizer=tokenizer,
    max_seq_length=4096,
    # Images auto-resized for optimal training
)
```

### Image Size Recommendations

| Image Resolution | Training Speed | Memory |
|-----------------|----------------|--------|
| 300x300 | Fastest | Low |
| 512x512 | Balanced | Medium |
| 1024x1024 | Slower | High |

---

## Best Practices

1. **Consistent image dimensions** - Reduces padding overhead
2. **r=16 for vision** - Higher ranks help with visual features
3. **Lower learning rate** - 2e-5 typical for VLM vs 2e-4 for text-only
4. **Gradient accumulation** - Essential for batch size 1 with large images
5. **Train on assistant responses only** - Collator handles this automatically

---

## Example: Medical Imaging

```python
from unsloth import FastVisionModel

model, tokenizer = FastVisionModel.from_pretrained(
    model_name="unsloth/Llama-3.2-11B-Vision-Instruct",
    max_seq_length=4096,
    load_in_4bit=True,
)

# Medical imaging requires vision layer fine-tuning
model = FastVisionModel.get_peft_model(
    model,
    r=32,  # Higher rank for medical detail
    finetune_vision_layers=True,
    finetune_language_layers=True,
    finetune_attention_modules=True,
    finetune_mlp_modules=True,
)
```
