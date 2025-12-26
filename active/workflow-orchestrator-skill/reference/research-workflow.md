# Research Workflow

Systematic approach to technical and market research with cost optimization and decision gates.

## Research Triggers

### When Research is Mandatory
1. **New Technology Adoption**
   - Considering new framework/library
   - Evaluating API providers
   - Selecting infrastructure services

2. **Architectural Decisions**
   - Microservices vs monolith
   - Database selection
   - Authentication approaches

3. **Cost-Impacting Choices**
   - LLM provider selection
   - Cloud platform decisions
   - SaaS tool evaluation

4. **Build vs Buy Decisions**
   - Custom implementation vs service
   - Open source vs commercial
   - In-house vs outsourced

## Phase 1: Existing Solution Scan

### Local Repository Search
```bash
# Search your existing projects first
SEARCH_TERM="$1"
BASE_DIR=~/tk_projects

# Find similar implementations
find "$BASE_DIR" -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.ts" | \
    xargs grep -l "$SEARCH_TERM" 2>/dev/null | \
    grep -v node_modules | \
    head -20

# Search documentation
find "$BASE_DIR" -name "README.md" -o -name "ARCHITECTURE.md" | \
    xargs grep -A5 -B5 "$SEARCH_TERM" 2>/dev/null
```

### MCP Cookbook Check
```bash
# Always check cookbook first
COOKBOOK=/Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook

if [ -d "$COOKBOOK" ]; then
    echo "=== MCP Cookbook Matches ==="
    grep -r "$SEARCH_TERM" "$COOKBOOK" --include="*.md" | head -10
fi
```

### Previous Research Cache
```bash
# Check if we've researched this before
RESEARCH_CACHE=~/.claude/research-cache
mkdir -p "$RESEARCH_CACHE"

HASH=$(echo "$SEARCH_TERM" | md5)
if [ -f "$RESEARCH_CACHE/$HASH.md" ]; then
    echo "Found previous research:"
    cat "$RESEARCH_CACHE/$HASH.md"
fi
```

## Phase 2: Evaluation Framework

### Technical Evaluation Matrix
```markdown
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Performance | 25% | 8/10 | 6/10 | 9/10 |
| Cost | 30% | $0 | $25/mo | $5/mo |
| Learning Curve | 15% | Low | Medium | High |
| Community | 10% | Large | Small | Medium |
| Maintenance | 20% | Active | Stale | Active |
| **Total Score** | | 7.5 | 5.8 | 8.2 |
```

### Cost Projection Model
```python
def project_costs(option, scale_factor=1.0):
    """Project costs for different scaling scenarios."""
    
    # Base costs
    base_costs = {
        'inference': option.get('cost_per_1k_tokens', 0) * estimated_tokens,
        'storage': option.get('storage_gb_cost', 0) * estimated_storage,
        'compute': option.get('compute_hour_cost', 0) * estimated_hours,
        'fixed': option.get('monthly_fixed', 0)
    }
    
    # Scale projections
    scenarios = {
        'current': base_costs,
        '10x': {k: v * 10 for k, v in base_costs.items()},
        '100x': {k: v * 100 for k, v in base_costs.items()},
        '1000x': {k: v * 1000 for k, v in base_costs.items()}
    }
    
    return scenarios
```

### LLM Selection Logic
```python
LLM_DECISION_TREE = {
    'reasoning': {
        'complex': 'claude-sonnet',      # Quality critical
        'simple': 'deepseek-v3',         # 95% cheaper
        'local': 'ollama-llama3'         # Free
    },
    'generation': {
        'code': 'claude-sonnet',         # Accuracy matters
        'content': 'deepseek-v3',        # Good enough
        'test': 'qwen-72b'              # Alternative
    },
    'embeddings': {
        'semantic': 'voyage-3',          # Best quality
        'basic': 'jina-embeddings-v3',   # Cheaper
        'local': 'ollama-nomic-embed'    # Free
    },
    'analysis': {
        'financial': 'deepseek-v3',      # Math capable
        'technical': 'claude-sonnet',    # Nuanced
        'summary': 'qwen-72b'           # Fast & cheap
    }
}
```

