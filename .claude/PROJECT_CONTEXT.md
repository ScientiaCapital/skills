# Skills Library

**Branch**: main | **Updated**: 2025-12-23

## Status
Production-ready skills library with **17 skills** (2 stable, 15 active). Complete GTME competency stack from ICP definition to investor presentations.

## Current State

### Stable Skills (2)
- workflow-enforcer
- project-context-skill

### Active Skills (15)
| Category | Skills |
|----------|--------|
| Trading/Finance | trading-signals-skill |
| Sales/GTM | sales-outreach-skill, gtm-strategy-skill, demo-discovery-skill, revenue-ops-skill, pricing-strategy-skill |
| AI/Agents | langgraph-agents-skill, voice-ai-skill |
| Infrastructure | runpod-deployment-skill, supabase-sql-skill |
| Research | market-research-skill, technical-research-skill, opportunity-evaluator-skill |
| Content | content-marketing-skill |
| Data | data-analysis-skill |

### Deployment
- All 17 skills in `~/.claude/skills/` (global access)
- All 17 zips in `dist/` (Claude Desktop)
- All committed to GitHub

## Blockers
None

## Next Tasks
| Priority | Task | Notes |
|----------|------|-------|
| P1 | Refine skills based on usage | Monitor trigger accuracy |
| P2 | Add more reference files | Based on real project needs |
| P3 | Consider promoting active → stable | After battle-testing |

## Quick Commands
```bash
# View all skills
cat SKILLS_INDEX.md

# Check global skills
ls ~/.claude/skills/

# View zips
ls dist/*.zip
```

## Tech Stack
Markdown | YAML frontmatter | Progressive Disclosure Architecture
