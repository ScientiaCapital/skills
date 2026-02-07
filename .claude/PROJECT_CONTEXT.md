# Skills Library

**Branch**: main | **Updated**: 2026-02-07

## Status
Production-ready skills library with **37 skills** (2 stable, 35 active). All skills comply with Anthropic YAML specification. All P1 tasks complete. Library fully documented with dependency graph. All commits pushed to origin.

## Today's Session (2026-02-07)

### Focus
- API-Awareness Upgrade sprint: propagate TaskCreate/Teams API across 6 orchestration skills

### Done (This Session)
- [x] Review + stage subagent-teams-skill diff (+137/-37: TaskCreate, TeamCreate, SendMessage)
- [x] Update agent-teams-skill: Native Teams API alternative section, cross-ref, limitations update
- [x] Update workflow-orchestrator-skill: TaskCreate progress rendering, activeForm pattern
- [x] Update agent-capability-matrix-skill: Progress tracking + Team coordination rows, model tier
- [x] Update workflow-enforcer: TaskCreate alongside TodoWrite in multi-step protocol
- [x] Update cost-metering-skill: TaskCreate/TeamCreate as zero-cost tools in integration table
- [x] Update SKILLS_INDEX.md: descriptions for all 6 modified skills
- [x] Update PROJECT_CONTEXT.md

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
