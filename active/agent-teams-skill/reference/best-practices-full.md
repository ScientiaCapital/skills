# Best Practices

## Context Engineering for Teams

**Each agent gets minimal, focused context.** This is the #1 factor in agent team success.

1. **Isolate context per agent** — An agent building the API doesn't need to know about React component patterns. Put only relevant information in WORKTREE_TASK.md.

2. **Use external state, not agent memory** — Agents forget everything between sessions. Track progress in files:
   - `.agent-status` — simple status flag
   - Git commits — work product audit trail
   - `WORKTREE_TASK.md` — the "briefing document"

3. **Front-load instructions** — Put the most important information (task, contract, boundaries) at the TOP of WORKTREE_TASK.md. Agents read top-down and may deprioritize content at the bottom.

4. **Keep agent tasks to <50 words** — If you can't describe an agent's task concisely, it's too complex. Break it down further.

## Project Config Inheritance

Each agent inherits the project's `.claude/` directory, which ensures consistency:

**CLAUDE.md inheritance** — Agents auto-load the project's CLAUDE.md on startup, giving them:
- Dev commands (`npm test`, `bun run build`, etc.)
- Code style conventions
- Tech stack context
- File structure documentation

**PostToolUse hooks** — If the project uses auto-formatting hooks (e.g., `bun run format || true` after Write/Edit), every agent runs them too. This prevents style conflicts at merge time.

**Permissions model** — Two approaches for agent safety:
```bash
# Option A: Skip all permissions (faster, less safe)
claude --model opus --dangerously-skip-permissions

# Option B: Explicit allowlist (safer, from .claude/settings.json)
claude --model opus --allowedTools "Bash(npm test),Bash(npm run build),Edit,Write,Read"
```

**Custom subagents** — If the project has `.claude/agents/` (e.g., `verify-app.md`, `build-validator.md`), agents can dispatch them for verification steps:
```markdown
## Verification
1. Run tests: `npm test`
2. Run build validator: dispatch `.claude/agents/build-validator.md`
3. Run verify-app: dispatch `.claude/agents/verify-app.md`
```

## Session Harness Patterns

Adapted from Anthropic's session harness methodology:

1. **Startup protocol** — Each agent should:
   - Read WORKTREE_TASK.md first
   - Check for existing work (`git log`, file listing)
   - Confirm understanding before starting

2. **Verification loops** — Build self-checks into agent tasks:
   ```
   After each major change:
   1. Run tests: npm test
   2. Check types: npx tsc --noEmit
   3. If failing, fix before moving on
   ```

3. **Completion protocol** — Each agent must:
   - Run final verification
   - Commit with descriptive message
   - Push branch
   - Update `.agent-status` to "DONE"

## Contract-First Development

When agents need to integrate, define the contract BEFORE spawning:

```typescript
// CONTRACT: Auth API Shape (shared between agents)
interface AuthResponse {
  token: string;
  user: { id: string; email: string; role: string };
}

// POST /api/auth/login
// Body: { email: string; password: string }
// Response: AuthResponse
```

Write this contract to a `CONTRACT.md` or shared type file that both agents can reference.

## Merge Strategy

1. **Merge order matters** — Merge the "foundation" branch first (usually API/backend), then the "consumer" branch (usually UI/frontend)
2. **Test after each merge** — Don't batch merges. Test incrementally.
3. **Use `--no-ff`** — Preserves branch history for debugging

## Native Agent Teams Hooks

Two hook events are specific to agent teams: `TeammateIdle` and `TaskCompleted`.

### TeammateIdle

Fires when a teammate is about to go idle (between turns).

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "type": "command",
        "command": "./scripts/check-remaining-work.sh"
      }
    ]
  }
}
```

**Exit code 2 pattern** (unique to team hooks):
- `exit 0` → Allow teammate to go idle
- `exit 2` → Keep teammate working (stderr fed back as instructions)
- `exit 1` → Error (logged, teammate goes idle anyway)

**Note:** Agent hooks (`type: "agent"`) are NOT supported for TeammateIdle — use command hooks only.

### TaskCompleted

Fires when a task is being marked complete.

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "type": "command",
        "command": "./scripts/verify-task.sh"
      }
    ]
  }
}
```

**Exit code 2 pattern:**
- `exit 0` → Allow task completion
- `exit 2` → Block completion (stderr explains why — e.g., "tests not passing")
- `exit 1` → Error (logged, task completes anyway)
