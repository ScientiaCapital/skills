---
name: "worktree-manager"
description: "Parallel development with git worktrees and Claude Code agents. Handles Ghostty terminal launching, port allocation, and global registry. Use when creating worktrees, managing parallel development, or launching agents in isolated workspaces."
disable-model-invocation: true
---

<objective>
Manage parallel development across ALL projects using git worktrees with Claude Code agents. Each worktree is an isolated copy of the repo on a different branch, stored centrally at `~/tmp/worktrees/`. This enables multiple agents to work simultaneously without conflicts.
</objective>

<quick_start>
**Create a single worktree with agent:**
```
/worktree create feature/auth
```

Claude will:
1. Allocate ports (8100-8101)
2. Create worktree at `~/tmp/worktrees/[project]/feature-auth`
3. Install dependencies
4. Create WORKTREE_TASK.md for the agent
5. Launch terminal with Claude Opus 4.6 agent
</quick_start>

## Native --worktree Flag (Claude Code v2.1.49+)

Claude Code now has built-in worktree support:

```bash
# Named worktree
claude --worktree feature-auth   # or: claude -w feature-auth

# Auto-generated name
claude -w
```

### What It Does

- Creates worktree at `<repo>/.claude/worktrees/<name>/`
- Branch: `worktree-<name>` (auto-created from default remote branch)
- On exit: auto-cleanup if no changes; prompts to keep/remove if changes exist

**Tip:** Add `.claude/worktrees/` to `.gitignore`

### When to Use Native vs This Skill

| Scenario | Use |
|----------|-----|
| Quick isolated work, single agent | `claude -w feature-name` |
| Multi-agent teams, port allocation, registry | This skill (worktree-manager) |
| Subagent isolation | `isolation: "worktree"` in Task tool param |
| Non-git VCS (Perforce, SVN) | WorktreeCreate/WorktreeRemove hooks |

### WorktreeCreate / WorktreeRemove Hooks

New hook events for VCS-agnostic worktree lifecycle. These replace the default git worktree behavior when configured:

```json
{
  "hooks": {
    "WorktreeCreate": [{
      "hooks": [{
        "type": "command",
        "command": "bash -c 'INPUT=$(cat); NAME=$(echo \"$INPUT\" | jq -r .name); mkdir -p /tmp/worktrees/$NAME && echo $NAME'"
      }]
    }],
    "WorktreeRemove": [{
      "hooks": [{
        "type": "command",
        "command": "bash -c 'INPUT=$(cat); PATH=$(echo \"$INPUT\" | jq -r .path); rm -rf $PATH'"
      }]
    }]
  }
}
```

**When to use hooks vs native:** Use hooks when working with non-git VCS systems or when you need custom isolation logic (e.g., Docker containers, remote dev servers). For standard git repos, the native `claude -w` flag or this skill's workflow is preferred.

**Note:** These hooks do NOT support matchers. They fire once per worktree lifecycle event. The hook receives `{name, path}` via stdin JSON.

<success_criteria>
A worktree setup is successful when:
- Worktree created at `~/tmp/worktrees/[project]/[branch-slug]`
- Ports allocated and registered globally
- Dependencies installed
- Agent launched in terminal (Ghostty/iTerm2/tmux)
- Entry added to `~/.claude/worktree-registry.json`
</success_criteria>

<current_state>
Git repository:
!`git status --short --branch 2>/dev/null`

Existing worktrees:
!`git worktree list 2>/dev/null`

Worktree registry:
!`cat ~/.claude/worktree-registry.json 2>/dev/null | jq -r '.worktrees[] | "\(.project)/\(.branch) → \(.status)"' | head -10`

Available ports:
!`cat ~/.claude/worktree-registry.json 2>/dev/null | jq '.portPool.allocated | length' || echo "0"` allocated
</current_state>

<activation_triggers>

## When This Skill Activates

**Trigger phrases:**
- "spin up worktrees for X, Y, Z"
- "create 3 worktrees for features A, B, C"
- "new worktree for feature/auth"
- "what's the status of my worktrees?"
- "show all worktrees" / "show worktrees for this project"
- "clean up merged worktrees"
- "launch agent in worktree X"

## Invocation

**Command syntax:**
- `/worktree create feature/auth` - Single worktree
- `/worktree create feat1 feat2 feat3` - Multiple worktrees
- `/worktree status` - Check all worktrees
- `/worktree status --project myapp` - Filter by project
- `/worktree cleanup feature/auth` - Remove worktree
- `/worktree launch feature/auth` - Launch agent in worktree

</activation_triggers>

<file_locations>

## Key Files

