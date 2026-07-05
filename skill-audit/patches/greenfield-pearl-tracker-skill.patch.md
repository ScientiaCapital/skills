# Patch: greenfield-pearl-tracker-skill

**Score:** trigger=5 tool_integration=4 output_contract=4 failure_handling=3 maintainability=5 (sum=21/25)

**Highest-leverage single change (S effort):** Add the standard outcome-sidecar emission + run log, and convert inline product specs to positioning labels enforced by a required search_product_knowledge call
**Expected impact:** Gives the strongest skill the observability the others already have and closes the from-memory-spec house-rule gap

## Description

**Before:**
> Find and track greenfield Pearl/EC20 opportunities from live CRM + Clari signals — new-build, remote production, and post-NAB broadcast fly-kit / automation. Use when: greenfield opportunities, new build, fly kit, remote production, broadcast deals, mobilization, find new logos, NAB signals, who's building.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] tool_integration
- **Evidence** (line 56-62): "line 61 `There is no "fly-kit" doc page ... Ground hard specs via search_product_knowledge; frame the fly-kit story, don't cite a spec sheet` and line 56 `Pearl Mini — portable switcher ... EC20 — PTZ, direct-to-CMS`"
- **Issue:** Product-fit map states specs (Pearl Mini 'portable switcher', EC20 'PTZ, direct-to-CMS, no operator', Pearl Nano 'PoE+') from memory. It correctly instructs grounding via search_product_knowledge for hard specs, but the inline spec claims themselves violate house rule 1 and could be cited before the tool runs.
- **Fix:** Convert product-fit lines to positioning labels only; make search_product_knowledge a required call before any spec appears in output.

### [MED] failure_handling
- **Evidence** (line 74-80): "config.json present (824 bytes) but SKILL.md body has no sidecar block and success_criteria ends at line 80"
- **Issue:** Unlike the other five, NO outcome-sidecar emission in the body and no run log — so this live-data-driven skill produces zero analytics/observability. No defined behavior when Clari/HubSpot returns no calls for a rep.
- **Fix:** Add the standard outcome-sidecar emission + 'rep has no calls in window -> skip rep, note in output' degrade path.

### [LOW] tool_integration
- **Evidence** (line 70-72): "line 71 `## Guardrail — internal only ... Output is internal ... buyer-facing copy stays clean`"
- **Issue:** No brand voice gate (get_writing_style / check_my_copy) — acceptable because output is explicitly internal-only, but if a row's 'Next action' text is reused buyer-facing there's no gate. Scoped-OK gap, noted not heavily penalized.
- **Fix:** Add a one-line note: any copy promoted buyer-facing must pass check_my_copy.

### [LOW] tool_integration
- **Evidence** (line 17-19, 32): "lines 17-19 collaborator_owner_id Edgar `93367782` / Vasil `93782443` / Nyasha `94135434` and repEmails at line 32"
- **Issue:** SDR owner IDs and rep emails hardcoded in two places (quick_start 17-19 and How-to-run 25-33). Roster drift (per project memory: Edgar on HOLD, Vasil ramping caveats) means these go stale in-file.
- **Fix:** Declare the cohort roster once (config.json exists) and reference it, rather than repeating IDs.

### [LOW] tool_integration
- **Evidence** (line 17-36, 75): "success_criteria line 75 `Data pulled LIVE (HubSpot deals via collaborator_owner_id + Clari call summaries) — no invented signals`"
- **Issue:** Sources deals via hubspot_search_deals but does not run qualify_lead / Golden Rules on surfaced accounts. Lower risk (internal tracker of existing SDR-owned deals, not net-new outreach), but customer/channel status isn't checked.
- **Fix:** Optional: note surfaced accounts inherit their deal's qualification; no new-contact gate needed for internal tracker.

## Missing tool references

- search_product_knowledge (referenced but must be enforced pre-output)
- qualify_lead (optional for internal tracker)

## Self-healing gap (see specs/self-healing-template.md)

Best-structured of the six (progressive disclosure via reference/signals.md, live-data success criteria) but has NO outcome sidecar and NO run log — the one skill here with zero analytics emission. No degrade path when a rep's Clari window is empty; no retry ladder.

## Overlap candidates (flag only — no removal)

- intent-signal-aggregator-skill
- he-dial-queue-skill
