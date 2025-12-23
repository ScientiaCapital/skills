---
name: revenue-ops-skill
description: |
  Analyzes sales metrics, pipeline health, forecasting, and revenue operations. Covers
  funnel analysis, conversion rates, CAC/LTV calculations, and attribution models.
  Use when building dashboards, analyzing pipeline, forecasting revenue, or optimizing sales process.
  Triggers: "pipeline analysis", "sales metrics", "forecast", "conversion rate", "CAC", "LTV",
  "funnel analysis", "revenue ops", "sales dashboard", "win rate", "deal velocity".
---

# Revenue Operations Skill

Sales metrics, pipeline analysis, and revenue forecasting for B2B.

## Quick Reference

| Metric Category | Key Metrics | Healthy Range |
|-----------------|-------------|---------------|
| Pipeline | Coverage, velocity, stages | 3-4x coverage |
| Conversion | Stage-to-stage, win rate | 20-30% win |
| Efficiency | CAC, LTV, payback | <12mo payback |
| Activity | Meetings, demos, proposals | Track trends |

## Core Sales Metrics

### Pipeline Metrics

```yaml
pipeline_metrics:
  coverage_ratio:
    formula: "Pipeline Value / Quota"
    healthy: "3-4x for SMB, 4-5x for Enterprise"
    warning: "Below 3x"

  pipeline_velocity:
    formula: "(# Opportunities × Win Rate × Avg Deal) / Sales Cycle Days"
    use: "Predict monthly revenue"

  weighted_pipeline:
    formula: "Sum of (Deal Value × Stage Probability)"
    stages:
      discovery: 10%
      qualified: 25%
      demo_complete: 50%
      proposal: 75%
      negotiation: 90%
```

### Conversion Metrics

```yaml
conversion_funnel:
  lead_to_mql:
    formula: "MQLs / Total Leads"
    benchmark: "15-30%"

  mql_to_sql:
    formula: "SQLs / MQLs"
    benchmark: "30-50%"

  sql_to_opportunity:
    formula: "Opportunities / SQLs"
    benchmark: "50-70%"

  opportunity_to_win:
    formula: "Closed Won / Opportunities"
    benchmark: "20-30%"

  overall_lead_to_win:
    formula: "Closed Won / Total Leads"
    benchmark: "1-5%"
```

### Efficiency Metrics

```yaml
unit_economics:
  cac:
    formula: "(Sales + Marketing Cost) / New Customers"
    benchmark: "Depends on ACV"

  ltv:
    formula: "(ARPU × Gross Margin) / Churn Rate"
    simplified: "ARPU × Average Customer Lifespan"

  ltv_cac_ratio:
    formula: "LTV / CAC"
    healthy: ">3:1"
    warning: "<2:1"

  cac_payback:
    formula: "CAC / (ARPU × Gross Margin)"
    healthy: "<12 months"
    warning: ">18 months"
```

## Pipeline Analysis Framework

### Stage Definitions

| Stage | Entry Criteria | Exit Criteria | Probability |
|-------|---------------|---------------|-------------|
| **Lead** | Contact info captured | Responded to outreach | 5% |
| **MQL** | Meets ICP criteria | SDR qualified | 10% |
| **SQL** | BANT confirmed | AE accepted | 20% |
| **Discovery** | Meeting scheduled | Pain confirmed | 30% |
| **Demo** | Demo completed | Interest confirmed | 50% |
| **Proposal** | Proposal sent | Decision timeline set | 70% |
| **Negotiation** | Terms discussed | Verbal agreement | 85% |
| **Closed Won** | Contract signed | - | 100% |
| **Closed Lost** | Deal disqualified | - | 0% |

### Pipeline Health Dashboard

```markdown
## Weekly Pipeline Review

### Coverage Check
- [ ] Current pipeline: $___
- [ ] Quota this month: $___
- [ ] Coverage ratio: ___x (target: 3-4x)

### Stage Movement
| Stage | Start of Week | End of Week | Net Change |
|-------|--------------|-------------|------------|
| Discovery | | | |
| Demo | | | |
| Proposal | | | |
| Negotiation | | | |

### Deals at Risk
| Deal | Amount | Days in Stage | Risk Factor |
|------|--------|---------------|-------------|
| | | | |

### Action Items
- [ ] Stalled deals to address
- [ ] Proposals to follow up
- [ ] Deals to close this week
```

## Forecasting Methods

### Three Forecasting Approaches