| File | Purpose |
|------|---------|
| `~/.claude/worktree-registry.json` | **Global registry** - tracks all worktrees across all projects |
| `~/.claude/skills/worktree-manager/config.json` | **Skill config** - terminal, shell, port range settings |
| `~/.claude/skills/worktree-manager/scripts/` | **Helper scripts** - optional, can do everything manually |
| `~/tmp/worktrees/` | **Worktree storage** - all worktrees live here |
| `.claude/` (per-project) | **Project config** - CLAUDE.md, hooks, permissions, custom agents |
| `.claude/worktree.json` (per-project) | **Project config** - optional custom settings |
| `WORKTREE_TASK.md` (per-worktree) | **Auto-loaded task prompt** - agent reads on startup |

</file_locations>

<core_concepts>

## Core Concepts

### Centralized Worktree Storage

All worktrees live in `~/tmp/worktrees/<project-name>/<branch-slug>/`

```
~/tmp/worktrees/
├── obsidian-ai-agent/
│   ├── feature-auth/           # branch: feature/auth
│   ├── feature-payments/       # branch: feature/payments
│   └── fix-login-bug/          # branch: fix/login-bug
└── another-project/
    └── feature-dark-mode/
```

### Branch Slug Convention

Branch names are slugified for filesystem safety:
- `feature/auth` → `feature-auth`
- `fix/login-bug` → `fix-login-bug`

**Slugify manually:** `echo "feature/auth" | tr '/' '-'`

### Port Allocation

- **Global pool**: 8100-8199 (100 ports total)
- **Per worktree**: 2 ports allocated (for API + frontend patterns)
- **Globally unique**: Ports tracked to avoid conflicts across projects

**See:** `reference/port-allocation.md` for detailed operations.

### Required Defaults

**CRITICAL**: These settings MUST be used when launching agents:

| Setting | Value | Reason |
|---------|-------|--------|
| Terminal | Ghostty or iTerm2 | Auto-detected, configurable in config.json |
| Model | `--model opus` | Opus 4.6 alias (most capable) |
| Flags | `--dangerously-skip-permissions` | Required for autonomous file ops |

**Launch command pattern:**
```bash
# Recommended: agent inherits .claude/ config (CLAUDE.md, hooks, permissions)
claude --model opus --dangerously-skip-permissions

# Or with explicit permission allowlist (safer, from .claude/settings.json):
claude --model opus --allowedTools "Bash(npm test),Bash(npm run build),Edit,Write,Read,Glob,Grep"
```

### Subagent Worktree Isolation

Subagents can be configured to run in isolated worktrees:

```yaml
# In subagent frontmatter:
---
name: my-subagent
isolation: worktree
---
```

The subagent runs in a temporary worktree. On completion:
- If no changes: auto-cleanup
- If changes exist: changes preserved for review

</core_concepts>

<config>

## Skill Config

Location: `~/.claude/skills/worktree-manager/config.json`

```json
{
  "terminal": "ghostty",
  "terminalPreference": "auto",
  "enableNumberedTabs": true,
  "shell": "zsh",
  "defaultModel": "opus",
  "claudeCommand": "claude --model opus --dangerously-skip-permissions",
  "portPool": { "start": 8100, "end": 8199 },
  "portsPerWorktree": 2,
  "worktreeBase": "~/tmp/worktrees",
  "defaultCopyDirs": [".claude"],
  "envFilePriority": [".env.local", ".env", ".env.example"],
  "autoCleanupOnMerge": true
}
```

### .claude/ Directory Propagation

When creating worktrees, the entire `.claude/` directory is copied so agents inherit project-level config:

```
.claude/
├── CLAUDE.md              # Project instructions (auto-loaded by Claude Code)
├── settings.json          # Hooks and permissions
│   ├── hooks.PostToolUse  # Auto-format on Write|Edit (e.g., "bun run format || true")
│   └── permissions.allow  # Whitelisted bash commands for agents
├── agents/                # Custom subagent definitions
│   ├── build-validator.md # Validates builds pass
│   ├── code-architect.md  # Plans implementation
│   ├── code-simplifier.md # Refactors for clarity
│   └── verify-app.md      # End-to-end verification
└── PROJECT_CONTEXT.md     # Session continuity (project-context-skill)
```

**Why this matters:**
- **CLAUDE.md**: Agent reads project conventions, dev commands, tech stack
- **Hooks**: Auto-formatting runs after every Write/Edit, keeping code consistent across agents
- **Permissions**: Agents can run pre-approved commands without prompting (e.g., `npm test`, `bun run build`)
- **Custom agents**: Agents can dispatch subagents (e.g., `verify-app.md` for end-to-end checks)

**Hook example (settings.json):**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "bun run format || true" }]
      }
    ]
  }
}
```

</config>

<workflows>

## Workflows

### Create Multiple Worktrees

**User says:** "Spin up 3 worktrees for feature/auth, feature/payments, and fix/login-bug"

**You do (can parallelize with subagents):**

```
For EACH branch (can run in parallel):

