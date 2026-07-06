---
name: "meddic-call-prep-auto"
description: "Auto-generate MEDDIC-structured call prep scripts from prospect context. Pulls HubSpot deal + contact data, Apollo enrichment, CRM activity history, and calendar context to build a complete demo/discovery brief in 60 seconds. Use when: 'call prep', 'prep me for', 'demo prep', 'discovery prep', 'meddic brief', 'prep [company]', 'get me ready for [company]'."
---

<objective>
Eliminate 15-20 minutes of manual demo prep per call. Auto-generates a MEDDIC-structured briefing by pulling context from HubSpot (deal stage, properties, notes), Apollo (contact enrichment, org data), CRM activity history (via ask_agent), and Google Calendar (meeting details + attendees). Outputs a single actionable brief with talking points, objection prep, and competitive intel.
</objective>

<quick_start>
**Before a call:**
"call prep Baylor University" → pulls all context → generates MEDDIC brief

**Before a demo:**
"demo prep for University of Michigan, meeting at 2pm" → adds demo-specific flow

**From calendar:**
"prep my next call" → reads next calendar event → auto-identifies company → runs full prep

**Trigger phrases:**
- "call prep [company]"
- "prep me for [company]"
- "demo prep [company]"
- "discovery prep [company]"
- "meddic brief [company]"
- "prep my next call"
- "get me ready for my [time] meeting"
</quick_start>

<success_criteria>
- Complete MEDDIC brief generated in under 60 seconds
- All 6 MEDDIC dimensions populated (even if some are "UNKNOWN — ask this")
- Prior conversation context included from CRM activity history
- Competitive displacement angle identified if relevant
- Attendee roles mapped to MEDDIC roles (champion, economic buyer, etc.)
- 3 personalized discovery questions generated from enrichment data
- Brief fits on one screen (scannable in 30 seconds before call)
</success_criteria>

<workflow>

## Pipeline

```
TRIGGER              CONTEXT GATHER              SYNTHESIZE              OUTPUT
───────────────────────────────────────────────────────────────────────────────
"call prep X"  →  Calendar: meeting details  →  Map attendees to   →  MEDDIC Brief
               →  HubSpot: deal + contact    →  MEDDIC roles       →  Talking Points
               →  Apollo: enrichment         →  Identify gaps       →  Questions
               →  CRM: activity history    →  Competitive angle   →  Objection Prep
               →  Epiphan CRM: device check  →  Pain hypothesis     →  Next Steps
```

## Stage 1: Context Gathering

Run these MCP calls in parallel:

### 1a. Calendar Context
| Tool | Purpose |
|------|---------|
| `gcal_list_events` | Find the meeting (by company name or next upcoming) |
| `gcal_get_event` | Get attendees, description, meeting link |

Extract: attendee names + emails, meeting time, any agenda in description.

### 1b. HubSpot Context
| Tool | Purpose |
|------|---------|
| `hubspot_search_companies` | Company record — lifecycle, owner, properties |
| `hubspot_search_contacts` | Contact records for each attendee |
| `hubspot_search_deals` | Active deals — stage, amount, close date, notes |

Extract: deal stage, deal amount, lifecycle stage, prior notes, form submissions, page views.

### 1c. Apollo Enrichment
| Tool | Purpose |
|------|---------|
| `apollo_organizations_enrich` | Company firmographics, tech stack, employee count |
| `apollo_people_match` | Each attendee — title, seniority, department |
| `apollo_organizations_job_postings` | Active AV/IT hiring = buying signal |

### 1d. Clari Conversation History
| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find prior calls with this prospect (by attendeeEmail, last 90 days) |
| `clari_get_call_summary` | Get AI summary, action items, key moments for each call |

For each attendee email:
1. `clari_search_calls(attendeeEmail=attendee_email, daysBack=90)`
2. For up to 3 most recent calls: `clari_get_call_summary(callId=call_id)`
3. Extract:
   - **Prior conversation topics**: What was discussed last time?
   - **Unresolved action items**: What did we promise to follow up on?
   - **Competitor mentions**: Were Extron, Blackmagic, Crestron, vMix, Teradek mentioned?
   - **Objections raised**: Price, features, integration concerns?
   - **MEDDIC gaps from prior call**: Which dimensions were NOT covered?

### 1e. Prior Conversation Context
| Tool | Purpose |
|------|---------|
| `ask_agent` | Query activity history, deal notes, and engagement timeline from CRM data warehouse |
| `hubspot_get_deal` | Pull deal notes and activity log for associated deals |

