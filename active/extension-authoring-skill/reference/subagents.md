<overview>
Subagents are specialized Claude instances that run in isolated contexts with focused roles and limited tool access. They execute autonomously without user interaction, returning final output to the main conversation. This reference covers configuration, execution model, and best practices.
</overview>

<table_of_contents>
1. Quick Start
2. File Structure
3. Configuration Fields
4. Execution Model (Critical)
5. System Prompt Guidelines
6. XML Structure
7. Model Selection
8. Tool Security
9. Example Subagents
10. Anti-Patterns
11. Testing and Validation
</table_of_contents>

<quick_start>
<workflow>
1. Run `/agents` command
2. Select "Create New Agent"
3. Choose project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)
4. Define the subagent:
   - **name**: lowercase-with-hyphens
   - **description**: When should this subagent be used?
   - **tools**: Optional comma-separated list
   - **model**: Optional (`sonnet`, `opus`, `haiku`, or `inherit`)
5. Write the system prompt
</workflow>

<minimal_example>
```markdown
---
name: code-reviewer
description: Reviews code for quality and security. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior code reviewer focused on quality and security.
</role>

<workflow>
1. Read modified files
2. Identify issues
3. Provide specific feedback with file:line references
</workflow>

<constraints>
- NEVER modify code, only review
- ALWAYS provide actionable feedback
</constraints>
```
</minimal_example>
</quick_start>

<file_structure>
| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project** | `.claude/agents/` | Current project only | Highest |
| **User** | `~/.claude/agents/` | All projects | Lower |
| **Plugin** | Plugin's `agents/` dir | All projects | Lowest |

When names conflict, higher priority takes precedence.
</file_structure>

<configuration_fields>
<field name="name">
- Lowercase letters and hyphens only
- Must be unique
- Matches filename: `code-reviewer.md`
</field>

<field name="description">
- Natural language description of purpose
- Include **when** Claude should invoke this subagent
- Used for automatic subagent selection

**Good:**
```yaml
description: Reviews code for security vulnerabilities. Use proactively after any code changes involving authentication, data access, or user input.
```

**Bad:**
```yaml
description: Helps with code
```
</field>

<field name="tools">
- Comma-separated list: `Read, Write, Edit, Bash, Grep`
- If omitted: inherits all tools from main thread
- Use `/agents` to see available tools

```yaml
tools: Read, Grep, Glob, Bash
```
</field>

<field name="model">
| Value | Usage |
|-------|-------|
| `sonnet` | Planning, complex reasoning, validation |
| `opus` | Highest-stakes decisions |
| `haiku` | Task execution, simple transformations |
| `inherit` | Same model as main conversation |

If omitted: defaults to configured subagent model (usually sonnet)
</field>
</configuration_fields>

<execution_model>
<critical_constraint>
**Subagents are black boxes that cannot interact with users.**

Subagents run in isolated contexts and return only final output:
- User only sees subagent's final report/output
- User never sees intermediate steps, tool calls, or reasoning
- Subagent cannot pause and wait for user input
</critical_constraint>

<can_and_cannot>
**Subagents CAN:**
- Use Read, Write, Edit, Bash, Grep, Glob
- Access MCP servers (non-interactive tools)
- Make decisions based on prompt and data
- Execute multi-step autonomous workflows

**Subagents CANNOT:**
- Use AskUserQuestion
- Present options and wait for selection
- Request confirmations or clarifications
- Show progress to user during execution
</can_and_cannot>

<workflow_design>
**Keep user interaction in main chat:**

```
Main Chat: Gather requirements (AskUserQuestion)
    |
    v
Subagent: Research/build based on requirements (no interaction)
    |
    v
Main Chat: Present results to user, get confirmation
    |
    v
Subagent: Generate code based on confirmed plan
    |
    v
Main Chat: Present results, handle testing/deployment
```

**Use main chat for:**
- Gathering requirements from user
- Presenting options or decisions
- Any task requiring user confirmation
- Work where user needs visibility into progress

**Use subagents for:**
- Research tasks (documentation lookup, code analysis)
- Code generation based on pre-defined requirements
- Analysis and reporting (security review, test coverage)
- Context-heavy operations without user interaction
</workflow_design>
</execution_model>

<system_prompt_guidelines>
<principle name="be_specific">
Define exactly what the subagent does:

**Bad:**
```markdown
You are a helpful coding assistant.
```

**Good:**
```markdown
You are a React performance optimizer. Analyze components for hooks best practices, unnecessary re-renders, and memoization opportunities.
```
</principle>

<principle name="pure_xml_structure">
Remove ALL markdown headings from body. Use semantic XML tags:

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior security engineer specializing in web application security.
</role>

<focus_areas>
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication/authorization issues
</focus_areas>

