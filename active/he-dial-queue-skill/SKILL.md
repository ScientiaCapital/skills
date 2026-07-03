---
name: he-dial-queue
description: "Use when building or refreshing the Higher-Ed SDR pod's daily dial queue, tiering callable leads into Tier 1/2/3, preparing a Nooks dial list from HubSpot, or checking Higher-Ed callable dial inventory."
schedule: "0 6 45 * * 1-5"
timezone: "America/New_York"
---

# Higher-Ed Dial Queue Builder (SDR Pod Lead Engine v1)

<objective>
Build the 4-SDR pod's daily tiered dial queue for the Higher-Ed vertical from the EXISTING HubSpot pool (follow-up-first). Apply Golden Rules + AE-ownership + deal-association suppression, classify into Tier 1 (hot + recently touched) → Tier 2 (hot, not recently touched) → Tier 3 (warm), order, assign SDRs, and emit a Nooks-ready Google Sheet. Monitor inventory and flag a capped Apollo greenfield top-up only when Tier 1+2 falls below the floor. Credit burn is near zero at steady state.
</objective>

<quick_start>
**Trigger:** M-F 6:45 AM ET (before morning-brief 7:30, before pod dials).
**Manual:** "Build HE dial queue" / "Refresh pod dial list".
**Config:** `reference/verticals/higher_ed.md` — lifecycle values, DIALABLE set, suppression (AE IDs, deal rules), tiering, floors, ATL/BTL, CMS signals. All knobs live there.
**Dependencies:** HubSpot (portal 21530819) read; Google Drive (Sheet); Slack (alert). Apollo only on top-up.
**Output:** Google Sheet `HE Dial Queue — <YYYY-MM-DD>` (Tier 1→2→3) + inventory status + sidecar JSON.
**Dialer:** Nooks (imports the Sheet / HubSpot natively). NOT Salesfinity.
</quick_start>

<success_criteria>
- [ ] Pull HE callable pool from HubSpot, filtered to the DIALABLE lifecycle set (keeps result < 10k cap), paginated to completion
- [ ] Apply suppression: AE-ownership (<90d), open-deal assoc, recently-closed-deal assoc, bad lead_status, Golden Rules
- [ ] Classify Tier 1/2/3 using REAL lifecyclestage values + `notes_last_contacted` recency (TIER1_RECENCY_DAYS)
- [ ] Order Tier 1 → Tier 2 → Tier 3; assign SDRs round-robin across the daily target (BLOCKED until roster confirmed)
- [ ] Emit Google Sheet (text/csv → auto-converts to Sheet) with contract columns; capture returned file URL
- [ ] Inventory check: if Tier 1+2 < floor, Slack-alert + flag capped Apollo top-up (≤50/day)
- [ ] (Gated) Stamp he_dial_tier + he_dial_date if the HubSpot property exists
- [ ] Emit sidecar JSON; consume ZERO Apollo/Clay credits unless top-up fired
</success_criteria>

<workflow>

## Stage 0: Load vertical config
Read `reference/verticals/higher_ed.md` — the single source for lifecycle internal values, DIALABLE set, AE_SUPPRESS_SET, deal-suppression rules, TIER1_RECENCY_DAYS, the inventory floor formula, ATL/BTL, and CMS signals. Keep values there, not here.

## Stage 1: Query the HE callable pool (HubSpot)
**MCP tool:** `search_crm_objects` (objectType `contacts`).
**Properties:** `firstname, lastname, email, phone, mobilephone, jobtitle, company, lifecyclestage, hs_lead_status, notes_last_contacted, hubspot_owner_id, industry, num_associated_deals, hs_lastmodifieddate`.

**Filter — OR filterGroups, each AND'd with the DIALABLE lifecycle set so the result stays under HubSpot's 10k search ceiling:**
- Phone present: include a group for `phone HAS_PROPERTY` AND a group for `mobilephone HAS_PROPERTY` (a contact with only a mobile must still appear).
- HE membership: `email CONTAINS_TOKEN "edu"` OR `industry CONTAINS_TOKEN "education"` (also "higher"/"university"/"college").
- Lifecycle: `lifecyclestage IN [opportunity, salesqualifiedlead, 970124947, marketingqualifiedlead, 1217869329, lead, 1028712882]` — the DIALABLE set. This EXCLUDES customer/Declined/Junk/Nurture at the query layer, cutting ~11.5k raw down to ~3.5k dialable (well under the 10k cap).

**Pagination:** page with the cursor/`offset` the API returns until `total` is covered. **Guard:** if `total` ≥ 9,900, the 10k search ceiling is in play — partition the query (e.g. by `hs_lastmodifieddate` ranges or per-lifecycle-bucket) and union the pages; log a warning and set sidecar `status:partial` if the cap is hit.

