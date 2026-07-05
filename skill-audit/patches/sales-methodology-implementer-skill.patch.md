# Patch: sales-methodology-implementer-skill

**Score:** trigger=3 tool_integration=1 output_contract=3 failure_handling=2 maintainability=4 (sum=13/25)

**Highest-leverage single change (M effort):** Replace the manual CRM-field prescription with a qualify_lead + Epiphan HubSpot MCP integration for deal scoring and write-back.
**Expected impact:** Deal scores become grounded in the ATL/BTL source of truth and persist to HubSpot instead of living in disposable markdown.

## Description

**Before:**
> Implement proven sales methodologies (MEDDIC, BANT, Sandler, Challenger, SPIN) across your team. Generate framework-specific questions, score deals, train reps, and enforce consistent qualification. Use when implementing or optimizing sales processes.

**After (proposed):**
> Team-wide sales methodology enablement (MEDDIC, BANT, Sandler, Challenger, SPIN, Value/Gap Selling): generate framework discovery questions, deal scorecards, rep training plans, and HubSpot scoring fields. Use when: implement MEDDIC across my team, build a BANT scorecard, train reps on Sandler, score this deal using [methodology], 30/60/90 sales enablement rollout, standardize qualification. (For single-call prep use meddic-call-prep-auto; for the Challenger narrative use challenger-sale.)

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 226-230): "### HubSpot Properties
- `meddic_score` (Number, 0-100)
- `meddic_metrics` / `meddic_decision_process` (Multi-line text)"
- **Issue:** Specifies CRM custom fields as a manual/generic integration plan but never calls the Epiphan HubSpot MCP or qualify_lead; scoring deals is done by hand rather than through the ATL/BTL source of truth (house rules 3 & 4).
- **Fix:** Wire deal scoring to qualify_lead and read/write HubSpot via the Epiphan CRM MCP instead of prescribing manual field creation.

### [MED] trigger_quality
- **Evidence** (line 3): "description: Implement proven sales methodologies (MEDDIC, BANT, Sandler, Challenger, SPIN) across your team. ... Use when implementing or optimizing sales processes."
- **Issue:** Generic and non-pushy — no enumerated trigger phrases in the description, and directly collides with challenger-sale-skill (Challenger), sales-revenue-skill (MEDDIC/SPIN), and meddic-call-prep-auto-skill.
- **Fix:** See rewritten_description; add explicit trigger phrases and a scope boundary (team-wide enablement/scorecards, not single-call prep).

### [MED] tool_integration
- **Evidence** (line 232-236): "### Salesforce Custom Fields
- `[Methodology]_[Component]_Score__c` (Number, 0-10) per component"
- **Issue:** Salesforce integration is out of scope for Tim's stack (HubSpot portal 21530819 per CLAUDE.md) and adds generic-CRM noise.
- **Fix:** Drop Salesforce or gate it behind an explicit non-HubSpot flag; default to Epiphan HubSpot MCP.

### [MED] failure_handling
- **Evidence** (line 283): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** No retry/skip/alert ladder or run log; sidecar status is the only failure signal.
- **Fix:** Add failure ladder + run log to ~/.claude/skill-runs/sales-methodology-implementer.jsonl.

### [LOW] output_contract
- **Evidence** (line 54-245): "### Output Format
```markdown
# Sales Methodology Implementation: [Methodology Name]"
- **Issue:** Output format is thoroughly specified (guide, scorecard, training plan) but delivery mechanism is undefined — no artifact/file/HubSpot destination.
- **Fix:** Name a delivery target (e.g., markdown doc or HubSpot note) for the generated scorecard/plan.

### [LOW] maintainability
- **Evidence** (line 1-285): "285 total lines, single file with one large Output Format block (54-245)."
- **Issue:** Under 500 lines; the giant embedded output template could move to references/ to keep the core scannable.
- **Fix:** Extract the output template to references/output-template.md.

## Missing tool references

- qualify_lead
- Epiphan CRM (HubSpot) MCP
- ask_agent

## Self-healing gap (see specs/self-healing-template.md)

No failure definition beyond sidecar status; no retry->degrade->alert->halt ladder; no run log to ~/.claude/skill-runs/sales-methodology-implementer.jsonl. Deal scoring has no source-of-truth tie-in (qualify_lead), so a scored deal can diverge from CRM reality with no reconciliation step.

## Overlap candidates (flag only — no removal)

- challenger-sale-skill
- sales-revenue-skill
- meddic-call-prep-auto-skill
- never-split-the-difference-skill
