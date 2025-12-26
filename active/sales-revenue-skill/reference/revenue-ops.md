# Revenue Operations Reference

Pipeline metrics, forecasting, dashboards, and attribution models.

---

## Pipeline Metrics

### Coverage Ratio

```yaml
formula: "Pipeline Value / Quota"
healthy:
  smb: "3-4x coverage"
  enterprise: "4-5x coverage"
warning: "Below 3x"
action: "Generate more pipeline or lower quota expectations"
```

### Pipeline Velocity

```yaml
formula: "(# Opportunities x Win Rate x Avg Deal Size) / Sales Cycle Days"
use: "Predict monthly/quarterly revenue"
example:
  opportunities: 50
  win_rate: 25%
  avg_deal: $10,000
  cycle_days: 30
  velocity: "(50 x 0.25 x 10000) / 30 = $4,166/day"
```

### Weighted Pipeline

```yaml
formula: "Sum of (Deal Value x Stage Probability)"
stages:
  lead: 5%
  mql: 10%
  sql: 20%
  discovery: 30%
  demo: 50%
  proposal: 70%
  negotiation: 85%
  closed_won: 100%
```

---

## Conversion Metrics

### Full Funnel

| Stage | Formula | Benchmark | Your Rate |
|-------|---------|-----------|-----------|
| Lead to MQL | MQLs / Total Leads | 15-30% | ___ |
| MQL to SQL | SQLs / MQLs | 30-50% | ___ |
| SQL to Opp | Opportunities / SQLs | 50-70% | ___ |
| Opp to Win | Closed Won / Opportunities | 20-30% | ___ |
| Overall | Closed Won / Total Leads | 1-5% | ___ |

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

---

## Unit Economics

### Core Formulas

```yaml
cac:
  formula: "(Sales Cost + Marketing Cost) / New Customers Acquired"
  benchmark: "Varies by ACV - typically 1/3 of first year revenue"

ltv:
  formula: "(ARPU x Gross Margin) / Churn Rate"
  simplified: "ARPU x Average Customer Lifespan"
  example:
    arpu: $500/month
    gross_margin: 80%
    churn_rate: 5%/month
    ltv: "(500 x 0.80) / 0.05 = $8,000"

ltv_cac_ratio:
  formula: "LTV / CAC"
  healthy: ">3:1"
  warning: "<2:1"
  excellent: ">5:1"

cac_payback:
  formula: "CAC / (ARPU x Gross Margin)"
  healthy: "<12 months"
  warning: ">18 months"
  units: "months"
```

---

## Forecasting Methods

### Method 1: Pipeline-Based

```yaml
name: "Pipeline-Based Forecast"
formula: "Sum of (Deal Value x Stage Probability)"
pros:
  - Simple to calculate
  - Data-driven
  - Easy to automate
cons:
  - Doesn't account for rep optimism
  - Assumes consistent conversion rates
best_for: "Early-stage companies with limited historical data"
```

### Method 2: Historical-Based

```yaml
name: "Historical Conversion Forecast"
formula: "Historical Conversion Rate x Current Pipeline"
pros:
  - Accounts for actual past performance
  - Self-correcting over time
cons:
  - Assumes future equals past
  - Slow to adapt to changes
best_for: "Mature companies with consistent sales cycles"
```

### Method 3: Commit-Based

```yaml
name: "Commit-Based Forecast"
formula: "Rep Commits + Manager Adjustments"
categories:
  commit: "90%+ likely to close this period"
  best_case: "50%+ likely to close"
  pipeline: "Everything else"
pros:
  - Incorporates human judgment
  - Accounts for deal-specific factors
cons:
  - Subject to sandbagging
  - Requires disciplined process
best_for: "Enterprise sales with complex deals"
```

### Forecast Accuracy Tracking

```markdown
| Month | Forecast | Actual | Variance | Accuracy |
|-------|----------|--------|----------|----------|
| Jan   | $100K    | $95K   | -$5K     | 95%      |
| Feb   | $120K    | $110K  | -$10K    | 92%      |
| Mar   | $150K    | $160K  | +$10K    | 93%      |

Rolling 3-Month Accuracy: 93%
Target: >85%
```

---

## Attribution Models

### Model Comparison

| Model | Logic | Credit Distribution | Best For |
|-------|-------|---------------------|----------|
| First Touch | 100% to first interaction | All to awareness | Understanding discovery |
| Last Touch | 100% to final interaction | All to closing | Sales efficiency |
| Linear | Equal credit across touches | Split evenly | Simple multi-touch |
| Time Decay | More credit to recent | Weighted toward close | Long sales cycles |
| U-Shaped | First and last get most | 40/20/40 | Most B2B SaaS |
| W-Shaped | First, lead, opp creation | 30/30/30/10 | Complex B2B |

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

---

## Dashboard Templates

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
Leads -> MQL -> SQL -> Opp -> Won
___  ->  ___ -> ___ -> ___ -> ___
      ___%   ___%   ___%   ___%

### Efficiency
- CAC: $__
- LTV: $__
- LTV:CAC: __:1
- Payback: __ months

### By Rep
| Rep | Quota | Closed | Pipeline | Forecast |
|-----|-------|--------|----------|----------|
|     |       |        |          |          |
```

### Weekly Pipeline Review

```markdown
## Weekly Pipeline Review - [Date]

### Coverage Check
- Current pipeline: $___
- Quota this month: $___
- Coverage ratio: ___x (target: 3-4x)

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
|      |        |               |             |

### Action Items
- [ ] Stalled deals to address
- [ ] Proposals to follow up
- [ ] Deals to close this week
```

### Activity Dashboard

```markdown
## Sales Activity - Weekly

| Rep | Calls | Emails | Meetings | Demos | Proposals |
|-----|-------|--------|----------|-------|-----------|
|     |       |        |          |       |           |
| **Total** | | | | | |
| **Target** | | | | | |

### Activity-to-Outcome Ratios
- Calls to Meeting: __:1
- Meetings to Demo: __:1
- Demos to Proposal: __:1
- Proposals to Close: __:1
```

---

## Bottleneck Analysis

### Identifying Problems

```yaml
symptoms:
  - "Deals stalling in [stage]"
  - "Low conversion from [stage] to [stage]"
  - "Long time in [stage]"

diagnosis_questions:
  - "What's the average time in each stage?"
  - "Where do we lose the most deals?"
  - "Which rep has best conversion at [stage]?"
```

### Common Fixes

| Bottleneck | Problem | Likely Causes | Fixes |
|------------|---------|---------------|-------|
| Discovery to Demo | Low demo rate | Poor qualification, weak value prop | Better BANT, discovery training |
| Demo to Proposal | Demo doesn't convert | Generic demo, wrong stakeholders | Personalized demos, multi-thread |
| Proposal to Close | Proposals go dark | No urgency, price shock | Create deadline, pre-proposal pricing discussion |

---

## Sales Cycle Analysis

### Measuring Cycle Length

```yaml
sales_cycle:
  by_segment:
    smb: "14-30 days"
    mid_market: "30-60 days"
    enterprise: "60-180 days"

  by_source:
    inbound: "Typically 20% shorter"
    outbound: "Typically 20% longer"
    referral: "Typically 30% shorter"

  optimization:
    - "Identify longest stages"
    - "Add urgency/scarcity"
    - "Multi-thread earlier"
    - "Get champion buy-in faster"
```

---

## Data Sources

- **CRM:** Salesforce, HubSpot, Pipedrive
- **Analytics:** SQL databases, data warehouse
- **Enrichment:** Clearbit, ZoomInfo
- **Attribution:** Segment, Mixpanel, HubSpot
