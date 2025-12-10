# Turtle Trading System

## Core Concept

Trend-following breakout system developed by Richard Dennis. "Trade like a turtle" - slow, methodical, rule-based.

## System Parameters

### System 1 (Short-term)
- **Entry**: 20-day high/low breakout
- **Exit**: 10-day opposite breakout
- **Skip Rule**: Skip if last signal was profitable

### System 2 (Long-term)
- **Entry**: 55-day high/low breakout
- **Exit**: 20-day opposite breakout
- **No skip rule** - take every signal

## Donchian Channels

```python
def calculate_donchian_channels(df: pd.DataFrame) -> dict:
    return {
        'system1_entry_high': df['high'].rolling(20).max(),
        'system1_entry_low': df['low'].rolling(20).min(),
        'system1_exit_high': df['high'].rolling(10).max(),
        'system1_exit_low': df['low'].rolling(10).min(),
        'system2_entry_high': df['high'].rolling(55).max(),
        'system2_entry_low': df['low'].rolling(55).min(),
        'system2_exit_high': df['high'].rolling(20).max(),
        'system2_exit_low': df['low'].rolling(20).min(),
    }
```

## Position Sizing (ATR-Based)

```python
def calculate_position_size(account: float, atr: float, price: float) -> int:
    """1 ATR = 1% account risk"""
    risk_per_unit = atr * price
    dollar_risk = account * 0.01  # 1% risk
    units = dollar_risk / risk_per_unit
    return int(units)
```

**N (Volatility Unit)** = 20-period ATR

## Pyramiding

Add positions at 0.5N intervals (half ATR):
```python
def get_pyramid_levels(entry: float, atr: float, direction: str) -> list:
    """Max 4 units total"""
    levels = [entry]
    for i in range(1, 4):
        if direction == 'long':
            levels.append(entry + (i * 0.5 * atr))
        else:
            levels.append(entry - (i * 0.5 * atr))
    return levels
```

## Stop Loss

**2N Stop**: 2 × ATR from entry

```python
def calculate_stop(entry: float, atr: float, direction: str) -> float:
    if direction == 'long':
        return entry - (2 * atr)
    return entry + (2 * atr)
```

## Crypto Adaptations

From ThetaRoom/SwaggyStacks implementations:

### Higher ATR Multiplier
```python
# Traditional: 2.0 ATR stop
# Crypto: 3.0 ATR stop (higher volatility)
CRYPTO_ATR_MULTIPLIER = 3.0
```

### Funding Rate Filter (Perpetuals)
```python
def should_trade(funding_rate: float, direction: str) -> bool:
    """Avoid crowded trades"""
    if direction == 'long' and funding_rate > 0.03:  # >3%
        return False  # Crowded long
    if direction == 'short' and funding_rate < -0.02:  # <-2%
        return False  # Crowded short
    return True
```

### Halving Cycle Position Scaling
```python
CYCLE_POSITION_SCALE = {
    'accumulation': 1.2,    # Increase size
    'early_markup': 1.0,    # Normal
    'late_markup': 0.75,    # Reduce into top
    'distribution': 0.5,    # Minimal exposure
}
```

## Implementation

```python
class TurtleSystem:
    def __init__(self, system: int = 1):
        self.entry_period = 20 if system == 1 else 55
        self.exit_period = 10 if system == 1 else 20
        self.atr_period = 20
        self.max_units = 4

    def analyze(self, df: pd.DataFrame) -> dict:
        channels = self._calculate_channels(df)
        atr = self._calculate_atr(df)

        signal, breakout_type = self._check_breakout(df, channels)

        if signal != 'NEUTRAL':
            entry = df['close'].iloc[-1]
            stop = self._calculate_stop(entry, atr, signal.lower())
            pyramids = self._get_pyramid_levels(entry, atr, signal.lower())

            return {
                'signal': signal,
                'entry': entry,
                'stop': stop,
                'pyramid_levels': pyramids,
                'position_size': self._calculate_size(atr),
                'system': self.entry_period,
                'atr': atr
            }

        return {'signal': 'NEUTRAL'}
```

## Signal Logic

| Condition | Signal |
|-----------|--------|
| Close > N-day high | LONG_ENTRY |
| Close < N-day low | SHORT_ENTRY |
| Long position + Close < Exit low | EXIT_LONG |
| Short position + Close > Exit high | EXIT_SHORT |

## Agent Message Format

> "Turtle System 1 LONG signal. 20-day breakout at $XXX. Entry: $XXX, Stop: $YYY (2N), First pyramid at $ZZZ. Position size: X units (1% risk per unit)."

## When to Use

| Market Condition | Turtle Effectiveness |
|-----------------|---------------------|
| Strong trend | High - designed for this |
| Ranging/Choppy | Low - many false breakouts |
| High volatility | Medium - wider stops help |
| Low volatility | Medium - fewer signals |

## Integration with Other Methods

- **Markov Regime**: Only trade Turtle in `trending_up` or `trending_down` regimes
- **Wyckoff**: Turtle breakout after Spring = high conviction
- **Elliott Wave**: Turtle entry aligned with Wave 3 start = high conviction
