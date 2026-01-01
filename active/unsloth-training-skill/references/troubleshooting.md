# Troubleshooting Reference

## Common Issues

### Reward Not Increasing

1. **Wait longer** - minimum 300 steps before expecting change
2. **Check reward function** - verify it returns non-zero values
3. **Verify dataset** - ensure it has verifiable answers
4. **Increase learning rate** - try 2x current value
5. **Use proximity rewards** - helps model learn direction
6. **Check model size** - use at least 1.5B parameters

### Out of Memory (OOM)

1. **Reduce max_completion_length** - shorter responses = less VRAM
2. **Reduce num_generations** - minimum 2 for GRPO
3. **Enable gradient checkpointing**:
   ```python
   use_gradient_checkpointing = "unsloth"
   ```
4. **Reduce LoRA rank** - try 32 instead of 64
5. **Lower gpu_memory_utilization**:
   ```python
   gpu_memory_utilization = 0.5
   ```
6. **Use 4-bit quantization**:
   ```python
   load_in_4bit = True
   ```

### Model Outputs Garbage

1. **Increase beta** - higher KL penalty constrains drift
2. **Decrease learning rate** - try 0.5x current value
3. **Check prompt format** - must match training format
4. **Verify reward functions** - check for bugs
5. **Start from instruction-tuned model** - not base model

### No Reasoning Tokens

1. **Train for more steps** - minimum 500 steps
2. **Use larger model** - at least 1.5B parameters
3. **Check format reward** - verify it's working
4. **Use stronger correctness signal** - +2.0 for correct
5. **Verify system prompt** - must include reasoning format

### JSON Parsing Failed

1. **Lower temperature** - try 0.05 for structured output
2. **Add more examples** - with clean JSON output
3. **Check training data quality** - garbage in, garbage out

### High Loss / Bad Outputs

1. **Check data quality** - review training examples
2. **Try more epochs** - 4-5 for better convergence
3. **Increase LoRA rank** - try 64 or higher

## Validation Checklist

### GRPO Training

```
□ Model loads without OOM
□ LoRA configured with gradient checkpointing
□ Dataset has prompt and answer fields
□ At least one reward function defined
□ Reward functions tested manually
□ num_generations >= 2
□ beta set (0.01-0.1)
□ learning_rate set (1e-6 to 1e-5)
□ At least 300 steps planned
□ Logging enabled to monitor progress
```

### SFT Training

```
□ Model loads without OOM
□ Dataset has conversations field
□ Chat template applied correctly
□ batch_size fits in VRAM
□ 2-4 epochs planned
□ learning_rate ~2e-4
```

## Error Messages

### "No module named unsloth"

```bash
pip install unsloth
# Or for latest:
pip install "unsloth @ git+https://github.com/unslothai/unsloth.git"
```

### "CUDA out of memory"

See OOM solutions above. Quick fix:
```python
gpu_memory_utilization = 0.5
num_generations = 2
max_completion_length = 256
```

### "Expected Float but got Long"

Usually a reward function returning int instead of float:
```python
# Wrong
return [2 if correct else 0 for ...]

# Right
return [2.0 if correct else 0.0 for ...]
```

### "Reward function must return list"

```python
# Wrong - returns single value
def bad_reward(completions, **kwargs):
    return 1.0

# Right - returns list
def good_reward(completions, **kwargs):
    return [1.0 for _ in completions]
```

## Debug Tips

### Print Reward Distribution

```python
# Add to training script
import numpy as np

for step, batch in enumerate(trainer.get_train_dataloader()):
    if step % 50 == 0:
        rewards = trainer.compute_rewards(batch)
        print(f"Step {step}: reward mean={np.mean(rewards):.3f}, std={np.std(rewards):.3f}")
```

### Test Reward Function

```python
test_completion = "<reasoning>2+2=4</reasoning><answer>4</answer>"
test_answer = "4"

result = correctness_reward([test_completion], [test_answer])
print(f"Reward: {result[0]}")  # Should be 2.0
```

### Check Model Output

```python
# After loading model
from vllm import SamplingParams

prompt = tokenizer.apply_chat_template([
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "What is 2+2?"}
], tokenize=False, add_generation_prompt=True)

output = model.fast_generate(
    prompt,
    sampling_params=SamplingParams(temperature=0.7, max_tokens=256)
)[0].outputs[0].text

print(output)
```
