---
name: "call-recording-analyzer"
description: "Gong/Chorus-style call transcript analysis using Clari data. Scores calls against MEDDIC framework, flags missed discovery questions, surfaces competitor mentions, extracts action items, and identifies coaching moments. Feeds deal-momentum-analyzer and morning-brief with call quality signals. Use when: 'analyze call', 'call review', 'score my call', 'what did I miss', 'call coaching', 'review transcript', 'Clari analysis', 'call scorecard', 'how did my call go', 'review my last call with [company]'."
---

<objective>
Replace manual call review with automated Clari transcript analysis. Every call Tim makes gets scored against MEDDIC dimensions, flagged for missed discovery questions, and fed into downstream skills (deal-momentum-analyzer, morning-brief). Targets: identify 3+ coaching moments per call, surface competitor intel automatically, and reduce post-call admin from 10 minutes to under 60 seconds.
</objective>

<quick_start>
**After a call:**
"analyze my last call with Baylor" → pulls Clari transcript → scores against MEDDIC → outputs scorecard

**Batch review:**
"review today's calls" → analyzes all calls from today → summary report

**Coaching mode:**
"call coaching for my University of Michigan demo" → deep analysis with talk ratio, question quality, objection handling

**Trigger phrases:**
- "analyze call [company]"
- "call review [company]"
- "score my call"
- "what did I miss on [company] call"
- "call coaching [company]"
- "review my last call"
- "review today's calls"
- "how did my call go"
- "Clari scorecard"
</quick_start>

<success_criteria>
- MEDDIC scorecard generated for every analyzed call
- Missed discovery questions identified (what SHOULD have been asked)
- Competitor mentions extracted and mapped to battlecard responses
- Talk-to-listen ratio calculated (target: prospect talks 60%+)
- Action items extracted with owner assignment
- Coaching moments flagged (interruptions, missed objection follow-ups, premature pitching)
- Results feed into deal-momentum-analyzer Signal 4 (call momentum scoring)
- Analysis completes in under 60 seconds per call
</success_criteria>

<workflow>

## Architecture

```
TRIGGER                    DATA PULL                 ANALYSIS                OUTPUT
──────────────────────────────────────────────────────────────────────────────────
"analyze call X"  →  Clari: transcript +     →  MEDDIC scoring      →  Call Scorecard
                     summary + action items   →  Discovery gaps       →  Coaching Report
                  →  HubSpot: deal context    →  Competitor extract   →  Action Items
                  →  Prior call history       →  Talk ratio analysis  →  Deal Update
                                              →  Objection mapping    →  Morning Brief Feed
```

## Stage 1: Data Collection

Run these MCP calls in parallel:

### 1a. Clari Call Data
| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find the call by company name, attendee email, or date range |
| `clari_get_call` | Full call metadata: duration, participants, recording URL |
| `clari_get_call_summary` | AI summary, key moments, action items, sentiment |

**Search strategy:**
1. If company name provided: `clari_search_calls(query=company_name, daysBack=7)`
2. If "last call" or "today's calls": `clari_search_calls(daysBack=1)`
3. If attendee specified: `clari_search_calls(attendeeEmail=email, daysBack=14)`

### 1b. HubSpot Deal Context
| Tool | Purpose |
|------|---------|
| `hubspot_search_companies` | Company record for the prospect |
| `hubspot_search_deals` | Active deals associated with this company |
| `hubspot_search_contacts` | Contact records for call participants |

**Pre-Flight Golden Rules Check:**
- If contact.lifecyclestage = 'customer' → Skip. Route to CSM.
- If hubspot_owner_id IN ('82625923', '423155215', '190030668') AND Tim is NOT collaborator → Skip.

### 1c. Prior Call History
| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find previous calls with same contacts (last 90 days) |
| `clari_get_call_summary` | Summaries of prior calls for progression context |

## Stage 2: MEDDIC Call Scoring

Score the call transcript against each MEDDIC dimension (0-100 total).

#### M — Metrics (0-20 points)
| Evidence | Points |
|----------|--------|
| Prospect stated specific success metrics | 20 |
| Prospect described general goals | 12 |
| Tim asked but prospect deflected | 8 |
| Not discussed | 0 |

**Missed question:** "How will you measure success? What does ideal look like in numbers?"

#### E — Economic Buyer (0-20 points)
| Evidence | Points |
|----------|--------|
| EB identified by name and confirmed as budget holder | 20 |
| EB referenced indirectly | 12 |
| Tim asked, answer unclear | 8 |
| No discussion of budget authority | 0 |

