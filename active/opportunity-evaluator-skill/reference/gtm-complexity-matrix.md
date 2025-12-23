# GTM Complexity Matrix

## Overview

Understanding sales complexity determines resource allocation, timeline expectations, and strategy selection. This framework maps opportunities against go-to-market difficulty.

---

## Complexity Levels

### Level 1: Self-Serve / PLG (Lowest Complexity)

```yaml
characteristics:
  buyer: Individual or small team
  company_size: 1-50 employees
  acv: $0 - $2,000/year
  sales_cycle: Minutes to days
  decision_maker: User = buyer
  process: Credit card, no approval needed
  
examples:
  - Developer tools
  - Productivity apps
  - Freemium SaaS
  - Marketplace listings
  
gtm_motion:
  primary: Product-led growth
  channels: SEO, content, community, Product Hunt
  sales_team: None or support-focused
  
tim_fit: EXCELLENT
  - Can build and launch solo
  - No sales overhead
  - Focus on product
  
success_metrics:
  - Signups
  - Activation rate
  - Conversion free → paid
  - Net revenue retention
```

### Level 2: Low-Touch Sales

```yaml
characteristics:
  buyer: Team lead or department head
  company_size: 10-200 employees
  acv: $2,000 - $15,000/year
  sales_cycle: 1-4 weeks
  decision_maker: Manager with budget authority
  process: Light demo, proposal, verbal approval
  
examples:
  - SMB SaaS tools
  - Marketing platforms
  - HR/recruiting tools
  - Analytics products
  
gtm_motion:
  primary: Inbound + light outbound
  channels: Content, ads, SDR outreach
  sales_team: 1-2 AEs can handle
  
tim_fit: EXCELLENT
  - Sweet spot for BDR/AE skills
  - Short cycle = fast feedback
  - Can do solo or small team
  
success_metrics:
  - Pipeline generated
  - Demo to close rate
  - Average deal size
  - Time to close
```

### Level 3: Mid-Market Sales

```yaml
characteristics:
  buyer: Director or VP
  company_size: 200-2,000 employees
  acv: $15,000 - $100,000/year
  sales_cycle: 1-3 months
  decision_maker: Committee (3-5 stakeholders)
  process: Multiple demos, POC, business case, procurement
  
examples:
  - Department-wide software
  - Security tools
  - Data platforms
  - Coperniq (current)
  
gtm_motion:
  primary: Account-based + inbound
  channels: Events, partners, outbound, content
  sales_team: SDR → AE → AM model
  
tim_fit: GOOD
  - Familiar territory from Coperniq
  - Requires more coordination
  - Best with full-time focus
  
success_metrics:
  - Qualified pipeline
  - Stage progression velocity
  - Win rate by competitor
  - Expansion revenue
```

### Level 4: Enterprise Sales

```yaml
characteristics:
  buyer: C-suite or SVP
  company_size: 2,000+ employees
  acv: $100,000 - $1M+/year
  sales_cycle: 6-18 months
  decision_maker: Executive committee + procurement
  process: RFP, security review, legal, pilot, business case
  
examples:
  - Platform replacements
  - Company-wide tools
  - Strategic partnerships
  - Infrastructure
  
gtm_motion:
  primary: Enterprise AE + overlay specialists
  channels: Executive relationships, partners, events
  sales_team: Full team (SDR, AE, SE, CSM, exec sponsor)
  
tim_fit: MODERATE
  - Have done before (Salesforce era)
  - Requires significant resources
  - Better as employee than founder
  
success_metrics:
  - Strategic accounts engaged
  - Executive relationships
  - Pipeline value
  - Multi-year contract value
```

### Level 5: Complex Enterprise (Highest Complexity)

```yaml
characteristics:
  buyer: Board level / cross-functional
  company_size: Global enterprise
  acv: $1M+/year
  sales_cycle: 12-36 months
  decision_maker: Multiple executives across functions
  process: Extensive evaluation, transformation project
  
examples:
  - Digital transformation
  - Core system replacement
  - Strategic consulting
  - Platform partnerships
  
gtm_motion:
  primary: Executive relationships + consulting
  channels: Partner networks, industry events, M&A
  sales_team: Dedicated team + partner ecosystem
  
tim_fit: LOW (as founder)
  - Requires organization, not individual
  - Capital intensive
  - Long runway needed
  
success_metrics:
  - Strategic relationships
  - Partner leverage
  - Multi-year pipeline
```

