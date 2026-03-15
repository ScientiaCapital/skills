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

### 1a. Pull All Open Deals
Use `hubspot_search_deals` with filters:
- `dealstage` NOT IN closed-won, closed-lost
- Sort by `closedate` ascending (nearest close dates first)

For each deal, capture:
| Field | HubSpot Property |
|-------|-----------------|
| Deal name | `dealname` |
| Amount | `amount` |
| Stage | `dealstage` |
| Close date | `closedate` |
| Create date | `createdate` |
| Last activity | `notes_last_updated` or `hs_last_activity_date` |
| Owner | `hubspot_owner_id` |
| Associated contacts | via associations |
| Associated company | via associations |

### 1a-bis. AE Exclusion Filter
Tim focuses on NET-NEW pipeline. **Exclude all deals owned by Account Executives:**

- `hubspot_owner_id` NOT IN ('82625923', '423155215') — Exclude AE-owned deals (Lex Evans, Phil Sanders, Ron, Anthony)

**Rationale:** Deals already owned by AEs are outside Tim's scope. For handoff context only, use the single-deal lookup: "deal health [deal name]"

**Validation:** After pulling deals, verify the Owner field against the AE blocklist to prevent AE deals from scoring.

### 1b. Pull Activity History
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
| Contacts engaged | Points |
|-----------------|--------|
| 3+ contacts, including EB | 15 |
| 2+ contacts | 10 |
| 1 contact (champion only) | 5 |
| 0 active contacts | 0 |

### Signal 4: Call Momentum (15 points)
| Activity signal | Points |
|-------------|--------|
| Call in last 7 days + positive sentiment | 15 |
| Call in last 7 days + neutral | 10 |
| Call in last 14 days | 7 |
| No calls in 14+ days | 0 |
| Negative sentiment on last call | -5 (penalty) |

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
