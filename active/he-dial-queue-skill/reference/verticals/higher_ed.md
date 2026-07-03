# Vertical Reference — Higher Education (v1)

> Config for `he-dial-queue-skill`. Source of truth for the SDR Pod Lead Engine v1 (Higher-Ed, follow-up-first).
> Owner: Tim Kipper · Validated against HubSpot portal 21530819 on 2026-06-09.
> Multi-vertical (Broadcast, Live Events, Courts/Gov, HoW, K-12, CC) is v1.1+ — add sibling files in this folder.

## ICP

- **Vertical:** Higher Education · **ICP score:** 90 (highest)
- **Why first:** highest ICP, ~5,312 callable contacts already in the warehouse pass Golden Rules, follow-up-first keeps Apollo/Clay credit burn near zero.
- **Pod consumption:** 4 SDRs · 200–240 dials/day (50–60/SDR) · pool lasts ~5–6 weeks before greenfield top-up.

## Higher-Ed definition (membership filter)

A contact is Higher Ed if **either**:
- `company.industry` ∈ {`higher education`, `HIGHER_EDUCATION`, `education management`, `EDUCATION_MANAGEMENT`, `e-learning`, `E_LEARNING`}, **or**
- contact email domain ends in `.edu` (incl. international `.edu.<cc>`, e.g. `.edu.au`).

**Precise source = SQL warehouse** (validated 5,312 callable). Via HubSpot MCP this filter is *approximate*: `industry` is free-text and there is no email domain-suffix operator. Use `email CONTAINS_TOKEN "edu"` → **11,513 raw callable** (validated 2026-06-09); do NOT use `"*.edu"` (over-matches to ~67k). After dropping non-dialable lifecycle + Golden Rules + deal/AE suppression → ~5,312. Reconcile MCP count against the warehouse; if the post-filter delta is large (>25%), set sidecar `status:partial` and log it.

## Lifecycle tiering (REAL HubSpot internal values — portal 21530819)

`lifecyclestage` enum captured live (label → internal value):

| Label | Internal value | Bucket |
|-------|----------------|--------|
| Opportunity | `opportunity` | HOT (dialable) |
| Sales Qualified Lead | `salesqualifiedlead` | HOT (dialable) |
| Sales Accepted Lead | `970124947` | HOT (dialable) |
| Marketing Qualified Lead | `marketingqualifiedlead` | HOT (dialable) |
| New Lead | `1217869329` | WARM (dialable) |
| Lead | `lead` | WARM (dialable) |
| Cold Lead | `1028712882` | WARM (dialable) |
| Nurture | `970063423` | ROUTE-OUT (email-only) |
| Declined Lead | `45709743` | SKIP |
| Junk | `969926400` | SKIP |
| Customer | `customer` | SKIP (route to CS/AE) |

**DIALABLE set** (query Stage 1 with these only — keeps result < 10k): `opportunity, salesqualifiedlead, 970124947, marketingqualifiedlead, 1217869329, lead, 1028712882`.

**Tier assignment** (after Golden Rules + suppression, contact must have a phone):

- **Tier 1 — Hot + recently touched:** bucket = HOT **and** `notes_last_contacted` within **TIER1_RECENCY_DAYS** (default **30**; configurable up to 90). (~150–200; touch-true sweet spot ≈304.)
- **Tier 2 — Hot, not recently touched:** bucket = HOT **and** not within the window (incl. never-touched). (~1,000–1,100; the hidden bench.)
- **Tier 3 — Warm:** bucket = WARM. (~2,300.)

> **Tier-1 caveat:** `notes_last_contacted` can be stamped by bulk sequences, not human dials (observed 2026-06-09: timestamps seconds apart). It is a *proxy*, not a true-dial signal — Tier 1 may include sequence-only touches. A narrower window (30d) reduces inflation. If/when a human-dial signal exists (Nooks/Clari call engagement), prefer it. Flag for scoping call.

**Dial order:** Tier 1 → Tier 2 → Tier 3 (fall through only when the higher tier is exhausted for the day).

## Suppression (CONFIRMED 2026-06-09) — drop a contact if ANY

> Owner→person map is from **live HubSpot `get_properties`** (2026-06-09, authoritative). NOTE: older sibling artifacts (e.g. `morning-brief-2026-04-10.html`) map `158872429`→Tim — that mapping is **stale**; IDs were reassigned. Current live values below are correct.

