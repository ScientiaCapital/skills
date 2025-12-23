# LLM Evaluation Checklist

## Provider Evaluation Template

```yaml
provider:
  name: ""
  website: ""
  api_docs: ""
  status_page: ""
  
models_available:
  - name: ""
    context_window: 0
    input_cost_per_1m: 0.00
    output_cost_per_1m: 0.00
    
access:
  signup_process: ""  # instant, waitlist, enterprise
  api_key_type: ""  # simple key, OAuth, etc.
  rate_limits: ""
  
evaluated_date: ""
verdict: ""  # USE, MAYBE, SKIP
```

---

## Tim's Approved Providers

### Tier 1: Primary (Use Freely)

| Provider | Best For | Access Via |
|----------|----------|------------|
| Anthropic | Complex reasoning, code | Direct API |
| Google | Multimodal, long context | Direct API |
| OpenRouter | Cost optimization | API gateway |

### Tier 2: Specialized (Use Cases)

| Provider | Best For | Access Via |
|----------|----------|------------|
| DeepSeek | Bulk processing, code | OpenRouter |
| Qwen | Chinese content, cost | OpenRouter |
| Voyage | Embeddings | Direct API |
| Cohere | Embeddings, rerank | Direct API |

### Tier 3: Local (Privacy/Cost)

| Provider | Best For | Access Via |
|----------|----------|------------|
| Ollama | Development, private | Local |
| LM Studio | Testing | Local |

### Forbidden

| Provider | Reason |
|----------|--------|
| OpenAI | Policy decision |
| Azure OpenAI | Same |

---

## Cost Analysis Framework

### Cost Per Task Type

```yaml
task_costs:
  simple_classification:
    tokens_typical: 500
    best_model: "deepseek-chat"
    cost_per_1000_tasks: "$0.07"
    
  summarization:
    tokens_typical: 2000
    best_model: "deepseek-chat"
    cost_per_1000_tasks: "$0.28"
    
  complex_reasoning:
    tokens_typical: 4000
    best_model: "claude-sonnet"
    cost_per_1000_tasks: "$12.00"
    
  code_generation:
    tokens_typical: 3000
    best_model: "claude-sonnet"
    cost_per_1000_tasks: "$9.00"
    
  embeddings:
    tokens_typical: 500
    best_model: "voyage-3"
    cost_per_1000_tasks: "$0.05"
```

### Monthly Cost Projection

```python
def estimate_monthly_cost(tasks: dict) -> float:
    """
    tasks = {
        'simple_classification': 10000,
        'summarization': 5000,
        'complex_reasoning': 1000,
        'code_generation': 500,
        'embeddings': 50000
    }
    """
    rates = {
        'simple_classification': 0.00007,
        'summarization': 0.00028,
        'complex_reasoning': 0.012,
        'code_generation': 0.009,
        'embeddings': 0.00005
    }
    return sum(tasks[k] * rates[k] for k in tasks)
```

---

## Capability Evaluation

### Reasoning Quality Test

```yaml
test_prompts:
  logic:
    prompt: "If all A are B, and all B are C, what can we conclude about A and C?"
    expected: "All A are C (transitive property)"
    
  math:
    prompt: "What is 17 * 23? Show your work."
    expected: "391 with clear steps"
    
  code:
    prompt: "Write a Python function to find the nth Fibonacci number using memoization."
    expected: "Correct implementation with @lru_cache or manual memo dict"
    
  analysis:
    prompt: "Given [complex scenario], what are the trade-offs?"
    expected: "Structured analysis with multiple perspectives"
```

### Instruction Following Test

```yaml
tests:
  format_compliance:
    prompt: "Respond in JSON format with keys: name, age, city"
    check: "Valid JSON, correct keys"
    
  length_control:
    prompt: "Explain X in exactly 3 sentences."
    check: "Exactly 3 sentences"
    
  constraint_respect:
    prompt: "List 5 items, no more, no less"
    check: "Exactly 5 items"
```

---

## Integration Checklist

### API Quality

- [ ] REST API available
- [ ] Python SDK official/maintained
- [ ] Streaming support
- [ ] Function calling / tools
- [ ] JSON mode
- [ ] Batch API available

### Reliability

- [ ] Status page exists
- [ ] SLA published
- [ ] Historical uptime >99%
- [ ] Rate limit headers clear
- [ ] Error messages helpful

### Developer Experience

- [ ] Quick start guide
- [ ] API playground
- [ ] SDK well-typed
- [ ] Examples in docs
- [ ] Active Discord/support

---

## Model Selection Decision Tree

```
START: What's the task?
│
├─► Complex reasoning / Analysis
│   └─► Claude Sonnet (or Gemini Pro)
│
├─► Code generation / Review
│   └─► Claude Sonnet (or DeepSeek Coder)
│
├─► Bulk text processing
│   └─► Is accuracy critical?
│       ├─► Yes → Claude Haiku
│       └─► No → DeepSeek V3
│
├─► Embeddings
│   └─► Voyage-3 (or Cohere)
│
├─► Multimodal (images)
│   └─► Claude Sonnet or Gemini Pro
│
├─► Long context (>100k)
│   └─► Gemini Pro (1M context)
│
├─► Local / Private
│   └─► Ollama + Qwen 2.5
│
└─► Cost is primary concern
    └─► DeepSeek V3 via OpenRouter
```

---

## Benchmark Template

```yaml
benchmark:
  name: ""
  date: ""
  
  test_set:
    description: ""
    sample_size: 0
    source: ""
    
  models_tested:
    - name: ""
      version: ""
      
  metrics:
    accuracy: 0.0
    latency_p50_ms: 0
    latency_p95_ms: 0
    cost_per_100: 0.00
    
  results:
    model_a:
      accuracy: 0.0
      latency: 0
      cost: 0.00
    model_b:
      accuracy: 0.0
      latency: 0
      cost: 0.00
      
  winner: ""
  notes: ""
```

---

## Provider Deep Dives

### Anthropic (Claude)

```yaml
strengths:
  - Best reasoning quality
  - Excellent instruction following
  - Strong code generation
  - Good at saying "I don't know"
  
weaknesses:
  - Higher cost than Chinese LLMs
  - No fine-tuning (yet)
  - Rate limits can be tight
  
best_for:
  - Complex analysis
  - Code review/generation
  - Agentic workflows
  - Customer-facing applications
  
cost_optimization:
  - Use Haiku for simple tasks
  - Batch API for bulk (50% off)
  - Cache system prompts
```

### DeepSeek (via OpenRouter)

```yaml
strengths:
  - 90%+ cost savings vs Claude
  - Good code generation
  - Fast inference
  - Generous rate limits
  
weaknesses:
  - Slightly lower reasoning
  - Less reliable on edge cases
  - Smaller context window
  
best_for:
  - Bulk processing
  - Code generation (routine)
  - Classification tasks
  - Cost-sensitive pipelines
  
cost_optimization:
  - Already cheap
  - Use V3 for quality/cost balance
```

### Google (Gemini)

```yaml
strengths:
  - Massive context (1M tokens)
  - Strong multimodal
  - Good reasoning
  - Competitive pricing
  
weaknesses:
  - API can be flaky
  - SDK less mature than Anthropic
  - Safety filters aggressive
  
best_for:
  - Long document analysis
  - Multimodal tasks
  - When 200k context isn't enough
  
cost_optimization:
  - Use Flash for simple tasks
  - Pro for complex reasoning
```
