# Agent Selection Flowchart

## Quick Decision Tree

```
What do I need to do?
│
├─ FIND something in code?
│  ├─ Know the filename pattern? → Glob (direct, no agent needed)
│  ├─ Know the code pattern? → Grep (direct, no agent needed)
│  ├─ Need broad exploration? → Explore agent (haiku)
│  └─ Need deep analysis? → code-explorer agent (sonnet)
│
├─ WRITE or CHANGE code?
│  ├─ Simple one-file change? → Do it directly (no agent)
│  ├─ Multi-file feature? → general-purpose agent (sonnet)
│  ├─ Need architecture first? → Plan agent (opus) → then build
│  ├─ Parallel components? → subagent-teams (sonnet builders)
│  └─ Conflicting file edits? → agent-teams (worktree isolation)
│
├─ REVIEW code?
│  ├─ Quick quality check? → code-reviewer (haiku)
│  ├─ Security review? → security skill (sonnet)
│  ├─ PR review? → pr-review-toolkit agents (haiku)
│  ├─ Error handling? → silent-failure-hunter (sonnet)
│  └─ Type design? → type-design-analyzer (sonnet)
│
├─ DEBUG something?
│  ├─ Simple error? → Fix directly
│  ├─ Complex/intermittent? → debug-like-expert skill (sonnet)
│  └─ Performance issue? → Explore + profiling (sonnet)
│
├─ RESEARCH something?
│  ├─ Codebase area? → Explore agent (haiku)
│  ├─ Framework/tool? → research skill + WebSearch (sonnet)
│  └─ Market/company? → research skill (sonnet)
│
└─ BUSINESS task?
   ├─ GTM/pricing? → gtm-pricing skill
   ├─ Sales? → sales-revenue skill
   ├─ Content? → content-marketing skill
   ├─ Data? → data-analysis skill
   └─ Strategy? → business-model-canvas or blue-ocean skill
```

## Model Selection Rules

1. **Default: Sonnet** — covers 80% of tasks well
2. **Downgrade to Haiku** when task is:
   - File/code search
   - Classification or categorization
   - Code review (pattern matching)
   - Simple documentation
3. **Upgrade to Opus** when task is:
   - Architecture decisions with trade-offs
   - Complex multi-system reasoning
   - Critical planning that affects many files

## Cost Impact

| Strategy | Typical Cost | When |
|----------|-------------|------|
| Direct tools (no agent) | $0 extra | Simple search/edit |
| Haiku agent | ~$0.01 | Search, review, classify |
| Sonnet agent | ~$0.05-0.20 | Code gen, reasoning |
| Opus agent | ~$0.50-2.00 | Architecture, planning |
| 3x Haiku team | ~$0.03 | Parallel search/review |
| 3x Sonnet team | ~$0.30-0.60 | Parallel build |
