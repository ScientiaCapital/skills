# Patch: cost-discovery-coach-skill

**Score:** trigger=5 tool_integration=4 output_contract=3 failure_handling=1 maintainability=5 (sum=18/25)

**Highest-leverage single change (S effort):** Add the standard Emit Outcome Sidecar stage and move the hardcoded spec table behind a search_product_knowledge lookup.
**Expected impact:** Brings the skill into the analytics framework (currently invisible) and removes spec-rot risk on the one place it states numbers.

## Description

**Before:**
> Turns the cost-of-inaction calculator's inputs into tight, killer discovery questions per vertical — JTBD job, Never-Split calibrated question, Challenger insight. Use when: discovery questions, how to ask, calculator discovery, cost of inaction questions, SDR call prep, what do I ask, qualify the room count, broadcast/live-events/corporate discovery.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] failure_handling
- **Evidence** (line 70): "</success_criteria>"
- **Issue:** Skill ends at </success_criteria> with NO Emit Outcome Sidecar section at all — unlike the other five skills it writes no ~/.claude/skill-analytics/last-outcome-*.json, so the self-improvement framework captures zero outcomes for it.
- **Fix:** Add the standard Emit Outcome Sidecar stage writing last-outcome-cost-discovery-coach.json.

### [MED] tool_integration
- **Evidence** (line 29-30): "Pearl-2 = 6 isolated full-HD channels; Pearl Nexus = 2 recommended (3 max); EC20
  publishes **straight to your CMS, no encoder in the path**; Edge fleet management is free."
- **Issue:** Concrete specs hardcoded in the body. It correctly INSTRUCTS verification ('Every spec cited must be verified ... never improvise a spec') but bakes the numbers in as source of truth, so they silently rot if the catalog changes. Borderline vs house rule 1.
- **Fix:** Move the spec table to a runtime search_product_knowledge lookup; keep only the instruction to verify in SKILL.md.

### [MED] output_contract
- **Evidence** (line 51): "5. **Hand off** with `ae_handoff` once a Manager+ economic buyer is in play."
- **Issue:** Names ae_handoff as terminal action but defines no output artifact for the coaching itself (no structured question-set format, no delivery target) — deliverable is implicit.
- **Fix:** Define the output contract: a per-input question card (Killer Q / Label / Job / Insight) block, plus the ae_handoff trigger condition.

## Missing tool references

- search_product_knowledge
- ae_handoff (referenced but not wired to a named MCP tool)

## Self-healing gap (see specs/self-healing-template.md)

Largest gap of the six: no outcome sidecar, no failure/partial definition, no retry->degrade->alert->halt ladder, no run log. A well-written coaching doc with zero run-state instrumentation.

## Overlap candidates (flag only — no removal)

- orlob-discovery-framework-skill
- meddic-call-prep-auto-skill
- sales-call-prep-assistant
- epiphan-call-playbook
