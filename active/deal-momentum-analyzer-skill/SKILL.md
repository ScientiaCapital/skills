---
name: "deal-momentum-analyzer"
description: "Deal health scoring + next-best-action for every open deal. Pulls HubSpot deals, CRM activity history, and engagement data to flag stalled deals, predict close probability, and recommend specific recovery actions. Runs daily at 7am CST or on-demand. Use when: 'deal health', 'pipeline review', 'stalled deals', 'deal momentum', 'which deals need attention', 'morning brief', 'SOD'."
---

<objective>
Score every open deal on momentum (not just stage) using multi-signal analysis: days in stage, activity recency, stakeholder engagement, call/activity sentiment, and MEDDIC completeness. Surfaces the 3-5 deals most likely to slip and prescribes specific next-best-actions to recover them. Target: recover 5-10% of stalled pipeline monthly (~$18K/mo at current pipeline levels).
</objective>

<quick_start>
**Daily automated run (7am CST):**
Scheduled task pulls all open deals → scores momentum → delivers prioritized action list

**On-demand:**
"deal momentum" → runs full analysis now
"pipeline review" → same, formatted as pipeline review
"which deals need attention" → filtered to at-risk only

**Trigger phrases:**
- "deal health" / "deal momentum"
- "pipeline review" / "stalled deals"
- "which deals need attention"
- "morning brief" / "SOD" (integrates into daily brief)
</quick_start>

<success_criteria>
- Every open deal scored 0-100 on momentum
- Deals classified: GREEN (on-track), YELLOW (slowing), RED (stalled)
- Top 3-5 at-risk deals surfaced with specific next-best-action
- Weekly trend: are deals accelerating or decelerating?
- Target: recover 5-10% of stalled deals per month via timely intervention
- Zero false negatives on deals about to slip close date
</success_criteria>

<workflow>

## Architecture

```
SCHEDULED (7am CST)          ANALYSIS                    OUTPUT
─────────────────────────────────────────────────────────────────
HubSpot: all open deals  →  Score each deal on     →  Prioritized dashboard
CRM: activity history    →  6 momentum signals     →  Next-best-action per deal
Activity: emails/calls   →  Classify G/Y/R         →  Gmail draft (optional)
                          →  Compare to last run    →  Calendar blocks (optional)
```

## Stage 1: Data Collection

### 1a. Pull All Open Deals (Owner OR Collaborator)
Use `search_crm_objects` (HubSpot MCP) with **two OR-ed filter groups** to capture both owned and collaborated deals:

**FilterGroup 1 — Tim is COLLABORATOR:**
- `hs_all_collaborator_owner_ids` CONTAINS_TOKEN `87486452`
- `hs_is_closed` EQ `false`

**FilterGroup 2 — Tim is OWNER:**
- `hubspot_owner_id` EQ `87486452`
- `hs_is_closed` EQ `false`

**Properties to request:**
`dealname`, `dealstage`, `amount`, `hubspot_owner_id`, `hs_lastmodifieddate`, `notes_last_updated`, `closedate`, `pipeline`, `createdate`, `hs_all_collaborator_owner_ids`, `num_associated_contacts`, `hs_deal_stage_probability`

Sort by `hs_lastmodifieddate` DESCENDING. Limit 100.

For each deal, capture:
| Field | HubSpot Property |
|-------|-----------------|
| Deal name | `dealname` |
| Amount | `amount` |
| Stage | `dealstage` |
| Close date | `closedate` |
| Create date | `createdate` |
| Last activity | `notes_last_updated` or `hs_lastmodifieddate` |
| Owner | `hubspot_owner_id` |
| Collaborators | `hs_all_collaborator_owner_ids` |
| Associated contacts | via associations |
| Associated company | via associations |

### 1a-bis. Deal Role Tagging
After pulling deals, tag each deal with Tim's role:
- **OWNER** — `hubspot_owner_id` = `87486452` → Tim owns the deal directly
- **COLLABORATOR** — `hs_all_collaborator_owner_ids` contains `87486452` but `hubspot_owner_id` ≠ `87486452` → Tim is helping close (AE-owned or SE-owned deal)

**Display both types** in the momentum report. Collaborator deals where an AE owns them (owner IDs 82625923 Lex Evans, 423155215 Ron Epstein, 190030668 Phillip Sandler) are deals Tim sourced or is actively supporting — they ARE his pipeline contribution and must be tracked.

**Exclude from scoring** only deals where Tim is NEITHER owner NOR collaborator (i.e., deals that somehow appeared but have no Tim involvement).

### 1b. Clari Call Intelligence (Signal 4 Data Source)

Pull recent Clari call data for contacts associated with each deal:

| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find calls involving deal contacts (filter by attendeeEmail, last 30 days) |
| `clari_get_call_summary` | Get AI summary + action items for each relevant call |

For each deal's associated contacts:
1. Search Clari calls: `clari_search_calls(attendeeEmail=contact_email, daysBack=30)`
2. For calls found: `clari_get_call_summary(callId=call_id)` 
3. Extract:
   - **Call sentiment**: positive/neutral/negative from AI summary
   - **Discovery completeness**: were MEDDIC questions asked?
   - **Competitor mentions**: any competitor names in summary
   - **Action items**: unresolved action items = stall risk
   - **Last call date**: recency signal for Signal 4 scoring

