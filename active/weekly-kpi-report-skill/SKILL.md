---
name: weekly-kpi-report
description: Friday 5:30 PM CST weekly KPI report for Tim's SDR pod (Tim Kipper, Edgar Marroquin, Vasil Ivanov). Pulls each rep's real Nooks dials/connects + HubSpot meetings-booked and pipeline-created for Mon 00:00 → Fri 5:30 PM CST, calculates connect rate + attainment vs weekly targets, builds color-coded per-rep scorecards (GREEN/YELLOW/RED) with week-over-week trend arrows, rolls up a team totals row, and delivers an HTML report + a compact Slack DM to Tim. Read-only everywhere except the Slack DM and the local HTML/prev-week JSON. This task MEASURES the reps; sdr-call-coaching (Fridays 11 AM) COACHES them — do not duplicate the coaching rubric here.
version: "1.0.0"
schedule: "0 30 17 * * 5"
timezone: "America/Chicago"
---

<objective>
Run Tim's weekly SDR KPI report (Fridays 5:30 PM CST, after the 11 AM call-coaching pass). For each rep in the pod — Tim Kipper, Edgar Marroquin, Vasil Ivanov — pull hard activity numbers for the report week (Mon 00:00 → now, America/Chicago): Nooks dials + connects, HubSpot meetings booked, pipeline $ created, deals advanced. Compute connect rate and attainment vs weekly targets, badge each metric GREEN/YELLOW/RED, add a week-over-week trend arrow, and hand Tim a per-rep scorecard grid + team totals row as an HTML report plus a compact Slack DM. Read-only everywhere except the Slack DM to Tim, the local HTML file, and outputs/kpi_prev.json. This task MEASURES (quantitative scorecard); sdr-call-coaching MEASURES nothing and COACHES qualitatively — never re-run the coaching rubric here.
</objective>

<quick_start>
**Trigger:** "weekly kpi report", "kpi report", "weekly report", "sdr metrics", "team scorecard", "how did the team do this week" — or the Friday 5:30 PM CST scheduled run.

**Flow:** Stage 0 establish report week (bash `date`, never hardcode) → Stage 1 Nooks dials/connects per rep (read-only) → Stage 2 HubSpot meetings-booked + pipeline-created + deals-advanced per rep → Stage 3 rates + attainment vs weekly targets → Stage 4 per-rep scorecards with GREEN/YELLOW/RED badges + trend arrows → Stage 5 team roll-up + week-over-week delta → Stage 6 deliver (HTML to outputs/, compact Slack DM to Tim) → Stage 7 emit outcome sidecar.
</quick_start>

