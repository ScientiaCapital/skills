<overview>
Hooks are event-driven automation for Claude Code that execute shell commands or LLM prompts in response to tool usage, session events, and user interactions. This reference covers hook configuration, types, and patterns.
</overview>

<table_of_contents>
1. Quick Start
2. Hook Types (Events)
3. Hook Anatomy
4. Matchers
5. Input/Output Schemas
6. Environment Variables
7. Common Patterns
8. Troubleshooting
9. Security Checklist
</table_of_contents>

<quick_start>
<workflow>
1. Create hooks config file:
   - Project: `.claude/hooks.json`
   - User: `~/.claude/hooks.json`
2. Choose hook event (when it fires)
3. Choose hook type (command or prompt)
4. Configure matcher (which tools trigger it)
5. Test with `claude --debug`
</workflow>

<minimal_example>
**Log all bash commands:**

`.claude/hooks.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```
</minimal_example>
</quick_start>

<hook_types>
| Event | When | Can Block? |
|-------|------|------------|
| `SessionStart` | Session begins or resumes | No |
| `UserPromptSubmit` | Before Claude processes prompt | Yes |
| `PreToolUse` | Before tool execution | Yes |
| `PermissionRequest` | Permission dialog appears | Yes |
| `PostToolUse` | After tool succeeds | No (feeds back) |
| `PostToolUseFailure` | After tool fails | No |
| `Notification` | Claude sends notification | No |
| `SubagentStart` | Subagent spawns | No |
| `SubagentStop` | Subagent finishes | Yes |
| `Stop` | Claude finishes responding | Yes |
| `TeammateIdle` | Agent team teammate about to go idle | Yes (exit 2 only) |
| `TaskCompleted` | Task being marked complete | Yes (exit 2 only) |
| `ConfigChange` | Config file changes mid-session | Yes (except policy) |
| `PreCompact` | Before context compaction | No |
| `SessionEnd` | Session terminates | No |

<pretooluse>
**Purpose:** Validate, modify, or block tool calls before execution.

**Use cases:**
- Block destructive commands (rm -rf, force push)
- Validate commit message format
- Add flags to commands (--save-exact)
- Log command attempts

**Example - Block force push to main (command hook):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-safety.sh"
          }
        ]
      }
    ]
  }
}
```

**Command hook output schema (PreToolUse):**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Explanation"
  },
  "updatedInput": { "command": "modified command" }
}
```

> **Note:** `"allow"` permits, `"deny"` blocks, `"ask"` escalates to the user.
> Top-level `decision`/`reason` fields are deprecated for PreToolUse. Other events (Stop, UserPromptSubmit) still use top-level `decision`.

**Example - Block force push to main (prompt hook):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this command is safe: $ARGUMENTS\n\nBlock if: force push to main/master\n\nReturn JSON: {\"ok\": true} or {\"ok\": false, \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

**Prompt hook output schema:**
```json
{
  "ok": true
}
// or
{
  "ok": false,
  "reason": "Explanation"
}
```
</pretooluse>

<posttooluse>
**Purpose:** React to completed tool calls.

**Use cases:**
- Auto-format code after Write/Edit
- Run tests after code changes
- Update documentation
- Send notifications

**Example - Auto-format after edits:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_PROJECT_DIR",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```
</posttooluse>

<stop>
**Purpose:** Validate before Claude stops working.

**Use cases:**
- Verify all tasks completed
- Check tests pass before stopping
- Validate deliverables

**Critical:** Check `stop_hook_active` to prevent infinite loops.

**Example:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm test && echo '{\"decision\": \"approve\"}' || echo '{\"decision\": \"block\", \"reason\": \"Tests failing\"}'"
          }
        ]
      }
    ]
  }
}
```

**Output schema:**
```json
{
  "decision": "block" | undefined,
  "reason": "Why Claude should continue",
  "continue": true,
  "systemMessage": "Additional instructions"
}
```
</stop>

<sessionstart>
**Purpose:** Inject context at session start.

**Use cases:**
- Load sprint context
- Set environment info
- Display welcome messages

**Example:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"Sprint 23. Focus: Authentication\"}}'"
          }
        ]
      }
    ]
  }
}
```
</sessionstart>

