# Multimodal Support with OpenRouter

Vision, PDF, and document analysis with Chinese LLMs through OpenRouter.

## Vision Models

| Model | Vision | PDF | Multi-Image | Best For |
|-------|--------|-----|-------------|----------|
| `qwen/qwen-2-vl-72b-instruct` | ✅ | ✅ | ✅ | Charts, documents, general |
| `qwen/qwen3-vl-30b` | ✅ | ✅ | ✅ | Cost-effective vision |
| `qwen/qwen-vl-max` | ✅ | ✅ | ✅ | Highest quality |
| `deepseek/deepseek-vl` | ✅ | ⚠️ | ✅ | Technical images |

---

## Basic Image Analysis

### From URL

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

llm = ChatOpenAI(
    model="qwen/qwen-2-vl-72b-instruct",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": "Describe this image in detail"},
        {
            "type": "image_url",
            "image_url": {"url": "https://example.com/image.jpg"}
        }
    ])
])

print(response.content)
```

### From Base64

```python
import base64
from pathlib import Path

def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_image_media_type(path: str) -> str:
    """Get MIME type from file extension."""
    ext = Path(path).suffix.lower()
    types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return types.get(ext, "image/png")

# Analyze local image
image_path = "chart.png"
image_data = encode_image(image_path)
media_type = get_image_media_type(image_path)

response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": "What does this chart show?"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:{media_type};base64,{image_data}"}
        }
    ])
])
```

---

## Chart and Graph Analysis

### Stock Chart Analysis

```python
CHART_ANALYSIS_PROMPT = """Analyze this financial chart and provide:

1. **Trend Direction**: Is the overall trend bullish, bearish, or sideways?
2. **Key Levels**: Identify support and resistance levels
3. **Patterns**: Any recognizable chart patterns (head & shoulders, triangles, etc.)
4. **Indicators**: If visible, interpret any technical indicators
5. **Volume**: Comment on volume trends if shown

Be specific with price levels when visible."""

response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": CHART_ANALYSIS_PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{chart_data}"}}
    ])
])
```

### Data Visualization Analysis

```python
DATA_VIZ_PROMPT = """Analyze this data visualization:

1. **Chart Type**: What type of chart is this?
2. **Main Message**: What story is this data telling?
3. **Key Insights**: List the 3-5 most important takeaways
4. **Anomalies**: Any outliers or unusual patterns?
5. **Data Quality**: Any concerns about the visualization?

Extract any visible numbers, percentages, or specific values."""

response = llm.invoke([
    HumanMessage(content=[
        {"type": "text", "text": DATA_VIZ_PROMPT},
        {"type": "image_url", "image_url": {"url": chart_url}}
    ])
])
```

---

## Multi-Image Analysis

Compare or analyze multiple images in one request:

```python
def analyze_multiple_images(images: list[str], prompt: str) -> str:
    """Analyze multiple images together.

    Args:
        images: List of image URLs or base64 strings
        prompt: Analysis prompt
    """
    content = [{"type": "text", "text": prompt}]

    for i, image in enumerate(images, 1):
        # Determine if URL or base64
        if image.startswith("http"):
            content.append({
                "type": "image_url",
                "image_url": {"url": image}
            })
        else:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image}"}
            })

    response = llm.invoke([HumanMessage(content=content)])
    return response.content


# Compare two charts
result = analyze_multiple_images(
    images=[chart1_url, chart2_url],
    prompt="Compare these two charts. What are the key differences in the trends shown?"
)
```

---

## PDF Analysis

### Using Vision Model for PDFs

```python
import fitz  # PyMuPDF
import base64
from io import BytesIO
from PIL import Image

def pdf_to_images(pdf_path: str, dpi: int = 150) -> list[str]:
    """Convert PDF pages to base64 images."""
    doc = fitz.open(pdf_path)
    images = []

    for page in doc:
        # Render page to image
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        images.append(img_base64)

    doc.close()
    return images


def analyze_pdf(pdf_path: str, prompt: str, max_pages: int = 5) -> str:
    """Analyze PDF document using vision model."""
    images = pdf_to_images(pdf_path)[:max_pages]

    content = [{"type": "text", "text": prompt}]
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img}"}
        })

    response = llm.invoke([HumanMessage(content=content)])
    return response.content


