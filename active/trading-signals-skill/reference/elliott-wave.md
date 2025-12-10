# Elliott Wave Analysis

## Validation Rules (Must Enforce)

- Wave 2 cannot retrace 100% of Wave 1
- Wave 3 is never the shortest impulse wave
- Wave 4 cannot overlap Wave 1 price territory

## Wave Structure

**Impulse (5-wave move in trend direction):**
- Wave 1: Initial move, accumulation breakout
- Wave 2: Retracement (never beyond Wave 1 start)
- Wave 3: Strongest, never shortest, institutional buying
- Wave 4: Consolidation (never overlaps Wave 1)
- Wave 5: Final push, often with divergence

**Corrective (3-wave counter-trend):**
- A-B-C patterns: Zigzag, Flat, Triangle

## Wave Relationships (Fibonacci)

| Wave | Retracement/Extension | Typical |
|------|----------------------|---------|
| Wave 2 | Retraces Wave 1 | 38-62% |
| Wave 3 | Extends Wave 1 | 1.618-2.618x |
| Wave 4 | Retraces Wave 3 | 24-38% |
| Wave 5 | Extends Wave 1 | 0.618-1.0x |

## Crypto Adaptation

```python
WAVE_TIME_MULTIPLIER = 0.6  # 40% faster cycles
EXTENDED_TARGETS = [2.618, 3.618, 4.236]  # Common in crypto
```

## Bitcoin Halving Supercycle (from SwaggyStacks)

Maps Elliott waves to 4-year halving cycles:

```python
HALVING_WAVE_MAP = {
    'wave_1': {
        'phase': 'post_halving_accumulation',
        'duration': '6-12 months',
        'confidence': 0.60,
        'character': 'Stealth accumulation, disbelief'
    },
    'wave_2': {
        'phase': 'retest',
        'retracement': '38-62%',
        'confidence': 0.55,
        'character': 'Fear return, "dead cat bounce" narrative'
    },
    'wave_3': {
        'phase': 'main_bull_run',
        'extension': '1.618-2.618x of Wave 1',
        'confidence': 0.75,
        'character': 'FOMO, institutional adoption, ATHs'
    },
    'wave_4': {
        'phase': 'mid_cycle_correction',
        'retracement': '24-38%',
        'confidence': 0.60,
        'character': 'Profit-taking, consolidation'
    },
    'wave_5': {
        'phase': 'euphoric_top',
        'extension': '0.618-1.0x of Wave 1',
        'confidence': 0.60,
        'character': 'Retail FOMO, media frenzy, blow-off top'
    }
}
```

## Implementation

```python
class ElliottWaveAnalyzer:
    PIVOT_THRESHOLD = 0.02  # 2% for swing detection

    def analyze(self, df: pd.DataFrame, symbol: str) -> dict:
        pivots = self._detect_pivots(df)
        waves = self._count_waves(pivots, df)
        targets = self._project_targets(waves, pivots, df)

        current_wave = waves[-1] if waves else None
        signal, confidence = self._determine_signal(current_wave, df)

        return {
            'wave_count': len(waves),
            'current_wave': current_wave,
            'wave_type': 'impulse' if len(waves) <= 5 else 'corrective',
            'targets': targets,
            'invalidation': self._get_invalidation(waves),
            'signal': signal,
            'confidence': confidence
        }

    def _detect_pivots(self, df: pd.DataFrame) -> list:
        """Zigzag pattern identification"""
        pivots = []
        # Find swing highs and lows with threshold
        return pivots

    def _validate_waves(self, waves: list) -> bool:
        """Enforce Elliott rules"""
        if len(waves) < 3:
            return True

        # Rule 1: Wave 2 cannot retrace 100% of Wave 1
        if waves[1]['end'] <= waves[0]['start']:
            return False

        # Rule 2: Wave 3 never shortest (check when we have 5)
        if len(waves) >= 5:
            w1_len = abs(waves[0]['end'] - waves[0]['start'])
            w3_len = abs(waves[2]['end'] - waves[2]['start'])
            w5_len = abs(waves[4]['end'] - waves[4]['start'])
            if w3_len < w1_len and w3_len < w5_len:
                return False

        # Rule 3: Wave 4 cannot overlap Wave 1
        if len(waves) >= 4:
            if waves[3]['end'] <= waves[0]['end']:
                return False

        return True
```

## Target Projection

```python
def project_wave_targets(waves: list, current_wave: int) -> dict:
    w1_length = abs(waves[0]['end'] - waves[0]['start'])

    if current_wave == 3:
        return {
            'conservative': waves[1]['end'] + (w1_length * 1.618),
            'target': waves[1]['end'] + (w1_length * 2.0),
            'extended': waves[1]['end'] + (w1_length * 2.618)
        }
    elif current_wave == 5:
        return {
            'conservative': waves[3]['end'] + (w1_length * 0.618),
            'target': waves[3]['end'] + w1_length,
            'extended': waves[3]['end'] + (w1_length * 1.618)
        }
```

## Confidence Scoring

```python
def calculate_confidence(wave_position: str, wave_type: str) -> float:
    """Confidence varies by wave position"""
    base_confidence = {
        'wave_1': 0.50,  # Hard to identify early
        'wave_2': 0.55,
        'wave_3': 0.75,  # Most reliable
        'wave_4': 0.60,
        'wave_5': 0.60,
        'wave_a': 0.50,
        'wave_b': 0.45,
        'wave_c': 0.55
    }
    return base_confidence.get(wave_position, 0.50)
```

## Agent Message Format

> "We're in Wave 3 of a bullish impulse (halving supercycle). Target: $XXX (1.618 extension), Extended: $YYY (2.618). Invalidation below $ZZZ (Wave 1 high). Confidence: 75%."

## Integration with Other Methods

| Method | Confluence Signal |
|--------|------------------|
| Fibonacci | Wave 2/4 at golden zone (0.618) = high conviction |
| Wyckoff | Wave 1 start = SOS after Spring |
| Turtle | Wave 3 breakout aligns with Donchian breakout |
| Markov | Wave 3 in `trending_up` regime = strongest signal |
