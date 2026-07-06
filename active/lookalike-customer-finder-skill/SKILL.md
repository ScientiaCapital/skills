---
name: lookalike-customer-finder-skill
description: Build a tiered target-account list by analyzing Epiphan's best customers (pulled live from HubSpot + CRM order history), deriving an ICP across firmographics/tech/growth, and scoring 100+ net-new lookalike companies 0-100 via Apollo/Clay expansion. Gates every surfaced company/contact through Golden Rules + qualify_lead so existing customers, channel partners, and actively-AE-owned accounts are excluded. Use when: "find companies like [customers]", "build a lookalike list", "who else looks like [account]", or expanding into a new Epiphan vertical (Higher Ed, Live Events, Corporate AV, Houses of Worship, Government, Healthcare).
---

# Lookalike Customer Finder

<objective>
Analyze Epiphan's best customers — sourced live from HubSpot + CRM order history, not recalled from memory — to build an ideal customer profile (ICP), then find 100+ net-new companies that match using firmographic data, tech stack, growth signals, and similarity scoring, expanded via Apollo/Clay. Every surfaced company and contact is gated through Golden Rules + `qualify_lead` before it reaches the output, so existing customers, channel partners, and actively-AE-owned accounts never show up disguised as "net-new lookalikes." Produces tiered target account lists ranked by match quality for account-based outreach.
</objective>

<quick_start>
**Trigger:** "find companies like [customer names]", "build a lookalike target account list", "who else looks like [account]"
**MCP Tools:** `hubspot_search_deals` / `hubspot_search_companies` / `crm_get_customer_orders` (seeds) → `apollo_organizations_enrich` / `apollo_mixed_companies_search` / Clay `find-and-enrich-company` (expansion) → `qualify_lead` (gate)
**Output:** ICP analysis, 100+ ranked lookalike companies with similarity scores (post-gate only), tiered targeting strategy, exported CSV
</quick_start>

<success_criteria>
- [ ] Seed "best customers" pulled live via `hubspot_search_deals` (closed-won) + CRM order history — never fabricated
- [ ] ICP derived from analysis of the real seed accounts (firmographics, tech, growth, behavior)
- [ ] Lookalike companies sourced via live Apollo/Clay expansion, scored 0-100 on weighted similarity model
- [ ] Every surfaced company/contact passes the Golden Rules + `qualify_lead` gate (Stage G) before inclusion — no existing customer, channel partner, or active-AE account surfaces as "net-new"
- [ ] Companies tiered into priority outreach groups (Tier 1/2/3)
- [ ] Contact intelligence (ATL/BTL/GRAY tier from `qualify_lead`) and recommended approach per top prospect
- [ ] Ranked list written to a real CSV export, not just asserted in prose
</success_criteria>

<workflow>

## Instructions

You are an expert at account-based prospecting and market analysis. Your mission is to analyze a company's best customers and find similar companies that match the same profile, creating high-quality target account lists.

### Analysis Framework

**Customer Profile Dimensions**:
1. **Firmographics** - Industry, size, revenue, location, public/private
2. **Technographics** - Tech stack, tools used, platforms
3. **Growth Signals** - Funding, hiring, expansion, momentum
4. **Behavioral** - How they buy, budget cycles, decision-making
5. **Psychographics** - Company culture, values, priorities

### Similarity Scoring

**Weighted Scoring Model**:
- Industry Match: 25%
- Company Size Match: 20%
- Tech Stack Similarity: 15%
- Growth Stage Match: 15%
- Geography Match: 10%
- Revenue Range Match: 15%

**Similarity Score**: 0-100
- 90-100: Near-perfect match
- 80-89: Strong match
- 70-79: Good match
- 60-69: Moderate match
- Below 60: Weak match

