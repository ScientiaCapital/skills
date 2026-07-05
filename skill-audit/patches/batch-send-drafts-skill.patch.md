# Patch: batch-send-drafts-skill

**Score:** trigger=5 tool_integration=4 output_contract=5 failure_handling=3 maintainability=4 (sum=21/25)

**Highest-leverage single change (S effort):** Replace the inline ATL substring heuristic with a qualify_lead call per recipient.
**Expected impact:** Prioritization matches the canonical ATL/BTL taxonomy instead of a partial keyword list, so ATL-first ordering is actually correct.

## Description

**Before:**
> Review and batch-send staged Gmail BDR outreach drafts. Lists all queued drafts, shows a prioritized review table (recipient / subject / vertical), and generates one-click Gmail send links so Tim can flush the outreach queue in under 2 minutes. Trigger: send staged drafts, flush draft queue, batch send drafts, review my drafts, what drafts do I have.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] tool_integration
- **Evidence** (line 55-57): "**ATL signal** (from subject or recipient name if available):
- Title keywords: Director, VP, CIO, Dean, Provost, Superintendent -> ATL"
- **Issue:** Re-implements ATL/BTL classification inline from a truncated keyword list instead of gating through qualify_lead (dedupe/ATL-BTL source of truth per house rule 3). The inline list is a strict subset of CLAUDE.md's full ATL taxonomy, so it will misclassify.
- **Fix:** Call qualify_lead to resolve ATL/BTL per recipient rather than substring-matching the subject line.

### [MED] failure_handling
- **Evidence** (line 41): "If `list_drafts` returns minimal header data, call `mcp__claude_ai_Gmail__get_thread` on the `threadId` of each draft to get full headers."
- **Issue:** Has a sensible degrade path for missing headers but no defined behavior if list_drafts itself errors/returns empty, and no run log — only the analytics sidecar.
- **Fix:** Add explicit empty-queue and list_drafts-error handling (report + halt) and a run log line.

### [LOW] maintainability
- **Evidence** (line 57): "- Title keywords: Director, VP, CIO, Dean, Provost, Superintendent -> ATL"
- **Issue:** Hardcoded ATL keyword subset duplicates CLAUDE.md ATL/BTL taxonomy and will drift as the canonical list evolves.
- **Fix:** Reference the canonical classification (or qualify_lead) instead of copying a partial keyword list.

## Missing tool references

- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Good structured stages and one degrade path (get_thread fallback), but no explicit error-state ladder for the primary list_drafts call and no run log to ~/.claude/skill-runs/{skill}.jsonl beyond the analytics sidecar.

## Overlap candidates (flag only — no removal)

- morning-brief-skill
- sequence-load-skill
