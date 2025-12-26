<overview>
Slash commands are reusable prompts triggered with `/command-name` syntax. They expand as prompts in the current conversation, allowing standardized workflows and operations. This reference covers command structure, arguments, and patterns.
</overview>

<table_of_contents>
1. Quick Start
2. File Structure
3. YAML Frontmatter
4. XML Body Structure
5. Arguments
6. Dynamic Context
7. File References
8. Tool Restrictions
9. Common Patterns
10. Anti-Patterns
</table_of_contents>

<quick_start>
<workflow>
1. Create `.claude/commands/` directory (project) or `~/.claude/commands/` (personal)
2. Create `command-name.md` file
3. Add YAML frontmatter (at minimum: `description`)
4. Write command prompt with XML structure
5. Test with `/command-name [args]`
</workflow>

<minimal_example>
**File:** `.claude/commands/optimize.md`

```markdown
---
description: Analyze code for performance issues and suggest optimizations
---

<objective>
Analyze code performance and suggest three specific optimizations.
</objective>

<process>
1. Review code in current context
2. Identify bottlenecks
3. Suggest three optimizations with rationale
</process>

<success_criteria>
- Performance issues identified
- Three concrete optimizations suggested
- Implementation guidance provided
</success_criteria>
```

**Usage:** `/optimize`
</minimal_example>
</quick_start>

<file_structure>
| Type | Location | Scope |
|------|----------|-------|
| **Project** | `.claude/commands/` | Shared via version control |
| **Personal** | `~/.claude/commands/` | Available across all projects |

**File naming:** `command-name.md` invoked as `/command-name`
</file_structure>

<yaml_frontmatter>
<required_field name="description">
```yaml
description: Clear description of what the command does
```

Shown in `/help` command list.
</required_field>

<optional_field name="argument-hint">
```yaml
argument-hint: [issue-number]
argument-hint: <pr-number> <priority> <assignee>
```

Helps users understand expected arguments.
</optional_field>

<optional_field name="allowed-tools">
Restricts which tools Claude can use:

```yaml
# Array format
allowed-tools: [Read, Edit, Write]

# Single tool
allowed-tools: SequentialThinking

# Bash restrictions
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

If omitted: All tools available.
</optional_field>

<complete_example>
```yaml
---
name: example-command
description: Does something useful
argument-hint: [input]
allowed-tools: Read, Edit, Bash(npm test:*)
---
```
</complete_example>
</yaml_frontmatter>

<xml_structure>
<required_tags>
Every command should have:

**`<objective>`** - What and why
```xml
<objective>
What needs to happen and why this matters.
Context about who uses this and what it accomplishes.
</objective>
```

**`<process>` or `<steps>`** - How to execute
```xml
<process>
1. First step
2. Second step
3. Final step
</process>
```

**`<success_criteria>`** - How to know it succeeded
```xml
<success_criteria>
Clear, measurable criteria for successful completion.
</success_criteria>
```
</required_tags>

<conditional_tags>
Add based on complexity:

**`<context>`** - When loading dynamic state
```xml
<context>
Current state: ! `git status`
Relevant files: @ package.json
</context>
```
(Remove space after @ and ! in actual usage)

**`<verification>`** - When producing artifacts
```xml
<verification>
Before completing, verify:
- Tests pass
- No lint errors
</verification>
```

**`<testing>`** - When running tests
```xml
<testing>
Run tests: ! `npm test`
Check lint: ! `npm run lint`
</testing>
```

**`<output>`** - When creating files
```xml
<output>
Files created/modified:
- `./path/to/file.ext` - Description
</output>
```
</conditional_tags>

<complexity_guidance>
**Simple commands** (single operation):
- Required tags only: objective, process, success_criteria

**Complex commands** (multi-step, artifacts):
- Required tags + context, verification, output as needed
</complexity_guidance>
</xml_structure>

<arguments>
<all_arguments>
Use `$ARGUMENTS` for all arguments as single string:

```markdown
---
description: Fix issue following coding standards
---