## Stage 1 — Source Seed Customers (live, HubSpot + CRM)
Never ask the analysis to run on remembered or assumed customer names. Pull the real seed set:
1. `hubspot_search_deals` filtered to closed-won (sorted by amount/recency) to identify accounts that actually bought.
2. `crm_get_customer_orders` / `crm_search_customers` to confirm device count, revenue, and order history per account — Epiphan's CRM is the source of truth for "customer" status, not `lifecyclestage` alone.
3. `hubspot_search_companies` to pull the matching company record (industry, size, domain) for each seed.
If the user names specific customers instead of asking for a general pull, still verify each one against HubSpot/CRM rather than trusting the name blind — an unverified "best customer" produces a garbage ICP downstream.

## Stage 2 — Derive the ICP
Score the Customer Profile Dimensions above (Firmographics, Technographics, Growth Signals, Behavioral, Psychographics) against the real seed accounts pulled in Stage 1 — not placeholder values.

## Stage 3 — Expand to Lookalikes (Apollo + Clay)
1. `apollo_mixed_companies_search` with filters derived from the Stage 2 ICP (industry, employee range, keywords, technologies) to surface 100+ candidate companies.
2. `apollo_organizations_enrich` on each candidate to fill firmographics, tech stack, and funding/hiring signals for the Weighted Scoring Model below.
3. Where Apollo returns incomplete data (missing tech stack, funding, or contact info), fall back to Clay's `find-and-enrich-company` waterfall.
Score every enriched candidate against the Weighted Scoring Model above.

## Stage G — Golden Rules + qualify_lead Gate (CRITICAL)
Before any candidate company or contact reaches the output (Tier 1/2/3, the ranked table, or Contact Intelligence), call `qualify_lead` on it. This is the single qualification gate — do not re-derive Golden Rules, ATL/BTL keyword tables, or suppression logic inline. Per `skill-audit/specs/suppression-spec.md`, `qualify_lead` returns `category`, `power_level` (atl/btl/gray/unknown), and a `junk` flag, and is the enforcement point for suppression state.
- **Exclude** anything `qualify_lead` flags as an existing customer, channel partner, or an account with an active AE deal inside the 90-day window (CLAUDE.md Golden Rules) — surfacing an existing customer as a "lookalike" is a bug, not a lead.
- **Surface, don't silently drop**, any `STALE AE LEAD` (AE-owned, >90 days inactive per the Golden Rules exception) — flag it in the report instead of either excluding it or treating it as fresh net-new.
- Tag every surviving contact with its `power_level` (ATL/GRAY/BTL) for Contact Intelligence — BTL-only accounts still get scored but are deprioritized, never presented as the primary contact.
- Log excluded counts by reason (customer, channel, ae_active, suppressed, junk) — these feed the Golden Rules & qualify_lead Summary in the report below.

### Output Format

