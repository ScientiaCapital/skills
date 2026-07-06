---
name: "sales-revenue"
description: "Umbrella B2B sales skill for Epiphan Video — qualification-gated lead scoring, pipeline/revenue metrics, and MEDDIC/SPIN discovery + demo execution for Pearl devices, EC20 PTZ, and Epiphan Connect across Higher Ed/Government/Corporate AV/Healthcare/Courts/K-12/Houses of Worship. Use for lead scoring, cold outreach, and pipeline reviews; for deep-dive demo scripts see demo-execution-playbook-skill, for MEDDIC call prep see meddic-call-prep-auto-skill, for cold-email copy see cold-email-sequence-generator-skill, for negotiation see challenger-sale-skill / never-split-the-difference-skill."
---

<objective>
Comprehensive B2B sales skill for Epiphan Video BDRs covering cold outreach to video/streaming verticals (Higher Ed, Government, Corporate AV, Courts/Legal, Healthcare, K-12, Houses of Worship), lead scoring for Pearl-2/Mini/Nano/Nexus/EC20/Connect, revenue operations (pipeline metrics, forecasting, LTV:CAC), and sales execution (MEDDIC qualification, SPIN discovery, demo delivery for video capture/streaming workflows, objection handling for video capture/streaming/NDI/SRT).
</objective>

<quick_start>
**Lead scoring:** Hot: 70+ | Warm: 40-69 | Nurture: <40

**Pipeline coverage:** 3-4x quota (SMB), 4-5x (Enterprise)

**LTV:CAC ratio:** Target >3:1

**MEDDIC:** Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion

**Cold email:** Under 100 words, problem-forward (video capture, streaming, hybrid/remote), clear single CTA

**Tim's 2026 Quota (full ramp since June):** 24 deals/mo, $714K pipeline/mo; H2 revenue targets rise monthly ($475K Jul → $600K Dec) — read the current month's row from the comp plan table in CLAUDE.md. Stretch = 126%+ (1.5x accelerator). 50+ daily dials, 8-12% connect rate, <60 min speed to lead
</quick_start>

<config>
## Declared reference values (single source of truth for this file)

Everywhere else in this skill, reference the two tables below instead of re-listing owner IDs or ICP
scores inline — this keeps the skill from drifting when CLAUDE.md's Golden Rules or ICP scoring change.

**AE owner IDs (`hubspot_owner_id`) — Golden Rule 4, 90-day stale exception scope:**
| AE | Owner ID | Stale-exception (>90d no activity) scope |
|----|----------|-------------------------------------------|
| Lex Evans | `82625923` | North America only (USA/Canada) |
| Ron Epstein | `423155215` | All regions |
| Phillip Sandler | `190030668` | North America only (USA/Canada) |

If last activity is <90 days, respect ownership and exclude regardless of AE.

**ICP vertical scores** (feeds `icp_fit` 0-30 scoring factor and tier/priority notes):
| Vertical | Score |
|----------|-------|
| Higher Ed | 90 |
| Courts/Legal | 85 |
| Government | 80 |
| Corporate AV | 80 |
| Healthcare | 75 |
| Houses of Worship | 70 |
| K-12 | 65 |

Full ATL/BTL keyword lists live in CLAUDE.md § ATL/BTL Classification v1.0 (canonical) — the fallback
copy in the Qualification Gate below is a degrade path, not a second source of truth.
</config>

<success_criteria>
Sales process is successful when:
- Leads scored and tiered (Gold/Silver/Bronze) before outreach
- Pipeline coverage at 3-4x quota minimum
- LTV:CAC ratio >3:1
- MEDDIC criteria documented for each qualified opportunity
- Demo follows RECAP → AGENDA → SHOW VALUE → SUMMARIZE → NEXT STEPS
- Objections handled with LAER (Listen, Acknowledge, Explore, Respond)
</success_criteria>

<core_content>
Comprehensive B2B sales skill: outreach, revenue operations, and demo execution.

## Quick Reference

