# VIX & Volatility — The Fear Gauge

The VIX is the single most important number for understanding market sentiment. It tells you how much fear (or complacency) is priced into the options market right now. Every volatility-based trading decision starts here.

---

## What VIX Actually Measures

VIX represents the **30-day implied volatility** of S&P 500 options. It's calculated from a weighted strip of SPX option prices across multiple strikes and two nearest-term expirations.

**Key facts:**
- VIX is **forward-looking**, not backward-looking. It reflects what the market *expects* volatility to be over the next 30 days, not what already happened.
- VIX is quoted in **annualized percentage points**. A VIX of 20 does NOT mean the market expects a 20% move this month.
- To convert to daily expected moves: divide by sqrt(252 trading days). VIX 20 implies ~1.26% daily moves in SPX (20 / 15.87).
- To convert to monthly expected moves: divide by sqrt(12). VIX 20 implies ~5.77% monthly moves.
- VIX is derived from *option prices*, which means it reflects the collective positioning of every hedger, speculator, and market maker in the SPX options pit.

**Why this matters for trading:** VIX tells you the *cost* of protection. When VIX is high, hedging is expensive and selling premium is lucrative. When VIX is low, hedges are cheap and selling premium barely pays. Every options trade is implicitly a bet on whether realized volatility will exceed or fall short of implied volatility.

---

## VIX Levels & What They Mean

Not all VIX readings are equal. Context determines whether a level signals opportunity or danger.

| VIX Range | Label | Market Conditions | Trading Implications |
|-----------|-------|-------------------|---------------------|
| 12-15 | Complacency | Extremely calm, low hedging demand | Premium selling pays little. Watch for spike setups. Cheap to buy protection. |
| 15-20 | Normal/Calm | Typical bull market conditions | Standard premium selling range. Normal position sizing. |
| 20-25 | Elevated | Uncertainty rising, news-driven moves | Premiums getting richer. Good for selling if you have conviction on direction. |
| 25-35 | Fear | Significant selling pressure, institutional hedging | Rich premiums but dangerous. Reduce size. Only sell with wide margins. |
| 35+ | Crisis | Panic liquidation, correlated selling | ThetaRoom v2 uses `vix_crisis_threshold = 35.0` for a reason. Reduce all positions, widen stops, shift to capital preservation. |

**Historical extremes for calibration:**
- COVID crash (March 2020): VIX peaked at ~82.69
- Financial crisis (October 2008): VIX peaked at ~79.13
- Volmageddon (February 2018): VIX spiked from 13 to 50 in one day
- Long-term median: roughly 17-19 depending on the measurement window

**Why this matters:** The level itself isn't the whole story — the *direction* and *speed* of change matter more. VIX moving from 15 to 22 over a week is different from VIX jumping from 15 to 22 overnight. Sudden spikes signal acute fear. Gradual rises signal building uncertainty.

---

## VIX Term Structure

The VIX spot index is just one point on a curve. VIX futures trade across multiple expirations, and the *shape* of that curve is more informative than the spot level alone.

### Contango (Normal State)

Near-term VIX futures trade **below** longer-term futures. The curve slopes upward.

- This is the default state roughly 80% of the time.
- It means: the market expects the near-term to be calmer than the future. No immediate panic.
- **Trading implication:** Short volatility strategies benefit from the "roll yield" as near-term futures decay toward spot. Products like VXX and UVXY bleed value in contango because they constantly roll into more expensive contracts.

### Backwardation (Fear State)

Near-term VIX futures trade **above** longer-term futures. The curve is inverted.

- This signals acute, right-now stress. The market is pricing in more chaos today than tomorrow.
- It's relatively rare and usually short-lived (days to weeks, not months).
- **Trading implication:** Short volatility positions get crushed. Long volatility positions finally pay off. VIX ETPs like UVXY can rally explosively because the roll yield reverses — they're rolling into *cheaper* contracts.

### Steepness Signals

The *degree* of contango or backwardation tells you more than just the direction:

| Curve Shape | Signal | What to Do |
|-------------|--------|------------|
| Steep contango | Deep complacency, potential for sharp reversal | Consider buying cheap downside protection |
| Mild contango | Normal, nothing unusual | Business as usual |
| Flat | Transitioning — market unsure | Reduce position size, watch closely |
| Mild backwardation | Fear present but contained | Start watching for mean-reversion setups |
| Steep backwardation | Full panic | Do NOT short vol. Wait for normalization. |

