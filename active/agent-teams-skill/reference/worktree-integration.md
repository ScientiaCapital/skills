# Worktree Integration Guide

> How agent-teams coordinates with worktree-manager for infrastructure.

---

## Dependency Relationship

```
agent-teams-skill (orchestration layer)
    │
    │  delegates to
    ▼
worktree-manager-skill (infrastructure layer)
    │
    │  manages
    ▼
git worktrees, ports, terminals, registry
```

**agent-teams** decides WHAT to do (task decomposition, agent assignments, merge strategy).
**worktree-manager** decides HOW to do it (create worktrees, allocate ports, launch terminals).

---

## Shared State: Registry

Both skills share `~/.claude/worktree-registry.json`:

```json
{
  "worktrees": [
    {
      "project": "my-app",
      "branch": "feature/auth-api",
      "path": "~/tmp/worktrees/my-app/feature-auth-api",
      "ports": [8100, 8101],
      "status": "active",
      "created": "2026-02-07T10:00:00Z",
      "team": "auth-system",
      "agentId": 1
    }
  ],
  "portPool": {
    "start": 8100,
    "end": 8199,
    "allocated": [8100, 8101, 8102, 8103]
  }
}
```

**agent-teams additions:** The `team` and `agentId` fields are added by agent-teams to track which worktrees belong to which team. worktree-manager ignores these fields.

---

## Port Allocation Strategy

### Per-Agent Ports

Each agent gets 2 ports from worktree-manager's global pool (8100-8199):

| Agent | Port 1 (API) | Port 2 (Frontend) |
|-------|-------------|-------------------|
| Agent 1 | 8100 | 8101 |
| Agent 2 | 8102 | 8103 |
| Agent 3 | 8104 | 8105 |

### Service Port Assignment

When agents run services (dev servers, APIs), include port info in WORKTREE_TASK.md:

```markdown
## Your Ports
- API server: localhost:8100
- Frontend dev server: localhost:8101

Do NOT use any other ports. These are exclusively yours.
```

### Avoiding Conflicts

- Always check registry before spawning: `cat ~/.claude/worktree-registry.json | jq '.portPool.allocated'`
- worktree-manager handles allocation — agent-teams just reads the result
- If ports are exhausted (all 100 used), clean up stale worktrees first

---

## Terminal Launching Patterns

### Ghostty (Default — Quick Spawn)

Best for: Quick parallel sessions where you don't need monitoring.

```bash
# worktree-manager creates worktree, then launches:
ghostty -e "cd ~/tmp/worktrees/my-app/feature-auth-api && claude --model opus --dangerously-skip-permissions"
```

**Team spawn sequence:**
```bash
# Agent 1
ghostty -e "cd ~/tmp/worktrees/my-app/feature-auth-api && claude --model opus --dangerously-skip-permissions" &

# Agent 2 (launch immediately after — don't wait)
ghostty -e "cd ~/tmp/worktrees/my-app/feature-auth-ui && claude --model opus --dangerously-skip-permissions" &
```

### iTerm2 (Numbered Tabs — Monitored Sessions)

Best for: When you want to monitor agents in numbered tabs with notifications.

```bash
# worktree-manager's launch-agent.sh handles numbered tabs:
~/.claude/skills/worktree-manager/scripts/launch-agent.sh \
  --worktree ~/tmp/worktrees/my-app/feature-auth-api \
  --terminal iterm2 \
  --tab-number 1
```

**Tab naming convention:**
```
[1] my-app/feature-auth-api
[2] my-app/feature-auth-ui
[3] my-app/feature-auth-tests
```

### iTerm2 + Notifications (Long-Running Teams)

Enable idle notifications so you know when an agent needs input:

```
iTerm2 → Preferences → Profiles → Terminal
→ Enable "Notification when idle"
→ After 30 seconds of silence
```

### tmux (CI/CD — Detached Sessions)

Best for: Background agents that don't need a visible terminal.

```bash
tmux new-session -d -s agent1 "cd ~/tmp/worktrees/my-app/feature-auth-api && claude --model opus --dangerously-skip-permissions"
tmux new-session -d -s agent2 "cd ~/tmp/worktrees/my-app/feature-auth-ui && claude --model opus --dangerously-skip-permissions"
```

---

## Cleanup Coordination

### Agent Done → Worktree Cleanup

When an agent reports DONE:

```
1. Team lead checks agent's work (git log, test results)
2. Team lead merges branch to main
3. Team lead requests worktree cleanup:
   → "cleanup worktree feature/auth-api"
4. worktree-manager:
   a. Removes worktree (git worktree remove)
   b. Deallocates ports
   c. Updates registry
   d. Optionally deletes branch
```

### Team Cleanup (All Agents)

After a team session completes:

```bash
# Check all team worktrees
cat ~/.claude/worktree-registry.json | jq '.worktrees[] | select(.team == "auth-system")'

# Cleanup all (via worktree-manager)
for branch in feature/auth-api feature/auth-ui feature/auth-tests; do
  ~/.claude/skills/worktree-manager/scripts/cleanup.sh my-app $branch --delete-branch
done
```

### Stale Team Detection

If a team was abandoned (user forgot to cleanup):

```bash
# Find worktrees older than 7 days with team tags
cat ~/.claude/worktree-registry.json | jq '
  .worktrees[]
  | select(.team != null)
  | select((.created | fromdateiso8601) < (now - 604800))
  | "\(.team): \(.branch) (created \(.created))"
'
```

---

## Error Recovery

### Worktree Creation Fails

If worktree-manager fails to create a worktree:
1. Check if branch already exists: `git branch -a | grep feature/auth`
2. Check if worktree path exists: `ls ~/tmp/worktrees/my-app/`
3. Clean up stale entries: `git worktree prune`
4. Retry creation

### Port Conflict

If a port is in use by a non-agent process:
1. worktree-manager skips to next available port
2. agent-teams reads the actual allocated port from registry
3. Updates WORKTREE_TASK.md with correct port

### Terminal Fails to Launch

If Ghostty/iTerm2 isn't available:
1. worktree-manager falls back to default terminal
2. Or use tmux as universal fallback
3. Manual launch: `cd <worktree-path> && claude --model opus --dangerously-skip-permissions`