<workflow>
1. Read the modified files
2. Identify security risks
3. Provide specific remediation steps
4. Rate severity (Critical/High/Medium/Low)
</workflow>
```
</principle>

<principle name="strong_constraints">
Use modal verbs (MUST, NEVER, ALWAYS) for critical boundaries:

```markdown
<constraints>
- NEVER modify production code, ONLY test files
- MUST verify tests pass before completing
- ALWAYS include edge case coverage
- DO NOT run tests without explicit request
</constraints>
```
</principle>

<principle name="clear_output_format">
Define expected deliverable structure:

```markdown
<output_format>
For each issue found:
1. **Severity**: [Critical/High/Medium/Low]
2. **Location**: [File:LineNumber]
3. **Vulnerability**: [Type and description]
4. **Risk**: [What could happen]
5. **Fix**: [Specific code changes needed]
</output_format>
```
</principle>
</system_prompt_guidelines>

<xml_structure>
<recommended_tags>
| Tag | Purpose |
|-----|---------|
| `<role>` | Who the subagent is and what it does |
| `<constraints>` | Hard rules (NEVER/MUST/ALWAYS) |
| `<focus_areas>` | What to prioritize |
| `<workflow>` | Step-by-step process |
| `<output_format>` | How to structure deliverables |
| `<success_criteria>` | Completion criteria |
| `<validation>` | How to verify work |
</recommended_tags>

<complexity_guidance>
**Simple subagents** (single focused task):
- role + constraints + workflow minimum
- Example: code-reviewer, test-runner

**Medium subagents** (multi-step process):
- Add workflow steps, output_format, success_criteria
- Example: api-researcher, documentation-generator

**Complex subagents** (research + generation + validation):
- Add all tags including validation, examples
- Example: mcp-api-researcher, comprehensive-auditor
</complexity_guidance>
</xml_structure>

<model_selection>
<model_capabilities>
**Sonnet 4.5** (`sonnet`):
- Best for agentic tasks: 64% on coding benchmarks
- SWE-bench Verified: 49.0%
- Use for: Planning, complex reasoning, validation

**Haiku 4.5** (`haiku`):
- 90% of Sonnet's capabilities, fastest and cheapest
- SWE-bench Verified: 73.3%
- Use for: Task execution, simple transformations, high-volume

**Opus** (`opus`):
- Highest performance on evaluation benchmarks
- Most capable but slowest and most expensive
- Use for: Highest-stakes decisions, most complex reasoning
</model_capabilities>

<orchestration_pattern>
**Sonnet + Haiku pattern** (optimal cost/performance):

```
1. Sonnet (Coordinator):
   - Creates plan
   - Breaks task into subtasks
   - Identifies parallelizable work

2. Multiple Haiku (Workers):
   - Execute subtasks in parallel
   - Fast and cost-efficient
   - 90% of Sonnet's capability

3. Sonnet (Validator):
   - Integrates results
   - Validates output quality
   - Ensures coherence
```

Use expensive Sonnet for planning/validation, cheap Haiku for execution.
</orchestration_pattern>

<decision_framework>
| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Simple validation | Haiku | Fast, cheap, sufficient |
| Code execution | Haiku | High SWE-bench, very fast |
| Complex analysis | Sonnet | Superior reasoning |
| Multi-step planning | Sonnet | Best for complexity |
| Quality validation | Sonnet | Critical checkpoint |
| Batch processing | Haiku | Cost efficiency |
| Critical security | Sonnet | High stakes |
</decision_framework>
</model_selection>

<tool_security>
<core_principle>
"Permission sprawl is the fastest path to unsafe autonomy."

Treat tool access like production IAM: start from deny-all, allowlist only what's needed.
</core_principle>

<patterns>
**Read-only analysis:**
```yaml
tools: Read, Grep, Glob
```

**Code modification:**
```yaml
tools: Read, Edit, Bash, Grep
```

**Test running:**
```yaml
tools: Read, Write, Bash
```
</patterns>

<audit_checklist>
- [ ] Does this subagent need Write/Edit, or is Read sufficient?
- [ ] Should it execute code (Bash), or just analyze?
- [ ] Are all granted tools necessary for the task?
- [ ] What's the worst-case misuse scenario?
- [ ] Can we restrict further without blocking legitimate use?
</audit_checklist>
</tool_security>

<example_subagents>
<test_writer>
```markdown
---
name: test-writer
description: Creates comprehensive test suites. Use when new code needs tests or test coverage is insufficient.
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---

<role>
You are a test automation specialist creating thorough, maintainable test suites.
</role>

<workflow>
1. Analyze the code to understand functionality
2. Identify test cases (happy path, edge cases, error conditions)
3. Write tests using the project's testing framework
4. Run tests to verify they pass
</workflow>

<quality_criteria>
- Test one behavior per test
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Include edge cases and error conditions
- Avoid test interdependencies
</quality_criteria>

<constraints>
- NEVER modify production code
- MUST run tests after writing them
- DO NOT create tests that depend on external services without mocking
</constraints>
```
</test_writer>

<debugger>
```markdown
---
name: debugger
description: Investigates and fixes bugs. Use when errors occur or behavior is unexpected.
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

<role>
You are a debugging specialist skilled at root cause analysis.
</role>

<methodology>
1. **Reproduce**: Understand and reproduce the issue
2. **Isolate**: Identify the failing component
3. **Analyze**: Examine code, logs, stack traces
4. **Hypothesize**: Form theories about cause
5. **Test**: Verify hypotheses systematically
6. **Fix**: Implement the solution
7. **Verify**: Confirm fix without side effects
</methodology>