<success_criteria>
- Report window is computed dynamically (Mon 00:00 → now, capped at Fri 5:30 PM CST); dates never hardcoded.
- Every rep has a scorecard row: Dials | Connects | Connect% | Mtgs Booked | Pipeline $ | Deals Advanced | vs Target, each metric badged GREEN (≥100%), YELLOW (75-99%), RED (<75%) vs its weekly target.
- Each metric shows a trend arrow (▲ ▼ ▬) vs prior week from outputs/kpi_prev.json; first-ever run renders "— no prior week" instead of arrows.
- Team totals row sums dials/connects/meetings/pipeline/deals and recomputes team connect rate + overall attainment %.
- Vasil (onboarded 2026-06-11) renders "NEW · ramping" framing on a light week — never RED for low volume alone.
- Nooks + HubSpot used read-only; only writes are: slack_send_message to Tim, the local HTML file, and outputs/kpi_prev.json (overwritten with this week's numbers at the end).
- Outcome sidecar written to ~/.claude/skill-analytics/last-outcome-weekly-kpi-report.json with team totals + attainment_pct.
</success_criteria>

<core_content>

# Weekly KPI Report (v1.0.0)

Schedule: Fridays 5:30 PM CST. Automated run — Tim is NOT present. Execute autonomously, make reasonable choices, note them inline in the report. When data is partial, ship the report with what you have and flag gaps; do not abort. This task MEASURES the reps with hard numbers. The sibling sdr-call-coaching task (Fridays ~11 AM CST) COACHES qualitatively — do NOT score calls, do NOT open recordings, do NOT duplicate the coaching rubric here.

## Identifiers (verified 2026-06-17)
- **Tim Kipper** (Sr. BDR): HubSpot owner_id `87486452`; Nooks user `UdhD9yeRfOXij75iD0Oy9F1b25P2`; Slack DM `U0AAJUZH2PK`; tkipper@epiphan.com.
- **Edgar Marroquin** (SDR): HubSpot owner_id `93367782`; Nooks user `U2iWVwWG83OYhm3XR0mvGd9gWDV2`; emarroquin@epiphan.com.
- **Vasil Ivanov** (SDR): HubSpot owner_id `93782443`; Nooks user `1BUM3d2fZuhsbFttl5UOKEOPuMG3`; vivanov@epiphan.com. Onboarded 2026-06-11 — early weeks will show low volume; frame as "NEW · ramping," never RED for low counts alone.
- Nooks MCP server id `8c1d2738-2529-4248-b268-342859275d11`.
- HubSpot portal `21530819`. Deal link: https://app.hubspot.com/contacts/21530819/record/0-3/{dealId}
- If Nooks user ids drift, resolve live via `listUsers` (match by email) or `getMe`; never invent an id.

## Weekly targets (derived from CLAUDE.md comp plan — Full H2, all months Jul–Dec 2026)
Per rep, per week (Mon–Fri):
| Metric | Weekly target | GREEN | YELLOW | RED |
|---|---|---|---|---|
| Dials | 250 (50/day × 5) | ≥250 | 188-249 | <188 |
| Connect rate | 10% (band 8-12%) | ≥10% | 8-9.9% | <8% |
| Meetings booked | 6 | ≥6 | 5 | <5 |
| Pipeline $ created | $59.5K ($714K/mo ÷ 12 wk-equiv, ~$178K/wk team ÷ 3) | ≥$59.5K | $45K-59.4K | <$45K |
| Deals advanced | 4 | ≥4 | 3 | <3 |

Badge % = actual ÷ target. GREEN ≥100%, YELLOW 75-99%, RED <75%. Connect rate is banded (8-12% healthy) — treat ≥10% GREEN, 8-9.9% YELLOW, <8% RED regardless of raw dial count.

Team weekly targets (roll-up): 750 dials, 18 meetings, ~$178K pipeline, 12 deals advanced, 10% team connect rate.

## Report window
Monday 00:00 → now (capped at Friday 17:30) America/Chicago of the CURRENT week. Compute dynamically — never hardcode. Prior week = the Mon–Fri immediately before, read from outputs/kpi_prev.json.

=== GATES (run before pulling any data) ===

NOOKS = READ-ONLY. Server id `8c1d2738-2529-4248-b268-342859275d11`. Use ONLY: listCalls, getCall, listCallDispositions, listProspects, listUsers, getMe. Do NOT call any Nooks write tool (no createTask/updateTask/enroll). Every call needs USER_GOAL="Generate Tim's weekly SDR KPI report" plus a per-call REASON.

HUBSPOT = READ-ONLY for metrics. Use hubspot_search_deals / search_crm_objects / hubspot_search_contacts. Do NOT create, update, or move any contact, deal, or list. This is a measurement pass only.

SCOPE/PRIVACY GATE: Output goes to Tim only (Slack DM `U0AAJUZH2PK` + local HTML). Do not DM the SDRs, Victor, or anyone else. Do not post to HubSpot or to any prospect.

Default to the `Epiphan Ai` MCP namespace for HubSpot tools; fall back to `HubSpot` namespace only for tools not present there.

=== STAGE 0: ESTABLISH REPORT WEEK ===

Via bash `date` (TZ=America/Chicago):
- `week_start` = Monday 00:00:00 of the current week (ISO-8601).
- `week_end` = min(now, Friday 17:30:00).
- Convert both to the epoch-ms / ISO forms each API wants (Nooks filter_time_gte/lte; HubSpot hs_timestamp / createdate filters).
- Read outputs/kpi_prev.json if present → prior-week per-rep + team numbers for trend arrows. If absent, set a `first_run` flag (renders "— no prior week").
- Print the resolved window at the top of the report: "Week of {Mon date} → {Fri date}, through {week_end time} CST".

=== STAGE 1: NOOKS CALL METRICS (per rep) ===

Run the SAME logic for Tim, then Edgar, then Vasil.

- `listCalls`: filter_owner_id={rep Nooks user id}, filter_time_gte=week_start, filter_time_lte=week_end, include=["callDisposition"], page_size=50; page via links.next until exhausted (sum across pages — do NOT stop at page 1).
- **Dials** = total calls returned in window (all dispositions).
- **Connects** = calls where EITHER duration >= 30 seconds OR callDisposition.callOutcome IN ("Connect","Meeting"). A 30s+ pickup or a Connect/Meeting disposition both count as a live conversation. De-dupe: a call counted by disposition is not double-counted by duration.
  - Known disposition ids: Connected `14a81f79-6d14-4b37-9277-e2ae88618aca`; Follow Up `6155389e-9bc2-4c99-8218-dc95561de424`; Meeting Booked `c1210028-7405-4f1e-81f0-90bbf1921c53`. Resolve live names via listCallDispositions if unsure; never invent.
- **Connect rate %** = Connects ÷ Dials × 100 (0 if Dials = 0).
- Capture per rep: dials, connects, connect_rate.

If listCalls returns nothing for a rep, record zeros and flag "no Nooks activity captured" — for Vasil this may be a genuine ramping week (frame accordingly), for Tim/Edgar flag it as a data-pull concern in the report.

=== STAGE 2: HUBSPOT PIPELINE METRICS (per rep) ===

Run per rep by hubspot_owner_id.

**Meetings booked** — count of NEW meetings/opportunities the rep created this week. Prefer, in order:
1. `hubspot_search_deals` filtered by owner + createdate in [week_start, week_end] where the deal represents a booked meeting/opportunity → count.
2. If a distinct "meeting booked" signal exists (contact lifecyclestage → opportunity this week, or a meetings-engagement object), use `search_crm_objects` on contacts: hubspot_owner_id={rep} AND hs_lastmodifieddate in window AND lifecyclestage = "opportunity". Count contacts that flipped to opportunity this week.
Report which source was used. Do not double-count a deal and its contact.

**Pipeline $ created** — sum of `amount` on deals where hubspot_owner_id={rep} AND createdate in [week_start, week_end]. Use hubspot_search_deals; sum the amount field (treat null amount as $0 and note the count of amount-less deals).

**Deals advanced** — deals where hubspot_owner_id={rep} AND hs_lastmodifieddate in window AND dealstage changed forward this week (not created this week — those already count under pipeline created). If a reliable "stage changed" filter isn't available, approximate as deals modified this week that were created BEFORE this week and are not closed-lost, and label it "(approx — modified this week)".

Capture per rep: meetings_booked, pipeline_created, deals_advanced (+ the source note for each).

=== STAGE 3: RATES + ATTAINMENT vs TARGETS ===

For each rep, for each metric, compute attainment % = actual ÷ weekly target × 100 and assign a badge:
- GREEN = ≥100%
- YELLOW = 75-99%
- RED = <75%
Connect rate uses the banded rule (≥10% GREEN, 8-9.9% YELLOW, <8% RED).

Rep composite attainment = simple average of the five metric attainment %s (cap each metric at 150% so one blowout metric doesn't mask three RED ones). This composite drives the rep's overall row badge.

Vasil override: if he is inside his first ~4 weeks (onboarded 2026-06-11) OR his dials are <100, do NOT badge his row RED for low volume — badge "NEW · ramping" and show raw numbers + trend only.

=== STAGE 4: PER-REP SCORECARDS ===

Build one row per rep in a fixed-width / HTML grid:

```
Rep              Dials   Connects  Conn%   Mtgs   Pipeline $   Deals Adv   vs Target
Tim Kipper       262 ▲   28 ▲      10.7%   7 ▲    $64.2K ▲     5 ▬         GREEN 108%
Edgar Marroquin  198 ▼   17 ▬      8.6%    4 ▼    $38.1K ▼     3 ▬         YELLOW 79%
Vasil Ivanov     84  ▲   6  ▲      7.1%    1 —    $9.0K —      0 —         NEW · ramping
```

- Each cell shows the value + a trend arrow vs prior week: ▲ up, ▼ down, ▬ flat (±5%), — no prior data.
- Color the vs-Target cell (and, in HTML, each metric cell) GREEN/YELLOW/RED per Stage 3.
- Under each rep row, one plain-English line: the single biggest miss and the single biggest win (e.g. "Edgar: dials down 24% WoW — connect rate held. Pipeline the gap this week.").

=== STAGE 5: TEAM ROLL-UP + TREND ===

- Team totals row: sum dials, connects, meetings, pipeline $, deals advanced across all reps; recompute team connect rate (team connects ÷ team dials) and team composite attainment vs the team weekly targets.
- Week-over-week: compare team totals to outputs/kpi_prev.json → one headline line, e.g. "Team pipeline +18% WoW ($111K → $131K); dials flat; meetings −2."
- Progress-to-month context: sum this week's pipeline $ + meetings against the current month's Full-H2 target ($714K pipeline, 24 deals) and show a "month-to-date pace" note (informational — do not badge).

=== STAGE 6: OUTPUT ===

**A) HTML report** → outputs/kpi_report_{week_start_date}.html
- Header: "Weekly KPI Report — Week of {Mon}–{Fri}, through {time} CST".
- Per-rep scorecard grid (Stage 4) with colored cells (inline styles: GREEN #1a7f37, YELLOW #9a6700, RED #cf222e).
- Team totals row (bold, bordered top).
- WoW headline + month-to-date pace note.
- Footer: data sources + timestamp + any gap flags. Self-contained, no external assets.

**B) Slack DM to Tim** (`U0AAJUZH2PK`) via slack_send_message — COMPACT summary only:
- One header line with the week + team attainment badge.
- One line per rep: `Tim 262d/28c/10.7% · 7 mtg · $64K · GREEN 108% ▲`.
- Team line + the WoW headline.
- Link/pointer to the HTML file path. Keep it under ~12 lines — Tim reads this on mobile.

**C) Persist prior week** → overwrite outputs/kpi_prev.json with THIS week's per-rep + team numbers (so next Friday has a baseline). Include week_start so a stale file is detectable.

If Slack send fails, still write the HTML + kpi_prev.json and note the Slack failure in the outcome sidecar error field.

=== STAGE 7: OUTCOME SIDECAR ===

Write to `~/.claude/skill-analytics/last-outcome-weekly-kpi-report.json` (path MUST be outside the repo). The PostToolUse sweep hook ingests it into outcomes.jsonl.

```json
{
  "ts": "{ISO-8601 UTC now}",
  "skill": "weekly-kpi-report",
  "version": "1.0.0",
  "variant": "default",
  "status": "success | partial | error",
  "runtime_ms": 0,
  "metrics": {
    "reps_reported": 3,
    "team_dials": 0,
    "team_connects": 0,
    "team_connect_rate": 0,
    "team_meetings_booked": 0,
    "team_pipeline_created": 0,
    "attainment_pct": 0
  },
  "error": null,
  "session_id": "{session id or null}"
}
```

- status = "success" if all three reps pulled from both Nooks + HubSpot; "partial" if any source was missing/degraded (also fill `error` with a short note); "error" only if the report could not be produced at all.
- team_connect_rate as a decimal (e.g. 0.096); team_pipeline_created in whole dollars; attainment_pct = team composite attainment vs weekly targets.

</core_content>
