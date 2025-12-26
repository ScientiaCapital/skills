# Outreach Reference

Email templates, domain warming, lead scoring, and multi-agent architecture.

---

## Cold Email Templates

### Template A: Tight / Problem-Forward (Recommended)

> Tim from Coperniq. At $5-50M with multiple trades, you're in no-man's land: too complex for Jobber, not ready to bet the business on ServiceTitan.
>
> So you're gluing it together with spreadsheets. That's not a you problem - it's a market gap.
>
> We built for that gap. 10 minutes?

### Template B: Question Hook

> Quick question: how many different systems is your team using to manage jobs right now?
>
> Most MEP contractors I talk to are at 3-4 minimum. One for projects, one for service, spreadsheets for equipment...
>
> We built a single platform that handles all of it. Worth 10 minutes to see if it fits?

### Template C: Trigger Event

> Saw you just hired [3 new field techs / opened a second location / added HVAC services].
>
> That usually means your current tools are about to break. We help growing multi-trade shops stay organized.
>
> Quick call to see if it's relevant?

---

## SMS Sequence

| Step | Day | Message |
|------|-----|---------|
| 1 | 0 | Tim w/ Coperniq. Quick q: how many different systems does your team use to run jobs? We help multi-trade shops consolidate. 5 mins? |
| 2 | 3 | Following up - most contractors your size are stuck between tools too simple or too bloated. We built for the middle. Worth a look? |
| 3 | 7 | Honest q: what's the most broken part of your current setup? Might have a solution. |
| 4 | 10 | Last text. If you're not stuck juggling systems, ignore this. If you are - 10 mins: [link] |

---

## Reply Intent Classification

```python
INTENT_CATEGORIES = {
    'INTERESTED': ['call me', 'tell me more', 'sounds good', 'let\'s talk'],
    'OBJECTION': ['we already', 'not right now', 'too busy', 'using X'],
    'UNSUBSCRIBE': ['stop', 'remove', 'unsubscribe', 'no more'],
    'INFO_REQUEST': ['pricing', 'how does', 'what is', 'demo'],
    'REFERRAL': ['talk to', 'reach out to', 'contact']
}

ROUTING = {
    'INTERESTED': 'sales_agent.schedule_call',
    'OBJECTION': 'nurture_sequence.add',
    'UNSUBSCRIBE': 'cold_reach.stop_sequence',
    'INFO_REQUEST': 'sales_agent.send_info',
    'REFERRAL': 'enricher.find_contact'
}
```

---

## Domain Warming Protocol

### DNS Records Required

```
SPF:   v=spf1 include:_spf.google.com ~all
DKIM:  Generated per domain
DMARC: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

### Warming Schedule

| Day | Daily Volume | Activity |
|-----|--------------|----------|
| 1-7 | 2-5 emails | Reply to warm emails only |
| 8-14 | 5-15 emails | Mix 70% warm + 30% cold |
| 15-21 | 15-30 emails | Monitor spam rates closely |
| 22-30 | 30-50 emails | Full capacity if <2% spam |

### Health Metrics

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| Bounce rate | <3% | Clean list, verify emails |
| Spam rate | <0.3% | Pause warming, check content |
| Open rate | >40% | Adjust subject lines |
| Reply rate | >5% | Good - continue |

### Deliverability Checklist

- [ ] Domain age > 30 days before cold outreach
- [ ] SPF, DKIM, DMARC all configured
- [ ] Warming period completed (30 days)
- [ ] Email verification for all leads
- [ ] Unsubscribe link in all emails
- [ ] Physical address in footer
- [ ] Daily volume < 50/mailbox

---

## 6-Agent Architecture Details

### Agent 1: RESEARCHER

**Purpose:** Company intelligence gathering

**Inputs:** Company name, domain, LinkedIn URL

**Outputs:**
- Tech stack (BuiltWith, Wappalyzer)
- Employee count
- Funding status
- News mentions
- Competitor usage

### Agent 2: QUALIFIER

**Purpose:** ICP fit scoring

**Scoring Model:**
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

### Agent 3: ENRICHER

**Purpose:** Contact discovery

**Outputs:**
- Decision maker contacts
- Verified email addresses
- LinkedIn profiles
- Org chart position

**Sources:** Clearbit, ZoomInfo, Hunter.io, LinkedIn

### Agent 4: WRITER

**Purpose:** Personalized sequence generation

**Inputs:** Enriched lead data, templates

**Outputs:** Multi-step email sequence with personalization tokens

### Agent 5: ANALYZER

**Purpose:** Reply intent classification

**Inputs:** Reply email text

**Outputs:** Intent category + routing decision

### Agent 6: ROUTER

**Purpose:** Orchestration and next-best-action

**Inputs:** Current lead state, agent outputs

**Outputs:** Next action to take

---

## Cost-Optimized Model Selection

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

---

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

---

## ICP Definition (Example: Coperniq)

**Target:** Multi-trade contractors (MEP+E), $5-50M revenue

**Pain Points:**
- Too complex for Jobber, not ready for ServiceTitan
- Projects in one system, service calls in another
- Trucks and equipment tracked in spreadsheets
- No single platform handles multiple trades

---

## Call Summary Format

When summarizing sales calls, capture:

1. **Software Stack:** What systems do they currently use?
2. **Interest Level:** What features/problems resonated?
3. **Team Size:** Field vs office headcount
4. **Goals:** What are they trying to achieve?
5. **Pain Points:** What's broken today?
6. **Failed Implementations:** Previous software attempts that didn't work

---

## Project Structure

```
cold-reach/
├── domains/      # Domain + DNS automation
├── warming/      # Reputation building
├── sequences/    # Email campaigns
└── signals/      # Reply detection

sales-agent/
├── agents/       # 6 specialized agents
│   ├── researcher.py
│   ├── qualifier.py
│   ├── enricher.py
│   ├── writer.py
│   ├── analyzer.py
│   └── router.py
├── services/
│   ├── lead_scorer.py
│   └── batch_processor.py
└── api/          # FastAPI endpoints

dealer-scraper/
├── scrapers/     # Playwright scripts
├── processors/   # Data cleaning
└── storage/      # Supabase integration
```
