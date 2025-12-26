# Feature Development Workflow

Comprehensive guide for multi-phase feature development with parallel execution, security gates, and quality checkpoints.

## Phase 0: Planning & Design

### Feature Brief Template
```markdown
# Feature: [NAME]
**JIRA/Issue:** [LINK]
**Priority:** P0/P1/P2
**Estimated Effort:** [X] days

## Problem Statement
[What problem does this solve?]

## Success Criteria
- [ ] Metric 1 improves by X%
- [ ] User can accomplish Y
- [ ] Performance remains under Zms

## Scope
### In Scope
- [Included functionality]

### Out of Scope
- [Explicitly excluded]

## Technical Approach
[High-level architecture]

## Dependencies
- External: [APIs, services]
- Internal: [Other features]

## Risks
1. [Risk]: [Mitigation]
```

### Agent Mapping
```python
FEATURE_AGENTS = {
    'planning': ['planning-prompts-skill', 'feature-dev:code-architect'],
    'database': ['database-design:schema-design', 'supabase-sql-skill'],
    'backend': ['backend-development:backend-architect', 'python-development:fastapi-pro'],
    'frontend': ['frontend-mobile-development:frontend-developer', 'javascript-typescript:typescript-pro'],
    'testing': ['unit-testing:test-automator', 'tdd-workflows:tdd-orchestrator'],
    'security': ['full-stack-orchestration:security-auditor', 'comprehensive-review:security-auditor'],
    'deployment': ['deployment-strategies:deployment-engineer', 'cicd-automation:deployment-engineer']
}
```

### Parallelization Analysis
```python
def analyze_parallelization(feature_tasks):
    """Identify which tasks can run in parallel."""
    
    dependencies = build_dependency_graph(feature_tasks)
    parallel_groups = []
    
    # Find independent task sets
    for task_set in find_independent_sets(dependencies):
        if len(task_set) > 1:
            parallel_groups.append({
                'tasks': task_set,
                'worktrees_needed': len(task_set),
                'estimated_time': max(t.estimate for t in task_set)
            })
    
    return parallel_groups
```

### Cost Estimation
```python
def estimate_feature_cost(feature_plan):
    """Estimate total cost for feature development."""
    
    costs = {
        'development': {
            'hours': feature_plan.dev_hours,
            'llm_calls': feature_plan.dev_hours * 50,  # Avg 50 LLM calls/hour
            'cost': feature_plan.dev_hours * 50 * 0.003  # Claude rate
        },
        'testing': {
            'hours': feature_plan.test_hours,
            'llm_calls': feature_plan.test_hours * 30,
            'cost': feature_plan.test_hours * 30 * 0.00014  # DeepSeek for tests
        },
        'infrastructure': {
            'database': 0,  # Supabase free tier
            'compute': feature_plan.compute_hours * 0.50,  # RunPod estimate
            'storage': feature_plan.storage_gb * 0.02
        }
    }
    
    total = sum(c['cost'] for c in costs.values())
    return costs, total
```

## Phase 1: Database & Schema

### Schema Design Checklist
```markdown
- [ ] Entity relationship diagram created
- [ ] Indexes identified for common queries
- [ ] RLS policies defined
- [ ] Migration rollback plan
- [ ] Test data generation strategy
```

### Database Setup Flow
```bash
# 1. Design schema
/database-design:schema-design

# 2. Create migration
/supabase-sql-skill

# 3. Review generated SQL
cat migrations/$(date +%Y%m%d)_feature_name.sql

# 4. Test in development
supabase db reset
supabase db push

# 5. Verify with test queries
psql $DATABASE_URL < test/queries/feature_verification.sql
```

### RLS Policy Template
```sql
-- Row Level Security for feature tables
CREATE POLICY "Users can view own data"
ON feature_table
FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own data"
ON feature_table
FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own data"
ON feature_table
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Enable RLS
ALTER TABLE feature_table ENABLE ROW LEVEL SECURITY;
```

**Gate: Schema Review Required** ⛔
- [ ] Naming conventions followed
- [ ] Proper indexes in place
- [ ] RLS policies comprehensive
- [ ] No performance anti-patterns

## Phase 2: Parallel Implementation

### Worktree Orchestration
```bash
#!/bin/bash
# parallel-feature-setup.sh

PROJECT=$(basename $(pwd))
FEATURE="feature-name"
BASE_PORT=8100

# Create worktrees for parallel development
create_worktree() {
    local name=$1
    local port=$2
    
    echo "Creating worktree: $name (ports: $port, $((port+1)))"
    git worktree add -b "$FEATURE-$name" ~/tmp/worktrees/$PROJECT/$name
    
    # Register in worktree registry
    update_registry "$PROJECT" "$FEATURE-$name" "$port" "$((port+1))"
    
    # Copy environment
    cp .env ~/tmp/worktrees/$PROJECT/$name/.env
    
    # Update ports in .env
    sed -i "s/PORT=.*/PORT=$port/" ~/tmp/worktrees/$PROJECT/$name/.env
}

# Spawn parallel worktrees
create_worktree "backend" $BASE_PORT
create_worktree "frontend" $((BASE_PORT+2))
create_worktree "tests" $((BASE_PORT+4))
```

