---
name: "subagent-teams"
description: "Orchestrate in-session Task tool teams for parallel work. Fan-out research, implementation, review, and documentation across subagents. Use when: parallel tasks, fan-out, subagent team, Task tool, in-session agents."
---

<objective>
Orchestrate teams of Task tool subagents within a single Claude Code session. Unlike agent-teams-skill (which uses worktrees + terminals for full parallel sessions), this skill uses the Task tool for lightweight, in-session parallelism with shared codebase access.
</objective>

<quick_start>
**Research fan-out:**
```
Launch 3 Explore agents in parallel:
- Agent 1: Search for authentication patterns
- Agent 2: Search for database schema
- Agent 3: Search for API endpoints
```

**Implementation fan-out:**
```
1. Plan agent designs architecture
2. 3 general-purpose agents build components in parallel
3. code-reviewer agent validates all changes
```
</quick_start>

<success_criteria>
- Subagents spawned with correct model tiers (Haiku for search/review, Sonnet for code, Opus for architecture)
- Parallel agents complete independently without conflicting file edits
- Fan-in synthesis captures key findings from all background agents
- Total parallel agents stays within 5-7 limit to avoid context overflow
- TaskCreate/TaskUpdate used for progress tracking with live UI spinners
</success_criteria>

<triggers>
- "set up subagent team", "fan out", "parallel tasks", "Task tool team"
- "research in parallel", "explore in parallel", "review in parallel"
- "spawn subagents", "in-session agents"
</triggers>

---

## When to Use This vs agent-teams

| Factor | subagent-teams (this) | agent-teams |
|--------|----------------------|-------------|
| Isolation | Shared codebase, shared context | Full worktree isolation |
| Overhead | Lightweight — just Task tool calls | Heavy — terminals, git branches, ports |
| Best for | Research, review, doc updates | Feature builds, conflicting file edits |
| Max agents | 5-7 (context limit) | 2-3 (M1 8GB RAM limit) |
| Duration | Minutes | Hours |
| Coordination | TeamCreate + TaskList/TaskUpdate | WORKTREE_TASK.md + git branches |

**Rule of thumb:** If agents will edit the same files → use agent-teams (worktree isolation). If agents read-only or edit different files → use subagent-teams (faster, lighter).

---

## Task Tool Parameters (Complete Reference)

### Core Parameters

```javascript
{
  subagent_type: "Explore" | "general-purpose" | "Plan" | ...,
  model: "haiku" | "sonnet" | "opus",
  prompt: "...",
  description: "3-5 word summary",        // Required
  run_in_background: true,                 // For parallel execution
  team_name: "my-team",                    // Scope to a team's task list
  name: "agent-1",                         // Name for team messaging
  mode: "default"                          // Permission mode (see below)
}
```

### Agent Frontmatter Fields (for .md agent files)

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | Agent identifier |
| `description` | string | What the agent does (shown in routing) |
| `model` | string | Default model: haiku, sonnet, opus |
| `tools` | list | Allowed tools (restrict agent capabilities) |
| `disallowedTools` | list | Explicitly blocked tools |
| `permissionMode` | string | `default`, `acceptEdits`, `dontAsk`, `plan` |
| `mcpServers` | list | MCP servers available to the agent |
| `hooks` | object | Event-driven automation (PostToolUse, etc.) |
| `maxTurns` | number | Max API round-trips before stopping |
| `skills` | list | Skills available to the agent |
| `memory` | object | Persistent state (see Memory Scopes below) |

### Memory Scopes

The `memory` field gives agents persistent state across sessions:

```yaml
# User-scoped: shared across all projects for this user
memory:
  scope: user    # Stored in ~/.claude/agent-memory/

# Project-scoped: shared across sessions within one project
memory:
  scope: project # Stored in .claude/agent-memory/

# Local-scoped: private to this machine + project combo
memory:
  scope: local   # Stored in .claude/local/agent-memory/
```

**When to use:** `user` for personal preferences/patterns. `project` for shared team knowledge. `local` for machine-specific paths or credentials.

### Background Execution

