---
name: "ae-handoff-brief"
description: "Auto-generate structured AE handoff briefs when Tim books a demo for Phil Sandler or Lex Evans. Packages MEDDIC scorecard, competitive intel, discovery notes, call transcripts, and next-best-action into a single document the AE can scan in 60 seconds. Increases demo-to-close rate by ensuring AEs walk in fully prepared. Use when: 'handoff to Phil', 'handoff to Lex', 'book demo for AE', 'ae brief', 'hand off [company]', 'prep handoff', 'pass to AE', 'transition [company] to Phil', 'transition [company] to Lex', 'demo booked for [company]'."
---

<objective>
Eliminate the information gap between BDR discovery and AE demo execution. When Tim books a qualified demo for Phil Sandler or Lex Evans, this skill auto-generates a comprehensive briefing document that packages everything the AE needs: MEDDIC scorecard with gaps flagged, competitive landscape, all prior call summaries, prospect pain points, and a recommended demo flow tailored to the prospect's vertical and stated needs. Target: AE walks into every demo with 80%+ context coverage, zero cold starts.
</objective>

<quick_start>
**After booking a demo:**
"handoff Baylor University to Lex" → pulls all context → generates AE brief → creates Gmail draft to AE

**Quick handoff:**
"ae brief for University of Michigan, demo Thursday at 2pm with Phil" → full brief + calendar context

**Batch handoff:**
"hand off all demos booked this week" → generates briefs for each

**Trigger phrases:**
- "handoff [company] to Phil/Lex"
- "hand off [company]"
- "ae brief [company]"
- "book demo for AE [company]"
- "prep handoff [company]"
- "pass [company] to Phil/Lex"
- "transition [company] to Phil/Lex"
- "demo booked for [company]"
</quick_start>

<success_criteria>
- Brief generated in under 90 seconds
- All 6 MEDDIC dimensions populated (known intel + explicit gaps)
- Every prior call summarized with key moments
- Competitive landscape mapped (current vendor, why switching, battlecard)
- Recommended demo flow aligned to prospect's vertical + stated pain
- AE-specific coaching notes (what worked in discovery, what to watch for)
- Gmail draft sent to AE with brief attached/inline
- HubSpot deal updated with handoff notes
- Brief scannable in 60 seconds (executive summary format)
</success_criteria>

<workflow>

## Architecture

```
TRIGGER                      CONTEXT GATHER              SYNTHESIZE              OUTPUT
─────────────────────────────────────────────────────────────────────────────────────────
"handoff X to AE"  →  HubSpot: deal + contacts   →  MEDDIC scorecard    →  AE Brief Doc
                   →  Clari: all call summaries   →  Pain → demo map     →  Gmail Draft
                   →  Apollo: org enrichment      →  Competitive angle   →  HubSpot Note
                   →  CRM: activity history       →  Objection forecast  →  Calendar Update
                   →  Calendar: demo details       →  Demo flow rec       →
```

## Stage 1: Identify AE and Demo Context

### 1a. Parse Trigger
Extract from user input:
- **Company name**: The prospect being handed off
- **AE name**: Phil Sandler or Lex Evans
  - Phil Sandler: HubSpot owner ID `190030668`, email phillip@epiphan.com
  - Lex Evans: HubSpot owner ID `82625923`, email lex@epiphan.com
- **Demo date/time**: If mentioned, pull from calendar

### 1b. Calendar Context
| Tool | Purpose |
|------|---------|
| `get_upcoming_meetings` | Find the scheduled demo |

Extract: date, time, duration, attendees, meeting link, any agenda notes.

## Stage 2: Context Gathering

Run these MCP calls in parallel:

### 2a. HubSpot Context (Full Deal Picture)
| Tool | Purpose |
|------|---------|
| `hubspot_search_companies` | Company record: lifecycle, industry, employee count |
| `hubspot_search_contacts` | All contacts associated: titles, emails, engagement |
| `hubspot_search_deals` | Active deals: stage, amount, close date, notes, collaborators |
| `hubspot_get_deal` | Detailed deal properties + activity log |

**Golden Rules check:** Verify deal is properly staged for handoff:
- Deal should be at "Presentation Scheduled" or "Qualified to Buy" stage
- Tim should be owner or collaborator
- If deal is at earlier stage, flag: "⚠️ Deal may not be fully qualified for AE demo"

### 2b. Clari Call History (All Prior Conversations)
| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find ALL calls with prospect contacts (last 90 days) |
| `clari_get_call_summary` | AI summary + action items for each call |

