# Patch: challenger-sale-skill

**Score:** trigger=5 tool_integration=1 output_contract=2 failure_handling=2 maintainability=4 (sum=14/25)

**Highest-leverage single change (S effort):** Add a spec-verification + brand gate before any product claim or email is emitted (search_product_knowledge, then check_my_copy).
**Expected impact:** Eliminates memory-stated Pearl specs and off-voice copy in the highest-risk customer-facing output.

## Description

**Before:**
> The Challenger Sale methodology — Teach-Tailor-Take Control framework for B2B sales. Use when: challenger sale, commercial teaching, constructive tension, reframe, teach tailor take control, insight selling, commercial insight, challenger rep.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 238): ""This is exactly what Pearl-2 was built for — a dedicated hardware encoder that captures, streams, and records simultaneously with zero PC dependency. When the network drops, it keeps recording locally.""
- **Issue:** Customer-facing product specs (Pearl-2 local-record-on-network-drop, LMS/LTI integration list at 254-255) are stated from memory, violating house rule 1 — no call to search_product_catalog / search_product_knowledge.
- **Fix:** Insert a gate: before emitting any product capability claim, call search_product_knowledge / search_product_catalog and cite verified specs.

### [HIGH] tool_integration
- **Evidence** (line 257-274): "### Cold Email (Challenger Style)
```
Subject: Lecture capture at [University]"
- **Issue:** Generates customer-facing email copy with no brand-voice gate (get_writing_style / check_my_copy) per house rule 2.
- **Fix:** Add a Brand Gate step that runs check_my_copy on every generated email/pitch before output.

### [MED] output_contract
- **Evidence** (line 257-274): "### Cold Email (Challenger Style)
```
Subject: Lecture capture at [University]"
- **Issue:** Produces outbound email copy but defines no delivery mechanism (no Gmail draft-first), conflicting with the CLAUDE.md 'ALWAYS create Gmail drafts' workflow.
- **Fix:** Specify output as a Gmail draft via create_draft (draft-first), not inline text.

### [MED] failure_handling
- **Evidence** (line 297): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Only failure semantics are in the outcome sidecar; no retry/skip/alert ladder and no run log to ~/.claude/skill-runs/.
- **Fix:** Add a failure ladder (missing product data -> call catalog, still missing -> flag placeholder -> alert Tim) and a run log line.

### [LOW] trigger_quality
- **Evidence** (line 3): "description: "The Challenger Sale methodology — Teach-Tailor-Take Control framework for B2B sales. Use when: challenger sale, commercial teaching, constructive tension, reframe, teach tailor take control, insight selling, commercial insight, challenger rep.""
- **Issue:** Enumerates trigger phrases well and is pushy; only risk is scope overlap with sales-methodology-implementer which also lists 'Challenger'.
- **Fix:** Add a disambiguation note: this skill is single-methodology deep-dive vs the multi-framework implementer.

### [LOW] maintainability
- **Evidence** (line 1-298): "298 total lines, single self-contained SKILL.md with tagged sections (<teach_framework>, <tailor_framework>, <take_control>)."
- **Issue:** Under 500 lines and well-structured; a large example_session (211-275) could move to references/ but no hardcoded owner IDs/list names that drift.
- **Fix:** Optionally relocate the higher-ed worked example to references/ to keep the core lean.

## Missing tool references

- search_product_catalog
- search_product_knowledge
- get_writing_style
- check_my_copy
- create_draft

## Self-healing gap (see specs/self-healing-template.md)

No failure definition beyond the sidecar status enum; no retry->degrade->alert->halt ladder; no run log to ~/.claude/skill-runs/challenger-sale.jsonl. A missing/unverifiable product spec should degrade to a placeholder + alert rather than being asserted from memory.

## Overlap candidates (flag only — no removal)

- sales-methodology-implementer-skill
- sales-revenue-skill
- demo-execution-playbook-skill
