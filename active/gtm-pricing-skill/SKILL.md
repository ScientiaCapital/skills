---
name: "gtm-pricing"
description: "Generic B2B go-to-market frameworks: ICP scoring rubric, April Dunford positioning, value-based/tiered pricing, and opportunity scoring. Use when: 'build an ICP', 'write a positioning statement', 'design pricing tiers', 'set list price', 'feature gating', 'score an opportunity', 'competitive battle card', 'GTM launch checklist'. Not for Epiphan account/competitor research (use research-skill) or live lead ICP scoring (use qualify_lead) or current Epiphan pricing/SKU truth (use search_product_catalog)."
---

<objective>
Comprehensive B2B go-to-market framework covering ICP development (firmographics, technographics, psychographics), positioning (April Dunford canvas), pricing strategy (value-based, tiered, feature gating), and opportunity evaluation (scoring, red flags, complexity levels).
</objective>

<quick_start>
**Trigger:** generic B2B GTM framework work — build an ICP, write positioning, design pricing tiers, score an opportunity, build a battle card, plan a launch. This skill is frameworks/templates only; it holds no live Epiphan data.

**ICP scoring:** 80+ = Ideal | 60-79 = Good | 40-59 = Marginal | <40 = Pass. Scoring a *specific, live* Epiphan lead or deal? Call `qualify_lead` instead of hand-scoring here — it's the source of truth for category/ATL-BTL/suppression (see `skill-audit/specs/suppression-spec.md`). Use this skill's rubric only to design or calibrate the scoring criteria themselves.

**Positioning statement:**
```
For [target] who [need], [product] is a [category] that [benefit].
Unlike [alternative], our product [differentiator].
```

**Value-based pricing:** Price at 10-20% of quantified value delivered. For an actual Epiphan quote, list price, or competitive price comparison, pull current numbers via `search_product_catalog` — never state an Epiphan price or SKU from memory.

**Opportunity score:** /100 across Market Fit, Technical Fit, GTM Fit, Personal Fit, Economics
</quick_start>

<success_criteria>
GTM strategy is successful when:
- ICP documented with scoring criteria (firmographics, technographics, psychographics)
- Positioning statement follows April Dunford framework
- Pricing anchored to quantified value (not cost-plus)
- Tier structure follows Good/Better/Best with clear feature gates
- Opportunity scoring identifies red flags and good signals
- Battle cards created for top 3 competitors
- Launch checklist completed (pre-launch, launch, post-launch)
- Deliverable has a landing place: render the finished ICP/positioning/pricing doc as an HTML one-pager artifact, or hand off the draft to a doc-coauthoring skill for a shareable doc — this skill produces the content, not the delivery channel
</success_criteria>

<core_content>
Comprehensive guide for B2B go-to-market strategy, pricing, and opportunity evaluation.

## Quick Reference

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| ICP Development | Define ideal customer | Before any outreach |
| Positioning | Differentiate in market | Product launch, pivot |
| Messaging Hierarchy | Consistent communication | Sales enablement |
| Competitive Intel | Understand landscape | Deal strategy, positioning |
| Value-Based Pricing | Price by value delivered | Setting initial prices |
| Tier Structure | Package offering | Feature gating decisions |
| Opportunity Scoring | Evaluate fit | New client/project decisions |

---

## Part 1: Go-To-Market Strategy

### ICP Development Framework

> **Epiphan-specific:** this section is for *designing* the ICP rubric (the dimensions, weights, and cutoffs). To score a real, live lead or account against Epiphan's ICP, call `qualify_lead` — don't re-derive category/ATL-BTL from raw CRM fields here.

Build your ICP across three dimensions, then score each prospect:

**Dimension 1 -- Firmographics (who they are):**
- Company size: employee count range, revenue range
- Industry: primary verticals, secondary, and explicitly excluded
- Geography: target regions, excluded regions
- Company type: startup, growth-stage, enterprise, SMB
- Funding stage: bootstrapped, seed, Series A-D, public/PE-backed

**Dimension 2 -- Technographics (what they use):**
- Required stack: must-have tech, nice-to-have, incompatible
- Tech maturity: early adopter, early majority, late majority, laggard
- Current solutions: CRM, ERP, industry-specific tools
- Integration requirements: what your product must connect to
- Pain indicators: manual processes, disconnected systems, spreadsheet workarounds

