# Cost Tracking & Optimization

Comprehensive cost tracking system with model routing, budget management, and optimization strategies.

## Cost Model Reference

### LLM Pricing (per 1K tokens)
```python
LLM_COSTS = {
    # Anthropic Claude
    'claude-3-opus': {'input': 0.015, 'output': 0.075},
    'claude-3.5-sonnet': {'input': 0.003, 'output': 0.015},
    'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
    
    # DeepSeek (95% cheaper than Claude)
    'deepseek-chat': {'input': 0.00014, 'output': 0.00028},
    'deepseek-coder': {'input': 0.00014, 'output': 0.00028},
    'deepseek-v3': {'input': 0.00014, 'output': 0.00028},
    
    # Groq (ultra-fast inference)
    'llama-3.1-70b': {'input': 0.00059, 'output': 0.00079},
    'llama-3.1-8b': {'input': 0.00005, 'output': 0.00008},
    'mixtral-8x7b': {'input': 0.00024, 'output': 0.00024},
    
    # OpenAI
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
    
    # Local (free)
    'ollama-llama3': {'input': 0.0, 'output': 0.0},
    'ollama-codellama': {'input': 0.0, 'output': 0.0},
    'ollama-mistral': {'input': 0.0, 'output': 0.0},
}

# Embeddings (per 1K tokens)
EMBEDDING_COSTS = {
    'voyage-3': 0.00002,
    'voyage-3-lite': 0.00002,
    'jina-embeddings-v3': 0.00002,
    'nomic-embed-text': 0.0,  # Local
    'text-embedding-3-small': 0.00002,
}

# Infrastructure
INFRA_COSTS = {
    'runpod': {
        'a100-80gb': 2.29,  # per hour
        'a100-40gb': 1.89,
        'a6000': 0.79,
        'rtx-4090': 0.44,
        'rtx-3090': 0.24,
    },
    'supabase': {
        'database': 0.0,     # Free tier: 500MB
        'storage': 0.02,     # per GB after 1GB free
        'bandwidth': 0.09,   # per GB after 2GB free
        'functions': 0.0,    # Free tier: 500K invocations
    },
    'vercel': {
        'bandwidth': 0.15,   # per GB after 100GB
        'functions': 0.0,    # Free tier: 100K GB-hours
        'storage': 0.0,      # Included
    },
}
```

## Intelligent Model Routing

### Task-Based Routing Logic
```python
class ModelRouter:
    """Intelligently route requests to optimal models based on task."""
    
    def __init__(self, budget_remaining=100, urgency='normal'):
        self.budget = budget_remaining
        self.urgency = urgency
        self.usage_history = []
        
    def select_model(self, task_type, complexity='medium', quality_required='high'):
        """Select optimal model for task."""
        
        # Emergency budget mode
        if self.budget < 5:
            return self.emergency_mode_selection(task_type)
            
        # Task-specific routing
        routes = {
            'complex_reasoning': self._route_reasoning,
            'code_generation': self._route_code_gen,
            'bulk_processing': self._route_bulk,
            'chat_conversation': self._route_chat,
            'summarization': self._route_summary,
            'embeddings': self._route_embeddings,
            'data_extraction': self._route_extraction,
        }
        
        router = routes.get(task_type, self._route_default)
        return router(complexity, quality_required)
        
    def _route_reasoning(self, complexity, quality):
        """Route complex reasoning tasks."""
        if quality == 'critical' or complexity == 'high':
            return 'claude-3.5-sonnet'  # Best reasoning
        elif self.budget > 20:
            return 'claude-3-haiku'     # Good balance
        else:
            return 'deepseek-v3'        # 95% cheaper
            
    def _route_code_gen(self, complexity, quality):
        """Route code generation tasks."""
        if complexity == 'high' or quality == 'critical':
            return 'claude-3.5-sonnet'  # Most accurate
        elif complexity == 'medium':
            return 'deepseek-coder'     # Specialized, cheap
        else:
            return 'ollama-codellama'   # Free for simple
            
    def _route_bulk(self, complexity, quality):
        """Route bulk processing tasks."""
        # Always use cheapest for bulk
        if self.urgency == 'high':
            return 'groq-llama-3.1-8b' # Ultra fast
        else:
            return 'deepseek-v3'        # Cheapest cloud
            
    def emergency_mode_selection(self, task_type):
        """Emergency mode when budget is critical."""
        print("⚠️ BUDGET CRITICAL: Using free/cheapest models only")
        
        emergency_models = {
            'complex_reasoning': 'ollama-llama3',
            'code_generation': 'ollama-codellama',
            'bulk_processing': 'ollama-mistral',
            'chat_conversation': 'ollama-llama3',
            'summarization': 'ollama-mistral',
            'embeddings': 'nomic-embed-text',
        }
        
        return emergency_models.get(task_type, 'ollama-mistral')
```