**ATL/BTL Validation (MANDATORY — per CLAUDE.md § ATL/BTL Classification v1.0):**
Classify ALL call attendees. If NO ATL attendee → Flag ⚠️ COACHING MOMENT: "Get the economic buyer on the next call."

#### D — Decision Criteria (0-15 points)
| Evidence | Points |
|----------|--------|
| Prospect listed specific evaluation criteria | 15 |
| Some factors mentioned | 10 |
| Tim asked, prospect uncertain | 5 |
| Not discussed | 0 |

#### D — Decision Process (0-15 points)
| Evidence | Points |
|----------|--------|
| Clear timeline + stakeholders + process | 15 |
| Partial timeline | 10 |
| Tim asked, vague | 5 |
| Not discussed | 0 |

#### I — Identify Pain (0-20 points)
| Evidence | Points |
|----------|--------|
| Specific quantified pain | 20 |
| Qualitative pain | 12 |
| Pain implied | 6 |
| No pain discussion (pitch without discovery) | 0 |

#### C — Champion (0-10 points)
| Evidence | Points |
|----------|--------|
| Contact volunteered to champion internally | 10 |
| High engagement (detailed questions, requested next steps) | 7 |
| Passive engagement | 3 |
| No champion signal | 0 |

### MEDDIC Classification
| Score | Rating | Meaning |
|-------|--------|---------|
| 80-100 | STRONG | Well-qualified deal |
| 60-79 | ADEQUATE | 1-2 gaps to fill next call |
| 40-59 | WEAK | Incomplete discovery |
| 0-39 | MISSED | Call was a pitch, not discovery |

## Stage 3: Coaching Analysis

### Talk-to-Listen Ratio
- **Target:** Prospect talks 60%+, Tim talks 40% or less
- **Red flag:** Tim talked 60%+ = premature pitching

### Question Quality
| Type | Quality |
|------|---------|
| Open-ended discovery | HIGH |
| Calibrated (NSTTD style) | HIGH |
| Closed confirmation | MEDIUM |
| Leading/assumptive | LOW |
| Product feature dump | COACHING MOMENT |

### Competitive Intelligence Extraction
Scan for: Extron, Blackmagic, Crestron, vMix, Matrox, Teradek, Kaltura, Panopto, YuJa, Echo360

## Stage 4: Output Format

```
╔══════════════════════════════════════════════════════════════╗
║  CALL SCORECARD: [Company Name]                              ║
║  [Date] [Duration] | [Call Type: Discovery/Demo/Follow-up]   ║
╠══════════════════════════════════════════════════════════════╣

MEDDIC SCORE: [XX/100] — [STRONG/ADEQUATE/WEAK/MISSED]

DISCOVERY GAPS — ASK THESE NEXT TIME:
1. [Specific question for biggest MEDDIC gap]
2. [Specific question for second gap]

COACHING MOMENTS:
⚠️ [Context] — [What happened] → [What to do differently]

COMPETITIVE INTEL: [Competitor mentioned + battlecard response]

TALK RATIO: Tim [X%] / Prospect [X%]

ACTION ITEMS:
☐ [Action] — Owner: [Tim/Prospect] — Due: [date]

╚══════════════════════════════════════════════════════════════╝
```

</workflow>

<downstream_integration>
## Feed to Sibling Skills

### deal-momentum-analyzer (Signal 4: Call Momentum)
Push: call_recency, call_sentiment, meddic_score, unresolved_actions, competitor_detected

### morning-brief
Include: yesterday's call scores, unresolved action items, deals with MEDDIC gaps needing follow-up

### meddic-call-prep-auto
Feed prior call gaps into next call prep
</downstream_integration>

<dependencies>
## Required MCP Tools
- **Epiphan Clari MCP:** clari_search_calls, clari_get_call, clari_get_call_summary
- **Epiphan CRM MCP:** hubspot_search_companies, hubspot_search_contacts, hubspot_search_deals, ask_agent
- **Gmail MCP:** gmail_create_draft

## Sibling Skills Referenced
- `deal-momentum-analyzer` — Consumes call quality signals for Signal 4 scoring
- `meddic-call-prep-auto` — Receives call gaps to inform next call prep
- `morning-brief` — Displays yesterday's call summaries
</dependencies>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-call-recording-analyzer.json`:
```json
{"ts":"[UTC ISO8601]","skill":"call-recording-analyzer","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"calls_analyzed":[n],"avg_meddic_score":[n],"coaching_moments_found":[n],"competitors_detected":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