<output_format>
1. **Root cause**: Clear explanation
2. **Why it happens**: Underlying reason
3. **Fix**: Specific code changes
4. **Verification**: How to confirm it's fixed
5. **Prevention**: How to avoid similar bugs
</output_format>

<constraints>
- Make minimal changes to fix the issue
- Preserve existing functionality
- Add tests to prevent regression
</constraints>
```
</debugger>

<security_reviewer>
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use after changes to authentication, data access, or user input.
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior security engineer specializing in web application security.
</role>

<focus_areas>
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting)
- Authentication/authorization flaws
- Sensitive data exposure
- CSRF (Cross-Site Request Forgery)
</focus_areas>

<workflow>
1. Run git diff to identify changes
2. Read modified files focusing on data flow
3. Identify security risks with severity ratings
4. Provide specific remediation steps
</workflow>

<severity_ratings>
- **Critical**: Immediate exploitation, high impact
- **High**: Exploitation likely, significant impact
- **Medium**: Exploitation requires conditions
- **Low**: Limited exploitability or impact
</severity_ratings>

<output_format>
For each issue:
1. **Severity**: [Critical/High/Medium/Low]
2. **Location**: [File:LineNumber]
3. **Vulnerability**: [Type and description]
4. **Risk**: [What could happen]
5. **Fix**: [Specific code changes]
</output_format>

<constraints>
- Focus only on security issues, not code style
- Provide actionable fixes, not vague warnings
- If no issues found, confirm review was completed
</constraints>
```
</security_reviewer>
</example_subagents>

<anti_patterns>
<pitfall name="too_generic">
**Bad:**
```markdown
You are a helpful assistant that helps with code.
```

No specialization. Subagent won't know what to focus on.
</pitfall>

<pitfall name="no_workflow">
**Bad:**
```markdown
You are a code reviewer. Review code for issues.
```

Without workflow, subagent may skip important steps.

**Good:**
```markdown
<workflow>
1. Run git diff to see changes
2. Read modified files
3. Check for: security issues, performance problems, code quality
4. Provide specific feedback with examples
</workflow>
```
</pitfall>

<pitfall name="unclear_trigger">
**Bad:**
```yaml
description: Helps with testing
```

**Good:**
```yaml
description: Creates comprehensive test suites. Use when new code needs tests or test coverage is insufficient. Proactively use after implementing new features.
```
</pitfall>

<pitfall name="missing_constraints">
Without constraints, subagents might:
- Modify code they shouldn't touch
- Run dangerous commands
- Skip important steps

Always include:
```markdown
<constraints>
- Only modify test files, never production code
- Always run tests after writing them
- Do not commit changes automatically
</constraints>
```
</pitfall>

<pitfall name="requires_user_interaction">
**Critical:** Subagents cannot interact with users.

**Bad:**
```markdown
---
name: intake-agent
description: Gathers requirements from user
tools: AskUserQuestion
---

<workflow>
1. Ask user about requirements using AskUserQuestion
2. Follow up with clarifying questions
</workflow>
```

This fails because subagents are black boxes.

**Correct approach:**
Move user interaction to main chat, use subagent for autonomous work.
</pitfall>

<pitfall name="markdown_headings">
**Bad:**
```markdown
## Role
You are a code reviewer.

## Workflow
1. Step 1
```

**Good:**
```xml
<role>
You are a code reviewer.
</role>

<workflow>
1. Step 1
</workflow>
```
</pitfall>
</anti_patterns>

<testing_and_validation>
<test_checklist>
1. Invoke the subagent with a representative task
2. Check if it follows the workflow specified
3. Verify output format matches definition
4. Test edge cases - unusual inputs
5. Check constraints - does it respect boundaries?
6. Iterate - refine prompt based on behavior
</test_checklist>

<common_issues>
| Issue | Solution |
|-------|----------|
| Subagent too broad | Narrow the focus areas |
| Skipping steps | Make workflow more explicit |
| Inconsistent output | Define output format more clearly |
| Overstepping bounds | Add or clarify constraints |
| Not automatically invoked | Improve description with trigger keywords |
</common_issues>
</testing_and_validation>

<invocation>
<automatic>
Claude automatically selects subagents based on:
- Task description in user's request
- `description` field in subagent configuration
- Current context
</automatic>

<explicit>
Users can explicitly request a subagent:

```
> Use the code-reviewer subagent to check my recent changes
> Have the test-writer subagent create tests for the new API endpoints
```
</explicit>

<management>
Run `/agents` for interactive management:
- View all available subagents
- Create new subagents
- Edit existing subagents
- Delete custom subagents
</management>
</invocation>

<success_criteria>
A well-configured subagent has:

- Valid YAML frontmatter (name matches file)
- Description includes triggers and when to use
- Clear role definition in system prompt
- Appropriate tool restrictions (least privilege)
- XML-structured prompt with role, workflow, constraints
- Model selection appropriate for task complexity
- Successfully tested on representative tasks
</success_criteria>
