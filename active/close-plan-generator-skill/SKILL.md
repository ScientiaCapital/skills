---
name: close-plan-generator
title: Close Plan Generator
description: |
  Generates comprehensive close plans for Epiphan Video deals. Maps stakeholders to MEDDIC 
  roles, identifies decision processes, assesses competitive position, and creates actionable 
  next-best-actions with a close confidence score (0-100). Outputs ASCII report + optional 
  mutual action plan for prospect outreach.
version: 1.0
author: Epiphan Sales Engineering
trigger_phrases:
  - "close plan [company]"
  - "build close plan"
  - "how do I close [company]"
  - "close strategy"
  - "deal close checklist"
  - "what's blocking [company]"
  - "close plan for"
  - "closing plan"

---

<objective>
Help Epiphan AEs (Phil Sandler, Lex Evans) move deals to close by generating data-driven close 
plans that surface stakeholder dynamics, decision blocks, competitive threats, and specific 
this-week actions. Combines MEDDIC qualification, HubSpot deal data, Clari call intelligence, 
and activity momentum to assign a deal confidence score and mutual action plan.
</objective>

<quick_start>
1. Say: "close plan for [Company Name]" or "build close plan [Deal Name]"
2. Skill pulls deal stage, contacts, call history, and company context (parallel calls)
3. Outputs: Close plan report + optional Gmail draft of mutual action plan
4. Share report with BDR Tim Kipper and/or SE for final review before execution
</quick_start>

<success_criteria>
✓ Stakeholder map is complete (all contacts identified with MEDDIC roles + ATL/BTL)
✓ Close confidence score explains top 3 drivers (MEDDIC, momentum, competitive)
✓ This-week actions are specific (owner, prospect contact, deliverable, deadline)
✓ Risk register flags actual blockers (budget, legal, procurement, incumbent)
✓ Mutual action plan is ready to email or share in meeting
✓ Timeline aligns with target close date (reverse-engineered milestones)
✓ Every product/competitive claim is confirmed live via `search_product_knowledge`/`search_product_catalog` before it appears in output — never stated from memory
✓ Mutual action plan passes `check_my_copy` before any Gmail draft is created
✓ Sparse/missing Clari call data is labeled "limited call history" (not fabricated) and the run is marked partial; outcome sidecar is written
</success_criteria>

<core_content>

# Workflow

## Stage 1: Deal Discovery & Data Collection

On trigger, gather parallel data:
- **HubSpot Deal:** `hubspot_search_deals` / `hubspot_get_deal` 
  (stage, amount, close date, collaborators, notes, last activity)
- **Contacts:** `hubspot_search_contacts` on deal company, extract all contacts with:
  - Name, title, email, phone, engagement level
- **Clari Calls:** `clari_search_calls` (rep_email) + `clari_get_call_summary` 
  (pull 3-5 most recent calls with sentiment, objections, next steps)
- **Activity Timeline:** `ask_agent` question for deal momentum 
  (last 30 days: calls, emails, meetings, sentiment trend)
- **ATL/BTL Qualification:** `qualify_lead` on each contact (Epiphan-native ATL/BTL, region, category) — 
  this is the required gate for Stage 2's ATL/BTL classification; don't infer ATL/BTL from title alone.
- **Company Context:** `apollo_organizations_enrich` (industry, headcount, location, tech stack) — 
  use Apollo only to fill firmographic gaps `qualify_lead` doesn't cover.

*Parallel calls accelerate stage 1 from 2-3 min to <1 min.*

---

## Stage 2: MEDDIC Role Mapping & Stakeholder Analysis

For each contact, assign:

**MEDDIC Roles (may overlap):**
- **Economic Buyer (EB):** Budget authority, final approval
- **Champion:** Internal advocate, pushes deal forward
- **User:** Day-to-day operator, influenced by tool
- **Coach:** Insider ally, provides intel, unblocks internal process
- **Blocker:** Opposes or delays (incumbent vendor advocate, budget gatekeeper, skeptic)

