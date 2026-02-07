# Prompt Templates for Team Patterns

> Ready-to-use spawn prompts for each of the 4 team patterns.
> Adapt these to your project — replace placeholders in `[brackets]`.

---

## Feature Parallel

**Pattern:** 2-3 agents build independent features simultaneously.
**Conflict risk:** Low (agents touch different directories).

### Team Lead Setup

```json
{
  "team": "[team-name]",
  "pattern": "feature-parallel",
  "agents": [
    { "id": 1, "branch": "feature/[feature-a]", "scope": "[directory-a]" },
    { "id": 2, "branch": "feature/[feature-b]", "scope": "[directory-b]" }
  ],
  "merge_order": [1, 2],
  "merge_target": "main"
}
```

### Agent 1 WORKTREE_TASK.md

```markdown
# Task: Build [Feature A]

## Context
We're building [project description]. This is one of 2 parallel features
being developed. Another agent is building [Feature B] in a separate worktree.

## Your Assignment
Implement [Feature A] with the following requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## File Boundaries
**Work in:** `[src/feature-a/]`
**Do NOT touch:** `[src/feature-b/]`, `[src/shared/]` (unless adding exports)

## Verification
1. Run tests: `[test command]`
2. Check types: `[type check command]`
3. Verify feature works: `[manual check]`

## When Done
1. Commit with message: `feat([scope]): [description]`
2. Push: `git push -u origin feature/[feature-a]`
3. Write "DONE" to `.agent-status`
```

### Agent 2 WORKTREE_TASK.md

Same structure, replace Feature A references with Feature B.

---

## Frontend / Backend

**Pattern:** One agent builds the API, another builds the UI. Shared contract.
**Conflict risk:** Low if contract is well-defined; medium if shared types exist.

### Team Lead Setup

```json
{
  "team": "[feature-name]",
  "pattern": "frontend-backend",
  "agents": [
    { "id": 1, "branch": "feature/[feature]-api", "scope": "src/api/, src/models/" },
    { "id": 2, "branch": "feature/[feature]-ui", "scope": "src/components/, src/pages/" }
  ],
  "contract": {
    "endpoint": "[METHOD /api/path]",
    "request": "{ [request shape] }",
    "response": "{ [response shape] }"
  },
  "merge_order": [1, 2],
  "merge_target": "main"
}
```

### Shared CONTRACT.md

Write this to BOTH worktrees before launching agents:

```markdown
# API Contract: [Feature Name]

## Endpoints

### [METHOD] /api/[resource]
**Request:**
```json
{
  "[field]": "[type]",
  "[field]": "[type]"
}
```

**Response (200):**
```json
{
  "[field]": "[type]",
  "[field]": "[type]"
}
```

**Error (400/401/500):**
```json
{
  "error": { "code": "string", "message": "string" }
}
```

## Shared Types
```typescript
interface [TypeName] {
  [field]: [type];
}
```
```

### Backend Agent WORKTREE_TASK.md

```markdown
# Task: Build [Feature] API

## Context
We're building [feature description]. You're the backend agent.
A frontend agent is building the UI in a separate worktree using the same contract.

## Your Assignment
Implement the API endpoints defined in CONTRACT.md:
- [Endpoint 1]: [description]
- [Endpoint 2]: [description]

## API Contract
See `CONTRACT.md` in this directory for exact request/response shapes.
Your implementation MUST match the contract exactly.

## File Boundaries
**Work in:** `src/api/`, `src/models/`, `src/middleware/`
**Do NOT touch:** `src/components/`, `src/pages/`

## Verification
1. Run: `[test command]`
2. Test endpoints with curl:
   ```bash
   curl -X [METHOD] localhost:[port]/api/[resource] \
     -H "Content-Type: application/json" \
     -d '{ [test payload] }'
   ```
3. Verify response matches CONTRACT.md shapes

## When Done
1. Commit: `feat(api): [description]`
2. Push: `git push -u origin feature/[feature]-api`
3. Write "DONE" to `.agent-status`
```

### Frontend Agent WORKTREE_TASK.md

```markdown
# Task: Build [Feature] UI

## Context
We're building [feature description]. You're the frontend agent.
A backend agent is building the API in a separate worktree.
The API may not be ready yet — code against the contract.

## Your Assignment
Build the UI components for [feature]:
- [Component 1]: [description]
- [Component 2]: [description]

## API Contract
See `CONTRACT.md` in this directory.
Use these types when calling the API. If the API isn't available yet,
mock the responses matching the contract shapes.

## File Boundaries
**Work in:** `src/components/`, `src/pages/`, `src/hooks/`
**Do NOT touch:** `src/api/`, `src/models/`

## Verification
1. Run: `[test command]`
2. Check types: `[type check command]`
3. Verify components render without errors

## When Done
1. Commit: `feat(ui): [description]`
2. Push: `git push -u origin feature/[feature]-ui`
3. Write "DONE" to `.agent-status`
```

---

## Test / Implement (TDD Pair)

**Pattern:** Agent 1 writes tests first. Agent 2 implements until tests pass.
**Conflict risk:** None (sequential execution).

### Team Lead Setup