<notification>
**Purpose:** Alert user when Claude needs input.

**Example - macOS notification:**
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```
</notification>

<teammateidle>
### TeammateIdle

Fires when an agent team teammate is about to go idle (between turns).

**Input:**
```json
{
  "session_id": "abc-123",
  "teammate_name": "researcher",
  "teammate_agent_id": "agent-456",
  "tasks_completed": 3,
  "tasks_remaining": 2
}
```

**Exit code 2 pattern:** Unlike standard blocking (exit 1), TeammateIdle uses exit code 2:
- `exit 0` → Allow teammate to go idle
- `exit 2` → Keep teammate working (stderr fed back as instructions)
- `exit 1` → Error (logged, teammate goes idle anyway)

**Note:** Agent hooks (`type: "agent"`) are NOT supported for TeammateIdle.
</teammateidle>

<taskcompleted>
### TaskCompleted

Fires when a task is being marked as complete in agent teams.

**Input:**
```json
{
  "session_id": "abc-123",
  "task_id": "task-789",
  "task_subject": "Implement auth module",
  "completed_by": "builder-1"
}
```

**Exit code 2 pattern:**
- `exit 0` → Allow task completion
- `exit 2` → Block completion (stderr fed back as reason — e.g., "tests not passing")
- `exit 1` → Error (logged, task completes anyway)
</taskcompleted>
</hook_types>

<hook_anatomy>
<command_hooks>
**Type:** Execute a shell command

**When to use:**
- Simple validation (check file exists)
- Logging (append to file)
- External tools (formatters, linters)
- Desktop notifications

**Input:** JSON via stdin
**Output:** JSON via stdout (optional)

```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 30000
}
```
</command_hooks>

<prompt_hooks>
**Type:** LLM evaluates a prompt

**When to use:**
- Complex decision logic
- Natural language validation
- Context-aware checks
- Reasoning required

**Input:** Prompt with `$ARGUMENTS` placeholder
**Output:** JSON with `ok` and `reason`

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS\n\nReturn JSON: {\"ok\": true} or {\"ok\": false, \"reason\": \"explanation\"}"
}
```

**Response schema:**
```json
{
  "ok": true
}
// or
{
  "ok": false,
  "reason": "Explanation of why the action was blocked"
}
```

**Note:** Prompt hooks use `{ "ok": true/false }` — NOT `{ "decision": "approve" | "block" }` which is for command hooks only.
</prompt_hooks>

<agent_hooks>

## Agent-Based Hooks (type: "agent")

Agent hooks spawn a subagent to evaluate conditions using Read, Grep, and Glob tools. Best for multi-step verification that requires reasoning.

### Configuration

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "agent",
        "prompt": "Verify all unit tests pass before stopping. $ARGUMENTS",
        "model": "claude-haiku-4-5",
        "timeout": 120
      }
    ]
  }
}
```

### How Agent Hooks Work

1. Subagent spawns with Read, Grep, and Glob tools (up to 50 turns)
2. Subagent evaluates the prompt against current state
3. Returns structured response: `{ "ok": true }` or `{ "ok": false, "reason": "..." }`
4. If `ok: false`, the action is blocked and reason is fed back to Claude

### Constraints

- Default model: `claude-haiku-4-5` (fast, cheap — override with `model` field)
- NOT supported for `TeammateIdle` event
- Maximum 50 agentic turns per invocation
- `$ARGUMENTS` expands to the hook's input JSON

### When to Use Agent Hooks

| Scenario | Handler |
|----------|---------|
| Deterministic check (lint, format) | `type: "command"` |
| Single LLM judgment ("is this safe?") | `type: "prompt"` |
| Multi-step verification (read files, grep patterns, reason) | `type: "agent"` |

</agent_hooks>

<async_hooks>

## Async Hooks (async: true)

Command hooks can run asynchronously — fire-and-forget without blocking Claude's response.

### Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "/path/to/run-tests.sh",
        "async": true,
        "timeout": 120
      }
    ]
  }
}
```

