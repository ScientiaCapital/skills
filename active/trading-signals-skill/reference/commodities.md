# Commodities — Gold, Silver, Oil

Commodity markets move on fundamentals that equities traders often ignore: physical supply
constraints, geopolitics, currency dynamics, and seasonal demand cycles. This reference
covers the three most-traded commodities and the signals that drive them.

Pattern for every indicator: **Signal → Why → Context → Action**

---

## Gold (XAU/USD)

### Safe Haven Dynamics

Gold rallies when confidence in paper assets erodes. Four primary catalysts:

| Catalyst | Why It Matters | Signal to Watch |
|----------|---------------|-----------------|
| Negative real rates | Holding cash costs money in real terms; gold has zero yield but no decay | 10Y TIPS yield < 0% |
| USD weakness | Gold is priced in dollars; weaker dollar = cheaper for foreign buyers | DXY falling below 100 |
| Geopolitical risk | Flight to safety when outcomes are unquantifiable | VIX spike + bond rally simultaneously |
| Central bank buying | Structural demand from nations diversifying away from USD reserves | PBOC, RBI monthly reserve reports |

**Why this matters**: Gold is not an inflation hedge in the simple sense. It is a *real rate*
hedge. Gold can fall during high inflation if the Fed hikes faster than inflation (positive
real rates). The key variable is always: what is the real yield on safe alternatives?

### Real Rates — The Master Signal

```
Gold Direction ≈ Inverse of Real Yields (10Y TIPS)

Real Yield = Nominal 10Y Treasury Yield - 10Y Breakeven Inflation Rate
```

- **Real yield falling / negative** → Bullish gold. Opportunity cost of holding gold drops to zero.
- **Real yield rising / positive** → Bearish gold. Treasuries offer real return without risk.

**Context**: This relationship has held with ~0.85 inverse correlation since 2006. It temporarily breaks during liquidity crises (March 2020) when everything sells for cash.

**Action**: Track the US 10Y TIPS yield on FRED (series: DFII10). When real yields cross from positive to negative, that is a major buy signal for gold. The reverse is a sell signal.

### Dollar Correlation (DXY)

**Signal**: Gold moves inversely to the US Dollar Index (DXY) approximately 70-80% of the time.

**Why**: Two reinforcing mechanisms:
1. **Mechanical**: Gold is priced in USD. When USD weakens, gold's price rises in dollar terms even if demand is flat.
2. **Fundamental**: The conditions that weaken the dollar (dovish Fed, fiscal deficits, risk-on sentiment abroad) are the same conditions that favor gold.

**Context**: The correlation breaks during panic events. In a true crisis, both gold AND the dollar can rally simultaneously as investors flee to *any* safe haven. When you see gold and DXY rising together, that is a fear signal — not a normal market.

**Action**: If gold is rising but DXY is also rising, the move is driven by pure fear, not macro fundamentals. These moves tend to reverse sharply once panic subsides. If gold rises while DXY falls, the move has fundamental support and is more sustainable.

### COT (Commitment of Traders) Reports

The CFTC publishes weekly positioning data every Friday (as of Tuesday close). Three groups:

| Group | Who They Are | What Their Position Means |
|-------|-------------|--------------------------|
| **Commercials** | Miners, jewelers, central banks | Hedgers. Extreme short = they expect prices are high (bearish signal) |
| **Large Speculators** | Hedge funds, CTAs | Trend followers. Extreme long = crowded trade, reversal risk |
| **Small Speculators** | Retail traders | Historically wrong at extremes. Fade their extremes. |

**Why this matters**: COT data shows you who is actually putting money behind their view. Commercials are considered "smart money" because they have real business exposure.

**Action**:
- **Commercials net short at historical extremes** → Gold likely near a top
- **Large speculators net long at extremes** → Crowded long trade, pullback likely
- **Commercials net long (rare)** → Very bullish; smart money is accumulating
- Use z-scores (standard deviations from mean) rather than raw numbers to normalize

### Seasonal Patterns

| Period | Tendency | Driver |
|--------|----------|--------|
| Jan-Feb | Strong | New year portfolio allocation, Chinese New Year buying |
| Jul-Aug | Strong | Indian wedding season buying begins (jewelers stock up) |
| Sep | Strong | Indian festival season (Diwali gold gifting) |
| Mar-Jun | Weak | Post-Q1 rebalancing, lower physical demand |

**Why this matters**: ~50% of global physical gold demand comes from India and China. Cultural buying patterns create predictable seasonal demand.

**Context**: Seasonals are a tailwind/headwind, not a standalone signal. A seasonal bullish period during a macro bearish environment (rising real rates) will still lose.

### Gold Miners vs Physical Gold (GDX vs GLD)

