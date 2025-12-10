# Multi-LLM Swarm Consensus

## Concept

Query multiple LLMs in parallel, aggregate votes with model-specific weights.
Higher confidence than single-model decisions.

## Model Selection (NO OPENAI)

From ThetaRoom/SwaggyStacks implementations:

```python
SWARM_MODELS = {
    'claude-opus-4-5': {
        'weight': 1.3,
        'role': 'Primary reasoning, highest quality'
    },
    'claude-sonnet-4-5': {
        'weight': 1.2,
        'role': 'Fast, reliable analysis'
    },
    'deepseek-r1': {
        'weight': 1.1,
        'role': 'Deep reasoning, chain-of-thought'
    },
    'deepseek-v3': {
        'weight': 1.0,
        'role': 'Fast inference, good quality'
    },
    'gemini-2.0-flash': {
        'weight': 0.9,
        'role': 'Fast validation'
    },
    'qwen-72b': {
        'weight': 0.85,
        'role': 'Quantitative analysis'
    },
    'mistral-large': {
        'weight': 0.8,
        'role': 'Research perspective'
    }
}
```

## Voting System

```python
class SwarmConsensus:
    def __init__(self, models: list[str]):
        self.models = models
        self.adapters = self._init_adapters()

    async def get_consensus(self, prompt: str, context: dict) -> dict:
        # Query all models in parallel
        votes = await asyncio.gather(*[
            self._query_model(model, prompt, context)
            for model in self.models
        ], return_exceptions=True)

        # Filter failed responses
        valid_votes = [v for v in votes if not isinstance(v, Exception)]

        # Weighted aggregation
        return self._aggregate_votes(valid_votes)

    def _aggregate_votes(self, votes: list[dict]) -> dict:
        weighted_scores = {'BUY': 0, 'SELL': 0, 'HOLD': 0}

        for vote in votes:
            model = vote['model']
            signal = vote['signal']
            confidence = vote['confidence']
            weight = SWARM_MODELS[model]['weight']

            weighted_scores[signal] += weight * confidence

        # Determine consensus
        total_weight = sum(weighted_scores.values())
        consensus_signal = max(weighted_scores, key=weighted_scores.get)
        consensus_confidence = weighted_scores[consensus_signal] / total_weight

        return {
            'signal': consensus_signal,
            'confidence': consensus_confidence,
            'votes': votes,
            'agreement_ratio': self._calc_agreement(votes, consensus_signal)
        }
```

## Consensus Thresholds

```python
CONSENSUS_RULES = {
    'strong_consensus': {
        'min_agreement': 0.75,  # 75% of models agree
        'min_confidence': 0.70,
        'action': 'Execute with full size'
    },
    'moderate_consensus': {
        'min_agreement': 0.60,
        'min_confidence': 0.55,
        'action': 'Execute with reduced size'
    },
    'weak_consensus': {
        'min_agreement': 0.50,
        'min_confidence': 0.40,
        'action': 'Wait for more data'
    },
    'no_consensus': {
        'min_agreement': 0.0,
        'action': 'HOLD - conflicting signals'
    }
}
```

## Tie-Breaking Logic

From SwaggyStacks' trading_workflow.py:

```python
def break_tie(weighted_scores: dict) -> str:
    """Deterministic tie-breaking: HOLD > BUY > SELL"""
    max_score = max(weighted_scores.values())
    tied = [k for k, v in weighted_scores.items() if v == max_score]

    if len(tied) == 1:
        return tied[0]

    # Priority: HOLD > BUY > SELL (conservative)
    priority = ['HOLD', 'BUY', 'SELL']
    for p in priority:
        if p in tied:
            return p

    return 'HOLD'  # Fallback
```

## Model Adapters

```python
class AnthropicAdapter:
    async def query(self, prompt: str, context: dict) -> dict:
        response = await anthropic.messages.create(
            model="claude-sonnet-4-5-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return self._parse_trading_signal(response)

class OpenRouterAdapter:
    """For DeepSeek, Qwen, Mistral via OpenRouter"""
    async def query(self, model: str, prompt: str) -> dict:
        response = await httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return self._parse_response(response.json())
```

## Prompt Template

```python
SWARM_PROMPT = """
Analyze the following trading setup and provide a signal.

Symbol: {symbol}
Timeframe: {timeframe}
Current Price: {price}

Technical Analysis:
{methodology_signals}

Market Context:
{market_context}

Respond with JSON:
{{
    "signal": "BUY" | "SELL" | "HOLD",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation",
    "key_levels": {{
        "entry": float,
        "stop": float,
        "target": float
    }}
}}
"""
```

## Cost Optimization

```python
MODEL_COSTS = {
    'claude-opus-4-5': 15.00,     # $/1M tokens
    'claude-sonnet-4-5': 3.00,
    'deepseek-r1': 0.55,
    'deepseek-v3': 0.27,
    'gemini-2.0-flash': 0.075,
    'qwen-72b': 0.40,
}

def select_swarm_tier(importance: str) -> list[str]:
    """Select models based on decision importance"""
    if importance == 'critical':
        return ['claude-opus-4-5', 'claude-sonnet-4-5', 'deepseek-r1']
    elif importance == 'standard':
        return ['claude-sonnet-4-5', 'deepseek-v3', 'gemini-2.0-flash']
    else:  # 'quick'
        return ['deepseek-v3', 'gemini-2.0-flash', 'qwen-72b']
```

## Error Handling

```python
async def query_with_fallback(self, models: list[str], prompt: str) -> list:
    """Graceful degradation if models fail"""
    results = []
    failed = []

    for model in models:
        try:
            result = await asyncio.wait_for(
                self._query_model(model, prompt),
                timeout=30.0
            )
            results.append(result)
        except Exception as e:
            failed.append({'model': model, 'error': str(e)})

    # Need at least 3 votes for consensus
    if len(results) < 3:
        raise InsufficientVotesError(f"Only {len(results)} models responded")

    return results
```

## Agent Message Format

> "Swarm Consensus: BUY (78% confidence). 5/6 models agree. Claude Opus: BUY 0.85, DeepSeek R1: BUY 0.80, Gemini: BUY 0.75, Qwen: HOLD 0.60, Mistral: BUY 0.70. Strong consensus - execute with full size."

## Integration Points

- **Entry Signals**: Require strong consensus (75%+) for new positions
- **Exit Signals**: Moderate consensus (60%+) acceptable
- **Risk Decisions**: Critical tier models only
- **Quick Scans**: Cheap tier for screening