```yaml
forecasting_methods:
  pipeline_based:
    formula: "Sum of (Deal Value × Stage Probability)"
    pros: "Simple, data-driven"
    cons: "Doesn't account for rep optimism"

  historical_based:
    formula: "Historical conversion × Current pipeline"
    pros: "Accounts for actual performance"
    cons: "Assumes past = future"

  commit_based:
    formula: "Rep commits + Manager adjustments"
    categories:
      commit: "90%+ likely to close"
      best_case: "50%+ likely"
      pipeline: "Everything else"
    pros: "Incorporates judgment"
    cons: "Subject to sandbagging"
```

### Forecast Accuracy Tracking

```markdown
## Monthly Forecast vs. Actual

| Month | Forecast | Actual | Variance | Accuracy |
|-------|----------|--------|----------|----------|
| Jan | $100K | $95K | -$5K | 95% |
| Feb | $120K | $110K | -$10K | 92% |
| Mar | $150K | $160K | +$10K | 93% |

**Rolling 3-Month Accuracy**: ___%
**Target**: >85%
```

## Attribution Models

### Common Models

| Model | Logic | Best For |
|-------|-------|----------|
| First Touch | 100% to first interaction | Understanding awareness |
| Last Touch | 100% to final interaction | Sales efficiency |
| Linear | Equal credit across touches | Simple multi-touch |
| Time Decay | More credit to recent | Long sales cycles |
| U-Shaped | 40/20/40 first-middle-last | Most B2B SaaS |
| W-Shaped | First/Lead Create/Opp Create | Complex B2B |

### Attribution Tracking Template

```yaml
deal_attribution:
  deal_name: ""
  closed_value: 0

  touches:
    first_touch:
      channel: ""
      campaign: ""
      date: ""

    lead_creation:
      channel: ""
      campaign: ""
      date: ""

    opportunity_creation:
      channel: ""
      campaign: ""
      date: ""

    last_touch:
      channel: ""
      campaign: ""
      date: ""

  attribution_credit:
    marketing: 0%
    sales: 0%
    channel: ""
```

## Sales Dashboard KPIs

### Executive Dashboard

```markdown
## Revenue Dashboard - [Month]

### Top Line
| Metric | Actual | Target | % of Target |
|--------|--------|--------|-------------|
| Closed Won | $__ | $__ | __% |
| Pipeline Created | $__ | $__ | __% |
| Pipeline Velocity | $__/day | $__/day | __% |

### Conversion Funnel
Leads → MQL → SQL → Opp → Won
___  →  ___ → ___ → ___ → ___
      ___%   ___%   ___%   ___%

### Efficiency
- CAC: $__
- LTV: $__
- LTV:CAC: __:1
- Payback: __ months

### By Rep
| Rep | Quota | Closed | Pipeline | Forecast |
|-----|-------|--------|----------|----------|
| | | | | |
```

### Activity Dashboard

```markdown
## Sales Activity - Weekly

| Rep | Calls | Emails | Meetings | Demos | Proposals |
|-----|-------|--------|----------|-------|-----------|
| | | | | | |
| **Total** | | | | | |
| **Target** | | | | | |

### Activity-to-Outcome Ratios
- Calls to Meeting: __:1
- Meetings to Demo: __:1
- Demos to Proposal: __:1
- Proposals to Close: __:1
```

## Process Optimization

### Identifying Bottlenecks

```yaml
bottleneck_analysis:
  symptoms:
    - "Deals stalling in [stage]"
    - "Low conversion from [stage] to [stage]"
    - "Long time in [stage]"

  diagnosis_questions:
    - "What's the average time in each stage?"
    - "Where do we lose the most deals?"
    - "Which rep has best conversion at [stage]?"

  common_fixes:
    discovery_to_demo:
      problem: "Low demo rate"
      causes: ["Poor qualification", "Weak value prop"]
      fixes: ["Better BANT", "Discovery training"]

    demo_to_proposal:
      problem: "Demo doesn't convert"
      causes: ["Generic demo", "Wrong stakeholders"]
      fixes: ["Personalized demos", "Multi-thread"]

    proposal_to_close:
      problem: "Proposals go dark"
      causes: ["No urgency", "Price shock"]
      fixes: ["Create deadline", "Pricing discussion pre-proposal"]
```

## Integration Notes

- **Pairs with**: gtm-strategy-skill (ICP analysis), demo-discovery-skill (conversion optimization)
- **Data sources**: Salesforce, HubSpot, SQL databases
- **Projects**: sales-agent, gtm-engineer-journey

## Reference Files

- `reference/metric-definitions.md` - Complete metric glossary
- `reference/dashboard-templates.md` - Ready-to-use dashboard layouts
- `reference/forecasting-models.md` - Advanced forecasting techniques