| Domain | Key Components | Reference File |
|--------|---------------|----------------|
| **Outreach** | Cold email, sequences, domain warming, lead scoring | `reference/outreach.md` |
| **Revenue Ops** | Pipeline metrics, forecasting, dashboards, attribution | `reference/revenue-ops.md` |
| **Discovery** | MEDDIC, SPIN, demo flow, objection handling | `reference/discovery.md` |

---

## Part 1: Sales Outreach

### The GTM Pipeline (Epiphan Video)

```
Apollo Discovery → Lead Scoring → ICP Filtering → Apollo Sequences → Clay Enrichment → CRM Routing
      ↓              ↓              ↓               ↓                 ↓               ↓
   Apollo MCP    sales-agent    Epiphan ICP   Apollo MCP         Clay MCP      Epiphan CRM MCP
```

### Lead Tiering (Epiphan Video)

| Tier | Criteria | Priority | Action | Exclude |
|------|----------|----------|--------|---------|
| GOLD | Demo request, pricing inquiry, Pearl family inquiry, general contact us | Immediate | Personalized Apollo sequence | lifecyclestage='customer', device_count≥1, is_channel=true, AE-owned (Lex, Phil, Ron, Anthony) |
| SILVER | Content download (whitepapers), free guide download, Facebook Lead Ads from video/streaming content | Week 1 | Standard Apollo sequence | First conversion contains 'setup', 'Pearl', 'Connect', 'signup'; product usage in engagement_overview |
| BRONZE | Webinar/lecture symposium attendance, newsletter signup | Nurture | Drip campaign + nurture flow | |

### Qualification Gate (Pre-Sequence) — `qualify_lead` is mandatory
Per `skill-audit/specs/suppression-spec.md`, **`qualify_lead` is the single gate.** Call it immediately
after the initial candidate pull (Gate A: dedupe) — **before** any ATL/BTL tiering, enrichment spend
(Apollo/Clay), Apollo sequence enrollment, or Gmail draft creation. `qualify_lead` returns `category`
(ideal_mql/warm/nurture/junk), `power_level` (atl/btl/unknown), region, and a junk flag — treat this as
authoritative over any inline keyword table. Drop junk; hold GRAY/unknown for Tim's review per the
90-day stale-AE exception (see `<config>`); never auto-enroll BTL.

