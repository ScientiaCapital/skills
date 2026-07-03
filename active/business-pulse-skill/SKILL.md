---
name: "business-pulse"
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
   weekly_brief({ bdr_owner_ids: ["93367782","93782443","94135434"] })
   query_dataset({ dataset: "rep_activity", group_by: ["owner"],
                   filters: { owner_ids: ["93367782","93782443","94135434"] } })
   ```
   (IDs + Nooks mapping live in `epiphan-ai-mcp-guide-skill` golden defaults.)

2. **Deeper cuts as needed:**
   ```
   query_dataset({ dataset: "pipeline_open", group_by: ["owner","stage"] })
   query_dataset({ dataset: "revenue", group_by: ["period_month"], date_from: "2025-11-01", date_to: "2026-11-01" })
   query_dataset({ dataset: "deals_closed", group_by: ["outcome"], date_from: <quarter start>, date_to: <quarter end> })
   ```

3. **Synthesize** into the output shape below — never just dump JSON.

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

<success_criteria>
- [ ] Pulled LIVE data via `weekly_brief` / `query_dataset` this run — no stale or fabricated numbers
- [ ] Output follows the BUSINESS PULSE shape: pace vs $19.5M target, revenue (week/MTD/QTD/YoY), pipeline by stage, won/lost, BDR activity, top movers
- [ ] Exactly three "SO WHAT" coaching takeaways, each tied to a number in the brief
- [ ] Any vertical breakdown is labeled approximate (derived via source/pipeline/country proxy — no native vertical dimension)
- [ ] Output stays internal-only; buyer-facing guardrails respected
</success_criteria>
