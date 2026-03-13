# Markov Regime Detection

Regime detection answers the most important question before any trade: **what kind of market are we in?** The wrong strategy in the wrong regime is a guaranteed loss — trend following in a range, mean reversion in a trend. Identify regime first, then pick tools.

## 7-State Bitcoin Model (SwaggyStacks)

The advanced model uses 7 states that capture the full cycle of crypto markets. Each state has distinct volatility characteristics, on-chain patterns, and strategy implications.

| State | Volatility | Description | What's Happening |
|-------|-----------|-------------|------------------|
| **Accumulation** | Low (<40% ann.) | Smart money buying quietly | Long-term holders accumulating, price range-bound, retail disinterested |
| **Bull Quiet** | Low-Medium | Steady uptrend, low drama | Consistent higher highs/lows, growing volume, institutional entries |
| **Bull Volatile** | High (>80% ann.) | Aggressive rally with pullbacks | Sharp moves up, 10-20% corrections, leverage building |
| **Euphoria** | Extreme (>120% ann.) | Parabolic blow-off top | Retail FOMO, media frenzy, funding rates extreme, everything is "going to the moon" |
| **Distribution** | Medium-High | Smart money selling to retail | Range-bound at highs, decreasing volume on rallies, increasing volume on drops |
| **Bear Quiet** | Medium | Steady downtrend, capitulation grinding | Slow bleed, low volume, apathy, "crypto is dead" narratives |
| **Bear Volatile** | High | Panic selling, cascading liquidations | Flash crashes, exchange outages, forced selling, margin calls |

**Why 7 states instead of 4:** The simple 4-state model (trending_up/down, ranging, volatile) misses critical transitions. Accumulation and Distribution look similar on price charts (both range-bound) but have opposite implications. Bull Quiet and Bull Volatile require different position sizing. The 7-state model captures the full market cycle.

## 4-State General Model (All Assets)

For non-crypto assets, the simpler 4-state model works well:

| Regime | Criteria | Strategy |
|--------|----------|----------|
| `trending_up` | ADX > 25, +DI > -DI | Trend following, pyramiding, debit spreads |
| `trending_down` | ADX > 25, -DI > +DI | Short positions, protective stops, bear call spreads |
| `ranging` | ADX < 20 | Mean reversion, iron condors, range trading |
| `volatile` | ATR expansion > 2 std dev | Reduce size, widen stops, long straddles |

## Implementation

```python
from hmmlearn import hmm

class MarkovRegimeDetector:
    """7-state model for crypto, 4-state for traditional assets"""

    def __init__(self, n_regimes: int = 7, asset_type: str = 'crypto'):
        self.model = hmm.GaussianHMM(
            n_components=n_regimes,
            covariance_type="full",
            n_iter=100
        )
        if asset_type == 'crypto':
            self.regimes = [
                'accumulation', 'bull_quiet', 'bull_volatile',
                'euphoria', 'distribution', 'bear_quiet', 'bear_volatile'
            ]
        else:
            self.regimes = ['trending_up', 'trending_down', 'ranging', 'volatile']

    def fit(self, returns: np.ndarray, volatility: np.ndarray):
        """Fit HMM on returns + volatility features"""
        features = np.column_stack([returns, volatility])
        self.model.fit(features)

    def predict(self, returns: np.ndarray, volatility: np.ndarray) -> dict:
        features = np.column_stack([returns, volatility])
        current_state = self.model.predict(features)[-1]
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

## Volatility Clustering

Regimes tend to persist (volatility clusters). High-vol days follow high-vol days. This is captured by the transition matrix — the diagonal values (staying in the same state) are typically 0.85-0.95, meaning regime changes are infrequent but significant.

```python
# Typical transition probabilities — diagonal is "stay in state"
# Accumulation has ~90% chance of staying in accumulation next period
# Transitions to adjacent states are most likely (accumulation → bull_quiet, not accumulation → euphoria)
```

## VIX-Based Regime Override

From ThetaRoom v2 config:
```python
vix_crisis_threshold = 35.0  # Override to crisis/bear_volatile regardless of model output
```

When VIX exceeds 35, the Markov model is overridden:
- All position sizes cut to minimum
- Only hedging trades allowed
- Existing positions reviewed for stop-loss tightening

## On-Chain Confirmation (Bitcoin)

The Markov model is enhanced with on-chain data for crypto:

| Metric | What It Shows | Regime Signal |
|--------|---------------|---------------|
| MVRV Ratio | Market value vs realized value | >3.5 = Euphoria, <1.0 = Accumulation |
| NUPL | Net unrealized profit/loss | >0.75 = Euphoria, <0 = Capitulation |
| Exchange Flows | BTC moving to/from exchanges | Inflows = selling pressure, Outflows = accumulation |
| Hash Rate | Network security | Rising = miner confidence, Falling = stress |
| Funding Rates | Futures market leverage | >0.1% = Euphoria, <-0.05% = Bear Volatile |

## Confluence Weights by Regime

The regime determines how much weight each methodology gets in the confluence score:

```python
REGIME_WEIGHTS = {
    'trending_up':   {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
    'trending_down': {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
    'ranging':       {'fib': 0.35, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.05},
    'volatile':      {'fib': 0.30, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.10},
}
```

**Why turtle gets 0.05 in ranging:** Turtle Trading is a breakout system — it needs trends. In ranging markets, breakout attempts fail repeatedly (false breakouts). Fibonacci and Wyckoff dominate because they identify support/resistance within the range.

## Strategy Implications (Expanded)

| Regime | Options Strategy | Position Size | Key Action |
|--------|-----------------|---------------|------------|
| Accumulation | CSPs on dips, LEAPS calls | Full size | Buy slowly, build position |
| Bull Quiet | Covered calls, PMCC | Full size | Ride the trend, sell premium |
| Bull Volatile | Iron condors (wide), collars | 75% size | Protect gains, sell vol |
| Euphoria | Protective puts, take profits | 50% size | Reduce exposure, lock gains |
| Distribution | Bear call spreads, collars | 50% size | Hedge aggressively |
| Bear Quiet | CSPs at deep support | 50% size | Nibble at value, be patient |
| Bear Volatile | Cash, VIX calls only | 25% size | Preserve capital, wait |

## Agent Message Format

> "Market regime: BULL QUIET (85% confidence). Volatility: 45% annualized. Transition probabilities: 72% stay Bull Quiet, 18% to Bull Volatile, 8% to Distribution, 2% other. Strategy: full position sizes, trend following with covered calls."