**Why this matters:** Term structure is the single best predictor of whether VIX is likely to rise or fall from here. Steep contango + low VIX = powder keg. Backwardation + high VIX = eventual snapback (but don't front-run it).

---

## IV Rank & IV Percentile

Raw implied volatility numbers are meaningless without context. IV Rank and IV Percentile tell you whether current IV is *relatively* high or low compared to the recent past.

### IV Rank (IVR)

**Formula:** (Current IV - 52-week Low) / (52-week High - 52-week Low)

- Ranges from 0 to 100 (can exceed 100 if IV breaks above the prior 52-week high).
- Tells you *where* current IV sits within its annual range.
- From ThetaRoom v2 config: `iv_rank_lookback_days = 252`, `min_iv_rank_entry = 20.0`.
- **Weakness:** Sensitive to outliers. One massive spike 11 months ago compresses all subsequent readings.

### IV Percentile (IVP)

**Formula:** (Number of days IV was below current level) / (Total trading days in lookback)

- Also ranges from 0 to 100.
- Tells you what *percentage of the time* IV was lower than today.
- More robust than IV Rank because it's not distorted by a single extreme reading.

### How to Use Them

| IVR / IVP | Premium Status | Preferred Strategies |
|-----------|---------------|---------------------|
| Below 20% | Cheap | Favor buying: long straddles, debit spreads, protective puts. Selling premium barely compensates for risk. |
| 20-50% | Fair | Neutral — either direction works depending on thesis. |
| Above 50% | Rich | Favor selling: iron condors, credit spreads, strangles. You're getting paid above-average for taking risk. |
| Above 80% | Very rich | High-probability selling setups, but beware — IV is high for a reason. Size down. |

**Why this matters:** IV Rank is the first filter before any options trade. If you're selling premium with IVR below 20, you're picking up pennies. If you're buying premium with IVR above 70, you're overpaying for protection. Let the rank guide your strategy selection, not the other way around.

---

## Regime Integration (Markov Model)

VIX levels map naturally to the 7-state Markov regime model used in the trading system. The VIX doesn't define the regime by itself, but it provides strong confirmation and override signals.

### VIX-to-Regime Mapping

| VIX Range | Likely Regimes | Rationale |
|-----------|---------------|-----------|
| < 15 | Accumulation, Bull Quiet | Low fear, institutions building positions or trend is strong and unchallenged |
| 15-25 | Bull Volatile, Distribution | Normal uncertainty or smart money beginning to distribute to retail |
| 25-35 | Bear Quiet, Bear Volatile | Sustained fear, downtrend mechanics in play |
| > 35 | Crisis override | Regardless of Markov state, crisis rules apply: cut size, widen stops, preserve capital |

### How the Override Works

The crisis mode override at VIX > 35 exists because regime models can lag during fast crashes. VIX responds in real-time to option pricing, while Markov models rely on price/volume patterns that may take days to recalibrate. In a crash:

1. VIX spikes above 35 first (sometimes within hours)
2. Markov model transitions to Bear Volatile or Crisis over 1-3 days
3. The VIX override bridges this gap — it forces defensive positioning immediately

**Practical rules:**
- If VIX > 35 but Markov says Bull Volatile: trust VIX. Go defensive.
- If VIX < 15 but Markov says Distribution: trust the Markov model. VIX is a lagging indicator of *topping* patterns.
- If both agree (VIX 30+ and Markov says Bear Volatile): high-conviction defensive positioning.

**Why this matters:** No single indicator is complete. VIX excels at detecting fear but misses distribution tops. The Markov model catches structural regime shifts but is slow during crashes. Using both in tandem covers each other's blind spots.

---

## Volatility Trading Strategies

### Selling VIX Call Spreads in Contango

**Setup:** Sell a VIX call spread (e.g., sell 18 call / buy 23 call) when term structure is in contango and VIX is in the 15-20 range.

**Why it works:** You're betting on two forces — VIX mean reversion and contango decay. Near-term VIX futures drift toward spot in contango, and VIX has a natural gravitational pull toward its long-term mean.

**Risk:** A sudden spike blows through your short strike. Always define risk with the long call. Never sell naked VIX calls.

### Buying VIX Calls as Portfolio Insurance

**Setup:** Buy OTM VIX calls (e.g., 25-30 strike) when VIX is below 15 and term structure is in steep contango.

**Why it works:** VIX calls are cheapest exactly when you need them most — during calm markets. They're the insurance policy you buy before the house fire, not during it.

**Sizing:** Portfolio insurance should cost 0.5-1.5% of portfolio value per quarter. If it costs more, VIX is too high and you're buying after the move.

### VIX Put Spreads on Normalization

**Setup:** Buy VIX put spreads after a spike, once the term structure begins returning from backwardation to contango.

**Why it works:** VIX decays are reliable — the question is timing. Waiting for term structure normalization (near-month futures dropping below next-month) gives you confirmation that the acute fear is subsiding.

### Calendar Spreads Exploiting Steep Term Structure

**Setup:** Sell the near-term VIX future, buy the next-month future when the spread between them is unusually wide (steep contango) or unusually narrow (near backwardation).

**Why it works:** Term structure spreads mean-revert. Steep contango eventually flattens. Backwardation eventually normalizes. The calendar spread profits from this normalization without needing to predict VIX direction.

See `options-strategies.md` for detailed mechanics on spreads, Greeks profiles, and optimal DTE windows.

---

## Mean Reversion

This is the single most important property of VIX: **it always mean-reverts.** Unlike stock prices, which can theoretically go to infinity, VIX is structurally bounded.

### Why VIX Must Mean-Revert

- VIX reflects implied volatility, which is priced from option premiums.
- At extremely high VIX levels, option premiums become so expensive that selling them offers extraordinary returns — attracting sellers who push premiums back down.
- At extremely low VIX levels, hedging becomes so cheap that demand increases — pushing premiums back up.
- This creates a natural equilibrium around the 15-20 range.

### The Asymmetry Problem

VIX mean-reverts, but it does so asymmetrically:

- **Spikes are fast:** VIX can double in a single day (it went from 13 to 50 during Volmageddon).
- **Decay is slow:** After a spike, VIX typically takes weeks to months to return to normal levels.
- **The elevator-escalator analogy:** VIX takes the elevator up and the escalator down.

### Practical Rules

1. **Never short VIX spikes immediately.** The spike might have further to go, and the leverage works against you explosively. Wait for confirmation.
2. **Wait for term structure normalization.** When near-term futures drop below next-month futures (contango resumes), the acute phase is over.
3. **Scale in, don't go all-in.** Even after normalization begins, VIX can re-spike on secondary shocks. Start with quarter-sized positions and add as decay continues.
4. **Respect the "VIX of VIX" (VVIX).** If VVIX is elevated, it means the *volatility of VIX itself* is high — expect whipsaws.

**Why this matters:** Mean reversion is a real edge, but only if you respect the asymmetry. Most VIX traders blow up not because their thesis was wrong, but because they were right too early. Patience and position sizing are everything.

---

## Data Sources

### Core VIX Data

| Source | What It Gives You | Notes |
|--------|------------------|-------|
| CBOE VIX Index | Real-time spot VIX | Calculated from SPX options. Not directly tradeable. |
| /VX Futures | VIX futures curve | Monthly contracts. This is what you actually trade. |
| VIX Options | Options on VIX futures | European-style, cash-settled. Priced off futures, NOT spot VIX. |

### VIX ETPs (Exchange-Traded Products)

These products provide VIX exposure without trading futures directly, but they come with structural issues you must understand.

| Product | Type | Mechanics | Key Risk |
|---------|------|-----------|----------|
| VXX | Long VIX | Holds blend of 1st and 2nd month /VX futures | Contango drag bleeds ~60-70% of value annually |
| UVXY | 1.5x Long VIX | Leveraged version of VXX | Even worse contango drag + volatility decay from leverage rebalancing |
| SVXY | 0.5x Inverse VIX | Short VIX exposure | Can lose catastrophically in VIX spikes. Was 1x inverse until Volmageddon forced the change. |

**Critical understanding: contango drag.** Long VIX ETPs (VXX, UVXY) must constantly roll their futures contracts forward. In contango (80% of the time), they sell cheap near-term contracts and buy expensive further-out contracts. This roll costs money every single day. Over time, this drag destroys the product's value regardless of where VIX goes.

- VXX is a tool for short-term hedging (days), never for buy-and-hold.
- UVXY is only for day trading VIX spikes. Holding overnight is almost always wrong.
- SVXY profits from contango drag but can gap against you violently in a spike.

### Derived Metrics

| Metric | What It Tells You | Where to Get It |
|--------|------------------|-----------------|
| VIX/VXV ratio | Term structure slope (30-day vs 90-day IV) | CBOE, calculated from VIX and VIX3M |
| VVIX | Volatility of VIX — how uncertain is the fear gauge itself | CBOE |
| Put/Call ratio | Directional sentiment confirming VIX signals | CBOE, most data providers |
| SKEW index | Tail risk pricing — high SKEW + low VIX = hidden risk | CBOE |

**Why data source matters:** Never confuse spot VIX with VIX futures with VIX ETPs. They move in the same direction but with very different magnitudes and timing. Trading VXX as if it tracks spot VIX will cost you money. Always know which instrument you're looking at and how it relates to the underlying VIX curve.
