# Debug Methodology

Systematic debugging approach with evidence gathering, hypothesis testing, and root cause analysis.

## Core Principles

### 1. No Drive-By Fixes
**Rule:** If you can't explain WHY something is broken, you can't properly fix it.

Bad approach:
```python
# "Let me just try adding this..."
try:
    result = problematic_function()
except:
    result = None  # This might work?
```

Good approach:
```python
# Evidence: Stack trace shows KeyError on line 42
# Root cause: API response missing expected field when user not authenticated
# Fix: Add proper validation before access
if not response.get('user_data'):
    raise AuthenticationError("User data missing - authentication required")
result = response['user_data']['profile']
```

### 2. Evidence-Based Debugging
Document everything BEFORE attempting fixes:

```markdown
## Debug Session: [Issue Name]
Started: [Timestamp]

### 1. Observable Symptoms
- Error message: `TypeError: cannot read property 'map' of undefined`
- Occurs when: User clicks "Load More" button
- Frequency: Intermittent (~30% of attempts)
- First reported: 2 days ago

### 2. Environment
- Browser: Chrome 120.0.6099.129
- OS: macOS 14.2
- API Version: v2.1.3
- Last deployment: 3 days ago

### 3. Reproduction Steps
1. Login as test user
2. Navigate to /dashboard
3. Scroll to bottom
4. Click "Load More" → Error occurs

### 4. Initial Observations
- Works on first page load
- Fails on subsequent loads
- API returns 200 but sometimes empty array
```

### 3. One Variable at a Time
**Never change multiple things simultaneously.**

```python
# BAD: Multiple changes
def debug_issue():
    # Changed API endpoint AND error handling AND retry logic
    response = call_new_api()  # Change 1
    with_retries = add_retry_logic(response)  # Change 2  
    formatted = new_error_handler(with_retries)  # Change 3
    return formatted

# GOOD: Isolate changes
def debug_issue_step1():
    # Test ONLY endpoint change
    response = call_new_api()
    return old_error_handler(response)

# If that works, then test next change...
```

### 4. Systematic Hypothesis Testing
```python
class DebugHypothesis:
    """Structure for systematic debugging."""
    
    def __init__(self, description, evidence, test_method):
        self.description = description
        self.evidence = evidence
        self.test_method = test_method
        self.result = None
        
    def test(self):
        """Execute test and record result."""
        print(f"Testing: {self.description}")
        print(f"Evidence: {self.evidence}")
        
        self.result = self.test_method()
        
        print(f"Result: {'CONFIRMED' if self.result else 'REJECTED'}")
        return self.result

# Example usage
hypotheses = [
    DebugHypothesis(
        "Race condition in state update",
        "Error only occurs on fast clicking",
        lambda: test_with_debounce()
    ),
    DebugHypothesis(
        "Cache corruption",
        "Works after clearing browser cache",
        lambda: test_with_fresh_cache()
    ),
]

for h in hypotheses:
    if h.test():
        print(f"Root cause found: {h.description}")
        break
```

## Debug Workflow Stages

### Stage 1: Information Gathering

#### Automated Context Collection
```bash
#!/bin/bash
# debug-context.sh

echo "=== Debug Context Collection ==="
echo "Timestamp: $(date -Iseconds)"

# System info
echo -e "\n## System"
uname -a
echo "Node: $(node --version 2>/dev/null || echo 'Not installed')"
echo "Python: $(python3 --version 2>/dev/null || echo 'Not installed')"

# Project info
echo -e "\n## Project"
pwd
git rev-parse HEAD
git status --short

# Recent changes
echo -e "\n## Recent Changes"
git log --oneline -10

# Running processes
echo -e "\n## Related Processes"
ps aux | grep -E "(node|python|nginx)" | grep -v grep

# Error logs
echo -e "\n## Recent Errors"
if [ -f "logs/error.log" ]; then
    tail -20 logs/error.log
fi

# Network
echo -e "\n## Network"
netstat -an | grep LISTEN | grep -E "(3000|8000|5432)"
```