```json
{
  "team": "[feature-name]-tdd",
  "pattern": "test-implement",
  "agents": [
    { "id": 1, "branch": "feature/[feature]-tests", "scope": "tests/", "phase": "first" },
    { "id": 2, "branch": "feature/[feature]-impl", "scope": "src/", "phase": "second" }
  ],
  "execution": "sequential",
  "handoff": "Agent 1 pushes, Agent 2 pulls tests then implements",
  "merge_order": [2],
  "merge_target": "main"
}
```

### Test Agent WORKTREE_TASK.md (Runs First)

```markdown
# Task: Write Tests for [Feature]

## Context
We're doing TDD for [feature]. You write the tests FIRST.
An implementation agent will run after you, implementing code until your tests pass.

## Your Assignment
Write comprehensive tests for [feature]:
- [Test case 1]: [description]
- [Test case 2]: [description]
- [Edge case 1]: [description]

## Guidelines
- Write tests that FAIL (no implementation exists yet)
- Cover happy paths, error cases, and edge cases
- Use descriptive test names that explain expected behavior
- Tests should be runnable with `[test command]`

## File Boundaries
**Work in:** `tests/[feature]/`
**Do NOT touch:** `src/` (no implementation!)

## When Done
1. Commit: `test([scope]): add [feature] test suite`
2. Push: `git push -u origin feature/[feature]-tests`
3. Write "DONE: [N] tests written, all currently failing" to `.agent-status`
```

### Implementation Agent WORKTREE_TASK.md (Runs Second)

```markdown
# Task: Implement [Feature] (Make Tests Pass)

## Context
A test agent has already written tests for [feature].
Your job: implement the code until ALL tests pass.

## Setup
First, pull the test branch:
```bash
git fetch origin feature/[feature]-tests
git merge origin/feature/[feature]-tests
```

## Your Assignment
Implement [feature] to make all tests pass:
1. Run tests to see what's expected: `[test command]`
2. Implement the minimum code to pass each test
3. Refactor once all tests pass

## File Boundaries
**Work in:** `src/[feature]/`
**Do NOT modify tests** in `tests/[feature]/`

## Verification
1. ALL tests pass: `[test command]`
2. No type errors: `[type check command]`
3. No skipped or pending tests

## When Done
1. Commit: `feat([scope]): implement [feature]`
2. Push: `git push -u origin feature/[feature]-impl`
3. Write "DONE: All [N] tests passing" to `.agent-status`
```

---

## Review / Refactor

**Pattern:** Agent 1 refactors code. Agent 2 reviews the changes.
**Conflict risk:** None (sequential, same branch).

### Team Lead Setup

```json
{
  "team": "[scope]-refactor",
  "pattern": "review-refactor",
  "agents": [
    { "id": 1, "branch": "refactor/[scope]", "role": "refactorer", "phase": "first" },
    { "id": 2, "branch": "refactor/[scope]", "role": "reviewer", "phase": "second" }
  ],
  "execution": "sequential",
  "handoff": "Agent 1 commits refactor, Agent 2 reviews and suggests improvements",
  "merge_order": [1],
  "merge_target": "main"
}
```

### Refactor Agent WORKTREE_TASK.md

```markdown
# Task: Refactor [Scope]

## Context
We're refactoring [scope] to [goal: improve readability / reduce duplication / etc.].
After you finish, a review agent will examine your changes.

## Your Assignment
Refactor [files/directory]:
- [Specific refactoring goal 1]
- [Specific refactoring goal 2]

## Constraints
- Do NOT change external behavior (all existing tests must still pass)
- Do NOT add new features
- Keep commits atomic (one logical change per commit)

## Verification
1. All tests pass: `[test command]`
2. No type errors: `[type check command]`
3. External behavior unchanged

## When Done
1. Commit with descriptive messages explaining each change
2. Push: `git push -u origin refactor/[scope]`
3. Write "DONE: [summary of changes]" to `.agent-status`
```

### Review Agent WORKTREE_TASK.md (Runs Second)

```markdown
# Task: Review Refactoring of [Scope]

## Context
A refactoring agent has made changes to [scope].
Your job: review the changes and document findings.

## Setup
Pull the latest refactoring work:
```bash
git fetch origin refactor/[scope]
git checkout refactor/[scope]
git pull
```

## Your Assignment
Review all changes by the refactoring agent:
1. `git log --oneline -20` to see what changed
2. `git diff main..refactor/[scope]` to see the full diff
3. For each change, evaluate:
   - Does it improve readability?
   - Does it introduce any bugs?
   - Are there better approaches?
   - Does it follow project conventions?

## Output
Create `REVIEW.md` in the worktree root with:
- Summary of changes reviewed
- Issues found (if any)
- Suggestions for improvement
- Overall assessment: APPROVE / REQUEST_CHANGES

## Verification
1. All tests still pass: `[test command]`
2. Review document is complete and actionable

## When Done
1. Commit: `docs: add refactoring review for [scope]`
2. Push: `git push -u origin refactor/[scope]`
3. Write "DONE: Review complete — [APPROVE/REQUEST_CHANGES]" to `.agent-status`
```
