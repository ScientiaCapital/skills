# Advanced Workflows

## Boris Cherny Workflow Integration

Based on Boris Cherny's (Claude Code creator) 13-step autonomous workflow.

### iTerm2 Notifications Setup

Enable system notifications when Claude needs input (Boris runs 5 numbered tabs):

**Step 1: iTerm2 Preferences**
1. iTerm2 → Preferences → Profiles → Terminal
2. Enable "Notification when idle"
3. Set "After 30 seconds of silence, send notification"

**Step 2: Shell Integration (Optional)**
```bash
# Add to ~/.zshrc for manual attention requests
it2attention() { printf "\e]1337;RequestAttention=fireworks\a"; }
```

**Step 3: Tab Numbering**
The launch-agent.sh script automatically numbers iTerm2 tabs as `[1] project - branch`, `[2] project - branch`, etc. when using `--terminal iterm2`.

### Web Session Handoff (Teleport)

Hand off local session to claude.ai/code for longer tasks or mobile monitoring:

```bash
# In terminal Claude session, run:
/teleport

# Or use ampersand for background handoff:
claude & teleport
```

**Workflow:**
1. Start work in terminal
2. When leaving desk, run `/teleport`
3. Continue from https://claude.ai/code
4. Or check in from Claude iOS app
5. Resume locally: `claude --resume <session-id>`

### Long-Running Autonomous Sessions (Ralph Loop)

For tasks that need extended autonomous work without intervention:

**Step 1: Create worktree**
```
spin up worktree for feature/big-refactor
```

**Step 2: Start ralph loop in worktree terminal**
```
/ralph-loop "Implement complete auth system with tests" --max-iterations 10
```

**Step 3: Set completion promise (optional)**
```
/ralph-loop "Refactor database layer" --completion-promise "All tests pass and no type errors"
```

**How Ralph Loop Works:**
- Claude works on the task
- When it tries to exit, the SAME PROMPT is fed back
- Claude sees previous work in files and git history
- Iterates until completion promise is met or max iterations reached
- Use with `--dangerously-skip-permissions` for fully autonomous operation

**Verification Integration:**
```bash
/ralph-loop "Implement feature X" --completion-promise "verify-app returns OVERALL: PASS"
```

### Terminal Strategy

| Use Case | Terminal | Why |
|----------|----------|-----|
| Quick interactive work | Ghostty | Fast, clean UI |
| Monitored parallel sessions | iTerm2 | Numbered tabs + notifications |
| Long autonomous tasks | iTerm2 + ralph-loop | Background with alerts |
| CI/CD integration | tmux | Detached sessions |

### Daily Workflow Protocol

**Morning:**
```bash
# 1. Check worktree status
cat ~/.claude/worktree-registry.json | jq '.worktrees[] | select(.status == "active")'

# 2. Review web sessions at https://claude.ai/code

# 3. Start primary session
cd ~/tk_projects/<priority-project>
claude --model opus
```

**Parallel Work:**
```bash
# Spin up 3 worktrees with iTerm2 tabs
spin up worktrees for feature/a, feature/b, feature/c --terminal iterm2

# Or use Ghostty for quick sessions
spin up worktree for fix/quick-bug --terminal ghostty
```

**End of Day:**
```bash
# Check merged PRs
gh pr list --state merged --author @me --limit 10

# Cleanup merged worktrees
cleanup merged worktrees
```
