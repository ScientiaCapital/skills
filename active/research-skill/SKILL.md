---
name: research-skill
description: |
  Comprehensive research framework for market intelligence, technical evaluations,
  and documentation discovery. Use when researching companies, analyzing competitors,
  evaluating frameworks, comparing APIs, or making technology decisions.
  Triggers: "research this company", "analyze competitors", "evaluate this framework",
  "compare these tools", "should we use X", "LLM provider comparison", "API assessment",
  "find market opportunities", "assess market size", "tech stack decision", "MCP discovery".
  Respects NO OpenAI constraint - uses Claude, DeepSeek, Gemini.
---

# Research Skill

Comprehensive research framework combining market intelligence and technical evaluation.

## Quick Reference

| Research Type | Output | When to Use | Reference |
|---------------|--------|-------------|-----------|
| Company Profile | Structured profile | Before outreach, call prep | `reference/market.md` |
| Competitive Intel | Market position, pricing | Deal strategy | `reference/market.md` |
| Tech Stack Discovery | Software + integrations | Lead qualification | `reference/market.md` |
| Framework Evaluation | Feature comparison + rec | Tech decisions | `reference/technical.md` |
| LLM Comparison | Cost/capability matrix | Provider selection | `reference/technical.md` |
| API Assessment | Limits, pricing, DX | Integration planning | `reference/technical.md` |
| MCP Discovery | Available servers/tools | Capability expansion | `reference/technical.md` |

---

## Part 1: Market Research

### Company Profile Framework

```python
company_profile = {
    # Basics
    'name': str,
    'website': str,
    'industry': str,
    'employee_count': int,
    'revenue_estimate': str,  # "$5-10M", "$10-50M"

    # Operations
    'field_vs_office': {'field': int, 'office': int},
    'service_area': list[str],  # States/regions
    'trades': list[str],  # Electrical, HVAC, Plumbing

    # Technology
    'software_stack': {
        'crm': str,
        'project_mgmt': str,
        'accounting': str,
        'field_service': str,
        'other': list[str]
    },

    # Sales Intel
    'pain_signals': list[str],
    'growth_indicators': list[str],
    'failed_implementations': list[str],
    'decision_makers': list[dict]
}
```

### Pain Signal Detection

| Signal | Indicates | Priority |
|--------|-----------|----------|
| Multiple systems mentioned | Integration pain | HIGH |
| "Growing fast" in news | Scaling challenges | HIGH |
| Recent leadership change | Open to new vendors | MEDIUM |
| Hiring ops/admin roles | Process problems | MEDIUM |
| Bad software reviews | Ready to switch | HIGH |
| No online presence | Not tech-savvy | LOW |

### Market Research Workflow

```
Step 1: Basic Discovery
└── Website, LinkedIn, Google News, Glassdoor

Step 2: Tech Stack
└── Job postings, integrations page, case studies

Step 3: Pain Signals
└── Reviews, social mentions, forum posts

Step 4: Decision Makers
└── LinkedIn Sales Nav, company about page

Step 5: Synthesize
└── Generate company profile, score against ICP
```

### Competitive Positioning

When researching competitors for a prospect:

```
1. What are they using now?
2. How long have they used it?
3. What's broken? (Check reviews, Reddit, forums)
4. What would make them switch?
5. Who else are they evaluating?
```

---

## Part 2: Technical Research

### Stack Constraints (Tim's Environment)

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

### LLM Selection Matrix

| Use Case | Primary | Fallback | Cost/1M tokens |
|----------|---------|----------|----------------|
| Complex reasoning | Claude Sonnet | Gemini Pro | $3-15 |
| Bulk processing | DeepSeek V3 | Qwen 2.5 | $0.14-0.27 |
| Code generation | Claude Sonnet | DeepSeek Coder | $3-15 |
| Embeddings | Voyage | Cohere | $0.10-0.13 |
| Vision | Claude/Gemini | Qwen VL | $3-15 |
| Local/Private | Ollama Qwen | Ollama Llama | Free |

**Cost Optimization Rule:** Use Chinese LLMs (DeepSeek, Qwen) for 90%+ cost savings on bulk/routine tasks. Reserve Claude/Gemini for complex reasoning.

### Framework Evaluation Checklist

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

### API Evaluation Template

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

### Technical Research Workflow

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

### MCP Discovery Workflow

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

---

## Part 3: Combined Research Outputs

### Research Report Template

```yaml
research_report:
  title: ""
  type: ""  # market, technical, hybrid
  date: ""
  researcher: ""

  # Executive Summary
  summary:
    question: ""
    answer: ""
    confidence: ""  # high, medium, low

  # Findings
  market_findings:
    companies_analyzed: []
    competitive_landscape: ""
    market_size: ""
    trends: []

  technical_findings:
    frameworks_evaluated: []
    recommended_stack: {}
    integration_considerations: []
    cost_analysis: {}

  # Recommendations
  recommendations:
    primary: ""
    alternatives: []
    risks: []
    next_steps: []

  # Sources
  sources:
    - type: ""
      url: ""
      date_accessed: ""
      key_findings: []
```

### Decision Matrix Template

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| [Criterion 1] | 25% | /10 | /10 | /10 |
| [Criterion 2] | 20% | /10 | /10 | /10 |
| [Criterion 3] | 20% | /10 | /10 | /10 |
| [Criterion 4] | 20% | /10 | /10 | /10 |
| [Criterion 5] | 15% | /10 | /10 | /10 |
| **Weighted Total** | 100% | **/10** | **/10** | **/10** |

---

## Integration Notes

### Market Research
- **Feeds into:** dealer-scraper (enrichment), sales-agent (qualification)
- **Data sources:** LinkedIn, Glassdoor, Indeed, G2, Capterra, Google
- **Pairs with:** sales-outreach-skill (messaging), opportunity-evaluator-skill (deals)

### Technical Research
- **References:** AI_MODEL_SELECTION_GUIDE.md, runpod-deployment-skill
- **Projects:** ai-cost-optimizer, mcp-server-cookbook
- **Tools:** Context7 MCP for docs, HuggingFace MCP for models
- **Pairs with:** opportunity-evaluator-skill (build vs partner decisions)

---

## Reference Files

### Market Research
- `reference/market.md` - Company profiles, tech stack discovery, ICP, competitive analysis

### Technical Research
- `reference/technical.md` - Framework comparison, LLM evaluation, API patterns, MCP discovery