**ATL/BTL Classification:**
- **ATL (Above-The-Line):** Visible, stakeholder map known to all
- **BTL (Below-The-Line):** Hidden, only coach/champion know, key for consensus
- Source each contact's ATL/BTL tier from Stage 1's `qualify_lead` call — the Epiphan-native gate, not a title guess.

**Engagement Scoring (0-10):**
- 10 = Champion, multiple recent calls, driving momentum
- 8-9 = Engaged User, attended demo, asking questions
- 5-7 = Aware but passive (email only, single call)
- 1-4 = Blocker or unaware

Output: Stakeholder table with role, ATL/BTL, engagement, risk.

---
## Stage 3: Decision Process Map

Document procurement/approval flow:
- Who signs PO? (EB name, title, typical SLA)
- Legal review required? (If yes, who, timeline, typical objections)
- Budget cycle alignment? (FY-to-date spend, remaining budget, next approval cycle)
- Vendor evaluation? (RFP process, incumbent, incumbent defense playbook)
- Competing alternatives? (Extron, Blackmagic, Crestron, vMix, Teradek—note which)

Source from: Clari call summaries, HubSpot deal notes, coach intel via activity timeline.

Output: Decision process flowchart (text-based, ASCII).

---

## Stage 4: Competitive Landscape & Displacement Strategy

**Incumbent/Alternative Assessment:**
- Who is they comparing against? (Incumbent or alternatives?)
- Incumbent advantage: What are they protecting?
- Displacement angle: Why Epiphan Pearl + Epiphan Connect?
- Battlecard: Key differentiators (price, ease of use, cloud integration, customer support)

