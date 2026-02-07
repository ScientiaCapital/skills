# Skill Activation Test Matrix

**Date:** 2026-02-07
**Total Skills:** 37 (2 stable, 35 active)
**Status:** ✅ All 37/37 activation tests passing

## Test Protocol

For each skill:
1. Use the trigger phrase in Claude Code
2. Verify skill activates (shows in skill panel)
3. Check YAML frontmatter parses correctly
4. Mark pass/fail

---

## Core Skills (5)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 1 | workflow-enforcer | "follow workflow" | ✅ | ✅ | Stable |
| 2 | project-context | "load project context" | ✅ | ✅ | Stable |
| 3 | workflow-orchestrator | "start day" | ✅ | ✅ | Active |
| 4 | cost-metering | "cost check" / "budget status" | ✅ | ✅ | NEW |
| 5 | portfolio-artifact | "capture metrics" / "portfolio report" | ✅ | ✅ | NEW |

---

## Dev Tools (13)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 6 | extension-authoring | "create skill" | ✅ | ✅ | |
| 7 | debug-like-expert | "debug systematically" | ✅ | ✅ | |
| 8 | planning-prompts | "create plan" | ✅ | ✅ | |
| 9 | worktree-manager | "create worktree" | ✅ | ✅ | |
| 10 | git-workflow | "commit" / "conventional commits" | ✅ | ✅ | Deployed |
| 11 | testing | "write tests" | ✅ | ✅ | |
| 12 | api-design | "design API" | ✅ | ✅ | |
| 13 | security | "security audit" | ✅ | ✅ | |
| 14 | api-testing | "postman" / "bruno" / "API testing" | ✅ | ✅ | |
| 15 | docker-compose | "docker compose" / "local dev env" | ✅ | ✅ | |
| 16 | agent-teams | "set up agent team" / "parallel development" | ✅ | ✅ | |
| 17 | subagent-teams | "subagent team" / "Task tool team" | ✅ | ✅ | NEW |
| 18 | agent-capability-matrix | "which agent" / "route task" | ✅ | ✅ | NEW |

---

## Infrastructure (8)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 19 | unsloth-training | "train with GRPO" | ✅ | ✅ | |
| 20 | langgraph-agents | "LangGraph agent" | ✅ | ✅ | |
| 21 | runpod-deployment | "deploy to RunPod" | ✅ | ✅ | |
| 22 | groq-inference | "groq" | ✅ | ✅ | |
| 23 | openrouter | "OpenRouter" / "DeepSeek" / "Chinese LLM" | ✅ | ✅ | |
| 24 | voice-ai | "voice agent" | ✅ | ✅ | |
| 25 | supabase-sql | "fix SQL" | ✅ | ✅ | |
| 26 | stripe-stack | "stripe" | ✅ | ✅ | |

---

## Business (9)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 27 | crm-integration | "Close CRM" | ✅ | ✅ | |
| 28 | gtm-pricing | "GTM strategy" | ✅ | ✅ | |
| 29 | research | "research company" | ✅ | ✅ | |
| 30 | sales-revenue | "cold email" | ✅ | ✅ | |
| 31 | content-marketing | "content strategy" | ✅ | ✅ | |
| 32 | data-analysis | "analyze data" | ✅ | ✅ | |
| 33 | trading-signals | "fibonacci levels" | ✅ | ✅ | |
| 34 | miro | "miro board" / "strategy canvas" | ✅ | ✅ | |
| 35 | hubspot-revops | "hubspot analytics" / "lead scoring" | ✅ | ✅ | NEW |

---

## Strategy (2)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 36 | business-model-canvas | "business model canvas" | ✅ | ✅ | |
| 37 | blue-ocean-strategy | "blue ocean" | ✅ | ✅ | |

---

## Summary

| Category | Count | YAML Pass | Activation Pass |
|----------|-------|-----------|-----------------|
| Core | 5 | 5/5 | 5/5 |
| Dev Tools | 13 | 13/13 | 13/13 |
| Infrastructure | 8 | 8/8 | 8/8 |
| Business | 9 | 9/9 | 9/9 |
| Strategy | 2 | 2/2 | 2/2 |
| **Total** | **37** | **37/37** | **37/37** |

---

## Changes This Session (2026-02-07)

| Skill | Action | Notes |
|-------|--------|-------|
| subagent-teams (NEW) | Created | In-session Task tool subagent orchestration |
| agent-capability-matrix (NEW) | Created | Task→agent mapping, 70+ agents cataloged |
| cost-metering (NEW) | Created | API cost tracking, budget alerts, optimization |
| portfolio-artifact (NEW) | Created | Engineering metrics capture, report templates |
| miro (NEW) | Created | Miro board interaction via MCP |
| hubspot-revops (NEW) | Created | HubSpot SQL analytics, lead scoring, pipeline forecasting |
| workflow-orchestrator | Polished | Cost gate, progress rendering, agent selection |

---

## Test Commands

```bash
# Verify skill count
ls -d active/*-skill stable/*-skill stable/workflow-enforcer 2>/dev/null | wc -l
# Expected: 37

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*-skill stable/*-skill stable/workflow-enforcer; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
