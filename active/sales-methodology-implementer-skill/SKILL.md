---
name: sales-methodology-implementer-skill
description: Team-wide sales methodology enablement (MEDDIC, BANT, Sandler, Challenger, SPIN, Value/Gap Selling) — generate framework discovery questions, deal scorecards, rep training plans, and qualify_lead-grounded HubSpot deal scoring. Use when: "implement MEDDIC across my team", "build a BANT scorecard", "train reps on Sandler", "score this deal using [methodology]", "30/60/90 sales enablement rollout", "standardize qualification". (For single-call prep use meddic-call-prep-auto-skill; for the Challenger narrative use challenger-sale-skill.)
---

# Sales Methodology Implementer

<objective>
Implement and scale proven sales methodologies across your team. Takes abstract frameworks (MEDDIC, BANT, Sandler, Challenger, SPIN, Value Selling, Gap Selling) and makes them concrete with discovery questions, deal scorecards, training materials, and a live HubSpot deal-scoring write-back — not just a field-naming spec.
</objective>

<quick_start>
**Trigger:** "Implement MEDDIC across my team" or "Score this deal using [methodology]"
**Input:** Methodology choice, deal type, average deal size, sales cycle length
**Output:** Framework guide, discovery questions by component, deal scorecard (scored via `qualify_lead` + written back to the HubSpot deal), training plan, delivered as a markdown doc under `[output_dir]/` (see Delivery below)
</quick_start>

<success_criteria>
- [ ] All framework components explained with discovery questions (Tier 1/2/3)
- [ ] Deal scorecard with scoring rubric and red/green flags per component
- [ ] Training plan covering 30/60/90 day implementation
- [ ] Call prep template and manager coaching guide included
- [ ] Deal score qualified via `qualify_lead` (ATL/BTL + Golden Rules) and written back to the HubSpot deal record via the Epiphan HubSpot MCP — not just specified as CRM fields for someone to create by hand
</success_criteria>

<workflow>

## Instructions

You are an expert sales enablement specialist who helps teams implement and execute proven sales methodologies.

### Supported Methodologies

| Methodology | Best For | Cycle | Deal Size |
|-------------|----------|-------|-----------|
| **MEDDIC** | Enterprise B2B, complex sales | 3-12 mo | $50K+ |
| **BANT** | SMB, transactional sales | 1-4 wk | $5K-$50K |
| **Sandler** | Consultative, avoiding "free consulting" | Varies | Varies |
| **Challenger** | Complex B2B, competitive markets | 3-9 mo | $25K+ |
| **SPIN** | Complex sales, large accounts | 3-12 mo | $50K+ |
| **Value Selling** | Competitive, commoditized markets | Varies | Varies |
| **Gap Selling** | Change-resistant prospects | Varies | Varies |

### Core Capabilities

- Generate methodology-specific discovery questions
- Create deal scorecards and qualification checklists
- Build rep training materials and playbooks
- Design pipeline stage gates aligned to methodology
- Develop coaching conversation guides for managers
- Score deals, identify gaps, predict health, flag disqualifications

### Deal Scoring & CRM Write-Back (live tool calls, not a manual field-creation guide)

When scoring an actual deal (not just generating a framework guide), don't hand the user a list of CRM
fields to go create by hand — call the tools:

1. **Qualify first:** for the Economic Buyer / Champion / Decision Process components (or the BANT
   Authority component, etc.), call `qualify_lead` (Epiphan AI) on the relevant contact(s) and read
   `power_level` (atl/btl/gray/unknown), `category`, and Golden Rules/suppression status — this is the
   single source of truth (see `skill-audit/specs/suppression-spec.md`); don't re-derive it from a
   hand-rolled title check. A non-ATL "Economic Buyer" caps that component's score rather than accepting
   the rep's self-report. If `qualify_lead` is unavailable, fall back to CLAUDE.md's ATL/BTL keyword table
   and mark the run `partial`.
2. **Locate the deal:** `hubspot_search_deals` / `hubspot_get_deal` (Epiphan HubSpot MCP) to confirm the
   deal record, current stage, and amount before writing anything back.
3. **Persist the score:** write the overall score, per-component scores, and qualification date back to
   the HubSpot deal record via the Epiphan HubSpot MCP's deal-write tool. Confirm the exact tool name
   against `epiphan-ai-mcp-guide-skill/resources/crm-tools.md` at first live use — as of this writing that
   guide documents `hubspot_search_deals`/`hubspot_get_deal` (read-only) but no deal-property write tool.
   Until a deal-write tool is confirmed, degrade to `hubspot_update_contact_note` on the deal's primary
   contact with the scorecard summary, and mark the run `partial` so Tim knows the score didn't land on
   the deal record itself.
4. Never propose Salesforce fields — Tim's stack is HubSpot only (portal `21530819` per CLAUDE.md).

### Output Format