> Caveat: `industry` is free-text and there is no email domain-suffix operator; `"*.edu"` over-matches (~67k) — use the bare `"edu"` token, then refine in Stage 2.

## Stage 2: Refine + per-contact suppression
Drop a contact if any:
- **Not truly HE:** email does NOT contain `.edu` (incl. `.edu.<cc>`) AND `industry` has no education token. (Keep international `.edu.au` etc. Do NOT drop solely because `industry` is blank when the email is `.edu`.) Track the drop count; if > 25% of the pool is dropped here, set `status:partial` and log the delta vs the warehouse's ~5,312.
- **AE-owned:** `hubspot_owner_id` ∈ AE_SUPPRESS_SET = {Lex `82625923`, Ron `423155215`, Phil `190030668`, Anthony `165812850`, Anh `165815985`} AND ownership/last-touch < 90 days. **KEEP (dialable, do NOT drop):** Robert `158872429` (works new leads), Tim `87486452` (BDR).
- **Bad lead status:** `hs_lead_status` ∈ {`UNQUALIFIED`, `BAD_TIMING`}.
- (Lifecycle skip/route-out already handled at the query layer; Nurture `970063423` if present → email-only.)
- Golden Rules (Customer-domain / Channel Partner / Device Owner): apply `phone-verification-waterfall-skill/golden-rules-filter.md`.
- **Suppressed (Stage S gate):** `bdr_suppression_until` IS SET AND > TODAY → drop. INCLUDE if not set or < TODAY (cooling expired). HubSpot filter: `propertyName: "bdr_suppression_until", operator: "NOT_HAS_PROPERTY"` OR `operator: "LT", value: TODAY_ISO`. Template: phone-verification-waterfall-skill "Stage S — Suppression Gate".

## Stage 2b: Deal-association suppression (efficient set-based)
Build an EXCLUDE-by-deal contact-ID set, then remove those contacts from the pool:
1. **Open deals:** `search_crm_objects` objectType `deals`, filter `dealstage NOT_IN [<closed stages>]` (closed stages are pipeline-specific — fetch via `get_properties` on `dealstage` once; typically `closedwon`/`closedlost`). Collect associated contact IDs (deals→contacts associations).
2. **Recently-closed deals:** `deals` with `closedate` ≥ today − **DEAL_COOLDOWN_MONTHS** (default 12). Collect associated contact IDs.
3. Exclude any queue contact whose ID is in either set.

> Rationale (per review): an associated open/recent deal is a more precise "hands-off" signal than owner alone. Set-based (query deals once) avoids per-contact lookups. `num_associated_deals` from Stage 1 is a cheap pre-filter (only contacts with >0 need checking).

## Stage 3: Tier classification
Buckets (config): **HOT** = {`opportunity`, `salesqualifiedlead`, `970124947`, `marketingqualifiedlead`}; **WARM** = {`1217869329`, `lead`, `1028712882`}.
```
recently_touched = notes_last_contacted set AND (today - notes_last_contacted) <= TIER1_RECENCY_DAYS   # default 30
IF bucket == HOT AND recently_touched:  tier = 1   # ~150-200
ELIF bucket == HOT:                     tier = 2   # ~1,000-1,100 (incl. never-touched)
ELSE (bucket == WARM):                  tier = 3   # ~2,300
```
> `notes_last_contacted` is a proxy (may be sequence-stamped, not a human dial). Default window 30d limits inflation. Prefer a true-dial signal (Nooks/Clari) if available.

## Stage 4: Order, assign SDRs, daily cut
1. Sort: tier ASC, then `notes_last_contacted` DESC within tier, then `hs_lastmodifieddate` DESC.
2. **Daily target:** default **240** (4 SDRs × 60), configurable. Top `target` rows = today's dials; rest stay queued for fall-through.
3. **SDR assignment — HARD PRECONDITION:** round-robin the top `target` across the confirmed pod roster. ⚠️ Roster names are **not yet confirmed** (placeholder `SDR-1..4`). Do NOT emit a production sheet with placeholder owners — block the full run until the roster is set (dry-run/sample is fine with placeholders).