## Phase 3: Research Execution

### Structured Research Template
```markdown
# Research: [TOPIC]
Date: [DATE]
Researcher: Claude
Time Invested: [X] minutes

## Executive Summary
**One-liner:** [Concise conclusion]
**Recommendation:** [GO/NO-GO]
**Confidence:** [1-10]

## Options Evaluated
1. **Option A** - [Brief description]
   - Pros: [List]
   - Cons: [List]
   - Cost: [$ amount]
   
2. **Option B** - [Brief description]
   - Pros: [List]
   - Cons: [List]
   - Cost: [$ amount]

## Decision Factors
1. **Critical:** [What matters most]
2. **Important:** [Secondary concerns]
3. **Nice-to-have:** [Bonus features]

## Cost Analysis
| Option | Monthly | Yearly | 10x Scale |
|--------|---------|--------|-----------|
| A | $X | $Y | $Z |
| B | $X | $Y | $Z |

## Risk Assessment
- **Technical Risks:** [List]
- **Business Risks:** [List]
- **Mitigation Strategies:** [List]

## Implementation Estimate
- **Time to POC:** [X days]
- **Time to Production:** [Y weeks]
- **Team Resources:** [Z engineers]

## Open Questions
1. [Question needing follow-up]
2. [Uncertain aspect]

## Decision
**Recommended:** [Option X]
**Rationale:** [2-3 sentences]
**Next Steps:** [Concrete actions]
```

### Research Execution Workflow
```bash
#!/bin/bash
# research-workflow.sh

TOPIC="$1"
OUTPUT="RESEARCH_$(date +%Y%m%d_%H%M%S).md"

# Step 1: Local scan
echo "# Research: $TOPIC" > "$OUTPUT"
echo "## Local Repository Findings" >> "$OUTPUT"
./scan-local-repos.sh "$TOPIC" >> "$OUTPUT"

# Step 2: MCP Cookbook
echo "## MCP Cookbook Patterns" >> "$OUTPUT"
./scan-mcp-cookbook.sh "$TOPIC" >> "$OUTPUT"

# Step 3: Web research (using DeepSeek for cost)
echo "## Market Research" >> "$OUTPUT"
# Use research-skill with DeepSeek

# Step 4: Cost projections
echo "## Cost Projections" >> "$OUTPUT"
python project-costs.py "$TOPIC" >> "$OUTPUT"

# Step 5: Generate recommendation
echo "## Recommendation" >> "$OUTPUT"
```

## Phase 4: Decision Gates

### Gate 1: Initial Viability
```python
def initial_viability_check(research):
    """Quick check before deep research."""
    
    checks = {
        'cost_reasonable': research.monthly_cost < budget * 0.2,
        'technically_feasible': research.complexity <= team_capability,
        'time_available': research.implementation_time < deadline,
        'aligns_with_strategy': research.strategic_fit > 7
    }
    
    if not all(checks.values()):
        return "NO-GO", checks
    
    return "PROCEED", checks
```

### Gate 2: Deep Dive Decision
```python
def deep_dive_decision(research):
    """Final decision after thorough research."""
    
    score = 0
    weights = {
        'cost_efficiency': 0.3,
        'technical_fit': 0.25,
        'scalability': 0.2,
        'maintenance': 0.15,
        'team_comfort': 0.1
    }
    
    for factor, weight in weights.items():
        score += research[factor] * weight
    
    decision = "GO" if score >= 7 else "NO-GO"
    confidence = min(10, int(score * 1.2))
    
    return decision, confidence, score
```

### Gate 3: Implementation Review
After POC or initial implementation:
```markdown
## Implementation Review Gate

### POC Results
- **Performance:** [Meets/Exceeds/Below] expectations
- **Cost Actual:** $[X] vs Projected $[Y]
- **Integration Effort:** [Easy/Medium/Hard]
- **Team Feedback:** [Positive/Mixed/Negative]

### Decision
[ ] Proceed to production
[ ] Iterate on POC
[ ] Pivot to alternative
[ ] Abandon approach
```

## Cost Optimization Strategies