### Behavior

- **Command hooks only** — not supported for `type: "prompt"` or `type: "agent"`
- Fire-and-forget — does NOT block the action
- Output is delivered via `systemMessage` on Claude's next turn
- Exit codes are ignored (cannot block)

### Best Used For

- `PostToolUse`: Run tests after file changes
- `Stop`: Trigger CI pipeline after session ends
- `SessionEnd`: Save analytics or cleanup

### Anti-pattern

Do NOT use `async: true` on blocking events (`PreToolUse`, `UserPromptSubmit`) — the action will proceed before the hook completes, defeating the purpose.

</async_hooks>

<skill_scoped_hooks>

## Skill-Scoped Hooks

Hooks can be defined directly in a skill's YAML frontmatter. These hooks are scoped to the skill's lifecycle — active only while the skill is loaded.

### Syntax

```yaml
---
name: my-skill
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
---
```

### The `once: true` Field

- Fires once per session, then auto-removes
- **Skills only** — not supported in `.claude/settings.json` or agent hooks
- Useful for one-time setup checks, session initialization validation

### Scoping Rules

- Hooks activate when the skill loads and deactivate when it unloads
- Multiple skills can register hooks for the same event (all fire in order)
- Skill hooks run AFTER global hooks (from settings.json)

### Known Issue

Skill-scoped hooks don't fire when the skill is loaded via a plugin/MCP server (GitHub Issue #17688). Workaround: define the hook in `.claude/settings.json` instead.

</skill_scoped_hooks>

<decision_tree>
```
Is the check simple and deterministic?
  YES --> type: "command"

Does it require a single LLM judgment ("is this safe?")?
  YES --> type: "prompt" (default model: Haiku)

Does it need multi-step verification (read files, grep patterns, reason)?
  YES --> type: "agent" (Read/Grep/Glob, up to 50 turns)

Is it just logging or formatting?
  YES --> type: "command"
```
</decision_tree>
</hook_anatomy>

<matchers>
Matchers filter which tools trigger the hook:

```json
{
  "matcher": "Bash",           // Exact match
  "matcher": "Write|Edit",     // Multiple tools (regex OR)
  "matcher": "mcp__.*",        // All MCP tools
  "matcher": "mcp__memory__.*" // Specific MCP server
}
```

**No matcher = fires for all tools:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [...]  // No matcher - fires on every tool
      }
    ]
  }
}
```

<common_matchers>
| Pattern | Matches |
|---------|---------|
| `Bash` | Bash tool only |
| `Write\|Edit` | Write OR Edit |
| `Read\|Write\|Edit` | Any file operation |
| `mcp__.*` | All MCP tools |
| `mcp__github__.*` | GitHub MCP tools |
| `Grep\|Glob` | Search tools |
</common_matchers>
</matchers>

<input_output_schemas>
<common_input_fields>
All hooks receive:

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```
</common_input_fields>

<pretooluse_input>
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies"
  }
}
```
</pretooluse_input>

<posttooluse_input>
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "..."
  },
  "tool_output": "File created successfully"
}
```
</posttooluse_input>

<blocking_output>
For PreToolUse, UserPromptSubmit, Stop:

**Command hooks — PreToolUse** (`type: "command"`):
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Explanation"
  },
  "updatedInput": { "command": "modified" }
}
```

> Top-level `decision`/`reason` are deprecated for PreToolUse. Use `hookSpecificOutput` instead.

**Command hooks — Stop, UserPromptSubmit** (`type: "command"`):
```json
{
  "decision": "block",
  "reason": "Explanation",
  "systemMessage": "Message to user"
}
```

**Prompt and agent hooks** (`type: "prompt"` or `type: "agent"`):
```json
{
  "ok": true
}
// or
{
  "ok": false,
  "reason": "Explanation of why the action was blocked"
}
```
</blocking_output>

<sessionstart_output>
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context to inject"
  }
}
```
</sessionstart_output>
</input_output_schemas>

