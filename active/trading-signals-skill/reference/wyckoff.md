# Wyckoff Method

## Purpose

Detect accumulation/distribution phases and institutional footprints.

## Phase State Machines

**Accumulation:**
```
PS → SC → AR → ST → Spring → SOS → LPS → BU
```

- PS: Preliminary Support
- SC: Selling Climax
- AR: Automatic Rally
- ST: Secondary Test
- Spring: Shakeout below support
- SOS: Sign of Strength
- LPS: Last Point of Support
- BU: Backup/Breakout

**Distribution:**
```
PSY → BC → AR → ST → UTAD → SOW → LPSY → SOW
```

- PSY: Preliminary Supply
- BC: Buying Climax
- AR: Automatic Reaction
- ST: Secondary Test
- UTAD: Upthrust After Distribution
- SOW: Sign of Weakness
- LPSY: Last Point of Supply

## Volume Spread Analysis (VSA)

Key patterns:
- No demand / No supply bars
- Stopping volume
- Effort vs Result divergence

## Crypto Enhancement

```python
# On-chain signals for Wyckoff
whale_activity = await self._get_whale_movements(symbol)
exchange_flows = await self._get_exchange_netflow(symbol)
funding_rate = await self._get_funding_rate(symbol)

# Negative funding during accumulation = SPRING_CONFIRMATION
# Positive funding during distribution = UTAD_CONFIRMATION
```

## Agent Message Format

> "Wyckoff Accumulation Phase 70% complete. Spring test successful. Watching for Sign of Strength."

## Phase Completion Scoring

| Phase | Weight |
|-------|--------|
| PS/PSY identified | 10% |
| SC/BC confirmed | 20% |
| AR complete | 30% |
| ST successful | 50% |
| Spring/UTAD | 70% |
| SOS/SOW | 85% |
| LPS/LPSY | 95% |
| BU/Breakdown | 100% |

## Composite Operator On-Chain Signals

From SwaggyStacks' `btc_wyckoff.py` — the "Composite Operator" is Wyckoff's concept of smart money: the large institutions that move markets. In crypto, on-chain data reveals their behavior directly.

```python
# Composite Operator detection via on-chain metrics
COMPOSITE_SIGNALS = {
    'accumulation': {
        'exchange_netflow': '< -1000 BTC (7d)',  # Coins leaving exchanges = accumulation
        'miner_reserves': 'stable or increasing',
        'lth_supply': '> 14M BTC',  # Long-term holders (>155 days) holding
        'funding_rate': 'negative',  # Leverage traders bearish = contrarian buy
    },
    'distribution': {
        'exchange_netflow': '> +1000 BTC (7d)',  # Coins entering exchanges = selling
        'miner_reserves': 'declining',
        'lth_supply': 'declining',
        'funding_rate': '> 0.05%',  # Extreme leverage = crowded trade
    }
}
```

**Why This Matters:**
When you see 1000+ BTC flowing OUT of exchanges over 7 days while long-term holders maintain their positions, that's the Composite Operator accumulating. They're buying OTC or withdrawing to cold storage — the opposite of retail dumping on exchanges. This on-chain transparency is what makes Wyckoff analysis far more powerful in crypto than in traditional markets.

## Volume Spread Analysis (VSA) Implementation

Expanding on the core VSA patterns — these are the mechanical signals that reveal smart money activity within price bars.

```python
class VolumeSpreadAnalyzer:
    def detect_stopping_volume(self, df):
        """High volume + narrow spread = absorption by smart money"""
        # Volume > 2x average BUT range < 50% average range
        # This means large participants are absorbing selling pressure
        avg_vol = df['volume'].rolling(20).mean()
        avg_range = (df['high'] - df['low']).rolling(20).mean()
        current_range = df['high'] - df['low']
        return (df['volume'] > 2 * avg_vol) & (current_range < 0.5 * avg_range)

    def detect_no_demand(self, df):
        """Up bar on declining volume = no buying interest"""
        # Close > open, volume < previous 2 bars, narrow range
        up_bar = df['close'] > df['open']
        low_vol = df['volume'] < df['volume'].shift(1).rolling(2).mean()
        narrow = (df['high'] - df['low']) < (df['high'] - df['low']).rolling(10).mean() * 0.7
        return up_bar & low_vol & narrow

    def detect_effort_vs_result(self, df):
        """High volume should produce proportional price movement"""
        # Volume spike (>2x avg) with small range = divergence
        # Smart money absorbing without moving price
        avg_vol = df['volume'].rolling(20).mean()
        avg_range = (df['high'] - df['low']).rolling(20).mean()
        current_range = df['high'] - df['low']
        high_effort = df['volume'] > 2 * avg_vol
        low_result = current_range < 0.6 * avg_range
        return high_effort & low_result
```

## Wyckoff Analyzer Implementation

From ThetaRoom v1 `backend/methodologies/wyckoff.py` — the full analysis pipeline that ties phases, events, and signals together.

```python
class WyckoffAnalyzer:
    def analyze(self, df: pd.DataFrame, symbol: str) -> dict:
        phase = self._detect_phase(df)
        completion = self._calculate_completion(phase, df)
        signal, confidence = self._generate_signal(phase, completion)

        return {
            'phase': phase,  # 'accumulation' | 'markup' | 'distribution' | 'markdown'
            'completion_pct': completion,
            'current_event': self._identify_event(df, phase),
            'signal': signal,
            'confidence': confidence,
            'composite_operator': self._check_on_chain(symbol) if self._is_crypto(symbol) else None
        }
```

## Phase-to-Signal Mapping

| Phase + Event | Signal | Confidence | Why |
|---------------|--------|------------|-----|
| Accumulation + Spring | BUY | 0.75 | Smart money trap complete, markup imminent |
| Accumulation + SOS | BUY | 0.80 | Confirmed demand, breakout underway |
| Distribution + UTAD | SELL | 0.70 | Failed breakout, distribution confirmed |
| Distribution + SOW | SELL | 0.80 | Weakness confirmed, markdown starting |
| Markup (mid-phase) | HOLD LONG | 0.65 | Trend in progress |
| Markdown (mid-phase) | HOLD SHORT | 0.65 | Downtrend in progress |

## Integration with Other Methodologies

| Method | Confluence Signal |
|--------|------------------|
| Elliott Wave | Wave 1 start often aligns with Accumulation SOS |
| Fibonacci | Spring at 0.786 retracement = high conviction accumulation |
| Turtle | Turtle breakout after Accumulation BU = confirmed trend start |
| Markov | Wyckoff Accumulation + Markov `accumulation` regime = strongest signal |
| Pattern Recognition | Double bottom pattern often IS Wyckoff Spring + ST |
