---
name: "business-pulse"
version: "1.0.0"
description: "Live firm-wide sales pulse from the Epiphan CRM — revenue vs pace, pipeline by stage, won/lost, BDR activity, with coaching takeaways. Use when: business pulse, how are we doing, pipeline health, revenue pace, weekly numbers, standup brief, are we on track, sales snapshot."
---

<objective>
Give a new SDR (or a manager in standup) a live, honest read on the business in one shot: are we on
pace, where's the pipeline, what won/lost, how's BDR activity — then three "so-what" takeaways. Pulls
REAL data from the Epiphan AI MCP every run. Tool reference: see `epiphan-ai-mcp-guide-skill`.
</objective>

<quick_start>
**Trigger:** "business pulse", "how are we doing", "weekly numbers", "standup brief".
**One call gets you 90% of it:**
```
weekly_brief({})
```
Then synthesize into the Output shape below (never dump raw JSON). For the new SDR cohort or deeper
cuts, use the `query_dataset` calls in "How to run it". Reference material: `reference/` in this skill
+ `epiphan-ai-mcp-guide-skill` (golden defaults, owner IDs, verticals pack).
</quick_start>

## How to run it

1. **One-shot brief (start here):**
   ```
   weekly_brief({})
   ```
   Returns revenue (week/MTD/QTD/YTD + prior-year), deals won/lost, new contacts by lifecycle +
   source, BDR activity, and AE pipeline by stage — already tuned to FY2026 (start 2025-11-01),
   $19.5M target, BDR IDs 87486452 (Tim) / 423155215 (Ron).

   **Track the new SDR cohort** (Edgar / Vasil / Nyasha — onboarded June 2026) explicitly:
   ```
   weekly_brief({ bdr_owner_ids: <new-SDR-cohort ids> })
   query_dataset({ dataset: "rep_activity", group_by: ["owner"],
                   filters: { owner_ids: <new-SDR-cohort ids> } })
   ```
   Pull the actual ids from `epiphan-ai-mcp-guide-skill` golden defaults (single source of truth —
   do not re-hardcode them here; they drift otherwise).

2. **Deeper cuts as needed:**
   ```
   query_dataset({ dataset: "pipeline_open", group_by: ["owner","stage"] })
   query_dataset({ dataset: "revenue", group_by: ["period_month"], date_from: "2025-11-01", date_to: "2026-11-01" })
   query_dataset({ dataset: "deals_closed", group_by: ["outcome"], date_from: <quarter start>, date_to: <quarter end> })
   ```

3. **Synthesize** into the output shape below — never just dump JSON.

4. **Deliver + emit outcome sidecar** (see "Delivery" and "Outcome sidecar" below).

## Empty-data guard (CRITICAL)
If `weekly_brief` (or a `query_dataset` call the output depends on) returns empty, errors, or times
out, **do not fabricate or estimate numbers to fill the shape**. Instead:
- Retry the call once.
- If still empty/unavailable, produce the report with the affected section replaced by
  `NO LIVE DATA — <source> unavailable this run` (e.g. `NO LIVE DATA — weekly_brief unavailable`),
  omit any coaching takeaway that would depend on the missing number, and mark the run `partial`.
- If `weekly_brief` itself fails and no fallback `query_dataset` cut can substitute, halt and mark
  the run `error` — never present a guess as the pace/revenue/pipeline figure.

## Delivery
Save the rendered report as `outputs/business_pulse_<YYYY-MM-DD>.html` (self-contained, matches the
Output shape below) — this is the concrete artifact a scheduled/standup run leaves behind. For an
interactive "business pulse" ask, also paste the same content inline in the reply.

## Output shape