<environment_variables>
Available in hook commands:

| Variable | Value |
|----------|-------|
| `$CLAUDE_PROJECT_DIR` | Project root directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory (plugin hooks only) |
| `$ARGUMENTS` | Hook input JSON (prompt hooks only) |
| `$cwd` | Current working directory |

**Example:**
```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.sh"
}
```
</environment_variables>

<common_patterns>
<desktop_notification>
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```
</desktop_notification>

<log_bash_commands>
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```
</log_bash_commands>

<block_destructive_commands>
Create `check-safety.sh`:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

if [[ "$command" == *"rm -rf /"* ]] || \
   [[ "$command" == *"git push"*"--force"*"main"* ]]; then
  echo '{"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "Destructive command detected"}}'
  exit 0
fi

echo '{"hookSpecificOutput": {"permissionDecision": "allow", "permissionDecisionReason": "Command is safe"}}'
```

Hook config:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-safety.sh"
          }
        ]
      }
    ]
  }
}
```
</block_destructive_commands>

<auto_format_code>
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$(cat | jq -r '.tool_input.file_path')\" 2>/dev/null || true",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```
</auto_format_code>

<load_sprint_context>
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat $CLAUDE_PROJECT_DIR/.sprint-context.txt | jq -Rs '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": .}}'"
          }
        ]
      }
    ]
  }
}
```
</load_sprint_context>

<verify_tests_before_stop>
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm test > /dev/null 2>&1 && echo '{\"decision\": \"approve\"}' || echo '{\"decision\": \"block\", \"reason\": \"Tests failing\"}'"
          }
        ]
      }
    ]
  }
}
```
</verify_tests_before_stop>

<chain_multiple_hooks>
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'First hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "command",
            "command": "echo 'Second hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "prompt",
            "prompt": "Final validation: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

Hooks execute in order. First block stops the chain.
</chain_multiple_hooks>
</common_patterns>

<troubleshooting>
<hooks_not_triggering>
1. Validate JSON: `jq . .claude/hooks.json`
2. Check matcher pattern matches tool name exactly
3. Verify file location (project vs user)
4. Test with `claude --debug`
</hooks_not_triggering>

<command_not_executing>
1. Check script has execute permission: `chmod +x script.sh`
2. Use absolute paths or `$CLAUDE_PROJECT_DIR`
3. Check timeout isn't too short
4. Verify command works standalone
</command_not_executing>

<infinite_loop_in_stop>
Always check `stop_hook_active`:

```bash
input=$(cat)
if [ "$(echo "$input" | jq -r '.stop_hook_active')" = "true" ]; then
  echo '{}'  # Empty object = no decision, allow stop
  exit 0
fi
```
</infinite_loop_in_stop>

<prompt_hook_issues>
1. Ensure prompt instructs JSON output format
2. Check `$ARGUMENTS` placeholder is present
3. Keep prompts clear and specific
4. Test prompt manually first
</prompt_hook_issues>
</troubleshooting>

<security_checklist>
**Critical safety requirements:**

- [ ] **Infinite loop prevention:** Check `stop_hook_active` in Stop hooks
- [ ] **Timeout configuration:** Set reasonable timeouts (default: 60s)
- [ ] **Permission validation:** Ensure scripts have `chmod +x`
- [ ] **Path safety:** Use absolute paths with `$CLAUDE_PROJECT_DIR`
- [ ] **JSON validation:** Validate config with `jq` before use
- [ ] **Selective blocking:** Be conservative to avoid workflow disruption

**Testing protocol:**
```bash
# Always test with debug flag first
claude --debug

# Validate JSON config
jq . .claude/hooks.json
```
</security_checklist>

<success_criteria>
A working hook configuration has:

- Valid JSON in `.claude/hooks.json`
- Appropriate hook event for the use case
- Correct matcher pattern
- Command/prompt executes without errors
- Proper output schema for blocking hooks
- Tested with `--debug` flag
- No infinite loops in Stop hooks
- Reasonable timeouts set
- Executable permissions on scripts
</success_criteria>
