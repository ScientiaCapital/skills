# Skill Activation Test Matrix

**Date:** 2026-02-07
**Total Skills:** 31 (2 stable, 29 active)
**Status:** ✅ All 31/31 activation tests passing

## Test Protocol

For each skill:
1. Use the trigger phrase in Claude Code
2. Verify skill activates (shows in skill panel)
3. Check YAML frontmatter parses correctly
4. Mark pass/fail

---

## Core Skills (3)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 1 | workflow-enforcer | "follow workflow" | ✅ | ✅ | Stable |
| 2 | project-context | "load project context" | ✅ | ✅ | Stable |
| 3 | workflow-orchestrator | "start day" | ✅ | ✅ | Active |

---

## Dev Tools (11)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 4 | extension-authoring | "create skill" | ✅ | ✅ | |
| 5 | debug-like-expert | "debug systematically" | ✅ | ✅ | |
| 6 | planning-prompts | "create plan" | ✅ | ✅ | |
| 7 | worktree-manager | "create worktree" | ✅ | ✅ | |
| 8 | git-workflow | "commit" / "conventional commits" | ✅ | ✅ | Deployed |
| 9 | testing | "write tests" | ✅ | ✅ | |
| 10 | api-design | "design API" | ✅ | ✅ | |
| 11 | security | "security audit" | ✅ | ✅ | |
| 12 | api-testing | "postman" / "bruno" / "API testing" | ✅ | ✅ | |
| 13 | docker-compose | "docker compose" / "local dev env" | ✅ | ✅ | NEW |
| 14 | agent-teams | "set up agent team" / "parallel development" | ✅ | ✅ | NEW |

---

## Infrastructure (8)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 15 | unsloth-training | "train with GRPO" | ✅ | ✅ | |
| 16 | langgraph-agents | "LangGraph agent" | ✅ | ✅ | |
| 17 | runpod-deployment | "deploy to RunPod" | ✅ | ✅ | |
| 18 | groq-inference | "groq" | ✅ | ✅ | |
| 19 | openrouter | "OpenRouter" / "DeepSeek" / "Chinese LLM" | ✅ | ✅ | NEW |
| 20 | voice-ai | "voice agent" | ✅ | ✅ | |
| 21 | supabase-sql | "fix SQL" | ✅ | ✅ | |
| 22 | stripe-stack | "stripe" | ✅ | ✅ | |

---

## Business (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 23 | crm-integration | "Close CRM" | ✅ | ✅ | |
| 24 | gtm-pricing | "GTM strategy" | ✅ | ✅ | |
| 25 | research | "research company" | ✅ | ✅ | |
| 26 | sales-revenue | "cold email" | ✅ | ✅ | |
| 27 | content-marketing | "content strategy" | ✅ | ✅ | |
| 28 | data-analysis | "analyze data" | ✅ | ✅ | |
| 29 | trading-signals | "fibonacci levels" | ✅ | ✅ | |

---

## Strategy (2)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 30 | business-model-canvas | "business model canvas" | ✅ | ✅ | |
| 31 | blue-ocean-strategy | "blue ocean" | ✅ | ✅ | |

---

## Summary

| Category | Count | YAML Pass | Activation Pass |
|----------|-------|-----------|-----------------|
| Core | 3 | 3/3 | 3/3 |
| Dev Tools | 11 | 11/11 | 11/11 |
| Infrastructure | 8 | 8/8 | 8/8 |
| Business | 7 | 7/7 | 7/7 |
| Strategy | 2 | 2/2 | 2/2 |
| **Total** | **31** | **31/31** | **31/31** |

---

## Changes This Session (2026-02-07)

| Skill | Action | Notes |
|-------|--------|-------|
| openrouter (NEW) | Created | Chinese LLMs via OpenRouter, LangChain integration |
| docker-compose (NEW) | Created | Local dev environments, multi-service setups |
| agent-teams (NEW) | Created | Parallel Claude Code session orchestration |
| worktree-manager | Polished | .claude/ dir propagation, hooks, permissions |
| agent-teams | Polished | CLAUDE.md inheritance, @claude bot, plan mode |

---

## Test Commands

```bash
# Verify skill count
ls -d active/*-skill stable/*-skill stable/workflow-enforcer 2>/dev/null | wc -l
# Expected: 31

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*-skill stable/*-skill stable/workflow-enforcer; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
