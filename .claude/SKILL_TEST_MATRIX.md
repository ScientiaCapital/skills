# Skill Activation Test Matrix

**Date:** 2026-02-05
**Total Skills:** 28 (2 stable, 26 active)
**Status:** ✅ All 28/28 activation tests passing

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

## Dev Tools (9)

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
| 12 | api-testing | "postman" / "bruno" / "API testing" | ✅ | ✅ | NEW |

---

## Infrastructure (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 13 | unsloth-training | "train with GRPO" | ✅ | ✅ | |
| 14 | langgraph-agents | "LangGraph agent" | ✅ | ✅ | |
| 15 | runpod-deployment | "deploy to RunPod" | ✅ | ✅ | |
| 16 | groq-inference | "groq" | ✅ | ✅ | |
| 17 | voice-ai | "voice agent" | ✅ | ✅ | |
| 18 | supabase-sql | "fix SQL" | ✅ | ✅ | |
| 19 | stripe-stack | "stripe" | ✅ | ✅ | |

---

## Business (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 20 | crm-integration | "Close CRM" | ✅ | ✅ | |
| 21 | gtm-pricing | "GTM strategy" | ✅ | ✅ | |
| 22 | research | "research company" | ✅ | ✅ | |
| 23 | sales-revenue | "cold email" | ✅ | ✅ | |
| 24 | content-marketing | "content strategy" | ✅ | ✅ | |
| 25 | data-analysis | "analyze data" | ✅ | ✅ | |
| 26 | trading-signals | "fibonacci levels" | ✅ | ✅ | |

---

## Strategy (2)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 27 | business-model-canvas | "business model canvas" | ✅ | ✅ | |
| 28 | blue-ocean-strategy | "blue ocean" | ✅ | ✅ | |

---

## Summary

| Category | Count | YAML Pass | Activation Pass |
|----------|-------|-----------|-----------------|
| Core | 3 | 3/3 | 3/3 |
| Dev Tools | 9 | 9/9 | 9/9 |
| Infrastructure | 7 | 7/7 | 7/7 |
| Business | 7 | 7/7 | 7/7 |
| Strategy | 2 | 2/2 | 2/2 |
| **Total** | **28** | **28/28** | **28/28** |

---

## Changes This Session

| Skill | Action | Notes |
|-------|--------|-------|
| project-context (stable) | YAML fix | Multiline `\|` → single-line quoted |
| workflow-enforcer (stable) | YAML fix | Added quotes, single-line description |
| git-workflow (NEW) | Created | Conventional commits, PR templates, branch naming |
| api-testing (NEW) | Created | Postman/Bruno patterns, test design, CI integration |

---

## Test Commands

```bash
# Verify skill count
ls -d active/*-skill stable/*-skill stable/workflow-enforcer 2>/dev/null | wc -l
# Expected: 28

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*-skill stable/*-skill stable/workflow-enforcer; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
