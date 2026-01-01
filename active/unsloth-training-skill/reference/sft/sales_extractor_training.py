"""
Sales Call Extraction Model - Fine-Tuning with Unsloth
======================================================

Run this on:
- Google Colab (free T4 GPU) - recommended for starting
- Kaggle (free P100 GPU)
- Any machine with 16GB+ VRAM

Training time: ~30-60 minutes for 1000 examples
Output: GGUF model ready for mobile deployment

Setup instructions:
1. Upload your training_data.jsonl file
2. Run all cells in order
3. Download the GGUF from sales_extractor_gguf/

Author: Tim Kipper
Purpose: GTME Portfolio - On-device sales assistant
"""

# =============================================================================
# CELL 1: Install Dependencies
# =============================================================================
# Run this cell first, then restart runtime if prompted

"""
# Uncomment and run in Colab/Kaggle:

!pip install unsloth
# Get the latest nightly Unsloth for best performance
!pip uninstall unsloth -y && pip install --upgrade --no-cache-dir "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps trl peft accelerate bitsandbytes
"""

# =============================================================================
# CELL 2: Imports and Configuration
# =============================================================================

import json
import torch
from datetime import datetime
from pathlib import Path

# Unsloth imports
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

# Training imports
from datasets import Dataset, load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# =============================================================================
# CELL 3: Configuration
# =============================================================================

# Model configuration
CONFIG = {
    # Base model - Qwen2.5-0.5B is the sweet spot for mobile
    # Other options: "unsloth/Qwen2.5-1.5B-Instruct" (larger, better)
    #                "unsloth/Phi-3-mini-4k-instruct" (Microsoft, good quality)
    #                "unsloth/gemma-2-2b-it" (Google, good for tool calling)
    "base_model": "unsloth/Qwen2.5-0.5B-Instruct",
    
    # Sequence length - 1024 is plenty for call notes
    "max_seq_length": 1024,
    
    # LoRA configuration
    "lora_r": 16,              # Rank - higher = more capacity, more memory
    "lora_alpha": 16,          # Scaling factor
    "lora_dropout": 0,         # 0 is optimized for Unsloth
    
    # Training configuration
    "num_epochs": 3,           # 2-4 epochs typically sufficient
    "batch_size": 2,           # Increase if you have more VRAM
    "gradient_accumulation": 4, # Effective batch = batch_size * grad_accum
    "learning_rate": 2e-4,     # Standard for LoRA fine-tuning
    "warmup_steps": 10,
    
    # Paths
    "training_data": "training_data.jsonl",
    "output_dir": "outputs",
    "model_name": "sales_extractor",
}

# System prompt - this gets baked into the model's behavior
SYSTEM_PROMPT = """You are a sales call extraction assistant for MEP (Mechanical, Electrical, Plumbing) contractor software sales.

Given a voice note transcript from a sales rep after a prospect call, extract structured information.

Output ONLY valid JSON with these fields:
{
  "company_name": "string",
  "contact_name": "string or null",
  "contact_title": "string or null",
  "team_size": "integer or null",
  "team_breakdown": "string or null (e.g., '15 field, 5 office')",
  "location": "string or null",
  "vertical": "string or null (e.g., 'commercial HVAC', 'residential plumbing')",
  "current_software": ["array", "of", "strings"],
  "pain_points": ["array", "of", "strings"],
  "interest_areas": ["array", "of", "strings"],
  "budget_mentioned": "string or null",
  "timeline": "string or null",
  "decision_makers": ["array", "of", "strings"],
  "next_step": "demo | follow_up_call | send_info | proposal | none",
  "next_step_date": "string or null",
  "next_step_notes": "string or null",
  "intent_level": "high | medium | low | unknown",
  "key_quotes": ["array", "of", "notable", "verbatim", "quotes"],
  "competitors_mentioned": ["array", "of", "strings"]
}

Rules:
- Only output JSON, no explanations
- Use null for missing information, don't guess
- Extract verbatim quotes that reveal intent or pain
- Normalize software names (e.g., "ST" → "ServiceTitan")
- Be conservative with intent_level unless signals are clear"""

print(f"Configuration loaded. Base model: {CONFIG['base_model']}")

# =============================================================================
# CELL 4: Load Base Model
# =============================================================================

print("Loading base model...")
print("This may take 2-5 minutes on first run (downloading weights)")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=CONFIG["base_model"],
    max_seq_length=CONFIG["max_seq_length"],
    dtype=None,  # Auto-detect: float16 for T4, bfloat16 for A100/H100
    load_in_4bit=True,  # QLoRA - reduces memory by 4x
)

print(f"✓ Model loaded: {CONFIG['base_model']}")
print(f"  Max sequence length: {CONFIG['max_seq_length']}")
print(f"  Quantization: 4-bit (QLoRA)")

# =============================================================================
# CELL 5: Add LoRA Adapters
# =============================================================================

print("Adding LoRA adapters...")