### Quality vs Cost Matrix
```python
QUALITY_COST_MATRIX = {
    # (quality_required, budget_sensitivity) -> model
    ('critical', 'low'): 'claude-3-opus',
    ('critical', 'medium'): 'claude-3.5-sonnet',
    ('critical', 'high'): 'claude-3-haiku',
    
    ('high', 'low'): 'claude-3.5-sonnet',
    ('high', 'medium'): 'claude-3-haiku',
    ('high', 'high'): 'deepseek-v3',
    
    ('medium', 'low'): 'claude-3-haiku',
    ('medium', 'medium'): 'deepseek-v3',
    ('medium', 'high'): 'groq-mixtral-8x7b',
    
    ('low', 'low'): 'deepseek-v3',
    ('low', 'medium'): 'groq-llama-3.1-8b',
    ('low', 'high'): 'ollama-llama3',
}
```

## Cost Tracking Implementation

### Real-time Cost Monitor
```python
class CostMonitor:
    """Real-time cost tracking with alerts."""
    
    def __init__(self, daily_budget=5.0, monthly_budget=100.0):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.costs_today = 0
        self.costs_mtd = self.load_mtd_costs()
        self.last_alert = None
        
    def track_llm_call(self, model, input_tokens, output_tokens):
        """Track individual LLM call cost."""
        
        # Calculate cost
        model_costs = LLM_COSTS.get(model, {'input': 0.001, 'output': 0.001})
        cost = (
            (input_tokens / 1000) * model_costs['input'] +
            (output_tokens / 1000) * model_costs['output']
        )
        
        # Update totals
        self.costs_today += cost
        self.costs_mtd += cost
        
        # Log call
        self.log_api_call({
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': cost,
            'total_today': self.costs_today,
            'total_mtd': self.costs_mtd,
        })
        
        # Check alerts
        self.check_budget_alerts()
        
        return cost
        
    def check_budget_alerts(self):
        """Check and trigger budget alerts."""
        
        alerts = []
        
        # Daily budget alerts
        daily_percent = (self.costs_today / self.daily_budget) * 100
        if daily_percent > 80 and self.last_alert != 'daily_80':
            alerts.append({
                'level': 'warning',
                'message': f'Daily budget 80% used (${self.costs_today:.2f}/${self.daily_budget})',
                'action': 'Consider switching to cheaper models'
            })
            self.last_alert = 'daily_80'
            
        elif daily_percent > 100:
            alerts.append({
                'level': 'critical',
                'message': f'Daily budget EXCEEDED (${self.costs_today:.2f}/${self.daily_budget})',
                'action': 'Switch to emergency mode - free models only'
            })
            
        # Monthly budget alerts
        monthly_percent = (self.costs_mtd / self.monthly_budget) * 100
        days_in_month = 30
        current_day = datetime.now().day
        expected_percent = (current_day / days_in_month) * 100
        
        if monthly_percent > expected_percent * 1.5:
            alerts.append({
                'level': 'warning',
                'message': f'Burning budget too fast ({monthly_percent:.1f}% used on day {current_day})',
                'action': 'Review usage patterns and optimize'
            })
            
        # Trigger alerts
        for alert in alerts:
            self.trigger_alert(alert)
            
    def trigger_alert(self, alert):
        """Trigger budget alert."""
        if alert['level'] == 'critical':
            print(f"🚨 {alert['message']}")
            print(f"   ACTION: {alert['action']}")
        else:
            print(f"⚠️  {alert['message']}")
            print(f"   Suggestion: {alert['action']}")
```

