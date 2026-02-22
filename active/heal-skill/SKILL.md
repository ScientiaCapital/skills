---
name: heal-skill
description: Use when skills fail to activate, produce errors, need structural validation, or the library needs a health audit. Diagnose YAML frontmatter, XML sections, config.json schema, file structure, and cross-skill dependencies.
user-invocable: true
---

<objective>
Diagnose and auto-repair broken skills. Run `/heal-skill` for a full library scan or `/heal-skill <name>` for a single skill diagnosis. Reports issues by severity with health scoring and offers auto-fixes with user confirmation.
</objective>

<quick_start>
```
/heal-skill              → Full library scan (all skills)
/heal-skill <name>       → Single skill diagnosis
/heal-skill --fix        → Apply all auto-fixes (with confirmation)
/heal-skill --fix <name> → Fix single skill (with confirmation)
```
</quick_start>

<success_criteria>
- All YAML frontmatter validates against Anthropic spec
- All required XML sections present (`<objective>`, `<quick_start>`, `<success_criteria>`)
- All config.json files use standard schema with correct keys
- Health score reported: X/Y checks passing per skill
- Auto-fixes applied ONLY with user confirmation (preview diff first)
- Self-test passes: `/heal-skill heal-skill` reports 0 issues
</success_criteria>

<core_content>

## 3-Layer Diagnostic Engine

The engine runs checks in order of severity. Each layer builds on the previous.

```
Layer 1: STRUCTURAL (CRITICAL)     → Files exist, YAML parses, required fields present
Layer 2: CONTENT (HIGH)            → XML sections, line count, naming conventions
Layer 3: INTEGRATION (MEDIUM)      → config.json schema, duplicate triggers, cross-refs
```

### Layer 1: Structural Validation (CRITICAL)

These checks verify the skill can even load. Failures here mean the skill is broken.

| ID | Check | Rule | Auto-fix |
|----|-------|------|----------|
| S1 | YAML frontmatter exists | SKILL.md starts with `---` | No |
| S2 | `name` field present | Required, non-empty string | No |
| S3 | `name` format valid | `^[a-z0-9-]+$`, max 64 chars | Yes — slugify |
| S4 | `description` field present | Required, non-empty string | No |
| S5 | `description` length | Max 1024 chars | Yes — truncate |
| S6 | `description` has no XML tags | No `<tags>` in value | Yes — strip tags |
| S7 | `description` is a string | Not YAML array/object | Yes — join if array |
| S7b | Frontmatter keys valid | All keys in valid set (see below) | Warning |
| S8 | SKILL.md exists | Must exist in skill directory | No |
| S9 | config.json exists | Must exist in skill directory | Yes — generate from SKILL.md |
| S10 | config.json is valid JSON | Must parse without error | No |

**Detection for S1-S2:** Read first 5 lines; check `---` delimiter and `name:` key.
**Detection for S3:** Regex `^[a-z0-9-]+$` on name value, check `length <= 64`.
**Detection for S6:** Regex `<[a-z_]+>` in description value.
**Detection for S7:** YAML parse — check type is string, not array/object.
**Detection for S7b:** Valid frontmatter keys are: `name`, `description`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `argument-hint`, `hooks`. Any other key is a WARNING (not an error — unknown keys are ignored by Claude Code, not rejected).

### Layer 2: Content Quality (HIGH)

These checks verify the skill follows library conventions for discoverability.

| ID | Check | Rule | Auto-fix |
|----|-------|------|----------|
| C1 | `<objective>` section exists | Must be present in SKILL.md body | Yes — add stub |
| C2 | `<quick_start>` section exists | Must be present in SKILL.md body | Yes — add stub |
| C3 | `<success_criteria>` section exists | Must be present in SKILL.md body | Yes — add stub |
| C4 | Line count | Body ≤ 500 lines (warning only) | Warning |
| C5 | Dead reference links | Internal `reference/` links must resolve | Yes — remove dead |
| C6 | Naming convention | Directory ends with `-skill` | Warning |

**Detection for C1-C3:** Search SKILL.md body (after frontmatter) for `<objective>`, `<quick_start>`, `<success_criteria>`.
**Detection for C4:** `wc -l SKILL.md`.
**Detection for C5:** Extract paths from `[text](reference/...)` links, verify file exists.
**Detection for C6:** Check directory name ends with `-skill`.

### Layer 3: Integration Health (MEDIUM)

These checks verify consistency across the library.

| ID | Check | Rule | Auto-fix |
|----|-------|------|----------|
| I1 | config.json has standard keys | Must have `name`, `version`, `category` | Yes — add missing |
| I2 | Uses `activation_triggers` key | Not `triggers` (legacy name) | Yes — rename key |
| I3 | Uses `depends_on` key | Not `dependencies` (legacy name) | Yes — rename key |
| I4 | Has `version` field | Must have `version` string | Yes — add "1.0.0" |
| I5 | No duplicate activation triggers | No trigger collisions across skills | Warning |

