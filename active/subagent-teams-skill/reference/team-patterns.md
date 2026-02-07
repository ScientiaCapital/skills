# Team Patterns

## Pattern 1: Research Team

**Purpose:** Explore unknown codebase areas from multiple angles.

**Composition:** 3 Explore agents (haiku)

```
Agent 1: "Search for [PATTERN] in src/ — report file paths and summaries"
Agent 2: "Search for [PATTERN] in tests/ — report test coverage"
Agent 3: "Search for [PATTERN] in config/docs — report configuration"
```

**Fan-in:** Team lead synthesizes into a codebase map.

**Cost:** ~$0.02 per research sprint (3x haiku)

---

## Pattern 2: Implement Team

**Purpose:** Build a feature with architecture review.

**Composition:** 1 Plan (sonnet) → 2-3 general-purpose (sonnet) → 1 code-reviewer (haiku)

```
Phase 1: Plan agent designs component architecture
Phase 2: Builder agents implement components in parallel
Phase 3: Reviewer validates all changes
```

**Fan-in:** Team lead merges approved changes.

**Cost:** ~$0.50-1.00 per feature (depends on complexity)

---

## Pattern 3: Review Team

**Purpose:** Thorough code review from multiple perspectives.

**Composition:** 3 code-reviewer agents (haiku)

```
Agent 1: Review for security (auth, injection, secrets)
Agent 2: Review for consistency (naming, patterns, style)
Agent 3: Review for performance (N+1, memory, complexity)
```

**Fan-in:** Team lead aggregates and deduplicates findings.

**Cost:** ~$0.02 per review sprint

---

## Pattern 4: Explore Team

**Purpose:** Build mental model of an unfamiliar area.

**Composition:** 3 Explore agents (haiku) with different strategies

```
Agent 1: Glob search for file structure patterns
Agent 2: Grep search for key function/class names
Agent 3: Read entry points and main files
```

**Fan-in:** Team lead builds architecture diagram.

**Cost:** ~$0.02 per exploration

---

## Pattern 5: Doc Team

**Purpose:** Update multiple independent docs simultaneously.

**Composition:** N general-purpose agents (haiku)

```
Agent 1: Update README.md
Agent 2: Update CHANGELOG.md
Agent 3: Update API docs
Agent N: Update [other independent file]
```

**Fan-in:** None needed (independent files).

**Cost:** ~$0.01 per file (haiku)