---

## Complexity Assessment Questions

### Buyer Assessment

| Question | Low Complexity | High Complexity |
|----------|---------------|-----------------|
| Who signs the check? | Individual | Committee/Board |
| Budget pre-approved? | Yes | Requires justification |
| Technical evaluation? | Self-serve trial | POC with IT |
| Security review? | None | SOC2, vendor assessment |
| Legal involved? | Standard terms | Custom negotiation |

### Process Assessment

| Question | Low Complexity | High Complexity |
|----------|---------------|-----------------|
| Typical sales cycle | Days/weeks | Months/years |
| Meetings to close | 1-3 | 10-20+ |
| Stakeholders involved | 1-2 | 5-15 |
| Competitive bake-off? | Rarely | Usually |
| Procurement process | Credit card | RFP/RFI |

### Resource Assessment

| Question | Low Complexity | High Complexity |
|----------|---------------|-----------------|
| Can one person sell this? | Yes | No |
| Demo complexity | Self-serve or simple | Multi-day, technical |
| Implementation needed? | Plug and play | Professional services |
| Support requirements | Community/docs | Dedicated CSM |
| Reference requirements | Reviews | Named references |

---

## Matching Complexity to Resources

### Solo Founder (Tim's current state)

```yaml
optimal_complexity: Level 1-2
max_complexity: Level 3 (with constraints)

constraints:
  - 20 hrs/week available for side projects
  - No sales team
  - Limited marketing budget
  - Mexico City timezone
  
strategies:
  - Focus on PLG or low-touch
  - Productize consulting
  - Partner for enterprise deals
  - Leverage Coperniq network
```

### With Co-founder/Partner

```yaml
optimal_complexity: Level 2-3
max_complexity: Level 4 (with investment)

enables:
  - Split technical/GTM
  - Higher touch sales
  - More accounts in parallel
  - Extended hours coverage
```

### Funded Startup

```yaml
optimal_complexity: Level 3-4
max_complexity: Level 5

enables:
  - Full sales team
  - Professional services
  - Enterprise readiness (SOC2, etc.)
  - Long sales cycles acceptable
```

---

## Complexity Reduction Tactics

### If Deal Seems Too Complex

1. **Target smaller segment**
   - Enterprise → Mid-market
   - Company-wide → Department
   - Platform → Point solution

2. **Simplify pricing**
   - Custom → Standard tiers
   - Annual → Monthly option
   - Per-seat → Flat rate

3. **Reduce stakeholders**
   - Find single budget holder
   - Start with pilot/POC
   - Land and expand

4. **Eliminate friction**
   - Self-serve trial
   - No-contract option
   - Simple implementation

5. **Partner for complexity**
   - Reseller handles procurement
   - SI handles implementation
   - Platform handles billing

---

## Decision Framework

```
Evaluate Opportunity Complexity
│
├─► Level 1-2? 
│   └─► GREEN LIGHT - Proceed as planned
│
├─► Level 3?
│   └─► Is this full-time focus?
│       ├─► Yes → Proceed with plan
│       └─► No → Can I simplify to Level 2?
│           ├─► Yes → Simplify and proceed
│           └─► No → Partner or pass
│
├─► Level 4?
│   └─► Is this a job/funded company?
│       ├─► Yes → Evaluate role fit
│       └─► No → Find partner or pass
│
└─► Level 5?
    └─► Only as employee at established company
```

---

## Template: Complexity Assessment

```yaml
opportunity: ""
date: ""

complexity_indicators:
  buyer_level: ""  # Individual, Manager, Director, VP, C-suite
  company_size: 0
  estimated_acv: 0
  expected_cycle: ""  # days, weeks, months
  stakeholders: 0
  procurement: ""  # credit card, PO, RFP
  security_review: bool
  legal_review: bool
  implementation: ""  # self-serve, guided, professional services
  
complexity_level: 0  # 1-5

resource_requirements:
  sales_team_needed: bool
  technical_resources: ""
  support_requirements: ""
  time_investment: ""
  
fit_assessment:
  matches_current_resources: bool
  simplification_possible: bool
  partnership_opportunity: bool
  
recommendation: ""  # proceed, simplify, partner, pass
```