For each contact associated with the deal:
1. `clari_search_calls(attendeeEmail=contact_email, daysBack=90)`
2. For ALL calls found: `clari_get_call_summary(callId=call_id)`
3. Sort chronologically and extract:
   - **Call-by-call progression**: How did discovery evolve?
   - **MEDDIC dimensions uncovered per call**: What was learned when?
   - **Objections raised**: What pushback did prospect give?
   - **Competitor mentions**: Any incumbent or alternative named?
   - **Action items**: Resolved and unresolved

### 2c. Apollo Enrichment (Org Intelligence)
| Tool | Purpose |
|------|---------|
| `enrich_contact` | Each attendee: title, seniority, department, LinkedIn |

### 2d. CRM Activity History
| Tool | Purpose |
|------|---------|
| `ask_agent` | Full engagement timeline: emails, calls, page views, form fills |

### 2e. Competitive Intel Check
| Tool | Purpose |
|------|---------|
| `gmail_search_messages` | Check for competitive intel reports mentioning this prospect |

## Stage 3: MEDDIC Scorecard Compilation

Compile everything known across ALL discovery touchpoints into a unified MEDDIC scorecard.

### M — Metrics
- **Known**: [Specific metrics from calls]
- **Unknown**: [What's still missing]
- **AE should ask**: [Specific question to fill the gap]

### E — Economic Buyer
- **Identified**: [Name, title, confirmed budget authority — ATL/BTL validated]
- **On the demo?**: [Yes/No — if no, flag as risk]

**ATL/BTL Validation (per CLAUDE.md § ATL/BTL Classification v1.0):**
Map ALL known contacts to ATL/BTL tiers. If no ATL contact is on the demo invite, this is a RED FLAG.

### D — Decision Criteria
- **Stated**: [What prospect said they'll evaluate]
- **Inferred**: [Based on vertical]
- **AE should validate**: [Confirm criteria during demo]

### D — Decision Process
- **Timeline**: [When they want to decide/deploy]
- **Stakeholders**: [Who else is involved]
- **AE should map**: [Missing pieces of the buying process]

### I — Identify Pain
- **Primary pain**: [Strongest pain point from discovery — quote the prospect]
- **Trigger event**: [What caused them to look now]

### C — Champion
- **Identified**: [Name + title + evidence of championing behavior]
- **AE should test**: [Champion validation question]

## Stage 4: Demo Flow Recommendation

| Vertical | Lead Feature | Close Angle |
|----------|-------------|-------------|
| Higher Ed | Multi-room capture + CMS auto-publish | "Cover [X] rooms by [semester]" |
| Courts/Legal | Automated recording + compliance archival | "Never miss a recording + audit trail" |
| Corporate AV | Meeting room capture + NDI/SRT streaming | "Standardize AV across [X] locations" |
| Government | Secure streaming + archival | "Broadcast public meetings + training" |
| Healthcare | HIPAA-friendly recording + cloud mgmt | "Record and distribute training at scale" |
| Houses of Worship | Live streaming + multi-camera | "Stream every service without a crew" |
| K-12 | Classroom capture + LMS integration | "Record every classroom, one dashboard" |

## Stage 5: Objection Forecast

| Predicted Objection | Source | Recommended Response |
|--------------------|---------|--------------------|
| [Objection from prior calls] | Clari call [date] | [LAER response] |
| [Objection typical for this vertical] | Vertical pattern | [Battlecard response] |

## Stage 6: Output Format

See `reference/ae-handoff-template.md` for full brief layout (MEDDIC scorecard table, discovery timeline, competitive landscape, recommended demo flow, objection forecast).

## Stage 7: Delivery

### 7a. Gmail Draft to AE
**To:** [Phil: phillip@epiphan.com | Lex: lex@epiphan.com]
**Subject:** AE Brief: [Company Name] — Demo [Date]

Use `gmail_create_draft` with the brief content.

### 7b. HubSpot Deal Update
Add a note via `ask_agent`: "BDR Handoff Brief generated [date]. MEDDIC: [X/6]. AE: [name]."

</workflow>

<dependencies>
## Required MCP Tools
- **Epiphan CRM MCP:** hubspot_search_companies, hubspot_search_contacts, hubspot_search_deals, hubspot_get_deal, ask_agent, get_upcoming_meetings
- **Epiphan Clari MCP:** clari_search_calls, clari_get_call_summary
- **Apollo/Enrichment MCP:** enrich_contact
- **Gmail MCP:** gmail_create_draft, gmail_search_messages

## Sibling Skills Referenced
- `meddic-call-prep-auto` — Shares MEDDIC synthesis logic
- `call-recording-analyzer` — Provides call-by-call MEDDIC scores
- `deal-momentum-analyzer` — Deal health context for the AE
</dependencies>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-ae-handoff-brief.json`:
```json
{"ts":"[UTC ISO8601]","skill":"ae-handoff-brief","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"briefs_generated":[n],"meddic_coverage_pct":[n],"calls_analyzed":[n],"ae_drafts_created":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
