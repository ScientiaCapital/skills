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
**Do this:**
1. Pull the cohort's deals: `hubspot_search_deals({ collaborator_owner_id: <SDR id>, year: 2026, limit: 50 })` for Edgar `93367782` / Vasil `93782443` / Nyasha `94135434`.
2. Scan calls: `clari_search_calls({ repEmail, daysBack: 90 })` + `clari_get_call_summary` for greenfield language.
3. Classify + score against `reference/signals.md`, map to product fit, emit the ranked GREENFIELD TRACKER table.
</quick_start>

## How to run it

1. **Pull the cohort's deals** (new SDRs — Edgar / Vasil / Nyasha):
   ```
   hubspot_search_deals({ collaborator_owner_id: "93367782", year: 2026, limit: 50 })  // Edgar
   hubspot_search_deals({ collaborator_owner_id: "93782443", year: 2026, limit: 50 })  // Vasil
   hubspot_search_deals({ collaborator_owner_id: "94135434", year: 2026, limit: 50 })  // Nyasha
   ```
2. **Scan recent calls for greenfield language:**
   ```
   clari_search_calls({ repEmail: "emarroquin@epiphan.com", daysBack: 90 })   // + vivanov@, nchigwedere@
   clari_get_call_summary({ /* callId */ })   // read the takeaways
   ```
3. **Classify + score** each opp against the greenfield signals (see `reference/signals.md`), map to
   product fit, and emit the ranked list.

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
- **Pearl Mini** — portable switcher, fast setup → fly-kit / remote.
- **EC20** — PTZ, direct-to-CMS, no operator → automation / easy mobilization.
- **Epiphan Unify** — remote multi-source / centralized production.
- **Pearl Nano** — single-source edge capture, PoE+.
⚠️ There is **no "fly-kit" doc page** in the Knowledge base — it's a positioning angle. Ground hard
specs via `search_product_knowledge`; frame the fly-kit story, don't cite a spec sheet for it.

## Vertical lens (full pack: `epiphan-ai-mcp-guide-skill/reference/verticals.md`)
Greenfield is strongest in **Broadcast** (post-NAB), **Live Events** (per-event), and new-build
**Courts/Gov't/Corporate**. Community College & Higher Ed are mostly *aging* — use the cost-of-inaction
motion there instead.

## Guardrail — internal only
Output is internal. Naming partners/competitors here is fine; buyer-facing copy stays clean (no
AV-matrix mechanism, no third-party brand names — "your CMS / LMS"; pooled = "a more affordable path,
a starting point, not a quote"). The AE owns fit, pricing, POC. See `epiphan-ai-mcp-guide-skill`.

<success_criteria>
- [ ] Data pulled LIVE (HubSpot deals via collaborator_owner_id + Clari call summaries) — no invented signals
- [ ] Every listed opp has a greenfield signal with an actual quote/evidence, classified per `reference/signals.md` (aging-vs-greenfield test applied)
- [ ] Output follows the GREENFIELD TRACKER table shape, ranked, with product fit + next action per row, plus a WATCH list
- [ ] Product fit grounded in real specs (`search_product_knowledge`) — fly-kit framed as positioning, never cited as a spec sheet
- [ ] Output stays internal; buyer-facing copy guardrails respected
</success_criteria>