### Port Management
```python
class PortAllocator:
    """Manage port allocation for parallel development."""
    
    PORT_POOL = range(8100, 8200, 2)  # Even numbers, pairs reserved
    
    def __init__(self, registry_path="~/.claude/worktree-registry.json"):
        self.registry = self.load_registry(registry_path)
    
    def allocate_ports(self, count=2):
        """Allocate consecutive ports for a worktree."""
        used_ports = self.get_used_ports()
        
        for port in self.PORT_POOL:
            if port not in used_ports and port+1 not in used_ports:
                if self.check_ports_free(port, count):
                    return list(range(port, port+count))
        
        raise Exception("No available port pairs")
    
    def check_ports_free(self, start_port, count):
        """Verify ports are actually free on system."""
        for port in range(start_port, start_port+count):
            if self.is_port_in_use(port):
                return False
        return True
```

### Task Distribution
```markdown
## Worktree A: Backend API
**Branch:** feature/api-backend
**Ports:** 8100 (API), 8101 (Debug)
**Agent:** backend-development:backend-architect

Tasks:
1. Create API endpoints
2. Implement business logic
3. Add authentication
4. Create integration tests

## Worktree B: Frontend UI
**Branch:** feature/ui
**Ports:** 8102 (Dev), 8103 (Storybook)
**Agent:** frontend-mobile-development:frontend-developer

Tasks:
1. Create components
2. Implement state management
3. Connect to API
4. Add loading/error states

## Worktree C: Testing
**Branch:** feature/tests
**Ports:** 8104 (Test server), 8105 (Coverage)
**Agent:** unit-testing:test-automator

Tasks:
1. Unit test suite
2. Integration tests
3. E2E test scenarios
4. Performance benchmarks
```

### Progress Synchronization
```python
def sync_worktree_progress():
    """Monitor and sync progress across worktrees."""
    
    status = {}
    
    for worktree in get_active_worktrees():
        # Check git status
        branch_status = check_git_status(worktree.path)
        
        # Check test status
        test_status = run_tests(worktree.path, quiet=True)
        
        # Check TODO completion
        todo_status = get_todo_progress(worktree.branch)
        
        status[worktree.name] = {
            'commits': branch_status['ahead'],
            'changes': branch_status['changes'],
            'tests': test_status['passing'],
            'todos': todo_status['completed_percent'],
            'blockers': identify_blockers(worktree)
        }
    
    return status
```

## Phase 3: Security & Quality Gates

### Security Scan Pipeline
```bash
#!/bin/bash
# security-scan.sh

echo "=== Security Scan Pipeline ==="

# 1. SAST Analysis
echo "[1/4] Running SAST..."
semgrep --config auto . --json -o security/sast-report.json
SAST_CRITICAL=$(jq '.results | map(select(.extra.severity == "ERROR")) | length' security/sast-report.json)

# 2. Secrets Detection
echo "[2/4] Scanning for secrets..."
gitleaks detect --source . --report-path security/secrets-report.json
SECRETS_FOUND=$(jq '.SecretsFound' security/secrets-report.json)

# 3. Dependency Audit
echo "[3/4] Auditing dependencies..."
if [ -f "package.json" ]; then
    npm audit --json > security/npm-audit.json
    VULN_CRITICAL=$(jq '.metadata.vulnerabilities.critical' security/npm-audit.json)
elif [ -f "requirements.txt" ]; then
    pip-audit --format json > security/pip-audit.json
    VULN_CRITICAL=$(jq '[.vulnerabilities[].fix_versions] | length' security/pip-audit.json)
fi

# 4. Code Coverage
echo "[4/4] Checking test coverage..."
if [ -f "package.json" ]; then
    npm test -- --coverage --json > test/coverage.json
    COVERAGE=$(jq '.total.lines.pct' test/coverage.json)
else
    pytest --cov=src --cov-report=json
    COVERAGE=$(jq '.totals.percent_covered' coverage.json)
fi

# Gate evaluation
GATE_PASSED=true
REASONS=()

if [ "$SAST_CRITICAL" -gt 0 ]; then
    GATE_PASSED=false
    REASONS+=("$SAST_CRITICAL critical SAST findings")
fi

if [ "$SECRETS_FOUND" = "true" ]; then
    GATE_PASSED=false
    REASONS+=("Secrets detected in code")
fi

if [ "$VULN_CRITICAL" -gt 0 ]; then
    GATE_PASSED=false
    REASONS+=("$VULN_CRITICAL critical vulnerabilities")
fi

if (( $(echo "$COVERAGE < 80" | bc -l) )); then
    GATE_PASSED=false
    REASONS+=("Coverage below 80% (actual: $COVERAGE%)")
fi

# Report
if [ "$GATE_PASSED" = true ]; then
    echo "✅ All security gates PASSED"
else
    echo "❌ Security gates FAILED:"
    printf '%s\n' "${REASONS[@]}"
    exit 1
fi
```

