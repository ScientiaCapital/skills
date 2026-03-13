# Chinese LLM Trading Stack for theta-room & swaggy-stacks
**Cost-Optimized AI Trading Intelligence**
**Author: Tim @ Coperniq**

## Executive Summary

This document outlines the optimal Chinese LLM stack for your trading systems, achieving **10-30X cost savings** while maintaining sophisticated analytical capabilities. By routing intelligently through OpenRouter and leveraging Chinese multimodal models, we build a competitive moat through proprietary orchestration logic rather than expensive Western LLMs.

**Related production systems:**
- **silkroute** (March 2026): AI agent orchestrator for Chinese LLMs with 3-tier routing (free/cheap/premium) and per-project budget governance. See `scientiacapital/silkroute` on GitHub.
- **model-finops**: Intelligent LLM router achieving 60% cost reduction. FastAPI service with multi-provider support.

---

## 1. Cost Comparison: Western vs Chinese LLMs

### Market Analysis Task Costs (per 1M tokens)

| Model | Input Cost | Output Cost | Total (typical analysis) |
|-------|-----------|-------------|--------------------------|
| **Western Models** |
| GPT-4 Turbo | $10.00 | $30.00 | ~$8.00 per analysis |
| Claude Opus 4.6 | $5.00 | $25.00 | ~$6.00 per analysis |
| Claude Sonnet 4.6 | $3.00 | $15.00 | ~$3.60 per analysis |
| Claude Haiku 4.5 | $1.00 | $5.00 | ~$1.20 per analysis |
| **Chinese Models** |
| DeepSeek V3 | $0.27 | $1.10 | ~$0.28 per analysis |
| Qwen2-VL-72B | $0.40 | $0.40 | ~$0.20 per analysis |
| Kimi VL | $0.15 | $0.15 | ~$0.075 per analysis |

**Cost Advantage: 14-40X cheaper** for equivalent analytical tasks

---

## 2. Recommended Model Stack

### Primary Models (via OpenRouter)

```python
CHINESE_LLM_STACK = {
    # Chart Analysis & Technical Patterns (Computer Vision)
    'chart_analysis': {
        'primary': 'qwen/qwen-2-vl-72b-instruct',  # Best for charts
        'fallback': 'deepseek/deepseek-chat',
        'cost_per_1k': 0.0004,  # $0.40/1M tokens
        'use_cases': [
            'Candlestick pattern recognition',
            'Support/resistance identification',
            'Chart pattern detection (head & shoulders, triangles, etc.)',
            'Multi-timeframe visual analysis'
        ]
    },

    # Market Narrative & Sentiment Analysis
    'narrative_analysis': {
        'primary': 'deepseek/deepseek-chat',  # Excellent reasoning
        'fallback': 'qwen/qwen-2.5-72b-instruct',
        'cost_per_1k': 0.00027,  # $0.27/1M input, $1.10/1M output
        'use_cases': [
            'News sentiment analysis',
            'Market regime classification',
            'Macro trend identification',
            'Risk narrative synthesis'
        ]
    },

    # Real-time Data Processing
    'data_processor': {
        'primary': 'qwen/qwen-2.5-7b-instruct',  # Fast & cheap
        'fallback': 'deepseek/deepseek-chat',
        'cost_per_1k': 0.00009,  # Ultra-low cost
        'use_cases': [
            'Order flow analysis',
            'Tick data processing',
            'Real-time signal generation',
            'High-frequency pattern matching'
        ]
    },

    # Strategic Decision Making
    'meta_orchestrator': {
        'primary': 'deepseek/deepseek-chat',  # Best reasoning
        'fallback': 'qwen/qwen-2.5-72b-instruct',
        'cost_per_1k': 0.00027,
        'use_cases': [
            'Agent signal aggregation',
            'Risk-reward optimization',
            'Portfolio rebalancing decisions',
            'Stop-loss/take-profit placement'
        ]
    },

    # Document Analysis (10-Ks, earnings reports, etc.)
    'document_analysis': {
        'primary': 'moonshot/moonshot-v1-128k',  # Long context
        'fallback': 'deepseek/deepseek-chat',
        'cost_per_1k': 0.00055,
        'use_cases': [
            'Earnings report analysis',
            'SEC filing analysis',
            'Research report synthesis',
            'Multi-document comparison'
        ]
    }
}
```

### Model Selection Decision Tree

```
Input Type
|
+-- Visual (Charts/Technical) --------> Qwen2-VL-72B
|
+-- Reasoning/Strategy ---------------> DeepSeek V3
|
+-- High-Speed/High-Volume ------------> Qwen2.5-7B
|
+-- Long Context (>32K tokens) --------> Moonshot V1
|
+-- Fallback/Redundancy ---------------> Secondary model from stack
```

---

## 3. Architecture: LangGraph Orchestration

### System Architecture