```markdown
# Sales Methodology Implementation: [Methodology Name]

**For**: [Company/Team Name]
**Methodology**: [MEDDIC/BANT/Sandler/etc.]
**Deal Type**: [Enterprise/SMB/Mid-Market]
**Average Deal Size**: [Range]
**Sales Cycle**: [Timeline]

---

## Methodology Overview

### What is [Methodology]?
[2-3 sentence explanation]

**Best For**: [Use cases]
**Not Ideal For**: [Situations]
**Success Metrics**: [Key targets]

---

## Framework Breakdown

### [Component 1]

**Definition**: [What this component means]
**Why It Matters**: [Business impact]

**Discovery Questions**:

**Tier 1 (Essential)**:
1. "[Critical question]"
   - **Why ask**: [Reasoning]
   - **Listen for**: [Key indicators]
   - **Follow-up**: [Next question]

2. "[Second critical question]"
   - **Why ask**: [Reasoning]
   - **Listen for**: [Key indicators]

3. "[Third critical question]"

**Tier 2 (Important)**:
4. "[Deeper question]"
5. "[Validation question]"

**Red Flags**: [Warning signs that disqualify]
**Green Flags**: [Strong positive indicators]

**Score**: [X/10]
- 10/10: [Perfect qualification]
- 7-9: [Good qualification]
- 4-6: [Risky deal]
- 0-3: [Disqualified]

---

[Repeat for each framework component]

---

## Deal Scorecard

### [Opportunity Name] Qualification Score

**Overall Score**: [X]/100

| Component | Score | Status | Evidence | Risk |
|-----------|-------|--------|----------|------|
| [Component 1] | [0-10] | [status] | [Evidence] | [Level] |
| [Component 2] | [0-10] | [status] | [Evidence] | [Level] |

**Interpretation**: 90-100 (excellent) | 70-89 (solid) | 50-69 (risky) | <50 (disqualify)

---

## Deal Status: [QUALIFIED / PURSUE WITH CAUTION / DISQUALIFY]

**Strengths**: [Evidence-based strong points]
**Gaps & Risks**: [Each with impact, mitigation, urgency]
**Missing Information**: [What you still need to learn]

---

## Next Actions (Prioritized)

### Immediate (This Week)
1. **[Action]**: Purpose, target, questions to ask, success metric

### Short-term (Next 2 Weeks)
2. [Action items]

### Before Close
3. [Action items]

---

## Call Preparation Template

**Objective**: [What you want to learn]

**Questions** (in order):
1. [ ] [Tier 1 for Component 1] — If yes: [follow-up] / If no: [different path]
2. [ ] [Tier 1 for Component 2]
3. [ ] [Tier 1 for Component 3]

**Red Flags to Watch**: [Warning signs]
**Success Metrics**: [What qualifies a successful call]

---

## Manager Coaching Guide

**1-on-1 Deal Review (30 min)**:

1. **Rep Self-Assessment** (5 min): "Walk me through your scoring. What's strong? Weak?"
2. **Manager Assessment** (5 min): Score independently, note gaps
3. **Gap Analysis** (10 min): Compare scores, discuss differences, review missed flags
4. **Action Plan** (10 min): Agree on status (pursue/risky/disqualify), define next actions, set deadline

**Coaching by Scenario**:
- **Over-scored**: "What evidence do you have?" / "How do you know that's true?"
- **Under-scored**: "What green flags might you be missing?"
- **Missed questions**: "Why didn't you ask about [component]? When could you have?"

---

## 30/60/90 Day Implementation

### Days 1-30: Foundation
- Train all reps on framework
- Integrate scorecard into CRM
- Establish minimum qualification standards
- Activities: All-hands training → Individual role plays → First deal reviews → Adjust scorecard
- Target: 100% trained, 80% deals scored, pipeline cleaned via disqualification

### Days 31-60: Adoption
- Framework becomes habitual, deal quality improves
- Weekly deal certification meetings, peer review sessions
- Update call scripts, create CRM shortcuts
- Target: 90%+ completion rate, average score improves, forecast accuracy up

### Days 61-90: Optimization
- Framework is second nature, predictable outcomes
- Analyze score-to-win correlation, refine thresholds
- Build best practice library from wins
- Target: Win rate +[X]%, sales cycle -[X]%, forecast within [X]%

---

## MEDDIC Example

**Deal**: Enterprise SaaS, $200K ARR, 8-month cycle

| Component | Score | Key Evidence |
|-----------|-------|-------------|
| Metrics | 8/10 | $500K current spend, 30% savings identified |
| Economic Buyer | 6/10 | CTO identified but not met directly |
| Decision Criteria | 9/10 | Formal RFP, align on 8/10 criteria |
| Decision Process | 7/10 | Demo→Pilot→Security→Contract mapped; final authority unclear |
| Identify Pain | 9/10 | 10 hrs/week manual work, 50+ users, executive pressure |
| Champion | 10/10 | VP Eng strong champion, KPI stake, will sell internally |

**Overall**: 49/60 (82%) — PURSUE | Win Probability: 65%
**Next Action**: Schedule CTO meeting through champion

---

## CRM Write-Back (HubSpot, via Epiphan MCP)

**qualify_lead result**: [power_level ATL/BTL/GRAY for the Economic Buyer/Champion; category; suppression status]
**Deal record**: [dealId from `hubspot_get_deal`] — [confirmed / not found]
**Written to deal**: `meddic_score` [XX/100] · `qualification_date` [date] · `deal_risk_level` [Low/Med/High]
(or, if no deal-write tool was confirmed yet: **Degraded** — summary posted via `hubspot_update_contact_note`
on the primary contact instead; run marked `partial`)

No Salesforce fields are generated — Tim's stack is HubSpot only.

---

## Success Metrics

**Leading**: % deals with scorecard | Avg qualification score | Disqualification rate
**Lagging**: Win rate | Sales cycle length | Avg deal size | Forecast accuracy | Revenue per rep
**Targets**: 95%+ scorecard completion | 70+ avg score | Win rate +10-20% in 6 months | Forecast +15% in 3 months
```

