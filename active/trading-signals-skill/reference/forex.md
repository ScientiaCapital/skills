# Forex — Currency Markets

Foreign exchange is the largest financial market on Earth, trading roughly
$7.5 trillion per day. Unlike equities, forex has no central exchange — it
runs 24 hours through an interbank network of dealers, banks, and electronic
platforms. Understanding why currencies move is essential for any
cross-asset trading system.

---

## How Forex Works

### Currency Pairs

Every forex quote is a ratio of two currencies:

- **Base currency** / **Quote currency**
- EUR/USD = 1.0850 means 1 euro costs 1.0850 US dollars
- Buying EUR/USD = buying euros, selling dollars
- Selling EUR/USD = selling euros, buying dollars

### Major Pairs (most liquid, tightest spreads)

| Pair    | Nickname   | Notes                          |
|---------|------------|--------------------------------|
| EUR/USD | Fiber      | Most traded pair globally      |
| GBP/USD | Cable      | High volatility, wide ranges   |
| USD/JPY | Gopher     | Sensitive to rate differentials |
| USD/CHF | Swissie    | Safe-haven dynamics            |
| AUD/USD | Aussie     | Commodity/China proxy          |
| USD/CAD | Loonie     | Oil-correlated                 |
| NZD/USD | Kiwi       | Dairy/agriculture exposure     |

### Cross Pairs (no USD leg)

- **EUR/GBP** — Brexit-sensitive, tight range
- **EUR/JPY** — Risk sentiment barometer
- **GBP/JPY** — "The Dragon," extremely volatile

Cross pairs matter because they reveal relative strength between
non-dollar economies. A rising EUR/GBP says the eurozone is outperforming
the UK, regardless of what the dollar is doing.

### Exotic Pairs

- **USD/MXN**, **USD/ZAR**, **USD/TRY**
- Wider spreads, lower liquidity, higher volatility
- Driven heavily by local politics, capital controls, and EM risk appetite

### Pips, Lots, and Leverage

- **Pip**: smallest standard price increment — 0.0001 for most pairs,
  0.01 for JPY pairs
- **Standard lot**: 100,000 units of base currency
- **Mini lot**: 10,000 units; **Micro lot**: 1,000 units
- **Leverage**: brokers offer 20:1 to 500:1 — this is why forex attracts
  speculation and why risk management is non-negotiable

A 1-pip move on a standard lot of EUR/USD = ~$10 profit or loss.
At 100:1 leverage, a 1% adverse move wipes out your margin.

---

## Fundamental Drivers

### Interest Rate Differentials

This is the single most important driver of currency trends.

**Why it works**: Capital flows toward higher real returns. If the Fed
offers 5% while the ECB offers 3%, global investors buy dollars to park
money in US treasuries. That buying pressure strengthens the dollar.

Key principles:
- **Actual rate levels** set the baseline
- **Rate expectations** move currencies before the decision happens
- **Forward guidance** (what the central bank signals about future rates)
  often matters more than today's rate
- Markets price in expected rate paths — surprises cause the sharpest moves

The 2-year government bond yield differential between two countries is
one of the best leading indicators for their currency pair.

### Carry Trade

The carry trade is the direct exploitation of interest rate differentials.

**How it works**:
1. Borrow in a low-interest-rate currency (e.g., JPY at 0.1%)
2. Convert to a high-interest-rate currency (e.g., AUD at 4.5%)
3. Invest in that country's bonds or deposits
4. Pocket the interest differential minus transaction costs

**Popular carry pairs** (historically):
- AUD/JPY, NZD/JPY — high-yielding commodity currencies vs. zero-rate yen
- USD/JPY — when US rates are elevated
- MXN/JPY — higher yield but higher risk

**Why carry trades blow up**: In a risk-off panic, investors unwind
simultaneously. Everyone sells the high-yielder and buys back the
funding currency (usually JPY or CHF). This creates violent, correlated
moves. The yen can surge 5-10% in days during a carry unwind.

The carry trade works in calm, trending environments. It fails
spectacularly in volatility spikes — making it a textbook example of
"picking up pennies in front of a steamroller" when risk is mispriced.

### Purchasing Power Parity (PPP)

PPP says exchange rates should eventually adjust so that identical goods
cost the same across countries (after currency conversion).

**The Big Mac Index** is the simplified version: if a Big Mac costs $5.50
in the US and EUR 4.50 in Germany, PPP implies EUR/USD should be ~1.22.
If the actual rate is 1.08, the euro is "undervalued" by PPP.

