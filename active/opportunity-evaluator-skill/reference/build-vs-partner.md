# Build vs Partner Decision Framework

## The Core Question

When facing a capability gap or market opportunity:

```
Should I BUILD it myself?
Should I PARTNER with someone?
Should I BUY/license a solution?
Should I IGNORE it entirely?
```

---

## Decision Tree

```
START: I need [capability/solution]
│
├─► Is this core to my value proposition?
│   │
│   ├─► YES → Strongly consider BUILD
│   │   └─► Can I build it in <2 weeks?
│   │       ├─► Yes → BUILD
│   │       └─► No → BUILD anyway (it's core)
│   │
│   └─► NO → Consider PARTNER or BUY
│       └─► Does a good solution exist?
│           ├─► Yes, affordable → BUY/USE
│           ├─► Yes, expensive → PARTNER or BUILD
│           └─► No → BUILD or IGNORE
│
├─► What's the opportunity cost?
│   │
│   ├─► Building distracts from revenue → PARTNER/BUY
│   └─► Building enables more revenue → BUILD
│
└─► What's the maintenance burden?
    │
    ├─► High ongoing maintenance → PARTNER/BUY
    └─► Low/one-time effort → BUILD
```

---

## Build Analysis

### When to BUILD

✅ **Strong signals to build:**
- Core differentiator for your product
- No good alternatives exist
- You have unique expertise
- Learning is valuable for future
- Control is critical (security, data, UX)
- Existing solutions are overpriced
- You'll use it across multiple projects

### When NOT to Build

❌ **Red flags for building:**
- Well-maintained open source exists
- Commodity functionality (auth, payments)
- You're building to avoid buying
- Timeline is critical
- It's outside your expertise
- Maintenance would consume you

### Build Evaluation Template

```yaml
build_option:
  capability: ""
  
  feasibility:
    have_skills: bool
    estimated_hours: 0
    confidence_level: ""  # high, medium, low
    
  timeline:
    mvp: ""  # days/weeks
    production_ready: ""
    
  maintenance:
    hours_per_month: 0
    complexity: ""  # low, medium, high
    
  benefits:
    - ""
    - ""
    
  risks:
    - ""
    - ""
    
  total_cost:
    build_hours: 0
    build_cost: 0  # hours × rate
    annual_maintenance: 0
    infrastructure: 0
```

---

## Partner Analysis

### Types of Partnerships

| Type | Description | Best For |
|------|-------------|----------|
| **Referral** | Send leads, get commission | Quick revenue, no integration |
| **Reseller** | Sell their product | When their product fits your customers |
| **Integration** | Technical connection | When both benefit from connected product |
| **White-label** | Rebrand their solution | When you need capability fast |
| **Joint venture** | Shared ownership | Large opportunities, aligned incentives |
| **Affiliate** | Commission on sales | Low commitment, test market |

### When to PARTNER

✅ **Strong signals to partner:**
- Complementary capabilities
- Aligned customer base
- Neither wants to build what other has
- Combined offering is stronger
- Shared go-to-market benefits
- Risk/investment sharing makes sense

### When NOT to Partner

❌ **Red flags for partnering:**
- Misaligned incentives
- Unclear economics
- Dependency on unreliable party
- Could become competitor
- Cultural mismatch
- Complicated legal/IP issues

### Partner Evaluation Template

```yaml
partner_option:
  partner_name: ""
  partnership_type: ""
  
  alignment:
    customer_overlap: ""  # high, medium, low
    value_alignment: ""
    culture_fit: ""
    
  economics:
    revenue_share: ""
    costs_to_integrate: 0
    ongoing_costs: 0
    
  dependencies:
    what_we_need_from_them: []
    what_they_need_from_us: []
    
  risks:
    - ""
    - ""
    
  exit_strategy: ""  # What if partnership ends?
```

---

## Buy/License Analysis

### When to BUY

✅ **Strong signals to buy:**
- Commodity functionality
- Time-to-market critical
- Well-established vendors
- Reasonable pricing
- Good documentation/support
- Standard APIs/integration

### Cost Categories

