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

**Rule of thumb:** If agents will edit the same files → use agent-teams (worktree isolation). If agents read-only or edit different files → use subagent-teams (faster, lighter).

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

## Task Tool Parameters

```javascript
// Key parameters for Task tool
{
  subagent_type: "Explore" | "general-purpose" | "Plan" | "code-reviewer" | ...,
  model: "haiku" | "sonnet" | "opus",  // haiku for search, sonnet for code, opus for architecture
  prompt: "...",                         // Clear, self-contained task description
  run_in_background: true,              // For parallel execution
  description: "3-5 word summary"       // Required
}
```

### Model Selection Guide

| Task | Model | Why |
|------|-------|-----|
| File search, pattern matching | haiku | Fast, cheap, sufficient |
| Code review, bug finding | haiku | Pattern matching, not generation |
| Code generation, refactoring | sonnet | Quality matters for code |
| Architecture decisions | opus | Complex reasoning needed |
| Documentation writing | sonnet | Needs context understanding |

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

## Progress Display

### During Execution
```
🔄 Subagent Team: Research Sprint
├── Agent 1 (Explore): Searching auth patterns... ⏳
├── Agent 2 (Explore): Searching DB schema... ✅ (found 12 matches)
└── Agent 3 (Explore): Searching API endpoints... ✅ (found 8 matches)
```

### After Fan-In
```
📊 Research Complete: 3/3 agents finished
├── Auth: 12 files, JWT + session patterns
├── DB: 8 tables, RLS policies found
└── API: 15 endpoints, REST conventions
```

---

## Constraints

- **Max 5-7 parallel agents** — beyond this, context window fills up
- **No conflicting file edits** — if agents might edit the same file, use agent-teams instead
- **Fan-in is manual** — you (team lead) synthesize results from background agents
- **Background agents can't see each other** — design tasks to be independently completable

**Deep dive:** See `reference/task-tool-guide.md`, `reference/team-patterns.md`, `reference/prompt-templates.md`