**Why PPP matters for traders**:
- It provides a long-term fair value anchor (5-10 year horizon)
- Currencies that deviate far from PPP tend to mean-revert eventually
- PPP gives direction, never timing — a currency can stay "overvalued"
  for years

PPP is useful as a sanity check: if your model says buy a currency
that's already 30% above PPP, you're fighting gravity.

---

## Central Bank Policy

Eight central banks dominate forex:

| Bank | Currency | Key Feature |
|------|----------|-------------|
| **Fed** (Federal Reserve) | USD | Global reserve currency issuer |
| **ECB** (European Central Bank) | EUR | Manages 20 member states |
| **BOJ** (Bank of Japan) | JPY | Decades of ultra-loose policy |
| **BOE** (Bank of England) | GBP | Often follows Fed direction |
| **RBA** (Reserve Bank of Australia) | AUD | Commodity cycle sensitive |
| **RBNZ** (Reserve Bank of New Zealand) | NZD | Small, open economy |
| **BOC** (Bank of Canada) | CAD | Oil-linked policy decisions |
| **SNB** (Swiss National Bank) | CHF | Intervenes to weaken CHF |

### What to Watch

- **Rate decisions**: the headline number (25bp hike, hold, cut)
- **Dot plots** (Fed): individual member rate projections
- **Press conferences**: tone matters — hawkish language strengthens
  the currency, dovish weakens it
- **Minutes/accounts**: released weeks later, can shift expectations
- **Dissenting votes**: signal future policy shifts

**Hawkish** = favoring higher rates (currency bullish)
**Dovish** = favoring lower rates or easing (currency bearish)

The market has usually priced in the expected decision. The move comes
from the surprise — the gap between what the market expected and what
happened. A 25bp hike when 50bp was priced in is effectively dovish.

---

## Economic Indicators

| Indicator | Impact | Frequency | Why It Moves Currencies |
|-----------|--------|-----------|------------------------|
| **NFP** (Non-Farm Payrolls) | High | Monthly (1st Friday) | Jobs = consumer spending = growth = rate expectations |
| **CPI / PCE** (Inflation) | High | Monthly | Inflation above target → higher rates → stronger currency |
| **GDP** | Medium | Quarterly | Growth confirms or denies rate path |
| **PMI** (Mfg/Services) | Medium | Monthly | Leading indicator — drops below 50 signal contraction |
| **Retail Sales** | Medium | Monthly | Consumer strength feeds GDP forecasts |
| **Trade Balance** | Low-Med | Monthly | Persistent deficits create structural selling pressure |

**NFP trading tip**: The reaction in the first 30 seconds is often wrong.
The initial spike gets faded as traders digest revisions, average hourly
earnings, and participation rate. Wait for the dust to settle.

**CPI nuance**: Core CPI (ex-food and energy) matters more than headline.
Central banks target core because food and energy are volatile and outside
monetary policy control.

---

## COT Positioning (CFTC)

The Commitment of Traders report, released every Friday (data from
Tuesday), breaks down futures positioning into three groups:

| Group | Who They Are | What Their Positioning Means |
|-------|-------------|----------------------------|
| **Commercials** (hedgers) | Banks, multinationals | Hedging real exposure — often contrarian signal |
| **Large Speculators** | Hedge funds, CTAs | Trend followers — extreme positions = crowded trade |
| **Small Speculators** | Retail traders | Historically wrong at extremes |

### How to Use COT Data

- **Extreme net-long** in large speculators = crowded bullish trade,
  vulnerable to reversal
- **Extreme net-short** = crowded bearish, squeeze risk
- Compare current positioning to 1-year and 3-year ranges
- COT is a timing tool for mean reversion, not a trend signal

When large speculator positioning hits a multi-year extreme, it means
the "easy money" trade is already done. Any catalyst that forces
position unwinding creates outsized moves because everyone exits at once.

---

## Technical Analysis in Forex

Forex is one of the most technically-driven markets because:
- Massive liquidity means patterns are harder to manipulate
- Institutional algos target the same levels, creating self-fulfilling zones
- No earnings surprises or corporate events to create random gaps

### Fibonacci Levels

Fibonacci retracements (38.2%, 50%, 61.8%) work particularly well in
forex because institutional algorithms are programmed to buy and sell at
these levels. When enough participants target the same zone, it becomes a
genuine support/resistance area.

### Round Number Psychology

Psychological levels like 1.0000 (EUR/USD parity), 1.1000, or 150.00
(USD/JPY) act as magnets and barriers. Options dealers set strikes at
round numbers, creating gamma exposure that pins price near these levels
as expiry approaches.

### Session-Based Analysis