1. **No phone:** both `phone` and `mobilephone` empty.
2. **AE-owned (anti-double-touch):** `hubspot_owner_id` ∈ **AE_SUPPRESS_SET** AND owned/last-touched < 90 days.
   - **AEs (SUPPRESS):** Lex Evans `82625923`, Ron Epstein `423155215`, Phil Sandler `190030668`, Anthony Taroni `165812850`, Anh Mai `165815985`. (CONFIRMED 2026-06-09: "everyone else suppress.")
   - **KEEP (dialable):** Robert Draxler `158872429` — works NEW leads, not deals-to-protect (confirmed); Tim Kipper `87486452` (BDR); + the 4 SDRs once rostered.
3. **Open-deal association:** contact is associated with **any open deal** (any pipeline; `dealstage` not in a closed stage) → suppress. (More precise than owner proxy.)
4. **Recently-closed deal:** contact is associated with a deal whose `closedate` is within **DEAL_COOLDOWN_MONTHS** (default **12**; configurable 6–12) → suppress (don't re-dial recently won/lost accounts).
5. **Non-dialable lifecycle:** `lifecyclestage` ∈ {`customer`, `45709743` Declined, `969926400` Junk}; `970063423` Nurture → route to email-only (not dial queue).
6. **Bad lead status:** `hs_lead_status` ∈ {`UNQUALIFIED`, `BAD_TIMING`}.
7. **Golden Rules:** Customer-domain / Channel Partner / Device Owner — apply the canonical rules in `phone-verification-waterfall-skill/golden-rules-filter.md` (live source). ATL/BTL maps: `callable-lead-count-skill/SKILL.md` + `scripts/scrapers/title_maps.py` (project repo).

Verify zero AE double-touches weekly via `ae_drift_detect`.

## ATL / BTL titles (Higher Ed)

**ATL (decision-makers / budget authority):** CIO, CTO, VP/AVP of Academic Technology, VP IT, Director of Classroom Technology, Director of IT Services, Director of Academic Technology, Director of Learning Spaces, Provost, Vice Provost, Dean, Director of Media/AV Services (budget-owning).

**BTL (skip for ATL-first; multi-thread context):** AV Engineer, AV Technician, Instructional Designer, Media Specialist, Classroom Support, Lab Coordinator, Multimedia Services staff, Video Production Specialist, Instructor/Professor/Faculty (non-admin).

## CMS displacement signals (competitive intel)

Incumbent lecture-capture / video platforms — flag for displacement messaging when detected:
**Panopto · Kaltura · YuJa · Echo360 · Opencast**

## Dialer contract (Nooks)

Nooks pulls from HubSpot/Sheet natively. v1 contract = a **Google Sheet** (one tab, ordered Tier 1→2→3), columns:
`contact_id, name, phone, email, tier, last_touch_date, lifecycle_stage, sdr_assignment`

Optional HubSpot enhancement (gated): once `he_dial_tier` (1|2|3) + `he_dial_date` contact properties are created in HubSpot UI (the MCP cannot create them), the skill also stamps them for native HubSpot/Nooks filtering.

## Inventory floor (greenfield top-up trigger)

- **Floor = TIER12_DAILY_DIALS × 3** (default `TIER12_DAILY_DIALS = 67` → floor ≈ 200; i.e. ~3 days of Tier 1+2 at the pod's Tier-1/2 consumption rate, distinct from the 240 total-dial target which includes Tier 3). Confirm the rate at scoping.
- When Tier 1+2 combined < floor → trigger capped Apollo greenfield top-up: **≤50 enrichments/day (<$25/day)**. No Clay phone waterfall in v1. Slack-alert the pod.

## Pod roster (SDR assignment)
- **SDR-1: Edgar Marroquin — HubSpot owner ID `93367782`** (active; confirmed 2026-06-09). "Edgar Yael" = Edgar (Yael) Marroquin.
- SDR-2..4: TBD (pod being assembled; 1 of 4).
- ⚠️ **HOLD — do NOT build/assign a dial list for Edgar yet** (per Tim 2026-06-09). His ID is recorded for config only; the queue builder must not emit a sheet or stamp tiers for him until released.

## Hard preconditions (block a real production run)
- AE_SUPPRESS_SET CONFIRMED: suppress Lex/Ron/Phil/Anthony/Anh; keep (dial) Robert `158872429` + Tim `87486452`.
- 4-SDR roster: SDR-1 = Edgar `93367782` (on HOLD); SDR-2..4 still TBD.
- `he_dial_tier`/`he_dial_date` properties created if Stage 6 stamping is wanted.
- Nooks↔HubSpot activity logging confirmed (for the downstream disposition loop).