**Detection for I2:** Check if config.json has key `triggers` instead of `activation_triggers`.
**Detection for I3:** Check if config.json has key `dependencies` instead of `depends_on`.

---

## Diagnostic Flow

```
1. DISCOVER
   - Scan active/ and stable/ directories
   - Build skill inventory (name, path, has SKILL.md, has config.json)

2. LAYER 1 — STRUCTURAL
   - For each skill: parse YAML frontmatter, validate fields
   - STOP on critical failures (no SKILL.md = skip remaining checks)

3. LAYER 2 — CONTENT
   - For each skill: search for XML sections, check line count
   - Check naming convention

4. LAYER 3 — INTEGRATION
   - For each skill: validate config.json schema
   - Cross-skill: check for duplicate triggers

5. REPORT
   - Generate health report grouped by severity
   - Calculate health score
   - List available auto-fixes
```

---

## Output Format

Generate the report in this exact format:

```
SKILL HEALTH REPORT
════════════════════════════════════════════════
Scanned: X skills | Health Score: Y/Z (N%)

CRITICAL (n):
  ✗ skill-name: Description of issue [CHECK-ID]

HIGH (n):
  ⚠ skill-name: Description of issue [CHECK-ID]

MEDIUM (n):
  ℹ skill-name: Description of issue [CHECK-ID]

WARNINGS (n):
  ~ skill-name: Description of advisory [CHECK-ID]

════════════════════════════════════════════════
AUTO-FIX AVAILABLE: N issues can be auto-fixed
  Run /heal-skill --fix to preview and apply
```

**Single skill mode** — same format but for one skill only.

**Severity definitions:**
- **CRITICAL:** Skill cannot load or activate (S1-S10 failures)
- **HIGH:** Skill loads but missing expected sections (C1-C3)
- **MEDIUM:** Schema inconsistencies that affect library tooling (I1-I5)
- **WARNING:** Advisory only, no action required (C4, C6)

---

## Auto-Fix Protocol

When `--fix` is specified, follow this exact protocol:

```
1. PREVIEW
   - Show each proposed change as a diff:
     ```
     FIX: skill-name — [CHECK-ID] Description
     --- before
     +++ after
     @@ change description @@
     -old content
     +new content
     ```

2. CONFIRM
   - Ask user: "Apply N fixes? (yes/no/select)"
   - "select" lets user pick individual fixes

3. APPLY
   - Make changes to files
   - Re-run affected checks to verify fix worked

4. RE-VALIDATE
   - Run full scan on fixed skills
   - Report new health score
```

**Auto-fix strategies by check:**

| Check | Fix Strategy |
|-------|-------------|
| S3 | Slugify: lowercase, replace spaces/special chars with hyphens |
| S5 | Truncate to 1024 chars at last sentence boundary |
| S6 | Strip XML tags with regex: `</?[a-z_]+>` → empty string |
| S7 | If array: join elements with ". ". If object: use first value |
| S9 | Generate minimal config.json from SKILL.md frontmatter |
| C1 | Add `<objective>\nTODO: Add objective\n</objective>` after frontmatter |
| C2 | Add `<quick_start>\nTODO: Add quick start\n</quick_start>` after objective |
| C3 | Add `<success_criteria>\nTODO: Add success criteria\n</success_criteria>` after quick_start |
| C5 | Remove dead `[text](reference/...)` links |
| I1 | Add missing keys with defaults from SKILL.md frontmatter |
| I2 | Rename `triggers` → `activation_triggers` in config.json |
| I3 | Rename `dependencies` → `depends_on` in config.json |
| I4 | Add `"version": "1.0.0"` to config.json |

---

## Known Issue Patterns

These patterns come from real GitHub issues and library audits. The diagnostic engine checks for all of them.

| Source | Pattern | Check |
|--------|---------|-------|
| GitHub #9817 | Whitespace before `---` prevents YAML parse | S1 |
| GitHub #11322 | Prettier reformats description to multi-line | S7 |
| GitHub #17604 | YAML array in description crashes slash commands | S7 |
| GitHub #6377 | Missing `name` field despite valid YAML structure | S2 |
| GitHub #14882 | Skills consume full tokens (no progressive disclosure) | C4 |
| GitHub #14577 | `/skills` shows "No skills found" — frontmatter parse failure | S1, S2 |
| Library audit | 8 skills missing XML sections | C1-C3 |
| Library audit | 9 skills using legacy config.json keys | I2, I3 |
| Library audit | 1 skill missing `-skill` suffix | C6 |

</core_content>

<common_mistakes>

## What Goes Wrong

| Mistake | Fix |
|---------|-----|
| Running `--fix` without reviewing diffs | Always preview first. The protocol requires confirmation. |
| Ignoring WARNINGS | Warnings are advisory but indicate tech debt. Track them. |
| Fixing only CRITICAL issues | HIGH and MEDIUM issues affect discoverability and tooling. Fix all layers. |
| Adding XML stubs without filling them in | Stubs are placeholders. Schedule time to write real content. |
| Running heal on a single skill when library-wide issues exist | Run full scan first to see the big picture. |

</common_mistakes>
