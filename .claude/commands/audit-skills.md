---
description: "Read-only audit of the BDR skill catalog — scores every skill, maps overlaps/gaps, and writes proposal patches (no skill files modified, nothing deprecated)"
argument-hint: "[skill-name ...]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent
---

# /audit-skills — BDR Skill Catalog Audit (Self-Healing, Read-Only)

You are the ORCHESTRATOR for a full audit of my BDR skill catalog. Nothing gets removed or deprecated. The audit itself is READ-ONLY: never modify any SKILL.md or bundled resource. All proposed changes ship as patch files for my approval.

## Context: who I am and what these skills serve

- Tim Kipper, BDR/Application Engineer at Epiphan Video. I book qualified demos for AEs Phil Sandler and Lex Evans and run an SDR team (Edgar, Vasil, Nyasha).
- Stack the skills orchestrate: Epiphan AI MCP (CRM, sales intel, device analytics, qualify_lead), HubSpot, Nooks, Apollo, Clay, Clari, Gmail, Slack, Google Calendar, ZoomInfo, Common Room.
- Non-negotiable house rules the audit must enforce: (1) product specs are never stated from memory — every customer-facing skill must call search_product_catalog / search_product_knowledge; (2) brand voice gate via Epiphan Brand (get_writing_style, check_my_copy) before customer-facing strings; (3) qualify_lead is the dedupe/ATL-BTL source of truth; (4) Epiphan-native tools preferred over generic when they overlap.

## Phase 0 — Inventory (orchestrator, no subagents)

1. Glob every skill directory. Search ALL of: `~/.claude/skills/`, `.claude/skills/`, and any plugin skill directories present in this environment. A skill = any directory containing SKILL.md.
2. Write `skill-audit/manifest.json`: one entry per skill with {name, path, frontmatter_description, line_count, bundled_resources[], last_modified}.
3. Print the manifest count and list to me. WAIT for my confirmation of scope before spawning agents. If I named specific skills to include/exclude, honor that.

## Phase 1 — Parallel audit (subagent swarm)

Spawn subagents via the Task tool, 5–6 skills per agent (keeps context tight; do not exceed 6). Each agent MUST:

1. Read the FULL SKILL.md and skim bundled resources for its assigned skills.
2. Score each skill 0–5 on five dimensions (rubric below).
3. Return findings as strict JSON matching the schema below. No prose outside the JSON.
4. EVIDENCE RULE: every finding must cite a quoted line or line range from the file. A claim with no quote is discarded by the orchestrator. Never describe a skill from its name alone.

### Scoring rubric (0 = absent/broken, 3 = functional, 5 = excellent)

- **trigger_quality**: Is the description specific, "pushy" (skills undertrigger by default — descriptions should enumerate trigger phrases and contexts), and free of collisions with sibling skills?
- **tool_integration**: Does it name the right tools in the right order? Deduct for: missing qualify_lead dedupe gate, missing spec-verification gate on customer-facing output, missing brand gate, manual steps that a named tool automates, generic tool used where an Epiphan-native equivalent exists.
- **output_contract**: Defined output format AND delivery mechanism (Gmail draft, Slack DM, XLSX, HubSpot list, HTML)? Draft-first for anything outbound?
- **failure_handling**: Does it define what a failed/partial run looks like and what to do (retry / skip / alert)? Does it log anywhere?
- **maintainability**: Under ~500 lines with progressive disclosure (references/ for detail)? Free of hardcoded values that drift (owner IDs, list names, dataset names should be declared in one place)?

### Per-skill JSON schema (return an array of these)

```json
{
  "skill": "", "path": "",
  "scores": {"trigger_quality": 0, "tool_integration": 0, "output_contract": 0, "failure_handling": 0, "maintainability": 0},
  "findings": [{"dimension": "", "severity": "high|med|low", "evidence": "quoted line(s)", "line_ref": "", "issue": "", "fix": ""}],
  "rewritten_description": "only if trigger_quality <= 3, else null",
  "overlap_candidates": ["skill names whose scope collides — flag only, never recommend removal"],
  "missing_tool_refs": ["tools this skill should call but doesn't"],
  "self_healing_gap": "what the skill lacks vs. the self-healing template",
  "one_improvement": {"change": "", "expected_impact": "", "effort": "S|M|L"}
}
```

