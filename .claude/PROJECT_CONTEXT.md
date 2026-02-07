# Skills Library

**Branch**: main | **Updated**: 2026-02-07

## Status
Production-ready skills library with **37 skills** (2 stable, 35 active). All skills comply with Anthropic YAML specification. All P1 tasks complete. Library fully documented with dependency graph. All commits pushed to origin.

## Today's Session (2026-02-07)

### Focus
- Morning standup + sprint planning
- Commit + push hubspot-revops-skill (#37)
- End-of-day audit + lockdown

### Done (This Session)
- [x] Commit hubspot-revops-skill + 6 metadata files
- [x] Push 5 commits to origin/main (now fully synced)
- [x] Security sweep (secrets=0, CVEs=N/A) — PASS
- [x] Quality gate (37/37 SKILL.md, index matches disk) — PASS
- [x] Update PROJECT_CONTEXT.md to current state

## Current State

### Skills by Category (37 total)

| Category | Count | Skills |
|----------|-------|--------|
| **Core** | 5 | workflow-orchestrator, cost-metering, portfolio-artifact, workflow-enforcer (stable), project-context (stable) |
| **Dev Tools** | 13 | extension-authoring, debug-like-expert, planning-prompts, worktree-manager, agent-teams, subagent-teams, agent-capability-matrix, git-workflow, testing, api-design, security, api-testing, docker-compose |
| **Infrastructure** | 8 | unsloth-training, runpod-deployment, voice-ai, groq-inference, langgraph-agents, openrouter, supabase-sql, stripe-stack |
| **Business** | 9 | crm-integration, gtm-pricing, research, sales-revenue, content-marketing, data-analysis, trading-signals, miro, hubspot-revops |
| **Strategy** | 2 | business-model-canvas, blue-ocean-strategy |

### Deployment Status
- All 37 skills in `active/` and `stable/`
- Zips in `dist/` (ready for Claude Desktop upload)
- All committed and pushed to GitHub
- Dependency graph current (DEPENDENCY_GRAPH.md)

### Known Tech Debt
- 26/37 skills missing config.json (legacy, non-blocking)
- `workflow-enforcer` lacks `-skill` suffix (naming inconsistency)

## Blockers
None

## Next Tasks
| Priority | Task | Notes |
|----------|------|-------|
| P3 | Skill version tracking | Add version field to config.json |
| P3 | Auto-healing for broken skills | /heal-skill command |
| P3 | Skill usage analytics | Track activation patterns |
| P3 | Integration tests for skill activation | Automated validation |
| P3 | Backfill config.json for 26 legacy skills | Standardize metadata |

## Recent Commits
```
c3bc872 feat(skills): Add hubspot-revops-skill, update metadata to 37 skills
0b1ad6f feat(skills): Add miro-skill, update all metadata to 36 skills
6a88989 feat(skills): Add subagent-teams + agent-capability-matrix + cost-metering + portfolio-artifact
767d54a feat(skills): Polish workflow-orchestrator with cost gate + progress rendering
12912c5 docs: Update all project docs to current state (36 skills, fix stale refs)
```

## Tech Stack
Markdown | YAML frontmatter | Mermaid diagrams | Progressive Disclosure Architecture
