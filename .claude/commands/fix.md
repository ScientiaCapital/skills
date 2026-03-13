---
description: "Quick fix — branch, fix, test, commit. No ceremony."
argument-hint: "<description of what to fix>"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent
---

# /fix — Quick Fix

You are fixing: **$ARGUMENTS**

## Instructions

1. Create a branch: `git checkout -b fix/$ARGUMENTS_SLUG` (slugify the description)
2. Find and fix the issue — use the minimum changes needed
3. Run tests if they exist:
   - `npm test 2>/dev/null || pytest 2>/dev/null || cargo test 2>/dev/null || echo "No tests"`
4. Commit with conventional format:
   ```
   fix: $ARGUMENTS
   ```
5. Report what changed and whether tests passed

No observers. No contracts. No security sweep. Just fix it.
If the fix touches >5 files, suggest upgrading to `/build` instead.