**Signal**: When gold miners (GDX) outperform physical gold (GLD), it confirms bullish momentum. When miners lag despite gold rising, it warns of a potential reversal.

**Why**: Miners are leveraged to the gold price because their costs are semi-fixed. If gold rises $100/oz and mining cost is $1,200/oz, a miner's profit margin expands dramatically. Miners *should* outperform gold in a healthy rally.

**Action**:
- **GDX/GLD ratio rising** → Smart money confirming the gold move. Trend likely continues.
- **Gold rising but GDX/GLD ratio falling** → Divergence warning. Equity investors are
  skeptical of the gold move. Consider tightening stops.
- **GDX leading gold higher** → Strongest bullish signal. Miners front-run gold moves.

### Gold-Specific Technical Levels

- Gold respects round numbers ($1,800, $1,900, $2,000) as psychological support/resistance
- 200-week moving average has been reliable long-term support in bull markets
- Gold trends persistently — breakouts above multi-year highs tend to run far

---

## Silver (XAG/USD)

### Gold/Silver Ratio

```
Gold/Silver Ratio = Gold Price / Silver Price

Historical range: ~60-90 (post-2000 era)
Long-term average: ~70
```

**Signal**: The ratio tells you whether silver is cheap or expensive relative to gold.

**Why**: Silver and gold share monetary demand, but silver also has industrial demand. When
the ratio is extreme, it tends to mean-revert because:
- At high ratios (>80): Silver is historically cheap. Industrial + monetary demand eventually
  catches up.
- At low ratios (<60): Silver has overshot. Usually happens at the blow-off top of a
  precious metals rally.

**Context**: The ratio hit 125 in March 2020 (extreme fear, pure flight to gold). It reverted
to ~65 within 18 months. In 2011 it hit ~32 at the silver blow-off top before reverting to 80+.

**Action**:
- **Ratio > 80** → Favor silver over gold for new long positions. Mean reversion trade.
- **Ratio < 60** → Silver is likely overextended. Take profits on silver, rotate to gold.
- **Ratio dropping rapidly** → Late-stage precious metals rally. Silver outperformance at the
  end of a move is often a sign of speculative excess.

### Industrial vs Monetary Demand

Silver's dual nature makes it more complex than gold:

| Demand Type | % of Total | Price Driver |
|-------------|-----------|--------------|
| Industrial (solar, electronics, medical) | ~55% | Global manufacturing PMI, solar installations |
| Investment/monetary | ~25% | Same drivers as gold (real rates, USD, fear) |
| Jewelry/silverware | ~20% | Consumer spending, cultural demand |

**Why this matters**: Silver can rally on *either* industrial strength *or* monetary demand.
But it can also get caught in a tug-of-war where recession fears (bad for industrial) fight
against rate cuts (good for monetary). Understanding which demand driver is dominant tells
you which macro data matters most right now.

**Action**: During a global growth expansion, silver benefits from both industrial AND monetary
tailwinds (if rates are low). This is when silver dramatically outperforms gold. During
stagflation, gold is the cleaner trade because it lacks the industrial drag.

### Silver's Higher Beta

Silver moves 1.5-2x the percentage of gold in both directions. A 5% gold rally often
produces a 7-10% silver rally — and vice versa on the downside.

**Why**: Silver's market is ~1/15th the size of gold's. Less liquidity means the same
dollar flows produce larger price movements. Silver also attracts more retail speculation,
amplifying momentum.

**Action**: Use silver for tactical positions when you have a high-conviction directional
view on precious metals. Use gold for core/strategic positions. Never size silver positions
the same as gold — reduce size to account for higher volatility.

### Silver-Specific Technicals

- Silver is prone to violent short squeezes due to concentrated short positions
- Watch COMEX silver inventory levels for physical supply stress signals
- Silver breaks out later than gold but moves faster — wait for gold to confirm direction,
  then enter silver for the amplified move

---

## Crude Oil (WTI / Brent)

### EIA & API Inventory Reports

| Report | Source | Release | Market Impact |
|--------|--------|---------|---------------|
| API (American Petroleum Institute) | Private survey | Tuesday 4:30 PM ET | Moderate — preview of EIA |
| EIA (Energy Information Administration) | Government data | Wednesday 10:30 AM ET | High — official numbers |

**Signal**: Weekly changes in crude oil inventories.

**Why**: Oil prices are set by supply/demand balance. Inventories are the most direct measure. Draws (inventory declining) mean demand exceeds supply. Builds (rising) mean supply exceeds demand.