**Signal 4 Enhancement (Call Momentum — 15 points):**
| Sub-signal | Points | Criteria |
|-----------|--------|----------|
| Clari call in last 7 days | 5 | Recent engagement confirmed |
| Positive sentiment | 4 | AI summary = positive/constructive |
| MEDDIC questions asked | 3 | Discovery topics covered in transcript |
| No unresolved action items | 2 | All action items closed |
| No competitor mentions | 1 | Clean competitive position |

If no Clari data found, fall back to HubSpot activity recency (existing logic). Never score 0 just because Clari is empty.

### 1c. Pull Activity History
For each deal's associated company, use `ask_agent`:
- Query: "Show all activity, notes, and engagement for [company] deals in last 30 days"
- Extracts: call notes, email activity, meeting outcomes, deal stage changes

### 1c. Pull Contact Engagement
For each deal's associated contacts, use `hubspot_search_contacts`:
- Last email open/click dates
- Form submissions
- Page views
- Meeting bookings

## Stage 2: Momentum Scoring (0-100)

Score each deal on 6 weighted signals:

### Signal 1: Days in Current Stage (25 points)
| Condition | Points |
|-----------|--------|
| < median for this stage | 25 |
| At median | 15 |
| 1.5x median | 8 |
| > 2x median | 0 |

