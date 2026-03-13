# Equities -- Stocks, ETFs & Sectors

## Why This Matters

Equities are the foundation of most trading portfolios. Understanding sector
rotation, screening methodology, and position sizing turns random stock picks
into a systematic edge. This reference covers the frameworks that ThetaRoom's
Scanner agent and Portfolio agent use to find, evaluate, and size equity trades.

---

## Sector Rotation Model

The economy moves through four phases. Different sectors lead in each phase
because their earnings respond to different macro drivers (interest rates,
consumer spending, commodity prices, credit conditions).

### The Four Phases

| Phase | Economic Signal | Leading Sectors | Lagging Sectors |
|-------|----------------|-----------------|-----------------|
| **Early Cycle** | Recovery from recession, rates low, credit easing | Technology, Consumer Discretionary, Industrials | Utilities, Energy |
| **Mid Cycle** | GDP expanding, earnings growing, rates rising | Technology, Healthcare, Financials | Utilities, Consumer Staples |
| **Late Cycle** | Growth slowing, inflation rising, rates peak | Energy, Materials, Healthcare | Technology, Consumer Discretionary |
| **Recession** | GDP contracting, rates falling, flight to safety | Utilities, Consumer Staples, Healthcare | Financials, Industrials, Energy |

### Why It Works

Sector rotation is not a timing tool -- it is a probability weighting tool.
You do not need to call the exact cycle turn. You need to overweight sectors
with tailwinds and underweight sectors with headwinds. Even a rough read of
the cycle improves risk-adjusted returns.

### How to Identify the Current Phase

- **Yield curve**: Steepening = early cycle. Flattening/inverting = late cycle.
- **ISM Manufacturing PMI**: Rising above 50 = expansion. Falling below 50 = contraction.
- **Unemployment claims**: Falling = early/mid cycle. Rising = late cycle/recession.
- **Credit spreads**: Tightening = risk-on. Widening = risk-off.

---

## Key Sectors and Their ETFs

| Sector | ETF | What Drives It | Volatility Profile |
|--------|-----|----------------|-------------------|
| Technology | XLK | Innovation, earnings growth, rate sensitivity | High beta, growth-driven |
| Healthcare | XLV | Demographics, drug pipelines, defensive earnings | Low-mid beta, defensive |
| Financials | XLF | Interest rates, credit cycle, yield curve | Mid beta, rate-sensitive |
| Energy | XLE | Oil/gas prices, supply constraints, geopolitics | High beta, commodity-linked |
| Consumer Staples | XLP | Steady demand, inflation pass-through | Low beta, defensive |
| Consumer Discretionary | XLY | Consumer spending, employment, confidence | High beta, cyclical |
| Industrials | XLI | Capex cycles, infrastructure, global trade | Mid beta, cyclical |
| Utilities | XLU | Interest rates (inverse), regulation, weather | Low beta, bond proxy |
| Real Estate | XLRE | Interest rates, housing demand, cap rates | Mid beta, rate-sensitive |

### Market Regime Proxies

These three ETFs tell you what the market is doing at a glance:

- **SPY** (S&P 500): Large-cap benchmark. If SPY is above its 200-day MA, the primary trend is up.
- **QQQ** (Nasdaq 100): Growth/tech sentiment. QQQ leading SPY = risk-on. QQQ lagging = rotation to value.
- **IWM** (Russell 2000): Small-cap health. IWM leading = broad participation (healthy). IWM lagging = narrow market (fragile).

**Quick regime check**: All three above 200-day MA = bullish. All three below = bearish.
Mixed signals = transitional (reduce size, hedge).

---

## Scanner Patterns

ThetaRoom's Scanner agent runs daily screens looking for actionable setups.
Here is what it looks for and why each pattern matters.

### Volume Breakouts

A stock breaks above resistance on volume 2x or more its 20-day average.
Volume confirms conviction. Without volume, breakouts frequently fail.

```
Criteria:
- Price closes above 20-day high
- Volume >= 2.0 * SMA(volume, 20)
- Relative volume rank in top 10% of sector
```

### New Highs

Stocks making 52-week or all-time highs tend to continue higher. This is
counterintuitive -- most beginners think "it's too high." But new highs
mean no overhead supply (no trapped buyers waiting to sell).

### Relative Strength

Compare a stock's performance to its sector and to SPY over 1-month and
3-month windows. Stocks that outperform during pullbacks are showing
institutional accumulation. This is the single most predictive scan factor.

```
relative_strength = stock_return_3m / spy_return_3m
# RS > 1.5 = strong outperformance, worth investigating
```

---

## Fundamental Screening

Scans find candidates. Fundamentals filter out the garbage.

