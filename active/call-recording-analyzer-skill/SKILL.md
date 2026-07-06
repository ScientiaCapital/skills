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
- Competitor mentions extracted and mapped to battlecard responses only after live verification via `search_product_knowledge`/`search_product_catalog` — never mapped from memory
- Talk-to-listen ratio calculated (target: prospect talks 60%+)
- Action items extracted with owner assignment
- Coaching moments flagged (interruptions, missed objection follow-ups, premature pitching)
- Scorecard persisted as an HTML report and staged as a Gmail draft — never left as chat-only text
- Call quality signals written to the shared call-signals feed and consumed by deal-momentum-analyzer Signal 4, morning-brief, and meddic-call-prep-auto
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
| `clari_get_call` (with `includeTranscript: true`) | Full call metadata + transcript: duration, participants, recording URL, summary, key moments, action items, sentiment |

Standardized on the same Clari access pattern as sibling `sdr-call-coaching` (verified 2026-06-17): `clari_search_calls` + `clari_get_call(includeTranscript=true)`. Do not call `clari_get_call_summary` — it is not a confirmed tool in the live Clari MCP surface.

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

**Pre-Flight Golden Rules Check (via `qualify_lead`):**
Run `qualify_lead` (dry run) on the call's primary contact before scoring — don't hand-roll the customer/channel/AE-owned checks against raw HubSpot reads.
- `qualify_lead` category = customer or channel partner → Skip. Route to CSM.
- AE-owned (per CLAUDE.md Golden Rules canonical owner list, not re-listed here) AND Tim is NOT collaborator AND outside the 90-day stale exception → Skip.
- If `qualify_lead` is unavailable, fall back to a raw `hubspot_search_contacts`/`hubspot_search_deals` read of lifecyclestage + `hubspot_owner_id` against the CLAUDE.md Golden Rules list, and note the degraded path in the outcome sidecar.

### 1c. Prior Call History
| Tool | Purpose |
|------|---------|
| `clari_search_calls` | Find previous calls with same contacts (last 90 days) |
| `clari_get_call` (with `includeTranscript: true`) | Summaries of prior calls for progression context |

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

**TECHNICAL-ACCURACY GATE (non-negotiable — run before mapping any competitor mention to a battlecard response):** a competitor mention is only "correct" or "wrong" relative to live, current facts, and battlecards go stale. For every competitor mention:
1. Verify the underlying claim (spec, EOL/discontinued status, integration support) via `search_product_knowledge` or `search_product_catalog` (Epiphan AI) before selecting a battlecard response — never map from memory.
2. Only present the battlecard rebuttal as fact once it's confirmed live.
3. If verification is unavailable or inconclusive, mark it "unverified — flag for Tim to confirm" in the scorecard instead of presenting a rebuttal as settled fact.

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

## Stage 5: Deliver + Feed Downstream

Don't leave the scorecard as ephemeral chat text — persist it and push the signals to the skills that consume them.

1. **Save the report.** Render the Stage 4 scorecard(s) as a self-contained HTML report and save to `${CLAUDE_OUTPUTS_DIR:-./outputs/}call_scorecard_<company-slug>_<YYYY-MM-DD>.html` (batch runs: one file, one card per call). Present via `mcp__cowork__present_files` if available.
2. **Stage a Gmail draft.** Call `mcp__Gmail__create_draft` (sender `tkipper@epiphan.com` per CLAUDE.md — never any other sender) addressed to `tkipper@epiphan.com`, subject `Call Scorecard — [Company] — [Date]` (batch: `Call Scorecards — [Date]`), body = the HTML report. Draft only, never auto-sent — Tim reviews before anything goes further.
3. **Write the downstream feed.** Append one JSON line per analyzed call to `~/.claude/skill-analytics/call-signals/<company-slug>.jsonl`:
   `{"ts":"[UTC ISO8601]","company":"[name]","dealId":"[if known]","call_recency_days":[n],"call_sentiment":"[pos/neu/neg]","meddic_score":[0-100],"unresolved_actions":[n],"competitor_detected":["[names]"],"atl_attendee":[bool]}`
   This is the concrete handoff `deal-momentum-analyzer` (Signal 4) and `morning-brief` read instead of re-deriving the same signals. If the feed directory is unwritable, note it in the outcome sidecar as `partial` and still deliver the scorecard (steps 1-2) — a failed handoff never blocks showing Tim the result.
4. **meddic-call-prep-auto** reads the same feed's `meddic_score` gaps to seed next-call prep questions (see `<downstream_integration>`).

</workflow>

<downstream_integration>
## Feed to Sibling Skills

### deal-momentum-analyzer (Signal 4: Call Momentum)
Reads `~/.claude/skill-analytics/call-signals/<company-slug>.jsonl` for: call_recency, call_sentiment, meddic_score, unresolved_actions, competitor_detected

### morning-brief
Reads the same feed for: yesterday's call scores, unresolved action items, deals with MEDDIC gaps needing follow-up

### meddic-call-prep-auto
Reads the same feed's prior call gaps to inform next call prep
</downstream_integration>

<dependencies>
## Required MCP Tools
- **Epiphan Clari MCP:** clari_search_calls, clari_get_call (with includeTranscript=true)
- **Epiphan AI MCP:** qualify_lead (pre-flight Golden Rules gate, Stage 1b), search_product_knowledge, search_product_catalog (technical-accuracy gate, Stage 3 — required before mapping any competitor mention to a battlecard response)
- **Epiphan CRM MCP:** hubspot_search_companies, hubspot_search_contacts, hubspot_search_deals, ask_agent (fallback only, if qualify_lead is unavailable)
- **Gmail MCP:** mcp__Gmail__create_draft — stages the scorecard to tkipper@epiphan.com; never sent directly

## Sibling Skills Referenced
- `deal-momentum-analyzer` — Consumes call quality signals for Signal 4 scoring, via the call-signals feed
- `meddic-call-prep-auto` — Receives call gaps to inform next call prep, via the call-signals feed
- `morning-brief` — Displays yesterday's call summaries, via the call-signals feed
- `sdr-call-coaching` — sibling Clari access pattern this skill now matches (clari_search_calls + clari_get_call(includeTranscript=true))
</dependencies>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-call-recording-analyzer.json`:
```json
{"ts":"[UTC ISO8601]","skill":"call-recording-analyzer","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"calls_analyzed":[n],"avg_meddic_score":[n],"coaching_moments_found":[n],"competitors_detected":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (including a degraded qualify_lead fallback or a failed call-signals feed write). Use "error" only if no output was generated.

Also append one line to `~/.claude/skill-runs/call-recording-analyzer.jsonl` (`{ts, status, calls_analyzed, feed_write_ok, draft_created, error}`) so a failed Clari pull, gate fallback, or feed write is visible in the run log, not just the analytics sidecar.
