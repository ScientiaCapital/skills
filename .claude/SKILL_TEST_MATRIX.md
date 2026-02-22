# Skill Activation Test Matrix

**Date:** 2026-02-22
**Total Skills:** 39 (2 stable, 37 active)
**Status:** ✅ All 39/39 activation tests passing

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
| 1 | workflow-enforcer-skill | "follow workflow" | ✅ | ✅ | Stable |
| 2 | project-context | "load project context" | ✅ | ✅ | Stable |
| 3 | workflow-orchestrator | "start day" | ✅ | ✅ | Active |
| 4 | cost-metering | "cost check" / "budget status" | ✅ | ✅ | NEW |
| 5 | portfolio-artifact | "capture metrics" / "portfolio report" | ✅ | ✅ | NEW |

---

## Dev Tools (15)

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
| 19 | heal-skill | "/heal-skill" / "fix broken skill" | ✅ | ✅ | NEW |
| 20 | frontend-ui | "React component" / "Tailwind" / "shadcn" | ✅ | ✅ | NEW |

---

## Infrastructure (8)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 21 | unsloth-training | "train with GRPO" | ✅ | ✅ | |
| 22 | langgraph-agents | "LangGraph agent" | ✅ | ✅ | |
| 23 | runpod-deployment | "deploy to RunPod" | ✅ | ✅ | |
| 24 | groq-inference | "groq" | ✅ | ✅ | |
| 25 | openrouter | "OpenRouter" / "DeepSeek" / "Chinese LLM" | ✅ | ✅ | |
| 26 | voice-ai | "voice agent" | ✅ | ✅ | |
| 27 | supabase-sql | "fix SQL" | ✅ | ✅ | |
| 28 | stripe-stack | "stripe" | ✅ | ✅ | |

---

## Business (9)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 29 | crm-integration | "Close CRM" | ✅ | ✅ | |
| 30 | gtm-pricing | "GTM strategy" | ✅ | ✅ | |
| 31 | research | "research company" | ✅ | ✅ | |
| 32 | sales-revenue | "cold email" | ✅ | ✅ | |
| 33 | content-marketing | "content strategy" | ✅ | ✅ | |
| 34 | data-analysis | "analyze data" | ✅ | ✅ | |
| 35 | trading-signals | "fibonacci levels" | ✅ | ✅ | |
| 36 | miro | "miro board" / "strategy canvas" | ✅ | ✅ | |
| 37 | hubspot-revops | "hubspot analytics" / "lead scoring" | ✅ | ✅ | NEW |

---

## Strategy (2)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 38 | business-model-canvas | "business model canvas" | ✅ | ✅ | |
| 39 | blue-ocean-strategy | "blue ocean" | ✅ | ✅ | |

---

## Summary

| Category | Count | YAML Pass | Activation Pass |
|----------|-------|-----------|-----------------|
| Core | 5 | 5/5 | 5/5 |
| Dev Tools | 15 | 15/15 | 15/15 |
| Infrastructure | 8 | 8/8 | 8/8 |
| Business | 9 | 9/9 | 9/9 |
| Strategy | 2 | 2/2 | 2/2 |
| **Total** | **39** | **39/39** | **39/39** |

---

## Changes This Session (2026-02-22)

| Skill | Action | Notes |
|-------|--------|-------|
| heal-skill (NEW) | Added to matrix | Auto-diagnose and repair broken skills |
| frontend-ui (NEW) | Created | Enterprise SaaS frontend: Tailwind v4, shadcn/ui, Next.js |

---

## Automated Testing

```bash
# Run all 8 integration tests across all skills
./scripts/test-skills.sh

# Verbose output (shows individual test results)
./scripts/test-skills.sh --verbose

# Test a single skill
./scripts/test-skills.sh --skill frontend-ui-skill
```

Tests: T1 (files exist), T2 (YAML frontmatter), T3 (config.json schema), T4 (XML sections), T5 (line count), T6 (circular deps), T7 (integrates_with refs), T8 (activation_triggers).

## Manual Test Commands

```bash
# Verify skill count
ls -d active/*-skill stable/*-skill 2>/dev/null | wc -l
# Expected: 39

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*-skill stable/*-skill; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