Forex trades across three overlapping sessions, each with distinct
character:

| Session | Hours (UTC) | Character |
|---------|-------------|-----------|
| **Asian** (Tokyo) | 00:00–09:00 | Range-bound, low volatility |
| **London** | 07:00–16:00 | Breakouts, trend initiation |
| **New York** | 12:00–21:00 | Continuation or reversal |
| **London/NY Overlap** | 12:00–16:00 | Highest volume, biggest moves |

The London session sets the tone. Roughly 43% of all forex volume flows
through London. Breakouts during the London open that align with the
fundamental trend are higher-probability setups.

---

## DXY (Dollar Index)

The DXY measures the dollar against a weighted basket of six currencies:

| Currency | Weight |
|----------|--------|
| EUR | 57.6% |
| JPY | 13.6% |
| GBP | 11.9% |
| CAD | 9.1% |
| SEK | 4.2% |
| CHF | 3.6% |

**Key observation**: The DXY is 57.6% euro. When someone says "the dollar
is strong," they often mean "the euro is weak." Always check whether
dollar strength is broad-based or driven by one component.

### DXY Cross-Asset Impact

- **Strong DXY → commodity weakness**: Commodities are priced in dollars.
  A stronger dollar means higher costs for non-US buyers, reducing demand.
- **Strong DXY → emerging market pressure**: EM countries with
  dollar-denominated debt face higher repayment costs.
- **Strong DXY → crypto headwind**: Bitcoin and crypto generally trade
  inversely to dollar strength (risk asset behavior).
- **Strong DXY → gold weakness**: Gold and the dollar compete as stores
  of value. The inverse correlation isn't perfect but is persistent.

---

## Cross-Asset Signals

Forex does not trade in isolation. Currency moves ripple through every
asset class, and vice versa.

### Dollar Strength Cascade

Strong dollar → commodity prices drop → commodity-exporting nations
(Australia, Canada, Brazil) see currency weakness → emerging market
stress rises → risk-off sentiment builds → yen and CHF strengthen
as safe havens.

This cascade is why a Fed rate hike doesn't just move USD/EUR — it can
trigger selling in copper, the Australian dollar, Brazilian equities,
and emerging market bonds simultaneously.

### Key Currency-Asset Relationships

| Signal | Interpretation |
|--------|---------------|
| **JPY strengthening** | Risk-off — carry trades unwinding, equity selloff likely |
| **AUD weakening** | China slowdown or commodity demand falling |
| **CHF strengthening** | Safe-haven demand, geopolitical stress |
| **CAD vs oil divergence** | One of them is mispriced — watch for convergence |
| **EUR/USD rising + US yields falling** | Market pricing Fed rate cuts |
| **Gold + JPY + CHF all rising** | Genuine risk-off event, not noise |

### AUD as China Proxy

Australia exports iron ore, coal, and LNG primarily to China. When
Chinese manufacturing data (PMI) disappoints, AUD sells off — often
before Chinese equity markets react. AUD/USD is a liquid, 24-hour way
to express a view on Chinese growth.

### CHF as Safe Haven

The Swiss franc strengthens during crises because Switzerland has a
current account surplus, political neutrality, and a stable banking
system. The SNB actively fights CHF strength (it hurts Swiss exporters),
which creates periodic intervention events — sudden, large moves when
the SNB steps in or steps back.

---

## Data Sources

| Source | What You Get | Access |
|--------|-------------|--------|
| **FRED** (Federal Reserve) | Interest rates, CPI, GDP, employment | Free API |
| **CFTC** | COT reports (weekly positioning) | Free download |
| **Central bank calendars** | Meeting dates, rate decisions | Each bank's website |
| **ForexFactory** | Economic calendar with consensus/actual | Free web |
| **Polygon.io** | Real-time and historical FX data | API (in your stack) |
| **BIS** (Bank for Intl Settlements) | Triennial survey, global FX stats | Free reports |

### Building a Forex Signal Pipeline

1. **Macro layer**: Track rate differentials, COT positioning, PPP deviation
2. **Event layer**: Flag central bank meetings, NFP, CPI releases
3. **Technical layer**: Session-based levels, Fibonacci zones, round numbers
4. **Cross-asset layer**: DXY trend, commodity correlations, risk sentiment
5. **Signal generation**: Combine layers — strongest signals occur when
   fundamental direction, positioning, and technicals all align

The best forex trades happen when a fundamental catalyst (rate surprise,
policy shift) hits a market that is already positioned in the wrong
direction (extreme COT), at a technically significant level. Those
three-factor alignments are rare but produce the cleanest moves.