**How to read the report**:
- **Crude inventories**: The headline number. Draw = bullish, build = bearish.
- **Gasoline inventories**: Demand proxy for consumer driving. Unexpected draws = strong demand.
- **Distillate inventories**: Diesel/heating oil. Reflects industrial activity and seasonal heating.
- **Cushing, OK stocks**: WTI delivery point. Low Cushing stocks = tighter physical market,
  supports backwardation.
- **Refinery utilization**: How much capacity is running. High util + draws = genuinely tight market.

**Action**: The *surprise* vs consensus matters more than the raw number. A 2M barrel draw
when consensus expected a 3M draw is actually bearish (less bullish than expected).

### OPEC Decisions

**Signal**: OPEC+ production quotas and compliance rates.

**Why**: OPEC controls ~35-40% of global oil production. Their supply decisions directly
shift the supply/demand balance. A 1 million barrel/day cut removes ~1% of global supply,
which is enough to swing prices 10-15%.

**Key factors to watch**:
- **Announced cuts vs actual compliance**: OPEC members historically cheat on quotas. A
  2M bpd cut with 70% compliance is really a 1.4M bpd cut.
- **Saudi Arabia's unilateral actions**: Saudi often carries the burden of cuts. Watch their
  production separately from the group.
- **Spare capacity**: How much OPEC *could* produce if they wanted to. Low spare capacity
  means supply shocks have outsized impact.

**Action**: OPEC meetings are scheduled events. Position *before* the decision based on
leaked signals and Saudi statements. After the announcement, trade the gap between headline
and compliance expectations.

### Contango vs Backwardation

```
Contango:      Front month < Back months  (futures curve slopes UP)
Backwardation: Front month > Back months  (futures curve slopes DOWN)
```

**Signal**: The shape of the futures curve reveals the market's view on supply/demand.

**Why**:
- **Contango** (normal state): Means supply is adequate. Storage costs and financing create
  natural upward slope. Traders can buy spot, store, and sell futures for guaranteed profit.
  This caps upside because storage arbitrage adds supply.
- **Backwardation** (tight market): Means buyers need oil *now* and will pay a premium for
  immediate delivery. Storage economics break down — no one stores oil when spot is higher
  than futures. This is a structural bullish signal.

**Action**:
- **Deep backwardation** → Market is physically tight. Bullish for spot prices. But also
  means oil ETFs (USO) *benefit* from positive roll yield.
- **Deep contango** → Oversupply. Bearish. Oil ETFs suffer from negative roll yield
  (selling cheap front month, buying expensive next month).
- **Contango flattening toward backwardation** → Supply tightening. Early bullish signal.

### Crack Spreads

```
3-2-1 Crack Spread = (2 × Gasoline Price + 1 × Heating Oil Price) - (3 × Crude Oil Price)
                      All in $/barrel
```

**Signal**: Refining profit margins.

**Why**: Crack spreads measure the value refiners add by converting crude into products.
High crack spreads mean product demand is strong relative to crude supply — refiners are
profitable and will buy more crude (bullish crude). Low crack spreads mean weak demand
for refined products (bearish crude eventually).

**Action**:
- **Crack spreads widening** → Product demand strong. Refiners will increase runs, supporting
  crude demand. Bullish crude.
- **Crack spreads collapsing** → Product demand weakening. Refiners will cut runs, reducing
  crude demand. Bearish crude with a lag.
- **Gasoline crack strong, heating oil crack weak** (or vice versa) → Seasonal demand shift.
  Not inherently bullish or bearish for crude.

### Oil Seasonal Patterns

| Period | Tendency | Driver |
|--------|----------|--------|
| Feb-Jun | Bullish | Refinery maintenance ends, summer driving season build |
| Jul-Aug | Mixed | Peak driving demand but well-anticipated |
| Sep-Oct | Bearish | Shoulder season, refinery turnaround |
| Nov-Dec | Mixed | Winter heating demand vs year-end inventory management |

**Context**: Oil seasonals have weakened in recent years as shale production responds faster
to price signals, smoothing traditional seasonal swings.

### Geopolitical Risk Premium

**Signal**: Oil prices include a premium for supply disruption risk from geopolitically
unstable producing regions.

**Key chokepoints**:
- **Strait of Hormuz**: ~20% of global oil passes through. Iran tensions = premium.
- **Russian supply**: Sanctions, pipeline disruptions, rerouting to Asian buyers.
- **Libyan production**: Frequent disruptions due to political instability.
- **Nigerian output**: Militancy, pipeline vandalism, export terminal attacks.

**Why**: Unlike most risk premiums, geopolitical risk in oil is asymmetric. Disruptions
remove real supply from the market instantly. The premium exists because the downside of
being unhedged during a disruption is far worse than the cost of the premium.

