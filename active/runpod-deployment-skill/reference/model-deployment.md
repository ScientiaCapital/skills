# Model Deployment Patterns - Complete Guide

Production patterns for deploying ML models on RunPod.

## HuggingFace Model Deployment

### Basic HuggingFace Handler

```python
import runpod
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model at startup (outside handler)
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN")

print(f"Loading model: {MODEL_NAME}")

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

print("Model loaded successfully")


def handler(job):
    """HuggingFace inference handler."""
    job_input = job["input"]

    # Support both chat and completion formats
    if "messages" in job_input:
        prompt = tokenizer.apply_chat_template(
            job_input["messages"],
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        prompt = job_input.get("prompt", "")

    # Generation parameters
    max_tokens = job_input.get("max_tokens", 512)
    temperature = job_input.get("temperature", 0.7)
    top_p = job_input.get("top_p", 0.95)
    top_k = job_input.get("top_k", 50)

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature if temperature > 0 else None,
            top_p=top_p,
            top_k=top_k,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove prompt from response if present
    if response.startswith(prompt):
        response = response[len(prompt):].strip()

    return {
        "response": response,
        "model": MODEL_NAME,
        "usage": {
            "prompt_tokens": len(inputs.input_ids[0]),
            "completion_tokens": len(outputs[0]) - len(inputs.input_ids[0])
        }
    }

runpod.serverless.start({"handler": handler})
```

### Environment Variables for HuggingFace

```python
# Required
HF_TOKEN = "hf_xxx"  # For gated models (Llama, etc.)
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

# Optional performance tuning
MAX_MODEL_LEN = "8192"
GPU_MEMORY_UTILIZATION = "0.95"
TORCH_DTYPE = "float16"  # or bfloat16
DEVICE_MAP = "auto"

# For multi-GPU
CUDA_VISIBLE_DEVICES = "0,1"
```

### Dockerfile for HuggingFace

```dockerfile
FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# Optional: Pre-download model for faster cold starts
ARG HF_TOKEN
ARG MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    AutoTokenizer.from_pretrained('${MODEL_NAME}', token='${HF_TOKEN}'); \
    AutoModelForCausalLM.from_pretrained('${MODEL_NAME}', token='${HF_TOKEN}')"

CMD ["python", "-u", "handler.py"]
```

---

## vLLM Deployment

### vLLM Handler

```python
import runpod
import os
from vllm import LLM, SamplingParams

# Initialize vLLM at startup
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
TENSOR_PARALLEL = int(os.environ.get("TENSOR_PARALLEL_SIZE", 1))
GPU_MEMORY_UTIL = float(os.environ.get("GPU_MEMORY_UTILIZATION", 0.95))
MAX_MODEL_LEN = int(os.environ.get("MAX_MODEL_LEN", 8192))

print(f"Initializing vLLM with {MODEL_NAME}")

llm = LLM(
    model=MODEL_NAME,
    tensor_parallel_size=TENSOR_PARALLEL,
    gpu_memory_utilization=GPU_MEMORY_UTIL,
    max_model_len=MAX_MODEL_LEN,
    trust_remote_code=True
)

print("vLLM engine ready")


def format_chat_messages(messages: list) -> str:
    """Format messages for chat models."""
    formatted = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            formatted += f"<|im_start|>system\n{content}<|im_end|>\n"
        elif role == "user":
            formatted += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == "assistant":
            formatted += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    formatted += "<|im_start|>assistant\n"
    return formatted


def handler(job):
    """vLLM inference handler with OpenAI-compatible interface."""
    job_input = job["input"]

    # Get prompt
    if "messages" in job_input:
        prompt = format_chat_messages(job_input["messages"])
    else:
        prompt = job_input.get("prompt", "")

    # Sampling parameters
    sampling_params = SamplingParams(
        max_tokens=job_input.get("max_tokens", 512),
        temperature=job_input.get("temperature", 0.7),
        top_p=job_input.get("top_p", 0.95),
        top_k=job_input.get("top_k", -1),
        presence_penalty=job_input.get("presence_penalty", 0),
        frequency_penalty=job_input.get("frequency_penalty", 0),
        stop=job_input.get("stop", None)
    )

    # Generate
    outputs = llm.generate([prompt], sampling_params)
    response = outputs[0].outputs[0].text

    # OpenAI-compatible response format
    return {
        "id": f"chatcmpl-{job['id']}",
        "object": "chat.completion",
        "model": MODEL_NAME,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": outputs[0].outputs[0].finish_reason
        }],
        "usage": {
            "prompt_tokens": len(outputs[0].prompt_token_ids),
            "completion_tokens": len(outputs[0].outputs[0].token_ids),
            "total_tokens": len(outputs[0].prompt_token_ids) + len(outputs[0].outputs[0].token_ids)
        }
    }

runpod.serverless.start({"handler": handler})
```

### vLLM with Streaming