<objective>
Fix issue #$ARGUMENTS following project conventions.
</objective>
```

**Usage:** `/fix-issue 123 high-priority`
**Claude receives:** "Fix issue #123 high-priority following project conventions."
</all_arguments>

<positional_arguments>
Use `$1`, `$2`, `$3` for structured input:

```markdown
---
description: Review PR with priority and assignee
argument-hint: <pr-number> <priority> <assignee>
---

<objective>
Review PR #$1 with priority $2 and assign to $3.
</objective>
```

**Usage:** `/review-pr 456 high alice`
- `$1` = `456`
- `$2` = `high`
- `$3` = `alice`
</positional_arguments>

<when_to_use_arguments>
**Commands that need arguments:**
- `/fix-issue [issue-number]` - Needs issue number
- `/review-pr [pr-number]` - Needs PR number
- `/optimize [file-path]` - Needs file to optimize

**Commands without arguments:**
- `/check-todos` - Operates on known file
- `/first-principles` - Operates on current conversation
- `/whats-next` - Analyzes current context
</when_to_use_arguments>

<incorporating_arguments>
**In `<objective>`:**
```xml
<objective>
Fix issue #$ARGUMENTS following project conventions.
</objective>
```

**In `<process>`:**
```xml
<process>
1. Understand issue #$ARGUMENTS from issue tracker
2. Locate relevant code
3. Implement fix
</process>
```

**In `<context>`:**
```xml
<context>
Issue details: @ issues/$ARGUMENTS.md
Related files: ! `grep -r "TODO.*$ARGUMENTS" src/`
</context>
```
(Remove space after @ and ! in actual usage)
</incorporating_arguments>
</arguments>

<dynamic_context>
Execute bash commands before the prompt using exclamation mark prefix:

**Note:** Examples show space after `!` to prevent execution during loading. Remove space in actual commands.

```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

<context>
- Current git status: ! `git status`
- Current git diff: ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`
</context>

<objective>
Create a git commit based on the above changes.
</objective>
```

Bash commands execute and output is included in the expanded prompt.
</dynamic_context>

<file_references>
Use `@` prefix to reference files:

**Note:** Examples show space after `@` to prevent loading during skill read.

```markdown
<context>
Review the implementation in @ src/utils/helpers.js
Check dependencies in @ package.json
</context>
```

Claude can access the referenced file's contents.

**Dynamic file reference:**
```markdown
<objective>
Review the implementation in @ $ARGUMENTS
</objective>
```

**Usage:** `/review src/app.js`
</file_references>

<tool_restrictions>
<git_commands>
```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

Prevents running arbitrary bash commands.
</git_commands>

<analysis_only>
```yaml
allowed-tools: [Read, Grep, Glob]
```

No write or execution permissions.
</analysis_only>

<thinking_only>
```yaml
allowed-tools: SequentialThinking
```

Only allows sequential thinking tool.
</thinking_only>

<specific_npm>
```yaml
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
```

Only allows specific npm scripts.
</specific_npm>
</tool_restrictions>

<common_patterns>
<git_commit>
```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

<objective>
Create a git commit for current changes following repository conventions.
</objective>

<context>
- Current status: ! `git status`
- Changes: ! `git diff HEAD`
- Recent commits: ! `git log --oneline -5`
</context>

<process>
1. Review staged and unstaged changes
2. Stage relevant files
3. Write commit message following recent commit style
4. Create commit
</process>

<success_criteria>
- All relevant changes staged
- Commit message follows repository conventions
- Commit created successfully
</success_criteria>
```
</git_commit>

<fix_issue>
```markdown
---
description: Fix issue following coding standards
argument-hint: [issue-number]
---

<objective>
Fix issue #$ARGUMENTS following project coding standards.
</objective>

<process>
1. Understand the issue described in ticket #$ARGUMENTS
2. Locate the relevant code
3. Implement a solution that addresses root cause
4. Add appropriate tests
5. Verify fix resolves the issue
</process>

<success_criteria>
- Issue fully understood and addressed
- Solution follows coding standards
- Tests added and passing
- No regressions introduced
</success_criteria>
```
</fix_issue>

<security_review>
```markdown
---
description: Review code for security vulnerabilities
---