#### Error Pattern Analysis
```python
import re
from collections import Counter
from datetime import datetime, timedelta

def analyze_error_patterns(log_file, hours_back=24):
    """Analyze error patterns in logs."""
    
    patterns = {
        'null_reference': r'(null|undefined|NoneType|nil).*(reference|property|attribute)',
        'timeout': r'(timeout|timed out|deadline exceeded)',
        'connection': r'(connection|socket|ECONNREFUSED)',
        'auth': r'(unauthorized|401|403|authentication|permission)',
        'database': r'(database|sql|constraint|foreign key)',
        'memory': r'(memory|heap|OOM|out of memory)',
        'api': r'(API|endpoint|route|404|500)',
    }
    
    errors = Counter()
    timeline = []
    
    cutoff = datetime.now() - timedelta(hours=hours_back)
    
    with open(log_file) as f:
        for line in f:
            # Extract timestamp
            timestamp = extract_timestamp(line)
            if timestamp < cutoff:
                continue
                
            # Categorize error
            for category, pattern in patterns.items():
                if re.search(pattern, line, re.I):
                    errors[category] += 1
                    timeline.append((timestamp, category, line.strip()))
    
    # Analysis
    print("Error Distribution:")
    for category, count in errors.most_common():
        print(f"  {category}: {count}")
    
    # Time clustering
    print("\nError Clustering:")
    analyze_time_clusters(timeline)
    
    return errors, timeline
```

### Stage 2: Hypothesis Formation

#### Hypothesis Templates

**Template 1: Timing/Race Condition**
```markdown
### Hypothesis: Race Condition in [Component]

**Evidence:**
- Only occurs under load
- Intermittent failures
- Works with artificial delays

**Test Method:**
1. Add mutex/lock around suspicious code
2. Add detailed timing logs
3. Run stress test with concurrency

**Expected Result:**
- With lock: No failures
- Timing logs: Show overlap
```

**Template 2: State Corruption**
```markdown
### Hypothesis: State Corruption in [Store/Cache]

**Evidence:**
- Inconsistent data between requests
- Works after cache clear
- Stale data appearing

**Test Method:**
1. Log all state mutations
2. Verify state before/after operations
3. Test with cache disabled

**Expected Result:**
- State logs show unexpected mutations
- No errors with cache disabled
```

**Template 3: External Dependency**
```markdown
### Hypothesis: External Service [API/DB] Issue

**Evidence:**
- Errors started at specific time
- Works in dev but not prod
- Timeout or connection errors

**Test Method:**
1. Direct service health check
2. Compare dev vs prod configs
3. Test with service mock

**Expected Result:**
- Service returns errors/timeouts
- Config mismatch found
```

#### Hypothesis Prioritization
```python
def prioritize_hypotheses(hypotheses):
    """Score and rank hypotheses by likelihood."""
    
    for h in hypotheses:
        h.score = 0
        
        # Evidence strength (0-40 points)
        if h.evidence_count >= 3:
            h.score += 40
        elif h.evidence_count >= 2:
            h.score += 25
        else:
            h.score += 10
            
        # Testability (0-30 points)
        if h.test_time < 5:  # minutes
            h.score += 30
        elif h.test_time < 15:
            h.score += 20
        else:
            h.score += 10
            
        # Impact scope (0-30 points)
        if h.affects_all_users:
            h.score += 30
        elif h.affects_subset:
            h.score += 20
        else:
            h.score += 10
    
    return sorted(hypotheses, key=lambda h: h.score, reverse=True)
```

### Stage 3: Systematic Testing

#### Test Execution Framework
```python
class DebugTest:
    """Structured debug test execution."""
    
    def __init__(self, name):
        self.name = name
        self.setup_steps = []
        self.test_steps = []
        self.teardown_steps = []
        self.results = []
        
    def add_setup(self, step, func):
        self.setup_steps.append((step, func))
        
    def add_test(self, step, func, expected):
        self.test_steps.append((step, func, expected))
        
    def add_teardown(self, step, func):
        self.teardown_steps.append((step, func))
        
    def execute(self):
        print(f"\n=== Executing Debug Test: {self.name} ===")
        
        # Setup
        print("\n[Setup]")
        for step, func in self.setup_steps:
            print(f"  {step}...", end='')
            try:
                func()
                print(" ✓")
            except Exception as e:
                print(f" ✗ ({e})")
                return False
                
        # Tests
        print("\n[Tests]")
        for step, func, expected in self.test_steps:
            print(f"  {step}...", end='')
            try:
                result = func()
                if result == expected:
                    print(f" ✓ (got {result})")
                    self.results.append((step, True, result))
                else:
                    print(f" ✗ (expected {expected}, got {result})")
                    self.results.append((step, False, result))
            except Exception as e:
                print(f" ✗ (exception: {e})")
                self.results.append((step, False, str(e)))
                
        # Teardown
        print("\n[Teardown]")
        for step, func in self.teardown_steps:
            print(f"  {step}...", end='')
            try:
                func()
                print(" ✓")
            except:
                print(" ✗")
                
        # Summary
        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)
        print(f"\n[Summary] {passed}/{total} tests passed")
        
        return passed == total
```

