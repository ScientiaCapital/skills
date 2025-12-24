# Skills Library

**Branch**: main | **Updated**: 2025-12-24

## Status
Production-ready skills library with **25 skills** (2 stable, 23 active). Worktree-manager enhanced with .env file copying and model selection.

## Current State

### Stable Skills (2)
- workflow-enforcer
- project-context-skill

### Active Skills (23)
| Category | Skills |
|----------|--------|
| Trading/Finance | trading-signals-skill |
| Sales/GTM | sales-outreach-skill, gtm-strategy-skill, demo-discovery-skill, revenue-ops-skill, pricing-strategy-skill |
| AI/Agents | langgraph-agents-skill, voice-ai-skill |
| Infrastructure | runpod-deployment-skill, supabase-sql-skill, worktree-manager-skill |
| Research | market-research-skill, technical-research-skill, opportunity-evaluator-skill |
| Content | content-marketing-skill |
| Data | data-analysis-skill |
| Meta/Claude | create-plans-skill, debug-like-expert-skill, create-subagents-skill, create-agent-skills-skill, create-hooks-skill, create-slash-commands-skill, create-meta-prompts-skill |

### Deployment
- All 25 skills in `~/.claude/skills/` (global access)
- All 25 zips in `dist/` (Claude Desktop)
- All committed to GitHub

## Recent Changes (2025-12-24)
- Enhanced worktree-manager with .env/.env.local copying
- Added model selection (opus/sonnet/haiku) for worktree agents
- Created ARCHIVE.md for completed work
- Cleaned up PLANNING.md and BACKLOG.md

## Blockers
None

## Next Tasks
| Priority | Task | Notes |
|----------|------|-------|
| P1 | Test each skill activation with trigger phrases | Monitor trigger accuracy |
| P2 | Add reference/ folders for complex skills | Based on real project needs |
| P3 | Document worktree workflow in README | User-facing docs |

## Quick Commands
```bash
# View all skills
cat SKILLS_INDEX.md

# Check global skills
ls ~/.claude/skills/

# View zips
ls dist/*.zip

# Worktree commands
wt-audit       # Check worktree status
wt-memory      # Check available memory
wt-cleanup     # Clean merged worktrees
```

## Tech Stack
Markdown | YAML frontmatter | Progressive Disclosure Architecture
