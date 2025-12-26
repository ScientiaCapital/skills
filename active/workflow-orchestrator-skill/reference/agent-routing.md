# Agent Routing Guide

Complete reference for 70+ specialized agents with intelligent routing logic and optimal selection strategies.

## Agent Categories Overview

### Core Development Agents
- **Debugging & Error Handling** (8 agents)
- **Code Review & Quality** (10 agents)
- **Testing & TDD** (6 agents)
- **Documentation** (7 agents)

### Specialized Development
- **Language Experts** (8 agents)
- **Frontend & Mobile** (2 agents)
- **Backend & Architecture** (6 agents)
- **Infrastructure & DevOps** (15 agents)

### Advanced Capabilities
- **AI & LLM Development** (2 agents)
- **Performance & Optimization** (6 agents)
- **Security & Compliance** (3 agents)
- **Refactoring & Modernization** (2 agents)

## Intelligent Agent Selection

### Selection Algorithm
```python
class AgentSelector:
    """Intelligent agent selection based on task analysis."""
    
    def __init__(self):
        self.agent_catalog = self.load_agent_catalog()
        self.usage_history = self.load_usage_history()
        self.performance_metrics = self.load_performance_metrics()
        
    def select_optimal_agent(self, task_description, context=None):
        """Select the most appropriate agent for a task."""
        
        # 1. Extract task features
        features = self.extract_task_features(task_description)
        
        # 2. Find candidate agents
        candidates = self.find_candidate_agents(features)
        
        # 3. Score candidates
        scored_candidates = []
        for agent in candidates:
            score = self.score_agent(agent, features, context)
            scored_candidates.append((agent, score))
            
        # 4. Select best agent
        best_agent = max(scored_candidates, key=lambda x: x[1])
        
        # 5. Log selection
        self.log_selection(task_description, best_agent[0], best_agent[1])
        
        return best_agent[0]
        
    def extract_task_features(self, description):
        """Extract features from task description."""
        features = {
            'keywords': self.extract_keywords(description),
            'task_type': self.classify_task_type(description),
            'complexity': self.estimate_complexity(description),
            'domain': self.identify_domain(description),
            'urgency': self.detect_urgency(description),
        }
        return features
        
    def score_agent(self, agent, features, context):
        """Score agent fitness for task."""
        score = 0
        
        # Keyword match (40 points)
        keyword_matches = len(
            set(features['keywords']) & set(agent['keywords'])
        )
        score += min(keyword_matches * 10, 40)
        
        # Task type match (30 points)
        if features['task_type'] in agent['specialties']:
            score += 30
        elif features['task_type'] in agent['capabilities']:
            score += 15
            
        # Past performance (20 points)
        performance = self.get_agent_performance(agent['id'])
        score += performance * 20
        
        # Context relevance (10 points)
        if context and self.is_context_relevant(agent, context):
            score += 10
            
        return score
```

### Task Type Classification
```python
TASK_PATTERNS = {
    'debugging': [
        'error', 'bug', 'fix', 'broken', 'failing', 'crash',
        'exception', 'stack trace', 'not working', 'issue'
    ],
    'code_review': [
        'review', 'check', 'audit', 'quality', 'feedback',
        'improvement', 'refactor', 'clean', 'best practice'
    ],
    'testing': [
        'test', 'unittest', 'integration', 'e2e', 'coverage',
        'pytest', 'jest', 'mock', 'assertion', 'tdd'
    ],
    'performance': [
        'slow', 'performance', 'optimize', 'speed', 'latency',
        'memory', 'cpu', 'bottleneck', 'profile', 'benchmark'
    ],
    'security': [
        'security', 'vulnerability', 'exploit', 'auth', 'encryption',
        'xss', 'sql injection', 'csrf', 'penetration', 'audit'
    ],
    'deployment': [
        'deploy', 'ci/cd', 'pipeline', 'release', 'production',
        'kubernetes', 'docker', 'terraform', 'aws', 'cloud'
    ],
    'architecture': [
        'architecture', 'design', 'pattern', 'structure', 'scalability',
        'microservices', 'monolith', 'api', 'schema', 'diagram'
    ],
}
```

## Complete Agent Catalog

### Debugging & Error Handling Agents

#### debugging-toolkit:debugger
**Specialties:** General debugging, test failures, runtime errors
**Best for:** Any error investigation, systematic debugging
**Keywords:** error, bug, debug, trace, investigate, fix
```bash
Task debugging-toolkit:debugger "Debug authentication error in login flow"
```