### Cost Analytics Dashboard
```python
def generate_cost_dashboard():
    """Generate cost analytics dashboard."""
    
    # Load cost data
    costs = load_all_cost_data()
    
    dashboard = f"""# Cost Analytics Dashboard
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary
- **Today**: ${costs['today']:.2f} ({costs['today_percent']:.1f}% of daily budget)
- **This Week**: ${costs['week']:.2f}
- **MTD**: ${costs['mtd']:.2f} ({costs['mtd_percent']:.1f}% of monthly budget)
- **Projected Month**: ${costs['projected']:.2f}

## Cost by Model
{generate_model_breakdown(costs['by_model'])}

## Cost by Task Type
{generate_task_breakdown(costs['by_task'])}

## Top Expensive Operations
{generate_expensive_operations(costs['operations'])}

## Optimization Opportunities
{generate_optimization_suggestions(costs)}

## Trends
{generate_cost_trends(costs['daily_history'])}
"""
    
    return dashboard

def generate_model_breakdown(model_costs):
    """Generate model cost breakdown."""
    
    total = sum(model_costs.values())
    
    table = "| Model | Cost | % of Total | Calls | Avg/Call |\n"
    table += "|-------|------|-----------|--------|----------|\n"
    
    for model, data in sorted(model_costs.items(), key=lambda x: x[1]['cost'], reverse=True):
        percent = (data['cost'] / total) * 100
        avg_cost = data['cost'] / max(data['calls'], 1)
        
        table += f"| {model} | ${data['cost']:.2f} | {percent:.1f}% | {data['calls']} | ${avg_cost:.4f} |\n"
        
    return table

def generate_optimization_suggestions(costs):
    """Generate specific optimization suggestions."""
    
    suggestions = []
    
    # Analyze model usage
    expensive_model_percent = costs['by_model'].get('claude-3.5-sonnet', {}).get('percent', 0)
    if expensive_model_percent > 50:
        savings = expensive_model_percent * 0.95 * costs['mtd'] / 100
        suggestions.append({
            'priority': 'HIGH',
            'suggestion': 'Reduce Claude Sonnet usage',
            'details': f'Currently {expensive_model_percent:.1f}% of costs',
            'action': 'Use DeepSeek V3 for bulk tasks',
            'savings': f'Up to ${savings:.2f}/month'
        })
        
    # Analyze task patterns
    bulk_tasks = costs['by_task'].get('bulk_processing', {})
    if bulk_tasks.get('avg_cost', 0) > 0.01:
        suggestions.append({
            'priority': 'MEDIUM',
            'suggestion': 'Optimize bulk processing',
            'details': 'High cost per bulk operation',
            'action': 'Batch operations and use cheaper models',
            'savings': 'Est. 70% reduction'
        })
        
    # Time-based analysis
    peak_hour_costs = analyze_peak_hours(costs)
    if peak_hour_costs['concentration'] > 0.5:
        suggestions.append({
            'priority': 'LOW',
            'suggestion': 'Spread processing load',
            'details': f"{peak_hour_costs['concentration']*100:.0f}% of costs in {peak_hour_costs['hours']} hours",
            'action': 'Use scheduled/batch processing',
            'savings': 'Better rate negotiation possible'
        })
        
    return format_suggestions(suggestions)
```

## Budget Management

### Budget Configuration
```json
{
  "budgets": {
    "daily": {
      "soft_limit": 5.00,
      "hard_limit": 7.50,
      "alert_threshold": 0.8
    },
    "weekly": {
      "soft_limit": 25.00,
      "hard_limit": 35.00,
      "alert_threshold": 0.8
    },
    "monthly": {
      "soft_limit": 100.00,
      "hard_limit": 150.00,
      "alert_threshold": 0.8
    }
  },
  "cost_controls": {
    "auto_switch_models": true,
    "block_on_limit": false,
    "emergency_mode_threshold": 0.95
  },
  "notifications": {
    "email": "alerts@example.com",
    "slack_webhook": "https://hooks.slack.com/...",
    "alert_frequency": "once_per_threshold"
  }
}
```

