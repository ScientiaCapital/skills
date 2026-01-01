"""
Basic GRPO Training Example
===========================

Minimal working example for GRPO training with Unsloth.
Suitable for RunPod, Colab, or local GPU with 16GB+ VRAM.

Usage:
    python basic_grpo.py

Requirements:
    pip install unsloth vllm trl datasets
"""

import re
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import GRPOConfig, GRPOTrainer


# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    # Model settings
    "model_name": "Qwen/Qwen2.5-3B-Instruct",
    "max_seq_length": 1024,
    "lora_rank": 64,
    
    # Training settings
    "num_generations": 4,
    "max_completion_length": 512,
    "learning_rate": 5e-6,
    "beta": 0.04,
    "num_train_epochs": 1,
    "max_steps": 300,  # Minimum for seeing results
    
    # Output
    "output_dir": "grpo_output",
}

SYSTEM_PROMPT = """You are a helpful assistant that thinks step-by-step.

Always respond in this exact format:
<reasoning>
[Your step-by-step thinking process]
</reasoning>
<answer>
[Your final answer - just the number or short response]
</answer>
"""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_answer(text: str) -> str:
    """Extract answer from XML tags"""
    match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_reasoning(text: str) -> str:
    """Extract reasoning from XML tags"""
    match = re.search(r"<reasoning>(.*?)</reasoning>", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_gsm8k_answer(text: str) -> str:
    """Extract numeric answer from GSM8K format"""
    # GSM8K answers are after ####
    if "####" in text:
        return text.split("####")[-1].strip()
    return text.strip()


# =============================================================================
# REWARD FUNCTIONS
# =============================================================================

def correctness_reward(completions, answer, **kwargs):
    """
    Primary reward: +2.0 for correct answer, 0.0 otherwise
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        true_clean = extract_gsm8k_answer(str(true_answer))
        
        try:
            pred = float(extracted.replace(",", "").replace("$", "").strip())
            true = float(true_clean.replace(",", "").replace("$", "").strip())
            reward = 2.0 if abs(pred - true) < 0.01 else 0.0
        except (ValueError, AttributeError):
            reward = 2.0 if extracted.strip() == true_clean.strip() else 0.0
        
        rewards.append(reward)
    return rewards


def format_reward(completions, **kwargs):
    """
    Format compliance: +0.5 for proper XML structure
    """
    rewards = []
    for completion in completions:
        has_reasoning = bool(re.search(
            r"<reasoning>.*?</reasoning>", completion, re.DOTALL
        ))
        has_answer = bool(re.search(
            r"<answer>.*?</answer>", completion, re.DOTALL
        ))
        
        if has_reasoning and has_answer:
            rewards.append(0.5)
        elif has_answer:
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards


def reasoning_quality_reward(completions, **kwargs):
    """
    Reasoning length: +0.3 for substantive reasoning
    """
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion)
        word_count = len(reasoning.split()) if reasoning else 0
        
        if 20 <= word_count <= 200:
            rewards.append(0.3)
        elif 10 <= word_count < 20:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards


def integer_answer_reward(completions, **kwargs):
    """
    Encourage integer answers for math: +0.2 if answer is integer
    """
    rewards = []
    for completion in completions:
        extracted = extract_answer(completion)
        try:
            value = float(extracted.replace(",", "").replace("$", "").strip())
            rewards.append(0.2 if value == int(value) else 0.0)
        except:
            rewards.append(0.0)
    return rewards


# =============================================================================
# DATASET PREPARATION
# =============================================================================

def prepare_dataset():
    """Load and format GSM8K dataset for GRPO"""
    
    dataset = load_dataset("openai/gsm8k", "main", split="train")
    
    def format_example(example):
        return {
            "prompt": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": example["question"]}
            ],
            "answer": extract_gsm8k_answer(example["answer"])
        }
    
    dataset = dataset.map(format_example)
    
    # Optional: limit dataset size for faster iteration
    # dataset = dataset.select(range(500))
    
    return dataset


# =============================================================================
# MODEL LOADING
# =============================================================================

def load_model():
    """Load model with LoRA adapters"""
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=CONFIG["model_name"],
        max_seq_length=CONFIG["max_seq_length"],
        load_in_4bit=True,
        fast_inference=True,
        max_lora_rank=CONFIG["lora_rank"],
        gpu_memory_utilization=0.6,
    )
    
    model = FastLanguageModel.get_peft_model(
        model,
        r=CONFIG["lora_rank"],
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=CONFIG["lora_rank"],
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )
    
    return model, tokenizer


# =============================================================================
# TRAINING
# =============================================================================

def train():
    """Run GRPO training"""
    
    print("Loading model...")
    model, tokenizer = load_model()
    
    print("Preparing dataset...")
    dataset = prepare_dataset()
    
    print(f"Dataset size: {len(dataset)} examples")
    
    training_args = GRPOConfig(
        output_dir=CONFIG["output_dir"],
        
        # Batch configuration
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        
        # GRPO parameters
        num_generations=CONFIG["num_generations"],
        max_completion_length=CONFIG["max_completion_length"],
        max_prompt_length=256,
        beta=CONFIG["beta"],
        
        # Learning parameters
        learning_rate=CONFIG["learning_rate"],
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        
        # Training duration
        num_train_epochs=CONFIG["num_train_epochs"],
        max_steps=CONFIG["max_steps"],
        
        # Logging
        logging_steps=10,
        save_steps=100,
        report_to="none",
    )
    
    trainer = GRPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        reward_funcs=[
            correctness_reward,
            format_reward,
            reasoning_quality_reward,
            integer_answer_reward,
        ],
    )
    
    print("Starting GRPO training...")
    print(f"  Model: {CONFIG['model_name']}")
    print(f"  Generations per prompt: {CONFIG['num_generations']}")
    print(f"  Learning rate: {CONFIG['learning_rate']}")
    print(f"  Beta (KL penalty): {CONFIG['beta']}")
    print(f"  Max steps: {CONFIG['max_steps']}")
    print()
    
    trainer.train()
    
    print("\nTraining complete!")
    return model, tokenizer


# =============================================================================
# SAVING
# =============================================================================

def save_model(model, tokenizer):
    """Save trained model in multiple formats"""
    
    # Save LoRA weights
    print("Saving LoRA weights...")
    model.save_lora(f"{CONFIG['output_dir']}/lora")
    
    # Save merged model
    print("Saving merged model...")
    model.save_pretrained_merged(
        f"{CONFIG['output_dir']}/merged",
        tokenizer,
        save_method="merged_16bit",
    )
    
    # Save GGUF for llama.cpp
    print("Saving GGUF...")
    model.save_pretrained_gguf(
        f"{CONFIG['output_dir']}/gguf",
        tokenizer,
        quantization_method="q4_k_m",
    )
    
    print(f"\nModels saved to {CONFIG['output_dir']}/")


# =============================================================================
# INFERENCE
# =============================================================================

def test_model(model, tokenizer):
    """Test the trained model"""
    from vllm import SamplingParams
    
    test_questions = [
        "Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?",
        "A store sells apples for $2 each. If I buy 7 apples and pay with a $20 bill, how much change do I get?",
        "What is 15 + 27?",
    ]
    
    sampling_params = SamplingParams(
        temperature=0.7,
        top_p=0.95,
        max_tokens=512,
    )
    
    print("\n" + "="*60)
    print("TESTING TRAINED MODEL")
    print("="*60)
    
    for i, question in enumerate(test_questions, 1):
        prompt = tokenizer.apply_chat_template(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            tokenize=False,
            add_generation_prompt=True,
        )
        
        output = model.fast_generate(
            prompt,
            sampling_params=sampling_params,
            lora_request=model.load_lora(f"{CONFIG['output_dir']}/lora"),
        )[0].outputs[0].text
        
        print(f"\n--- Question {i} ---")
        print(f"Q: {question[:100]}...")
        print(f"\nA: {output}")
        print()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    model, tokenizer = train()
    save_model(model, tokenizer)
    test_model(model, tokenizer)
