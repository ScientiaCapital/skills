# Miro Prompt Templates

## Strategy Canvas

```
Create a Miro board for our GTM strategy analysis.

Board: "GTM Strategy: [Product Name] — [Quarter]"

Layout:
1. Business Model Canvas (left, 2400x1600)
   - 9 sections with color-coded sticky notes
   - Key Partners (gray), Activities (blue), Resources (blue)
   - Value Props (yellow), Relations (green), Channels (green)
   - Segments (purple), Costs (orange), Revenue (orange)

2. Competitive Position (right, 1200x1200)
   - 2x2 matrix: Value vs Price
   - Plot 5 competitors + our position
   - Mark opportunity gaps

3. Action Items (bottom, full width)
   - Priority-colored cards
   - Owner + deadline per item
```

## Architecture Diagram

```
Create a Miro board for system architecture.

Board: "Architecture: [System Name]"

Components:
- [Service 1] (blue rectangle) — [tech stack]
- [Service 2] (blue rectangle) — [tech stack]
- [Database] (green cylinder) — [PostgreSQL/etc]
- [Queue] (orange parallelogram) — [Redis/SQS/etc]
- [External API] (gray cloud) — [name]

Connections:
- [Service 1] → [Service 2]: REST/JSON, sync
- [Service 1] → [Queue]: async, events
- [Queue] → [Service 2]: consume, batch
- [Service 2] → [Database]: SQL, read/write

Add notes per component: scaling strategy, SLA, owner team.
```

## Sprint Board

```
Create a Miro sprint board.

Board: "Sprint [N]: [Name] — [Start] to [End]"

Columns: Backlog | In Progress | Review | Done

Tasks:
| Task | Points | Priority | Assignee |
|------|--------|----------|----------|
| [task 1] | [N] | P0 | [name] |
| [task 2] | [N] | P1 | [name] |
| [task 3] | [N] | P2 | [name] |

Capacity: [committed] / [available] points

Add swimlanes for: [team 1], [team 2]
```

## Competitive Landscape

```
Create a competitive analysis board.

Board: "Competitive: [Market] — [Date]"

Competitors:
| Name | Price | Key Strength | Key Weakness |
|------|-------|-------------|--------------|
| [comp 1] | $[N]/mo | [strength] | [weakness] |
| [comp 2] | $[N]/mo | [strength] | [weakness] |
| [comp 3] | $[N]/mo | [strength] | [weakness] |

Our Position:
- Price: $[N]/mo
- Differentiator: [what makes us unique]
- Target: [ICP description]

Plot on 2x2 (Value vs Price), highlight gaps.
Add action plan per opportunity gap.
```

## Retrospective Board

```
Create a sprint retrospective board.

Board: "Retro: Sprint [N] — [Date]"

Three columns:
1. What Went Well (green sticky notes)
2. What Didn't Go Well (red sticky notes)
3. Action Items (blue cards with owners)

Add voting dots for prioritization.
Group similar items in frames.
```

## User Journey Map

```
Create a user journey map.

Board: "Journey: [Persona] — [Flow Name]"

Stages (horizontal):
1. Awareness → 2. Consideration → 3. Purchase → 4. Onboarding → 5. Retention

Per stage (vertical):
- Actions (blue notes)
- Thoughts (yellow notes)
- Emotions (green=positive, red=negative)
- Touchpoints (gray notes)
- Opportunities (orange notes)

Connect pain points to opportunity areas.
```
