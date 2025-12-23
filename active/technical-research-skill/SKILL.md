---
name: technical-research-skill
version: 1.0.0
description: |
  Framework comparisons, API evaluations, and implementation pattern research.
  Use when evaluating technologies, comparing frameworks, or planning integrations.
  Triggers: "evaluate this framework", "compare these tools", "should we use X",
  "LLM provider comparison", "API assessment", "MCP server research", "tech stack decision".
  Respects NO OpenAI constraint - uses Claude, DeepSeek, Gemini.
---

# Technical Research Skill

Systematic evaluation of frameworks, APIs, and implementation patterns.

## Quick Reference

| Research Type | Output | When to Use |
|---------------|--------|-------------|
| LLM Comparison | Cost/capability matrix | Provider selection |
| Framework Eval | Feature comparison + rec | Tech decisions |
| API Assessment | Limits, pricing, DX | Integration planning |
| MCP Discovery | Available servers/tools | Capability expansion |
| Pattern Research | Implementation examples | Before building |

## Stack Constraints (Tim's Environment)

```yaml
constraints:
  llm_providers:
    preferred:
      - anthropic  # Claude - primary
      - google     # Gemini - multimodal
      - openrouter # DeepSeek, Qwen, Yi - cost optimization
    forbidden:
      - openai     # NO OpenAI
      
  infrastructure:
    compute: runpod_serverless
    database: supabase
    hosting: vercel
    local: ollama  # M1 Mac compatible
    
  frameworks:
    preferred:
      - langgraph  # Over langchain
      - fastmcp    # For MCP servers
      - pydantic   # Data validation
    avoid:
      - langchain  # Too abstracted
      - autogen    # Complexity
      
  development:
    machine: m1_mac
    ide: cursor, claude_code
    version_control: github
```

## LLM Selection Matrix

| Use Case | Primary | Fallback | Cost/1M tokens |
|----------|---------|----------|----------------|
| Complex reasoning | Claude Sonnet | Gemini Pro | $3-15 |
| Bulk processing | DeepSeek V3 | Qwen 2.5 | $0.14-0.27 |
| Code generation | Claude Sonnet | DeepSeek Coder | $3-15 |
| Embeddings | Voyage | Cohere | $0.10-0.13 |
| Vision | Claude/Gemini | Qwen VL | $3-15 |
| Local/Private | Ollama Qwen | Ollama Llama | Free |

**Cost Optimization Rule:** Use Chinese LLMs (DeepSeek, Qwen) for 90%+ cost savings on bulk/routine tasks. Reserve Claude/Gemini for complex reasoning.

## Framework Evaluation Checklist

```markdown
## [Framework Name] Evaluation

### Basic Info
- [ ] GitHub stars / activity
- [ ] Last commit date
- [ ] Maintainer reputation
- [ ] License type
- [ ] Documentation quality

### Technical Fit
- [ ] Python 3.11+ compatible
- [ ] M1 Mac compatible
- [ ] Async support
- [ ] Type hints / Pydantic
- [ ] MCP integration possible

### Ecosystem
- [ ] Active Discord/community
- [ ] Stack Overflow presence
- [ ] Tutorial availability
- [ ] Example projects

### Red Flags
- [ ] OpenAI-only
- [ ] Unmaintained (>6 months)
- [ ] Poor documentation
- [ ] Heavy dependencies
- [ ] Vendor lock-in
```

## API Evaluation Template

```yaml
api_evaluation:
  name: ""
  provider: ""
  documentation_url: ""
  
  access:
    auth_method: ""  # API key, OAuth, etc.
    rate_limits:
      requests_per_minute: 0
      tokens_per_minute: 0
    quotas: ""
    
  pricing:
    model: ""  # per request, per token, subscription
    free_tier: ""
    cost_estimate: ""  # for our use case
    
  developer_experience:
    sdk_quality: ""  # 1-5
    documentation: ""  # 1-5
    error_messages: ""  # 1-5
    response_time: ""  # ms
    
  integration:
    existing_mcps: []
    sdk_languages: []
    webhook_support: bool
    
  verdict: ""  # USE, MAYBE, SKIP
  notes: ""
```

## MCP Discovery Workflow

```python
# When looking for MCP capabilities:

1. Check mcp-server-cookbook first
   └── /Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook/

2. Search official MCP servers
   └── github.com/modelcontextprotocol/servers

3. Search community servers
   └── github.com search: "mcp server" + [capability]

4. Check if FastMCP wrapper exists
   └── Can we build it quickly?

5. Evaluate build vs. use existing
   └── Time to integrate vs. time to build
```

## Research Workflow

```
┌─────────────────────────────────────────────┐
│ 1. DEFINE                                    │
│    What problem are we solving?              │
│    What are the requirements?                │
│    What are the constraints?                 │
└─────────────────┬───────────────────────────┘
                  ▼
┌─────────────────────────────────────────────┐
│ 2. DISCOVER                                  │
│    Search GitHub, HuggingFace, blogs         │
│    Check Context7 for docs                   │
│    Review existing tk_projects               │
└─────────────────┬───────────────────────────┘
                  ▼
┌─────────────────────────────────────────────┐
│ 3. EVALUATE                                  │
│    Apply checklist above                     │
│    Test minimal example                      │
│    Check M1 compatibility                    │
└─────────────────┬───────────────────────────┘
                  ▼
┌─────────────────────────────────────────────┐
│ 4. DECIDE                                    │
│    Build vs buy vs skip                      │
│    Document decision rationale               │
│    Update AI_MODEL_SELECTION_GUIDE if LLM    │
└─────────────────────────────────────────────┘
```

## Integration Notes

- **References:** AI_MODEL_SELECTION_GUIDE.md, runpod-deployment-skill
- **Projects:** ai-cost-optimizer, mcp-server-cookbook
- **Tools:** Context7 MCP for docs, HuggingFace MCP for models
- **Pairs with:** opportunity-evaluator-skill (build vs partner decisions)

## Reference Files

- `reference/framework-comparison.md` - Side-by-side evaluation template
- `reference/llm-evaluation-checklist.md` - Deep LLM provider analysis
- `reference/api-integration-patterns.md` - Common integration approaches
- `reference/mcp-discovery.md` - Finding and evaluating MCP servers