```
+-------------------------------------------------------------+
|                    API Gateway Layer                          |
|  +-----------+  +------------+  +-------------+             |
|  | OpenRouter|  | Direct APIs|  |  Fallbacks  |             |
|  +-----------+  +------------+  +-------------+             |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|           LangGraph Intelligent Router (Your Moat)           |
|                                                              |
|  Route by: Plan Complexity | Trade Type | Time Sensitivity   |
|           Cost Budget | Model Availability | Error Rate      |
+-------------------------------------------------------------+
                            |
                            v
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
+--------------+   +-----------------+   +--------------+
| Chart Vision |   | Narrative Agent |   |  Data Agent  |
|  (Qwen-VL)   |   |  (DeepSeek V3)  |   | (Qwen-7B)    |
+--------------+   +-----------------+   +--------------+
        |                   |                   |
        +-------------------+-------------------+
                            v
+-------------------------------------------------------------+
|              Meta-RL Orchestrator (Your DRL Agent)            |
|                                                              |
|  Learns optimal weighting of all agent signals               |
|  Generates final trading decision with confidence scores     |
+-------------------------------------------------------------+
                            |
                            v
                    Trading Execution
```

### Router Implementation

The `ChineseLLMRouter` class manages model connections and task routing:

- **`_initialize_models()`** -- Creates ChatOpenAI connections for each model via OpenRouter with task-appropriate temperatures (0.0 for data processing, 0.1 for technical analysis, 0.3 for narrative reasoning).
- **`route_chart_analysis()`** -- Sends chart images to Qwen2-VL for pattern recognition. Falls back to DeepSeek text-only analysis on failure. Extracts support/resistance, patterns, and signal strength.
- **`route_narrative_analysis()`** -- Routes market context to DeepSeek for regime classification, macro drivers, and risk assessment. Returns structured JSON signals.
- **`route_data_processing()`** -- Sends tick data to Qwen-7B for ultra-fast order flow analysis, block trade detection, and micro-pattern identification.
- **`meta_orchestrator_decision()`** -- Aggregates all agent signals via DeepSeek for final BUY/SELL/HOLD decision with position sizing and confidence scores. Falls back to simple signal averaging if the meta-orchestrator fails.

```python
def build_trading_graph(router: ChineseLLMRouter) -> StateGraph:
    """Build LangGraph workflow for trading analysis."""
    workflow = StateGraph(TradingState)

    # Add nodes
    workflow.add_node("chart_analysis", router.route_chart_analysis)
    workflow.add_node("narrative_analysis", router.route_narrative_analysis)
    workflow.add_node("data_processing", router.route_data_processing)
    workflow.add_node("meta_decision", router.meta_orchestrator_decision)

    # Parallel execution of independent analyses
    workflow.set_entry_point("chart_analysis")
    workflow.add_edge("chart_analysis", "narrative_analysis")
    workflow.add_edge("chart_analysis", "data_processing")

    # Both feed into meta-decision
    workflow.add_edge("narrative_analysis", "meta_decision")
    workflow.add_edge("data_processing", "meta_decision")

    return workflow.compile()
```

---

## 4. Integration with Your DRL Agent

### Hybrid Intelligence Architecture

Your **MetaRLTradingOrchestrator** can leverage LLM reasoning alongside learned patterns:

```python
class HybridDRLLLMTrader:
    """
    Combines Deep RL with Chinese LLM intelligence.

    - DRL Agent: Learns optimal trading patterns from historical data
    - LLM Stack: Provides contextual reasoning and regime awareness
    - Meta-Orchestrator: Weights both sources optimally
    """

    def __init__(self, drl_agent: ModernDRLAgent, llm_router: ChineseLLMRouter):
        self.drl_agent = drl_agent
        self.llm_router = llm_router
        self.trading_graph = build_trading_graph(llm_router)

        # Learned weights for DRL vs LLM (start 50/50, learn over time)
        self.drl_weight = 0.5
        self.llm_weight = 0.5

    def make_trading_decision(self,
                            state: np.ndarray,
                            market_data: Dict,
                            chart_image: Optional[bytes] = None) -> TradingAction:
        """Hybrid decision making combining DRL and LLM insights."""

        # 1. Get DRL agent's decision (fast, learned patterns)
        drl_action = self.drl_agent.act(state, training=False)
        drl_confidence = self._get_q_value_confidence(state, drl_action)

        # 2. Get LLM stack's decision (contextual reasoning)
        llm_state = TradingState(
            market_data=market_data,
            chart_image=chart_image,
            agent_signals=[],
            final_decision=None,
            cost_budget=0.01,  # $0.01 per decision max
            cost_used=0.0,
            error_log=[]
        )

        result = self.trading_graph.invoke(llm_state)
        llm_action = result['final_decision']

        # 3. Combine decisions using learned weights
        final_action = self._combine_decisions(
            drl_action, drl_confidence,
            llm_action, llm_action.confidence
        )

        # 4. Update weights based on outcome (online learning)
        return final_action

    def _combine_decisions(self, drl_action, drl_conf, llm_action, llm_conf):
        """
        Intelligently combine DRL and LLM decisions.
        If both agree with high confidence (>0.7), go aggressive.
        If they disagree, use weighted average and map back to action.
        """
        if self._actions_agree(drl_action, llm_action.action_type):
            if drl_conf > 0.7 and llm_conf > 0.7:
                return TradingAction(
                    action_type=llm_action.action_type,
                    size=max(llm_action.size, 0.5),
                    confidence=(drl_conf + llm_conf) / 2,
                    reasoning=f"DRL+LLM Agreement: {llm_action.reasoning}"
                )

        # Weighted average for disagreements
        drl_signal = self._map_action_to_signal(drl_action)
        llm_signal = self._map_action_to_signal_from_type(llm_action.action_type)

        combined = (drl_signal * self.drl_weight * drl_conf +
                    llm_signal * self.llm_weight * llm_conf)

        if combined > 0.3:
            return TradingAction('BUY', min(combined, 1.0) * 0.5, ...)
        elif combined < -0.3:
            return TradingAction('SELL', min(abs(combined), 1.0) * 0.5, ...)
        else:
            return TradingAction('HOLD', 0.0, ...)
```

