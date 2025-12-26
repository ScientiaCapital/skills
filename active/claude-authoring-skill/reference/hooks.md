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
| Event | When It Fires | Can Block? |
|-------|---------------|------------|
| **PreToolUse** | Before tool execution | Yes |
| **PostToolUse** | After tool execution | No |
| **UserPromptSubmit** | User submits a prompt | Yes |
| **Stop** | Claude attempts to stop | Yes |
| **SubagentStop** | Subagent attempts to stop | Yes |
| **SessionStart** | Session begins | No |
| **SessionEnd** | Session ends | No |
| **PreCompact** | Before context compaction | Yes |
| **Notification** | Claude needs input | No |

<pretooluse>
**Purpose:** Validate, modify, or block tool calls before execution.

**Use cases:**
- Block destructive commands (rm -rf, force push)
- Validate commit message format
- Add flags to commands (--save-exact)
- Log command attempts

**Example - Block force push to main:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this command is safe: $ARGUMENTS\n\nBlock if: force push to main/master\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
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
  "decision": "approve" | "block",
  "reason": "Explanation",
  "updatedInput": { "command": "modified command" }
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
**Output:** JSON with `decision` and `reason`

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
}
```
</prompt_hooks>

<decision_tree>
```
Is the check simple and deterministic?
  YES --> Command hook

Does it require natural language understanding?
  YES --> Prompt hook

Does it need to inspect code semantics?
  YES --> Prompt hook

Is it just logging or formatting?
  YES --> Command hook
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

```json
{
  "decision": "approve" | "block",
  "reason": "Explanation",
  "systemMessage": "Message to user",
  "updatedInput": { "command": "modified" }
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
  echo '{"decision": "block", "reason": "Destructive command detected"}'
  exit 0
fi

echo '{"decision": "approve", "reason": "Command is safe"}'
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
  echo '{"decision": undefined}'
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
