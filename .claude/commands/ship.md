---
description: "Stage, commit, push. One command."
argument-hint: "[optional commit message]"
allowed-tools: Bash, Read, Glob
---

# /ship — Quick Ship

## Instructions

1. Show `git status --short` and `git diff --stat`
2. If `$ARGUMENTS` is provided, use it as the commit message
3. If no arguments, auto-generate a conventional commit message from the diff
4. Stage relevant files (NOT node_modules, .env, or other ignored files)
5. Commit with:
   ```
   $TYPE: $MESSAGE

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   ```
6. Push to current branch: `git push origin $(git branch --show-current)`
7. Show the commit hash and pushed branch

If there's nothing to commit, say so and stop.