# Analyze a PDF report
result = analyze_pdf(
    "quarterly_report.pdf",
    "Summarize this quarterly report. Extract key financial metrics and highlights."
)
```

---

## Document OCR and Extraction

### Table Extraction

```python
TABLE_EXTRACTION_PROMPT = """Extract all tables from this document image.

For each table:
1. Provide the table title/header if visible
2. List all column names
3. Extract all data rows
4. Format as markdown tables

Be precise with numbers and text."""

def extract_tables(image_path: str) -> str:
    """Extract tables from document image."""
    image_data = encode_image(image_path)

    response = llm.invoke([
        HumanMessage(content=[
            {"type": "text", "text": TABLE_EXTRACTION_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
        ])
    ])
    return response.content
```

### Form Field Extraction

```python
from pydantic import BaseModel, Field
from typing import Optional

class FormData(BaseModel):
    """Extracted form data."""
    name: Optional[str] = Field(description="Full name")
    date: Optional[str] = Field(description="Date field")
    address: Optional[str] = Field(description="Address")
    phone: Optional[str] = Field(description="Phone number")
    email: Optional[str] = Field(description="Email address")
    signature_present: bool = Field(description="Whether signature is visible")
    additional_fields: dict = Field(default_factory=dict, description="Other fields")

FORM_EXTRACTION_PROMPT = """Extract all form fields from this document image.

Return a JSON object with these fields:
- name: Full name if present
- date: Any date fields
- address: Address if present
- phone: Phone number if present
- email: Email if present
- signature_present: true/false
- additional_fields: Object with any other labeled fields

Be precise and extract exactly what's visible."""

def extract_form_data(image_path: str) -> FormData:
    """Extract structured data from form image."""
    image_data = encode_image(image_path)

    # Use structured output
    structured_llm = llm.with_structured_output(FormData)

    response = structured_llm.invoke([
        HumanMessage(content=[
            {"type": "text", "text": FORM_EXTRACTION_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
        ])
    ])
    return response
```

---

## Vision + Reasoning Workflow

Combine vision analysis with reasoning:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# Vision model for image analysis
vision_llm = ChatOpenAI(
    model="qwen/qwen-2-vl-72b-instruct",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# Reasoning model for deeper analysis
reasoning_llm = ChatOpenAI(
    model="qwen/qwq-32b",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

def vision_then_reason(image_path: str, question: str) -> str:
    """Two-stage analysis: vision extraction then reasoning."""

    # Stage 1: Extract information from image
    image_data = encode_image(image_path)
    extraction_prompt = """Extract all relevant information from this image.
    Be comprehensive and include all visible text, numbers, and relationships."""

    extraction = vision_llm.invoke([
        HumanMessage(content=[
            {"type": "text", "text": extraction_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
        ])
    ])

    # Stage 2: Reason about the extracted information
    reasoning_prompt = f"""Based on the following extracted information from an image:

{extraction.content}

Please answer this question with detailed reasoning:
{question}

Think step by step and show your work."""

    reasoning = reasoning_llm.invoke(reasoning_prompt)

    return reasoning.content


# Example: Analyze a financial chart with deep reasoning
result = vision_then_reason(
    "stock_chart.png",
    "Based on the patterns in this chart, what is the likely price target for the next month?"
)
```

---

## Best Practices

1. **Image Quality**
   - Use high resolution images (min 512px)
   - Ensure text is legible
   - Good contrast for charts

2. **Model Selection**
   - `qwen-2-vl-72b` for general vision tasks
   - `qwen3-vl-30b` for cost-effective analysis
   - Combine with reasoning models for complex analysis

3. **Prompt Engineering**
   - Be specific about what to extract
   - Ask for structured output when needed
   - Request specific formats (markdown tables, JSON)

4. **Cost Optimization**
   - Compress images before encoding
   - Limit PDF pages analyzed
   - Use cheaper models for simple OCR

5. **Error Handling**
   - Validate image format support
   - Handle encoding errors gracefully
   - Check for empty or invalid responses
