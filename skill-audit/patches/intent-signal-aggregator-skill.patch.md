# Patch: intent-signal-aggregator-skill

**Score:** trigger=4 tool_integration=3 output_contract=3 failure_handling=2 maintainability=4 (sum=16/25)

**Highest-leverage single change (M effort):** Wire intent signals to apollo_organizations_job_postings + apollo_organizations_enrich so 'Signals Detected' is real evidence, not narrated
**Expected impact:** Converts a well-gated but hollow report into a genuine live intent feed; keeps the strong Golden Rules gate it already has

## Description

**Before:**
> Monitor buyer intent signals across the web including job postings, tech changes, funding rounds, and leadership changes. Alerts when prospects show buying signals and prioritizes "hot" accounts. Use for timing-based prospecting.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 37, 59-79): "line 37 `Check HubSpot via mcp__claude_ai_Epiphan_Ai__hubspot_search_companies or ...hubspot_search_contacts before including any account` — signal sources unnamed"
- **Issue:** Golden Rules + suppression correctly gate through HubSpot MCP, but the actual signal SOURCING (job postings, funding, leadership — 59-79) invokes no tool. Apollo has apollo_organizations_job_postings + apollo_organizations_enrich; instead signals are described abstractly so 'Signals Detected' (98-112) would be invented.
- **Fix:** Wire detection to apollo_organizations_job_postings + apollo_organizations_enrich (and Clay track-event) so evidence is real.

### [MED] tool_integration
- **Evidence** (line 32): "line 32 `hubspot_owner_id IN [82625923 (Lex), 423155215 (Ron), 190030668 (Phil)]`"
- **Issue:** Owner IDs hardcoded inline rather than declared once — same triplet in contact-hunter (line 37) and CLAUDE.md. Drift risk. Also no qualify_lead final dedupe before an account is marked hot.
- **Fix:** Reference a single shared owner-ID source; add qualify_lead as final gate.

### [MED] output_contract
- **Evidence** (line 15, 82-146): "line 15 `Output: Prioritized intent signal report with hot accounts` and line 134 `## Weekly Digest`"
- **Issue:** Report format defined but delivery is not — no Slack DM / Gmail draft / file for the weekly digest, no handoff to a dial-list/sequence skill for hot accounts. Terminal Markdown only.
- **Fix:** Define delivery (Slack digest or hand hot accounts to sdr-dial-lists / contact-hunter); draft-first any outreach.

### [MED] failure_handling
- **Evidence** (line 150-159): "lines 152-159 outcome sidecar with signal_types breakdown"
- **Issue:** Sidecar is only failure signal; no behavior when a source returns nothing/errors, no run log. 'partial' (159) not mapped to specific source failures.
- **Fix:** Add per-source degrade ('funding empty -> proceed with hiring, flag partial') and run-log append.

### [LOW] maintainability
- **Evidence** (line 122-130): "line 123 `| Funding | 15 | 3-5 days | 18% |` win-rate table with hardcoded benchmarks"
- **Issue:** Signal win-rate benchmarks are hardcoded illustrative numbers that read as real and will drift/mislead. 161 lines otherwise lean.
- **Fix:** Mark benchmarks illustrative or source from outcome data.

## Missing tool references

- mcp__claude_ai_Apollo_io__apollo_organizations_job_postings
- mcp__claude_ai_Apollo_io__apollo_organizations_enrich
- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Strong on gates (Golden Rules + Suppression) but no failure definition per signal source, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/intent-signal-aggregator.jsonl. Sidecar status is the only observability.

## Overlap candidates (flag only — no removal)

- linkedin-sales-navigator-alt-skill
- lookalike-customer-finder-skill
- weak-signal-synthesizer