### Budget Enforcement
```python
class BudgetEnforcer:
    """Enforce budget limits and controls."""
    
    def __init__(self, config_path='costs/budget-config.json'):
        self.config = self.load_config(config_path)
        self.current_costs = self.load_current_costs()
        
    def check_request_allowed(self, estimated_cost, priority='normal'):
        """Check if request should be allowed based on budget."""
        
        # Always allow critical requests
        if priority == 'critical':
            return True, None
            
        # Check daily limit
        daily_total = self.current_costs['today'] + estimated_cost
        if daily_total > self.config['budgets']['daily']['hard_limit']:
            return False, "Daily hard limit exceeded"
            
        # Check monthly limit
        monthly_total = self.current_costs['mtd'] + estimated_cost
        if monthly_total > self.config['budgets']['monthly']['hard_limit']:
            return False, "Monthly hard limit exceeded"
            
        # Warning but allow
        if daily_total > self.config['budgets']['daily']['soft_limit']:
            return True, "Warning: Exceeding daily soft limit"
            
        return True, None
        
    def get_model_override(self, requested_model):
        """Get model override based on budget status."""
        
        if not self.config['cost_controls']['auto_switch_models']:
            return requested_model
            
        # Calculate budget usage
        daily_usage = self.current_costs['today'] / self.config['budgets']['daily']['soft_limit']
        monthly_usage = self.current_costs['mtd'] / self.config['budgets']['monthly']['soft_limit']
        
        # Emergency mode
        if max(daily_usage, monthly_usage) > self.config['cost_controls']['emergency_mode_threshold']:
            return self.get_emergency_model(requested_model)
            
        # Progressive degradation
        if max(daily_usage, monthly_usage) > 0.8:
            return self.get_cheaper_alternative(requested_model)
            
        return requested_model
```

## Cost Optimization Strategies

### 1. Caching Strategy
```python
class CostOptimizedCache:
    """Cache expensive operations to reduce costs."""
    
    def __init__(self, cache_dir='~/.claude/cost-cache'):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_stats = {'hits': 0, 'misses': 0, 'savings': 0}
        
    def get_or_compute(self, key, compute_func, model_cost, ttl=86400):
        """Get from cache or compute with cost tracking."""
        
        cache_file = self.cache_dir / f"{hashlib.md5(key.encode()).hexdigest()}.json"
        
        # Check cache
        if cache_file.exists():
            cache_data = json.loads(cache_file.read_text())
            if time.time() - cache_data['timestamp'] < ttl:
                self.cache_stats['hits'] += 1
                self.cache_stats['savings'] += model_cost
                return cache_data['result']
                
        # Compute and cache
        self.cache_stats['misses'] += 1
        result = compute_func()
        
        cache_data = {
            'key': key,
            'result': result,
            'timestamp': time.time(),
            'model_cost': model_cost
        }
        
        cache_file.write_text(json.dumps(cache_data))
        
        return result
        
    def report_savings(self):
        """Report cache effectiveness."""
        hit_rate = self.cache_stats['hits'] / max(
            self.cache_stats['hits'] + self.cache_stats['misses'], 1
        )
        
        return {
            'hit_rate': f"{hit_rate*100:.1f}%",
            'total_saves': f"${self.cache_stats['savings']:.2f}",
            'api_calls_saved': self.cache_stats['hits']
        }
```

### 2. Batch Processing
```python
def batch_optimize_requests(requests, max_batch_size=20):
    """Optimize multiple requests through batching."""
    
    # Group by model and similar prompts
    grouped = defaultdict(list)
    
    for req in requests:
        key = (req['model'], req['task_type'])
        grouped[key].append(req)
        
    optimized = []
    
    for (model, task_type), group in grouped.items():
        # Batch similar requests
        batches = [group[i:i+max_batch_size] for i in range(0, len(group), max_batch_size)]
        
        for batch in batches:
            if len(batch) > 1:
                # Combine into single request
                combined = combine_requests(batch)
                combined['cost_savings'] = calculate_batch_savings(batch, combined)
                optimized.append(combined)
            else:
                optimized.extend(batch)
                
    return optimized
```

### 3. Progressive Model Degradation
```python
class ProgressiveModelDegradation:
    """Gradually switch to cheaper models as budget depletes."""
    
    DEGRADATION_PATH = {
        'claude-3-opus': ['claude-3.5-sonnet', 'claude-3-haiku', 'deepseek-v3', 'ollama-llama3'],
        'claude-3.5-sonnet': ['claude-3-haiku', 'deepseek-v3', 'groq-mixtral', 'ollama-llama3'],
        'claude-3-haiku': ['deepseek-v3', 'groq-llama-70b', 'groq-llama-8b', 'ollama-llama3'],
        'gpt-4-turbo': ['gpt-3.5-turbo', 'deepseek-v3', 'groq-mixtral', 'ollama-mistral'],
    }
    
    def get_degraded_model(self, original_model, budget_percent_remaining):
        """Get appropriate model based on remaining budget."""
        
        if original_model not in self.DEGRADATION_PATH:
            return original_model
            
        path = self.DEGRADATION_PATH[original_model]
        
        if budget_percent_remaining > 50:
            return original_model
        elif budget_percent_remaining > 30:
            return path[0] if len(path) > 0 else original_model
        elif budget_percent_remaining > 15:
            return path[1] if len(path) > 1 else path[0]
        elif budget_percent_remaining > 5:
            return path[2] if len(path) > 2 else path[1]
        else:
            return path[3] if len(path) > 3 else path[2]
```