**Dimension 3 -- Psychographics (how they buy):**
- Awareness stage: unaware, problem-aware, solution-aware, product-aware
- Buying committee: economic buyer, technical buyer, user buyer, champion, blocker
- Decision criteria: primary (speed, cost, features) and secondary
- Risk tolerance: budget concerns, implementation risk, change management, vendor stability

**ICP Scoring Rubric:**

| Score | Label | Action |
|-------|-------|--------|
| 80-100 | Ideal | Prioritize -- full outreach cadence, executive sponsorship |
| 60-79 | Good | Pursue -- standard cadence, qualify thoroughly |
| 40-59 | Marginal | Conditional -- only if specific signal changes (budget, timing) |
| <40 | Pass | Decline -- opportunity cost too high |

**Behavioral Signals to Watch:**
- High intent: searched for competitor alternatives, visited pricing page 3+ times, downloaded buyer's guide
- Medium intent: attended webinar, engaged with case study, connected on LinkedIn
- Low intent: blog subscriber, social follower, newsletter open

**ICP Validation Checklist:**
1. TAM/SAM/SOM calculated with minimum 1,000 companies in ICP
2. Historical win rate against ICP >30%
3. ICP customers have lowest churn and highest NPS
4. Sales team, CS, and product all agree on the profile

See `reference/gtm.md` for full YAML ICP worksheet templates and an example ICP (MEP contractors).

---

### Positioning (April Dunford Framework)

**The 5 Components of Positioning:**

1. **Competitive alternatives** -- What would customers use if you didn't exist? (Not just direct competitors -- include spreadsheets, manual processes, hiring, doing nothing)
2. **Unique attributes** -- What do you have that alternatives don't? (Features, architecture, team expertise, data, integrations)
3. **Value** -- What does the unique attribute enable for customers? (Time saved, revenue gained, risk reduced, cost avoided)
4. **Target customer** -- Who cares most about that value? (The segment where your strengths matter most)
5. **Market category** -- What market do you position in? (Existing category, subcategory, or create new category)

**Positioning Statement Template:**
```
For [target customer segment] who [key need/pain],
[product name] is a [market category]
that [primary value proposition].
Unlike [competitive alternative],
our product [key differentiator tied to unique attribute].
```

**Messaging Hierarchy (3 levels, max 3 differentiators each):**

| Level | Audience | Message Type |
|-------|----------|-------------|
| Strategic | C-suite, board | Business outcomes, ROI, risk reduction |
| Solution | Directors, VPs | Capability, integration, workflow improvement |
| Persona | End users, admins | Features, UX, daily workflow benefits |

**Competitive Battle Card Essentials:**

> **Epiphan-specific:** for Epiphan account or competitor research, use `research-skill`, not this framework skill; when a battle card needs a current Epiphan price, spec, or SKU, verify it live via `search_product_catalog` rather than from memory.

For each top-3 competitor, document:
- Overview: founded, HQ, funding, target market, pricing model
- Strengths (acknowledge honestly -- credibility requires it)
- Weaknesses mapped to your advantages
- Common objections with value-based responses
- Win strategy: lead differentiator, proof point, reference story
- Questions to ask the prospect that expose competitor weaknesses

See `reference/gtm.md` for battle card template, positioning examples, and competitive positioning framework.

---

### GTM Motion and Launch

**GTM Motion Selection:**

| Motion | ACV | Sales Cycle | Team Needed | CAC |
|--------|-----|-------------|-------------|-----|
| Product-Led Growth (PLG) | <$5K | Days | Growth/product | Low |
| Sales-Assisted | $5-50K | Weeks | SDR + AE | Medium |
| Enterprise | $50K+ | Months | AE + SE + CSM | High |
| Partner/Channel | Variable | Variable | Partner Manager | Variable |

**Channel Mix:** 60-70% primary motion, 20-30% secondary, 10% experimental.

**Launch Checklist Milestones:**
- **T-30 (Pre-launch):** ICP validated, positioning finalized, messaging hierarchy complete, battle cards created, pricing approved, sales team trained, demo environment stable
- **T-0 (Launch):** Website updated, outbound sequences activated, press release distributed, social campaign live, partner notifications sent
- **T+30 (Post-launch):** Win/loss analysis started, messaging refined from feedback, pipeline reviewed, competitive response documented, metrics dashboard active

