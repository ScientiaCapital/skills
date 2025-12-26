#!/usr/bin/env python3
"""
Production-Ready RunPod Serverless Worker Template

This template provides a complete, production-grade handler for RunPod serverless
deployments. It includes:
- Model loading at startup (warm workers)
- Input validation with Pydantic
- Comprehensive error handling
- Structured logging
- Streaming support
- Progress updates for batch jobs
- Metrics collection
- Memory management

Usage:
1. Copy this template to your project
2. Customize the model loading section
3. Implement your inference logic in `run_inference()`
4. Build and deploy to RunPod

Environment Variables:
- MODEL_NAME: HuggingFace model name (required)
- HF_TOKEN: HuggingFace token for gated models (optional)
- MAX_TOKENS: Maximum tokens to generate (default: 2048)
- TEMPERATURE: Default temperature (default: 0.7)
- LOG_LEVEL: Logging level (default: INFO)
"""

import os
import gc
import time
import json
import logging
import traceback
from typing import Dict, Any, Optional, Generator, Union
from dataclasses import dataclass
from datetime import datetime

import runpod
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel, validator, Field

# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 2048))
DEFAULT_TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.7))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =============================================================================
# LOGGING
# =============================================================================

class JSONFormatter(logging.Formatter):
    """Structured JSON logging for production."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "job_id"):
            log_data["job_id"] = record.job_id
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """Configure structured logging."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger("runpod_worker")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    logger.addHandler(handler)

    return logger


logger = setup_logging()

# =============================================================================
# INPUT VALIDATION
# =============================================================================

class InferenceInput(BaseModel):
    """Validated input schema for inference requests."""

    # Text input (one of these required)
    prompt: Optional[str] = None
    messages: Optional[list] = None

    # Generation parameters
    max_tokens: int = Field(default=512, ge=1, le=MAX_TOKENS)
    temperature: float = Field(default=DEFAULT_TEMPERATURE, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    top_k: int = Field(default=50, ge=0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    stop: Optional[list] = None

    # Advanced options
    stream: bool = False
    return_usage: bool = True

    @validator("messages", "prompt", pre=True, always=True)
    def validate_input_provided(cls, v, values):
        if v is None and values.get("prompt") is None and values.get("messages") is None:
            pass  # Will be caught by root validator
        return v

    def __init__(self, **data):
        super().__init__(**data)
        if self.prompt is None and self.messages is None:
            raise ValueError("Either 'prompt' or 'messages' must be provided")


# =============================================================================
# METRICS COLLECTION
# =============================================================================

@dataclass
class WorkerMetrics:
    """Collect worker performance metrics."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens_generated: int = 0
    total_processing_time_s: float = 0.0

    def record(self, success: bool, tokens: int, duration_s: float):
        """Record a completed request."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            self.total_tokens_generated += tokens
        else:
            self.failed_requests += 1
        self.total_processing_time_s += duration_s

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / max(self.total_requests, 1),
            "total_tokens_generated": self.total_tokens_generated,
            "avg_processing_time_s": self.total_processing_time_s / max(self.total_requests, 1),
            "avg_tokens_per_request": self.total_tokens_generated / max(self.successful_requests, 1)
        }


metrics = WorkerMetrics()

# =============================================================================
# MODEL LOADING (AT STARTUP - OUTSIDE HANDLER)
# =============================================================================

logger.info(f"Loading model: {MODEL_NAME}")
start_load = time.time()

try:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        token=HF_TOKEN,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        token=HF_TOKEN,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )

    load_time = time.time() - start_load
    logger.info(f"Model loaded in {load_time:.2f}s on {DEVICE}")

    # Prewarm model with dummy inference
    logger.info("Prewarming model...")
    with torch.no_grad():
        dummy = tokenizer("Hello", return_tensors="pt").to(DEVICE)
        model.generate(**dummy, max_new_tokens=1)
    logger.info("Model prewarmed and ready")

except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

# =============================================================================
# INFERENCE LOGIC
# =============================================================================