### 4. Smart Token Optimization
```python
class TokenOptimizer:
    """Optimize token usage to reduce costs."""
    
    def optimize_prompt(self, prompt, target_reduction=0.2):
        """Reduce prompt tokens while preserving meaning."""
        
        original_tokens = self.count_tokens(prompt)
        
        # Optimization strategies
        optimized = prompt
        
        # 1. Remove redundant whitespace
        optimized = ' '.join(optimized.split())
        
        # 2. Compress system messages
        optimized = self.compress_system_message(optimized)
        
        # 3. Use abbreviations for common terms
        optimized = self.apply_abbreviations(optimized)
        
        # 4. Remove unnecessary examples if over token limit
        if self.count_tokens(optimized) > original_tokens * (1 - target_reduction):
            optimized = self.remove_examples(optimized)
            
        # 5. Summarize context if still too long
        if self.count_tokens(optimized) > original_tokens * (1 - target_reduction):
            optimized = self.summarize_context(optimized)
            
        new_tokens = self.count_tokens(optimized)
        reduction = (original_tokens - new_tokens) / original_tokens
        
        return {
            'optimized_prompt': optimized,
            'original_tokens': original_tokens,
            'new_tokens': new_tokens,
            'reduction': f"{reduction*100:.1f}%",
            'cost_savings': self.calculate_savings(original_tokens - new_tokens)
        }
```

## Reporting & Analytics

### Daily Cost Report
```python
def generate_daily_report():
    """Generate comprehensive daily cost report."""
    
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# Daily Cost Report - {report_date}

## Executive Summary
{generate_executive_summary()}

## Cost Breakdown by Hour
{generate_hourly_breakdown()}

## Model Usage Analysis
{generate_model_analysis()}

## Task Type Distribution
{generate_task_distribution()}

## Cost Anomalies
{generate_anomaly_detection()}

## Optimization Achievements
{generate_optimization_report()}

## Tomorrow's Budget Plan
{generate_budget_plan()}

## Recommendations
{generate_daily_recommendations()}
"""
    
    # Save report
    report_path = f"costs/reports/daily-{report_date}.md"
    Path(report_path).parent.mkdir(exist_ok=True)
    Path(report_path).write_text(report)
    
    # Send notifications if needed
    if should_send_notification():
        send_cost_report(report)
        
    return report
```

### ROI Analysis
```python
def calculate_feature_roi(feature_name):
    """Calculate ROI for specific features."""
    
    # Get feature costs
    feature_costs = get_feature_costs(feature_name)
    
    # Get feature metrics
    metrics = get_feature_metrics(feature_name)
    
    # Calculate ROI
    roi_analysis = {
        'feature': feature_name,
        'total_cost': feature_costs['total'],
        'development_cost': feature_costs['development'],
        'operational_cost': feature_costs['operational'],
        'users_impacted': metrics['users'],
        'revenue_impact': metrics.get('revenue_impact', 0),
        'cost_per_user': feature_costs['total'] / max(metrics['users'], 1),
        'roi_percentage': ((metrics.get('revenue_impact', 0) - feature_costs['total']) / feature_costs['total']) * 100
    }
    
    # Cost breakdown
    roi_analysis['cost_breakdown'] = {
        'llm_costs': feature_costs['llm'],
        'infrastructure': feature_costs['infrastructure'],
        'development_hours': feature_costs['dev_hours'],
        'testing_costs': feature_costs['testing']
    }
    
    # Recommendations
    if roi_analysis['cost_per_user'] > 0.10:
        roi_analysis['recommendation'] = "Consider optimization - high cost per user"
    elif roi_analysis['roi_percentage'] < 0:
        roi_analysis['recommendation'] = "Review feature value - negative ROI"
    else:
        roi_analysis['recommendation'] = "Healthy ROI - maintain current approach"
        
    return roi_analysis
```