# Skills Library

**Branch**: main | **Updated**: 2026-01-01

## Status
Production-ready skills library with **22 skills** (2 stable, 20 active). All skills now comply with Anthropic YAML specification. New strategic framework skills added.

## Today's Session (2026-01-01)

### Completed
- [x] Fixed YAML frontmatter for all 19 existing skills (Anthropic spec)
- [x] Added `business-model-canvas-skill` (Osterwalder's 9 blocks)
- [x] Added `blue-ocean-strategy-skill` (ERRC, Strategy Canvas, Six Paths)
- [x] Enhanced `unsloth-training-skill` with 15+ new features (FP8, Docker, vision, mobile)
- [x] Added reference files for `worktree-manager-skill`
- [x] Rebuilt all zip files with SKILL.md at root level
- [x] Updated SKILLS_INDEX.md

### Key Discovery
Anthropic YAML spec requires:
```yaml
---
name: "skill-name"
description: "Description. Use when: trigger1, trigger2."
---
```
- Quoted values required
- Only `name` and `description` allowed
- Single-line descriptions

## Current State

### Skills by Category (22 total)

| Category | Skills |
|----------|--------|
| **Strategy** | business-model-canvas, blue-ocean-strategy |
| **Infrastructure** | unsloth-training, runpod-deployment, voice-ai, groq-inference, langgraph-agents, supabase-sql, stripe-stack |
| **Dev Tools** | worktree-manager, extension-authoring, debug-like-expert, planning-prompts |
| **Business** | crm-integration, gtm-pricing, research, sales-revenue, content-marketing, data-analysis, trading-signals |
| **Core** | workflow-orchestrator, workflow-enforcer (stable), project-context (stable) |

### Deployment Status
- All 22 skills in `active/` and `stable/`
- 23 zips in `dist/` (ready for Claude Desktop upload)
- All committed to GitHub

## Blockers
None

## Next Tasks
| Priority | Task | Notes |
|----------|------|-------|
| P1 | Upload new skill zips to Claude Desktop | Test trigger activation |
| P2 | Test business-model-canvas skill | Use on real startup idea |
| P3 | Test blue-ocean-strategy skill | Apply to market analysis |

## Recent Commits
```
ea1cac4 feat(skills): Add strategic frameworks + fix YAML spec compliance
8efb839 Add stripe-stack-skill for Stripe + Supabase integrations
2a70139 feat(skills): Add comprehensive Workflow Orchestrator Skill v2.0
```

## Quick Commands
```bash
# View all skills
cat SKILLS_INDEX.md

# Check zips
ls dist/*.zip | wc -l  # Should be 23

# Upload to Claude Desktop
# Drag zip file to Claude Desktop settings > Skills
```

## Tech Stack
Markdown | YAML frontmatter | Progressive Disclosure Architecture