model = FastLanguageModel.get_peft_model(
    model,
    r=CONFIG["lora_r"],
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj",      # MLP
    ],
    lora_alpha=CONFIG["lora_alpha"],
    lora_dropout=CONFIG["lora_dropout"],
    bias="none",
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

# Count trainable parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"✓ LoRA adapters added")
print(f"  Total parameters: {total_params:,}")
print(f"  Trainable parameters: {trainable_params:,} ({100*trainable_params/total_params:.2f}%)")

# =============================================================================
# CELL 6: Load and Prepare Training Data
# =============================================================================

print(f"Loading training data from {CONFIG['training_data']}...")

# Load the JSONL file
dataset = load_dataset(
    "json", 
    data_files=CONFIG["training_data"], 
    split="train"
)

print(f"✓ Loaded {len(dataset)} training examples")

# Preview first example
print("\nFirst example preview:")
print(f"  Keys: {list(dataset[0].keys())}")

# Apply chat template formatting
def format_for_training(examples):
    """
    Format examples using the model's chat template.
    
    Expected input format (from your JSONL):
    {
        "conversations": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }
    """
    texts = []
    
    for convo in examples["conversations"]:
        # Apply the model's native chat template
        text = tokenizer.apply_chat_template(
            convo,
            tokenize=False,
            add_generation_prompt=False
        )
        texts.append(text)
    
    return {"text": texts}

# Check if data is already in conversation format
if "conversations" in dataset.column_names:
    print("Data is in conversation format, applying chat template...")
    dataset = dataset.map(format_for_training, batched=True)
elif "text" in dataset.column_names:
    print("Data already has 'text' field, using as-is...")
else:
    raise ValueError(
        f"Unexpected data format. Found columns: {dataset.column_names}. "
        "Expected either 'conversations' or 'text' column."
    )

# Show formatted example
print("\nFormatted example preview (first 500 chars):")
print(dataset[0]["text"][:500] + "...")

# =============================================================================
# CELL 7: Configure Trainer
# =============================================================================

print("Configuring trainer...")

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=CONFIG["max_seq_length"],
    dataset_num_proc=2,
    packing=False,  # Don't pack multiple examples (simpler, more stable)
    args=TrainingArguments(
        # Batch configuration
        per_device_train_batch_size=CONFIG["batch_size"],
        gradient_accumulation_steps=CONFIG["gradient_accumulation"],
        
        # Training schedule
        warmup_steps=CONFIG["warmup_steps"],
        num_train_epochs=CONFIG["num_epochs"],
        
        # Optimizer configuration
        learning_rate=CONFIG["learning_rate"],
        optim="adamw_8bit",  # Memory-efficient optimizer
        weight_decay=0.01,
        lr_scheduler_type="linear",
        
        # Precision
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        
        # Logging
        logging_steps=10,
        logging_first_step=True,
        
        # Saving
        output_dir=CONFIG["output_dir"],
        save_strategy="epoch",
        
        # Reproducibility
        seed=3407,
    ),
)

# Estimate training time
steps_per_epoch = len(dataset) // (CONFIG["batch_size"] * CONFIG["gradient_accumulation"])
total_steps = steps_per_epoch * CONFIG["num_epochs"]
print(f"✓ Trainer configured")
print(f"  Steps per epoch: {steps_per_epoch}")
print(f"  Total training steps: {total_steps}")
print(f"  Estimated time: {total_steps * 2}s - {total_steps * 4}s")  # ~2-4s per step on T4

# =============================================================================
# CELL 8: Train the Model
# =============================================================================

print("="*60)
print("STARTING TRAINING")
print("="*60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Train!
trainer_stats = trainer.train()

print()
print("="*60)
print("TRAINING COMPLETE")
print("="*60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total training time: {trainer_stats.metrics['train_runtime']:.1f}s")
print(f"Final loss: {trainer_stats.metrics['train_loss']:.4f}")

# =============================================================================
# CELL 9: Test the Model
# =============================================================================

print("\nTesting the fine-tuned model...")

# Enable inference mode
FastLanguageModel.for_inference(model)

# Test examples - mix of easy and hard
test_transcripts = [
    # Easy - clear signals
    """Just finished a great call with Mike Thompson over at Reliable Mechanical. 
    They're a 35-person commercial HVAC shop in Phoenix, been running ServiceTitan 
    for two years but Mike says the pricing has gotten insane, like three times what 
    they signed up for. Really interested in our job costing features, said that's 
    their biggest gap right now. Wants to do a demo next Tuesday.""",
    
    # Medium - some missing info
    """Quick call with someone at Premier Plumbing, I think his name was Dave. 
    Small shop, maybe 10 guys. They're still on paper and QuickBooks. 
    Not sure they're ready to move yet but said to check back in Q2.""",
    
    # Hard - messy, multiple signals
    """So that was interesting, ABC Services, they do HVAC and plumbing, talked to 
    the owner Sarah and her ops manager. They tried Housecall Pro last year, total 
    disaster, techs refused to use it. Now they're gun shy. But Sarah mentioned 
    they're losing track of parts inventory and it's killing their margins. 
    Maybe 20 people, mix of residential and light commercial in the Denver area. 
    She wants to see something simple, said her guys aren't tech savvy. 
    I'm sending over some case studies first.""",
]

for i, transcript in enumerate(test_transcripts, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}")
    print(f"{'='*60}")
    print(f"Input (first 100 chars): {transcript[:100]}...")
    
    # Format the input
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": transcript}
    ]
    
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)
    
    # Generate
    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=512,
        temperature=0.1,  # Low temperature for structured output
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    # Decode and extract the assistant's response
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Try to extract just the JSON
    try:
        json_start = full_response.rfind("{")
        json_end = full_response.rfind("}") + 1
        json_str = full_response[json_start:json_end]
        parsed = json.loads(json_str)
        print(f"\nExtracted JSON (valid ✓):")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"\nRaw output (JSON parsing failed):")
        print(full_response[-1000:])  # Last 1000 chars
        print(f"\nJSON Error: {e}")

