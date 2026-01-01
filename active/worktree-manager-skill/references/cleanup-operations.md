# Cleanup Operations Reference

## Full Worktree Cleanup

### Using Script

```bash
~/.claude/skills/worktree-manager/scripts/cleanup.sh my-project feature/auth --delete-branch
```

### Manual Cleanup Steps

```bash
# 1. Get worktree info from registry
ENTRY=$(cat ~/.claude/worktree-registry.json | jq '.worktrees[] | select(.project == "my-project" and .branch == "feature/auth")')
WORKTREE_PATH=$(echo "$ENTRY" | jq -r '.worktreePath')
PORTS=$(echo "$ENTRY" | jq -r '.ports[]')
REPO_PATH=$(echo "$ENTRY" | jq -r '.repoPath')

# 2. Kill processes on ports
for PORT in $PORTS; do
  lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true
done

# 3. Remove worktree
cd "$REPO_PATH"
git worktree remove "$WORKTREE_PATH" --force 2>/dev/null || rm -rf "$WORKTREE_PATH"
git worktree prune

# 4. Remove from registry
TMP=$(mktemp)
jq 'del(.worktrees[] | select(.project == "my-project" and .branch == "feature/auth"))' \
  ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json

# 5. Release ports
TMP=$(mktemp)
for PORT in $PORTS; do
  jq ".portPool.allocated = (.portPool.allocated | map(select(. != $PORT)))" \
    ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json
done

# 6. Optionally delete branch
git branch -D feature/auth
git push origin --delete feature/auth
```

## Auto-Cleanup on Merge

When a PR is merged, clean up its associated worktree:

**Trigger:** User says "cleanup merged worktrees" or "my PR was merged, clean it up"

### Check for Merged PRs

```bash
# List PRs that have been merged
gh pr list --state merged --author @me --limit 10

# Check if specific branch's PR was merged
gh pr view <branch> --json state --jq '.state'
```

## Safety Guidelines

**Before cleanup**, check PR status:

| PR State | Action |
|----------|--------|
| PR merged | Safe to clean everything |
| PR open | Warn user, confirm before proceeding |
| No PR | Warn about unsubmitted work |

**Before deleting branches**, confirm if:
- PR not merged
- No PR exists
- Worktree has uncommitted changes

## Orphaned Worktree Detection

If original repo is deleted, the worktree becomes orphaned:

```bash
# Find orphaned worktrees
cat ~/.claude/worktree-registry.json | jq -r '.worktrees[] | select(.status == "orphaned") | .worktreePath'

# Or check if repoPath still exists
cat ~/.claude/worktree-registry.json | jq -r '.worktrees[] | .repoPath' | while read path; do
  [ ! -d "$path" ] && echo "Orphaned: $path"
done
```

## Resource Limits

- **Max worktrees**: With 100-port pool and 2 ports each, max ~50 concurrent
- **Disk space**: Each worktree is a full copy of repo (minus git history)
- **Memory**: Each Claude agent uses significant memory