1. SETUP
   PROJECT=$(basename $(git remote get-url origin 2>/dev/null | sed 's/\.git$//') || basename $(pwd))
   REPO_ROOT=$(git rev-parse --show-toplevel)
   BRANCH_SLUG=$(echo "feature/auth" | tr '/' '-')
   WORKTREE_PATH=~/tmp/worktrees/$PROJECT/$BRANCH_SLUG

2. ALLOCATE PORTS
   Find 2 unused ports from 8100-8199, add to registry

3. CREATE WORKTREE
   mkdir -p ~/tmp/worktrees/$PROJECT
   git worktree add $WORKTREE_PATH -b $BRANCH

4. COPY PROJECT CONFIG (.claude/ directory)
   cp -r .claude $WORKTREE_PATH/ 2>/dev/null || true
   Copy .env.local or .env as appropriate

5. CREATE WORKTREE_TASK.md
   Create detailed task file for agent

6. INSTALL DEPENDENCIES
   Detect package manager, run install command

7. VALIDATE (optional)
   Start server, health check, stop

8. REGISTER IN GLOBAL REGISTRY
   Update ~/.claude/worktree-registry.json with entry

9. LAUNCH AGENT
   ghostty -e "cd $WORKTREE_PATH && claude --model opus --dangerously-skip-permissions"

AFTER ALL COMPLETE:
- Report summary table to user
```

### Check Status

**With script:**
```bash
~/.claude/skills/worktree-manager/scripts/status.sh
~/.claude/skills/worktree-manager/scripts/status.sh --project my-project
```

**Manual:**
```bash
cat ~/.claude/worktree-registry.json | jq -r '.worktrees[] | "\(.project)\t\(.branch)\t\(.ports | join(","))\t\(.status)"'
```

### Cleanup Worktree

**See:** `reference/cleanup-operations.md` for full cleanup procedure.

**Quick cleanup:**
```bash
~/.claude/skills/worktree-manager/scripts/cleanup.sh <project> <branch> --delete-branch
```

</workflows>

<routing>

## Reference Files

For detailed operations, see:

| Topic | File |
|-------|------|
| Registry operations | `reference/registry-operations.md` |
| Port allocation | `reference/port-allocation.md` |
| Agent launching | `reference/agent-launching.md` |
| **System notifications** | `reference/system-notifications.md` |
| Script reference | `reference/script-reference.md` |
| Cleanup operations | `reference/cleanup-operations.md` |
| Advanced workflows | `reference/advanced-workflows.md` |
| Troubleshooting | `reference/troubleshooting.md` |

</routing>

<safety_guidelines>

## Safety Guidelines

1. **Before cleanup**, check PR status:
   - PR merged → safe to clean everything
   - PR open → warn user, confirm before proceeding
   - No PR → warn about unsubmitted work

2. **Before deleting branches**, confirm if:
   - PR not merged
   - No PR exists
   - Worktree has uncommitted changes

3. **Port conflicts**: If port in use by non-worktree process, pick different port

4. **Environment files**: Never commit `.env` or `.env.local` to git

</safety_guidelines>

<example_session>

## Example Session

**User:** "Spin up 2 worktrees for feature/dark-mode and fix/login-bug"

**You:**
1. Detect project: `obsidian-ai-agent` (from git remote)
2. Detect package manager: `uv` (found uv.lock)
3. Allocate 4 ports: `8100 8101 8102 8103`
4. Create worktrees:
   ```bash
   git worktree add ~/tmp/worktrees/obsidian-ai-agent/feature-dark-mode -b feature/dark-mode
   git worktree add ~/tmp/worktrees/obsidian-ai-agent/fix-login-bug -b fix/login-bug
   ```
5. Copy .claude/ and .env to each
6. Install deps: `(cd <path> && uv sync)`
7. Register both in `~/.claude/worktree-registry.json`
8. Launch agents:
   ```bash
   ghostty -e "cd ~/tmp/worktrees/.../feature-dark-mode && claude --model opus --dangerously-skip-permissions"
   ```
9. Report:
   ```
   Created 2 worktrees with agents:

   | Branch | Ports | Path | Task |
   |--------|-------|------|------|
   | feature/dark-mode | 8100, 8101 | ~/tmp/worktrees/.../feature-dark-mode | Implement dark mode |
   | fix/login-bug | 8102, 8103 | ~/tmp/worktrees/.../fix-login-bug | Fix login redirect |

   Both agents running in Ghostty windows.
   ```

</example_session>

---

## Boris Cherny Workflow Integration

iTerm2 notifications, web session handoff (`/teleport`), ralph-loop for autonomous sessions, and daily workflow protocols.

See `reference/advanced-workflows.md` for iTerm2 setup, teleport handoff, ralph-loop patterns, terminal strategy, and daily workflow protocol.
