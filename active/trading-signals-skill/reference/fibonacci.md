# Fibonacci Analysis

## Key Levels

| Type | Levels |
|------|--------|
| Retracement | 0.236, 0.382, 0.5, 0.618, 0.786 |
| Extension | 1.272, 1.618, 2.0, 2.618, 4.236 |
| **Golden Zone** | 0.618 - 0.786 (high probability reversal) |
| **Golden Pocket** | 0.618 - 0.65 (institutional money zone) |

## Golden Pocket (Institutional Grade)

From ThetaRoom's `golden_pocket_analyzer.py`:

```python
# The Golden Pocket: Where institutional money concentrates
GOLDEN_POCKET = {
    'lower': 0.618,
    'upper': 0.65,
    'description': 'Institutional accumulation zone',
    'confidence': 0.80
}

# Banks and institutions preferentially accumulate at 61.8%-65%
# Research shows highest reversal probability in this narrow band
```

**Why It Works:**
- Institutional algorithms target 0.618 retracement
- Stop-loss clusters below 0.65 create liquidity
- Smart money accumulates where retail gives up

## Implementation

```python
class FibonacciAnalyzer:
    RETRACEMENT_LEVELS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.65, 0.786, 1.0]
    EXTENSION_LEVELS = [1.272, 1.414, 1.618, 2.0, 2.618, 3.618]

    def analyze(self, df: pd.DataFrame) -> dict:
        swing_high, swing_low = self._find_swing_points(df)
        levels = self._calculate_levels(swing_high, swing_low)
        current_price = df['close'].iloc[-1]

        zone = self._identify_zone(current_price, levels)
        confluence = self._calculate_confluence(current_price, levels)

        return {
            'levels': levels,
            'current_zone': zone,
            'in_golden_pocket': self._is_golden_pocket(current_price, levels),
            'confluence_score': confluence,
            'signal': self._generate_signal(zone, confluence)
        }

    def _is_golden_pocket(self, price: float, levels: dict) -> bool:
        """Check if price is in institutional accumulation zone"""
        return levels['0.65'] <= price <= levels['0.618']

    def _calculate_levels(self, high: float, low: float) -> dict:
        diff = high - low
        levels = {}
        for ratio in self.RETRACEMENT_LEVELS:
            levels[str(ratio)] = high - diff * ratio
        for ratio in self.EXTENSION_LEVELS:
            levels[str(ratio)] = high + diff * (ratio - 1)
        return levels
```

## On-Chain Enhanced Fibonacci (Crypto)

From SwaggyStacks' `btc_fibonacci.py`:

```python
# Bitcoin-specific levels using on-chain data
ON_CHAIN_LEVELS = {
    'realized_price': 'Strong support - average cost basis',
    'rp_upper_band': 'realized_price * 3.5 - Historical top zone',
    'rp_lower_band': 'realized_price * 0.8 - Extreme accumulation'
}

# MVRV-Based Zone Classification
MVRV_ZONES = {
    'extreme_greed': {'mvrv': 3.5, 'action': 'Distribution zone'},
    'greed': {'mvrv': 2.5, 'action': 'Take profits'},
    'optimism': {'mvrv': 1.5, 'action': 'Hold'},
    'fear': {'mvrv': 1.0, 'action': 'Accumulate'},
    'extreme_fear': {'mvrv': 0.8, 'action': 'Strong buy zone'}
}
```

## Multi-Timeframe Confluence

```python
def calculate_confluence_score(price: float, levels_by_tf: dict) -> float:
    """Score increases when multiple timeframes align"""
    TOLERANCE = 0.02  # 2% proximity

    confluence_count = 0
    for tf, levels in levels_by_tf.items():
        for level_name, level_price in levels.items():
            if abs(price - level_price) / level_price < TOLERANCE:
                confluence_count += 1

    # Scoring
    if confluence_count >= 3:
        return 1.0  # Strong confluence
    elif confluence_count == 2:
        return 0.7
    elif confluence_count == 1:
        return 0.4
    return 0.0
```

| Timeframes Aligned | Confluence Score | Signal Strength |
|-------------------|------------------|-----------------|
| 1 | 0.4 | Weak |
| 2 | 0.7 | Moderate |
| 3+ | 1.0 | Strong |

## Signal Generation

```python
def generate_signal(self, current_price: float, levels: dict) -> dict:
    # Near support (within 2%)
    for level in ['0.618', '0.65', '0.786']:
        if self._near_level(current_price, levels[level], below=True):
            return {
                'signal': 'BUY',
                'level': level,
                'stop': levels['1.0'],  # Below swing low
                'target': levels['0.382'],
                'rr_ratio': self._calc_rr(current_price, levels)
            }

    # Near resistance
    for level in ['0.236', '0.382']:
        if self._near_level(current_price, levels[level], below=False):
            return {
                'signal': 'SELL',
                'level': level,
                'stop': levels['0.0'],  # Above swing high
                'target': levels['0.618']
            }

    return {'signal': 'NEUTRAL'}
```

## Agent Message Format

> "Price entering Golden Pocket ($XXX-$YYY). Institutional accumulation zone. 3 timeframe confluence at 0.618. R:R = 3.2:1. High probability long setup."

## Best Practices

1. Draw fibs from swing low to swing high (uptrend) or vice versa
2. **Golden Pocket (0.618-0.65)** has highest institutional interest
3. Look for confluence with horizontal support/resistance
4. Shallow retracement (0.236-0.382) = strong trend continuation
5. Deep retracement (0.786+) = trend weakness, potential reversal
6. Combine with volume analysis for confirmation

## Integration with Other Methods

| Method | Confluence Signal |
|--------|------------------|
| Elliott Wave | Wave 2/4 at golden pocket = high conviction |
| Wyckoff | Spring at 0.786 retracement = strong buy |
| Turtle | Breakout from golden zone = trend confirmation |
| Markov | Golden pocket in `ranging` regime = mean reversion |