**Action**: Geopolitical premium tends to be priced in gradually and released suddenly.
If a feared disruption doesn't materialize, the premium evaporates fast. Fade geopolitical
spikes only when the actual supply disruption is confirmed to be minimal.

### WTI vs Brent Spread

```
Brent - WTI Spread (normally Brent trades at a premium of $2-6/barrel)
```

**Why the spread exists**:
- **Quality**: WTI is lighter and sweeter (lower sulfur). In isolation, WTI should trade
  at a premium. But logistics override quality.
- **Logistics**: WTI delivers at Cushing, OK (landlocked). Brent is seaborne (global access).
  When Cushing fills up, WTI collapses relative to Brent.
- **Global benchmark**: Brent prices ~75% of global crude. It reflects global supply/demand,
  while WTI is more influenced by US-specific factors (shale production, pipeline capacity).

**Action**:
- **Spread widening (Brent >> WTI)** → US oversupply (Cushing filling) or global tightness.
  Bullish Brent, neutral WTI.
- **Spread narrowing or WTI premium** → US exports clearing Cushing, or US-specific tightness.
- **Spread goes negative (WTI > Brent)** → Rare. Usually means US export capacity is
  constrained and domestic supply is tight.

---

## Cross-Commodity Signals

### Gold/Oil Ratio

```
Gold/Oil Ratio = Gold Price ($/oz) / WTI Price ($/bbl)

Normal range: 15-25 barrels of oil per ounce of gold
```

**Signal**: Relative value between the two most important commodities.

**Why**: Both gold and oil are priced in dollars and respond to inflation, but through
different channels. Gold responds to monetary conditions; oil responds to real economic
activity. The ratio reveals which force is dominant.

**Action**:
- **Ratio > 25** → Oil is cheap relative to gold. Either growth is weak (bearish risk assets)
  or oil-specific oversupply. If growth indicators stabilize, buy oil / sell gold.
- **Ratio < 15** → Oil is expensive relative to gold. Often precedes recession as energy
  costs crimp growth. Rotate to gold.

### Commodity Super-Cycles

Long-term (10-20 year) bull and bear cycles driven by structural supply/demand imbalances.

**Why they form**: Commodity production has long lead times (5-10 years for a new mine or
oil field). When prices are low, investment dries up. When demand eventually recovers,
supply cannot respond quickly. Prices spike, triggering investment, which takes years to
produce new supply, eventually creating oversupply. Repeat.

**Where to look**: Track global capex spending in mining and energy. Multi-year declines in
capex during steady demand growth set up the next bull cycle. Bloomberg Commodity Index
(BCOM) relative to S&P 500 at multi-decade lows has historically preceded commodity
outperformance.

### Inflation Hedge Basket

No single commodity perfectly hedges inflation. A balanced approach:
- **Gold** → Monetary inflation hedge (real rate driven)
- **Oil** → Cost-push inflation hedge (energy input costs)
- **Silver** → Hybrid: monetary + industrial inflation
- **Broad commodities (DJP, PDBC)** → Diversified exposure to commodity-driven inflation

**Action**: If you are hedging inflation, allocate across the basket rather than
concentrating in gold. Different inflation regimes favor different commodities.

---

## Data Sources

| Source | URL | Data Available | Update Frequency |
|--------|-----|----------------|------------------|
| FRED | fred.stlouisfed.org | Real rates (DFII10), DXY, breakevens | Daily |
| EIA | eia.gov | Oil inventories, production, demand | Weekly (Wed) |
| CFTC | cftc.gov/MarketReports | COT reports (futures positioning) | Weekly (Fri) |
| World Gold Council | gold.org | Gold demand/supply, central bank flows | Quarterly |

### Key ETFs for Tracking

| ETF | Tracks | Notes |
|-----|--------|-------|
| GLD | Gold spot price | Largest gold ETF, tight tracking |
| IAU | Gold spot price | Lower expense ratio than GLD |
| SLV | Silver spot price | Standard silver exposure |
| GDX | Gold miners (senior) | Leveraged gold exposure via equities |
| GDXJ | Gold miners (junior) | Higher beta, higher risk |
| USO | WTI front-month | Suffers from contango roll drag |
| BNO | Brent front-month | Global benchmark exposure |
| DBO | WTI (optimized roll) | Better roll strategy than USO |

### Essential FRED Series

| Series ID | Description | Use Case |
|-----------|-------------|----------|
| DFII10 | 10-Year TIPS yield | Master gold signal |
| DTWEXBGS | Trade-weighted USD (broad) | Dollar strength |
| T10YIE | 10-Year breakeven inflation | Inflation expectations |
| DCOILWTICO | WTI spot price | Oil benchmark |
| GOLDAMGBD228NLBM | London gold fixing | Gold benchmark |
