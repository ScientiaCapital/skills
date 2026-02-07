# Known Issues Reference

Failure patterns sourced from GitHub issues and library audits. Each pattern maps to specific diagnostic checks.

---

## GitHub Issue Patterns

### #9817 — Frontmatter Whitespace Sensitivity

**Problem:** Leading whitespace before the `---` delimiter causes YAML parse failure. The skill loads as plain text instead of being recognized as a skill.

**Symptom:** Skill doesn't appear in `/skills` list despite having valid YAML content.

**Check:** S1 — YAML frontmatter exists

**Example:**
```yaml
  ---
name: my-skill
description: Use when...
---
```
The two leading spaces before `---` break parsing.

---

### #11322 — Prettier Multi-line Descriptions

**Problem:** Prettier (and similar formatters) can reformat long description strings into YAML block scalars or arrays, which breaks the Anthropic parser.

**Symptom:** Skill name appears but description is `[object Object]` or empty.

**Check:** S7 — description is a string

**Example (broken):**
```yaml
description:
  - Use when skills fail to activate
  - or produce errors
```
Prettier reformatted the single string into a YAML array.

**Prevention:** Add SKILL.md to `.prettierignore` or use `# prettier-ignore` comments.

---

### #17604 — YAML Array Descriptions Crash Slash Commands

**Problem:** When the description field contains XML-style tags, the slash command parser can crash or behave unpredictably.

**Symptom:** `/skill-name` command throws an error or produces garbled output.

**Check:** S6 — description has no XML tags

**Example (broken):**
```yaml
description: "Use when <objective> parsing fails or <success_criteria> are missing"
```
The `<objective>` and `<success_criteria>` tags in the description confuse the parser.

---

### #6377 — Missing Name Field Despite Valid YAML

**Problem:** YAML frontmatter parses successfully but lacks the required `name` field. The skill is silently ignored.

**Symptom:** Skill directory exists, SKILL.md has frontmatter, but skill never activates.

**Check:** S2 — name field present

**Example (broken):**
```yaml
---
description: Use when debugging is needed
---
```
Valid YAML, but missing `name` — skill is invisible.

---

### #14882 — Skills Consume Full Tokens

**Problem:** Large skills (500+ lines) consume significant context tokens when loaded. Without progressive disclosure (reference files), skills eat into the conversation budget.

**Symptom:** Conversations hit context limits faster when multiple large skills are loaded.

**Check:** C4 — line count (warning)

**Mitigation:** Extract heavy content into `reference/` files. Keep SKILL.md body under 500 lines. Use progressive disclosure architecture.

---

### #14577 — `/skills` Shows "No Skills Found"

**Problem:** The `/skills` slash command returns empty even though skills exist on disk. Usually caused by frontmatter parse failure (whitespace, missing fields, invalid YAML).

**Symptom:** User sees "No skills found" when running `/skills`.

**Checks:** S1 (frontmatter exists), S2 (name present), S3 (name format)

**Debugging:** Run heal-skill on the skills directory. Layer 1 structural checks will identify which skills have broken frontmatter.

---

## Library Audit Findings (2026-02-07)

### Missing XML Sections (8 skills)

Skills that loaded successfully but lacked standard XML structure:

| Skill | Missing Sections |
|-------|-----------------|
| docker-compose-skill | `<objective>`, `<quick_start>`, `<success_criteria>` |
| hubspot-revops-skill | `<objective>`, `<quick_start>`, `<success_criteria>` |
| miro-skill | `<objective>`, `<quick_start>`, `<success_criteria>` |
| agent-capability-matrix-skill | `<success_criteria>` |
| cost-metering-skill | `<success_criteria>` |
| openrouter-skill | `<success_criteria>` |
| portfolio-artifact-skill | `<success_criteria>` |
| subagent-teams-skill | `<success_criteria>` |

**Impact:** Skills work but are harder to discover and don't follow library conventions.

**Checks:** C1, C2, C3

---

### Non-Standard config.json Keys (9 skills)

Skills using legacy key names from before the schema was standardized:

| Skill | Issue |
|-------|-------|
| agent-capability-matrix-skill | Uses `triggers` instead of `activation_triggers` |
| agent-teams-skill | Uses `triggers` instead of `activation_triggers` |
| cost-metering-skill | Uses `triggers` instead of `activation_triggers` |
| docker-compose-skill | Uses `triggers` instead of `activation_triggers` |
| openrouter-skill | Uses `triggers` instead of `activation_triggers` |
| portfolio-artifact-skill | Uses `triggers` instead of `activation_triggers` |
| subagent-teams-skill | Uses `triggers` instead of `activation_triggers` |
| worktree-manager-skill | Uses `triggers` instead of `activation_triggers` |
| hubspot-revops-skill | Uses `dependencies` instead of `depends_on` |

**Impact:** Library tooling that expects standard keys may miss these skills.

**Checks:** I2, I3

---

### Naming Convention (1 skill)

| Skill | Issue |
|-------|-------|
| workflow-enforcer | Missing `-skill` suffix |

**Impact:** Directory listing and glob patterns like `*-skill` miss this skill.

**Check:** C6

**Note:** This is tracked as known tech debt. Renaming would require updating all references across the library.