### Quality Metrics
```python
class QualityGates:
    """Enforce quality standards before merge."""
    
    THRESHOLDS = {
        'test_coverage': 80,
        'code_duplication': 5,  # Max 5% duplication
        'cyclomatic_complexity': 10,
        'lint_errors': 0,
        'type_coverage': 90,  # For TypeScript
        'bundle_size_increase': 5  # Max 5% increase
    }
    
    def check_all_gates(self, metrics):
        results = {}
        
        for metric, threshold in self.THRESHOLDS.items():
            if metric in metrics:
                passed = self.check_metric(metric, metrics[metric], threshold)
                results[metric] = {
                    'passed': passed,
                    'value': metrics[metric],
                    'threshold': threshold
                }
        
        return results
    
    def check_metric(self, metric, value, threshold):
        if metric in ['test_coverage', 'type_coverage']:
            return value >= threshold
        elif metric in ['code_duplication', 'cyclomatic_complexity', 'lint_errors', 'bundle_size_increase']:
            return value <= threshold
        return True
```

### Integration Testing
```python
# integration_test_template.py

import pytest
from httpx import AsyncClient

class TestFeatureIntegration:
    """Integration tests for new feature."""
    
    @pytest.fixture
    async def client(self):
        async with AsyncClient(base_url="http://localhost:8100") as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_full_user_journey(self, client):
        """Test complete user journey through feature."""
        # 1. Create user
        user_response = await client.post("/auth/register", json={...})
        assert user_response.status_code == 201
        
        # 2. Authenticate
        token = user_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Use feature
        feature_response = await client.post(
            "/api/feature",
            json={...},
            headers=headers
        )
        assert feature_response.status_code == 200
        
        # 4. Verify side effects
        verify_response = await client.get(
            f"/api/feature/{feature_response.json()['id']}",
            headers=headers
        )
        assert verify_response.json()["status"] == "completed"
```

## Phase 4: Ship & Deploy

### Pre-Deploy Checklist
```markdown
## Deployment Readiness Checklist

### Code Quality
- [ ] All tests passing
- [ ] Security scan clean
- [ ] Code review approved
- [ ] Documentation updated

### Performance
- [ ] Load tested at expected scale
- [ ] Database queries optimized
- [ ] Caching strategy implemented
- [ ] CDN configured for assets

### Monitoring
- [ ] Metrics instrumented
- [ ] Alerts configured
- [ ] Error tracking enabled
- [ ] Logs structured

### Rollback Plan
- [ ] Feature flag created
- [ ] Database rollback tested
- [ ] Canary deployment ready
- [ ] Incident response plan

### Documentation
- [ ] API docs updated
- [ ] User guides created
- [ ] Team runbook updated
- [ ] Architecture diagram current
```

### Deployment Pipeline
```yaml
# .github/workflows/deploy-feature.yml
name: Deploy Feature

on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  deploy:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Run Security Gates
      run: ./scripts/security-scan.sh
    
    - name: Deploy Database Migrations
      run: |
        supabase db push --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
    
    - name: Deploy Backend
      run: |
        docker build -t feature-api .
        docker push $REGISTRY/feature-api:${{ github.sha }}
        kubectl set image deployment/api api=$REGISTRY/feature-api:${{ github.sha }}
    
    - name: Deploy Frontend
      run: |
        npm run build
        vercel --prod
    
    - name: Run Smoke Tests
      run: |
        npm run test:e2e:smoke
    
    - name: Update Feature Flags
      run: |
        # Enable feature for 10% of users
        curl -X PATCH $FEATURE_FLAG_API/features/new-feature \
          -H "Authorization: Bearer ${{ secrets.FF_TOKEN }}" \
          -d '{"rollout_percentage": 10}'
```

### Cost Logging
```python
def log_feature_cost(feature_name, actual_costs):
    """Log actual costs for feature development."""
    
    entry = {
        'feature': feature_name,
        'date': datetime.now().isoformat(),
        'costs': {
            'development_hours': actual_costs['dev_hours'],
            'llm_tokens': actual_costs['llm_tokens'],
            'llm_cost': actual_costs['llm_cost'],
            'infrastructure': actual_costs['infra_cost'],
            'total': sum(actual_costs.values())
        },
        'roi_metrics': {
            'users_impacted': get_feature_usage(feature_name),
            'revenue_impact': estimate_revenue_impact(feature_name),
            'cost_per_user': actual_costs['total'] / get_feature_usage(feature_name)
        }
    }
    
    # Append to cost log
    with open('costs/by-feature.jsonl', 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    # Update feature documentation
    update_feature_docs(feature_name, entry)
```