Stage medians (calibrate from Tim's historical data):
| Stage | Expected Days |
|-------|--------------|
| Appointment Scheduled | 7 |
| Qualified to Buy | 14 |
| Presentation Scheduled | 10 |
| Decision Maker Bought-In | 14 |
| Contract Sent | 7 |
| Closed Won | — |

### Signal 2: Activity Recency (20 points)
| Last activity | Points |
|--------------|--------|
| < 3 days ago | 20 |
| 3-7 days | 15 |
| 7-14 days | 8 |
| 14-21 days | 3 |
| > 21 days | 0 |

### Signal 3: Stakeholder Breadth (15 points)
**ATL/BTL Validation Required (see CLAUDE.md § ATL/BTL Classification v1.0):**
For each deal's associated contacts, classify by title before scoring:
- **ATL:** Chief, VP, Director, Dean, Provost, Superintendent, Court Administrator, City Manager, Senior Pastor, Executive Pastor
- **GRAY:** Manager (AV/Facilities/IT) — only counts as ATL-equivalent if confirmed budget >$25K
- **BTL:** Technician, Specialist, Coordinator, Support, Administrator (Systems/Network/Database), Engineer, Operator, Instructor/Faculty, Designer, Assistant, Clerk (non-Court Admin), Volunteer, Intern, Student, Resident, Help Desk
- **NEVER ATL:** Warehouse Manager, Network Manager, Systems Administrator, AV Technician, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew

| Contacts engaged | Points |
|-----------------|--------|
| 3+ contacts, including at least 1 ATL-tier contact (confirmed EB) | 15 |
| 2+ contacts with at least 1 ATL-tier | 12 |
| 2+ contacts but ALL are BTL/GRAY (no confirmed ATL) | 7 |
| 1 contact (champion only, regardless of tier) | 5 |
| 1+ contacts but ALL are NEVER ATL titles | 2 |
| 0 active contacts | 0 |

**Penalty flag:** If a deal has 0 ATL-tier contacts, add a ⚠️ flag in the report: "NO ECONOMIC BUYER IDENTIFIED — deal at risk of stalling at Decision Maker stage. Action: ask champion to intro Director+/VP+."

### Signal 4: Call Momentum (15 points)
Uses Clari call data as primary signal source (see Stage 1b: Clari Call Intelligence).

| Activity signal | Points |
|-------------|--------|
| Call in last 7 days + positive sentiment | 15 |
| Call in last 7 days + neutral | 10 |
| Call in last 14 days | 7 |
| No calls in 14+ days | 0 |
| Negative sentiment on last call | -5 (penalty) |

**Data sources:**
- Primary: Clari call summaries (via `clari_search_calls` + `clari_get_call_summary`)
- Fallback: HubSpot activity recency if no Clari data available

### Signal 5: MEDDIC Completeness (15 points)
Estimate from available data:
| MEDDIC fields identified | Points |
|-------------------------|--------|
| 5-6 of 6 dimensions | 15 |
| 3-4 dimensions | 10 |
| 1-2 dimensions | 5 |
| 0 dimensions | 0 |

### Signal 6: Close Date Integrity (10 points)
| Condition | Points |
|-----------|--------|
| Close date in future, never pushed | 10 |
| Close date pushed once | 6 |
| Close date pushed 2+ times | 2 |
| Close date in the past (overdue) | 0 |

### Classification
| Score | Classification | Action Priority |
|-------|---------------|----------------|
| 70-100 | GREEN — On Track | Monitor |
| 40-69 | YELLOW — Slowing | Intervene this week |
| 0-39 | RED — Stalled | Intervene TODAY |

## Stage 3: Next-Best-Action Engine

For each YELLOW/RED deal, prescribe specific action:

### Action Matrix
| Primary Signal Gap | Recommended Action | Tool |
|-------------------|-------------------|------|
| No activity > 14 days | Send re-engagement email | `gmail_create_draft` |
| No calls > 14 days | Book a check-in call | `gcal_create_event` |
| Single-threaded (1 contact) | Research + reach additional stakeholder | `apollo_mixed_people_api_search` |
| No economic buyer identified | Ask champion to intro EB | Call script |
| Close date overdue | Propose new timeline in email | `gmail_create_draft` |
| Negative call sentiment | Address objection head-on | Call prep brief |
| Competitor mentioned | Pull competitive battlecard | Research |
| MEDDIC gaps | Discovery questions for next call | MEDDIC brief |

### Action Output Format
For each action, provide:
1. **What:** Specific action description
2. **Why:** Which signal triggered this
3. **How:** Draft email / calendar invite / talking point ready to use
4. **When:** Today / This week / Before [close date]

## Stage 4: Output Format

```
╔══════════════════════════════════════════════════════════════╗
║  DEAL MOMENTUM REPORT — [Date]                               ║
║  Pipeline: $[total] | Deals: [count] | Weighted: $[weighted] ║
╠══════════════════════════════════════════════════════════════╣

SUMMARY:
🟢 GREEN: [X] deals ($[amount]) — on track
🟡 YELLOW: [X] deals ($[amount]) — slowing, intervene this week
🔴 RED: [X] deals ($[amount]) — stalled, intervene TODAY

TREND vs LAST RUN:
- Deals improved: [X] (moved from RED→YELLOW or YELLOW→GREEN)
- Deals declined: [X] (moved down)
- New deals: [X]
- Pipeline delta: [+/- $amount]

═══════════════════════════════════════════════════════════════

🔴 PRIORITY ACTIONS (do these today):

1. [Deal Name] — $[amount] | Stage: [stage] | Score: [XX/100]
   ⚠️ Signals: [days in stage: 28 | no activity: 18 days | single-threaded]
   → ACTION: [specific next-best-action]
   → DRAFT: [ready-to-send email or talking points]

2. [Deal Name] — $[amount] | Stage: [stage] | Score: [XX/100]
   ⚠️ Signals: [close date overdue | negative call sentiment]
   → ACTION: [specific next-best-action]
   → DRAFT: [ready-to-send email or talking points]

═══════════════════════════════════════════════════════════════

🟡 WATCH LIST (intervene this week):

3. [Deal Name] — $[amount] | Score: [XX/100]
   → [brief action recommendation]

═══════════════════════════════════════════════════════════════

🟢 ON TRACK:

[Deal list with scores, sorted by close date]

╚══════════════════════════════════════════════════════════════╝
```

</workflow>

<scheduled_automation>
## Daily 7am CST Run

This skill is designed to run as a scheduled task:

**Schedule:** Daily at 7:00 AM CST (13:00 UTC)
**Task name:** "deal-momentum-daily"
**Scheduling options:**
- **Session-based:** `CronCreate "57 6 * * 1-5"` with prompt `"Run deal-momentum-analyzer"` (3-day auto-expire, must re-create each session)
- **Persistent:** launchd agent at `~/Library/LaunchAgents/com.tim.deal-momentum.plist` (future work)
- **On-demand:** Tim says "deal momentum" or "morning brief"

**Flow:**
1. Pull all open deals from HubSpot
2. Score each deal on 6 momentum signals
3. Classify GREEN/YELLOW/RED
4. Generate next-best-actions for YELLOW/RED
5. Create Gmail drafts for recommended re-engagement emails
6. Output report (saved to workspace + presented in morning brief)

**Integration with SOD/Morning Brief:**
When Tim says "morning brief" or "SOD", this report is included as the pipeline section.
</scheduled_automation>

<dependencies>
## Required MCP Tools
- **Epiphan CRM MCP:** hubspot_search_deals, hubspot_search_companies, hubspot_search_contacts, hubspot_get_deal, hubspot_get_company, hubspot_get_contact, ask_agent (activity history, stage velocity medians, pipeline coverage, deal conversion benchmarks)
- **Epiphan Clari MCP:** clari_search_calls, clari_get_call_summary (for call sentiment analysis and momentum scoring)
- **Apollo MCP:** apollo_mixed_people_api_search, apollo_people_match (for multi-threading actions)
- **Gmail MCP:** gmail_create_draft (for re-engagement email actions)
- **Google Calendar MCP:** gcal_create_event (for booking check-in calls)
- **Scheduling:** CronCreate (session-based, 3-day max) or launchd (persistent)

## Sibling Skills Referenced
- `hubspot-revops-skill` — HubSpot query patterns, pipeline stage definitions
- `sales-revenue-skill` — MEDDIC framework, pipeline coverage benchmarks
- `meddic-call-prep-auto-skill` — Generates full call prep when action = "book a call"
- `portfolio-artifact-skill` — Captures deal recovery metrics for GTME portfolio
</dependencies>
