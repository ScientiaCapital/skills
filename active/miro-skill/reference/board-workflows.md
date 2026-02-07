# Board Workflows

## Strategy Board → Tech Spec

### Purpose
Transform business strategy discussions into actionable technical specifications.

### Step-by-Step

1. **Create Board**
   ```
   create_board(title="Strategy: [Topic] — [Date]")
   ```

2. **Add Business Model Canvas Frame**
   ```
   create_frame(title="Business Model Canvas", x=0, y=0, width=2400, height=1600)
   ```

3. **Populate 9 Sections**
   | Section | Position | Color |
   |---------|----------|-------|
   | Key Partners | x=50, y=50 | gray |
   | Key Activities | x=350, y=50 | blue |
   | Key Resources | x=350, y=450 | blue |
   | Value Props | x=700, y=50 | yellow |
   | Customer Relations | x=1050, y=50 | green |
   | Channels | x=1050, y=450 | green |
   | Customer Segments | x=1400, y=50 | purple |
   | Cost Structure | x=50, y=850 | orange |
   | Revenue Streams | x=700, y=850 | orange |

4. **Add Tech Implications**
   ```
   create_frame(title="Tech Requirements", x=2500, y=0, width=800, height=1600)
   ```
   - Map each strategy item → technical requirement
   - Connect with arrows using `create_connector`

5. **Export**
   - Screenshot for docs
   - Extract text for JIRA/Linear tickets

---

## Architecture → Code Scaffold

### Purpose
Design system architecture visually, then extract as implementation spec.

### Step-by-Step

1. **Create Board**
   ```
   create_board(title="Architecture: [System] — [Date]")
   ```

2. **Add Component Legend**
   | Shape | Color | Meaning |
   |-------|-------|---------|
   | Rectangle | Blue | Service/API |
   | Cylinder | Green | Database |
   | Cloud | Gray | External API |
   | Parallelogram | Orange | Queue/Stream |
   | Hexagon | Purple | Serverless Function |

3. **Layout Components** (left-to-right flow)
   ```
   Client → API Gateway → Services → Database
                            ↓
                         Queue → Workers
   ```

4. **Label Connections**
   - Protocol (HTTP, gRPC, WebSocket)
   - Sync vs Async
   - Data format (JSON, protobuf)

5. **Add Detail Notes**
   Per component: tech stack, scaling strategy, SLA requirements

---

## Sprint Board → Tasks

### Purpose
Visual sprint planning with capacity tracking.

### Step-by-Step

1. **Create Board**
   ```
   create_board(title="Sprint: [Name] — [Start] to [End]")
   ```

2. **Create Column Frames**
   | Column | x | Width | Color |
   |--------|---|-------|-------|
   | Backlog | 0 | 400 | gray |
   | In Progress | 450 | 400 | blue |
   | Review | 900 | 400 | orange |
   | Done | 1350 | 400 | green |

3. **Add Task Cards**
   ```
   create_card(
     title="[Task Name]",
     description="[Details]",
     assignee="[Name]",
     due_date="[Date]"
   )
   ```

4. **Color by Priority**
   - Red border: P0 (critical)
   - Orange border: P1 (important)
   - Yellow border: P2 (nice to have)

5. **Capacity Bar**
   Add horizontal bar at top:
   ```
   Total Points: [committed] / [available]
   [████████░░] 80%
   ```

---

## Competitive Analysis → GTM Playbook

### Purpose
Map competitive landscape and identify market opportunities.

### Step-by-Step

1. **Create Board**
   ```
   create_board(title="Competitive: [Market] — [Date]")
   ```

2. **Draw 2x2 Matrix**
   - X-axis: Price (Low → High)
   - Y-axis: Value/Features (Low → High)
   ```
   create_shape(type="rectangle", x=0, y=0, width=1200, height=1200)
   create_text("High Value", x=600, y=-30)
   create_text("Low Value", x=600, y=1230)
   create_text("Low Price", x=-80, y=600)
   create_text("High Price", x=1280, y=600)
   ```

3. **Plot Competitors**
   ```
   create_sticky_note(
     content="[Competitor]\n$[Price]\n[Key Feature]",
     x=[position], y=[position],
     color="yellow"
   )
   ```

4. **Plot Our Position**
   ```
   create_sticky_note(
     content="[Our Product]\n$[Price]\n[Differentiator]",
     color="blue"
   )
   ```

5. **Mark Opportunity Gaps**
   ```
   create_shape(type="circle", style="dashed", color="green")
   create_text("Opportunity: [Description]")
   ```

6. **Action Items**
   Add frame below matrix with action items per opportunity gap.
