# Greenfield Signals + Product-Fit Map

> INTERNAL. Used by `greenfield-pearl-tracker` to classify and score opportunities from
> `hubspot_search_deals` + `clari_search_calls`/`clari_get_call_summary`.

## The aging-vs-greenfield test (one question)
**"Is there an install base to feel pain about?"**
- **Yes → aging.** Use the cost-of-inaction motion (Higher Ed, Community College, established corp).
- **No → greenfield.** Per-project / net-new; price the risk or the speed, not the install base
  (Broadcast, Live Events, new-build Courts/Gov't/Corporate).

## Greenfield keyword signals (scan call summaries + deal notes)
**Build:** "new building", "renovation", "standing up a new studio / courtroom / HQ", "phase 1",
"breaking ground", "fit-out".
**Mobile / remote:** "fly-kit", "flyaway", "fly-pack", "road kit", "case", "remote production",
"REMI", "onsite", "field", "tour", "venue-to-venue".
**Automation / ease (post-NAB):** "automate the workflow", "fewer operators", "easier to use",
"one-button", "no crew", "set up fast", "tear down".
**Per-project:** "per event", "per show", "per game", "rental", "one-off".
**Event triggers:** "NAB", "saw you at NAB", "since the show".

## Scoring (quick rubric, 0–5)
- +2 explicit greenfield keyword in a call quote (not just a deal name)
- +1 Manager+ / economic-buyer title on the thread (Chief Engineer, TD, Court Admin, Dir Workplace Tech)
- +1 timeline named (FY, "by fall", "before the season")
- +1 budget or phase named
- −2 single-threaded below Manager level (every 2026 loss was single-threaded)

## Product-fit map by greenfield signal
| Signal | Lead product | Why (spec-true) |
|---|---|---|
| Fly-kit / fast setup | **Pearl Mini** | portable switcher, multi-cam out of one case |
| No operator / automation | **EC20** | PTZ + AI tracking, publishes straight to your CMS, no encoder |
| Remote / multi-site production | **Epiphan Unify** | centralized remote multi-source |
| Single-source edge capture | **Pearl Nano** | one cable, PoE+ |
| Multi-cam flagship / 6 ISOs | **Pearl-2** | 6 isolated full-HD channels |
⚠️ No "fly-kit" doc page exists — it's positioning. Ground hard specs via `search_product_knowledge`.

## Vertical → greenfield strength
Broadcast (post-NAB) **HIGH** · Live Events **HIGH** · new-build Courts/Gov't/Corporate **MED–HIGH** ·
Higher Ed / Community College **LOW** (aging motion instead). Full pack:
`epiphan-ai-mcp-guide-skill/reference/verticals.md`.