**Fallback (only if `qualify_lead` is unavailable):** classify by title against these keyword lists.
This is a documented degrade path, not a second source of truth — if `qualify_lead` comes back online
mid-run, re-qualify anything already routed off the fallback before it goes further down the funnel.
- **ATL (auto-approve for sequence):** Chief, VP, Director, Dean, Provost, Superintendent, Court Administrator, City Manager, Senior Pastor, Executive Pastor
- **GRAY (require Tim's review):** Manager (AV/Facilities/IT) — only if confirmed reports to Director+ with budget >$25K
- **BTL (deprioritize):** Technician, Specialist, Coordinator, Support, Administrator (Systems/Network/Database), Engineer (AV/Network/Systems), Operator, Instructor/Professor/Faculty, Designer (Learning/Instructional/Graphic), Assistant, Clerk (non-Court Admin), Volunteer, Intern, Student, Resident, Help Desk
- **NEVER sequence (hard block):** Warehouse Manager, Network Manager, Systems Administrator, AV Technician, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew

See CLAUDE.md § ATL/BTL Classification v1.0 for full vertical-specific patterns.

### Lead Scoring (0-100) — Epiphan Video

```python
scoring_factors = {
    'icp_fit': 0-30,              # per-vertical score — see ICP vertical scores table in <config>
    'intent_signals': 0-25,       # Pearl inquiry, CMS integration (Kaltura, Panopto, YuJa), streaming protocol (RTMP/S, SRT, HLS, NDI)
    'engagement': 0-20,           # Email opens, clicks, replies, website visits to Pearl product pages
    'timing': 0-15,               # Budget cycle (edu = spring/summer, govt = fiscal year), event season (conferences)
    'budget_signals': 0-10        # Company size, multi-campus/location, existing AV investment
}
# Thresholds: Hot: 70+ | Warm: 40-69 | Nurture: <40
```

### 6-Agent Architecture (Epiphan MCP Tools)

| Agent | Role | MCP Tool | Output |
|-------|------|----------|--------|
| RESEARCHER | Company intel, tech stack (Extron SMP EOL?, Blackmagic, Crestron, vMix, Teradek presence) | Clay MCP | Enriched company data + competitor intel |
| QUALIFIER | Mandatory dedupe/qualify gate, then ICP fit scoring (vertical + device readiness) | `qualify_lead` (Epiphan AI) + Epiphan CRM MCP + ask_agent | category/power_level/junk flag, 0-100 score + tier |
| ENRICHER | Contact discovery for `qualify_lead`-approved leads only — ATL-first: VP/Director/Dean/CIO/CTO/Provost (ATL), then Manager (GRAY — flag for review). Exclude NEVER-ATL titles per CLAUDE.md § ATL/BTL v1.0 (fallback keyword table in Qualification Gate above) | Apollo MCP | Verified emails, org chart, buying signals, ATL/BTL tier |
| WRITER | Personalized Apollo sequences (Pearl pain points, CMS integrations) | Apollo MCP | Multi-step email campaign |
| ANALYZER | Reply intent (demo request vs nurture vs disqualify) | Gmail MCP + Epiphan CRM MCP | Route to next action |
| ROUTER | Orchestration (add to sequence, update HubSpot, schedule follow-up) | Calendar MCP + Epiphan CRM MCP | Next-best-action |

### Cold Email Principles (Epiphan Video)

1. **Short and specific** - Under 100 words
2. **Problem-forward** - Lead with their pain (hybrid lecture capture, board meeting recording, multi-location streaming, NDI/RTMP integration, CMS workflow)
3. **Clear CTA** - One ask (usually 10-min Pearl product demo or technical fit call)
4. **Personalization** - Company name + vertical signal (e.g., "I noticed you're in Higher Ed using Panopto...")
5. **Brand gate (mandatory)** - Before finalizing any generated copy, run it through `get_writing_style` / `check_my_copy`. Do not send copy that hasn't passed the brand-voice check.

### Outreach Delivery Path (Draft-First)
Per CLAUDE.md's Gmail Draft Workflow mandate, **default outbound is a Gmail draft, not a direct send or
auto-fired sequence step**, for any lead-specific/high-touch touch (GOLD tier, STALE AE LEAD re-engagement,
1:1 follow-ups): create via `create_draft`, Tim reviews/edits/sends. Apollo sequences are for the
automated multi-step SILVER/BRONZE nurture cadence (Apollo Email Sequence Structure below) — even then,
a lead only enters an Apollo sequence after it has cleared the Qualification Gate (`qualify_lead`) above.

### Apollo Email Sequence Structure (Epiphan Video)

| Step | Timing | Purpose | Example |
|------|--------|---------|---------|
| 1 | Day 0 | Initial outreach - video capture pain point | "Hybrid lectures + lecture capture best practice" |
| 2 | Day 3 | Follow-up - different angle (CMS integration or protocol) | "How are you integrating Kaltura/Panopto?" |
| 3 | Day 7 | Value add - case study or Pearl comparison | "Why Higher Ed departments prefer Pearl Mini over [competitor]" |
| 4 | Day 10 | Break-up - last chance + link to free trial/webinar | "One last thing: 15-min free Pearl fit assessment" |

---

## Part 2: Revenue Operations

### Core Metrics

#### Pipeline Metrics

```yaml
pipeline_coverage:
  formula: "Pipeline Value / Quota"
  healthy: "3-4x for SMB, 4-5x for Enterprise"
  warning: "Below 3x"

pipeline_velocity:
  formula: "(# Opps x Win Rate x Avg Deal) / Cycle Days"
  use: "Predict monthly revenue"

weighted_pipeline:
  formula: "Sum of (Deal Value x Stage Probability)"
```

#### Conversion Funnel

| Stage | Formula | Benchmark |
|-------|---------|-----------|
| Lead to MQL | MQLs / Total Leads | 15-30% |
| MQL to SQL | SQLs / MQLs | 30-50% |
| SQL to Opp | Opportunities / SQLs | 50-70% |
| Opp to Win | Closed Won / Opportunities | 20-30% |
| Overall | Closed Won / Total Leads | 1-5% |

#### Unit Economics

| Metric | Formula | Healthy |
|--------|---------|---------|
| CAC | (Sales + Marketing) / New Customers | Depends on ACV |
| LTV | (ARPU x Gross Margin) / Churn Rate | - |
| LTV:CAC | LTV / CAC | >3:1 |
| Payback | CAC / (ARPU x Gross Margin) | <12 months |

### Pipeline Stages

| Stage | Probability | Entry Criteria |
|-------|-------------|----------------|
| Lead | 5% | Contact captured |
| MQL | 10% | Meets ICP |
| SQL | 20% | BANT confirmed |
| Discovery | 30% | Meeting scheduled |
| Demo | 50% | Demo completed |
| Proposal | 70% | Proposal sent |
| Negotiation | 85% | Terms discussed |
| Closed Won | 100% | Contract signed |

### Forecasting Methods

| Method | Formula | Best For |
|--------|---------|----------|
| Pipeline-based | Sum(Deal x Stage Probability) | Simple, data-driven |
| Historical | Historical conversion x Pipeline | Past performance |
| Commit-based | Rep commits + Manager adjustment | Incorporates judgment |

---

## Part 3: Demo & Discovery

### Call Structure

| Stage | Goal | Duration |
|-------|------|----------|
| Opening | Build rapport, set agenda | 2-3 min |
| Discovery | Uncover pain, qualify | 15-20 min |
| Demo | Show relevant value | 15-20 min |
| Close | Agree next steps | 5 min |

### SPIN Questioning

| Type | Purpose | Example |
|------|---------|---------|
| **S**ituation | Understand context | "Walk me through your current process..." |
| **P**roblem | Surface pain | "What challenges do you face with...?" |
| **I**mplication | Deepen pain | "What happens when that goes wrong?" |
| **N**eed-Payoff | Envision solution | "If you could fix that, what would change?" |

### MEDDIC Qualification

| Letter | Element | Key Question |
|--------|---------|--------------|
| **M** | Metrics | What's the measurable impact? |
| **E** | Economic Buyer | Who controls budget? |
| **D** | Decision Criteria | How will they decide? |
| **D** | Decision Process | What are steps to buy? |
| **I** | Identify Pain | What's compelling reason to act? |
| **C** | Champion | Who's selling internally? |

### Demo Best Practices

```
1. RECAP (2 min)
   "Based on our discovery, you mentioned [pain 1], [pain 2]..."

2. AGENDA (1 min)
   "I'll show how we address each. Stop me anytime."

3. SHOW VALUE (15-20 min)
   Pain -> Feature -> Benefit -> Proof (repeat for each pain)

4. SUMMARIZE (2 min)
   "So you'd be able to [benefit 1], [benefit 2]..."

5. NEXT STEPS (5 min)
   "What questions? What's our next step?"
```

### Demo Rules

1. **Show, don't tell** - Open the product, demonstrate
2. **Connect to pain** - Every feature tied to their problem
3. **Pause for reactions** - "How does that compare to current?"

### Objection Handling (LAER)

```
L - Listen (fully, don't interrupt)
A - Acknowledge (validate the concern)
E - Explore (understand the root)
R - Respond (address specifically)
```

<methodology_integration>
## Methodology Integration

Sales-revenue integrates with the strategy skill cluster for first-principles selling:

**Discovery Calls:**
- Use **JTBD Forces of Progress** to identify what's pushing the prospect to switch
- Use **Challenger's Teach-Tailor-Take Control** to structure the conversation around a commercial insight
- Use **NSTTD calibrated questions** ("What does success look like?") instead of closed questions

**Cold Outreach:**
- Lead with a **Challenger reframe** (not product features)
- Open with an **NSTTD accusation audit** ("You probably get dozens of vendor emails...")
- Frame the CTA as a **no-oriented question** ("Would it be out of the question to...?")
- Under 100 words, technically precise

**Objection Handling:**
- Use **NSTTD labeling** to name the objection: "It seems like timing is a concern..."
- Apply **Challenger's assertive redirect** to steer back to value
- Use **calibrated questions** to make them solve YOUR problem: "How am I supposed to do that?"

**Price Negotiations:**
- Use the **Ackerman model** (65% → 85% → 95% → 100% with precise final number)
- Anchor with **Challenger rational drowning** (quantify the problem before discussing price)

See: `challenger-sale-skill`, `never-split-the-difference-skill`, `jobs-to-be-done-skill`
</methodology_integration>

**Product-knowledge gate (mandatory before any spec/competitive claim):** the table below (TCO, NDI/SRT
support, Kaltura native integration, etc.) is illustrative framing, not a source of current specs. Before
stating a spec, competitive comparison, or TCO number in a live objection response or demo script, verify
it via `search_product_catalog` / `search_product_knowledge` — never assert Pearl/competitor specs from
memory.

| Objection | Response Framework (Epiphan) |
|-----------|-------------------|
| "Too expensive" | Acknowledge -> "Compared to Extron SMP or Blackmagic?" -> Show Total Cost of Ownership (Pearl-2 vs legacy + integration) |
| "We use [Blackmagic/Crestron/vMix]" | Acknowledge -> "What pain points?" -> Differentiate (Pearl = portable, NDI + SRT, Kaltura native integration) |
| "Not ready / testing phase" | Acknowledge -> "When's your pilot window?" -> Offer 30-day trial of Pearl Mini + Epiphan Connect |
| "Need IT approval" | Acknowledge -> "What will IT ask?" -> Prepare tech brief on NDI/RTMP/SRT support, security |
| "Looking at free option" | Acknowledge -> "OBS works, but what about reliability + support?" -> Show Pearl value (pro support, firmware updates, CMS integration) |

---

## Call Prep Checklist (Epiphan Video)

```markdown
### Research (10 min)
- [ ] Company website - video/streaming mentions, CMS (Kaltura/Panopto/YuJa/Echo360)
- [ ] LinkedIn - prospect AV/IT/Broadcast background
- [ ] Tech stack - BuiltWith (CDN, video), job postings (streaming engineer?)
- [ ] Competitor presence - Extron, Blackmagic, Crestron, vMix, Teradek

### Preparation (5 min)
- [ ] Hypothesis: Hybrid lectures? Multi-location streaming? CMS integration pain?
- [ ] 3 discovery questions ready (Pearl capability fit, current workflow, CMS integration)
- [ ] Pearl demo environment ready (focus on their vertical: K-12 classroom? University lecture hall? Government broadcast?)
- [ ] Clear next step in mind (trial, technical assessment, peer reference call)

### Mindset
- [ ] Curiosity about their video workflow, not pitch mode
- [ ] Understand their AV/IT ecosystem first (NDI? RTMP? SRT comfort level?)
```

---

## Weekly Pipeline Review Template

```markdown
### Coverage Check
- Current pipeline: $___
- Quota this month: $___
- Coverage ratio: ___x (target: 3-4x)

### Stage Movement
| Stage | Start | End | Net |
|-------|-------|-----|-----|
| Discovery | | | |
| Demo | | | |
| Proposal | | | |

### Deals at Risk
| Deal | Amount | Days in Stage | Risk |
|------|--------|---------------|------|

### Action Items
- [ ] Stalled deals to address
- [ ] Proposals to follow up
- [ ] Deals to close this week
```

---

## Integration Notes (Epiphan Video)

- **Email Sequences:** Apollo.io (MCP connected) — use for GOLD/SILVER tier outreach
- **CRM:** HubSpot (Epiphan CRM MCP connected) — sync deals, track device_count and engagement_overview
- **Enrichment:** Apollo MCP (contact discovery), Clay MCP (company intel + competitor tech stack)
- **Discovery Tools:** Gmail MCP (reply detection), Google Calendar MCP (schedule follow-ups)
- **Channel Partners:** AVI-SPL, Diversified, CTI, CCS Presentation Systems, Ford AV (cross-check is_channel=true to exclude)
- **ATL/BTL Classification:** See CLAUDE.md § ATL/BTL Classification v1.0 — approved title patterns for decision-maker identification across all 7 ICP verticals (2026-03-17); gated through `qualify_lead` per the Qualification Gate above
- **Related Skills (umbrella vs. specialist):** this skill is the BDR umbrella; route to `demo-execution-playbook-skill` for deep-dive demo scripts, `sales-methodology-implementer-skill` / `meddic-call-prep-auto-skill` for MEDDIC call prep, `cold-email-sequence-generator-skill` for cold-email copy generation, `challenger-sale-skill` / `never-split-the-difference-skill` for negotiation framing
- **Products:** Pearl-2, Pearl Mini, Pearl Nano, Pearl Nexus, EC20 PTZ, Epiphan Connect
- **Verticals / ICP scores:** see ICP vertical scores table in `<config>`
- **CMS Integrations:** Kaltura, Panopto, YuJa, Echo360, Opencast
- **Streaming Protocols:** RTMP/S, SRT, HLS, NDI, RTSP

## Output Contracts (per mode)

| Mode | Delivery | Notes |
|------|----------|-------|
| Lead scoring / tiering | Tiered list (Gold/Silver/Bronze) with score breakdown | Input to outreach, not sent anywhere |
| Cold outreach (GOLD, STALE AE LEAD, 1:1) | Gmail draft via `create_draft` (draft-first, default) | Tim reviews/edits/sends — never auto-sent |
| Cold outreach (SILVER/BRONZE nurture) | Apollo sequence enrollment | Only after the Qualification Gate (`qualify_lead`) above; brand-gated copy |
| Pipeline review | Weekly Pipeline Review Template (below) | For Tim / pipeline syncs |
| Call prep / demo | Call Prep Checklist + Demo flow (below) | Spec claims pass the product-knowledge gate above |

## Golden Rules — EXCLUDE These Leads

**DO NOT OUTREACH if ANY of these conditions are true (mirrors what `qualify_lead` enforces —
see Qualification Gate above; this table is the documented fallback):**
- `lifecyclestage = 'customer'` — Already a customer, route to AE/CSM
- `first_conversion_source` contains 'Pearl', 'setup', 'Connect', 'signup' — Already converting/onboarding
- `company.device_count >= 1` — Has active devices, route to AE/CSM
- `engagement_overview` contains product usage data — Already engaged, notify AE
- `is_channel = true` — Channel partner, route to channel manager
- `hubspot_owner_id` matches an AE in the AE Owner IDs table (`<config>`) → **90-day stale exception** applies per that table's scope column: if no activity >90d, surface as STALE AE LEAD for Tim (ATL/BTL + deal value). <90d = respect ownership, exclude.

**Action:** Before adding to Apollo sequence, query Epiphan CRM MCP to validate lead state (in addition to, not instead of, the `qualify_lead` gate).

## Failure Handling (MCP degrade ladder)

Apollo / Clay / Epiphan CRM MCP calls can fail mid-run. Ladder, per call:
1. **Retry once** (transient error only).
2. **Skip + log** the affected lead/stage with reason; continue the run — don't let one failed enrichment call halt the whole batch.
3. **Alert Tim** in the run output if the same MCP tool fails 3+ times in one run (likely an outage, not a fluke) — e.g. "Apollo MCP degraded: N enrichments skipped."
4. **Halt** only if `qualify_lead` itself is unavailable AND the keyword-list fallback also can't be applied (e.g. no title data) — never silently ship unqualified leads.

Append each run to `~/.claude/skill-runs/sales-revenue.jsonl`: `{ts, stage, mcp_tool, status, leads_affected, note}` per failure, in addition to the outcome sidecar below.

---

## Reference Files

- `reference/outreach.md` - Email templates, Apollo sequences, Pearl messaging by vertical
- `reference/revenue-ops.md` - Metrics, dashboards, forecasting, pipeline health
- `reference/discovery.md` - MEDDIC scorecard, Pearl demo scripts, objection library (video capture specific)

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-sales-revenue.json`:
```json
{"ts":"[UTC ISO8601]","skill":"sales-revenue","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"emails_generated":[n],"calls_scripted":[n],"leads_qualified":[n],"pipeline_value":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
</core_content>