**Product & Competitive Claim Verification (required, before any claim below is used):**
Never state an Epiphan capability, spec, or competitive differentiator from memory. Before it
appears in the battlecard, competitive summary, or mutual action plan, confirm it live via
`search_product_knowledge` / `search_product_catalog`. If a claim can't be confirmed, drop it
(don't guess) and note it as unverified in the output — this degrades the run to `partial`
(see Self-Healing).

**Epiphan Competitive Advantages (by vertical)** — illustrative starting points only; confirm
each live via `search_product_knowledge`/`search_product_catalog` before citing it in output:
- Higher Ed: NDI + Kaltura/Panopto integration, multi-campus cloud
- Courts/Legal: SRT reliability, secure RTMP/S, compliance-ready
- Live Events: Pearl Nano portability, EC20 PTZ flexibility, low latency
- Corporate AV: Pearl Mini simplicity, Epiphan Connect for hybrid work
- Houses of Worship: Affordable Pearl Nano, YouTube Live + Vimeo streaming

Output: 1-2 sentence competitive summary (specs verified live) + battlecard reference.

---

## Stage 5: Close Timeline (Reverse-Engineered)

Given target close date, work backward:
- **Close Date (T):** When signature needed?
- **T-5 days:** Legal sign-off complete
- **T-10 days:** PO approved by EB + budget confirmed
- **T-15 days:** Final demo + SOW signed
- **T-20 days:** RFP response complete (if applicable)
- **T-25 days:** Procurement kick-off, champion secures budget

Map to: Clari call sentiments, activity momentum, deal stage velocity (from `ask_agent`).

Output: Milestone calendar (text-based).

---

## Stage 6: Risk Register (Top 3)

For each risk:
- **Risk:** What could derail close?
- **Probability:** Low/Med/High
- **Impact:** Deal slip 30/60/90 days or lost entirely?
- **Mitigation:** Specific action (who, when, deliverable)

Common risks:
- Budget freeze / competing priority (mitigate: champion confirms budget with EB)
- Incumbent won RFP round (mitigate: battlecard demo vs. incumbent, customer reference call)
- Legal review delays (mitigate: pre-circulate SOW to counsel, coach escalates)
- EB disengaged (mitigate: AE calls EB directly, demo with EB + Champion together)

Output: Risk table (risk, probability, impact, owner, action, deadline).

---
## Stage 7: Next-Best-Action (This Week)

**Specific, time-bound actions for THIS WEEK:**

For each action:
- **Action:** What to do (e.g., "Send competitive battlecard + customer reference to Champion")
- **Owner:** AE, BDR, or SE?
- **Prospect Contact:** Whom to reach (name, title, email)
- **Deliverable:** What to send/share (deck, reference, SOW, demo time)
- **Deadline:** Day of week (e.g., "Tuesday EOD")
- **Success Metric:** How to know it worked (reply received, meeting scheduled, objection surfaced)

Derive from:
- Clari call objections (unaddressed concerns → action items)
- Stakeholder engagement gaps (EB disengaged → schedule EB call)
- Decision process blockers (legal review pending → pre-circulate SOW)
- Competitive threats (incumbent advantage → battlecard demo)

Output: Numbered action list (format: "1. [Action] | Owner: [AE/BDR/SE] | Contact: [Name] | Deadline: [Day]")

---

## Stage 8: Mutual Action Plan (Prospect Share)

Format as a shared document (can email or share in meeting):

```
MUTUAL ACTION PLAN: [Company] - [Product/Solution]
Date: [Today]
Close Target: [Date]

EPIPHAN COMMITMENTS:
1. [Specific deliverable] by [date] from [person]
2. [Second deliverable] by [date] from [person]
(etc.)

[PROSPECT COMPANY] COMMITMENTS:
1. [Budget confirmation] by [date] from [decision maker]
2. [Legal review / RFP response] by [date] from [approver]
(etc.)

OPEN ITEMS / RISKS:
- [Risk or open question]
- [Incumbent concern or budget question]

NEXT MEETING: [Date/Time/Format] with [stakeholders]
```

**Brand Voice Gate (required before any Gmail draft):** run `check_my_copy` (Epiphan Brand;
`get_writing_style` for voice reference) on the full mutual action plan body before creating the
draft. Resolve every flag — never stage off-voice or unverified-claim copy as a draft.

Output as Gmail draft (optional, after the Brand Voice Gate passes) or copy-paste ready.

---

## Stage 9: Close Confidence Score (0-100)

Weighted scoring framework:

**MEDDIC Completeness (25 pts):**
- EB identified + engaged (8 pts)
- Champion identified + pushing (8 pts)
- Users identified (4 pts)
- Coach confirmed (3 pts)
- No major Blockers surfaced (2 pts)

**Stakeholder Breadth + EB Engagement (20 pts):**
- 4+ contacts identified (5 pts)
- 2+ recent calls/meetings (5 pts)
- EB attended demo or call (5 pts)
- EB sent email or question last 7 days (5 pts)

**Activity Momentum (15 pts):**
- 3+ activities last 14 days (5 pts)
- Upward sentiment trend in Clari (5 pts)
- Deal stage velocity on track (5 pts)

**Competitive Position (15 pts):**
- No incumbent advantage identified (5 pts)
- Clear Epiphan differentiator vs. alternatives (5 pts)
- Battlecard executed with Champion (5 pts)

**Timeline Integrity (15 pts):**
- Target close date reasonable (5 pts)
- Milestone dates achievable based on velocity (5 pts)
- Budget approval likely by target close (5 pts)

**Champion Strength (10 pts):**
- Champion actively pushing (engagement 9-10) (5 pts)
- Champion has EB ear (5 pts)

**Score Interpretation:**
- 80-100: High confidence, proceed with close
- 60-79: Moderate, address top 2 gaps
- 40-59: Cautious, needs work on MEDDIC/momentum
- <40: At risk, reassess or reset close date

**Sparse Clari data:** if `clari_search_calls`/`clari_get_call_summary` return fewer than 2 calls
or nothing at all, do not fabricate sentiment/objections/momentum detail. Degrade Activity
Momentum and Champion Strength scoring to HubSpot notes + `ask_agent` activity timeline only,
label the report with a "limited call history" caveat, and mark the run `partial` (see
Self-Healing below).

---

# Output Format

Full ASCII Close Plan Report template and email-ready Mutual Action Plan format: see [reference/output-format.md](reference/output-format.md).

---

# Self-Healing

Follows `skill-audit/specs/self-healing-template.md`. For each external call (HubSpot, Clari,
Apollo, `qualify_lead`, `search_product_knowledge`/`search_product_catalog`, `check_my_copy`):
retry once on a transient error, then degrade rather than fail the whole run:
- **Clari sparse/unavailable:** proceed on HubSpot notes + `ask_agent` activity timeline only,
  add a "limited call history" caveat to the report (Stage 9), and mark the run `partial` —
  never invent call sentiment, objections, or next steps to fill the gap.
- **Product/competitive claim unverifiable:** `search_product_knowledge`/`search_product_catalog`
  fails or can't confirm a claim → drop that claim (don't guess), note it as unverified, mark
  `partial`.
