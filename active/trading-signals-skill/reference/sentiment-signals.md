# Sentiment Signals -- Social & Market Indicators

## Why This Matters

Price moves before news, and sentiment moves before price. Most retail traders
react to sentiment after the move has happened. A systematic sentiment pipeline
lets you detect shifts early, filter noise from signal, and use crowd psychology
as an edge rather than a trap. This reference covers how SignalSiphon works,
what market sentiment indicators to track, and how sentiment integrates into
the MasterQuantAgent ensemble.

---

## The SignalSiphon Pipeline

SignalSiphon is the sentiment ingestion system. It transforms raw social media
noise into scored, trackable trading signals through five stages.

### Stage 1: Scrape

Collect posts from multiple sources on a scheduled cadence.

| Source | Subreddit / Feed | Cadence | Why This Source |
|--------|-----------------|---------|-----------------|
| Reddit | r/wallstreetbets | Every 15 min | High volume, options-heavy, meme stock early signals |
| Reddit | r/options | Every 30 min | Higher quality, strategy-focused discussion |
| Reddit | r/stocks | Every 30 min | Fundamental analysis, longer-term sentiment |
| Reddit | r/cryptocurrency | Every 15 min | Crypto sentiment, altcoin rotation signals |
| Twitter/X | Cashtag streams | Every 5 min | Fastest source, but noisiest |

### Stage 2: Filter (Quality Gates)

Raw social data is mostly noise. These filters remove the garbage before
analysis, saving LLM costs and improving signal quality.

**Noise Detection Rules:**

```
REJECT if:
- Emoji count > 5 per post (hype posts, not analysis)
- ALL CAPS ratio > 50% of text (shouting, not reasoning)
- Duplicate content (copy-paste spam across subs)
- Account age < 30 days (pump-and-dump accounts)
- Post length < 50 characters (no substance)
```

**Quality DD Detection:**

```
ELEVATE if:
- Contains thesis statement (identified by LLM)
- References specific financial data (earnings, revenue, margins)
- Includes supporting evidence (charts, SEC filings, data)
- Author has tracked accuracy > 60% over 10+ signals
```

### Stage 3: Analyze (Multi-Model Consensus)

Each post that passes filters gets scored by multiple LLMs. Using multiple
models reduces the bias of any single model.

| Model | Role | Why |
|-------|------|-----|
| **Gemini Flash** | Primary scorer | Fast, cheap, good at sentiment classification |
| **Claude** | Fallback scorer | Better nuance on complex posts, higher quality |
| **OpenRouter** | Tiebreaker / validation | Access to diverse models for consensus |

The consensus approach works because different models have different failure
modes. Gemini might miss sarcasm that Claude catches. Claude might overanalyze
a simple bullish post. Averaging across models smooths these errors.

### Stage 4: Score

Each signal gets a composite score on a -1 to +1 scale.

| Score Range | Interpretation | Trading Implication |
|-------------|---------------|---------------------|
| -1.0 to -0.7 | Strongly bearish | Potential short signal (or contrarian long at extremes) |
| -0.7 to -0.3 | Moderately bearish | Caution, reduce long exposure |
| -0.3 to +0.3 | Neutral / mixed | No sentiment edge, rely on other signals |
| +0.3 to +0.7 | Moderately bullish | Supports long bias from other signals |
| +0.7 to +1.0 | Strongly bullish | Potential long signal (or contrarian short at extremes) |

**Confidence Rating (1-10):**

Each signal also gets a confidence rating. Signals below confidence 3 are
discarded entirely. This is the most important filter -- a strongly bullish
signal with confidence 2 is just someone shouting into the void.

```
Confidence factors:
- Author track record (0-3 points)
- Supporting data quality (0-3 points)
- Multi-model agreement (0-2 points)
- Novelty (not recycled thesis) (0-2 points)
```

### Stage 5: Track Accuracy

Every signal gets a ticker and timestamp. SignalSiphon records the price at
signal time and checks it at three intervals:

```
price_after_1h   -- Was the direction right short-term?
price_after_24h  -- Did the thesis play out intraday?
price_after_7d   -- Was this a real signal or noise?
```

This creates a feedback loop. Authors whose signals are consistently accurate
get higher confidence scores. Authors who are consistently wrong get filtered
more aggressively. Over time, the system self-calibrates.

---

## Market Sentiment Indicators

Social sentiment is one input. Institutional and options-market sentiment
indicators provide a broader picture. These are quantitative and harder to
manipulate than social media posts.

### Put/Call Ratio

The ratio of put volume to call volume on equity options.

| Reading | Interpretation | Trading Signal |
|---------|---------------|----------------|
| > 1.2 | Elevated fear, heavy put buying | Contrarian bullish (retail hedging = bottoming) |
| 0.7 - 1.0 | Normal range | No signal |
| < 0.6 | Extreme complacency, heavy call buying | Contrarian bearish (greed = topping) |

**Why it is contrarian**: When everyone is buying puts, the "wall of worry"
is priced in. Market makers who sold those puts are delta-hedged and will
need to buy stock as the market rises, fueling a rally. The reverse is true
for extreme call buying.

