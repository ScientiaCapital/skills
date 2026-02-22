<overview>
Skills are modular, filesystem-based capabilities that provide domain expertise on demand. This reference covers skill structure, patterns, and best practices.
</overview>

<table_of_contents>
1. File Structure
2. YAML Frontmatter
3. Required XML Tags
4. Conditional XML Tags
5. Skill-Scoped Hooks
6. Router Pattern
7. Progressive Disclosure
8. Templates and Patterns
9. Anti-Patterns
10. Validation Checklist
</table_of_contents>

<file_structure>
<simple_skill>
Single file for straightforward domain knowledge:

```
skill-name/
└── SKILL.md
```
</simple_skill>

<complex_skill>
Router pattern for multi-workflow skills:

```
skill-name/
├── SKILL.md              # Router + essential principles
├── workflows/            # Step-by-step procedures (FOLLOW)
├── references/           # Domain knowledge (READ)
├── templates/            # Output structures (COPY + FILL)
└── scripts/              # Reusable code (EXECUTE)
```

**When to use each folder:**
- **workflows/** - Multi-step procedures Claude follows sequentially
- **references/** - Domain knowledge Claude reads for context
- **templates/** - Consistent output structures (plans, specs, configs)
- **scripts/** - Executable code Claude runs as-is (deploy, setup, API calls)
</complex_skill>
</file_structure>

<yaml_frontmatter>
<required_fields>
```yaml
---
name: skill-name-here
description: What it does and when to use it (third person, specific triggers)
---
```
</required_fields>

<name_field>
**Validation rules:**
- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- No reserved words: "anthropic", "claude"
- Must match directory name exactly

**Good examples:**
- `process-pdfs`
- `manage-facebook-ads`
- `setup-stripe-payments`

**Bad examples:**
- `PDF_Processor` (uppercase)
- `helper` (vague)
- `claude-helper` (reserved word)
</name_field>

<description_field>
**Structure:** Include WHAT it does AND WHEN to use it.

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with documents
```

**Critical:** Always use third person.
- Good: "Processes Excel files and generates reports"
- Bad: "I can help you process Excel files"
</description_field>

<naming_conventions>
Use verb-noun convention:

| Pattern | Use Case | Examples |
|---------|----------|----------|
| `create-*` | Building/authoring tools | `create-agent-skills`, `create-hooks` |
| `manage-*` | External services | `manage-facebook-ads`, `manage-stripe` |
| `setup-*` | Configuration | `setup-stripe-payments`, `setup-meta-tracking` |
| `generate-*` | Generation tasks | `generate-ai-images` |
| `process-*` | Data processing | `process-pdfs`, `process-excel` |
</naming_conventions>

<invocation_control>
### `disable-model-invocation: true`

Prevents Claude from auto-invoking the skill. The skill description is NOT loaded into Claude's context, resulting in zero passive token cost.

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---
```

**Use for:** Destructive operations (deploy, delete), high-cost operations, side-effect-heavy workflows.

Only the user can invoke via `/skill-name`. The full skill body loads on manual invocation.

### Invocation Control Matrix

| Frontmatter | User invokes | Claude invokes | Context cost |
|-------------|-------------|----------------|--------------|
| _(default)_ | Yes | Yes | Description always loaded |
| `disable-model-invocation: true` | Yes | No | Zero until invoked |
| `user-invocable: false` | No | Yes | Description always loaded |
</invocation_control>

<additional_frontmatter_fields>
### Complete Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Lowercase, hyphens, max 64 chars |
| `description` | Recommended | What the skill does + when to use it |
| `argument-hint` | No | Autocomplete hint shown in `/` menu, e.g. `[issue-number]` |
| `disable-model-invocation` | No | `true` = manual-only via `/name` |
| `user-invocable` | No | `false` = hidden from `/` menu |
| `allowed-tools` | No | Restrict tools when skill is active (comma-separated) |
| `model` | No | Override model when skill is active (e.g. `haiku`, `sonnet`) |
| `context` | No | `fork` = run in isolated subagent |
| `agent` | No | Subagent type for `context: fork` (e.g. `Explore`, `Plan`) |
| `hooks` | No | Skill-scoped lifecycle hooks (see hooks reference) |

### `context: fork`

Runs the skill in an isolated subagent rather than the main conversation. The subagent gets its own context window but can use tools.

```yaml
---
name: research-topic
description: Deep research on a topic
context: fork
agent: Explore
---
```

**Important:** When using `context: fork`, the skill body should contain explicit task instructions (not just guidelines), since the subagent starts fresh without conversation context.

### `allowed-tools`

Restricts which tools Claude can use while the skill is active:

```yaml
---
name: read-only-audit
description: Audit codebase without modifications
allowed-tools: Read, Grep, Glob
---
```

### String Substitution Variables

These variables expand dynamically in the skill body:

| Variable | Expands to |
|----------|------------|
| `$ARGUMENTS` | Full argument string after `/skill-name` |
| `$ARGUMENTS[N]` | Nth space-delimited argument (0-indexed) |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session UUID |

**Example:**
```yaml
---
name: review-pr
argument-hint: [pr-number]
---
Review PR #$ARGUMENTS[0] using gh pr view $ARGUMENTS[0].
```

### Dynamic Context Injection

Load external content into a skill at runtime using `` !`command` `` syntax:

```
!`git log --oneline -5`
```

The command runs when the skill loads and its stdout replaces the directive.
</additional_frontmatter_fields>
</yaml_frontmatter>

<required_tags>
Every skill MUST have these three tags:

<tag name="objective">
**Purpose:** What the skill does and why it matters.

```xml
<objective>
Extract text and tables from PDF files, fill forms, and merge documents using Python libraries. This skill provides patterns for common PDF operations without external services.
</objective>
```
</tag>

<tag name="quick_start">
**Purpose:** Immediate, actionable guidance. Minimal working example.

```xml
<quick_start>
Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
</quick_start>
```
</tag>

<tag name="success_criteria">
**Purpose:** How to know the task worked.

```xml
<success_criteria>
A well-structured skill has:

- Valid YAML frontmatter with descriptive name and description
- Pure XML structure with no markdown headings in body
- Required tags: objective, quick_start, success_criteria
- Progressive disclosure (SKILL.md < 500 lines)
- Real-world testing
</success_criteria>
```
</tag>
</required_tags>

<conditional_tags>
Add based on skill complexity:

| Tag | When to Use |
|-----|-------------|
| `<context>` | Background information before starting |
| `<workflow>` or `<process>` | Step-by-step procedures |
| `<advanced_features>` | Deep-dive topics (progressive disclosure) |
| `<validation>` | Verification steps or quality checks |
| `<examples>` | Multi-shot learning, input/output pairs |
| `<anti_patterns>` | Common mistakes to avoid |
| `<security_checklist>` | API keys, payments, authentication |
| `<testing>` | Testing workflows |
| `<common_patterns>` | Code examples and recipes |
| `<reference_guides>` | Links to reference files |

<tag_selection_intelligence>
**Simple skills** (single domain): Required tags only
**Medium skills** (multiple patterns): Required + workflow/examples
**Complex skills** (security, APIs): Required + conditional as appropriate
</tag_selection_intelligence>
</conditional_tags>

<skill_scoped_hooks>
### Skill-Scoped Hooks

Skills can define hooks directly in their YAML frontmatter. These hooks are active only while the skill is loaded.

```yaml
---
name: my-skill
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/lint-check.sh"
          once: true
---
```

- `once: true` — fires once per session, then auto-removes (skills only)
- Skill hooks run after global hooks from settings.json
- See [hooks reference](../reference/hooks.md) for full hook documentation
</skill_scoped_hooks>

<router_pattern>
For skills with multiple workflows, use the router pattern:

<skill_md_structure>
```xml
<essential_principles>
Core principles that always apply (can't be skipped)
</essential_principles>

<intake>
What would you like to do?

1. Option 1
2. Option 2
3. Option 3

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action |
|----------|-------------|
| 1 | Read workflows/option-1.md |
| 2 | Read workflows/option-2.md |
| 3 | Read workflows/option-3.md |

**After reading the workflow, follow it exactly.**
</routing>
```
</skill_md_structure>

<workflow_structure>
```xml
<required_reading>
Before starting, read:
- references/domain-knowledge.md
</required_reading>

<process>
1. Step 1
2. Step 2
3. Step 3
</process>

<success_criteria>
Done when:
- Criterion 1 met
- Criterion 2 met
</success_criteria>
```
</workflow_structure>
</router_pattern>

<progressive_disclosure>
Keep token usage proportional to task complexity:

<principle>
- Simple task: Load SKILL.md only (~500 tokens)
- Medium task: Load SKILL.md + one reference (~1000 tokens)
- Complex task: Load SKILL.md + multiple references (~2000 tokens)
</principle>

<implementation>
- Keep SKILL.md under 500 lines
- Split detailed content into reference files
- Keep references one level deep from SKILL.md
- Add table of contents to files over 100 lines
- Link to references from relevant sections
</implementation>

<pattern_example>
```xml
<quick_start>
<creating_documents>
Use docx-js for new documents. See [docx-js.md](docx-js.md).
</creating_documents>

<editing_documents>
For simple edits, modify XML directly.

**For tracked changes**: See [redlining.md](redlining.md)
**For OOXML details**: See [ooxml.md](ooxml.md)
</editing_documents>
</quick_start>
```

Claude reads redlining.md or ooxml.md only when needed.
</pattern_example>
</progressive_disclosure>

<templates_and_patterns>
<template_pattern>
Provide templates for output format:

**Strict (compliance, automated processing):**
```xml
<report_structure>
ALWAYS use this exact template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1
- Finding 2

## Recommendations
1. Recommendation 1
2. Recommendation 2
```
</report_structure>
```

**Flexible (exploratory, context-dependent):**
```xml
<report_structure>
Sensible default format, adapt as needed:
...
</report_structure>
```
</template_pattern>

<examples_pattern>
For multi-shot learning:

```xml
<examples>
<example number="1">
<input>Added user authentication</input>
<output>feat(auth): implement JWT-based authentication</output>
</example>

<example number="2">
<input>Fixed date display bug</input>
<output>fix(reports): correct date formatting</output>
</example>
</examples>
```
</examples_pattern>

<default_with_escape_hatch>
Provide ONE default, not a menu:

**Good:**
```xml
<quick_start>
Use pdfplumber for text extraction:

```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
</quick_start>
```

**Bad:**
```xml
<quick_start>
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...
</quick_start>
```
</default_with_escape_hatch>
</templates_and_patterns>

<anti_patterns>
<pitfall name="markdown_headings_in_body">
**Bad:**
```markdown
## Quick start
Extract text...
```

**Good:**
```xml
<quick_start>
Extract text...
</quick_start>
```
</pitfall>

<pitfall name="vague_descriptions">
Bad: `description: Helps with documents`
Good: `description: Extract text from PDF files. Use when processing PDFs.`
</pitfall>

<pitfall name="inconsistent_pov">
Bad: `description: I can help you process files`
Good: `description: Processes files for analysis`
</pitfall>

<pitfall name="deeply_nested_references">
Bad: `SKILL.md --> advanced.md --> details.md --> examples.md`
Good: Keep references one level deep from SKILL.md
</pitfall>

<pitfall name="windows_paths">
Bad: `scripts\helper.py`
Good: `scripts/helper.py`
</pitfall>

<pitfall name="unclosed_tags">
Always close XML tags properly:

```xml
<objective>
Content here
</objective>
```
</pitfall>

<pitfall name="dynamic_context_execution">
When showing examples of `!`backticks` or `@file` syntax in documentation, add a space to prevent execution during skill loading:

```xml
<examples>
Load status: ! `git status` (remove space in actual usage)
</examples>
```
</pitfall>
</anti_patterns>

<validation_checklist>
Before finalizing a skill:

- [ ] YAML frontmatter valid (name matches directory, description in third person)
- [ ] No markdown headings in body (pure XML structure)
- [ ] Required tags present: objective, quick_start, success_criteria
- [ ] Conditional tags appropriate for complexity level
- [ ] All XML tags properly closed
- [ ] Progressive disclosure applied (SKILL.md < 500 lines)
- [ ] Reference files use pure XML structure
- [ ] File paths use forward slashes
- [ ] Descriptive file names
- [ ] Tested with real usage
</validation_checklist>

<degrees_of_freedom>
Match specificity to task fragility:

| Task Type | Freedom Level | Approach |
|-----------|--------------|----------|
| Fragile (migrations, payments) | Low | Exact instructions, no variation |
| Standard (API calls, file processing) | Medium | Preferred pattern with flexibility |
| Creative (code review, analysis) | High | Heuristics and principles |
</degrees_of_freedom>

<model_testing>
Test skills with target models (Haiku, Sonnet, Opus):

- **Haiku:** Needs more explicit instructions, complete examples
- **Sonnet:** Balanced detail, good progressive disclosure
- **Opus:** Concise instructions, principles over procedures

Find balance that works across all target models.
</model_testing>