Query `ask_agent` with: "Show recent activity, notes, and engagement history for [company name] in the last 90 days"

Extract: what was discussed, commitments made, objections raised, next steps promised.

### 1f. Competitive Intelligence Context
Check for stored competitive intel from the bdr-v3-competitive-intel daily task:
1. Search Gmail for recent competitive intel reports: `search_threads(query="subject:competitive-intel from:me newer_than:7d")`
2. If company or competitor was mentioned in recent Clari extractions, pull the relevant battlecard context
3. Integrate into MEDDIC brief:
   - **If competitor mentioned in Clari calls**: Include displacement talking points
   - **If no competitor mentioned**: Include proactive competitive positioning for top 2 competitors in prospect's vertical
   - **Specific objection rebuttals**: Map Clari objections to prepared responses

**Non-negotiable: spec/competitor live-verification gate.** Before emitting the displacement table or any spec/price/competitor-status claim in the brief, call `search_product_catalog` (SKUs, pricing, short names) and/or `search_product_knowledge` (technical/integration/EOL status) to confirm it's current — per the `epiphan-call-playbook` technical-accuracy gate. Specs and competitor claims (e.g. "discontinued", "EOL") must never be stated from memory in the output brief. The table below is a fallback only for when live lookup is unavailable; if used as a fallback, mark it `⚠️ UNVERIFIED — confirm before the call` in the brief.

**Competitive Quick Reference (by vertical) — fallback only, confirm live before use:**
| Vertical | Primary Competitor | Displacement Angle |
|----------|-------------------|-------------------|
| Higher Ed | Extron SMP (last known: discontinued) | Extron EOL → Pearl migration path |
| Corporate AV | Crestron | Pearl = simpler, no programmer needed |
| Houses of Worship | vMix | Pearl = hardware reliability, no PC crashes |
| Healthcare | Blackmagic | Pearl = HIPAA-friendly, Connect cloud mgmt |
| Courts/Legal | Teradek | Pearl = all-in-one, no separate encoder needed |

### 1g. Epiphan CRM Check
| Tool | Purpose |
|------|---------|
| `crm_search_customers` | Existing customer match — devices, orders, channel relationship |
| `analytics_search_by_email` | Device registration lookup by contact email |

**Golden Rules / suppression gate:** Call `qualify_lead` for the primary contact(s) on this deal — it is the single source of truth for Golden Rules, ATL/BTL, and suppression (per `skill-audit/specs/suppression-spec.md`); do not re-derive customer/channel/AE-owned status from raw HubSpot/CRM fields. If `qualify_lead` returns `junk` or a suppression/Golden-Rules category (customer, channel partner, AE-owned <90 days), STOP and skip this prep.
  - **Fallback (qualify_lead unavailable):** apply the Golden Rules inline as a degraded check — `lifecyclestage = 'customer'` or `device_count >= 1` → existing customer; `is_channel = true` → channel partner; `hubspot_owner_id` IN ('82625923', '423155215', '190030668') → AE-owned (Lex Evans, Ron Epstein, Phillip Sandler) with the 90-day stale exception per CLAUDE.md — and mark the brief `partial` in the outcome sidecar since the gate was degraded.

**Exception:** If Tim explicitly says 'prep me for [company]' and the company is flagged (by `qualify_lead` or the fallback), generate the brief but add a ⚠️ WARNING banner at the top: 'This is an EXISTING customer/channel partner/AE deal. Coordinate with the owner before reaching out.'

## Stage 2: MEDDIC Synthesis

Map gathered context into MEDDIC framework:

### M — Metrics
- **Known:** Any quantifiable goals mentioned in prior calls or deal notes
- **Hypothesis:** Based on vertical benchmarks (e.g., "Universities your size typically manage 50-200 rooms")
- **Ask if unknown:** "How are you measuring success for this project?"

