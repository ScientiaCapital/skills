# Skill Activation Test Matrix

**Date:** 2026-02-05
**Total Skills:** 26 (2 stable, 24 active)

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
| 1 | workflow-enforcer | "follow workflow" | ✅ | | Stable |
| 2 | project-context | "load project context" | ✅ | | Stable |
| 3 | workflow-orchestrator | "start day" | ✅ | | Active |

---

## Dev Tools (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 4 | extension-authoring | "create skill" | ✅ | | |
| 5 | debug-like-expert | "debug systematically" | ✅ | | |
| 6 | planning-prompts | "create plan" | ✅ | | |
| 7 | worktree-manager | "create worktree" | ✅ | | |
| 8 | testing | "write tests" | ✅ | | |
| 9 | api-design | "design API" | ✅ | | |
| 10 | security | "security audit" | ✅ | | |

---

## Infrastructure (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 11 | unsloth-training | "train with GRPO" | ✅ | | |
| 12 | langgraph-agents | "LangGraph agent" | ✅ | | |
| 13 | runpod-deployment | "deploy to RunPod" | ✅ | | |
| 14 | groq-inference | "groq" | ✅ | | |
| 15 | voice-ai | "voice agent" | ✅ | | |
| 16 | supabase-sql | "fix SQL" | ✅ | | |
| 17 | stripe-stack | "stripe" | ✅ | | |

---

## Business (7)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 18 | crm-integration | "Close CRM" | ✅ | | |
| 19 | gtm-pricing | "GTM strategy" | ✅ | | |
| 20 | research | "research company" | ✅ | | |
| 21 | sales-revenue | "cold email" | ✅ | | |
| 22 | content-marketing | "content strategy" | ✅ | | |
| 23 | data-analysis | "analyze data" | ✅ | | |
| 24 | trading-signals | "fibonacci levels" | ✅ | | |

---

## Strategy (2)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 25 | business-model-canvas | "business model canvas" | ✅ | | |
| 26 | blue-ocean-strategy | "blue ocean" | ✅ | | |

---

## Summary

| Category | Count | YAML Pass | Activation Pass |
|----------|-------|-----------|-----------------|
| Core | 3 | 3/3 | /3 |
| Dev Tools | 7 | 7/7 | /7 |
| Infrastructure | 7 | 7/7 | /7 |
| Business | 7 | 7/7 | /7 |
| Strategy | 2 | 2/2 | /2 |
| **Total** | **26** | **26/26** | **/26** |

---

## YAML Fixes Applied This Session

| Skill | Issue | Fix |
|-------|-------|-----|
| project-context (stable) | Multiline `\|` description | Converted to single-line quoted |
| workflow-enforcer (stable) | Unquoted name + multiline description | Added quotes, single-line |

---

## Test Commands

```bash
# Verify skill count
ls -d active/*-skill stable/*-skill stable/workflow-enforcer 2>/dev/null | wc -l
# Expected: 26

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*-skill stable/*-skill stable/workflow-enforcer; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