See `reference/gtm.md` for full launch checklists, channel strategy details, and complexity-to-resource matching.

---

## Part 2: Pricing Strategy

### Value-Based Pricing Method

**Step 1 -- Quantify customer value:**
```
Total Value = Time Savings + Revenue Impact + Cost Avoidance

Time Savings:   Hours saved/month x Hourly rate x 12
Revenue Impact: Additional revenue enabled per year
Cost Avoidance: Costs eliminated or reduced per year
```

**Step 2 -- Set price at 10-20% of quantified value:**
- 10% = conservative (easy sell, high perceived value)
- 15% = balanced (standard B2B SaaS)
- 20% = aggressive (strong differentiation required)

**Step 3 -- Validate against willingness-to-pay:**
- Van Westendorp price sensitivity: ask "too cheap / cheap / expensive / too expensive"
- Competitive benchmarking: where do alternatives price?
- Customer interviews: "Would you pay $X for Y outcome?"

### Pricing Models

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| Flat rate | Simple products | Easy to understand | Doesn't scale with value |
| Per seat | Team tools | Predictable, scales with org | Discourages adoption |
| Usage-based | APIs, infra | Aligns cost with value | Unpredictable revenue |
| Tiered (Good/Better/Best) | Feature differentiation | Anchoring, clear upgrade path | Complex to design |
| Hybrid (seat + usage) | Enterprise SaaS | Predictable base + upside | Complex billing |

### Tier Design (Good/Better/Best)

**Tier structure principles:**
- 3-4 tiers optimal (more creates decision paralysis)
- Middle tier should be your target -- it gets the "Most Popular" badge
- Top tier makes middle tier look reasonable (price anchoring)
- Free tier only if PLG motion (land, qualify, viral growth)

**Feature Gating Rules:**

| Gate By | Examples | When to Use |
|---------|----------|-------------|
| Scale | Users, API calls, storage, projects | Usage naturally grows with value |
| Sophistication | Advanced analytics, AI features, workflows | Features require maturity to use |
| Control | SSO, SAML, audit logs, custom roles | Enterprise compliance needs |
| Support | SLA, dedicated CSM, phone support | Willingness to pay for service |

**Never gate:** Security features, data export, basic integrations. Gating these breeds resentment and churn.

### Discounting Strategy

> **Epiphan-specific:** discount ranges below are generic guardrails, not authorization. Current Epiphan list price, active promos, and warranty terms must come from `search_product_catalog` before quoting a real number to a prospect.

| Type | Trigger | Range | Use When |
|------|---------|-------|----------|
| Volume | Commitment to scale | 10-30% | Large seat count, multi-year |
| Term | Annual commitment | 15-25% | Monthly-to-annual conversion |
| Competitive | Switching from competitor | 20-40% | Match remaining contract value |
| Strategic | Reference customer, logo value | Up to 50% | Brand-name + case study commitment |

