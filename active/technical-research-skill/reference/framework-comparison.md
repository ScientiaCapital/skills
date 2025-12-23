# Framework Comparison Template

## Comparison Overview

Use this template when evaluating 2+ frameworks for a specific use case.

```yaml
comparison:
  use_case: ""
  date: ""
  decision_needed_by: ""
  stakeholders: []
  
  requirements:
    must_have: []
    nice_to_have: []
    constraints: []
```

---

## Framework Profiles

### Framework A: [Name]

```yaml
basics:
  name: ""
  url: ""
  github: ""
  stars: 0
  last_release: ""
  license: ""
  
maturity:
  age_years: 0
  production_users: []  # Known companies
  stability: ""  # alpha, beta, stable, mature
  
community:
  discord_members: 0
  github_contributors: 0
  stackoverflow_questions: 0
  
documentation:
  quality: ""  # 1-5
  examples: ""  # 1-5
  api_reference: ""  # 1-5
  tutorials: ""  # 1-5
```

### Framework B: [Name]
[Same structure]

---

## Feature Comparison Matrix

| Feature | Framework A | Framework B | Weight |
|---------|-------------|-------------|--------|
| [Feature 1] | ✅ / ⚠️ / ❌ | ✅ / ⚠️ / ❌ | HIGH |
| [Feature 2] | ✅ / ⚠️ / ❌ | ✅ / ⚠️ / ❌ | MED |
| [Feature 3] | ✅ / ⚠️ / ❌ | ✅ / ⚠️ / ❌ | LOW |

**Legend:**
- ✅ Full support (native, well-documented)
- ⚠️ Partial support (possible but difficult, plugin required)
- ❌ Not supported

---

## Technical Evaluation

### Installation & Setup

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| pip install works | | |
| M1 Mac compatible | | |
| Dependencies clean | | |
| Setup time | | |

### Code Quality

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Type hints | | |
| Async support | | |
| Error messages | | |
| Debugging ease | | |

### Performance

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Startup time | | |
| Memory usage | | |
| Throughput | | |
| Latency | | |

---

## Integration Assessment

### With Our Stack

| Integration | Framework A | Framework B |
|-------------|-------------|-------------|
| Supabase | | |
| RunPod | | |
| Vercel | | |
| MCP servers | | |
| LangGraph | | |

### API/SDK Quality

| Criteria | Framework A | Framework B |
|----------|-------------|-------------|
| Python SDK | | |
| REST API | | |
| WebSocket | | |
| Streaming | | |

---

## Risk Assessment

### Framework A Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | LOW/MED/HIGH | LOW/MED/HIGH | |

### Framework B Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | LOW/MED/HIGH | LOW/MED/HIGH | |

---

## Cost Analysis

```yaml
framework_a:
  licensing: ""  # Free, paid, usage-based
  hosting_cost: ""
  development_time: ""
  maintenance_burden: ""
  total_estimate: ""
  
framework_b:
  licensing: ""
  hosting_cost: ""
  development_time: ""
  maintenance_burden: ""
  total_estimate: ""
```

---

## Proof of Concept Results

### Framework A PoC

```yaml
poc:
  goal: ""
  time_spent: ""
  outcome: ""  # success, partial, failure
  
  what_worked: []
  what_didnt: []
  surprises: []
  
  code_sample: |
    # Key code that worked or didn't
```

### Framework B PoC

[Same structure]

---

## Decision Matrix

| Criteria | Weight | Framework A | Framework B |
|----------|--------|-------------|-------------|
| Feature completeness | 25% | /10 | /10 |
| Ease of use | 20% | /10 | /10 |
| Performance | 15% | /10 | /10 |
| Community/support | 15% | /10 | /10 |
| Integration fit | 15% | /10 | /10 |
| Cost | 10% | /10 | /10 |
| **Weighted Total** | 100% | **/10** | **/10** |

---

## Recommendation

```yaml
recommendation:
  winner: ""
  confidence: ""  # high, medium, low
  
  primary_reasons:
    - ""
    - ""
    - ""
    
  concerns:
    - ""
    
  next_steps:
    - ""
    - ""
    
  fallback_plan: ""
```

---

## Example: LangGraph vs LangChain

| Criteria | LangGraph | LangChain |
|----------|-----------|-----------|
| Complexity | Lower | Higher |
| Flexibility | Higher | Lower |
| State management | Native graphs | Chains/agents |
| Debugging | Easier | Harder |
| Learning curve | Moderate | Steep |
| Our preference | ✅ **Winner** | ❌ Avoid |

**Decision:** Use LangGraph for all agent orchestration. Avoid LangChain's abstractions.
