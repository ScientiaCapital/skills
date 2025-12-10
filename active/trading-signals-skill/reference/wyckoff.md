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
