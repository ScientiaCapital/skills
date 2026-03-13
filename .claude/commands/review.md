---
description: "Quick code review of recent changes"
argument-hint: "[number of commits to review, default 5]"
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# /review — Quick Code Review

## Instructions

1. Get the diff: `git diff HEAD~${ARGUMENTS:-5}..HEAD`
2. Launch a code-reviewer agent (haiku model) with the diff:
   - Check for bugs, logic errors, security issues
   - Check for project conventions (read `.claude/rules/coding.md` if it exists)
   - Only report HIGH confidence issues
3. Present findings as:

```
## Review: last N commits

| Severity | File:Line | Issue | Suggestion |
|----------|-----------|-------|------------|

**Verdict:** [LGTM / N issues found]
```

If no issues found, just say "LGTM — no issues in last N commits."
