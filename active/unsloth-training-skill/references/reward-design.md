# Reward Function Design Reference

Reward functions are the core of GRPO. They return a list of floats for each completion.

## Reward Function Anatomy

```python
def reward_function(
    completions: list[str],     # Generated responses
    answer: list[str] = None,   # Ground truth (if available)
    **kwargs                    # Additional dataset fields
) -> list[float]:
    """
    Returns a list of float rewards, one per completion.
    Positive = reinforce, Negative = suppress, Zero = neutral
    """
    rewards = []
    for completion in completions:
        reward = compute_reward(completion)
        rewards.append(reward)
    return rewards
```

## Essential Extraction Helpers

```python
import re

def extract_answer(text: str) -> str:
    """Extract answer from XML tags"""
    match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_reasoning(text: str) -> str:
    """Extract reasoning from XML tags"""
    match = re.search(r"<reasoning>(.*?)</reasoning>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

def normalize_number(text: str) -> float | None:
    """Parse number from text"""
    if not text:
        return None
    cleaned = text.replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None
```

## Pattern 1: Correctness Reward (Primary Signal)

```python
def correctness_reward(completions, answer, **kwargs):
    """
    Primary learning signal: +2.0 for correct, 0.0 otherwise
    This should be your highest-weighted reward.
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        try:
            pred = float(extracted.replace(",", "").strip())
            true = float(true_answer.replace(",", "").strip())
            reward = 2.0 if abs(pred - true) < 0.01 else 0.0
        except (ValueError, AttributeError):
            reward = 2.0 if extracted.strip() == str(true_answer).strip() else 0.0
        rewards.append(reward)
    return rewards
```

## Pattern 2: Proximity Reward (Gradient Signal)

```python
def proximity_reward(completions, answer, **kwargs):
    """
    Gradient reward based on closeness to correct answer.
    Helps model learn direction even when wrong.
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        pred_num = normalize_number(extracted)
        true_num = normalize_number(str(true_answer))

        if pred_num is not None and true_num is not None:
            if abs(pred_num - true_num) < 0.01:
                reward = 2.0
            else:
                error_ratio = abs(pred_num - true_num) / max(abs(true_num), 1)
                reward = max(0.0, 2.0 * (1.0 - min(error_ratio, 1.0)))
        else:
            reward = 2.0 if extracted.strip().lower() == str(true_answer).strip().lower() else 0.0

        rewards.append(reward)
    return rewards
```

## Pattern 3: Format Compliance

```python
def format_reward(completions, **kwargs):
    """
    XML format compliance: +0.5 for proper structure
    """
    rewards = []
    for completion in completions:
        has_reasoning = bool(re.search(r"<reasoning>.*?</reasoning>", completion, re.DOTALL))
        has_answer = bool(re.search(r"<answer>.*?</answer>", completion, re.DOTALL))

        if has_reasoning and has_answer:
            rewards.append(0.5)
        elif has_answer:
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards
```

## Pattern 4: Reasoning Quality

```python
def reasoning_length_reward(completions, **kwargs):
    """
    Encourage substantive reasoning: +0.3 for good length
    """
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion)
        word_count = len(reasoning.split()) if reasoning else 0

        if 30 <= word_count <= 200:
            rewards.append(0.3)   # Good length
        elif 15 <= word_count < 30:
            rewards.append(0.1)   # Too brief
        elif word_count > 200:
            rewards.append(0.1)   # Too verbose
        else:
            rewards.append(0.0)   # Way too short
    return rewards

def step_count_reward(completions, **kwargs):
    """Reward explicit step-by-step reasoning"""
    step_patterns = [r"step \d+", r"first[,:]", r"then[,:]", r"finally[,:]", r"\d+\."]

    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion).lower()
        steps = sum(len(re.findall(p, reasoning)) for p in step_patterns)

        if 2 <= steps <= 10:
            rewards.append(0.3)
        elif steps > 0:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards
```

## Pattern 5: Negative Constraints

```python
def no_hedging_reward(completions, **kwargs):
    """Penalize uncertainty language: -0.3 if hedging"""
    hedging = [
        "i think", "maybe", "perhaps", "possibly",
        "i'm not sure", "i believe", "it could be",
        "probably", "might be"
    ]
    rewards = []
    for completion in completions:
        lower = completion.lower()
        has_hedging = any(phrase in lower for phrase in hedging)
        rewards.append(-0.3 if has_hedging else 0.0)
    return rewards

def no_repetition_reward(completions, **kwargs):
    """Penalize repetitive text: -0.5 if too repetitive"""
    rewards = []
    for completion in completions:
        sentences = [s.strip().lower() for s in completion.split('.') if s.strip()]
        if len(sentences) < 2:
            rewards.append(0.0)
            continue

        unique = set(sentences)
        ratio = len(unique) / len(sentences)
        rewards.append(0.0 if ratio >= 0.7 else -0.5)
    return rewards
```

## Reward Weighting Strategy

```python
# Typical reward weights (sum of max possible ~3.0-4.0)
reward_funcs = [
    correctness_reward,      # +2.0 max (primary signal)
    format_reward,           # +0.5 max (structure)
    reasoning_length_reward, # +0.3 max (quality)
    no_hedging_reward,       # -0.3 max (constraint)
]

# Total possible range: -0.3 to +2.8
```

## Best Practices

**DO:**
- Start with correctness as highest-weighted reward
- Use multiple complementary rewards (rubric approach)
- Test rewards manually before training
- Log reward distributions during training
- Use proximity rewards to help learning direction

**DON'T:**
- Use a single "all or nothing" reward
- Weight formatting higher than correctness
- Create rewards that conflict with each other
- Forget to handle edge cases (empty responses, errors)

## Testing Rewards

```python
def test_reward_functions(reward_funcs, test_completion, test_answer="42"):
    """Debug utility to test reward functions"""
    print("="*60)
    print("REWARD FUNCTION TEST")
    print("="*60)

    total = 0.0
    for func in reward_funcs:
        result = func([test_completion], [test_answer])[0]
        total += result
        print(f"  {func.__name__}: {result:+.2f}")

    print("-"*40)
    print(f"  TOTAL: {total:+.2f}")

# Example usage
test_completion = """<reasoning>
Let me solve this step by step.
Step 1: The problem asks for 6 * 7
Step 2: 6 * 7 = 42
</reasoning>
<answer>42</answer>"""

test_reward_functions([correctness_reward, format_reward], test_completion, "42")
```
