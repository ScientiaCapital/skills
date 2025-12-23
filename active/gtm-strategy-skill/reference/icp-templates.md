# ICP Development Templates

## Full ICP Worksheet

### Section 1: Firmographics

```yaml
company_profile:
  size:
    employees_min:
    employees_max:
    revenue_min:
    revenue_max:

  industry:
    primary: []
    secondary: []
    excluded: []

  geography:
    regions: []
    countries: []
    excluded: []

  company_type:
    - [ ] Startup (seed-Series A)
    - [ ] Growth (Series B-D)
    - [ ] Enterprise (public/PE-backed)
    - [ ] SMB (bootstrapped)
```

### Section 2: Technographics

```yaml
tech_profile:
  required_stack:
    must_have: []
    nice_to_have: []
    incompatible: []

  tech_maturity:
    - [ ] Early adopter (bleeding edge)
    - [ ] Early majority (proven tech)
    - [ ] Late majority (conservative)
    - [ ] Laggard (legacy-bound)

  current_solutions:
    crm: ""
    erp: ""
    industry_specific: ""

  integration_requirements: []
```

### Section 3: Psychographics

```yaml
buyer_profile:
  awareness_stage:
    - [ ] Unaware (doesn't know problem)
    - [ ] Problem-aware (feels pain)
    - [ ] Solution-aware (researching)
    - [ ] Product-aware (evaluating us)

  buying_committee:
    economic_buyer: ""
    technical_buyer: ""
    user_buyer: ""
    champion: ""
    blocker: ""

  decision_criteria:
    primary: []
    secondary: []

  risk_factors:
    - [ ] Budget concerns
    - [ ] Implementation risk
    - [ ] Change management
    - [ ] Vendor stability
```

### Section 4: Behavioral Signals

```yaml
intent_signals:
  high_intent:
    - "Searched for [competitor] alternatives"
    - "Visited pricing page 3+ times"
    - "Downloaded buyer's guide"

  medium_intent:
    - "Attended webinar"
    - "Engaged with case study"
    - "Connected on LinkedIn"

  low_intent:
    - "Blog subscriber"
    - "Social follower"
    - "Newsletter open"
```

## ICP Validation Checklist

```markdown
## Validate Your ICP

### Market Size Check
- [ ] TAM: Total addressable market calculated
- [ ] SAM: Serviceable addressable market defined
- [ ] SOM: Realistic obtainable market estimated
- [ ] Minimum 1000 companies in ICP

### Win Rate Check
- [ ] Historical win rate against ICP: >30%
- [ ] Average deal size meets targets
- [ ] Sales cycle length acceptable

### Customer Success Check
- [ ] ICP customers have lowest churn
- [ ] Highest NPS scores from ICP
- [ ] Most expansions/upsells from ICP

### Qualitative Check
- [ ] Sales team agrees on ICP
- [ ] Customer success validates fit
- [ ] Product roadmap serves ICP
```

## Example ICP: MEP Contractors (Coperniq)

```yaml
icp_mep_contractor:
  firmographics:
    employees: "50-500"
    revenue: "$10M-$100M"
    trades: ["Electrical", "Plumbing", "HVAC", "Fire Protection"]
    geography: "US, primarily Sun Belt"

  technographics:
    current_tools:
      - "QuickBooks or Sage"
      - "Spreadsheets for project tracking"
      - "Paper or basic mobile for field"
    pain_indicators:
      - "Manual data entry between systems"
      - "No real-time job costing"
      - "Field-office communication gaps"

  psychographics:
    champions: ["Operations Manager", "CFO", "Owner"]
    pain_points:
      - "Can't see project profitability until job ends"
      - "Billing delays due to paperwork"
      - "Losing bids due to slow estimates"

  disqualifiers:
    - "Under $5M revenue (can't afford)"
    - "Union-only shops (different workflow)"
    - "Already on ServiceTitan (entrenched)"
```
