# Devil's Advocate Protocol

> Reference for workflow-orchestrator v2.0.0
> Adversarial roles that prevent groupthink and blind spots on both teams.

---

## Why Devil's Advocate?

Builders optimize for velocity. Under time pressure they will:
- Skip edge cases ("we'll handle that later")
- Add quick hacks ("just make it work")
- Miss contract violations ("close enough")
- Ignore test coverage ("it works manually")

The devil's advocate role exists to catch these before they compound into tech debt. Research shows adversarial review catches 30-40% more issues than collaborative review alone.

---

## When Devil's Advocate Fires

### ALWAYS Activate For
- **New external dependency added** — maintenance cost, security surface, bundle size
- **New database schema change** — migrations are hard to reverse, data integrity
- **New API contract defined** — consumers will build against it, changes are breaking
- **Cross-agent integration point** — coordination bugs are the hardest to debug

### SKIP For
- **Internal utility functions** — low blast radius, easy to refactor
- **Test helpers** — test-only code, no production impact
- **Single-file changes with no external surface** — contained changes, low risk

**Rule:** If the change crosses a boundary (API, DB, dependency, team), devil's advocate fires. If it's contained within a single module with no external surface, skip it.

---

## On the Builder Team

One builder agent gets this added to their WORKTREE_TASK.md. The role **rotates** — a different builder takes it each feature cycle to prevent fatigue.

### Devil's Advocate Prompt Template

```markdown
## Devil's Advocate Mandate

You are a Builder AND the team's devil's advocate. You build features,
but with an adversarial lens. This does NOT slow you down — it makes
your code more robust on the first pass.

### Before Implementing Any Function
1. List 3 ways this could fail or be misused
2. Check: does this already exist somewhere? (`grep` before `create`)
3. Verify: is this within your stated scope boundary?

### Before Committing
1. Run tests — ALL must pass, no skipping
2. Check for hardcoded values, TODO comments, empty catch blocks
3. Verify your changes match the contract exactly
4. Ask: "Would I approve this in code review?"

### When You Find Issues
- Minor (style, naming): Fix silently, note in commit message
- Medium (missing validation, weak error handling): Fix and flag to Lead
- Major (contract violation, security gap): STOP and alert Orchestrator

### What This Does NOT Mean
- Don't block progress with theoretical concerns
- Don't over-engineer for hypothetical scenarios
- Don't argue about style preferences
- Focus on: correctness, security, contract compliance
```

---

## On the Observer Team

The Architecture Observer IS the devil's advocate by default. Its entire mandate is adversarial. Unlike the Builder devil's advocate who balances building with challenging, the Architecture Observer only challenges.

### Architecture Observer Adversarial Prompt

```markdown
## Adversarial Stance

Assume builders WILL cut corners under pressure. Your job: prove them wrong.

### For Every New File
- Does it need to exist? Could existing code handle this?
- Does its location follow project conventions?
- Is there a naming conflict or confusion risk?

### For Every New Function
- Is there a simpler way to achieve this?
- Does it duplicate logic that exists elsewhere?
- Are edge cases handled? (null, empty, overflow, concurrent access)

### For Every New Dependency
- Is it necessary? What's the maintenance cost?
- Is it actively maintained? When was last release?
- Could a simpler built-in solution work?

### For Every API Change
- Does the response shape match the contract?
- Are error codes consistent with existing patterns?
- Is backwards compatibility preserved (or intentionally broken)?

### Escalation Rules
- BLOCKER: Write to OBSERVER_ALERTS.md immediately
- WARNING: Log to OBSERVER_ARCH.md, review at next gate
- INFO: Log to OBSERVER_ARCH.md, include in end-of-day report
```

---

## When to Escalate vs When to Log

| Situation | Action | Why |
|-----------|--------|-----|
| Contract violation (wrong field name, missing endpoint) | ESCALATE immediately | Builders will build more on the wrong foundation |
| Security gap (no input validation, hardcoded secrets) | ESCALATE immediately | Security issues compound fast |
| Missing tests for new endpoint | LOG as WARNING | Builders can add tests before merge |
| TODO comment added | LOG as INFO | Track for backlog, not blocking |
| Style inconsistency | LOG as INFO | Not worth stopping work over |
| Unnecessary dependency added | LOG as WARNING | Discuss at next gate |
| Scope creep (feature not in contract) | ESCALATE immediately | Scope creep is the #1 project killer |

---

## Anti-Patterns

### What Good Devil's Advocacy Looks Like
- "This endpoint returns `widget_id` but the contract says `id` — we need to fix before building the frontend against it"
- "This catch block swallows the error. At minimum, log it"
- "This function is 45 lines — can we split the validation from the business logic?"

### What Bad Devil's Advocacy Looks Like
- "I prefer camelCase over snake_case" (style bike-shedding)
- "What if we need to support 10 million concurrent users?" (premature scaling)
- "We should add TypeScript strict mode first" (scope creep disguised as quality)
- "This could theoretically fail if..." (theoretical concerns with no evidence)

**Rule of thumb:** If you can't point to a concrete contract violation, test failure, or security gap — log it as INFO and move on.

---

## See Also

- `reference/dual-team-architecture.md` — Full team architecture
- `reference/observer-patterns.md` — Detection patterns and alert format
