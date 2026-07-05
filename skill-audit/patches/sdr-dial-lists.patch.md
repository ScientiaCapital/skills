# Patch: sdr-dial-lists

**Score:** trigger=5 tool_integration=4 output_contract=5 failure_handling=3 maintainability=4 (sum=21/25)

**Highest-leverage single change (M effort):** Route Step 1/2 inventory through qualify_lead and add an outcome sidecar + run log
**Expected impact:** Removes reinvented dedupe/suppression drift and gives the queue an analytics trail like its siblings

## Description

**Before:**
> Daily SDR dial-list builder for Edgar Marroquin + Vasil Ivanov (Tim's SDRs). Builds each SDR their own ranked callable queue every weekday morning — HubSpot-owned contacts first, callback-owed prospects from Nooks, vertical-matched cold ATL/BTL — each row carrying spec-accurate talking points + calibrated discovery questions sourced from the epiphan-call-playbook skill. The dial-list sibling to Tim's morning-brief; same engine, run for the SDRs. Read-only except per-SDR Slack DM + an optional HTML/XLSX artifact. Use when the user says "build SDR dial lists", "Edgar's call list", "Vasil's dial queue", "feed the SDRs", "SDR morning queue".

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 50, 59): "A) HubSpot-owned callable contacts — `hubspot_search_contacts` with hubspot_owner_id={SDR owner_id} ... SUPPRESSION GATE: enforce the same lead-suppression rules ... (If a dedicated suppression spec/skill is installed, use it; else use the available HubSpot fields.)"
- **Issue:** No qualify_lead gate — dedupe/ATL-BTL/suppression is reconstructed inline from raw hubspot_search_contacts instead of routing through the canonical qualify_lead source of truth.
- **Fix:** Gate Step 1/Step 2 output through qualify_lead for dedupe + ATL-BTL + suppression, keeping HubSpot search only for inventory pull.

### [MED] tool_integration
- **Evidence** (line 52): "TECHNICAL-ACCURACY GATE (non-negotiable): ... verify live via `search_product_catalog` / `search_product_knowledge` before putting it on a row. Never invent specs."
- **Issue:** Spec-verification gate is present and correct, but there is no brand-voice gate (get_writing_style / check_my_copy) on the per-SDR Slack DM copy in Step 5.
- **Fix:** Add a check_my_copy pass on the Slack DM opener text before slack_send_message (low stakes since internal, but consistent with house rule 2).

### [MED] failure_handling
- **Evidence** (line 92-96): "=== EDGE CASES === - Vasil thin/zero owned inventory -> fill from greenfield ... - A referenced skill ... not installed this run -> note the gap in output, fall back ... continue."
- **Issue:** Good degrade ladder for edge cases, but no run log — nothing written to ~/.claude/skill-runs/ or a sidecar; unlike its siblings this skill emits no outcome JSON for analytics.
- **Fix:** Emit an outcome sidecar (per-SDR counts, fill flags, gate results) like callable-lead-count / he-dial-queue do.

### [LOW] trigger_quality
- **Evidence** (line 3): "description: Daily SDR dial-list builder for Edgar Marroquin + Vasil Ivanov ... Use when the user says "build SDR dial lists", "Edgar's call list", "Vasil's dial queue", "feed the SDRs", "SDR morning queue"."
- **Issue:** Excellent enumerated trigger set, but scope overlaps he-dial-queue (both build SDR dial queues, both name Edgar 93367782) — collision risk on 'build dial queue' phrasing.
- **Fix:** Add a disambiguation line: this builds per-SDR ALL-vertical queues; he-dial-queue builds the Higher-Ed pod queue.

## Missing tool references

- qualify_lead
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Has failure definition (never empty queue / never RED) and a degrade ladder (greenfield fill, fall-back to HubSpot-direct + live verify), but no retry step, no alert-on-total-failure, and no run log to ~/.claude/skill-runs/sdr-dial-lists.jsonl (no sidecar at all).

## Overlap candidates (flag only — no removal)

- he-dial-queue
- callable-lead-count
- morning-brief
