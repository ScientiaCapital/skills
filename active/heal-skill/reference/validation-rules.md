# Validation Rules Reference

Complete reference for all 16 diagnostic checks used by heal-skill.

---

## Layer 1: Structural Validation (CRITICAL)

### S1 — YAML Frontmatter Exists

- **Severity:** CRITICAL
- **Rule:** SKILL.md must begin with `---` on the first line
- **Detection:** Read first line of SKILL.md. Must be exactly `---` (with optional trailing whitespace).
- **Auto-fix:** No — requires manual creation
- **Source:** Anthropic skill specification
- **Pass example:** `---\nname: my-skill\ndescription: Use when...\n---`
- **Fail example:** `# My Skill\n\nThis skill does...` (no frontmatter)
- **Fail example:** `  ---\nname: my-skill` (leading whitespace — GitHub #9817)

### S2 — `name` Field Present

- **Severity:** CRITICAL
- **Rule:** YAML frontmatter must contain `name` key with non-empty string value
- **Detection:** Parse YAML between `---` delimiters. Check `name` key exists and value is non-empty string.
- **Auto-fix:** No — skill identity requires human decision
- **Source:** Anthropic skill specification, GitHub #6377
- **Pass example:** `name: my-skill`
- **Fail example:** `name:` (empty value)
- **Fail example:** Frontmatter with no `name` key at all

### S3 — `name` Format Valid

- **Severity:** CRITICAL
- **Rule:** Name must match `^[a-z0-9-]+$`, max 64 characters
- **Detection:** Regex match on name value
- **Auto-fix:** Yes — slugify (lowercase, replace `[^a-z0-9-]` with `-`, collapse consecutive hyphens, trim leading/trailing hyphens)
- **Source:** Anthropic skill specification
- **Pass example:** `name: my-skill-v2`
- **Fail example:** `name: My Skill` (uppercase, spaces)
- **Fail example:** `name: my_skill(v2)` (underscore, parentheses)

### S4 — `description` Field Present

- **Severity:** CRITICAL
- **Rule:** YAML frontmatter must contain `description` key with non-empty string value
- **Detection:** Parse YAML. Check `description` key exists and value is non-empty.
- **Auto-fix:** No — description requires human authoring
- **Source:** Anthropic skill specification

### S5 — `description` Length

- **Severity:** CRITICAL
- **Rule:** Description must be ≤1024 characters
- **Detection:** Check `len(description) <= 1024`
- **Auto-fix:** Yes — truncate at last sentence boundary before 1024 chars
- **Source:** Anthropic skill specification

### S6 — `description` Has No XML Tags

- **Severity:** CRITICAL
- **Rule:** Description must not contain XML-style tags
- **Detection:** Regex `</?[a-z_]+>` in description value
- **Auto-fix:** Yes — strip matching tags
- **Source:** GitHub #17604 — XML in description can crash slash command parsing

### S7 — `description` Is a String

- **Severity:** CRITICAL
- **Rule:** Description must be a plain YAML string, not an array or object
- **Detection:** YAML parse — check `typeof description === 'string'`
- **Auto-fix:** Yes — if array, join with ". ". If object, use first value.
- **Source:** GitHub #11322 — Prettier can reformat long strings to YAML arrays

### S8 — SKILL.md Exists

- **Severity:** CRITICAL
- **Rule:** Skill directory must contain SKILL.md
- **Detection:** Check file exists at `<skill-dir>/SKILL.md`
- **Auto-fix:** No — skill content requires human authoring

### S9 — config.json Exists

- **Severity:** CRITICAL
- **Rule:** Skill directory must contain config.json
- **Detection:** Check file exists at `<skill-dir>/config.json`
- **Auto-fix:** Yes — generate minimal config from SKILL.md frontmatter:
  ```json
  {
    "name": "<from-frontmatter>",
    "version": "1.0.0",
    "category": "Uncategorized",
    "description": "<from-frontmatter>",
    "requires": [],
    "depends_on": [],
    "integrates_with": [],
    "activation_triggers": []
  }
  ```

### S10 — config.json Is Valid JSON

- **Severity:** CRITICAL
- **Rule:** config.json must parse as valid JSON
- **Detection:** Attempt `JSON.parse()` on file contents
- **Auto-fix:** No — broken JSON requires manual inspection

---

## Layer 2: Content Quality (HIGH)

### C1 — `<objective>` Section Exists

- **Severity:** HIGH
- **Rule:** SKILL.md body (after frontmatter) must contain `<objective>` XML section
- **Detection:** Search for `<objective>` in file content after second `---`
- **Auto-fix:** Yes — insert stub after frontmatter:
  ```xml
  <objective>
  TODO: Add objective describing what this skill does.
  </objective>
  ```

### C2 — `<quick_start>` Section Exists

- **Severity:** HIGH
- **Rule:** SKILL.md body must contain `<quick_start>` XML section
- **Detection:** Search for `<quick_start>` in file content after second `---`
- **Auto-fix:** Yes — insert stub after `</objective>`:
  ```xml
  <quick_start>
  TODO: Add quick start usage examples.
  </quick_start>
  ```

### C3 — `<success_criteria>` Section Exists

- **Severity:** HIGH
- **Rule:** SKILL.md body must contain `<success_criteria>` XML section
- **Detection:** Search for `<success_criteria>` in file content after second `---`
- **Auto-fix:** Yes — insert stub after `</quick_start>`:
  ```xml
  <success_criteria>
  TODO: Add success criteria for this skill.
  </success_criteria>
  ```

### C4 — Line Count

- **Severity:** WARNING
- **Rule:** SKILL.md should be ≤500 lines (advisory — Anthropic recommendation for token efficiency)
- **Detection:** `wc -l SKILL.md`
- **Auto-fix:** Warning only — no automatic action
- **Note:** Skills exceeding 500 lines should consider extracting content to `reference/` files

### C5 — Dead Reference Links

- **Severity:** HIGH
- **Rule:** All `[text](reference/...)` links in SKILL.md must point to existing files
- **Detection:** Extract relative paths matching `reference/` from markdown links, verify each file exists
- **Auto-fix:** Yes — remove dead link (replace `[text](reference/dead.md)` with `text`)

### C6 — Naming Convention

- **Severity:** WARNING
- **Rule:** Skill directory name should end with `-skill`
- **Detection:** Check if directory basename ends with `-skill`
- **Auto-fix:** Warning only — renaming directories has cascading effects on references
- **Known issue:** `workflow-enforcer` is the only skill that doesn't follow this convention

---

## Layer 3: Integration Health (MEDIUM)

### I1 — config.json Has Standard Keys

- **Severity:** MEDIUM
- **Rule:** config.json must contain `name`, `version`, and `category` keys
- **Detection:** Parse JSON, check for presence of required keys
- **Auto-fix:** Yes — add missing keys:
  - `name`: from SKILL.md frontmatter
  - `version`: "1.0.0"
  - `category`: "Uncategorized"

### I2 — Uses `activation_triggers` Key

- **Severity:** MEDIUM
- **Rule:** config.json should use `activation_triggers`, not legacy `triggers`
- **Detection:** Check if JSON has `triggers` key
- **Auto-fix:** Yes — rename key `triggers` → `activation_triggers`

### I3 — Uses `depends_on` Key

- **Severity:** MEDIUM
- **Rule:** config.json should use `depends_on`, not legacy `dependencies`
- **Detection:** Check if JSON has `dependencies` key
- **Auto-fix:** Yes — rename key `dependencies` → `depends_on`

### I4 — Has `version` Field

- **Severity:** MEDIUM
- **Rule:** config.json must have `version` string field
- **Detection:** Check if JSON has `version` key with string value
- **Auto-fix:** Yes — add `"version": "1.0.0"`

### I5 — No Duplicate Activation Triggers

- **Severity:** WARNING
- **Rule:** No two skills should share the same activation trigger string
- **Detection:** Collect all `activation_triggers` arrays, check for duplicates across skills
- **Auto-fix:** Warning only — requires human decision on which skill should own the trigger
- **Note:** Some overlap is acceptable for related skills (e.g., "parallel development" in both agent-teams and worktree-manager)