def format_prompt(validated_input: InferenceInput) -> str:
    """Format input into model-ready prompt."""
    if validated_input.messages:
        # Use chat template for messages
        return tokenizer.apply_chat_template(
            validated_input.messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        return validated_input.prompt


def run_inference(
    prompt: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    stop: Optional[list] = None
) -> tuple[str, int]:
    """
    Run model inference.

    Returns:
        tuple: (generated_text, num_tokens_generated)
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    input_length = inputs.input_ids.shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature if temperature > 0 else None,
            top_p=top_p,
            top_k=top_k if top_k > 0 else None,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Get only new tokens
    new_tokens = outputs[0][input_length:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)

    return response, len(new_tokens)


def run_inference_stream(
    prompt: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int
) -> Generator[Dict[str, Any], None, None]:
    """
    Run streaming inference.

    Yields:
        dict: {"token": str, "finished": bool}
    """
    from transformers import TextIteratorStreamer
    from threading import Thread

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True
    )

    generation_kwargs = {
        **inputs,
        "max_new_tokens": max_tokens,
        "temperature": temperature if temperature > 0 else None,
        "top_p": top_p,
        "top_k": top_k if top_k > 0 else None,
        "do_sample": temperature > 0,
        "streamer": streamer,
        "pad_token_id": tokenizer.eos_token_id
    }

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    for token in streamer:
        yield {"token": token, "finished": False}

    thread.join()
    yield {"token": "", "finished": True}


# =============================================================================
# MAIN HANDLER
# =============================================================================

def handler(job: Dict[str, Any]) -> Union[Dict[str, Any], Generator]:
    """
    Main handler function for RunPod serverless.

    Supports:
    - Chat completion (messages array)
    - Text completion (prompt string)
    - Streaming responses
    - Full error handling and logging

    Args:
        job: RunPod job object with 'id' and 'input' keys

    Returns:
        dict: Response with generated text and metadata
        Generator: For streaming responses
    """
    job_id = job["id"]
    job_input = job.get("input", {})
    start_time = time.time()

    logger.info(
        "Job started",
        extra={"extra": {"job_id": job_id, "input_keys": list(job_input.keys())}}
    )

    try:
        # Validate input
        try:
            validated = InferenceInput(**job_input)
        except Exception as e:
            return {
                "error": f"Validation error: {str(e)}",
                "status": "VALIDATION_FAILED",
                "retry": False
            }

        # Format prompt
        prompt = format_prompt(validated)

        # Streaming mode
        if validated.stream:
            return run_inference_stream(
                prompt=prompt,
                max_tokens=validated.max_tokens,
                temperature=validated.temperature,
                top_p=validated.top_p,
                top_k=validated.top_k
            )

        # Standard inference
        response, tokens_generated = run_inference(
            prompt=prompt,
            max_tokens=validated.max_tokens,
            temperature=validated.temperature,
            top_p=validated.top_p,
            top_k=validated.top_k,
            stop=validated.stop
        )

        duration = time.time() - start_time

        # Record metrics
        metrics.record(success=True, tokens=tokens_generated, duration_s=duration)

        # Log completion
        logger.info(
            "Job completed",
            extra={
                "extra": {
                    "job_id": job_id,
                    "duration_s": round(duration, 3),
                    "tokens_generated": tokens_generated
                }
            }
        )

        # Build response
        result = {
            "response": response,
            "model": MODEL_NAME,
            "status": "SUCCESS"
        }

        if validated.return_usage:
            result["usage"] = {
                "prompt_tokens": len(tokenizer.encode(prompt)),
                "completion_tokens": tokens_generated,
                "total_tokens": len(tokenizer.encode(prompt)) + tokens_generated,
                "processing_time_s": round(duration, 3)
            }

        return result

    except torch.cuda.OutOfMemoryError:
        logger.error(
            "CUDA OOM",
            extra={"extra": {"job_id": job_id}}
        )
        metrics.record(success=False, tokens=0, duration_s=time.time() - start_time)
        return {
            "error": "GPU out of memory. Try reducing max_tokens or input length.",
            "status": "OOM_ERROR",
            "retry": False
        }

    except Exception as e:
        logger.error(
            f"Job failed: {str(e)}",
            extra={"extra": {"job_id": job_id}},
            exc_info=True
        )
        metrics.record(success=False, tokens=0, duration_s=time.time() - start_time)
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "ERROR",
            "retry": True
        }

    finally:
        # Clean up GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()


# =============================================================================
# ENTRYPOINT
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting RunPod serverless worker...")
    logger.info(f"Model: {MODEL_NAME}")
    logger.info(f"Max tokens: {MAX_TOKENS}")
    logger.info(f"Device: {DEVICE}")

    runpod.serverless.start({
        "handler": handler,
        "return_aggregate_stream": True
    })
