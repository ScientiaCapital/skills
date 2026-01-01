# Mobile Deployment

Quantization-Aware Training (QAT) and ExecuTorch export for iOS/Android.

---

## Overview

Deploy LLMs to phones with ~40 tokens/second inference:

```
Training → QAT → ExecuTorch → .pte file → Mobile App
```

---

## Quantization-Aware Training (QAT)

QAT simulates quantization during training, recovering up to 70% of accuracy lost from naive quantization.

### Performance

| Model | Benchmark | Recovery | Raw Gain |
|-------|-----------|----------|----------|
| Gemma3-4B | GPQA | 66.9% | +1.0% |
| Gemma3-12B | BBH | 45.5% | +2.1% |

### QAT Schemes

| Scheme | Weights | Activations | Use Case |
|--------|---------|-------------|----------|
| `int8-int4` | INT4 | INT8 | **Phone deployment** |
| `fp8-int4` | INT4 | FP8 | Better accuracy |
| `fp8-fp8` | FP8 | FP8 | Datacenter |
| `int4` | INT4 | None | Maximum compression |

### Installation

```bash
pip install --upgrade unsloth torchao==0.14.0 fbgemm-gpu-genai==1.3.0
```

### Training with QAT

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-0.6B",
    max_seq_length=1024,
    full_finetuning=True,           # QAT requires full fine-tuning
    qat_scheme="phone-deployment",  # Internally uses int8-int4
)

# Then train normally with SFTTrainer or GRPOTrainer
```

---

## ExecuTorch Export

After QAT training, export to ExecuTorch format:

### Export Process

```python
# After training, save for mobile
model.save_pretrained_executorch(
    "mobile_model",
    tokenizer,
)
# Produces .pte file (~472MB for Qwen3-0.6B)
```

### File Structure

```
mobile_model/
├── model.pte           # ExecuTorch model (~472MB)
├── tokenizer.json      # Tokenizer
└── config.json         # Model config
```

---

## iOS Deployment

### Requirements

- macOS with Xcode 15+
- Apple Developer account (for physical devices)
- iPhone with A14 chip or later

### Setup

1. Clone ExecuTorch iOS demo app
2. Copy `.pte` file to app resources
3. Build and run in Xcode

### Performance

| Device | Model | Tokens/sec |
|--------|-------|------------|
| iPhone 15 Pro | Qwen3-0.6B | ~40 |
| iPhone 14 | Qwen3-0.6B | ~30 |
| iPhone 13 | Qwen3-0.6B | ~20 |

### File Transfer

Drag and drop `.pte` file via Finder or use simulated file system in Xcode.

---

## Android Deployment

### Requirements

- Java 17
- Android SDK
- NDK 25.0.8775105
- Device with ARM64 (most modern Android phones)

### Setup

```bash
# Build ExecuTorch for Android
cd executorch
./gradlew :examples:demo-apps:android:llama-demo:assembleRelease

# Install APK
adb install -r examples/demo-apps/android/llama-demo/build/outputs/apk/release/llama-demo-release.apk
```

### File Transfer

```bash
# Push model to device
adb push mobile_model/model.pte /sdcard/Android/data/com.executorch.llamademo/files/
```

### Performance

| Device | Model | Tokens/sec |
|--------|-------|------------|
| Pixel 8 Pro | Qwen3-0.6B | ~40 |
| Galaxy S24 | Qwen3-0.6B | ~35 |
| Pixel 6 | Qwen3-0.6B | ~20 |

---

## Model Selection for Mobile

| Model | Size (.pte) | Quality | Recommended Device |
|-------|-------------|---------|-------------------|
| Qwen3-0.6B | ~472MB | Good | Any modern phone |
| Gemma3-270M | ~250MB | OK | Older phones |
| Qwen3-4B | ~2GB | Better | Flagship phones |

---

## Best Practices

### 1. Start with Small Model

```python
# Start with 0.6B for testing
model_name = "unsloth/Qwen3-0.6B"
```

### 2. Use Phone-Optimized QAT

```python
qat_scheme = "phone-deployment"  # Best for mobile
```

### 3. Limit Sequence Length

```python
max_seq_length = 512  # Reduces memory on device
```

### 4. Test on Simulator First

Before deploying to physical device, test in iOS Simulator or Android Emulator.

### 5. Monitor Memory

Mobile devices have limited RAM. Keep model under 2GB for best compatibility.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| App crashes on load | Model too large | Use smaller model (0.6B) |
| Slow inference | Old device | Use Gemma3-270M |
| Poor quality | Insufficient training | More QAT epochs |
| Export fails | Missing dependencies | Install torchao, fbgemm |

---

## Complete Workflow

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

# 1. Load with QAT
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-0.6B",
    max_seq_length=512,
    full_finetuning=True,
    qat_scheme="phone-deployment",
)

# 2. Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=SFTConfig(
        per_device_train_batch_size=4,
        num_train_epochs=3,
        learning_rate=2e-5,
    ),
)
trainer.train()

# 3. Export
model.save_pretrained_executorch("mobile_model", tokenizer)

# 4. Deploy .pte to iOS/Android
```