## Stage 5: Emit the Nooks dial-queue Google Sheet
**MCP tool:** `mcp__claude_ai_Google_Drive__create_file`.
1. Build CSV text: header `contact_id,name,phone,email,tier,last_touch_date,lifecycle_stage,sdr_assignment` + one row per queued contact, ordered Tier 1→2→3. `phone` prefers `phone`, falls back to `mobilephone`. `lifecycle_stage` = human label. Escape commas/quotes per CSV.
2. Call: `title="HE Dial Queue — <YYYY-MM-DD>"`, `textContent=<CSV>`, `contentMimeType="text/csv"`. Per the tool, `text/csv` **auto-converts to a Google Sheet** (`application/vnd.google-apps.spreadsheet`) — do NOT set `disableConversionToGoogleType`. Optionally set `parentId` to the pod's Drive folder if known.
3. **Capture the returned File object's id/URL** → use in the sidecar and the Slack message. Nooks imports this Sheet (or a HubSpot view).

## Stage 6 (GATED): Stamp HubSpot tier property
Only if `he_dial_tier` (1|2|3) + `he_dial_date` contact properties EXIST (MCP cannot create them). `manage_crm_objects` batch-update the top `target` contacts. If absent: skip silently, log "tier-stamp skipped (property not provisioned)".

## Stage 7: Inventory monitor (greenfield top-up gate)
```
tier12 = count(tier in {1,2})
floor  = TIER12_DAILY_DIALS * 3        # default 67*3 ≈ 200 (Tier 1+2 consumption rate, NOT the 240 total target)
IF tier12 < floor:
    top_up_needed = true
    slack_send_message: "⚠️ HE Tier 1+2 low: <tier12> (< <floor>). Triggering capped Apollo top-up (≤50/day)."
ELSE:
    top_up_needed = false              # zero credits
```
Slack via `slack_send_message` (pod channel / Tim DM `U0AAJUZH2PK`). The ≤50/day Apollo top-up (no Clay waterfall) runs as a guarded sub-step or the inventory-monitor skill.

## Stage 8: Emit outcome sidecar
Write `~/.claude/skill-analytics/last-outcome-he-dial-queue.json`:
```json
{"ts":"[UTC ISO8601]","skill":"he-dial-queue","version":"1.1.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[est ms],
 "metrics":{"pool_dialable":[n],"tier1":[n],"tier2":[n],"tier3":[n],"suppressed_ae":[n],"suppressed_deal":[n],
            "daily_target":[n],"tier12":[n],"floor":[n],"top_up_flagged":[bool],"sheet_url":"[url]","credits_used":0},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use "partial" if the 10k cap was hit, the HE delta exceeded threshold, or a stage degraded; "error" only if no queue was produced.

</workflow>

---

## Validation protocol (first runs)
1. **Read-only dry run:** Stages 1–4 only. Print tier counts + 10-row sample. Reconcile total vs the warehouse's 5,312; sanity-check (T1 ~150-200, T2 ~1,000+, T3 ~2,300).
2. **Small write test:** emit the Sheet for the top 25 rows; eyeball columns + Tier ordering + the returned URL.
3. **Full run:** full queue → Sheet; Stage 6 only if the property exists; only after the SDR roster is confirmed.
Never run Stage 7's top-up unless the floor is genuinely breached.

## Hard preconditions (block a full production run)
- **SDR roster** (4 names) for `sdr_assignment` — SDR-1 = Edgar Marroquin `93367782` (recorded). ⚠️ **HOLD: do NOT build/assign a list for Edgar yet** (per Tim 2026-06-09). SDR-2..4 TBD.
- **AE_SUPPRESS_SET** — CONFIRMED: suppress Lex/Ron/Phil/Anthony/Anh; KEEP (dial) Robert `158872429` + Tim `87486452`. (No longer a blocker.)
- `he_dial_tier`/`he_dial_date` HubSpot properties (only if Stage 6 stamping wanted).
- Nooks↔HubSpot activity logging (for the downstream disposition loop).

## Known gaps / scoping-call items
- Closed `dealstage` values are pipeline-specific — fetch once via `get_properties` on `dealstage`.
- DEAL_COOLDOWN_MONTHS (6–12), TIER1_RECENCY_DAYS (≤90), daily target (200–240), TIER12_DAILY_DIALS — confirm at scoping.
- True-dial signal (vs sequence-stamped `notes_last_contacted`) — needs Nooks/Clari engagement read (disposition loop, separate component).

---

## Skill metadata
**Version:** 1.1 · **Status:** v1 (Higher-Ed, follow-up-first) · **Author:** Tim Kipper
**Integration:** HubSpot (21530819) + Google Drive + Slack; Apollo on top-up only; Nooks dialer (HubSpot/Sheet-native)
**Tier:** P1 (Core BDR Automation) · **Triggers:** Scheduled (M-F 6:45 AM ET) + Manual
**Feeds:** morning-brief (7:30 AM), the disposition feedback loop, and the daily pod digest.