```markdown
# Lookalike Customer Analysis

**Analysis Date**: [Date]
**Best Customers Analyzed**: [X] companies
**Lookalike Companies Found**: [X] companies
**Avg Similarity Score**: [X]/100

---

## 🎯 Ideal Customer Profile (ICP)

Based on analysis of your best customers:

**Firmographics**:
- **Industry**: [Primary industry] ([X]% of best customers)
- **Company Size**: [X-Y] employees (median: [X])
- **Revenue**: $[X]M - $[Y]M annually
- **Stage**: [Startup/Growth/Enterprise]
- **Geography**: [Primary regions]
- **Company Type**: [Public/Private/VC-backed]

**Tech Stack** (Common technologies):
- [Technology 1]: [X]% of best customers use
- [Technology 2]: [X]% of best customers use
- [Technology 3]: [X]% of best customers use
- [Technology 4]: [X]% of best customers use

**Growth Indicators**:
- [X]% recently raised funding
- [X]% actively hiring ([X]+ open roles)
- [X]% expanding to new markets
- [X]% launching new products

**Buying Behavior**:
- **Decision Maker**: Typically [C-level/VP/Director]
- **Deal Size**: $[X]K - $[Y]K
- **Sales Cycle**: [X] days average
- **Evaluation Process**: [Demo → Pilot → Purchase / Committee / etc.]

---

## 🏆 Your Best Customers (Reference)

### Top Customer #1: [Company Name]

**Why They're Great**:
- Revenue: $[X]K ARR
- Growth: [X]% YoY
- Engagement: [High usage, expansion, referrals]
- Profile: [Industry, size, stage]

**What They Have in Common** (with other best customers):
- All in [industry/vertical]
- All between [X-Y] employees
- All use [technology platform]
- All experiencing [growth phase]

---

## 📊 Lookalike Companies (Ranked by Similarity)

### #1 - [Company Name] | Similarity: 94/100 ⭐ EXCELLENT MATCH

**Company Profile**:
- **Industry**: [Industry]
- **Size**: [X] employees
- **Revenue**: $[X]M (estimated)
- **Location**: [City, State]
- **Founded**: [Year]
- **Stage**: [Growth stage]
- **Website**: [URL]

**Similarity Breakdown**:
- Industry: ✅ Perfect match ([same industry])
- Size: ✅ [X] employees (vs your avg [Y])
- Tech Stack: ✅ Uses [X]/[Y] common technologies
- Growth: ✅ Raised $[X]M in last 12 months
- Geography: ✅ [Same region as best customers]
- Revenue: ✅ $[X]M (within target range)

**Why They're a Great Prospect**:
1. **Same Problem**: [Specific pain point your best customers had]
2. **Buying Window**: [Indicators they're ready to buy]
3. **Budget Signals**: [Funding/growth = budget available]
4. **Tech Fit**: Already using [complementary technology]

**Contact Intelligence** (post-`qualify_lead` gate — ATL/GRAY only; BTL-only accounts flagged, not featured):
- **Decision Maker**: [Name], [Title] — `power_level`: [ATL/GRAY]
- **Champion Candidate**: [Name], [Title] — `power_level`: [ATL/GRAY/BTL]
- **Mutual Connections**: [X] 2nd degree connections
- **Recent Activity**: [Hiring/funding/expansion news]

**Recommended Approach**:
> "Hi [Name], noticed [Company] recently [growth signal]. We work with similar companies like [Best Customer 1] and [Best Customer 2] to solve [problem]. Given [their situation], thought it might be relevant..."

**Priority**: 🔴 HIGH - Reach out this week

---

### #2 - [Company Name] | Similarity: 91/100 ⭐ EXCELLENT MATCH

[Similar structure]

---

### #3-10 - Strong Matches (85-90 similarity)

| Rank | Company | Industry | Size | Score | Key Signal | Priority |
|------|---------|----------|------|-------|-----------|----------|
| 3 | [Company] | [Industry] | [X] emp | 89 | Just raised Series B | High |
| 4 | [Company] | [Industry] | [X] emp | 88 | Hiring 15+ roles | High |
| 5 | [Company] | [Industry] | [X] emp | 87 | Expanding to US | High |
| 6 | [Company] | [Industry] | [X] emp | 86 | New VP joined | Medium |
| 7 | [Company] | [Industry] | [X] emp | 86 | Product launch | Medium |
| 8 | [Company] | [Industry] | [X] emp | 85 | Same tech stack | Medium |
| 9 | [Company] | [Industry] | [X] emp | 85 | Similar customers | Medium |
| 10 | [Company] | [Industry] | [X] emp | 85 | [Signal] | Medium |

---

### #11-50 - Good Matches (70-84 similarity)

**Tier 2 Prospects** (50 companies)

Common characteristics:
- Industry: [X]% match your ICP
- Size: Slightly smaller/larger but close
- Tech: Using [X]/[Y] target technologies
- Geography: [X]% in target regions

**Export**: write the full ranked list (all tiers, post-`qualify_lead`) to `lookalike_accounts_[YYYY-MM-DD].csv` — company, domain, industry, size, similarity score, tier, ATL/BTL/GRAY contact(s), `qualify_lead` category. Don't assert an export exists without producing the file.

---

### #51-100 - Moderate Matches (60-69 similarity)

**Tier 3 Prospects** (50 companies)

Why they score lower:
- Industry adjacent but not exact
- Size outside ideal range
- Different tech stack
- Different growth stage

**Recommendation**: Reach out if you exhaust Tier 1 & 2

---

## 🔍 Market Insights

### Industry Distribution

| Industry | # Companies | % of Lookalikes |
|----------|-------------|-----------------|
| [Industry 1] | XX | XX% |
| [Industry 2] | XX | XX% |
| [Industry 3] | XX | XX% |
| Other | XX | XX% |

**Insight**: [X]% of lookalikes concentrated in [industry], suggesting strong product-market fit there.

---

### Size Distribution

| Company Size | # Companies | % of Lookalikes |
|--------------|-------------|-----------------|
| 1-50 | XX | XX% |
| 51-200 | XX | XX% |
| 201-500 | XX | XX% |
| 500-1000 | XX | XX% |
| 1000+ | XX | XX% |

**Sweet Spot**: [X-Y] employees ([X]% of best customers in this range)

---

### Geographic Distribution

| Region | # Companies | % of Lookalikes |
|--------|-------------|-----------------|
| [Region 1] | XX | XX% |
| [Region 2] | XX | XX% |
| [Region 3] | XX | XX% |

**Insight**: [Observation about geographic concentration]

---

### Growth Stage Distribution

| Stage | # Companies | % of Lookalikes |
|-------|-------------|-----------------|
| Seed | XX | XX% |
| Series A | XX | XX% |
| Series B | XX | XX% |
| Series C+ | XX | XX% |
| Bootstrapped | XX | XX% |

**Best Stage**: [Stage] companies have highest win rate

---

### Golden Rules & qualify_lead Summary

Every company/contact below already passed the Stage G gate — this section reports the gate's counts, it does not re-derive the rule:

| Excluded reason | Count |
|---|---|
| Existing customer | [X] |
| Channel partner | [X] |
| Active AE deal (<90d) | [X] |
| Suppressed (`qualify_lead` suppression state) | [X] |
| Junk / unqualified | [X] |
| **STALE AE LEAD (surfaced, not excluded)** | [X] — see flagged rows above |

Reference: `skill-audit/specs/suppression-spec.md` (enforcement point = `qualify_lead`).

---

## 🎯 Targeting Strategy

### Tier 1: Top 10

**Approach**: Highly personalized, multi-channel outreach — research each company deeply, find warm intro paths, executive-level engagement.

### Tier 2: Next 40

**Approach**: Personalized at scale — account-based sequences, industry-specific content, multi-threading.

### Tier 3: Next 50

**Approach**: Volume with relevance — segment by characteristics, nurture over time.

Response/meeting/close rate benchmarks are not invented here — track actuals per tier once sequences run (via HubSpot/Nooks), and hand tiered execution to `prospect-research-to-cadence-skill` / `sequence-load` / `nooks-autopilot`, which own outreach-cadence mechanics. This skill's job stops at a qualified, tiered, exported list.

---

## 💡 Data Sources (live MCP tools actually used)

Report which tools produced this run's data — no third-party tools that aren't wired in (Crunchbase, ZoomInfo, BuiltWith, 6sense, etc. are NOT used):

- **Seeds**: `hubspot_search_deals`, `hubspot_search_companies`, `crm_get_customer_orders` / `crm_search_customers`
- **Expansion**: `apollo_organizations_enrich`, `apollo_mixed_companies_search`, `apollo_organizations_job_postings` (hiring signals)
- **Waterfall enrichment**: Clay `find-and-enrich-company`
- **Gate**: `qualify_lead`

---

## 📈 Success Metrics

**Track These KPIs**:
- **Outreach Metrics**: Response rate, meeting rate
- **Quality Metrics**: Similarity score correlation to close rate
- **Efficiency Metrics**: Time to first meeting, sales cycle length
- **Outcome Metrics**: Win rate by similarity tier

**Hypothesis to Test**:
- Do 90+ similarity companies close faster?
- Do certain industries respond better?
- Does company size affect deal size?

---

## 🔄 Continuous Improvement

### Monthly Refresh
- Add new best customers to analysis
- Remove churned customers
- Update ICP based on recent wins
- Find new lookalikes matching updated profile

### Quarterly Review
- Analyze which lookalike tiers performed best
- Adjust similarity weightings
- Expand to adjacent markets
- Update targeting strategy

```