- **`check_my_copy` fails or is unavailable:** do not create the Gmail draft; surface the mutual
  action plan as copy-paste-ready only with a flag that the brand gate didn't clear, mark `partial`.
- **`qualify_lead` unavailable:** fall back to title-based ATL/BTL heuristics (Key Definitions),
  flag the stakeholder table as "ATL/BTL not gate-confirmed," mark `partial`.
- **Alert:** if HubSpot deal/contact lookup fails outright, or every data source for the deal
  comes back empty, flag it plainly at the top of the report rather than producing a plan that
  looks complete.
- **Halt:** if the deal/company can't be identified in HubSpot at all, stop and report the error —
  don't guess which deal was meant.

In addition to the outcome sidecar below, append one line per run to
`~/.claude/skill-runs/close-plan-generator.jsonl` per the template's run-log convention.

## Emit Outcome Sidecar
As the final step, write to `~/.claude/skill-analytics/last-outcome-close-plan-generator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"close-plan-generator","version":"1.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"contacts_mapped":[n],"atl_count":[n],"btl_count":[n],"calls_pulled":[n],
            "close_confidence_score":[0-100],"claims_verified":[n],"claims_dropped_unverified":[n],
            "brand_gate_passed":[true|false]},
 "error":"[name the degraded stage, e.g. 'clari_sparse' | 'claim_unverified' | 'brand_gate_failed' | 'qualify_lead_unavailable', or null]",
 "session_id":"[YYYY-MM-DD]"}
```
Use `"partial"` for any of the degrade cases above (name the stage in `error`); use `"error"` only
if no usable close plan was produced at all (e.g. deal/company not found in HubSpot). The
`version` above must match this SKILL.md's frontmatter `version:` — don't hardcode it a second time.

---

# Dependencies

**HubSpot CRM Integration (Portal 21530819):**
- `hubspot_search_deals` — find deal by name or company
- `hubspot_get_deal` — fetch deal details (amount, stage, close date, notes)
- `hubspot_search_contacts` — find all contacts at prospect company
- `hubspot_get_contact` — contact details (title, email, phone, engagement)

**Clari Call Intelligence:**
- `clari_search_calls` — find calls by rep email or attendee
- `clari_get_call_summary` — sentiment, objections, action items (30-60 sec per call)

**Epiphan CRM AI Agent:**
- `ask_agent` — activity timeline (calls, emails, notes, meetings, sentiment trend last 30d)
- `qualify_lead` — required ATL/BTL/region/category gate for each contact (Stage 1/2); don't infer ATL/BTL from title alone
- `search_product_knowledge` / `search_product_catalog` — required live verification for any Epiphan/competitor product or competitive claim (Stage 4) before it appears in output

**Apollo Database:**
- `apollo_organizations_enrich` — company context (headcount, industry, location, tech stack); firmographic gap-fill only, not the ATL/BTL gate

**Epiphan Brand:**
- `check_my_copy` — required brand-voice gate on the mutual action plan body before any Gmail draft (Stage 8)
- `get_writing_style` — voice reference for the Brand Gate

**Gmail (Optional):**
- Create draft mutual action plan for prospect outreach (after the Brand Voice Gate passes)

