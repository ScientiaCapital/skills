---
description: "Clean PR workflow — branch, build, simplify, review, submit."
argument-hint: "<feature or fix description>"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent
---

# /pr — Clean Pull Request Workflow

You are preparing a PR for: **$ARGUMENTS**

## Instructions

### Step 1: Sync with upstream
```bash
git fetch origin
git checkout main
git pull origin main
```

### Step 2: Create a clean branch
Slugify the description into a branch name:
```bash
git checkout -b feat/$ARGUMENTS_SLUG   # or fix/$ARGUMENTS_SLUG
```

### Step 3: Build the feature/fix
Implement what was requested. Follow these rules strictly:
- Read `.claude/rules/coding.md` and follow every convention
- Make the MINIMUM changes needed — no drive-by refactors
- No unrelated formatting changes, no renaming things "while you're in there"
- Each file you touch should be directly related to the PR description
- Run tests: `cargo test 2>/dev/null || npm test 2>/dev/null || pytest 2>/dev/null`

### Step 4: Self-review before simplifying
Check your own work:
- `git diff` — read every line you changed
- Are there files that shouldn't be in this PR? Revert them.
- Are there debug prints, TODO comments, or commented-out code? Remove them.

### Step 5: Simplify
Launch a code-simplifier agent (sonnet) on the changed files:
- Remove unnecessary complexity, verbose error handling, over-abstraction
- Keep all functionality intact
- Make sure the code matches the project's existing style, not "AI style"

### Step 6: Final review
Launch a code-reviewer agent (haiku) on the diff:
- Check for bugs, logic errors, security issues
- Check conventions match `.claude/rules/coding.md`
- Only flag HIGH confidence issues

### Step 7: Commit and push
```bash
git add -A
git commit -m "feat: $ARGUMENTS"
git push origin HEAD
```

### Step 8: Create PR
Use `gh pr create` with:
- Short title (under 70 chars)
- Body with: what changed, why, how to test
- Tag the PR for review

```bash
gh pr create --title "feat: $ARGUMENTS" --body "$(cat <<'EOF'
## What
[1-2 sentences: what this PR does]

## Why
[1 sentence: why this change is needed]

## Changes
- [bullet list of files/components changed]

## How to test
- [ ] [step-by-step testing checklist]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### Step 9: Report
Show the PR URL and a summary of what was changed.

## Rules for contributing to someone else's repo
- **No scaffolding changes** — don't add/modify CLAUDE.md, init.sh, .claude/ files
- **No dependency upgrades** unless directly related to the feature
- **No style/formatting changes** outside your feature's scope
- **Match their commit style** — check `git log --oneline -10` first
- **Small PRs** — if the change is big, discuss splitting into multiple PRs