| Metric | What It Tells You | Green Flag | Red Flag |
|--------|-------------------|------------|----------|
| **P/E** (Price/Earnings) | How much you pay per dollar of earnings | Below sector median | >3x sector median with no growth |
| **P/S** (Price/Sales) | Valuation relative to revenue | <5 for growth, <2 for value | >20 without hypergrowth |
| **PEG** (P/E / Growth) | P/E adjusted for growth rate | 0.5-1.5 | >3 (paying too much for growth) |
| **Revenue Growth** | Top-line momentum | Accelerating QoQ | Decelerating for 2+ quarters |
| **Earnings Surprise** | Actual vs. analyst estimates | Beat by >5% for 2+ quarters | Miss by >5% |

### Why PEG Matters More Than P/E

A stock with P/E of 40 growing earnings at 50% (PEG = 0.8) is cheaper than
a stock with P/E of 15 growing at 5% (PEG = 3.0). P/E without growth context
is misleading. Always check PEG for growth stocks.

---

## Kelly Criterion Allocation

The Kelly Criterion calculates the mathematically optimal bet size based on
your edge. ThetaRoom's Portfolio agent uses it to size positions.

### The Formula

```python
kelly_fraction = (win_prob * avg_win - (1 - win_prob) * avg_loss) / avg_win
position_size = kelly_fraction * 0.5  # Half Kelly for safety
```

### Why Half Kelly

Full Kelly maximizes long-term growth rate but produces stomach-churning
drawdowns (30-50% is normal). Half Kelly sacrifices roughly 25% of the
growth rate but cuts drawdown risk by about half. In practice, your
estimates of win probability and average win/loss are imperfect, which
makes Full Kelly dangerously aggressive.

### Example

```
Win rate: 60%
Average win: $500
Average loss: $300

kelly_fraction = (0.60 * 500 - 0.40 * 300) / 500
             = (300 - 120) / 500
             = 0.36 (36%)

half_kelly = 0.36 * 0.5 = 0.18 (18% of portfolio per trade)
```

Even Half Kelly can be aggressive. Most practitioners cap at 5-10% per
position and use Kelly as a relative sizing tool (larger Kelly = larger
relative allocation, not necessarily 18% of portfolio).

---

## Earnings Plays

Earnings announcements create the highest single-day volatility events for
individual stocks. Understanding the mechanics prevents costly mistakes.

### Expected Move Calculation

Options markets price in an expected move around earnings. Calculate it from
the at-the-money straddle price for the nearest expiration after earnings.

```
expected_move = ATM_straddle_price * 0.85
# The 0.85 factor accounts for time value in the straddle
```

### Pre-Earnings: IV Crush Setup

Implied volatility rises into earnings as uncertainty increases. If you buy
options before earnings, you are paying inflated prices. Selling premium
before earnings captures this IV crush -- but you must use defined-risk
strategies (spreads, iron condors) because the underlying can gap far
beyond the expected move.

### Post-Earnings: Directional Move

After earnings, IV collapses. The stock either gaps and runs, or gaps and
reverses. Wait for the first 30-minute range to establish, then trade the
breakout direction with reduced position size (earnings gaps are unreliable).

---

## Market Cap Tiers

Different market cap tiers have fundamentally different risk/reward profiles.

| Tier | Market Cap | Characteristics |
|------|-----------|-----------------|
| **Mega Cap** | >$200B | Liquid, institutional, lower volatility, benchmark weight |
| **Large Cap** | $10B-$200B | Good liquidity, analyst coverage, moderate volatility |
| **Mid Cap** | $2B-$10B | Sweet spot for growth, less coverage = more opportunity |
| **Small Cap** | $300M-$2B | Higher volatility, less liquidity, wider spreads |
| **Micro Cap** | <$300M | Illiquid, easy to manipulate, avoid for options trading |

**Rule of thumb**: Trade options only on stocks with average daily volume
above 500K shares and option open interest above 1,000 contracts per strike.
Below these thresholds, bid-ask spreads eat your edge.

---

## Data Sources

| Source | What It Provides | Cost | Best For |
|--------|-----------------|------|----------|
| **yfinance** | Historical OHLCV, fundamentals, options chains | Free | Backtesting, screening, prototyping |
| **Polygon.io** | Real-time and historical data, websockets | Free tier + paid | Production data feeds |
| **Alpaca** | Brokerage API, real-time data, paper trading | Free (with account) | Live trading execution, paper testing |

### yfinance Gotchas

- Rate limited (unofficial API). Add 0.5s delays between requests.
- Options chain data can be stale by 15+ minutes.
- Adjusted close handles splits/dividends but can cause confusion in backtests.
- Use `Ticker.fast_info` for quick lookups instead of `Ticker.info` (much faster).

### Polygon.io Tips

- Free tier: 5 API calls/minute, delayed data.
- Paid tier: unlimited calls, real-time data.
- Websocket streams are more efficient than polling for live signals.

### Alpaca Tips

- Paper trading environment mirrors production exactly -- always test there first.
- Market orders on options are not supported (and you should never market-order options anyway).
- Use their built-in bracket orders for automatic stop-loss and take-profit.