```python
import runpod
from vllm import LLM, SamplingParams

llm = LLM(model=os.environ["MODEL_NAME"])


def handler(job):
    """Streaming vLLM handler."""
    job_input = job["input"]
    prompt = job_input.get("prompt", "")

    sampling_params = SamplingParams(
        max_tokens=job_input.get("max_tokens", 512),
        temperature=job_input.get("temperature", 0.7)
    )

    def stream_generator():
        for output in llm.generate([prompt], sampling_params, use_tqdm=False):
            for o in output.outputs:
                yield {
                    "token": o.text,
                    "finished": o.finish_reason is not None
                }

    return stream_generator()

runpod.serverless.start({
    "handler": handler,
    "return_aggregate_stream": True
})
```

### vLLM Environment Variables

```bash
# Model
MODEL_NAME=meta-llama/Llama-3.1-70B-Instruct
HF_TOKEN=hf_xxx

# Multi-GPU (tensor parallelism)
TENSOR_PARALLEL_SIZE=2

# Performance
MAX_MODEL_LEN=16384
GPU_MEMORY_UTILIZATION=0.95

# Quantization
QUANTIZATION=awq  # awq, gptq, or omit for none

# Troubleshooting
ENFORCE_EAGER=false  # Set to true if CUDA graph issues
VLLM_ATTENTION_BACKEND=FLASH_ATTN  # or XFORMERS

# Logging
VLLM_LOGGING_LEVEL=INFO
```

---

## Text Generation Inference (TGI)

### TGI Docker Deployment

```dockerfile
FROM ghcr.io/huggingface/text-generation-inference:latest

ENV MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
ENV HUGGING_FACE_HUB_TOKEN=hf_xxx
ENV MAX_INPUT_LENGTH=4096
ENV MAX_TOTAL_TOKENS=8192
ENV MAX_BATCH_PREFILL_TOKENS=4096
ENV PORT=80

CMD ["--model-id", "${MODEL_ID}"]
```

### TGI Client Handler

```python
import runpod
import aiohttp
import os

TGI_URL = os.environ.get("TGI_URL", "http://localhost:80")


async def handler(job):
    """Handler for TGI backend."""
    job_input = job["input"]

    payload = {
        "inputs": job_input.get("prompt", ""),
        "parameters": {
            "max_new_tokens": job_input.get("max_tokens", 512),
            "temperature": job_input.get("temperature", 0.7),
            "top_p": job_input.get("top_p", 0.95),
            "do_sample": job_input.get("temperature", 0.7) > 0,
            "return_full_text": False
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{TGI_URL}/generate", json=payload) as response:
            result = await response.json()

    return {
        "response": result["generated_text"],
        "details": result.get("details", {})
    }

runpod.serverless.start({"handler": handler})
```

---

## Embedding Models

### Sentence Transformers

```python
import runpod
import os
import torch
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.environ.get("MODEL_NAME", "all-MiniLM-L6-v2")

print(f"Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")
print("Embedding model ready")


def handler(job):
    """Embedding generation handler."""
    job_input = job["input"]

    # Support single text or batch
    texts = job_input.get("texts", [])
    if isinstance(texts, str):
        texts = [texts]

    # Single text alternative
    if not texts and "text" in job_input:
        texts = [job_input["text"]]

    if not texts:
        return {"error": "No texts provided", "status": "FAILED"}

    # Generate embeddings
    embeddings = model.encode(
        texts,
        batch_size=job_input.get("batch_size", 32),
        normalize_embeddings=job_input.get("normalize", True),
        convert_to_numpy=True
    )

    return {
        "embeddings": embeddings.tolist(),
        "model": MODEL_NAME,
        "dimensions": embeddings.shape[1],
        "count": len(embeddings)
    }

runpod.serverless.start({"handler": handler})
```

### BGE/E5 Embeddings

```python
import runpod
import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = os.environ.get("MODEL_NAME", "BAAI/bge-large-en-v1.5")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to("cuda")
model.eval()


def mean_pooling(model_output, attention_mask):
    """Mean pooling for embeddings."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def handler(job):
    """BGE embedding handler."""
    job_input = job["input"]
    texts = job_input.get("texts", [])

    # Add instruction prefix for BGE
    instruction = job_input.get("instruction", "Represent this sentence for retrieval: ")
    texts = [instruction + t for t in texts]

    # Tokenize
    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).to("cuda")

    # Generate embeddings
    with torch.no_grad():
        outputs = model(**encoded)
        embeddings = mean_pooling(outputs, encoded["attention_mask"])

        # Normalize
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    return {
        "embeddings": embeddings.cpu().numpy().tolist(),
        "model": MODEL_NAME
    }

runpod.serverless.start({"handler": handler})
```

---

## Vision Models

### LLaVA / Vision-Language Models

```python
import runpod
import torch
import base64
from io import BytesIO
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration

MODEL_NAME = os.environ.get("MODEL_NAME", "llava-hf/llava-1.5-7b-hf")

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = LlavaForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)


def decode_image(image_data: str) -> Image.Image:
    """Decode base64 image."""
    if image_data.startswith("data:"):
        image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    return Image.open(BytesIO(image_bytes))


def handler(job):
    """Vision-language model handler."""
    job_input = job["input"]

    image = decode_image(job_input["image"])
    prompt = job_input.get("prompt", "Describe this image.")

    # Format prompt for LLaVA
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt}
            ]
        }
    ]

    text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text_prompt, image, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=job_input.get("max_tokens", 512),
            do_sample=False
        )

    response = processor.decode(output[0], skip_special_tokens=True)

    return {"response": response}

runpod.serverless.start({"handler": handler})
```

