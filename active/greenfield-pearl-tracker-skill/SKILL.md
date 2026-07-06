---
name: "greenfield-pearl-tracker"
description: "Find and track greenfield Pearl/EC20 opportunities from live CRM + Clari signals — new-build, remote production, and post-NAB broadcast fly-kit / automation. Use when: greenfield opportunities, new build, fly kit, remote production, broadcast deals, mobilization, find new logos, NAB signals, who's building."
---

<objective>
Surface and rank GREENFIELD opportunities — buyers with no aging install base to feel pain about, who
buy per-project or net-new: new buildings, remote/onsite production, and the post-NAB **broadcast**
push toward workflow automation, easier-to-use gear, and easy **mobilization** (fly-kits). Pulls live
from the Epiphan AI MCP. Tool reference: `epiphan-ai-mcp-guide-skill`. Signal heuristics + product-fit
map: `reference/signals.md`.
</objective>

<quick_start>
**Trigger:** "greenfield opportunities", "fly kit", "who's building", "NAB signals", "find new logos".
**Cohort roster (single source — reference this table, don't re-type IDs elsewhere in this file):**
| Rep | owner_id | repEmail |
|---|---|---|
| Edgar | `93367782` | emarroquin@epiphan.com |
| Vasil | `93782443` | vivanov@epiphan.com |
| Nyasha | `94135434` | nchigwedere@epiphan.com |
Roster drifts (holds, ramp status) faster than this file — confirm the current cohort before running.
**Do this:**
1. Pull each rep's deals: `hubspot_search_deals({ collaborator_owner_id: <owner_id from roster above>, year: 2026, limit: 50 })`.
2. Scan calls: `clari_search_calls({ repEmail: <repEmail from roster above>, daysBack: 90 })` + `clari_get_call_summary` for greenfield language.
3. Classify + score against `reference/signals.md`, map to product fit (positioning only, grounded via `search_product_knowledge` — see Product-fit map below), emit the ranked GREENFIELD TRACKER table.
</quick_start>

## How to run it

1. **Pull each rep's deals**, one call per rep in the cohort roster (Quick Start above):
   ```
   hubspot_search_deals({ collaborator_owner_id: <owner_id>, year: 2026, limit: 50 })
   ```
   If a rep returns zero deals, skip them and note it — don't invent one.
2. **Scan recent calls for greenfield language**, one rep at a time (roster `repEmail`):
   ```
   clari_search_calls({ repEmail: <repEmail>, daysBack: 90 })
   clari_get_call_summary({ /* callId */ })   // read the takeaways
   ```
   If a rep has no calls in the 90-day window, skip that rep — don't fabricate a signal — note it
   (e.g. under WATCH or a "no activity" line), and mark the run `partial` (see Self-Healing below).
3. **Classify + score** each opp against the greenfield signals (see `reference/signals.md`), map to
   product fit (positioning label only, grounded via `search_product_knowledge` — see Product-fit map
   below), and emit the ranked list.

## Greenfield signal (what you're hunting for)
New building / renovation · "standing up a new studio/courtroom/HQ" · truck / fly-pack / flyaway ·
remote or onsite production · "automate the workflow" · "easier to use" / "fewer operators" ·
mobilization / fast setup/teardown · **NAB** follow-ups · per-event / per-project (no install base).
Full keyword list + the aging-vs-greenfield test: `reference/signals.md`.

## Output shape
```
GREENFIELD TRACKER — <cohort / date>

# | Account | Vertical | Signal (quote) | Stage | Product fit | Next action
--+---------+----------+----------------+-------+-------------+------------
1 | …       | Broadcast| "flyaway kit…" | Disc. | Pearl Mini  | thread up to Chief Engineer
…

WATCH: <accounts with a weak/early signal worth a touch>
```

## Product-fit map (broadcast & remote lead the greenfield story)
Positioning labels only — not spec sheets. `search_product_knowledge` (or `search_product_catalog`) is
a **required call before any spec/capability claim appears in output** (the "Product fit" column or
elsewhere). If the tool can't confirm a claim, drop the spec detail and output the positioning label
alone plus "AE to confirm fit" — never cite a spec from memory.
- **Pearl Mini** — fly-kit / remote angle (fast-mobilization story).
- **EC20** — automation / easy-mobilization angle (fewer-operators story).
- **Epiphan Unify** — remote multi-source production angle.
- **Pearl Nano** — single-source edge-capture angle.
⚠️ There is **no "fly-kit" doc page** in the Knowledge base — it's a positioning angle, not a spec.
Ground any hard spec via `search_product_knowledge`; frame the fly-kit story, don't cite a spec sheet.

## Vertical lens (full pack: `epiphan-ai-mcp-guide-skill/reference/verticals.md`)
Greenfield is strongest in **Broadcast** (post-NAB), **Live Events** (per-event), and new-build
**Courts/Gov't/Corporate**. Community College & Higher Ed are mostly *aging* — use the cost-of-inaction
motion there instead.

## Guardrail — internal only
Output is internal. Naming partners/competitors here is fine; buyer-facing copy stays clean (no
AV-matrix mechanism, no third-party brand names — "your CMS / LMS"; pooled = "a more affordable path,
a starting point, not a quote"). The AE owns fit, pricing, POC. See `epiphan-ai-mcp-guide-skill`.
If any row's "Next action" text gets reused buyer-facing, it must pass `check_my_copy` first — this
skill's guardrail covers internal tone only, not buyer-facing brand voice.

Surfaced accounts are existing SDR-owned deals already in HubSpot, not net-new outreach — they inherit
their deal's existing Golden Rules qualification. No separate `qualify_lead` gate is needed for this
internal tracker.

<success_criteria>
- [ ] Data pulled LIVE (HubSpot deals via collaborator_owner_id + Clari call summaries) — no invented signals
- [ ] Every listed opp has a greenfield signal with an actual quote/evidence, classified per `reference/signals.md` (aging-vs-greenfield test applied)
- [ ] Output follows the GREENFIELD TRACKER table shape, ranked, with product fit + next action per row, plus a WATCH list
- [ ] Product fit shown as a positioning label only until `search_product_knowledge` (or `search_product_catalog`) confirms it live — no spec cited from memory; fly-kit framed as positioning, never cited as a spec sheet
- [ ] Output stays internal; buyer-facing copy guardrails respected
- [ ] Outcome sidecar written and a line appended to the run log (see Self-Healing below)
</success_criteria>

## Self-Healing
Follows `skill-audit/specs/self-healing-template.md`. For each external call (HubSpot, Clari,
`search_product_knowledge`): retry once on a transient error. Degrade — if a rep has no deals or no
calls in the 90-day window, skip that rep, note it in the output (don't invent a signal), and mark the
run `partial`; if `search_product_knowledge`/`search_product_catalog` can't confirm a product-fit
claim, drop the spec detail and keep only the positioning label, marked `partial`. Alert (flag it in
the output) if every rep in the cohort comes back empty. Halt (no table) only if HubSpot is unreachable
for the whole cohort. In addition to the outcome sidecar below, append one line per run to
`~/.claude/skill-runs/greenfield-pearl-tracker-skill.jsonl` per the template's run-log convention.

## Emit Outcome Sidecar
As the final step, write to `~/.claude/skill-analytics/last-outcome-greenfield-pearl-tracker-skill.json`:
```json
{"ts":"[UTC ISO8601]","skill":"greenfield-pearl-tracker","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"reps_scanned":[n],"deals_pulled":[n],"opps_surfaced":[n],"specs_confirmed_live":[n],
            "reps_skipped_no_activity":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use "partial" if any rep was skipped for no deals/no calls in window, or a product-fit spec fell back
to positioning-only because `search_product_knowledge` couldn't confirm it — name the degraded stage
in `error`. Use "error" only if no deals could be pulled for any rep in the cohort. The `version` above
must match this skill's `config.json` version — don't hardcode it a second time.