**Google Calendar (Optional):**
- Check AE/prospect availability for next meeting booking

---

# Integration with Other Skills

**Cross-References:**

1. **deal-momentum-analyzer:** 
   - Close Plan Generator references momentum score for "Activity Momentum" stage
   - Use deal-momentum-analyzer output to populate Stage 1 deal health

2. **meddic-call-prep-auto:**
   - Pulls MEDDIC roles + call questions from prior prep
   - Close Plan extends MEDDIC qualification to full stakeholder map + decision process

3. **ae-handoff-brief:**
   - Close Plan builds on AE handoff context (discovery, champion, use case, budget)
   - BDR Tim Kipper uses ae-handoff-brief to qualify; AE uses close-plan-generator to close

4. **epiphan-ai-mcp-guide:**
   - Product context (Pearl-2, Pearl Mini, Pearl Nano, Pearl Nexus, EC20, Epiphan Connect)
   - CMS integrations (Kaltura, Panopto, YuJa, Echo360, Opencast)
   - Protocols (RTMP/S, SRT, HLS, NDI, RTSP)
   - Competitor profiles (Extron, Blackmagic, Crestron, vMix, Teradek)

---

# Usage Examples

Three worked examples (Enterprise Higher Ed, Corporate AV, Courts/Legal competitive displacement) with full inputs and outputs: see [reference/usage-examples.md](reference/usage-examples.md).

---

# Tips & Best Practices

Seven best practices for Phil Sandler & Lex Evans (run cadence, stakeholder mapping, Clari objections as actions, score interpretation, mutual action plan usage, BDR coordination, reference calls): see [reference/tips-best-practices.md](reference/tips-best-practices.md).

---

# Troubleshooting & FAQs

Eight common questions (missing EB, low confidence score, sparse Clari data, mutual action plan timing, incumbent price matching, renewals/expansions, when to run): see [reference/troubleshooting-faq.md](reference/troubleshooting-faq.md).

---

# Key Definitions

**MEDDIC Roles:**
- **Economic Buyer:** Controls budget, final signature authority
- **Champion:** Internal advocate, pushes deal forward, coaches you on process
- **User:** Day-to-day operator, influenced by product experience
- **Coach:** Insider ally, provides intel on decision process, unblocks obstacles
- **Blocker:** Opposes deal (incumbent advocate, risk-averse, budget gatekeeper)

**ATL (Above-The-Line):** Stakeholder visible to entire team, known to all
**BTL (Below-The-Line):** Stakeholder known only to Champion/Coach, key for consensus-building

**Close Confidence:** 0-100 weighted score across MEDDIC completeness, stakeholder engagement, momentum, competitive position, timeline, champion strength

**This-Week Actions:** Specific, time-bound, deliverable-driven actions (not vague tasks) to move deal forward in the next 5 days

**Mutual Action Plan:** Shared document with Epiphan and prospect commitments, used in meetings and follow-up emails to create accountability

---

# Version History

- **v1.0 (April 2026):** Initial release for Epiphan AEs (Phil Sandler, Lex Evans)
  - 9-stage workflow: discovery, MEDDIC mapping, decision process, competitive analysis, timeline, risk register, this-week actions, mutual action plan, confidence scoring
  - ASCII report output + Gmail draft capability
  - Integration with deal-momentum-analyzer, meddic-call-prep-auto, ae-handoff-brief, epiphan-ai-mcp-guide
  - Example workflows for Higher Ed, Corporate AV, and Courts/Legal verticals

---

# Support & Feedback

For questions or improvements:
- Slack: Reach out to Sales Engineering
- Bug reports: Note skill output, deal stage, which stage failed
- Feature requests: "Add X vertical battlecard" or "Add SE collaboration workflow"

---

# License & Attribution

Internal Epiphan Sales tool. For authorized AE use only.
Built on: HubSpot CRM, Clari Intelligence, Apollo Database, Gmail, Google Calendar

---

END OF SKILL.MD

</core_content>