#### Binary Search Debugging
```python
def binary_search_debug(commits, test_func):
    """Find the commit that introduced a bug."""
    
    print("Starting binary search debug...")
    
    left, right = 0, len(commits) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        print(f"\nTesting commit {mid}: {commits[mid]}")
        checkout_commit(commits[mid])
        
        if test_func():
            print("  → Bug NOT present")
            left = mid + 1
        else:
            print("  → Bug IS present")
            right = mid
            
    print(f"\nBug introduced in commit: {commits[left]}")
    return commits[left]
```

### Stage 4: Root Cause Analysis

#### 5 Whys Technique
```python
class FiveWhysAnalysis:
    """Systematic root cause analysis."""
    
    def __init__(self, initial_problem):
        self.problem = initial_problem
        self.whys = []
        
    def ask_why(self, answer, evidence):
        """Add a why level with evidence."""
        self.whys.append({
            'level': len(self.whys) + 1,
            'question': f"Why {self.whys[-1]['answer'] if self.whys else self.problem}?",
            'answer': answer,
            'evidence': evidence
        })
        
    def generate_report(self):
        """Generate root cause analysis report."""
        print(f"## 5 Whys Analysis: {self.problem}\n")
        
        for why in self.whys:
            print(f"**Level {why['level']}:** {why['question']}")
            print(f"→ {why['answer']}")
            print(f"Evidence: {why['evidence']}\n")
            
        print(f"**Root Cause:** {self.whys[-1]['answer']}")
```

#### Fishbone Diagram Generator
```python
def generate_fishbone_diagram(problem, categories):
    """Create fishbone (Ishikawa) diagram for root cause analysis."""
    
    diagram = f"""
    ## Fishbone Diagram: {problem}
    
    ```
                     Environment          People
                          |                 |
                          |                 |
    Methods ______________|_________________|______________ Problem: {problem}
                          |                 |
                          |                 |
                     Materials          Technology
    ```
    
    ### Contributing Factors:
    """
    
    for category, factors in categories.items():
        diagram += f"\n**{category}:**\n"
        for factor in factors:
            diagram += f"- {factor}\n"
            
    return diagram

# Example usage
categories = {
    'Environment': [
        'Production vs Development differences',
        'Load/traffic patterns',
        'Network conditions'
    ],
    'People': [
        'User behavior patterns',
        'Admin actions',
        'Support team changes'
    ],
    'Methods': [
        'Deployment process',
        'Testing procedures',
        'Monitoring gaps'
    ],
    'Materials': [
        'Data quality issues',
        'Resource constraints',
        'Input validation'
    ],
    'Technology': [
        'API changes',
        'Library updates',
        'Infrastructure issues'
    ]
}
```

## Debug Tools & Commands

### Memory Profiling
```python
import tracemalloc
import psutil
import gc

def profile_memory_usage(func):
    """Profile memory usage of a function."""
    
    # Start tracing
    tracemalloc.start()
    gc.collect()
    
    # Get baseline
    process = psutil.Process()
    baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Execute function
    result = func()
    
    # Get peak
    current, peak = tracemalloc.get_traced_memory()
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Get top allocations
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print(f"\nMemory Profile for {func.__name__}:")
    print(f"  Baseline: {baseline_memory:.1f} MB")
    print(f"  Peak: {peak_memory:.1f} MB")
    print(f"  Allocated: {peak / 1024 / 1024:.1f} MB")
    print("\n  Top allocations:")
    
    for stat in top_stats[:5]:
        print(f"    {stat}")
        
    tracemalloc.stop()
    return result
```

