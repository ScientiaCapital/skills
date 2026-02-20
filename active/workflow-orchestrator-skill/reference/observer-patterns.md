# Observer Patterns

> Reference for workflow-orchestrator v2.0.0
> Observer team detection patterns, templates, and escalation protocol.

---

## Observer WORKTREE_TASK.md Templates

### Code Quality Observer

```markdown
# WORKTREE_TASK: Code Quality Observer

## Your Role
You are the Code Quality Observer. Monitor builder output continuously for:
- Tech debt accumulation (TODOs, FIXMEs, hacks)
- Test coverage gaps (new functions without tests)
- Import bloat (unused imports, redundant dependencies)
- Silent failures (empty catch blocks, swallowed errors)
- Code style violations (inconsistent patterns)

## Monitoring Loop
Every 5-10 minutes:
1. `git pull` latest from builder branches
2. Run detection patterns below
3. Write findings to `.claude/OBSERVER_QUALITY.md`
4. If BLOCKER found → append to `.claude/OBSERVER_ALERTS.md`

## Output Format
[SEVERITY] — file:line — description — suggested fix
```

### Architecture Observer

```markdown
# WORKTREE_TASK: Architecture Observer (Devil's Advocate)

## Your Role
You are the Architecture Observer AND devil's advocate. Your mandate:
- Contract drift (response shapes vs contract definition)
- Scope creep (features not in the contract)
- Design violations (patterns inconsistent with codebase)
- Dependency creep (unnecessary new packages)

## Adversarial Stance
Assume builders WILL cut corners. Your job is to prove them wrong.
- Every new file: does it need to exist? Could existing code handle this?
- Every new function: is there a simpler way?
- Every new dependency: is it necessary? What's the maintenance cost?

## Output Format
[SEVERITY] — file:line — description — suggested fix
```

---

## 7 Drift Detection Patterns

### 1. Agent Drift (Scope Violation)

Detect when builders work outside their assigned scope boundaries.

```bash
# Compare modified files against scope boundary in contract
git diff --name-only main...builder-branch | while read f; do
  grep -q "$f" .claude/CONTRACT.md || echo "SCOPE VIOLATION: $f not in contract"
done
```

**Severity:** BLOCKER if touching files explicitly marked OUT OF SCOPE

### 2. Tech Debt Accumulation

Detect growing TODO/FIXME/HACK comments.

```bash
# Count debt markers in changed files
git diff --name-only main...HEAD | xargs grep -Hn "TODO\|FIXME\|HACK\|XXX\|TEMP" 2>/dev/null
```

**Severity:** WARNING if count increases by >3 in a session

### 3. Test Gap

Detect new functions/exports without corresponding tests.

```bash
# Find new exported functions
git diff main...HEAD --diff-filter=A -- '*.ts' '*.js' '*.py' | grep -E "^\\+.*(export function|def |class )" | head -20

# Check for corresponding test files
for file in $(git diff --name-only main...HEAD -- 'src/'); do
  test_file=$(echo "$file" | sed 's/src/test/' | sed 's/\.\(ts\|js\|py\)/.test.\1/')
  [ ! -f "$test_file" ] && echo "TEST GAP: $file has no test at $test_file"
done
```

**Severity:** WARNING for utilities, BLOCKER for API endpoints

### 4. Scope Creep

Detect features being built that aren't in the contract.

```bash
# Compare actual endpoints vs contract
grep -E "(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete|patch))" src/**/*.ts 2>/dev/null | \
  while read line; do
    endpoint=$(echo "$line" | grep -oE "'[^']+'" | head -1)
    grep -q "$endpoint" .claude/CONTRACT.md 2>/dev/null || echo "SCOPE CREEP: $endpoint not in contract"
  done
```

**Severity:** BLOCKER — new endpoints MUST be in contract

### 5. Import Bloat

Detect unused imports and redundant dependencies.