Use `run_in_background: true` for agents that don't block your next action:

```javascript
// Launch in background — returns immediately with output_file path
Task({
  subagent_type: "Explore",
  prompt: "Search for all auth patterns",
  run_in_background: true  // Non-blocking
})

// Check results later
TaskOutput({ task_id: "agent-id", block: false })  // Non-blocking check
TaskOutput({ task_id: "agent-id", block: true })    // Wait for completion
```

**Foreground vs background:**
- **Foreground** (default): Use when you need results before proceeding — research that informs next steps
- **Background**: Use when you have independent work to do in parallel — observers, linters, long searches

**Tip:** Background agents are ideal for observer-lite/observer-full, security scans, and parallel research where you can synthesize results later.

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Normal approval flow |
| `acceptEdits` | Auto-approve file edits, prompt for Bash |
| `dontAsk` | Auto-approve everything (use with trusted agents) |
| `plan` | Agent must get plan approved before implementing |
| `delegate` | Agent can only delegate to sub-agents |

### Spawning Restrictions

Restrict which subagents an agent can spawn using `Task(agent_type)` in the tools field:
```yaml
tools:
  - Read
  - Glob
  - Task(Explore)        # Can only spawn Explore subagents
  - Task(code-reviewer)  # Can also spawn code reviewers
```

**Built-in agent types and their tool access:**

| Agent Type | Tools | Best For |
|-----------|-------|----------|
| `Explore` | Glob, Grep, Read, LS, WebFetch, WebSearch | Fast codebase search (read-only) |
| `Plan` | Glob, Grep, Read, LS, WebFetch, WebSearch | Architecture design (read-only) |
| `general-purpose` | All tools | Implementation, full access |
| `feature-dev:code-reviewer` | Glob, Grep, Read, LS, WebFetch | Code review (read-only) |
| `feature-dev:code-explorer` | Glob, Grep, Read, LS, WebFetch | Deep feature analysis (read-only) |
| `feature-dev:code-architect` | Glob, Grep, Read, LS, WebFetch | Architecture blueprints (read-only) |
| `observer-lite` | Read, Glob, Grep, Bash, Write | Quick quality checks |
| `observer-full` | Read, Glob, Grep, Bash, Write | Full drift detection |

**Custom agents:** Define in `.claude/agents/*.md` with frontmatter. Reference by filename (without `.md`).

### Model Selection Guide

| Task | Model | Why |
|------|-------|-----|
| File search, pattern matching | haiku | Fast, cheap, sufficient |
| Code review, bug finding | haiku | Pattern matching, not generation |
| Code generation, refactoring | sonnet | Quality matters for code |
| Architecture decisions | opus | Complex reasoning needed |
| Documentation writing | sonnet | Needs context understanding |

---

## Team Patterns

### 1. Research Team (3 Explore agents)

Fan-out 3 search strategies, fan-in to synthesize:

```
Task 1 (Explore, haiku): "Search for [pattern] in src/"
Task 2 (Explore, haiku): "Search for [pattern] in tests/"
Task 3 (Explore, haiku): "Search for [pattern] in docs/"
→ Fan-in: Synthesize findings into summary
```

**When:** Exploring unfamiliar codebase, understanding how a feature works across layers.

### 2. Implement Team (architect → builders → reviewer)

Sequential pipeline with parallel build phase:

```
Phase 1: Plan agent designs architecture (1 agent)
Phase 2: 2-3 general-purpose agents build components (parallel)
Phase 3: code-reviewer validates (1 agent)
```

**When:** Building a feature with multiple independent components.

### 3. Review Team (3 reviewers in parallel)

```
Task 1 (code-reviewer, haiku): "Review src/auth/ for security"
Task 2 (code-reviewer, haiku): "Review src/api/ for consistency"
Task 3 (code-reviewer, haiku): "Review src/db/ for performance"
→ Fan-in: Aggregate findings, deduplicate
```

**When:** Pre-PR review of large changesets.

### 4. Explore Team (3 search strategies)

