---
description: "Simplify recent code — reduce complexity, improve readability."
argument-hint: "[number of commits to simplify, default 3]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Agent
---

# /simplify — Code Simplification Pass

## Instructions

1. Get the changed files: `git diff --name-only HEAD~${ARGUMENTS:-3}..HEAD`
2. Read each changed file fully
3. Launch a code-simplifier agent (sonnet model) with these files. The agent should:
   - Read `.claude/rules/coding.md` for project conventions
   - Simplify overly complex logic (nested ternaries, deep callbacks, unnecessary abstractions)
   - Remove dead code, unused imports, redundant comments
   - Flatten unnecessary wrappers or indirection
   - Replace verbose patterns with idiomatic equivalents
   - Preserve ALL functionality — no behavior changes
   - Keep changes minimal and focused
4. Present results as:

```
## Simplified: N files from last M commits

| File | What changed | Why simpler |
|------|-------------|-------------|

**Total: N simplifications across M files**
```

If code is already clean, say "Already clean — nothing to simplify."