### Best Practices

1. **Start with One Methodology**: Don't implement multiple frameworks at once
2. **Customize to Your Business**: Adapt questions and scoring to your sales motion
3. **Make It Easy**: Integrate scorecards directly into CRM workflow
4. **Coach Consistently**: Review deal scoring in every 1-on-1
5. **Celebrate Disqualifications**: Praise reps who disqualify bad deals early
6. **Track Over Time**: Measure correlation between scores and actual wins

### Common Use Cases

**Trigger Phrases**:
- "Implement MEDDIC across my team"
- "Create BANT qualification questions"
- "Score this deal using Challenger methodology"
- "Train reps on Sandler selling"

**Response Approach**:
1. Understand sales motion and deal characteristics
2. Generate comprehensive framework guide
3. Create methodology-specific discovery questions
4. Build scoring system aligned to their business
5. Provide training materials and coaching guides
6. When scoring a real deal: qualify via `qualify_lead`, then write the score back to the HubSpot deal via
   the Epiphan HubSpot MCP (see Deal Scoring & CRM Write-Back above) — don't just hand back a field list

Remember: The methodology is only as good as the execution. Focus on making it practical, measurable, and habitual for reps!

### Delivery

Write the full generated guide/scorecard/training plan to a markdown file at `[output_dir]/sales-methodology-<methodology>-<team-or-company>-<YYYY-MM-DD>.md`. When scoring a specific deal, also post the
scorecard summary as a HubSpot note on the deal's primary contact (`hubspot_update_contact_note`) in
addition to the deal-property write-back in the CRM Write-Back step, so the score is visible from the
CRM record itself, not only in a chat reply that gets lost.

</workflow>

<dependencies>
## MCP tools
- **Epiphan AI:** `qualify_lead` (Golden Rules / ATL-BTL / suppression gate — see `skill-audit/specs/suppression-spec.md`), `ask_agent` (deal/activity history context when scoring an existing deal)
- **Epiphan HubSpot MCP:** `hubspot_search_deals`, `hubspot_get_deal`, deal-property write tool (name TBC — see Deal Scoring & CRM Write-Back), `hubspot_update_contact_note` (degraded write-back path)

## Sibling skills referenced (reuse, don't rebuild)
- `meddic-call-prep-auto-skill` — single-call MEDDIC brief; this skill covers team-wide enablement + scoring, not per-call prep
- `challenger-sale-skill` — Challenger-specific narrative/teaching pitch
- `sales-revenue-skill` — MEDDIC/SPIN usage in the broader revenue workflow
</dependencies>

## Guardrails
- Never fabricate an Economic Buyer/Champion's authority — `power_level` comes from `qualify_lead`, not the rep's say-so.
- Never propose Salesforce fields; Tim's stack is HubSpot only (portal `21530819`).
- If the HubSpot deal-write tool can't be confirmed, degrade to a contact note and mark the run `partial` — don't silently drop the write-back.

## Self-Healing
Follows `skill-audit/specs/self-healing-template.md`. For each external call (`qualify_lead`, HubSpot
search/get/write): retry once on transient errors; degrade (CLAUDE.md ATL/BTL keyword fallback if
`qualify_lead` is down, or a contact-note write if no deal-write tool is available) and mark the run
`partial`; alert (surface a warning in the output) if a mandatory gate — ATL/BTL qualification on the
Economic Buyer — can't be evaluated at all; halt (no scorecard) if the deal/company can't be identified.
In addition to the outcome sidecar below, append one line per run to
`~/.claude/skill-runs/sales-methodology-implementer.jsonl` per the template's run-log convention.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-sales-methodology-implementer.json`:
```json
{"ts":"[UTC ISO8601]","skill":"sales-methodology-implementer","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"methodologies_implemented":[n],"scorecards_created":[n],"discovery_questions_generated":[n],"deals_scored":[n],"hubspot_writes":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (including a degraded qualify_lead
fallback or a deal-write that fell back to a contact note) — name the degraded stage in `error`. Use
"error" only if no output was generated. The `version` above must match the Skill metadata footer below,
per the template's version-consistency rule — don't hardcode it a second time.

## Skill metadata
**Version:** 1.0.0 · **Author:** Tim Kipper · **Status:** active · **Tier:** P2 (Sales Enablement)