## Merge & Cleanup

### Merge Strategy
```bash
#!/bin/bash
# merge-feature-branches.sh

FEATURE="feature-name"

# 1. Merge backend
git checkout main
git merge --no-ff "$FEATURE-backend" -m "feat(backend): Add $FEATURE API endpoints"

# 2. Merge frontend
git merge --no-ff "$FEATURE-frontend" -m "feat(frontend): Add $FEATURE UI components"

# 3. Merge tests
git merge --no-ff "$FEATURE-tests" -m "test: Add $FEATURE test suite"

# 4. Tag release
git tag -a "v1.2.0-$FEATURE" -m "Release: $FEATURE feature"

# 5. Clean up worktrees
for worktree in backend frontend tests; do
    git worktree remove ~/tmp/worktrees/$PROJECT/$worktree
done

# 6. Update registry
update_registry --remove "$FEATURE-*"
```

### Documentation Updates
```markdown
## Updates Required

1. **CLAUDE.md**
   - Add new patterns learned
   - Document architectural decisions
   - Note performance considerations

2. **PLANNING.md**
   - Move feature to completed
   - Update roadmap progress
   - Note any scope changes

3. **README.md**
   - Add feature to feature list
   - Update setup instructions if needed
   - Add configuration examples

4. **API Documentation**
   - New endpoints
   - Request/response examples
   - Error codes

5. **Architecture Docs**
   - Update diagrams
   - Document new components
   - Explain design decisions
```

## Common Patterns

### 1. API Endpoint Pattern
```python
# Standard API endpoint structure
@router.post("/feature", response_model=FeatureResponse)
async def create_feature(
    request: FeatureRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache),
    metrics: MetricsClient = Depends(get_metrics)
):
    """Create new feature with standard patterns."""
    
    # Input validation
    await validate_feature_request(request, current_user)
    
    # Business logic
    with metrics.timer("feature.create"):
        feature = await feature_service.create(
            db=db,
            user=current_user,
            data=request
        )
    
    # Cache invalidation
    await cache.delete(f"user:{current_user.id}:features")
    
    # Event emission
    await emit_event("feature.created", {
        "user_id": current_user.id,
        "feature_id": feature.id
    })
    
    return feature
```

### 2. Frontend Component Pattern
```typescript
// Standard React component structure
export const FeatureComponent: React.FC<FeatureProps> = ({ 
    initialData,
    onSuccess,
    onError 
}) => {
    // State management
    const [state, dispatch] = useReducer(featureReducer, initialState);
    const queryClient = useQueryClient();
    
    // Data fetching
    const { data, isLoading, error } = useQuery({
        queryKey: ['feature', initialData?.id],
        queryFn: () => fetchFeature(initialData?.id),
        enabled: !!initialData?.id
    });
    
    // Mutations
    const createMutation = useMutation({
        mutationFn: createFeature,
        onSuccess: (data) => {
            queryClient.invalidateQueries(['features']);
            onSuccess?.(data);
        },
        onError: (error) => {
            console.error('Feature creation failed:', error);
            onError?.(error);
        }
    });
    
    // Error boundary
    if (error) return <ErrorDisplay error={error} />;
    
    // Loading state
    if (isLoading) return <FeatureSkeleton />;
    
    // Render
    return (
        <FeatureProvider value={{ state, dispatch }}>
            <FeatureUI data={data} onCreate={createMutation.mutate} />
        </FeatureProvider>
    );
};
```

### 3. Test Pattern
```python
# Standard test structure
class TestFeature:
    """Comprehensive test suite for feature."""
    
    @pytest.fixture
    def feature_data(self):
        """Standard test data."""
        return {
            "name": "Test Feature",
            "config": {"enabled": True}
        }
    
    def test_create_success(self, client, auth_headers, feature_data):
        """Test successful creation."""
        response = client.post(
            "/api/feature",
            json=feature_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["name"] == feature_data["name"]
    
    def test_create_validation(self, client, auth_headers):
        """Test input validation."""
        response = client.post(
            "/api/feature",
            json={"invalid": "data"},
            headers=auth_headers
        )
        
        assert response.status_code == 422
        assert "validation_error" in response.json()["detail"]
    
    def test_create_unauthorized(self, client, feature_data):
        """Test authentication required."""
        response = client.post("/api/feature", json=feature_data)
        assert response.status_code == 401
```