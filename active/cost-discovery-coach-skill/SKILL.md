---
name: "cost-discovery-coach"
description: "Turns the cost-of-inaction calculator's inputs into tight, killer discovery questions per vertical — JTBD job, Never-Split calibrated question, Challenger insight. Use when: discovery questions, how to ask, calculator discovery, cost of inaction questions, SDR call prep, what do I ask, qualify the room count, broadcast/live-events/corporate discovery."
---

<objective>
Teach a new SDR (Edgar, Vasil, Nyasha) to run discovery that fills the cost-of-inaction calculator —
using questions that are short, sayable, and **spec-true**. Each calculator input becomes one killer
question. The rep masters tonality, pace, and inflection; the words are already right. Pairs with
`jobs-to-be-done-skill`, `never-split-the-difference-skill`, `challenger-sale-skill`. Full question
bank: `reference/discovery-by-input.md`.
</objective>

<quick_start>
**Trigger:** "discovery questions", "what do I ask", "cost of inaction questions", "SDR call prep".
**Do this:**
1. Identify the vertical + the calculator inputs still missing (rooms, equipment age, failed captures, downtime, tickets, staff).
2. Pull the matching questions from `reference/discovery-by-input.md` — for each input, pick one of the four layers (Killer Q / Label / Job / Insight) that fits the moment.
3. Coach delivery with the Riff rules: one question per breath, mirror, go quiet after the number.
Every spec cited must be verified **live** via `search_product_knowledge` / `search_product_catalog`
(Epiphan AI MCP) before it goes in a question — never improvise a spec, and never cite the
illustrative table below as current without re-checking it first.
</quick_start>

## The principle (read this first)
- **Concise & killer.** One breath. If it needs a comma to survive, cut it.
- **Easy to riff.** A frame they can say five ways, not a line they recite.
- **Spec-true.** Every fact in a question is verified **live** via `search_product_knowledge` /
  `search_product_catalog` before it's used — never sourced from memory or from the illustrative
  table below, which rots the moment the catalog changes.
- **Master the voice, not the script.** The skill's job is to make the words bulletproof so the rep's
  only job is delivery.

## Illustrative spec reference — fallback only, never cite without a live check
This is the shape of the answer as of this doc's last edit, kept only so a rep isn't starting cold
if the live lookup is temporarily unavailable. It is **not** the source of truth — `search_product_knowledge`
/ `search_product_catalog` always wins if the two disagree.

| Product | Illustrative spec (verify live before citing) |
|---|---|
| Pearl-2 | 6 isolated full-HD channels |
| Pearl Nexus | 2 recommended (3 max) |
| EC20 | publishes straight to your CMS, no encoder in the path |
| Edge | fleet management is free |

## The method: each input is a question
The calculator can't compute until the rep earns these answers. For every input, the bank gives four
layers — pick the one that fits the moment:

| Layer | Source | What it does |
|---|---|---|
| **Killer Q** | Never Split the Difference | a calibrated, no-oriented question — short, opens the room |
| **Label** | Never Split the Difference | "It sounds like… / It seems like…" — names the pain, gets a "that's right" |
| **Job** | Jobs To Be Done | the outcome the buyer is really hiring for |
| **Insight** | Challenger | the reframe that teaches them something about their own cost |

## Output contract
Each coaching pass delivers one **question card per missing calculator input**:
`{input, layer: Killer Q|Label|Job|Insight, line, why_it_fits}` — the exact sayable line plus a
one-clause reason that layer fits the moment. Deliver as a short list in chat (not a document).
Terminal action: once a Manager+ economic buyer is in play, call `ae_handoff` (Epiphan AI MCP,
account + champion + signal) — see `<dependencies>` below.

## The flow (one call)
1. **Open** with a label, not a pitch ("Sounds like the older rooms are the ones eating your week.").
2. **Earn the inputs** with killer questions — rooms, equipment age, failed captures, downtime,
   tickets, staff (and per vertical: events/yr, headcount, time-to-first-frame).