### Best Practices

1. **Quality Over Quantity**: 10 perfect matches > 100 mediocre ones
2. **Use Multiple Criteria**: Don't just match on industry and size
3. **Look for Growth Signals**: Companies in growth mode buy more
4. **Prioritize Recent Similarity**: Recently funded/hired companies
5. **Test and Learn**: Track which profiles actually close
6. **Refresh Regularly**: Markets change, keep list current
7. **Enrich Before Outreach**: Get contact data before campaign

### Common Use Cases

(See frontmatter `description` for trigger phrases.)

**Example Request**:
> "Who else looks like our best Higher Ed lecture-capture customers? Pull our closed-won accounts and find 100 companies with similar profiles, prioritized by similarity score."

**Response Approach**:
1. Pull seed "best customers" live from HubSpot + CRM (Stage 1) — never from memory
2. Build ideal customer profile (ICP) from the real seeds (Stage 2)
3. Expand via Apollo/Clay to 100+ candidates (Stage 3)
4. Gate every candidate through Golden Rules + `qualify_lead` (Stage G) — drop customers/channel/active-AE, surface stale-AE
5. Score survivors on similarity dimensions and rank/tier
6. Export the ranked list and hand off tiering strategy pointers

Remember: Your best future customers look a lot like your best current customers — but only if the "lookalike" isn't secretly already a customer.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-lookalike-customer-finder.json`:
```json
{"ts":"[UTC ISO8601]","skill":"lookalike-customer-finder","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"seed_customers_analyzed":[n],"lookalikes_found":[n],"icp_dimensions_scored":[n],
            "qualify_lead_excluded":[n],"stale_ae_surfaced":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>

<dependencies>
## MCP tools
- **Seeds:** `hubspot_search_deals` (closed-won), `hubspot_search_companies`, `crm_get_customer_orders` / `crm_search_customers` (Stage 1)
- **Expansion:** `apollo_organizations_enrich`, `apollo_mixed_companies_search`, `apollo_organizations_job_postings` (Stage 3)
- **Waterfall enrichment:** Clay `find-and-enrich-company` (Stage 3, fallback)
- **Gate:** `qualify_lead` — Golden Rules, dedupe, ATL/BTL/gray/junk, suppression (Stage G)

## Sibling skills referenced (reuse, don't rebuild)
- `prospect-research-to-cadence-skill` — actual outreach cadence/sequence execution for tiered accounts
- `sequence-load` / `nooks-autopilot` — enrollment + dial-list mechanics once a tier is exported

## Reference
- `skill-audit/specs/suppression-spec.md` — suppression contract and `qualify_lead` enforcement point (referenced by path, not duplicated here)

## Overlap (flagged, not removed)
This skill's ICP/scoring scope overlaps `territory-planning-optimizer`, `gtm-pricing-skill`, and `intent-signal-aggregator-skill`. No consolidation performed here — flagging only.
</dependencies>

## Guardrails
- Never hand-roll Golden Rules/ATL-BTL/suppression logic inline — `qualify_lead` is the single gate (Stage G, `skill-audit/specs/suppression-spec.md`).
- Never surface an existing customer, channel partner, or an account with an active AE deal (<90 days) as a "net-new lookalike."
- `STALE AE LEAD` accounts (AE-owned, >90 days inactive) are surfaced with a flag for Tim's review — never silently dropped, never treated as fresh net-new.
- Never create HubSpot properties/lists or write suppression state — that requires Tim's separate approval (see suppression-spec.md fallback: append-only local file, reconcile later).
- Don't assert an export exists without writing it — produce the CSV described in the Output Format section.

## Skill metadata
**Version:** 1.1 · **Author:** Tim Kipper · **Status:** active