#### error-debugging:error-detective
**Specialties:** Log analysis, error pattern detection
**Best for:** Finding error patterns across distributed systems
**Keywords:** logs, patterns, correlation, search, analyze
```bash
Task error-debugging:error-detective "Search logs for connection timeout patterns"
```

#### distributed-debugging:devops-troubleshooter
**Specialties:** Production incidents, distributed systems
**Best for:** Complex multi-service debugging, incident response
**Keywords:** incident, production, distributed, microservices, outage
```bash
Task distributed-debugging:devops-troubleshooter "Investigate service mesh communication failure"
```

### Code Review & Quality Agents

#### code-documentation:code-reviewer
**Specialties:** Elite code review, security vulnerabilities
**Best for:** Critical code paths, security-sensitive changes
**Keywords:** review, security, vulnerability, quality, audit
```bash
Task code-documentation:code-reviewer "Review authentication middleware for vulnerabilities"
```

#### comprehensive-review:architect-review
**Specialties:** Architecture review, design patterns
**Best for:** System design reviews, major refactoring
**Keywords:** architecture, design, patterns, structure, scalability
```bash
Task comprehensive-review:architect-review "Review microservices communication architecture"
```

#### git-pr-workflows:code-reviewer
**Specialties:** Pull request reviews, git workflows
**Best for:** Standard PR reviews, merge conflict resolution
**Keywords:** pr, pull request, git, merge, branch
```bash
Task git-pr-workflows:code-reviewer "Review feature branch PR #123"
```

### Testing & TDD Agents

#### unit-testing:test-automator
**Specialties:** Test automation, coverage improvement
**Best for:** Writing comprehensive test suites
**Keywords:** test, unit, coverage, pytest, jest, mock
```bash
Task unit-testing:test-automator "Create test suite for payment processing module"
```

#### tdd-workflows:tdd-orchestrator
**Specialties:** Test-driven development workflows
**Best for:** Implementing features using TDD methodology
**Keywords:** tdd, red-green-refactor, test-first
```bash
Task tdd-workflows:tdd-orchestrator "Implement user registration with TDD approach"
```

#### performance-testing-review:test-automator
**Specialties:** Performance testing, load testing
**Best for:** Creating performance test suites
**Keywords:** performance, load, stress, benchmark, latency
```bash
Task performance-testing-review:test-automator "Create load tests for API endpoints"
```

### Documentation Agents

#### documentation-generation:docs-architect
**Specialties:** System documentation, architecture guides
**Best for:** Comprehensive technical documentation
**Keywords:** documentation, architecture, guide, manual, readme
```bash
Task documentation-generation:docs-architect "Create system architecture documentation"
```

#### documentation-generation:api-documenter
**Specialties:** API documentation, OpenAPI specs
**Best for:** REST/GraphQL API documentation
**Keywords:** api, openapi, swagger, rest, graphql, endpoints
```bash
Task documentation-generation:api-documenter "Generate OpenAPI spec for user service"
```

#### documentation-generation:tutorial-engineer
**Specialties:** Tutorials, onboarding guides
**Best for:** Step-by-step tutorials, user guides
**Keywords:** tutorial, guide, howto, onboarding, walkthrough
```bash
Task documentation-generation:tutorial-engineer "Create getting started tutorial"
```

### Language-Specific Experts

#### python-development:python-pro
**Specialties:** Modern Python, async, type hints
**Best for:** Python 3.12+ development, async patterns
**Keywords:** python, async, asyncio, type hints, dataclasses
```bash
Task python-development:python-pro "Refactor sync code to use async/await"
```

#### javascript-typescript:typescript-pro
**Specialties:** TypeScript, advanced types, generics
**Best for:** Complex TypeScript systems, type safety
**Keywords:** typescript, types, generics, interfaces, strict
```bash
Task javascript-typescript:typescript-pro "Add strict typing to React components"
```

#### python-development:fastapi-pro
**Specialties:** FastAPI, async APIs, microservices
**Best for:** High-performance Python APIs
**Keywords:** fastapi, api, async, pydantic, microservices
```bash
Task python-development:fastapi-pro "Build async REST API with FastAPI"
```

### Infrastructure & DevOps

#### deployment-strategies:deployment-engineer
**Specialties:** CI/CD pipelines, deployment automation
**Best for:** Setting up deployment pipelines
**Keywords:** deploy, ci/cd, pipeline, automation, release
```bash
Task deployment-strategies:deployment-engineer "Create GitHub Actions deployment pipeline"
```

#### cicd-automation:kubernetes-architect
**Specialties:** Kubernetes, GitOps, service mesh
**Best for:** K8s deployments, cluster management
**Keywords:** kubernetes, k8s, gitops, helm, cluster
```bash
Task cicd-automation:kubernetes-architect "Design K8s deployment for microservices"
```

