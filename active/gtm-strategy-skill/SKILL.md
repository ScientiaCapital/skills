---
name: gtm-strategy-skill
description: |
  Develops go-to-market strategies including ICP definition, positioning, messaging frameworks,
  and competitive analysis. Use when planning market entry, defining ideal customer profiles,
  creating positioning statements, building messaging hierarchies, or analyzing competitors.
  Triggers: "GTM strategy", "go-to-market plan", "ICP definition", "ideal customer profile",
  "positioning statement", "messaging framework", "competitive positioning", "market entry".
---

# GTM Strategy Skill

Go-to-market strategy development for B2B SaaS and technical products.

## Quick Reference

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| ICP Development | Define ideal customer | Before any outreach |
| Positioning | Differentiate in market | Product launch, pivot |
| Messaging Hierarchy | Consistent communication | Sales enablement |
| Competitive Intel | Understand landscape | Deal strategy, positioning |
| Channel Strategy | Select GTM motions | Resource allocation |

## ICP Development Framework

### Three Dimensions of ICP

```yaml
icp_framework:
  firmographics:
    - company_size: "50-500 employees"
    - revenue_range: "$10M-$100M ARR"
    - industry: ["Construction", "MEP", "Field Services"]
    - geography: "North America"
    - growth_stage: "Series A-C or profitable"

  technographics:
    - current_stack: ["Procore", "ServiceTitan", "QuickBooks"]
    - tech_maturity: "Mid - has CRM, considering automation"
    - integration_needs: ["ERP", "Accounting", "Field Service"]
    - cloud_adoption: "Hybrid or cloud-first"

  psychographics:
    - pain_awareness: "Problem-aware, solution-seeking"
    - change_readiness: "Has budget, executive sponsor"
    - buying_process: "Committee (3-5 stakeholders)"
    - risk_tolerance: "Moderate - needs proof points"
```

### ICP Scoring Template

| Criterion | Weight | Score (1-5) | Weighted |
|-----------|--------|-------------|----------|
| Company size fit | 20% | | |
| Industry match | 20% | | |
| Tech stack compatibility | 15% | | |
| Pain point alignment | 25% | | |
| Budget availability | 20% | | |
| **Total** | 100% | | |

**Tiers**: 80+ = Ideal | 60-79 = Good Fit | 40-59 = Marginal | <40 = Poor Fit

## Positioning Framework

### April Dunford's Positioning Canvas

```markdown
## [Product] Positioning Statement

**Competitive Alternatives**: What would customers use if we didn't exist?
→ [List 2-3 alternatives]

**Unique Attributes**: What do we have that alternatives don't?
→ [List differentiators]

**Value**: What capability do those attributes enable?
→ [Translate features to benefits]

**Target Customers**: Who cares most about this value?
→ [Specific customer characteristics]

**Market Category**: What context makes our value obvious?
→ [Category or create new one]
```

### Positioning Statement Template

```
For [target customer] who [statement of need],
[product name] is a [market category]
that [key benefit/differentiation].
Unlike [competitive alternative],
our product [primary differentiator].
```

## Messaging Hierarchy

### Three Levels of Messaging

```
Level 1: Strategic Narrative (Company)
├── Who we are
├── What we believe
└── Why we exist

Level 2: Solution Messaging (Product)
├── What it does
├── Key differentiators (3 max)
└── Proof points

Level 3: Persona Messaging (Audience)
├── Pain points by role
├── Value props by role
└── Objection handling by role
```

### Persona Messaging Matrix

| Persona | Pain Points | Value Props | Proof Points |
|---------|-------------|-------------|--------------|
| CFO | Cost visibility, compliance | ROI, audit trail | Case study: 30% savings |
| Ops Director | Manual processes, errors | Automation, accuracy | Demo: 10x faster |
| End User | Clunky tools, training | Easy to use, mobile | G2 reviews: 4.8/5 |

## Competitive Intelligence

### Battle Card Structure

```markdown
## Competitor: [Name]

### Overview
- Founded: YYYY | HQ: Location | Funding: $XXM
- Target market: [description]
- Pricing: [model and range]

### Strengths (acknowledge honestly)
- [Strength 1]
- [Strength 2]

### Weaknesses (our opportunities)
- [Weakness 1 → our advantage]
- [Weakness 2 → our advantage]

### Common Objections When We Compete
| Objection | Response |
|-----------|----------|
| "They're cheaper" | [Value-based response] |
| "They have feature X" | [Alternative or roadmap] |

### Win Strategy
1. Lead with [differentiator]
2. Demonstrate [proof point]
3. Reference [customer story]
```

## Channel Strategy

### GTM Motion Selection

| Motion | Best For | CAC | Sales Cycle | Team |
|--------|----------|-----|-------------|------|
| Product-Led | Low ACV (<$5K), self-serve | Low | Days | Growth |
| Sales-Assisted | Mid ACV ($5-50K) | Medium | Weeks | SDR+AE |
| Enterprise | High ACV ($50K+) | High | Months | AE+SE |
| Partner/Channel | Geographic expansion | Variable | Variable | Partner Mgr |

### Channel Mix Framework

```
Primary Channel (60-70% of pipeline)
└── [Selected motion based on ACV and complexity]

Secondary Channel (20-30%)
└── [Supporting motion for different segments]

Experimental (10%)
└── [New channel being tested]
```

## Launch Playbook Checklist

```markdown
## Pre-Launch (T-30 days)
- [ ] ICP documented and validated
- [ ] Positioning finalized
- [ ] Messaging hierarchy complete
- [ ] Battle cards created
- [ ] Sales enablement materials ready
- [ ] Pricing approved

## Launch Week
- [ ] Press release distributed
- [ ] Website updated
- [ ] Sales team trained
- [ ] Customer references lined up
- [ ] Outbound sequences activated

## Post-Launch (T+30 days)
- [ ] Win/loss analysis started
- [ ] Messaging refinement based on feedback
- [ ] Pipeline review
- [ ] Competitive response documented
```

## Integration Notes

- **Pairs with**: market-research-skill (company intel), demo-discovery-skill (execution)
- **Feeds into**: sales-outreach-skill (sequences), content-marketing-skill (assets)
- **Projects**: gtm-engineer-journey, coperniq-forge, coperniq-battle-cards

## Reference Files

- `reference/icp-templates.md` - Detailed ICP worksheets and examples
- `reference/positioning-examples.md` - Real positioning statements
- `reference/battle-card-template.md` - Full battle card format
- `reference/launch-checklist.md` - Comprehensive launch playbook