### E — Economic Buyer
- **Known:** Map attendees by seniority → VP/Director/Dean = likely EB
- **ATL/BTL Validation (MANDATORY — route through `qualify_lead`):** For each attendee, call `qualify_lead` and read its `power_level` (`atl` / `btl` / `gray` / `unknown`) — this is the single gate for ATL/BTL classification (per `skill-audit/specs/suppression-spec.md`); do not re-derive it from a hand-rolled title keyword table.
  - `power_level = atl` → Mark EB as ✅ IDENTIFIED
  - `power_level = gray` → Confirm budget authority before treating as EB. Ask: "Does [name] control the budget for this purchase, or do they need approval from someone above them?" (full gray-zone criteria, e.g. the $25K delegated-budget threshold for AV/Facilities/IT Managers, are defined in CLAUDE.md § ATL/BTL Classification v1.0 — `qualify_lead` applies them, this skill doesn't re-implement them)
  - `power_level = btl` → Mark EB as ⚠️ NOT IDENTIFIED — need to find the person who signs the PO. Do not list BTL/junk-flagged titles as potential EBs.
  - `power_level = unknown` (e.g. `qualify_lead` unavailable) → fall back to CLAUDE.md § ATL/BTL Classification v1.0 title matching, and mark the brief `partial` in the outcome sidecar since the gate was degraded.
- **Unknown attendees:** Flag for discovery ("Who controls the budget for this?")
- **Signal:** If only BTL/technical staff on call, EB isn't engaged yet — flag as ⚠️ and add discovery question: "Who would sign off on this purchase?"

### D — Decision Criteria
- **Known:** From prior call notes, form submissions, or deal properties
- **Hypothesis:** Based on vertical (Higher Ed cares about CMS integration + room scale; Courts care about compliance + reliability)
- **Standard criteria:** Price, features, CMS integration, support, ease of use

### D — Decision Process
- **Known:** Timeline from deal properties, procurement notes
- **Ask if unknown:** "What's your evaluation timeline? Who else needs to weigh in?"
- **Red flag:** No clear process = deal likely stalls

### I — Identify Pain
- **Known:** Pain expressed in prior calls, form submission context
- **Hypothesis:** Based on trigger signal (hiring = scaling pain; Extron exit = replacement pain)
- **Ask if unknown:** "What's broken about your current setup?"

### C — Champion
- **Known:** Who initiated contact? Who's been most engaged?
- **Test:** "If this made sense, would you advocate for it internally?"
- **Red flag:** No champion identified after 2nd call

## Stage 3: Output Format

```
╔══════════════════════════════════════════════════════════════╗
║  CALL PREP: [Company Name]                                   ║
║  [Date] [Time] | [Meeting Type: Discovery/Demo/Follow-up]    ║
╠══════════════════════════════════════════════════════════════╣

ATTENDEES & ROLES:
┌─────────────────────────────────────────────────────────────┐
│ [Name] — [Title] → MEDDIC Role: [EB/Champion/User/Coach]   │
│   LinkedIn: [url] | Email: [email]                          │
│   Context: [personalization note from enrichment]           │
├─────────────────────────────────────────────────────────────┤
│ [Name 2] — [Title] → MEDDIC Role: [...]                    │
└─────────────────────────────────────────────────────────────┘

DEAL STATUS:
- Stage: [stage] | Amount: [$XX,XXX] | Close: [date]
- Days in stage: [X] | Last activity: [date]

MEDDIC SCORECARD:
┌───────────────────────┬──────────┬──────────────────────────┐
│ Dimension             │ Status   │ Key Intel / Gap          │
├───────────────────────┼──────────┼──────────────────────────┤
│ M — Metrics           │ ✅/⚠️/❌ │ [what we know or need]  │
│ E — Economic Buyer    │ ✅/⚠️/❌ │ [identified or not]     │
│ D — Decision Criteria │ ✅/⚠️/❌ │ [known criteria]        │
│ D — Decision Process  │ ✅/⚠️/❌ │ [timeline/blockers]     │
│ I — Identify Pain     │ ✅/⚠️/❌ │ [stated pain or hypo]   │
│ C — Champion          │ ✅/⚠️/❌ │ [who + engagement]      │
└───────────────────────┴──────────┴──────────────────────────┘

PRIOR CONVERSATION CONTEXT:
[CRM activity summary or "No prior activity found"]
- Key commitments: [...]
- Objections raised: [...]
- Follow-ups promised: [...]

COMPETITIVE INTEL:
🆚 COMPETITOR STATUS
[Detection result from Clari calls or CRM]

If competitor detected:
```
Competitor detected: [name] (from Clari call on [date])
Displacement angle: [specific talking point]
Objection prep: [specific rebuttal to raised objection]
Key differentiator: [most relevant Pearl advantage]
```

If no competitor detected:
```
No competitor identified — lead with [vertical-specific value prop]
```

DISCOVERY QUESTIONS (ask these):
1. [Personalized question based on trigger/enrichment]
2. [MEDDIC gap-filling question]
3. [Competitive displacement question]

OBJECTION PREP:
| Likely Objection | Response |
|------------------|----------|
| "We're happy with current setup" | [response] |
| "Budget is tight" | [response] |
| "Need to evaluate others" | [response] |

CALL AGENDA (suggested):
1. [2 min] Rapport + confirm agenda
2. [5 min] Discovery: pain + metrics
3. [10 min] Demo / value prop aligned to pain
4. [3 min] Decision process + next steps

╚══════════════════════════════════════════════════════════════╝
```

## Stage 4: Delivery (optional — durable artifact)
The terminal brief above doesn't survive the chat session. If Tim asks to save/share the prep, or by default when prepping for a meeting >2 hours out, deliver one of:
- **Gmail draft:** `create_draft` to `tkipper@epiphan.com` with the brief as the body (subject: `Call Prep: [Company] — [Date]`).
- **Saved HTML:** render the same content to a self-contained HTML file for quick reference/sharing.
Skip delivery (terminal-only) for "prep my next call" quick-lookups run just before a call.

</workflow>

<demo_prep_addon>
When trigger is "demo prep" instead of "call prep", append:

## Demo Flow (RECAP → AGENDA → SHOW VALUE → SUMMARIZE → NEXT STEPS)

1. **RECAP** (2 min): "Last time we discussed [prior activity summary]. You mentioned [pain]. Did I capture that right?"
2. **AGENDA** (1 min): "Today I'll show you [feature aligned to pain], then we'll discuss [decision criteria]."
3. **SHOW VALUE** (10 min): Demo path aligned to their vertical:
   - Higher Ed: Multi-room capture → CMS auto-publish → room scheduling
   - Courts: Automated recording → compliance archival → failover
   - Corporate: Meeting room capture → NDI/SRT streaming → cloud management
4. **SUMMARIZE** (2 min): "You mentioned [metrics] — here's how Pearl delivers [quantified value]."
5. **NEXT STEPS** (2 min): "What would a pilot look like? Who else should see this?"
</demo_prep_addon>

<dependencies>
## Required MCP Tools
- **Google Calendar MCP:** gcal_list_events, gcal_get_event
- **Epiphan CRM MCP:** hubspot_search_companies, hubspot_search_contacts, hubspot_search_deals, hubspot_get_deal, crm_search_customers, analytics_search_by_email, ask_agent (activity history queries), `qualify_lead` (Golden Rules / ATL-BTL / suppression gate), `search_product_catalog`, `search_product_knowledge` (spec/competitor live-verification gate)
- **Apollo MCP:** apollo_organizations_enrich, apollo_people_match, apollo_organizations_job_postings
- **Clari MCP (NEW):** clari_search_calls, clari_get_call_summary
- **Gmail MCP:** search_threads (for competitive intel reports), create_draft (optional delivery, Stage 4)

## Sibling Skills Referenced
- `sales-revenue-skill` — MEDDIC framework, objection handling (LAER), demo flow
- `prospect-research-to-cadence-skill` — Shares enrichment logic, Golden Rules filter
- `hubspot-revops-skill` — HubSpot query patterns, deal stage definitions
- `epiphan-call-playbook` — source of the technical-accuracy gate pattern reused above (Stage 1f)
</dependencies>

## Self-Healing

Follows `skill-audit/specs/self-healing-template.md`. For each external call (HubSpot, Apollo, Clari, Calendar, qualify_lead): retry once on transient errors, degrade to a lesser source and mark the run `partial` (e.g. `qualify_lead` down → CLAUDE.md keyword fallback above; Clari down → skip prior-call context), alert (flag in the brief) if a mandatory gate — Golden Rules or the spec-verification gate — can't be evaluated at all, and halt (no brief) if the company/deal can't be identified. In addition to the outcome sidecar below, append one line per run to `~/.claude/skill-runs/meddic-call-prep-auto.jsonl` per the template's run-log convention.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-meddic-call-prep-auto.json`:
```json
{"ts":"[UTC ISO8601]","skill":"meddic-call-prep-auto","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"calls_prepped":[n],"meddic_fields_filled":[n],"contacts_enriched":[n],"economic_buyers_identified":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (including a degraded Golden-Rules/qualify_lead fallback or a skipped spec-verification lookup) — name the degraded stage in `error`. Use "error" only if no output was generated. The `version` above must match the Skill metadata footer below, per the template's version-consistency rule — don't hardcode it a second time.

## Skill metadata
**Version:** 1.0.0 · **Author:** Tim Kipper · **Status:** active · **Tier:** P1 (Core BDR Automation)