3. **Teach** with the cost-of-inaction number the calculator returns (Challenger reframe).
4. **Tease the cheaper path** — "there may be a more affordable path; not every room records at once"
   — *a starting point, not a quote*. Never name the mechanism.
5. **Hand off** with `ae_handoff` once a Manager+ economic buyer is in play.

## Riff rules (so it stays natural)
- Drop the number, then go quiet. Let the silence work.
- Mirror their last 1–3 words to keep them talking before the next question.
- One question at a time; never stack two.
- If they're junior (Coordinator/Technician), your real goal is the name of whoever signs — thread up.

## Guardrail — internal only
This coaches the rep; it is not buyer copy. In anything the prospect sees, never name the AV-matrix
mechanism (*matrix/switchboard/routing switch*) or third-party brands — "your CMS / LMS," pooled =
"a more affordable path, a starting point, not a quote." The AE owns fit, pricing, POC.
See `epiphan-ai-mcp-guide-skill`.

<success_criteria>
- [ ] Every calculator input the rep needs is covered by exactly one killer question (plus a Label / Job / Insight fallback layer)
- [ ] Questions are one breath long, sayable five ways, and spec-true (every spec re-verified live via `search_product_knowledge`/`search_product_catalog` — never sourced from the illustrative table alone)
- [ ] The flow ends with a Challenger reframe on the cost-of-inaction number and, when a Manager+ EB is in play, an `ae_handoff`
- [ ] No buyer-facing copy names the AV-matrix mechanism or third-party brands; pooled = "a more affordable path, a starting point, not a quote"
- [ ] Junior contact? The coached goal shifts to threading up to whoever signs
- [ ] Output delivered as one question card per input (`input`/`layer`/`line`/`why_it_fits`), per the Output contract above
</success_criteria>

<dependencies>
## MCP tools (Epiphan AI)
- `search_product_knowledge`, `search_product_catalog` — live spec-verification gate; required before any spec is cited in a question (see Spec-true above)
- `ae_handoff` — BDR→AE handoff package (account + champion + signal); the flow's terminal action once a Manager+ economic buyer is in play

## Sibling skills referenced
- `jobs-to-be-done-skill`, `never-split-the-difference-skill`, `challenger-sale-skill` — source the four question layers
- `epiphan-ai-mcp-guide-skill` — MCP tool reference and the spec-verification pattern this skill reuses
</dependencies>

## Failure Handling
Per `skill-audit/specs/self-healing-template.md`:
- **success** — vertical/inputs identified, every cited spec verified live, question cards delivered.
- **partial** — `search_product_knowledge`/`search_product_catalog` was unavailable and the coach fell
  back to the illustrative spec table (flagged unverified to the rep), OR `ae_handoff` failed to fire
  — name the degraded stage in the sidecar's `error` field.
- **error** — no question cards were produced at all (vertical/inputs couldn't be identified).

Retry once on a transient `search_product_knowledge`/`search_product_catalog` failure; if it still
fails, degrade to the illustrative table (marked unverified) rather than silently treating it as
live-confirmed, and mark the run `partial`. If `ae_handoff` can't be reached, tell the rep to hand off
manually rather than silently dropping the handoff. Halt only if the vertical/inputs can't be
identified at all.

## Emit Outcome Sidecar
As the final step, write to `~/.claude/skill-analytics/last-outcome-cost-discovery-coach-skill.json`:
```json
{"ts":"[UTC ISO8601]","skill":"cost-discovery-coach","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"inputs_covered":[n],"question_cards_produced":[n],"specs_verified_live":[n],
            "specs_fell_back_to_table":[n],"ae_handoffs_triggered":[0|1]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use "partial" if any spec fell back to the illustrative table instead of a live lookup, or `ae_handoff`
degraded — name the degraded stage in `error` (e.g. `"spec verification degraded to fallback table"`).
Use "error" only if no question cards were produced. The `version` above must match this skill's
`config.json` version — don't hardcode it a second time.