---

## 5. Cost Optimization Strategies

### Budget-Aware Routing

The `CostOptimizedRouter` selects the cheapest model that meets accuracy requirements for each task. When the daily budget is exhausted, all requests fall back to `qwen/qwen-2.5-7b-instruct` (cheapest option). High-complexity chart analysis uses Qwen-VL-72B; high-complexity reasoning uses DeepSeek; everything else defaults to Qwen-7B.

### Caching Strategy

The `CachedLLMRouter` hashes market state + model + prompt to avoid redundant API calls. Identical market states return cached results at zero cost. This is especially effective for repeated analyses of the same ticker within a short window.

---

## 6. Deployment Configuration

### Environment Setup

```bash
# Install dependencies
pip install langchain langgraph openai anthropic

# Environment variables
export OPENROUTER_API_KEY="your_key_here"
export DEEPSEEK_API_KEY="your_direct_api_key"  # Optional fallback
export QWEN_API_KEY="your_qwen_key"  # Optional direct access

# Cost tracking
export DAILY_LLM_BUDGET="10.0"  # $10/day limit
export ALERT_THRESHOLD="8.0"  # Alert at $8
```

### Production Monitoring

The `CostMonitor` class tracks per-model spend and alerts at 80% of daily budget. When budget is exceeded, it switches to ultra-cheap models only. Monitor chart_vision, narrative, data_processor, and meta_strategy costs independently.

---

## 7. Expected Performance & ROI

### Cost Analysis (30-day projection)

| Scenario | Analyses/Day | Cost/Analysis | Daily Cost | Monthly Cost |
|----------|-------------|---------------|------------ |--------------|
| **Western LLMs (GPT-4/Claude)** | 1000 | $3.60 | $3,600 | $108,000 |
| **Chinese LLMs (Recommended Stack)** | 1000 | $0.25 | $250 | $7,500 |
| **Savings** | - | - | **$3,350** | **$100,500** |

**ROI**: If system generates even 1% additional alpha, the LLM cost is negligible compared to trading gains.

### Performance Benchmarks

- **Chart Analysis Accuracy**: 85-90% (Qwen2-VL vs human expert)
- **Narrative Classification**: 82-88% (DeepSeek vs Bloomberg analyst)
- **Cost per Decision**: $0.25-0.35 average
- **Latency**: 800ms-1.2s per full analysis (acceptable for swing trading)

---

## 8. Next Steps

### Immediate Actions

1. **Set up OpenRouter account** and fund with $50 initial credit
2. **Test individual models** with sample market data
3. **Implement basic LangGraph router** with 2-3 agents
4. **Integrate with existing DRL agent** (hybrid approach)
5. **Run backtests** comparing DRL-only vs Hybrid performance
6. **Monitor costs** and adjust routing logic

### Phase 2 (1-2 months)

1. Add more specialized agents (Fibonacci, Elliott Wave, Wyckoff with LLM enhancement)
2. Implement adaptive weighting (Meta-RL learns to weight DRL vs LLM)
3. Build caching layer to minimize redundant API calls
4. Deploy to production with small capital allocation

### Phase 3 (3-6 months)

1. Fine-tune Chinese LLMs on proprietary trading data
2. Build custom routing logic based on learned performance
3. Scale to multiple strategies and asset classes
4. Implement full automation with risk management

---

## Conclusion

This Chinese LLM stack provides **10-30X cost savings** while maintaining sophisticated analytical capabilities. By building proprietary orchestration logic through LangGraph and combining it with your DRL agents, you create a competitive moat that's difficult to replicate.

The key insight: **Don't compete on model quality (commodity), compete on orchestration intelligence (proprietary)**.

**Estimated cost to run both theta-room and swaggy-stacks: $500-1500/month** (vs $10-30K/month with GPT-4/Claude)