**Protect your pricing -- never discount when:**
- Customer hasn't articulated the value they'll receive
- No competitive pressure exists
- You're early in negotiation (discount later, not first)
- Customer is purely price-shopping (they'll churn anyway)

**Alternatives to discounting:** Extended payment terms, additional training/onboarding, extended trial period, success-milestone feature unlocks, multi-year lock-in at current rate.

### Key SaaS Pricing Metrics

| Metric | Target | Formula |
|--------|--------|---------|
| LTV | >3x CAC | ARPU / monthly churn rate |
| CAC Payback | <12 months | CAC / ARPU |
| NRR | >100% | (Start MRR + expansion - contraction - churn) / Start MRR |
| Gross Margin | >70% | (Revenue - COGS) / Revenue |

See `reference/pricing.md` for per-model deep dives, price increase playbook, services pricing, productized service model, and revenue model templates.

---

## Part 3: Opportunity Evaluation

### Quick Score (/100)

| Dimension | Points | What to Assess |
|-----------|--------|----------------|
| Market Fit | 25 | Problem clarity (10), market size (8), timing (7) |
| Technical Fit | 20 | Can I build it (10), infrastructure fit (5), maintenance burden (5) |
| GTM Fit | 20 | Sales complexity (8), channel access (7), competition (5) |
| Personal Fit | 20 | Interest/energy (8), growth potential (7), lifestyle fit (5) |
| Economics | 15 | Revenue potential (8), time to revenue (4), risk/reward (3) |

### Score Interpretation and Action

| Score | Action | Next Step |
|-------|--------|-----------|
| 80-100 | **STRONG PURSUE** | Prioritize immediately, allocate resources |
| 60-79 | **EXPLORE** | Worth a time-boxed deep dive (1-2 weeks) |
| 40-59 | **CONDITIONAL** | Park it -- revisit only if a specific factor changes |
| 0-39 | **PASS** | Decline -- opportunity cost too high |

### Red Flags (Automatic Deductions)

Any of these should subtract 10-20 points from your score:

- **Unclear payment terms:** "We'll figure out compensation later"
- **Expanding scope pre-start:** Requirements growing before contract signed
- **Pressure to decide fast:** "We need an answer by Friday" on a major commitment
- **Misaligned incentives:** Their success doesn't require your success
- **Economics don't work even optimistically:** If best-case math doesn't pencil, walk away
- **Single-threaded champion:** Only one person wants this; no organizational buy-in
- **No budget allocated:** Interested but no approved spend

### GTM Complexity Levels

| Level | Buyer | ACV | Cycle | Decision Style |
|-------|-------|-----|-------|----------------|
| PLG | Individual user | <$2K | Days | User = buyer, self-serve |
| Low-Touch | Manager | $2-15K | 1-4 weeks | Light demo, quick approval |
| Mid-Market | Director/VP | $15-100K | 1-3 months | Committee, multiple stakeholders |
| Enterprise | C-suite | $100K-1M | 6-18 months | RFP, security review, legal |
| Complex | Board-level | $1M+ | 12-36 months | Transformation project |

**Match complexity to your resources:**
- Solo / side project: target Level 1-2 max
- Small team: target Level 2-3
- Funded startup: target Level 2-4
- Enterprise sales org: target Level 3-5

### 5-Minute Viability Test

Before deep-diving any opportunity, answer four questions:

1. How much will one customer pay? $____/month
2. How many customers can I realistically get in 6 months? ____
3. What does it cost to serve one customer? $____/month
4. How many hours/week will this take? ____

**Quick math:**
- Monthly revenue at 6 months: #2 x #1
- Monthly costs: #2 x #3
- Monthly margin: Revenue - Costs
- Effective hourly rate: Margin / (hours x 4.33)
- If hourly rate < $100 --> needs rethinking

### Build vs Partner vs Buy Decision

| Signal | Build | Partner | Buy |
|--------|-------|---------|-----|
| Core differentiator | Yes | | |
| Commodity capability | | | Yes |
| Complementary strength | | Yes | |
| Time-critical | | | Yes |
| Learning value high | Yes | | |
| Maintenance burden high | | Yes | Yes |
| No good alternative exists | Yes | | |

See `reference/opportunity.md` for detailed scoring rubrics per dimension, full scorecard YAML templates, unit economics worksheets, cost structure analysis, break-even calculations, and build-vs-partner decision trees.

---

## Reference Files

- `reference/gtm.md` - ICP YAML templates, behavioral signals, validation checklist, channel strategy, launch playbooks, battle card template, positioning examples
- `reference/pricing.md` - Model deep dives, tier design, price increase playbook, services pricing, discount framework, SaaS metrics dashboard
- `reference/opportunity.md` - Full scoring rubrics (5 sections), scorecard YAML, unit economics, cost analysis, break-even formulas, build/partner/buy decision trees
</core_content>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-gtm-pricing.json`:
```json
{"ts":"[UTC ISO8601]","skill":"gtm-pricing","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"pricing_models_evaluated":[n],"tiers_designed":[n],"gtm_channels_mapped":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
**Degrade rule:** if inputs needed for a precise answer are missing (e.g. no quantified customer value for pricing, no competitor data for a battle card), don't block — proceed using clearly labeled assumptions/placeholders and flag them as low-confidence in the output, then mark status "partial" in the sidecar below.

Use status "partial" if some stages failed but results were produced (including a degraded/assumption-based pass per the rule above). Use "error" only if no output was generated.
