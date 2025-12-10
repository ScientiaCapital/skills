# Sales Multi-Agent Architecture

## 6-Agent System

```python
AGENTS = {
    'RESEARCHER': 'Company intel, tech stack discovery',
    'QUALIFIER': 'ICP fit scoring, budget signals',
    'ENRICHER': 'Contact discovery, org chart',
    'WRITER': 'Personalized sequence generation',
    'ANALYZER': 'Reply intent classification',
    'ROUTER': 'Next-best-action orchestration'
}
```

## Agent Details

### 1. RESEARCHER
**Purpose:** Company intelligence gathering

**Inputs:** Company name, domain, LinkedIn URL

**Outputs:**
- Tech stack (from BuiltWith, Wappalyzer)
- Employee count
- Funding status
- News mentions
- Competitor usage

### 2. QUALIFIER
**Purpose:** ICP fit scoring

**Inputs:** Researched company data

**Outputs:** Qualification score (0-100)

```python
class LeadScorer:
    def score(self, lead: Lead) -> QualificationScore:
        factors = {
            'icp_fit': self._score_icp_fit(lead),       # 0-30
            'intent_signals': self._score_intent(lead),  # 0-25
            'engagement': self._score_engagement(lead),  # 0-20
            'timing': self._score_timing(lead),          # 0-15
            'budget_signals': self._score_budget(lead)   # 0-10
        }
        return QualificationScore(
            total=sum(factors.values()),
            tier=self._assign_tier(sum(factors.values())),
            factors=factors
        )
```

**Tier Thresholds:** 70+ = Hot | 40-69 = Warm | <40 = Nurture

### 3. ENRICHER
**Purpose:** Contact discovery

**Inputs:** Company domain

**Outputs:**
- Decision maker contacts
- Email addresses (verified)
- LinkedIn profiles
- Org chart position

**Sources:** Clearbit, ZoomInfo, Hunter.io, LinkedIn

### 4. WRITER
**Purpose:** Personalized sequence generation

**Inputs:** Enriched lead data, templates

**Outputs:** Multi-step email sequence with personalization

### 5. ANALYZER
**Purpose:** Reply intent classification

**Inputs:** Reply email text

**Outputs:** Intent category + routing decision

### 6. ROUTER
**Purpose:** Orchestration and next-best-action

**Inputs:** Current lead state, agent outputs

**Outputs:** Next action to take

## Cost-Optimized Processing

| Task | Time | Cost | Model |
|------|------|------|-------|
| Qualification | 633ms | $0.000006/lead | Qwen local |
| Enrichment | <3s | $0.0002/lead | DeepSeek |
| Sequence gen | <4s | $0.0002/lead | DeepSeek |

```python
def select_model(complexity: int, cost_limit: float):
    if complexity <= 5:
        return "ollama-qwen"      # Free, local
    elif complexity <= 7:
        return "deepseek-api"     # $0.14/1M tokens
    else:
        return "claude-haiku"     # $0.25/1M tokens
```

## Project Structure

```
sales-agent/
├── agents/           # 6 specialized agents
│   ├── researcher.py
│   ├── qualifier.py
│   ├── enricher.py
│   ├── writer.py
│   ├── analyzer.py
│   └── router.py
├── services/
│   ├── lead_scorer.py
│   └── batch_processor.py
└── api/              # FastAPI endpoints
```

## Full Pipeline Execution

```python
async def execute_gtm_pipeline(leads: list[Lead]):
    for lead in leads:
        # 1. Qualify
        score = await sales_agent.qualify(lead)  # 633ms, $0.000006

        if score.tier == "GOLD":
            # 2. Enrich
            enriched = await sales_agent.enrich(lead)  # <3s

            # 3. Generate sequence
            sequence = await sales_agent.generate_sequence(enriched)

            # 4. Send through cold-reach
            await cold_reach.start_sequence(enriched, sequence)

            # 5. Monitor for replies (handled by signals module)
```