```yaml
buy_option:
  solution: ""
  vendor: ""
  
  direct_costs:
    setup_fee: 0
    monthly_fee: 0
    per_usage_fee: 0
    annual_total: 0
    
  integration_costs:
    development_hours: 0
    development_cost: 0
    
  ongoing_costs:
    maintenance_hours: 0
    support_subscription: 0
    
  hidden_costs:
    vendor_lock_in: ""  # low, medium, high
    switching_cost: 0
    
  total_cost_year_1: 0
  total_cost_3_year: 0
```

### Vendor Evaluation

| Criteria | Weight | Score (1-5) | Notes |
|----------|--------|-------------|-------|
| Feature fit | 25% | | |
| Pricing | 20% | | |
| Reliability | 15% | | |
| Support | 15% | | |
| Integration ease | 15% | | |
| Vendor stability | 10% | | |
| **Total** | 100% | | |

---

## Ignore Analysis

### When to IGNORE

Sometimes the best decision is to not pursue at all:

✅ **Signals to ignore:**
- Nice-to-have, not need-to-have
- Distracts from core focus
- Market too small
- Timing not right
- Not aligned with goals
- Opportunity cost too high

### IGNORE Checklist

```markdown
Before deciding to ignore, confirm:

[ ] Customers aren't asking for this
[ ] Competitors succeeding without it
[ ] Doesn't block critical path
[ ] Can revisit later without penalty
[ ] Ignoring won't create technical debt
[ ] Team/stakeholders aligned on decision
```

---

## Comparative Analysis Template

### Side-by-Side Comparison

| Factor | Build | Partner | Buy | Ignore |
|--------|-------|---------|-----|--------|
| Time to capability | | | | N/A |
| Upfront cost | | | | $0 |
| Ongoing cost | | | | $0 |
| Control level | High | Medium | Low | N/A |
| Maintenance burden | | | | None |
| Strategic value | | | | |
| Risk level | | | | |

### Scoring Matrix

| Factor | Weight | Build | Partner | Buy | Ignore |
|--------|--------|-------|---------|-----|--------|
| Speed to market | 20% | /5 | /5 | /5 | /5 |
| Total cost (3yr) | 20% | /5 | /5 | /5 | /5 |
| Quality/control | 15% | /5 | /5 | /5 | /5 |
| Strategic fit | 15% | /5 | /5 | /5 | /5 |
| Maintenance | 15% | /5 | /5 | /5 | /5 |
| Risk | 15% | /5 | /5 | /5 | /5 |
| **Weighted Score** | | | | | |

---

## Decision Documentation

```yaml
decision:
  capability_needed: ""
  date: ""
  
  options_evaluated:
    build:
      summary: ""
      score: 0
      
    partner:
      with: ""
      summary: ""
      score: 0
      
    buy:
      solution: ""
      summary: ""
      score: 0
      
    ignore:
      rationale: ""
      score: 0
      
  decision: ""  # BUILD, PARTNER, BUY, IGNORE
  
  rationale:
    primary_reasons:
      - ""
      - ""
      - ""
      
    concerns_acknowledged:
      - ""
      
  implementation_plan:
    next_steps:
      - action: ""
        owner: ""
        deadline: ""
        
  success_criteria:
    - ""
    - ""
    
  review_date: ""  # When to revisit this decision
```

---

## Quick Decision Heuristics

### Tim's Rules of Thumb

1. **If it's an MCP server → BUILD**
   - Fast to build with FastMCP
   - Reusable across projects
   - Learning value high

2. **If it's infrastructure → BUY**
   - Supabase, Vercel, RunPod
   - Don't reinvent the wheel

3. **If it's an LLM capability → BUY via API**
   - Anthropic, Google, OpenRouter
   - Don't train your own

4. **If it's GTM capability → PARTNER**
   - Leverage existing networks
   - Coperniq, industry connections

5. **If it doesn't exist and you need it → BUILD**
   - Be the first
   - Create the category

6. **If in doubt → START SMALL**
   - Build MVP to validate
   - Partner on pilot
   - Buy smallest tier
   - Easier to scale up than unwind