# =============================================================================
# CELL 10: Save the Model
# =============================================================================

print("\n" + "="*60)
print("SAVING MODEL")
print("="*60)

# Create output directories
Path(f"{CONFIG['model_name']}_lora").mkdir(exist_ok=True)
Path(f"{CONFIG['model_name']}_gguf").mkdir(exist_ok=True)

# Option 1: Save LoRA adapters only (small, ~50MB)
print("\n1. Saving LoRA adapters...")
model.save_pretrained(f"{CONFIG['model_name']}_lora")
tokenizer.save_pretrained(f"{CONFIG['model_name']}_lora")
print(f"   ✓ Saved to {CONFIG['model_name']}_lora/")

# Option 2: Save merged model as GGUF (for llama.cpp, Ollama, ExecuTorch)
print("\n2. Saving as GGUF (q4_k_m quantization)...")
model.save_pretrained_gguf(
    f"{CONFIG['model_name']}_gguf",
    tokenizer,
    quantization_method="q4_k_m"  # Good balance of size/quality
)
print(f"   ✓ Saved to {CONFIG['model_name']}_gguf/")

# Option 3: Additional GGUF quantizations (optional)
print("\n3. Saving additional GGUF variants...")
for quant in ["q8_0", "f16"]:  # Higher quality options
    try:
        model.save_pretrained_gguf(
            f"{CONFIG['model_name']}_gguf",
            tokenizer,
            quantization_method=quant
        )
        print(f"   ✓ Saved {quant}")
    except Exception as e:
        print(f"   ✗ {quant} failed: {e}")

# =============================================================================
# CELL 11: Export Summary
# =============================================================================

print("\n" + "="*60)
print("EXPORT COMPLETE - SUMMARY")
print("="*60)

print(f"""
Files created:

1. LoRA Adapters ({CONFIG['model_name']}_lora/):
   - adapter_config.json
   - adapter_model.safetensors
   Use: Load with base model for inference
   Size: ~50MB
   
2. GGUF Models ({CONFIG['model_name']}_gguf/):
   - *-q4_k_m.gguf  (recommended for mobile)
   - *-q8_0.gguf    (higher quality)
   - *-f16.gguf     (highest quality)
   Use: llama.cpp, Ollama, ExecuTorch
   Size: ~200-400MB depending on quantization

Next steps:
1. Download the q4_k_m.gguf file
2. Test locally with Ollama:
   ollama create sales-extractor -f Modelfile
   ollama run sales-extractor
   
3. For ExecuTorch mobile deployment:
   See the ExecuTorch export script

Training metadata:
- Base model: {CONFIG['base_model']}
- Training examples: {len(dataset)}
- Final loss: {trainer_stats.metrics['train_loss']:.4f}
- Training time: {trainer_stats.metrics['train_runtime']:.1f}s
""")

# =============================================================================
# CELL 12: Create Ollama Modelfile (for local testing)
# =============================================================================

modelfile_content = f'''# Modelfile for sales-extractor
# Usage: ollama create sales-extractor -f Modelfile

FROM ./{CONFIG['model_name']}_gguf/*-q4_k_m.gguf

TEMPLATE """{{{{ if .System }}}}<|im_start|>system
{{{{ .System }}}}<|im_end|>
{{{{ end }}}}<|im_start|>user
{{{{ .Prompt }}}}<|im_end|>
<|im_start|>assistant
"""

SYSTEM """{SYSTEM_PROMPT}"""

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER stop "<|im_end|>"
'''

with open("Modelfile", "w") as f:
    f.write(modelfile_content)

print("Created Modelfile for Ollama")
print("\nTo test locally:")
print("  1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh")
print("  2. ollama create sales-extractor -f Modelfile")
print("  3. ollama run sales-extractor")
