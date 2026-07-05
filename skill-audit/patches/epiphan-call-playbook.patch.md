# Patch: epiphan-call-playbook

**Score:** trigger=5 tool_integration=5 output_contract=4 failure_handling=3 maintainability=5 (sum=22/25)

**Highest-leverage single change (S effort):** Add a 'spec bank verified on DATE — re-verify if older than N days' staleness marker plus a config block for the booking link/roster.
**Expected impact:** Prevents the verified spec bank from silently going stale and centralizes drift-prone roster/link.

## Description

**Before:**
> Canonical Epiphan cold + discovery CALL playbook for Tim's BDR/SDR team (Tim, Edgar, Vasil). The phone-call sibling to sdr-email-sms-playbook. Covers the opener, the live discovery flow (Orlob-applied per vertical), objection handling, spec-accurate talking points by product, and the close/next-step. Every spec verified via Epiphan AI search_product_catalog / search_product_knowledge. Use when prepping or making cold calls, writing or reviewing call scripts, coaching reps, building dial-list talking points, or when the sdr-call-coaching task needs the canonical "what good sounds like" reference. Trigger on: call script, cold call, discovery call, opener, objection handling, talking points, what to say on the phone, dial list talking points, SDR coaching reference, Pearl/EC20/Nexus pitch on a call.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] output_contract
- **Evidence** (line 162): "AE discovery call (Phil or Lex): https://meetings.hubspot.com/timkipper/discovery-call"
- **Issue:** Reference skill (no outbound artifact expected), but booking link and rep roster (Tim/Edgar/Vasil) hardcoded in prose; drift risk when roster/link changes.
- **Fix:** Declare booking link + current roster once in a config block (or reference sdr-call-coaching Identifiers); note Vasil 'ramping' caveat has a known late-July 2026 removal date.

### [LOW] tool_integration
- **Evidence** (line 33): "Before quoting any spec, price, or competitive claim that is NOT in the "Verified spec bank" below, look it up live (search_product_catalog for SKUs/pricing/short names, search_product_knowledge for technical/integration)."
- **Issue:** Model implementation of house rule 1 — spec-accuracy gate is explicit and non-negotiable. Cited as the reference standard other skills should copy.
- **Fix:** None — propagate this exact gate to meddic-call-prep-auto and call-recording-analyzer.

### [LOW] failure_handling
- **Evidence** (line 28): "# Epiphan Call Playbook (v1, 2026-06-17)"
- **Issue:** Static reference skill emits no outcome sidecar and no run log, so its usage/health is invisible to the analytics pipeline the other call skills feed.
- **Fix:** Optional: emit a lightweight sidecar when loaded as a coaching reference, for parity with orlob-discovery-framework.

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no retry->degrade->alert ladder, no run log — acceptable for a static reference, but no 'spec bank last-verified' staleness check, so the 2026-06-17 verified facts silently age.

## Overlap candidates (flag only — no removal)

- orlob-discovery-framework
- sdr-email-sms-playbook
- sales-call-prep-assistant
- sdr-dial-lists