## Phase 2 — Cross-skill synthesis (orchestrator)

After all agents return:

1. **Overlap matrix**: cluster skills with colliding scopes/trigger words (e.g., multiple daily-brief, call-prep, or outreach skills across plugin families vs. my custom ones). For each cluster, propose a disambiguation rule (which skill wins on which signal) — never removal.
2. **Gap analysis**: map the catalog against my BDR job map — inbound speed-to-lead, outbound dial prep, live-call support, post-call wrap, follow-up, list building, expansion, displacement, coaching, reporting, social, demo handoff. Name jobs with NO covering skill and jobs covered only by a generic (non-Epiphan) skill.
3. **Trigger collision report**: any two skills whose descriptions would fire on the same user phrase, with the phrase quoted.
4. **Score leaderboard**: all skills ranked by total score, worst first.

## Phase 3 — Shared specs (write once, reference everywhere)

Author these two spec files. Skills reference them; do not duplicate the logic into 40 files.

### `skill-audit/specs/self-healing-template.md`

Standard block every skill should adopt (propose as patch, don't apply):

- **Failure definition**: what counts as failed vs. partial (e.g., tool auth error, empty dataset, spec-verification miss).
- **Fallback ladder**: retry once with backoff → degrade (skip enrichment, proceed with core) → alert (Slack DM to the running rep) → halt with a written state file.
- **Run log convention**: every skill appends one JSON line to `~/.claude/skill-runs/{skill-name}.jsonl` with {ts, rep, inputs_hash, status, error, records_in, records_out}. This is the drift-detection substrate.

### `skill-audit/specs/suppression-spec.md`

One global lead-suppression rule, not per-skill:

- **State of record**: HubSpot contact properties `bdr_suppressed` (bool), `bdr_suppression_reason` (enum: no_email | no_phone | dismissed | bad_fit | do_not_contact), `bdr_suppressed_date`.
- **Fallback**: `~/.claude/skill-state/suppression.jsonl` when HubSpot write access is unavailable; reconcile to HubSpot on next authorized run.
- **Release condition**: suppression lifts on a NEW engagement signal (form fill, email reply, meeting booked, device registration, page visit via intent tooling) — define the exact signal checks.
- **Enforcement point**: every list-producing skill filters suppressed leads at Gate A (dedupe), immediately after qualify_lead.
- IMPORTANT: creating the HubSpot properties and writing suppression state are actions I must approve separately. The audit only specifies; it never writes to HubSpot.

## Phase 4 — Patches (proposals only)

- For every skill with any dimension ≤ 3: write a proposed patch to `skill-audit/patches/{skill-name}.patch.md` containing the rewritten description, the self-healing block referencing the template, and any tool-order fixes — as before/after diffs.
- For the 10 worst `trigger_quality` scores: if the skill-creator skill's description optimizer (`run_loop.py`, requires `claude -p`) is available in this environment, run it against a small trigger eval set built from my real phrasing patterns, and use its empirically best description in the patch. If unavailable, note that and keep the hand-rewritten description.

## Phase 5 — Report

- One self-contained HTML file at `skill-audit/report.html` (inline CSS/JS, no external deps): executive summary, score leaderboard, overlap matrix, gap analysis, trigger collision table, per-skill sections (scores, evidence-backed findings, patch link), suppression spec, and a final priority list.
- **Priority ranking**: score each recommended action ICE-style (Impact 1–5 × Confidence 1–5 ÷ Effort 1–5). Bucket into: Fix now (top decile), Monitor (log-and-watch), Revisit quarterly.
- **Sharing**: default is LOCAL ONLY. This report contains internal CRM logic and lead-handling rules. Do NOT deploy to any public URL unless I explicitly confirm, and if I do, require password protection on the deployment. Offer the safer path first: I share the HTML file directly via Slack/Drive with Victor, Phil, Lex.

## Guardrails (repeat: these override everything above)

- Read-only against all skill files, HubSpot, Nooks, and every MCP. Writes limited to the `skill-audit/` directory.
- Every finding carries quoted evidence or it is dropped.
- No skill is removed, renamed, or deprecated.
- Ask before Phase 1 (scope confirm) and before any deployment. Everything else runs without interruption.
