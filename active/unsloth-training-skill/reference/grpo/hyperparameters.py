"""
GRPO Hyperparameter Quick Reference
====================================

Condensed reference for tuning GRPO training.
Print this or keep it open during experiments.
"""

# =============================================================================
# CORE PARAMETERS - START HERE
# =============================================================================

CORE_PARAMS = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ CORE GRPO PARAMETERS                                                        │
├─────────────────┬───────────┬───────────────────────────────────────────────┤
│ Parameter       │ Default   │ Notes                                         │
├─────────────────┼───────────┼───────────────────────────────────────────────┤
│ num_generations │ 4         │ Completions per prompt (G in paper)           │
│                 │           │ Range: 2-16, Must be >= 2                     │
│                 │           │ Higher = more stable, more VRAM               │
├─────────────────┼───────────┼───────────────────────────────────────────────┤
│ beta            │ 0.04      │ KL penalty coefficient                        │
│                 │           │ Range: 0.001-0.5                              │
│                 │           │ Higher = more constrained to reference        │
├─────────────────┼───────────┼───────────────────────────────────────────────┤
│ learning_rate   │ 5e-6      │ Gradient step size                            │
│                 │           │ Range: 1e-6 to 1e-5 (smaller than SFT!)       │
│                 │           │ Start conservative, increase if too slow      │
├─────────────────┼───────────┼───────────────────────────────────────────────┤
│ max_completion  │ 512       │ Max tokens in generated response              │
│ _length         │           │ Match to task needs, affects VRAM             │
└─────────────────┴───────────┴───────────────────────────────────────────────┘
"""

# =============================================================================
# TROUBLESHOOTING GUIDE
# =============================================================================

TROUBLESHOOTING = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ SYMPTOM → ACTION                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Reward not increasing:                                                      │
│   1. Wait longer (minimum 300 steps)                                        │
│   2. Increase learning_rate (2x)                                            │
│   3. Verify reward functions return non-zero                                │
│   4. Check dataset has verifiable answers                                   │
│   5. Use proximity rewards instead of binary                                │
│                                                                             │
│ Reward spiky/unstable:                                                      │
│   1. Decrease learning_rate (0.5x)                                          │
│   2. Increase beta (KL penalty)                                             │
│   3. Increase gradient_accumulation_steps                                   │
│   4. Increase num_generations                                               │
│                                                                             │
│ Model outputs garbage:                                                      │
│   1. Increase beta significantly (2-4x)                                     │
│   2. Decrease learning_rate (0.25x)                                         │
│   3. Check prompt format matches training                                   │
│   4. Start from instruction-tuned model (not base)                          │
│                                                                             │
│ No reasoning tokens appearing:                                              │
│   1. Train for more steps (500+)                                            │
│   2. Use model >= 1.5B parameters                                           │
│   3. Verify format reward is working                                        │
│   4. Add explicit format examples in system prompt                          │
│                                                                             │
│ Out of Memory (OOM):                                                        │
│   1. Reduce max_completion_length                                           │
│   2. Reduce num_generations (minimum 2)                                     │
│   3. Enable use_gradient_checkpointing = "unsloth"                          │
│   4. Reduce LoRA rank                                                       │
│   5. Lower gpu_memory_utilization                                           │
│   6. Ensure load_in_4bit = True                                             │
│                                                                             │
│ Reward increases then crashes:                                              │
│   1. Increase beta (model drifted too far)                                  │
│   2. Lower learning_rate                                                    │
│   3. Save checkpoints more frequently                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# LOSS TYPE SELECTION
# =============================================================================

LOSS_TYPES = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ LOSS TYPE SELECTION                                                         │
├─────────────┬───────────────────────────────────────────────────────────────┤
│ loss_type   │ Use When                                                      │
├─────────────┼───────────────────────────────────────────────────────────────┤
│ "grpo"      │ Default. General purpose. Start here.                         │
│             │ Original DeepSeek algorithm.                                  │
├─────────────┼───────────────────────────────────────────────────────────────┤
│ "dr_grpo"   │ Long outputs being under-penalized.                           │
│             │ Removes length bias. Set scale_rewards=False.                 │
├─────────────┼───────────────────────────────────────────────────────────────┤
│ "dapo"      │ Training instability. Better token normalization.             │
│             │ Use with epsilon=0.2, epsilon_high=0.28                       │
├─────────────┼───────────────────────────────────────────────────────────────┤
│ "gspo"      │ Sequence-level tasks. Qwen-style.                             │
│             │ Set importance_sampling_level="sequence"                      │
├─────────────┼───────────────────────────────────────────────────────────────┤
│ "bnpo"      │ Batch-normalized. Results vary with batch size.               │
│             │ Equivalent to GRPO when batch_size=1.                         │
└─────────────┴───────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# VRAM REQUIREMENTS
# =============================================================================

VRAM_GUIDE = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ VRAM REQUIREMENTS (QLoRA 4-bit)                                             │
├─────────────────┬─────────────┬─────────────────────────────────────────────┤
│ Model Size      │ Min VRAM    │ Recommended num_generations                  │
├─────────────────┼─────────────┼─────────────────────────────────────────────┤
│ 1.5B            │ 5GB         │ 2-4                                          │
│ 3B              │ 8GB         │ 4                                            │
│ 7B              │ 16GB        │ 4-6                                          │
│ 14B             │ 20GB        │ 4                                            │
│ 70B             │ 48GB+       │ 2-4                                          │
├─────────────────┴─────────────┴─────────────────────────────────────────────┤
│                                                                             │
│ Memory-saving options:                                                      │
│   - use_gradient_checkpointing = "unsloth"  →  60% less VRAM                │
│   - load_in_4bit = True                     →  4x less model memory         │
│   - float8_kv_cache = True (RTX 3090+)      →  2x less KV cache             │
│   - gpu_memory_utilization = 0.5            →  More headroom                │
│                                                                             │
│ Unsloth efficiency:                                                         │
│   Standard GRPO (20K context): 510GB VRAM                                   │
│   Unsloth GRPO (20K context):   54GB VRAM  (90% reduction!)                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# REWARD FUNCTION WEIGHTS
# =============================================================================

REWARD_WEIGHTS = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ RECOMMENDED REWARD WEIGHTS                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ The total reward range should be approximately -1.0 to +3.0                 │
│ Correctness should be the dominant signal.                                  │
│                                                                             │
│ Typical configuration:                                                      │
│                                                                             │
│   correctness_reward      →  +2.0 max  (PRIMARY SIGNAL)                     │
│   format_reward           →  +0.5 max  (structure compliance)               │
│   reasoning_quality       →  +0.3 max  (optional quality bonus)             │
│   constraint penalties    →  -0.3 max  (guard against bad outputs)          │
│   ──────────────────────────────────────                                    │
│   Total range: -0.3 to +2.8                                                 │
│                                                                             │
│ Anti-patterns to avoid:                                                     │
│   ✗ Single binary reward (all or nothing)                                   │
│   ✗ Format weighted higher than correctness                                 │
│   ✗ Too many conflicting constraints                                        │
│   ✗ Rewards that can't be achieved together                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# TRAINING CHECKLIST
# =============================================================================

CHECKLIST = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ PRE-TRAINING CHECKLIST                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ □ Model loads without OOM                                                   │
│ □ LoRA configured with gradient_checkpointing = "unsloth"                   │
│ □ Dataset has 'prompt' and 'answer' fields                                  │
│ □ At least 500 rows of data (minimum 10, more is better)                    │
│ □ At least one reward function defined                                      │
│ □ Reward functions tested manually with sample outputs                      │
│ □ num_generations >= 2                                                      │
│ □ beta set between 0.01 and 0.1 (start at 0.04)                            │
│ □ learning_rate set between 1e-6 and 1e-5 (start at 5e-6)                  │
│ □ At least 300 steps planned (more for better results)                      │
│ □ Logging enabled to monitor progress                                       │
│ □ Checkpoint saving configured                                              │
│                                                                             │
│ Minimum viable training time:                                               │
│   - See first results: ~300 steps (~30 min)                                 │
│   - Decent results: ~1000 steps (~2-3 hours)                                │
│   - Good results: ~3000+ steps (12+ hours)                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# SCIENTIFIC NOTATION REFERENCE
# =============================================================================

NOTATION = """
┌─────────────────────────────────────────────────────────────────────────────┐
│ SCIENTIFIC NOTATION QUICK REFERENCE                                         │
├───────────┬───────────────┬─────────────────────────────────────────────────┤
│ Notation  │ Decimal       │ Common Use                                      │
├───────────┼───────────────┼─────────────────────────────────────────────────┤
│ 1e-2      │ 0.01          │ Weight decay                                    │
│ 1e-3      │ 0.001         │ SFT learning rate (aggressive)                  │
│ 1e-4      │ 0.0001        │ SFT learning rate (typical)                     │
│ 5e-5      │ 0.00005       │ SFT learning rate (conservative)                │
│ 1e-5      │ 0.00001       │ RL learning rate (aggressive)                   │
│ 5e-6      │ 0.000005      │ RL learning rate (typical)                      │
│ 1e-6      │ 0.000001      │ RL learning rate (conservative)                 │
├───────────┴───────────────┴─────────────────────────────────────────────────┤
│                                                                             │
│ The negative exponent = decimal places to move left                         │
│ Example: 5e-6 = 5 × 10^-6 = 0.000005                                        │
│                                                                             │
│ Rule: RL needs ~10x smaller learning rate than SFT                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""


def print_all():
    """Print all reference tables"""
    print(CORE_PARAMS)
    print(TROUBLESHOOTING)
    print(LOSS_TYPES)
    print(VRAM_GUIDE)
    print(REWARD_WEIGHTS)
    print(CHECKLIST)
    print(NOTATION)


if __name__ == "__main__":
    print_all()