### 1. Provider Selection by Use Case
```python
PROVIDER_MATRIX = {
    # Use case -> (primary, fallback, dev)
    'customer_facing': ('claude-sonnet', 'gpt-4', None),
    'internal_tools': ('deepseek-v3', 'qwen-72b', 'ollama'),
    'batch_processing': ('deepseek-v3', 'qwen-72b', 'groq'),
    'embeddings': ('voyage-3', 'jina-v3', 'nomic-embed'),
    'development': ('ollama', 'deepseek-v3', None),
}
```

### 2. Caching Strategy
```python
CACHE_POLICIES = {
    'embeddings': 30 * 24 * 60 * 60,  # 30 days
    'llm_responses': 7 * 24 * 60 * 60,  # 7 days
    'search_results': 24 * 60 * 60,     # 1 day
    'static_analysis': 'forever',       # Never expires
}
```

### 3. Batch vs Streaming
```python
def choose_processing_mode(task):
    if task.latency_sensitive:
        return 'streaming'
    elif task.volume > 1000:
        return 'batch'  # Better pricing
    else:
        return 'standard'
```

## Research Tools Integration

### With /research-skill
```bash
# Trigger research skill for market analysis
echo "Use /research-skill for market analysis of $TOPIC"
```

### With Web Search
```python
# Use DeepSeek for research queries
search_queries = [
    f"{topic} comparison 2024",
    f"{topic} pricing calculator",
    f"{topic} vs alternatives",
    f"{topic} production experience",
    f"{topic} scaling issues"
]
```

### With Cost Tracking
```bash
# Log research costs
RESEARCH_COST=$(calculate_research_cost)
echo "{\"task\": \"research\", \"topic\": \"$TOPIC\", \"cost\": $RESEARCH_COST}" >> costs/by-feature.jsonl
```

## Common Research Patterns

### 1. Framework Selection
```markdown
Research Checklist:
- [ ] Check awesome-{framework} lists
- [ ] Review GitHub stars/issues/activity
- [ ] Find production case studies
- [ ] Evaluate ecosystem (tools, libs)
- [ ] Check job market demand
- [ ] Review upgrade/migration paths
```

### 2. API Provider Evaluation
```markdown
API Checklist:
- [ ] Pricing at current and 10x scale
- [ ] Rate limits and quotas
- [ ] Latency from your regions
- [ ] SDK quality and languages
- [ ] Error handling and retries
- [ ] Data retention policies
```

### 3. Infrastructure Decisions
```markdown
Infrastructure Checklist:
- [ ] Multi-region capabilities
- [ ] Scaling limits and costs
- [ ] Compliance certifications
- [ ] Disaster recovery options
- [ ] Vendor lock-in assessment
- [ ] Migration complexity
```

## Research Artifacts

### 1. Decision Documents
Store in: `docs/decisions/`
```markdown
# ADR-001: Chose Supabase over Firebase

## Status
Accepted

## Context
[Background and requirements]

## Decision
[What we decided]

## Consequences
[What happens as a result]
```

### 2. Comparison Matrices
Store in: `docs/research/`
```markdown
# Provider Comparison: Vector Databases

| Feature | Pinecone | Weaviate | Qdrant | Chroma |
|---------|----------|----------|---------|---------|
| Pricing | $$$ | $$ | $$ | $ |
| Performance | A | B+ | A- | B |
| Ease of Use | A | B | B+ | A |
```

### 3. Cost Models
Store in: `docs/costs/`
```python
# cost_model_embeddings.py
def calculate_embedding_costs(documents, provider='voyage'):
    # Detailed cost calculation model
    pass
```

## Anti-Patterns to Avoid

### 1. Research Paralysis
- Set time box: 2 hours max for initial research
- Use confidence scores, not perfection
- "Good enough" at 80% confidence > Perfect at 95%

### 2. Ignoring Existing Solutions
- Always check your own code first
- Look for similar problems already solved
- Consider adapting existing approach

### 3. Over-Engineering Research
- Simple decisions need simple research
- Not everything needs a formal process
- Use judgment on research depth

### 4. Ignoring Hidden Costs
- Developer time to learn
- Maintenance burden
- Switching costs later
- Operational overhead