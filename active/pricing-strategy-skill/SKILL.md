---
name: pricing-strategy-skill
description: |
  Develops pricing strategies including value-based pricing, packaging, tiering, and
  monetization models for B2B SaaS and services. Covers pricing psychology, competitive
  positioning, and price optimization. Use when setting prices, creating tiers, or evaluating
  monetization strategies. Triggers: "pricing strategy", "price point", "packaging", "tiering",
  "value-based pricing", "monetization", "pricing model", "discount strategy", "price increase".
---

# Pricing Strategy Skill

B2B pricing strategy, packaging, and monetization for SaaS and services.

## Quick Reference

| Pricing Model | Best For | Complexity |
|---------------|----------|------------|
| Flat rate | Simple products | Low |
| Per seat | Team collaboration tools | Medium |
| Usage-based | APIs, infrastructure | High |
| Tiered | Feature differentiation | Medium |
| Hybrid | Enterprise SaaS | High |

## Pricing Frameworks

### Value-Based Pricing Process

```yaml
value_pricing_steps:
  1_understand_value:
    - "What problem does this solve?"
    - "What's the cost of the problem?"
    - "What's the value of the solution?"

  2_quantify_value:
    - "Time saved × hourly rate"
    - "Revenue increased"
    - "Costs avoided"
    - "Risk mitigated"

  3_capture_value:
    - "Price at 10-20% of value delivered"
    - "Anchor to alternatives"
    - "Leave money on table for adoption"

  4_communicate_value:
    - "ROI calculators"
    - "Case studies with numbers"
    - "Value-based proposals"
```

### Value Calculation Template

```markdown
## Value Calculation: [Product/Service]

### Time Savings
- Hours saved per week: __
- Hourly rate of user: $__
- Weekly savings: $__
- Annual savings: $__

### Revenue Impact
- Additional deals/month: __
- Average deal value: $__
- Monthly revenue increase: $__
- Annual revenue increase: $__

### Cost Avoidance
- Errors prevented: __
- Cost per error: $__
- Annual savings: $__

### Total Annual Value: $__

### Suggested Price Point
- 10% of value: $__/year
- 15% of value: $__/year
- 20% of value: $__/year
```

## Pricing Models Deep Dive

### Per-Seat Pricing

```yaml
per_seat_model:
  pros:
    - "Easy to understand"
    - "Scales with organization size"
    - "Predictable revenue"

  cons:
    - "Discourages adoption"
    - "Gaming (shared logins)"
    - "Hard to price for varying usage"

  best_practices:
    - "Offer viewer/editor tiers"
    - "Volume discounts at thresholds"
    - "Annual commitment discounts"

  example_tiers:
    starter: "$15/seat/month (up to 5)"
    professional: "$25/seat/month (5-50)"
    enterprise: "Custom (50+)"
```

### Usage-Based Pricing

```yaml
usage_model:
  pros:
    - "Aligns cost with value"
    - "Low barrier to start"
    - "Scales naturally"

  cons:
    - "Unpredictable revenue"
    - "Complex billing"
    - "Customer budget anxiety"

  common_metrics:
    - "API calls"
    - "Compute time"
    - "Storage"
    - "Active users"
    - "Transactions processed"

  best_practices:
    - "Include free tier/credits"
    - "Provide usage dashboards"
    - "Alert before overage"
    - "Offer committed use discounts"
```

### Tiered Pricing

```yaml
tiered_model:
  structure:
    free:
      purpose: "Land, qualify, viral growth"
      limits: "Core features, limited usage"

    starter:
      purpose: "Individuals, small teams"
      price: "$X/month"
      features: "Essential features"

    professional:
      purpose: "Growing teams"
      price: "$Y/month"
      features: "Full features + integrations"

    enterprise:
      purpose: "Large orgs, compliance needs"
      price: "Custom"
      features: "SSO, SLA, dedicated support"

  psychology:
    - "3-4 tiers optimal"
    - "Middle tier most popular (anchor)"
    - "Enterprise tier prices pro tier down"
```

## Packaging Best Practices

### Good/Better/Best Framework

```markdown
## Tier Structure

### Good (Entry)
**Price**: $X/month
**Target**: [Entry segment]
**Core value**: [Primary use case]
**Limitations**: [What's not included]

### Better (Growth) ← ANCHOR
**Price**: $Y/month (most popular)
**Target**: [Primary segment]
**Core value**: [Expanded use cases]
**Includes**: Everything in Good, plus:
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Best (Scale)
**Price**: $Z/month or Custom
**Target**: [Enterprise segment]
**Core value**: [Full platform]
**Includes**: Everything in Better, plus:
- [Advanced feature 1]
- [Advanced feature 2]
- [Enterprise requirements]
```