**Which ratio to use**: The CBOE equity-only put/call ratio (not total, which
includes index hedging by institutions that distorts the signal).

### AAII Sentiment Survey

The American Association of Individual Investors surveys members weekly on
whether they are bullish, bearish, or neutral for the next 6 months.

| Reading | Historical Average | Extreme |
|---------|-------------------|---------|
| Bullish | ~37% | > 55% (contrarian bearish) |
| Bearish | ~31% | > 50% (contrarian bullish) |

**Why it works**: Retail investors as a group are reliably wrong at extremes.
When 55%+ are bullish, most buying is already done. When 50%+ are bearish,
most selling is already done. This indicator has a strong 6-month forward
return signal at extremes.

### CNN Fear & Greed Index

A composite of seven indicators scored 0 (extreme fear) to 100 (extreme greed):

1. Market momentum (S&P 500 vs. 125-day MA)
2. Stock price strength (new highs vs. new lows)
3. Stock price breadth (advancing vs. declining volume)
4. Put/Call ratio
5. Market volatility (VIX vs. 50-day MA)
6. Safe haven demand (stock vs. bond returns)
7. Junk bond demand (yield spread vs. investment grade)

| Score | Zone | Implication |
|-------|------|-------------|
| 0-25 | Extreme Fear | Contrarian buy zone |
| 25-45 | Fear | Cautiously bullish |
| 45-55 | Neutral | No edge |
| 55-75 | Greed | Cautiously bearish |
| 75-100 | Extreme Greed | Contrarian sell zone |

### Fund Flows

ETF inflows and outflows reveal what large pools of money are doing. This is
institutional-grade sentiment data.

```
Key flows to monitor:
- SPY/VOO/IVV inflows: Broad equity confidence
- TLT/IEF inflows: Flight to safety
- HYG/JNK inflows: Risk appetite (high yield = risk-on)
- GLD/SLV inflows: Inflation/uncertainty hedging
- Sector ETF flows: Sector rotation in real time
```

**Important nuance**: A single week of flows means nothing. Look for 4-week
rolling trends. Sustained outflows from equities into bonds over a month is
meaningful. One bad week is not.

---

## Trader Reputation Tracking

SignalSiphon maintains a reputation score for each author it tracks. This is
one of the most valuable features because it solves the core problem of social
sentiment: anyone can post anything.

### How Reputation Is Calculated

```python
def calculate_reputation(author_signals):
    if len(author_signals) < 10:
        return None  # Not enough data to judge

    correct = sum(1 for s in author_signals if s.direction_correct_24h)
    accuracy = correct / len(author_signals)

    # Weight recent signals more heavily
    recent_accuracy = weighted_accuracy(author_signals[-20:])

    # Penalize inconsistency (flip-floppers)
    consistency = 1.0 - signal_reversal_rate(author_signals)

    reputation = (accuracy * 0.4) + (recent_accuracy * 0.4) + (consistency * 0.2)
    return reputation
```

### Reputation Tiers

| Tier | Score | Signal Weight |
|------|-------|--------------|
| Unproven | < 10 signals | 0.5x (discount) |
| Noise | < 0.40 | 0.0x (filter out) |
| Average | 0.40 - 0.55 | 0.5x |
| Reliable | 0.55 - 0.70 | 1.0x |
| Expert | > 0.70 | 1.5x (amplify) |

---

## The Contrarian Principle

The single most important concept in sentiment analysis: extreme readings
are reversal signals. This is not a theory -- it is backed by decades of
market data.

**Why it works**: Markets are reflexive. When sentiment reaches an extreme,
the participants who hold that view have already acted on it. If everyone
is bullish, everyone has already bought. There are no more buyers left, so
the next move is down. The reverse is equally true.

**When it fails**: Strong trends can sustain extreme sentiment longer than
expected. Extreme bullish sentiment in a secular bull market may persist
for months. Use sentiment as a timing refinement within your broader
regime analysis, not as a standalone reversal trigger.

---

## Integration with MasterQuantAgent

Sentiment is one of several inputs in the MasterQuantAgent ensemble. It
carries a weight of 0.10 (10%) in the final signal.

```
MasterQuantAgent ensemble weights:
- Technical signals:  0.35
- Options flow:       0.25
- Regime detection:   0.20
- Sentiment:          0.10
- Fundamental:        0.10
```

### Why Only 10%?

Sentiment is noisy, lagging relative to options flow, and easy to manipulate.
It adds value at extremes but provides little edge in the neutral zone (which
is where it sits most of the time). A 10% weight means sentiment can tip a
borderline signal but cannot override strong technical or options flow data.

### How Sentiment Modifies Signals

```
If technical_signal == LONG and sentiment > +0.5:
    confidence += 0.10  # Sentiment confirms

If technical_signal == LONG and sentiment < -0.5:
    confidence -= 0.15  # Sentiment disagrees (larger penalty)

If sentiment > +0.8 or sentiment < -0.8:
    flag_as_contrarian_opportunity()  # Alert for manual review
```

The asymmetry is intentional. Disagreement is penalized more than agreement
is rewarded because sentiment extremes against your position indicate a
crowded trade with reversal risk.