#### deployment-strategies:terraform-specialist
**Specialties:** Infrastructure as Code, Terraform
**Best for:** Cloud infrastructure automation
**Keywords:** terraform, iac, infrastructure, aws, cloud
```bash
Task deployment-strategies:terraform-specialist "Create Terraform modules for AWS setup"
```

### Performance & Optimization

#### observability-monitoring:performance-engineer
**Specialties:** APM, performance optimization
**Best for:** Application performance issues
**Keywords:** performance, apm, monitoring, metrics, optimization
```bash
Task observability-monitoring:performance-engineer "Optimize API response times"
```

#### observability-monitoring:database-optimizer
**Specialties:** Database performance tuning
**Best for:** Query optimization, indexing strategies
**Keywords:** database, query, index, performance, sql
```bash
Task observability-monitoring:database-optimizer "Optimize slow database queries"
```

### Security & Compliance

#### full-stack-orchestration:security-auditor
**Specialties:** Security audits, compliance, DevSecOps
**Best for:** Comprehensive security reviews
**Keywords:** security, audit, compliance, vulnerability, pentest
```bash
Task full-stack-orchestration:security-auditor "Perform security audit on API endpoints"
```

#### data-validation-suite:backend-security-coder
**Specialties:** Secure coding, input validation
**Best for:** Implementing security features
**Keywords:** validation, sanitization, security, auth, encryption
```bash
Task data-validation-suite:backend-security-coder "Implement secure user input handling"
```

### AI & LLM Development

#### llm-application-dev:ai-engineer
**Specialties:** LLM applications, RAG systems
**Best for:** Building AI-powered features
**Keywords:** llm, ai, rag, embeddings, vector, gpt
```bash
Task llm-application-dev:ai-engineer "Build RAG system for documentation search"
```

#### llm-application-dev:prompt-engineer
**Specialties:** Prompt optimization, LLM tuning
**Best for:** Improving LLM performance
**Keywords:** prompt, optimization, llm, tuning, few-shot
```bash
Task llm-application-dev:prompt-engineer "Optimize prompts for code generation"
```

## Agent Routing Patterns

### Pattern 1: Cascading Expertise
```python
def cascade_agents(task):
    """Use multiple agents in sequence for complex tasks."""
    
    # Start with general agent
    initial_analysis = Task(
        "error-debugging:debugger",
        f"Initial analysis: {task}"
    )
    
    # Route to specialist based on findings
    if "performance" in initial_analysis:
        return Task(
            "observability-monitoring:performance-engineer",
            f"Deep dive: {task}"
        )
    elif "security" in initial_analysis:
        return Task(
            "full-stack-orchestration:security-auditor",
            f"Security analysis: {task}"
        )
    # ... continue routing
```

### Pattern 2: Parallel Expertise
```python
def parallel_review(code_change):
    """Use multiple agents in parallel for comprehensive review."""
    
    reviews = []
    
    # Security review
    reviews.append(Task(
        "code-documentation:code-reviewer",
        f"Security review: {code_change}",
        async=True
    ))
    
    # Performance review
    reviews.append(Task(
        "performance-testing-review:performance-engineer",
        f"Performance impact: {code_change}",
        async=True
    ))
    
    # Architecture review
    reviews.append(Task(
        "comprehensive-review:architect-review",
        f"Architecture compliance: {code_change}",
        async=True
    ))
    
    return await_all(reviews)
```

### Pattern 3: Domain-Specific Routing
```python
DOMAIN_AGENTS = {
    'auth': 'data-validation-suite:backend-security-coder',
    'api': 'python-development:fastapi-pro',
    'database': 'observability-monitoring:database-optimizer',
    'frontend': 'frontend-mobile-development:frontend-developer',
    'deployment': 'deployment-strategies:deployment-engineer',
    'testing': 'unit-testing:test-automator',
}

def route_by_domain(task, file_path):
    """Route based on code domain."""
    
    domain = identify_domain(file_path)
    agent = DOMAIN_AGENTS.get(domain, 'general-purpose')
    
    return Task(agent, task)
```

## Agent Performance Tracking