```
Task 1 (Explore, haiku): Glob for file patterns
Task 2 (Explore, haiku): Grep for code patterns
Task 3 (Explore, haiku): Read key entry points
→ Fan-in: Build mental model of codebase area
```

**When:** First time working in a new area of the codebase.

### 5. Doc Team (N independent file updaters)

```
Task 1 (general-purpose, haiku): "Update README.md with new API"
Task 2 (general-purpose, haiku): "Update CHANGELOG.md"
Task 3 (general-purpose, haiku): "Update API docs"
→ No fan-in needed (independent files)
```

**When:** Updating multiple independent documentation files.

---

## Progress Rendering

### Native Progress (TaskCreate/TaskUpdate)

Use TaskCreate with `activeForm` for live UI spinners during execution:

```javascript
// Create tasks for each agent's work
TaskCreate({ subject: "Search auth patterns", activeForm: "Searching auth patterns" })
TaskCreate({ subject: "Search DB schema", activeForm: "Searching DB schema" })
TaskCreate({ subject: "Search API endpoints", activeForm: "Searching API endpoints" })

// Track status transitions
TaskUpdate({ taskId: "1", status: "in_progress" })  // → shows spinner
TaskUpdate({ taskId: "1", status: "completed" })     // → shows checkmark
```

### Task Dependencies (Sequential Phases)

Use `addBlockedBy` to sequence phases:

```javascript
// Phase 1: Architecture (runs first)
TaskCreate({ subject: "Design architecture" })  // → task #1

// Phase 2: Implementation (blocked by Phase 1)
TaskCreate({ subject: "Build backend" })   // → task #2
TaskCreate({ subject: "Build frontend" })  // → task #3
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "3", addBlockedBy: ["1"] })

// Phase 3: Review (blocked by Phase 2)
TaskCreate({ subject: "Code review" })  // → task #4
TaskUpdate({ taskId: "4", addBlockedBy: ["2", "3"] })
```

### Summary Rendering (Markdown)

After all agents complete, render a markdown summary:

```
## Research Complete: 3/3 agents finished

| Agent | Scope | Findings | Time |
|-------|-------|----------|------|
| Auth search | src/auth/ | 12 files, JWT + session | 8s |
| DB search | src/db/ | 8 tables, RLS policies | 5s |
| API search | src/api/ | 15 endpoints, REST | 6s |

### Key Insights
- [Synthesized finding 1]
- [Synthesized finding 2]
```

---

## Team Coordination (Native Agent Teams API)

For complex multi-agent work, use the native Teams API:

```javascript
// Create a team with shared task list
TeamCreate({ team_name: "research-sprint" })

// Spawn teammates into the team
Task({ subagent_type: "Explore", team_name: "research-sprint", name: "searcher-1" })
Task({ subagent_type: "Explore", team_name: "research-sprint", name: "searcher-2" })

// Teammates coordinate via shared TaskList
// Send messages between teammates
SendMessage({ type: "message", recipient: "searcher-1", content: "Focus on auth/" })

// Shutdown when done
SendMessage({ type: "shutdown_request", recipient: "searcher-1" })
```

---

## Prompt Templates

### Research Spawn
```
Search the codebase for [PATTERN]. Look in [SCOPE].
Report: file paths, line numbers, and a 2-sentence summary of each match.
Do NOT modify any files.
```

### Build Spawn
```
Implement [COMPONENT] in [FILE_PATH].
Requirements: [SPEC]
Follow existing patterns in [EXAMPLE_FILE].
Write code only — do not run tests.
```

### Review Spawn
```
Review [FILE_PATH] for [CONCERN: security|performance|consistency].
Report only HIGH confidence issues.
Format: file:line — issue — suggestion
```

---

## Constraints

- **Max 5-7 parallel agents** — beyond this, context window fills up
- **No conflicting file edits** — if agents might edit the same file, use agent-teams instead
- **Fan-in is manual** — you (team lead) synthesize results from background agents
- **Background agents can't see each other** — design tasks to be independently completable

**Deep dive:** See `reference/task-tool-guide.md`, `reference/team-patterns.md`, `reference/prompt-templates.md`
