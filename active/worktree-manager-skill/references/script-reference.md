# Script Reference

Scripts are located at `~/.claude/skills/worktree-manager/scripts/`

**IMPORTANT**: You (Claude) can perform ALL operations manually using standard tools (jq, git, bash). Scripts are helpers, not requirements. If a script fails, fall back to manual operations.

## allocate-ports.sh

Allocates ports from the global pool.

```bash
~/.claude/skills/worktree-manager/scripts/allocate-ports.sh <count>
# Returns: space-separated port numbers (e.g., "8100 8101")
# Automatically updates registry
```

**Example:**
```bash
PORTS=$(~/.claude/skills/worktree-manager/scripts/allocate-ports.sh 2)
echo $PORTS  # "8100 8101"
```

## register.sh

Registers a worktree in the global registry.

```bash
~/.claude/skills/worktree-manager/scripts/register.sh \
  <project> <branch> <branch-slug> <worktree-path> <repo-path> <ports> [task]
```

**Example:**
```bash
~/.claude/skills/worktree-manager/scripts/register.sh \
  "my-project" "feature/auth" "feature-auth" \
  "$HOME/tmp/worktrees/my-project/feature-auth" \
  "/path/to/repo" "8100,8101" "Implement OAuth"
```

## launch-agent.sh

Opens a new terminal window with Claude Code agent.

```bash
~/.claude/skills/worktree-manager/scripts/launch-agent.sh <worktree-path> [task]
```

**Example:**
```bash
~/.claude/skills/worktree-manager/scripts/launch-agent.sh \
  ~/tmp/worktrees/my-project/feature-auth "Implement OAuth login"
```

**Default behavior:**
- Opens Ghostty terminal (configurable in config.json)
- Runs `claude --model claude-opus-4-5-20250514 --dangerously-skip-permissions`
- Changes to worktree directory first

## status.sh

Shows status of all registered worktrees.

```bash
~/.claude/skills/worktree-manager/scripts/status.sh [--project <name>]
```

**Examples:**
```bash
# All worktrees
~/.claude/skills/worktree-manager/scripts/status.sh

# Filter by project
~/.claude/skills/worktree-manager/scripts/status.sh --project my-project
```

## cleanup.sh

Removes a worktree and releases its resources.

```bash
~/.claude/skills/worktree-manager/scripts/cleanup.sh <project> <branch> [--delete-branch]
```

**What it does:**
1. Kills processes on allocated ports
2. Removes worktree directory
3. Updates registry (removes entry)
4. Releases ports back to pool
5. Optionally deletes local and remote git branches

**Example:**
```bash
~/.claude/skills/worktree-manager/scripts/cleanup.sh my-project feature/auth --delete-branch
```

## release-ports.sh

Releases ports back to the pool (without full cleanup).

```bash
~/.claude/skills/worktree-manager/scripts/release-ports.sh <port1> [port2] ...
```

**Example:**
```bash
~/.claude/skills/worktree-manager/scripts/release-ports.sh 8100 8101
```

## Script vs Manual Operations

| Task | Script | Manual Fallback |
|------|--------|-----------------|
| Allocate ports | `allocate-ports.sh 2` | See port-allocation.md |
| Register worktree | `register.sh ...` | See registry-operations.md |
| Launch agent | `launch-agent.sh` | See agent-launching.md |
| Show status | `status.sh` | `jq '.worktrees[]' ~/.claude/worktree-registry.json` |
| Cleanup | `cleanup.sh` | See cleanup-operations.md |