### Document Processing (Florence-2)

```python
import runpod
import torch
import base64
from io import BytesIO
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

MODEL_NAME = "microsoft/Florence-2-large"

processor = AutoProcessor.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)


def decode_image(image_data: str) -> Image.Image:
    if image_data.startswith("data:"):
        image_data = image_data.split(",")[1]
    return Image.open(BytesIO(base64.b64decode(image_data)))


def handler(job):
    """Florence-2 document processing handler."""
    job_input = job["input"]

    image = decode_image(job_input["image"])
    task = job_input.get("task", "OCR")

    # Task prompts
    task_prompts = {
        "OCR": "<OCR>",
        "OCR_WITH_REGION": "<OCR_WITH_REGION>",
        "CAPTION": "<CAPTION>",
        "DETAILED_CAPTION": "<DETAILED_CAPTION>",
        "MORE_DETAILED_CAPTION": "<MORE_DETAILED_CAPTION>",
        "OD": "<OD>",
        "DENSE_REGION_CAPTION": "<DENSE_REGION_CAPTION>",
    }

    prompt = task_prompts.get(task, "<OCR>")

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device, torch.float16)

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3
        )

    result = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Parse structured output
    parsed = processor.post_process_generation(
        result,
        task=prompt,
        image_size=(image.width, image.height)
    )

    return {
        "task": task,
        "raw_output": result,
        "parsed": parsed
    }

runpod.serverless.start({"handler": handler})
```

---

## Audio/Voice Models

### Whisper (Speech-to-Text)

```python
import runpod
import torch
import base64
import io
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

MODEL_NAME = os.environ.get("MODEL_NAME", "openai/whisper-large-v3")

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    device_map="auto",
    torch_dtype=torch.float16
)


def handler(job):
    """Whisper transcription handler."""
    job_input = job["input"]

    # Decode audio
    audio_b64 = job_input["audio"]
    audio_bytes = base64.b64decode(audio_b64)

    # Transcribe
    result = pipe(
        io.BytesIO(audio_bytes),
        return_timestamps=job_input.get("timestamps", False),
        generate_kwargs={
            "language": job_input.get("language"),
            "task": job_input.get("task", "transcribe")  # or "translate"
        }
    )

    return {
        "text": result["text"],
        "chunks": result.get("chunks", [])
    }

runpod.serverless.start({"handler": handler})
```

### XTTS (Text-to-Speech)

```python
import runpod
import torch
import base64
import io
from TTS.api import TTS

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

print(f"Loading TTS model: {MODEL_NAME}")
tts = TTS(MODEL_NAME).to("cuda")
print("TTS model ready")


def handler(job):
    """XTTS voice synthesis handler."""
    job_input = job["input"]

    text = job_input["text"]
    language = job_input.get("language", "en")
    speaker_wav = job_input.get("speaker_wav")  # Base64 reference audio

    if speaker_wav:
        # Voice cloning
        ref_audio = base64.b64decode(speaker_wav)
        ref_path = "/tmp/reference.wav"
        with open(ref_path, "wb") as f:
            f.write(ref_audio)

        wav = tts.tts(
            text=text,
            speaker_wav=ref_path,
            language=language
        )
    else:
        # Default voice
        wav = tts.tts(text=text, language=language)

    # Convert to bytes
    buffer = io.BytesIO()
    import soundfile as sf
    sf.write(buffer, wav, 24000, format="WAV")
    audio_b64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "audio": audio_b64,
        "format": "wav",
        "sample_rate": 24000
    }

runpod.serverless.start({"handler": handler})
```

---

## Model Caching

### Using Network Volumes

```python
import os
from huggingface_hub import snapshot_download

VOLUME_PATH = "/runpod-volume"
MODEL_CACHE = f"{VOLUME_PATH}/models"

def ensure_model_cached(model_name: str) -> str:
    """Download model to network volume if not cached."""
    model_path = os.path.join(MODEL_CACHE, model_name.replace("/", "_"))

    if os.path.exists(model_path):
        print(f"Model cached at {model_path}")
        return model_path

    print(f"Downloading model to {model_path}")
    snapshot_download(
        model_name,
        local_dir=model_path,
        token=os.environ.get("HF_TOKEN")
    )

    return model_path


# Use cached path
model_path = ensure_model_cached("meta-llama/Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained(model_path)
```

### Pre-warming Models

```python
def prewarm_model():
    """Run dummy inference to warm up model."""
    print("Pre-warming model...")

    dummy_input = "Hello"
    inputs = tokenizer(dummy_input, return_tensors="pt").to(model.device)

    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=1)

    print("Model warmed up")


# Call after loading
prewarm_model()
```
