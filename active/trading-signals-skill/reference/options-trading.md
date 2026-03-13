# Options Trading — Greeks, Pricing & Volatility

## The Greeks — Your Risk Dashboard

Greeks measure how an option's price changes in response to market variables. Think of them as dials on a control panel — each one tells you a different dimension of risk.

### First-Order Greeks

| Greek | Measures | Range | What It Means |
|-------|----------|-------|---------------|
| **Delta (Δ)** | Price sensitivity | -1 to +1 | How much option moves per $1 underlying move |
| **Gamma (Γ)** | Delta acceleration | 0+ | How fast delta changes (delta of delta) |
| **Theta (Θ)** | Time decay | Usually negative | How much value bleeds per day |
| **Vega (ν)** | Vol sensitivity | 0+ | How much option moves per 1% IV change |
| **Rho (ρ)** | Rate sensitivity | Small | Impact of interest rate changes |

**Delta as probability proxy:** A 0.30 delta call has roughly a 30% chance of expiring ITM. ATM options are ~0.50 delta. This is an approximation — real probability depends on the vol surface — but it's useful for quick strike selection.

**Gamma risk concentrates near expiration.** ATM options with <7 DTE have explosive gamma. This is why zero-DTE trades are thrilling but dangerous — your delta can flip from 0.30 to 0.80 in minutes. The Black-Scholes gamma formula shows this: gamma scales inversely with sqrt(time).

**Theta accelerates inside 45 DTE.** The time decay curve is not linear — it's roughly proportional to 1/sqrt(T). At 90 DTE, decay is gentle. At 30 DTE, it's noticeable. Inside 14 DTE, it's aggressive. This is why premium sellers target the 30-45 DTE window — maximum theta capture before gamma risk spikes.

**Vega is highest for ATM, long-dated options.** A 90-DTE ATM option might have vega of 0.40 (gains $0.40 per 1% IV increase). A 7-DTE option might have vega of 0.05. If you're playing an IV expansion event (earnings, FOMC), you want high vega. If you're selling premium, you want low vega or negative vega exposure.

### Second-Order Greeks

These matter for portfolio-level risk and sophisticated strategies. From SwaggyStacks' `options_trading.py`:

| Greek | Measures | Why It Matters |
|-------|----------|----------------|
| **Vanna** | dDelta/dVol | Delta shifts when IV changes — critical for skew trades |
| **Charm** | dDelta/dTime | Delta drift from time passage — affects hedging frequency |
| **Vomma** | dVega/dVol | Vega convexity — big IV moves amplify vega itself |
| **Veta** | dVega/dTime | Vega decay — long-dated vega is more stable |
| **Color** | dGamma/dTime | Gamma evolution — predicts when gamma risk spikes |
| **Speed** | dGamma/dPrice | Gamma sensitivity to underlying — relevant for large moves |
| **Zomma** | dGamma/dVol | Gamma changes with IV — matters during vol events |
| **Ultima** | dVomma/dVol | Third-order vol sensitivity — extreme tail risk |

**When second-order Greeks matter:**
- Portfolio with 50+ options contracts → charm and vanna dominate daily P&L
- Gamma scalping strategy → speed and color determine rehedge timing
- Vol event trades (earnings, FOMC) → vomma and zomma predict nonlinear P&L
- Tail risk hedging → ultima warns of convexity blowups

## Black-Scholes Pricing

The foundation. From ThetaRoom's `greeks_actor.py`:

```python
from scipy.stats import norm
import numpy as np

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    S: spot price    K: strike    T: time to expiry (years)
    r: risk-free rate    sigma: implied volatility
    """
    d1 = (np.log(S/K) + (r + sigma**2/2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else:
        return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
```

**Key insight:** Black-Scholes assumes constant volatility, log-normal returns, and no dividends. Real markets violate all three. The model is "wrong" but useful — it provides a common language for option pricing and Greeks. The vol surface (smile/skew) captures what Black-Scholes misses.

## Implied Volatility

### IV Calculation

IV is the volatility the market is pricing into an option. You solve for it numerically — there's no closed-form solution. From SwaggyStacks:

```python
from scipy.optimize import brentq

def implied_vol(market_price, S, K, T, r, option_type='call'):
    """Solve for IV using Brent's method (fast, reliable)"""
    def objective(sigma):
        return black_scholes(S, K, T, r, sigma, option_type) - market_price

    return brentq(objective, 0.01, 5.0)  # IV between 1% and 500%
```

### IV Rank & IV Percentile

| Metric | Formula | Use |
|--------|---------|-----|
| **IV Rank** | (Current IV - 52wk Low) / (52wk High - 52wk Low) | Where is IV relative to its range? |
| **IV Percentile** | % of days IV was lower than current | How often has IV been this low? |

**Why it matters:** An IV rank of 80% means current IV is near the top of its annual range — premiums are expensive, favoring premium selling strategies (iron condors, credit spreads, short strangles). IV rank below 20% means cheap premiums — favor buying strategies (long straddles, debit spreads).

**ThetaRoom v2 threshold:** `min_iv_rank_entry = 20.0` — won't enter premium-selling trades below 20% IV rank.

### Volatility Surface

The vol surface maps IV across strikes and expirations. It captures two phenomena:

**Volatility Skew:** OTM puts typically have higher IV than OTM calls (in equities). This reflects crash risk — investors pay more for downside protection. The skew steepens during market stress.

**Volatility Term Structure:** Near-term IV can differ from long-term IV. Before events (earnings, FOMC), near-term IV spikes while long-term remains stable. This creates opportunities for calendar spreads.

```python
# From SwaggyStacks — vol surface interpolation
from scipy.interpolate import griddata

def build_vol_surface(strikes, expiries, ivs):
    """Interpolate IV across strike-expiry grid"""
    grid_strikes = np.linspace(min(strikes), max(strikes), 50)
    grid_expiries = np.linspace(min(expiries), max(expiries), 30)
    return griddata((strikes, expiries), ivs,
                    (grid_strikes[None,:], grid_expiries[:,None]),
                    method='cubic')
```

## Gamma Exposure (GEX)

GEX measures net gamma across all options at each strike. It reveals where market makers need to hedge, creating predictable price behavior:

- **Positive GEX:** Market makers are long gamma → they buy dips, sell rallies → dampens volatility → price pins to high-GEX strikes
- **Negative GEX:** Market makers are short gamma → they sell dips, buy rallies → amplifies volatility → fast moves and gaps

**Pin risk:** As expiration approaches, high open interest strikes act as magnets. Price tends to "pin" to max-pain (the strike where total option value is minimized). This effect is strongest on monthly OpEx Fridays.

## Options Flow & Institutional Signals

- **Unusual options activity:** Volume > 3x average OI at a specific strike signals institutional positioning
- **Put/Call ratio:** Elevated ratios (>1.2) can signal fear (contrarian bullish) or hedging (neutral)
- **Dark pool prints:** Large block trades off-exchange often precede significant moves
- **Sweep orders:** Aggressive fills across multiple exchanges indicate urgency

## Data Sources

| Source | Assets | Features |
|--------|--------|----------|
| Polygon.io | Stocks, Options, Crypto, Forex | Real-time + historical, options chain snapshots |
| Alpaca SDK | Stocks, Options, Crypto | Trading + data, paper trading |
| Deribit | BTC/ETH options | ~90% crypto options market share |
| yfinance | Stocks, ETFs | Free historical data, options chains |
| IBKR | All asset classes | Professional-grade data + execution |

## Integration with ThetaRoom

The 8-node pipeline processes options through multiple stages:
1. **Scanner** → screens universe for high IV rank opportunities
2. **Volatility** → builds vol surface, detects skew anomalies
3. **Greeks** → calculates portfolio Greeks, identifies imbalances
4. **Risk** → pre-trade checks against position limits
5. **Entry** → generates specific strike/expiry recommendations
6. **Position** → Kelly Criterion sizing with Greeks constraints
7. **Execution** → smart order routing with fill improvement
8. **Exit** → stop-loss, profit target, DTE-based exit rules
