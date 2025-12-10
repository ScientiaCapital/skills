# Pattern Recognition

## Candlestick Patterns

### High-Probability Patterns

| Pattern | Direction | Strength | Success Rate |
|---------|-----------|----------|--------------|
| Three White Soldiers | Bullish | 0.80 | 75% |
| Three Black Crows | Bearish | 0.80 | 73% |
| Bullish Engulfing | Bullish | 0.70 | 68% |
| Bearish Engulfing | Bearish | 0.70 | 66% |
| Morning Star | Bullish | 0.75 | 70% |
| Evening Star | Bearish | 0.75 | 68% |
| Hammer | Bullish | 0.65 | 62% |
| Shooting Star | Bearish | 0.65 | 60% |
| Doji | Neutral/Reversal | 0.40 | 50% |

### Pattern Detection

```python
class PatternDetector:
    def detect_engulfing(self, df: pd.DataFrame) -> dict:
        """Detect bullish/bearish engulfing patterns"""
        curr = df.iloc[-1]
        prev = df.iloc[-2]

        # Bullish Engulfing
        if (prev['close'] < prev['open'] and  # Previous red
            curr['close'] > curr['open'] and  # Current green
            curr['open'] < prev['close'] and  # Opens below prev close
            curr['close'] > prev['open']):    # Closes above prev open
            return {'pattern': 'bullish_engulfing', 'strength': 0.70}

        # Bearish Engulfing
        if (prev['close'] > prev['open'] and  # Previous green
            curr['close'] < curr['open'] and  # Current red
            curr['open'] > prev['close'] and  # Opens above prev close
            curr['close'] < prev['open']):    # Closes below prev open
            return {'pattern': 'bearish_engulfing', 'strength': 0.70}

        return None

    def detect_doji(self, df: pd.DataFrame) -> dict:
        """Doji = indecision, body < 10% of range"""
        curr = df.iloc[-1]
        body = abs(curr['close'] - curr['open'])
        range_ = curr['high'] - curr['low']

        if range_ > 0 and body / range_ < 0.1:
            return {'pattern': 'doji', 'strength': 0.40}
        return None

    def detect_hammer(self, df: pd.DataFrame) -> dict:
        """Hammer at support = bullish reversal"""
        curr = df.iloc[-1]
        body = abs(curr['close'] - curr['open'])
        lower_wick = min(curr['open'], curr['close']) - curr['low']
        upper_wick = curr['high'] - max(curr['open'], curr['close'])

        # Lower wick >= 2x body, small upper wick
        if lower_wick >= 2 * body and upper_wick < body * 0.5:
            return {'pattern': 'hammer', 'strength': 0.65}
        return None
```

## Chart Patterns

### Reversal Patterns

| Pattern | Direction | Target Calculation |
|---------|-----------|-------------------|
| Head & Shoulders | Bearish | Neckline - (Head - Neckline) |
| Inverse H&S | Bullish | Neckline + (Neckline - Head) |
| Double Top | Bearish | Support - (Resistance - Support) |
| Double Bottom | Bullish | Resistance + (Resistance - Support) |
| Triple Top/Bottom | Same as double | Same as double |

### Continuation Patterns

| Pattern | Direction | Target |
|---------|-----------|--------|
| Bull Flag | Bullish | Flagpole projected from breakout |
| Bear Flag | Bearish | Flagpole projected from breakdown |
| Ascending Triangle | Bullish | Height added to resistance |
| Descending Triangle | Bearish | Height subtracted from support |
| Symmetrical Triangle | Either | Height from breakout point |

### Chart Pattern Detection

```python
class ChartPatternDetector:
    def detect_double_bottom(self, df: pd.DataFrame, tolerance: float = 0.02) -> dict:
        """Detect W pattern"""
        lows = self._find_swing_lows(df)

        if len(lows) >= 2:
            low1, low2 = lows[-2], lows[-1]

            # Lows within tolerance
            if abs(low1['price'] - low2['price']) / low1['price'] < tolerance:
                neckline = max(df['high'].iloc[low1['idx']:low2['idx']])
                pattern_height = neckline - low1['price']

                return {
                    'pattern': 'double_bottom',
                    'direction': 'bullish',
                    'neckline': neckline,
                    'target': neckline + pattern_height,
                    'stop': min(low1['price'], low2['price']) * 0.98,
                    'success_rate': 0.71
                }
        return None

    def detect_head_shoulders(self, df: pd.DataFrame) -> dict:
        """Detect H&S top pattern"""
        highs = self._find_swing_highs(df)

        if len(highs) >= 3:
            left, head, right = highs[-3], highs[-2], highs[-1]

            # Head higher than shoulders, shoulders roughly equal
            if (head['price'] > left['price'] and
                head['price'] > right['price'] and
                abs(left['price'] - right['price']) / left['price'] < 0.03):

                neckline = min(
                    df['low'].iloc[left['idx']:head['idx']].min(),
                    df['low'].iloc[head['idx']:right['idx']].min()
                )
                pattern_height = head['price'] - neckline

                return {
                    'pattern': 'head_and_shoulders',
                    'direction': 'bearish',
                    'neckline': neckline,
                    'target': neckline - pattern_height,
                    'stop': head['price'] * 1.02,
                    'success_rate': 0.65
                }
        return None
```

## Confluence Scoring

```python
def calculate_pattern_confluence(patterns: list, fib_levels: dict, support_resistance: list) -> float:
    """Pattern + Level confluence = higher conviction"""
    score = 0

    for pattern in patterns:
        base_score = pattern.get('strength', 0.5)

        # At Fibonacci level?
        for level, price in fib_levels.items():
            if abs(pattern['price'] - price) / price < 0.02:
                base_score += 0.2

        # At support/resistance?
        for sr in support_resistance:
            if abs(pattern['price'] - sr) / sr < 0.02:
                base_score += 0.15

        score = max(score, min(base_score, 1.0))

    return score
```

## Volume Confirmation

```python
def confirm_with_volume(pattern: dict, df: pd.DataFrame) -> bool:
    """Patterns need volume confirmation"""
    avg_volume = df['volume'].rolling(20).mean().iloc[-1]
    current_volume = df['volume'].iloc[-1]

    # Breakout patterns need above-average volume
    if pattern['type'] in ['engulfing', 'three_soldiers', 'breakout']:
        return current_volume > avg_volume * 1.5

    # Reversal patterns need volume spike
    if pattern['type'] in ['hammer', 'doji', 'star']:
        return current_volume > avg_volume * 1.2

    return True
```

## Agent Message Format

> "Bullish Engulfing at Golden Pocket ($XXX). Volume 180% of average. Pattern strength: 0.70 + Fib confluence: 0.20 = 0.90 conviction. Target: $YYY (0.382 fib)."

## Integration with Methodologies

| Pattern | Best Confluence |
|---------|----------------|
| Hammer at support | Wyckoff Spring, Fib 0.786 |
| Engulfing | Elliott Wave 2/4 completion |
| Three Soldiers | Turtle breakout confirmation |
| H&S breakdown | Distribution phase completion |
| Double bottom | Accumulation Spring test |
