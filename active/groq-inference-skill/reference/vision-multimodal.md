# GROQ Vision & Multimodal

Complete guide for GROQ's vision and multimodal capabilities.

---

## Supported Models

| Model | Max Images | Context | Use Case |
|-------|------------|---------|----------|
| `meta-llama/llama-4-scout-17b-16e-instruct` | 5 | 128K | General vision, OCR |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | 5 | 128K | Complex vision reasoning |

---

## Image Input Methods

### Method 1: Base64 Encoding

```python
import base64
from groq import Groq

client = Groq(api_key="gsk_...")

def analyze_image_base64(image_path: str, prompt: str) -> str:
    """Analyze image using base64 encoding"""
    with open(image_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    # Detect mime type
    if image_path.endswith(".png"):
        mime_type = "image/png"
    elif image_path.endswith(".gif"):
        mime_type = "image/gif"
    elif image_path.endswith(".webp"):
        mime_type = "image/webp"
    else:
        mime_type = "image/jpeg"

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}
                }
            ]
        }],
        max_tokens=1024
    )
    return response.choices[0].message.content
```

### Method 2: URL-Based

```python
def analyze_image_url(image_url: str, prompt: str) -> str:
    """Analyze image using URL"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }],
        max_tokens=1024
    )
    return response.choices[0].message.content

# Usage
result = analyze_image_url(
    "https://example.com/image.jpg",
    "What's in this image?"
)
```

---

## Multiple Images

Llama 4 Scout/Maverick support up to 5 images per request:

```python
def analyze_multiple_images(image_urls: list, prompt: str) -> str:
    """Analyze up to 5 images together"""
    content = [{"type": "text", "text": prompt}]

    for url in image_urls[:5]:  # Max 5 images
        content.append({
            "type": "image_url",
            "image_url": {"url": url}
        })

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": content}],
        max_tokens=1024
    )
    return response.choices[0].message.content

# Compare images
result = analyze_multiple_images(
    ["https://example.com/before.jpg", "https://example.com/after.jpg"],
    "Compare these two images and describe the differences."
)
```

---

## Common Use Cases

### OCR / Text Extraction

```python
def extract_text(image_path: str) -> str:
    """Extract all text from image"""
    return analyze_image_base64(
        image_path,
        "Extract all text from this image. Return only the text content."
    )
```

### Document Analysis

```python
def analyze_document(image_path: str) -> dict:
    """Analyze document and extract structured data"""
    import json

    prompt = """Analyze this document and extract:
    1. Document type
    2. Key fields and values
    3. Any signatures or stamps

    Return as JSON with keys: type, fields, signatures"""

    result = analyze_image_base64(image_path, prompt)
    return json.loads(result)
```

### Chart/Graph Analysis

```python
def analyze_chart(image_path: str) -> str:
    """Analyze chart and extract insights"""
    return analyze_image_base64(
        image_path,
        "Analyze this chart. Describe the data trends, key values, and insights."
    )
```

### Product Image Analysis

```python
def analyze_product(image_url: str) -> str:
    """Analyze product image for e-commerce"""
    return analyze_image_url(
        image_url,
        """Analyze this product image and provide:
        1. Product category
        2. Key features visible
        3. Condition assessment
        4. Suggested keywords for listing"""
    )
```

---

## Multi-Turn Vision Conversations

```python
messages = []

# First turn - analyze image
messages.append({
    "role": "user",
    "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": image_url}}
    ]
})

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=messages
)

messages.append(response.choices[0].message)

# Follow-up turn - no image needed
messages.append({
    "role": "user",
    "content": "Can you describe the colors in more detail?"
})

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=messages
)

print(response.choices[0].message.content)
```

---

## Vision with Tool Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "save_extracted_data",
        "description": "Save extracted data from image",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "category": {"type": "string"}
            },
            "required": ["text"]
        }
    }
}]

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract the receipt items and save them"},
            {"type": "image_url", "image_url": {"url": receipt_url}}
        ]
    }],
    tools=tools,
    tool_choice="auto"
)
```

---

## Best Practices

1. **Image Size**: Keep images under 5MB for optimal performance
2. **Resolution**: Higher resolution = better OCR accuracy
3. **Format**: JPEG, PNG, GIF, WebP supported
4. **Multi-image**: Use when comparing or analyzing related images
5. **Prompting**: Be specific about what to look for in the image

---

## NO OPENAI

```python
from groq import Groq  # Never: from openai import OpenAI
```