### Network Debugging
```bash
#!/bin/bash
# network-debug.sh

echo "=== Network Debug ==="

# DNS resolution
echo -e "\n## DNS Resolution"
nslookup api.example.com

# Connection test
echo -e "\n## Connection Test"
nc -zv api.example.com 443

# SSL certificate
echo -e "\n## SSL Certificate"
openssl s_client -connect api.example.com:443 -servername api.example.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Route tracing
echo -e "\n## Route Trace"
traceroute -m 10 api.example.com

# Current connections
echo -e "\n## Active Connections"
netstat -an | grep -E "ESTABLISHED|TIME_WAIT" | grep 443 | head -10

# Bandwidth test
echo -e "\n## Response Time"
curl -w "@curl-format.txt" -o /dev/null -s https://api.example.com/health
```

### Database Query Analysis
```sql
-- Query performance analysis
EXPLAIN ANALYZE
SELECT u.*, p.*
FROM users u
LEFT JOIN profiles p ON p.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '7 days'
ORDER BY u.created_at DESC
LIMIT 100;

-- Lock detection
SELECT
    pid,
    usename,
    pg_blocking_pids(pid) as blocked_by,
    query as blocked_query
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;

-- Slow query log
SELECT
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    min_exec_time,
    max_exec_time,
    stddev_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- queries averaging > 100ms
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Common Bug Patterns

### 1. Race Conditions
```javascript
// Problem pattern
let data = null;
async function loadData() {
    const response = await fetch('/api/data');
    data = await response.json();
}
function useData() {
    return data.map(item => item.name); // Race: data might be null
}

// Debug approach
function useData() {
    console.log('[DEBUG] data state:', data);
    console.log('[DEBUG] data type:', typeof data);
    console.log('[DEBUG] is array:', Array.isArray(data));
    
    if (!data || !Array.isArray(data)) {
        console.error('[DEBUG] Data not ready or invalid');
        return [];
    }
    return data.map(item => item.name);
}
```

### 2. Memory Leaks
```python
# Problem pattern
class EventManager:
    def __init__(self):
        self.handlers = []
    
    def subscribe(self, handler):
        self.handlers.append(handler)  # Leak: never removed

# Debug approach
import weakref

class EventManager:
    def __init__(self):
        self.handlers = []
        self._debug_subscriptions = 0
        
    def subscribe(self, handler):
        self._debug_subscriptions += 1
        print(f"[DEBUG] Subscription #{self._debug_subscriptions}")
        print(f"[DEBUG] Total handlers: {len(self.handlers)}")
        
        # Use weak reference to prevent leak
        self.handlers.append(weakref.ref(handler))
        
    def _clean_handlers(self):
        """Remove dead references."""
        self.handlers = [h for h in self.handlers if h() is not None]
```

### 3. Async/Promise Issues
```typescript
// Problem pattern
async function processItems(items: Item[]) {
    items.forEach(async (item) => {
        await processItem(item);  // Bug: forEach doesn't wait
    });
}

// Debug approach
async function processItems(items: Item[]) {
    console.log(`[DEBUG] Processing ${items.length} items`);
    
    // Method 1: Sequential
    for (const item of items) {
        console.log(`[DEBUG] Processing item ${item.id}`);
        await processItem(item);
    }
    
    // Method 2: Parallel
    await Promise.all(
        items.map((item, index) => {
            console.log(`[DEBUG] Starting item ${index}`);
            return processItem(item);
        })
    );
}
```

## Debug Documentation Template

```markdown
# Debug Report: [Issue Title]

## Summary
- **Issue ID:** #123
- **Severity:** High/Medium/Low
- **First Observed:** [Date]
- **Resolution Time:** [X hours]

## Problem Description
[Clear description of the issue]

## Impact
- Users affected: [Number/%]
- Features impacted: [List]
- Data loss: Yes/No

## Root Cause
[Technical explanation of why it happened]

## Evidence Trail
1. [Timestamp] - Initial error observed
2. [Timestamp] - Hypothesis 1 tested (failed)
3. [Timestamp] - Hypothesis 2 tested (confirmed)
4. [Timestamp] - Root cause identified

## Solution
[What was changed to fix it]

## Prevention
[How to prevent this in the future]

## Lessons Learned
[What we learned from this issue]

## Related Issues
- [Links to similar or related issues]
```