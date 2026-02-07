---
name: miro-skill
description: Use when creating visual boards, strategy canvases, architecture diagrams, or sprint boards in Miro. Triggers on "miro board", "visual diagram", "strategy canvas", "whiteboard".
---

# Miro Board Interaction

Visual collaboration boards for strategy, architecture, and sprint planning via Miro MCP + AI plugin.

## Setup

### MCP Server (Required)
```bash
claude mcp add --transport http miro https://mcp.miro.com
```
Then authenticate:
```
/mcp auth
```

### AI Plugin (Optional Enhancement)
Install `miroapp/miro-ai` from Miro marketplace for:
- Browse board contents
- Create diagrams from text
- Generate docs from boards
- Build tables from data
- Summarize board sections

## Quick Start

1. Authenticate with Miro MCP
2. Create or select a board
3. Use workflows below to populate it

## Board Workflows

### Strategy Board → Tech Spec

**When:** GTM planning, product strategy, competitive analysis

```
1. Create board with "Strategy: [Topic]" title
2. Add Business Model Canvas frame (3x3 grid)
3. Populate sticky notes per section:
   - Value Props (yellow)
   - Customer Segments (blue)
   - Channels (green)
   - Revenue Streams (orange)
4. Add tech implications column (right side)
5. Connect strategy items → tech requirements with arrows
```

**Miro tools used:** `create_board`, `create_sticky_note`, `create_shape`, `create_connector`

### Architecture → Code Scaffold

**When:** System design, service architecture, data flow

```
1. Create board "Architecture: [System]"
2. Add component shapes:
   - Services (rectangles, blue)
   - Databases (cylinders, green)
   - External APIs (clouds, gray)
   - Queues (parallelograms, orange)
3. Connect with labeled arrows (sync/async, protocol)
4. Add notes for each component (tech stack, scaling notes)
5. Export as spec for implementation
```

**Miro tools used:** `create_shape`, `create_connector`, `create_text`, `create_frame`

### Sprint Board → Tasks

**When:** Sprint planning, task breakdown, capacity planning

```
1. Create board "Sprint: [Name] — [Start] to [End]"
2. Add columns: Backlog | In Progress | Review | Done
3. Create cards per task:
   - Title (bold)
   - Story points (tag)
   - Assignee (avatar)
   - Priority (color: red=P0, orange=P1, yellow=P2)
4. Add swimlanes per team/workstream
5. Capacity bar at top (points committed vs available)
```

**Miro tools used:** `create_frame`, `create_card`, `create_sticky_note`, `create_tag`

### Competitive Analysis → GTM Playbook

**When:** Market positioning, competitor mapping, pricing strategy

```
1. Create board "Competitive: [Market]"
2. Add 2x2 matrix (Value vs Price axes)
3. Plot competitors as positioned sticky notes
4. Add our product with differentiation callouts
5. Draw opportunity gaps (dashed circles)
6. Add action items per gap
```

**Miro tools used:** `create_shape`, `create_sticky_note`, `create_connector`, `create_text`

## MCP Tools Reference

| Tool | Use For | Example |
|------|---------|---------|
| `create_board` | New board | Strategy canvas, sprint board |
| `get_boards` | List boards | Find existing board to update |
| `create_sticky_note` | Ideas, tasks | Brainstorm items, sprint tasks |
| `create_shape` | Components | Architecture boxes, matrix axes |
| `create_connector` | Relationships | Data flow, dependencies |
| `create_frame` | Grouping | Columns, sections, swimlanes |
| `create_card` | Rich items | Tasks with assignee, due date |
| `create_text` | Labels | Titles, annotations |
| `create_tag` | Categories | Priority, status, team |
| `get_items` | Read board | Parse existing board content |
| `update_item` | Modify | Change position, color, text |
| `delete_item` | Remove | Clean up board items |

## Color Conventions

| Color | Meaning |
|-------|---------|
| Yellow | Ideas, brainstorm, general |
| Blue | Technical, engineering |
| Green | Data, databases, success |
| Orange | Warning, queues, P1 |
| Red | Critical, blockers, P0 |
| Gray | External, third-party |
| Purple | Design, UX, creative |

## Positioning Guide

Miro uses x,y coordinates (pixels from top-left):
- Standard sticky note: 200x200px
- Standard shape: 300x200px
- Grid spacing: ~250px horizontal, ~250px vertical
- Frame padding: 50px inside edges

```
Layout example (3-column board):
Column 1: x=0,    items at y=0, 250, 500...
Column 2: x=350,  items at y=0, 250, 500...
Column 3: x=700,  items at y=0, 250, 500...
```

## Integration Points

- **business-model-canvas-skill** → Export canvas to Miro board
- **blue-ocean-strategy-skill** → Strategy Canvas visualization
- **gtm-pricing-skill** → Pricing matrix on Miro
- **research-skill** → Competitive landscape board
- **workflow-orchestrator-skill** → Sprint boards from End Day metrics

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Board too cluttered | Use frames to group, limit items per section |
| No authentication | Run `/mcp auth` after adding MCP server |
| Items overlapping | Use positioning guide grid spacing |
| Lost board URL | Use `get_boards` to list all boards |
| Stale board | Use `get_items` to verify current state before updates |
