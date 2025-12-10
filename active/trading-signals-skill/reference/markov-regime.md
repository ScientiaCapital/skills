# Markov Regime Detection

## State Definitions

| Regime | Criteria |
|--------|----------|
| `trending_up` | ADX > 25, +DI > -DI |
| `trending_down` | ADX > 25, -DI > +DI |
| `ranging` | ADX < 20 |
| `volatile` | ATR expansion > 2 std dev |

## Implementation

```python
from hmmlearn import hmm

class MarkovRegimeDetector:
    def __init__(self, n_regimes: int = 4):
        self.model = hmm.GaussianHMM(
            n_components=n_regimes,
            covariance_type="full",
            n_iter=100
        )
        self.regimes = ['trending_up', 'trending_down', 'ranging', 'volatile']

    def fit(self, returns: np.ndarray, volatility: np.ndarray):
        """Fit HMM on returns + volatility features"""
        features = np.column_stack([returns, volatility])
        self.model.fit(features)

    def predict(self, returns: np.ndarray, volatility: np.ndarray) -> dict:
        features = np.column_stack([returns, volatility])
        current_state = self.model.predict(features)[-1]

        # Get transition probabilities
        trans_probs = self.model.transmat_[current_state]

        return {
            'current_regime': self.regimes[current_state],
            'confidence': float(max(trans_probs)),
            'transition_probs': {
                self.regimes[i]: float(p)
                for i, p in enumerate(trans_probs)
            }
        }
```

## Output Format

```python
{
    'current_regime': 'ranging',
    'confidence': 0.73,
    'transition_probs': {
        'trending_up': 0.45,
        'trending_down': 0.15,
        'ranging': 0.35,
        'volatile': 0.05
    }
}
```

## Agent Message Format

> "Market regime: RANGING (73% confidence). 45% probability of transition to TRENDING_UP within 3 sessions."

## Strategy Implications

| Regime | Strategy |
|--------|----------|
| `trending_up` | Trend following, pyramiding |
| `trending_down` | Short positions, protective stops |
| `ranging` | Mean reversion, range trading |
| `volatile` | Reduce position size, widen stops |
