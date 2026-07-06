---
name: "research"
description: "Structured research reports for GTM and tech decisions: company/competitor profiles, tech-stack discovery, framework/LLM/API evaluations, decision matrices with confidence scores. Use when: research a company before a call, competitive analysis, evaluate a framework or LLM, tech-stack decision, build-vs-buy. For Epiphan account prep prefer sales_brief/identify_company; for lead ICP scoring use qualify_lead."
---

<objective>
Comprehensive research framework combining market intelligence (company profiles, competitive analysis, tech stack discovery) and technical evaluation (framework comparisons, LLM selection, API assessment). Produces structured reports with confidence scores and actionable recommendations.
</objective>

<quick_start>
**Market research:**
1. Basic discovery: Website, LinkedIn, Google News
2. Tech stack: Job postings, integrations page
3. Pain signals: Reviews, social mentions
4. Decision makers: LinkedIn, about page

**Technical research:**
1. Define: Problem, requirements, constraints
2. Discover: GitHub, HuggingFace, Context7 docs
3. Evaluate: Apply framework checklist, test minimal example
4. Decide: Build vs buy, document rationale

**Output:** Research report with question, answer, confidence, sources
</quick_start>

<success_criteria>
Research is successful when:
- Question clearly defined with constraints documented
- Multiple sources consulted (not just one)
- Confidence level assigned (high/medium/low) with rationale
- Recommendations are specific and actionable
- Decision matrix used for multi-option comparisons
- NO OPENAI constraint respected for technical research
- Sources documented with access dates
</success_criteria>

<core_content>
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

### Epiphan-Native Tool Order (Required First Pass)

Before touching generic web sources, run the Epiphan-native MCP tools in this order. They cover
CRM history, device install base, and Clari deal context that no web search can see — generic
sources (LinkedIn, Glassdoor, G2, Google, etc.) are for filling gaps these tools don't cover.

```
1. identify_company        # Fuzzy-match the target to CRM + HubSpot company record
2. sales_brief              # Full pre-call briefing: device history, Clari, engagement timeline
3. activity_get_timeline    # Contact/company/rep activity timeline (recency, cadence, gaps)
4. enrich_contact           # Fill decision-maker + firmographic gaps on named contacts
   |__ only fall back to LinkedIn/Glassdoor/Indeed/G2/Capterra/Google for what's still missing
```

If the target isn't an existing Epiphan account/contact (e.g. pure competitor or tech-stack
research with no CRM record), skip straight to generic discovery below and note the skip reason
in the report's `sources` section.

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
└── hubspot_find_contacts_by_role (Epiphan-native first), then LinkedIn Sales Nav, company about page

Step 5: Synthesize
└── Generate company profile; score against ICP via qualify_lead (house source of truth —
    do not re-implement ICP scoring manually)
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
    local: ollama  # see Tim's current machine spec in CLAUDE.md, not hardcoded here

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
   └── ~/Desktop/tk_projects/mcp-server-cookbook/  (Tim's home dir — verify with `echo ~` if unsure)

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
  delivery: ""  # where this report is handed off: HubSpot note on the company/deal record,
                # artifact (chat), or doc — pick one per Integration Notes below

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
- **Data sources (in order):** Epiphan-native first — `identify_company`, `sales_brief`,
  `activity_get_timeline`, `enrich_contact`, `qualify_lead`, `hubspot_find_contacts_by_role`,
  `hubspot_search_companies`, `search_product_catalog` — then generic web (LinkedIn, Glassdoor,
  Indeed, G2, Capterra, Google) to fill remaining gaps
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

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-research.json`:
```json
{"ts":"[UTC ISO8601]","skill":"research","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"sources_consulted":[n],"findings_synthesized":[n],"recommendations":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