<objective>
Review code for security vulnerabilities and suggest fixes.
</objective>

<process>
1. Scan code for common vulnerabilities (XSS, SQL injection, etc.)
2. Identify specific issues with line numbers
3. Assess severity of each vulnerability
4. Suggest remediation for each issue
</process>

<success_criteria>
- All major vulnerability types checked
- Specific issues identified with locations
- Severity levels assigned
- Actionable fixes provided
</success_criteria>
```
</security_review>

<file_optimization>
```markdown
---
description: Optimize specific file
argument-hint: [file-path]
---

<objective>
Analyze performance of @ $ARGUMENTS and suggest three optimizations.
</objective>

<process>
1. Review code in @ $ARGUMENTS
2. Identify bottlenecks and inefficiencies
3. Suggest three optimizations with rationale
4. Estimate performance impact
</process>

<success_criteria>
- File analyzed thoroughly
- Three concrete optimizations suggested
- Implementation guidance provided
</success_criteria>
```
(Remove space after @ in actual usage)
</file_optimization>

<first_principles>
```markdown
---
description: Analyze problem from first principles
allowed-tools: SequentialThinking
---

<objective>
Analyze the current problem from first principles.
</objective>

<process>
1. Identify the core problem
2. Strip away all assumptions
3. Identify fundamental truths and constraints
4. Rebuild solution from first principles
5. Compare with current approach
</process>

<success_criteria>
- Problem analyzed from ground up
- Assumptions identified and questioned
- Solution rebuilt from fundamentals
- Novel insights discovered
</success_criteria>
```
</first_principles>

<compare_files>
```markdown
---
description: Compare two files
argument-hint: <file1> <file2>
---

<objective>
Compare @ $1 with @ $2 and highlight key differences.
</objective>

<process>
1. Read @ $1 and @ $2
2. Identify structural differences
3. Compare functionality and logic
4. Highlight key changes
5. Assess impact
</process>

<success_criteria>
- Both files analyzed
- Key differences identified
- Impact of changes assessed
</success_criteria>
```
(Remove space after @ in actual usage)
</compare_files>
</common_patterns>

<anti_patterns>
<no_description>
```yaml
---
# Missing description field - BAD
---
```
</no_description>

<broad_tool_access>
```yaml
# Git command with no restrictions - BAD
---
description: Create commit
---
```

**Better:**
```yaml
---
description: Create commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```
</broad_tool_access>

<vague_instructions>
```markdown
Do the thing for $ARGUMENTS
```

**Better:**
```markdown
<objective>
Fix issue #$ARGUMENTS by implementing a solution.
</objective>

<process>
1. Understanding the issue
2. Locating relevant code
3. Implementing solution
4. Adding tests
</process>
```
</vague_instructions>

<missing_context>
```markdown
Create a git commit
```

**Better:**
```markdown
<context>
Current changes: ! `git status`
Diff: ! `git diff`
</context>

Create a git commit for these changes
```
</missing_context>

<markdown_headings>
```markdown
## Objective
Do something

## Process
1. Step 1
```

**Better:**
```xml
<objective>
Do something
</objective>

<process>
1. Step 1
</process>
```
</markdown_headings>
</anti_patterns>

<success_criteria>
A well-structured slash command has:

**YAML Frontmatter:**
- `description` field is clear and concise
- `argument-hint` present if command accepts arguments
- `allowed-tools` specified if tool restrictions needed

**XML Structure:**
- Required tags: `<objective>`, `<process>`, `<success_criteria>`
- Conditional tags used appropriately
- No markdown headings in body
- All XML tags properly closed

**Arguments:**
- `$ARGUMENTS` used for user-specified data
- Positional arguments for structured input
- No `$ARGUMENTS` for self-contained commands

**Functionality:**
- Command expands correctly when invoked
- Dynamic context loads properly
- Tool restrictions prevent unauthorized operations
- Command accomplishes intended purpose
</success_criteria>