```bash
# TypeScript/JavaScript unused imports (basic check)
for file in $(git diff --name-only main...HEAD -- '*.ts' '*.tsx' '*.js'); do
  # Find imported names not used in file body
  grep -oE "import.*{([^}]+)}" "$file" 2>/dev/null | grep -oE "[A-Za-z]+" | while read name; do
    count=$(grep -c "$name" "$file" 2>/dev/null)
    [ "$count" -le 1 ] && echo "UNUSED IMPORT: $name in $file"
  done
done
```

**Severity:** INFO — log to backlog

### 6. Silent Failures

Detect empty catch blocks and swallowed errors.

```bash
# Empty catch blocks
grep -rn "catch.*{" --include="*.ts" --include="*.js" --include="*.py" -A 2 | \
  grep -B 1 "^[^:]*:.*}" | grep "catch"

# Python bare except
grep -rn "except:" --include="*.py" | grep -v "except.*Error"
```

**Severity:** WARNING — silent failures mask bugs

### 7. Contract Drift

Detect when response shapes diverge from the contract definition.

```bash
# Extract response types from contract
grep -A 5 "→ {" .claude/CONTRACT.md 2>/dev/null

# Compare against actual return statements
grep -rn "return.*{" --include="*.ts" --include="*.js" src/ | head -20

# Check for fields in code not in contract (manual review trigger)
echo "Compare above outputs for field mismatches"
```

**Severity:** BLOCKER if response shape doesn't match contract

---

## Observer Output Format

All findings use a consistent format:

```
[SEVERITY] — file:line — description — fix

Examples:
[BLOCKER] — src/api/widgets.ts:45 — POST /api/widgets returns { widget_id } but contract says { id } — rename to match contract
[WARNING] — src/utils/helpers.ts:12 — TODO: implement proper validation — write validation or remove TODO
[INFO] — src/lib/cache.ts:3 — unused import: Redis — remove import
```

### Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| BLOCKER | Stops work | Builder must fix before next commit |
| WARNING | Should fix | Fix before merge, or add to backlog with justification |
| INFO | Nice to have | Log to backlog, fix when convenient |

---

## Alert Escalation

### OBSERVER_ALERTS.md Format

When a BLOCKER is found, Observers write to `.claude/OBSERVER_ALERTS.md`:

```markdown
# Observer Alerts

## Active Blockers

### [BLOCKER] Contract drift in widgets API
- **Found by:** Architecture Observer
- **Time:** 2026-02-20T14:30:00
- **File:** src/api/widgets.ts:45
- **Issue:** Response shape { widget_id, title } doesn't match contract { id, name }
- **Required action:** Rename fields to match contract
- **Status:** OPEN
```

### Orchestrator Check Protocol

The Orchestrator checks `OBSERVER_ALERTS.md` at every phase gate:
1. Before allowing Phase 2 → Phase 3 transition (Implementation → Security)
2. Before END DAY security sweep
3. Before any merge to main

**If active BLOCKERs exist:** Gate is blocked. Builders must resolve before proceeding.

---

## Observer Session Lifecycle

```
START DAY
  └→ Orchestrator spawns Observer team (auto)
      ├→ Code Quality Observer (haiku, runs every 5 min)
      └→ Architecture Observer (sonnet, runs every 10 min)

FEATURE DEVELOPMENT
  └→ Observers monitor builder branches concurrently
      ├→ Write to .claude/OBSERVER_QUALITY.md
      ├→ Write to .claude/OBSERVER_ARCH.md
      └→ Escalate BLOCKERs to .claude/OBSERVER_ALERTS.md

END DAY
  └→ Observer Final Report
      ├→ Summary of all findings (resolved + open)
      ├→ Metrics: debt items, test coverage delta, contract compliance
      └→ Archive to .claude/OBSERVER_HISTORY/
```

---

## See Also

- `reference/dual-team-architecture.md` — Full architecture overview
- `reference/devils-advocate.md` — Adversarial prompt templates
- `templates/OBSERVER_QUALITY.md` — Quality report template
- `templates/OBSERVER_ARCH.md` — Architecture report template
