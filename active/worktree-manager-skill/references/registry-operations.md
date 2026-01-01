# Registry Operations Reference

Manual operations for the global worktree registry at `~/.claude/worktree-registry.json`.

## Registry Schema

```json
{
  "worktrees": [
    {
      "id": "unique-uuid",
      "project": "obsidian-ai-agent",
      "repoPath": "/Users/user/Projects/obsidian-ai-agent",
      "branch": "feature/auth",
      "branchSlug": "feature-auth",
      "worktreePath": "/Users/user/tmp/worktrees/obsidian-ai-agent/feature-auth",
      "ports": [8100, 8101],
      "createdAt": "2025-12-04T10:00:00Z",
      "validatedAt": "2025-12-04T10:02:00Z",
      "agentLaunchedAt": "2025-12-04T10:03:00Z",
      "task": "Implement OAuth login",
      "prNumber": null,
      "status": "active"
    }
  ],
  "portPool": {
    "start": 8100,
    "end": 8199,
    "allocated": [8100, 8101]
  }
}
```

## Field Descriptions

### Worktree Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (UUID) |
| `project` | string | Project name (from git remote or directory) |
| `repoPath` | string | Absolute path to original repository |
| `branch` | string | Full branch name (e.g., `feature/auth`) |
| `branchSlug` | string | Filesystem-safe name (e.g., `feature-auth`) |
| `worktreePath` | string | Absolute path to worktree |
| `ports` | number[] | Allocated port numbers (usually 2) |
| `createdAt` | string | ISO 8601 timestamp |
| `validatedAt` | string\|null | When validation passed |
| `agentLaunchedAt` | string\|null | When agent was launched |
| `task` | string\|null | Task description for the agent |
| `prNumber` | number\|null | Associated PR number if exists |
| `status` | string | `active`, `orphaned`, or `merged` |

### Port Pool Fields

| Field | Type | Description |
|-------|------|-------------|
| `start` | number | First port in pool (default: 8100) |
| `end` | number | Last port in pool (default: 8199) |
| `allocated` | number[] | Currently allocated ports |

## Manual Operations

### Read Registry

```bash
# Entire registry
cat ~/.claude/worktree-registry.json | jq '.'

# List all worktrees
cat ~/.claude/worktree-registry.json | jq '.worktrees[]'

# Worktrees for specific project
cat ~/.claude/worktree-registry.json | jq '.worktrees[] | select(.project == "my-project")'

# Get allocated ports
cat ~/.claude/worktree-registry.json | jq '.portPool.allocated'

# Find worktree by branch (partial match)
cat ~/.claude/worktree-registry.json | jq '.worktrees[] | select(.branch | contains("auth"))'
```

### Add Entry

```bash
TMP=$(mktemp)
jq '.worktrees += [{
  "id": "'$(uuidgen)'",
  "project": "my-project",
  "repoPath": "/path/to/repo",
  "branch": "feature/auth",
  "branchSlug": "feature-auth",
  "worktreePath": "/Users/me/tmp/worktrees/my-project/feature-auth",
  "ports": [8100, 8101],
  "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
  "validatedAt": null,
  "agentLaunchedAt": null,
  "task": "My task",
  "prNumber": null,
  "status": "active"
}]' ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json
```

### Remove Entry

```bash
TMP=$(mktemp)
jq 'del(.worktrees[] | select(.project == "my-project" and .branch == "feature/auth"))' \
  ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json
```

### Port Operations

```bash
# Add ports to allocated pool
TMP=$(mktemp)
jq '.portPool.allocated += [8100, 8101] | .portPool.allocated |= unique | .portPool.allocated |= sort_by(.)' \
  ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json

# Release ports from pool
TMP=$(mktemp)
jq '.portPool.allocated = (.portPool.allocated | map(select(. != 8100 and . != 8101)))' \
  ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json
```

### Initialize Empty Registry

```bash
mkdir -p ~/.claude
cat > ~/.claude/worktree-registry.json << 'EOF'
{
  "worktrees": [],
  "portPool": {
    "start": 8100,
    "end": 8199,
    "allocated": []
  }
}
EOF
```