```
BUSINESS PULSE — week ending <date>

PACE        YTD $<x> of $19.5M target  →  <n>% of FY pace   [On / Behind / Ahead]
REVENUE     Week $<x> · MTD $<x> · QTD $<x> · YoY <±%>
PIPELINE    $<x> open across <n> deals
            by stage: Discovery $<x> · … · Commit $<x>
WON / LOST  Won <n> ($<x>) · Lost <n> ($<x>) this period
BDR         Tim: <dials/connects/meetings> · Ron: <…>
TOP MOVERS  <2-3 notable deals advancing or slipping>

SO WHAT (coaching)
 1. <where the gap is, and the single highest-leverage action>
 2. <a stage with stalled volume → who multi-threads it>
 3. <a vertical/segment signal worth a play this week>
```

## Vertical-awareness — and its honest limit
There is **no native vertical/industry dimension** in the datasets (`group_by` =
period/owner/stage/outcome/country/pipeline/lifecycle/**source**). So any HigherEd / Community College
/ Live Events / Corporate / Broadcast split is **derived** — proxy via `source`/`pipeline`/`country`,
or enrich the top open deals account-by-account (`sales_brief`). **Always label a vertical breakdown as
approximate**; never present a fabricated clean split. (Vertical pack: `epiphan-ai-mcp-guide-skill/reference/verticals.md`.)

## Coaching lens (tie back to the data we have)
- Every 2026 loss was single-threaded below Manager level → if a big deal sits in Discovery, the play
  is "thread up to the economic buyer," not "follow up."
- 22 of 29 HigherEd deals stalled in Discovery → Discovery-stage bulk is the leading indicator to act on.

## Guardrail — internal only
Output is internal. Naming partners/competitors here is fine; anything buyer-facing must stay clean
(no AV-matrix mechanism, no third-party brand names — "your CMS / LMS"). The pooled figure is "a more
affordable path, a starting point, not a quote." See `epiphan-ai-mcp-guide-skill`.

## Outcome sidecar (every run)
Write `~/.claude/skill-analytics/last-outcome-business-pulse-skill.json` (path MUST be outside the
repo) so a broken `weekly_brief` pull is visible to the analytics sweep instead of a silent no-op.
Failure definition per `skill-audit/specs/self-healing-template.md`: **success** = pulled live and
delivered clean; **partial** = one or more sections replaced by the `NO LIVE DATA` guard above but a
report was still produced; **error** = no usable report produced at all (`weekly_brief` failed with no
fallback). `partial`/`error` must name the failing source in `error` — never leave it blank.

```json
{
  "ts": "{ISO-8601 UTC now}",
  "skill": "business-pulse-skill",
  "version": "1.0.0",
  "variant": "default",
  "status": "success | partial | error",
  "runtime_ms": 0,
  "metrics": {
    "ytd_pace_pct": 0,
    "week_revenue": 0,
    "pipeline_open": 0,
    "deals_won": 0,
    "deals_lost": 0,
    "sections_missing": []
  },
  "error": null,
  "session_id": "{session id or null}"
}
```
`version` must match the frontmatter `version:` above. `sections_missing` lists any output rows
replaced by `NO LIVE DATA` this run (empty array on a clean success).

<success_criteria>
- [ ] Pulled LIVE data via `weekly_brief` / `query_dataset` this run — no stale or fabricated numbers
- [ ] Any empty/failed source is flagged inline as `NO LIVE DATA — <source>` (never guessed) and the run marked partial/error accordingly
- [ ] Output follows the BUSINESS PULSE shape: pace vs $19.5M target, revenue (week/MTD/QTD/YoY), pipeline by stage, won/lost, BDR activity, top movers
- [ ] Exactly three "SO WHAT" coaching takeaways, each tied to a number in the brief (fewer if a dependent section is missing)
- [ ] Any vertical breakdown is labeled approximate (derived via source/pipeline/country proxy — no native vertical dimension)
- [ ] Output stays internal-only; buyer-facing guardrails respected
- [ ] Report saved to `outputs/business_pulse_<YYYY-MM-DD>.html`
- [ ] Outcome sidecar written to `~/.claude/skill-analytics/last-outcome-business-pulse-skill.json`
</success_criteria>