### Metrics Collection
```python
class AgentMetrics:
    """Track agent performance metrics."""
    
    def __init__(self):
        self.metrics_db = "~/.claude/agent-metrics.db"
        
    def track_usage(self, agent, task, outcome):
        """Track agent usage and outcomes."""
        
        metrics = {
            'agent': agent,
            'task_type': classify_task(task),
            'timestamp': datetime.now().isoformat(),
            'duration': outcome.get('duration'),
            'success': outcome.get('success'),
            'user_satisfaction': outcome.get('satisfaction'),
            'tokens_used': outcome.get('tokens'),
            'cost': outcome.get('cost'),
        }
        
        self.save_metrics(metrics)
        
    def get_agent_stats(self, agent):
        """Get performance stats for agent."""
        
        stats = self.query_metrics(agent)
        
        return {
            'usage_count': len(stats),
            'success_rate': sum(s['success'] for s in stats) / len(stats),
            'avg_duration': sum(s['duration'] for s in stats) / len(stats),
            'avg_satisfaction': sum(s['satisfaction'] for s in stats) / len(stats),
            'total_cost': sum(s['cost'] for s in stats),
            'common_tasks': self.get_common_tasks(stats),
        }
```

### Agent Recommendation Engine
```python
class AgentRecommender:
    """Recommend optimal agents based on history."""
    
    def __init__(self):
        self.metrics = AgentMetrics()
        self.ml_model = self.load_recommendation_model()
        
    def recommend_agents(self, task_description, top_k=3):
        """Recommend top K agents for task."""
        
        # Feature extraction
        features = self.extract_features(task_description)
        
        # Get predictions from ML model
        predictions = self.ml_model.predict(features)
        
        # Combine with rule-based recommendations
        rule_based = self.get_rule_based_recommendations(task_description)
        
        # Weighted combination
        final_scores = self.combine_recommendations(
            predictions, rule_based, weights=[0.7, 0.3]
        )
        
        # Return top K
        return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
```

## Quick Decision Trees

### Debugging Decision Tree
```
Error/Bug Detected?
├── Production incident? → distributed-debugging:devops-troubleshooter
├── Test failure? → unit-testing:debugger
├── Performance issue? → observability-monitoring:performance-engineer
├── Security concern? → full-stack-orchestration:security-auditor
└── General debugging → debugging-toolkit:debugger
```

### Development Decision Tree
```
New Development Task?
├── API Development?
│   ├── Python → python-development:fastapi-pro
│   ├── Node.js → javascript-typescript:javascript-pro
│   └── GraphQL → backend-development:graphql-architect
├── Frontend Development?
│   ├── React/Next.js → frontend-mobile-development:frontend-developer
│   └── Mobile → frontend-mobile-development:mobile-developer
├── Database Work?
│   ├── Schema Design → database-design:schema-design
│   └── Optimization → observability-monitoring:database-optimizer
└── Infrastructure?
    ├── Kubernetes → cicd-automation:kubernetes-architect
    ├── Terraform → deployment-strategies:terraform-specialist
    └── CI/CD → deployment-strategies:deployment-engineer
```

## Agent Chaining Examples

### Example 1: Full Feature Development
```python
# 1. Architecture design
architect = Task("feature-dev:code-architect", "Design user authentication system")

# 2. Implementation
backend = Task("python-development:fastapi-pro", "Implement auth API based on design")
frontend = Task("frontend-mobile-development:frontend-developer", "Build auth UI components")

# 3. Testing
tests = Task("unit-testing:test-automator", "Create comprehensive test suite")

# 4. Security review
security = Task("full-stack-orchestration:security-auditor", "Audit auth implementation")

# 5. Documentation
docs = Task("documentation-generation:api-documenter", "Document auth API endpoints")
```

### Example 2: Production Issue Resolution
```python
# 1. Initial investigation
investigate = Task("distributed-debugging:devops-troubleshooter", "Investigate service outage")

# 2. Root cause analysis
if "database" in investigate.findings:
    analyze = Task("observability-monitoring:database-optimizer", "Analyze DB performance")
elif "memory" in investigate.findings:
    analyze = Task("observability-monitoring:performance-engineer", "Profile memory usage")

# 3. Fix implementation
fix = Task("error-debugging:debugger", f"Fix root cause: {analyze.root_cause}")

# 4. Preventive measures
prevent = Task("incident-response:incident-responder", "Create runbook for future incidents")
```

## Best Practices

### 1. Agent Selection
- Start with specialized agents over general-purpose
- Use domain experts for domain-specific tasks
- Chain agents for complex workflows
- Parallelize independent agent tasks

### 2. Cost Optimization
- Use lighter agents for simple tasks
- Cache agent responses when possible
- Batch similar requests to same agent
- Monitor agent token usage

### 3. Quality Assurance
- Always use review agents for critical changes
- Chain testing agents after implementation
- Use security agents for sensitive features
- Document agent decisions and rationale

### 4. Performance
- Track agent response times
- Identify slow agents for optimization
- Use async calls for parallel execution
- Set appropriate timeouts per agent type