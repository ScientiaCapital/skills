---
name: "worktree-manager"
description: "Parallel development with git worktrees and Claude Code agents. Ghostty terminal launching, port allocation, global registry. Use when: create worktree, spin up worktrees, parallel development, worktree status, cleanup worktrees, launch agent in worktree."
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
5. Launch Ghostty terminal with Claude Opus 4.5 agent
</quick_start>

<success_criteria>
A worktree setup is successful when:
- Worktree created at `~/tmp/worktrees/[project]/[branch-slug]`
- Ports allocated and registered globally
- Dependencies installed
- Agent launched in Ghostty terminal
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

**See:** `references/port-allocation.md` for detailed operations.

### Required Defaults

**CRITICAL**: These settings MUST be used when launching agents:

| Setting | Value | Reason |
|---------|-------|--------|
| Terminal | Ghostty | Required terminal for agent launching |
| Model | `claude-opus-4-5-20250514` | Most capable for autonomous work |
| Flags | `--dangerously-skip-permissions` | Required for autonomous file ops |

**Launch command pattern:**
```bash
ghostty -e "cd {worktree_path} && claude --model claude-opus-4-5-20250514 --dangerously-skip-permissions"
```

</core_concepts>

<config>

## Skill Config

Location: `~/.claude/skills/worktree-manager/config.json`

```json
{
  "terminal": "ghostty",
  "shell": "zsh",
  "defaultModel": "opus",
  "modelId": "claude-opus-4-5-20250514",
  "claudeCommand": "claude --model claude-opus-4-5-20250514 --dangerously-skip-permissions",
  "portPool": { "start": 8100, "end": 8199 },
  "portsPerWorktree": 2,
  "worktreeBase": "~/tmp/worktrees",
  "defaultCopyDirs": [".agents"],
  "envFilePriority": [".env.local", ".env", ".env.example"],
  "autoCleanupOnMerge": true
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

4. COPY UNCOMMITTED RESOURCES
   cp -r .agents $WORKTREE_PATH/ 2>/dev/null || true
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
   ghostty -e "cd $WORKTREE_PATH && claude --model claude-opus-4-5-20250514 --dangerously-skip-permissions"

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

**See:** `references/cleanup-operations.md` for full cleanup procedure.

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
| Registry operations | `references/registry-operations.md` |
| Port allocation | `references/port-allocation.md` |
| Agent launching | `references/agent-launching.md` |
| Script reference | `references/script-reference.md` |
| Cleanup operations | `references/cleanup-operations.md` |
| Troubleshooting | `references/troubleshooting.md` |

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
5. Copy .agents/ and .env to each
6. Install deps: `(cd <path> && uv sync)`
7. Register both in `~/.claude/worktree-registry.json`
8. Launch agents:
   ```bash
   ghostty -e "cd ~/tmp/worktrees/.../feature-dark-mode && claude --model claude-opus-4-5-20250514 --dangerously-skip-permissions"
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