### Feature Gating Strategy

```yaml
feature_gating:
  gate_by_scale:
    - "Number of users"
    - "Number of projects"
    - "API calls"
    - "Storage"

  gate_by_sophistication:
    - "Advanced features in higher tiers"
    - "Integrations at higher tiers"
    - "Automation at higher tiers"

  gate_by_control:
    - "Admin controls"
    - "SSO/SAML"
    - "Audit logs"
    - "Custom roles"

  never_gate:
    - "Security features"
    - "Core functionality"
    - "Data export"
```

## Pricing Psychology

### Key Principles

```yaml
pricing_psychology:
  anchoring:
    principle: "First price seen influences perception"
    application: "Show enterprise tier first, or '60% choose Pro'"

  decoy_effect:
    principle: "Irrelevant option changes preference"
    application: "Add tier that makes target tier look good"

  price_ending:
    principle: "9s feel like deals, 0s feel premium"
    application: "$99 for SMB, $100 for enterprise"

  bundling:
    principle: "Bundles feel like better value"
    application: "Package features vs. selling à la carte"

  annual_discount:
    principle: "Upfront commitment = better terms"
    application: "20% discount for annual (2 months free)"
```

### Pricing Page Best Practices

```markdown
## Pricing Page Checklist

### Above the Fold
- [ ] Clear tier names
- [ ] Prices visible immediately
- [ ] "Most Popular" badge on target tier
- [ ] CTA buttons for each tier

### Tier Details
- [ ] Feature comparison table
- [ ] Check marks for included features
- [ ] Expansion for feature details
- [ ] Clear upgrade path

### Trust Elements
- [ ] Money-back guarantee
- [ ] Customer logos
- [ ] Security badges
- [ ] "No credit card required" (if free trial)

### Conversion Optimization
- [ ] FAQ section
- [ ] "Compare plans" toggle
- [ ] Annual/monthly toggle
- [ ] Enterprise "Contact us" CTA
```

## Discounting Strategy

### Discount Framework

```yaml
discount_types:
  volume:
    trigger: "Commitment to scale"
    range: "10-30%"
    example: "20% off for 100+ seats"

  term:
    trigger: "Annual commitment"
    range: "15-25%"
    example: "2 months free on annual"

  competitive:
    trigger: "Switching from competitor"
    range: "20-40%"
    example: "Match remaining contract"

  strategic:
    trigger: "Reference customer, logo value"
    range: "Up to 50%"
    example: "Name brand + case study"
```

### When NOT to Discount

```markdown
## Protect Your Pricing

### Never Discount When:
- Customer hasn't articulated value
- No competitive pressure
- Early in negotiation
- Customer is price shopping
- Deal doesn't meet minimum size

### Alternatives to Discounting:
- Extended payment terms
- Additional services/training
- Extended trial
- Success milestones unlock features
- Multi-year lock-in
```

## Price Increase Strategy

### Planning a Price Increase

```yaml
price_increase_playbook:
  preparation:
    - "Analyze customer value delivered"
    - "Review competitive pricing"
    - "Segment by price sensitivity"
    - "Prepare value justification"

  communication:
    timing: "60-90 days notice minimum"
    channel: "Email from executive"
    messaging:
      - "Lead with value added"
      - "Be transparent about increase"
      - "Offer annual lock-in at current rate"

  execution:
    - "Grandfather best customers if needed"
    - "Prepare for some churn"
    - "Train support on objections"
    - "Monitor churn closely"

  typical_increase:
    annual: "3-5% inflation adjustment"
    strategic: "10-20% with value adds"
    catch_up: "25%+ if underpriced"
```

## Services Pricing

### Consulting/Services Rates

```yaml
services_pricing:
  hourly:
    junior: "$100-150/hr"
    mid: "$150-250/hr"
    senior: "$250-400/hr"
    executive: "$400-600/hr"

  project_based:
    method: "Estimate hours × 1.2 buffer × rate"
    include: "Scope change process"

  retainer:
    discount: "10-20% vs hourly"
    minimum: "40 hours/month"
    benefit: "Predictable, priority access"

  value_based:
    method: "% of value delivered"
    range: "10-30% of documented savings"
    risk: "Tie to measurable outcome"
```

## Integration Notes

- **Pairs with**: gtm-strategy-skill (positioning), revenue-ops-skill (metrics)
- **Data sources**: Competitive intel, customer feedback, usage data
- **Projects**: All SaaS products

## Reference Files

- `reference/pricing-models.md` - Deep dive on each model
- `reference/packaging-examples.md` - Real SaaS packaging examples
- `reference/negotiation-tactics.md` - Sales team pricing guidance
