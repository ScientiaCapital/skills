---
name: sales-outreach-skill
version: 1.0.0
description: |
  B2B sales automation patterns for cold outreach, lead scraping, and multi-agent
  sales systems. Use when building sales infrastructure, creating email sequences,
  implementing lead scoring, or developing GTM automation. Triggers: "cold email",
  "lead scoring", "email sequence", "BDR automation", "domain warming", "sales pipeline",
  "ICP definition", "outreach campaign", "lead qualification".
---

# Sales Outreach Skill

B2B sales automation patterns for GTM systems.

## Quick Reference

| Component | Purpose | When to Use |
|-----------|---------|-------------|
| Lead Scraping | Collect prospect data | Building lead lists |
| Lead Scoring | Qualify + tier leads | Prioritizing outreach |
| Domain Warming | Build email reputation | Before cold campaigns |
| Sequence Engine | Multi-step outreach | Running campaigns |
| Intent Classification | Route replies | Processing responses |

## The GTM Pipeline

```
dealer-scraper → sales-agent → cold-reach → vozlux
   (leads)       (AI agents)    (email)    (voice)
                     ↓
            ai-cost-optimizer
             (saves 40-70%)
```

## Lead Tiering

| Tier | Criteria | Priority |
|------|----------|----------|
| GOLD | Multi-trade, $5-50M revenue, website | Immediate |
| SILVER | Single trade, has reviews/website | Week 1 |
| BRONZE | Basic listing only | Nurture |

## Lead Scoring (Quick)

```python
factors = {
    'icp_fit': 0-30,        # Match to ideal customer profile
    'intent_signals': 0-25, # Buying signals detected
    'engagement': 0-20,     # Email opens, clicks, replies
    'timing': 0-15,         # Budget cycle, seasonality
    'budget_signals': 0-10  # Company size, funding
}
# Total: 0-100
# Hot: 70+ | Warm: 40-69 | Nurture: <40
```

## 6-Agent Architecture (Quick)

| Agent | Role |
|-------|------|
| RESEARCHER | Company intel, tech stack |
| QUALIFIER | ICP fit scoring |
| ENRICHER | Contact discovery |
| WRITER | Sequence generation |
| ANALYZER | Reply intent |
| ROUTER | Next-best-action |

## Project Structure

```
cold-reach/
├── domains/      # Domain + DNS automation
├── warming/      # Reputation building
├── sequences/    # Email campaigns
└── signals/      # Reply detection

sales-agent/
├── agents/       # 6 specialized agents
├── services/     # Lead scoring, batch processing
└── api/          # FastAPI endpoints

dealer-scraper/
├── scrapers/     # Playwright scripts
├── processors/   # Data cleaning
└── storage/      # Supabase integration
```

## Integration Notes

- **Email:** Instantly.ai, Apollo.io, custom SMTP
- **CRM:** Salesforce, HubSpot, Airtable
- **Enrichment:** Clearbit, ZoomInfo, LinkedIn
- **Projects:** cold-reach, sales-agent, dealer-scraper-mvp

## Reference Files

- `reference/coperniq-messaging.md` - ICP, templates, SMS sequences
- `reference/domain-warming.md` - Protocol, deliverability checklist
- `reference/agent-architecture.md` - 6-agent system details, pipeline code
