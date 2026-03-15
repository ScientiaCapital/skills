---
name: "trading-alert-scheduler"
description: "Market signals → daily digest delivered before market open. Scans watchlist tickers for regime changes, technical setups, options flow anomalies, and IBKR position health — then delivers a prioritized action list. No IBKR distraction during 50-call BDR days. Use when: 'market digest', 'trading alerts', 'pre-market scan', 'watchlist check', 'what's setting up', 'trading morning brief', 'market open prep'."
---

<objective>
Eliminate real-time market monitoring during BDR work hours. Scan Tim's watchlist and IBKR positions once daily before market open, identify actionable setups using the trading-signals framework, and deliver a single prioritized digest. No intraday distractions — just one morning read that surfaces what matters.

Target: 30 min/day saved + fewer missed setups from not watching screens during 50-call days.
</objective>

<quick_start>
**Daily automated run (7am CST / 8am EST — 1.5 hrs before market open):**
Scheduled task scans all watchlist tickers + open positions → delivers digest

**On-demand:**
"market digest" → runs full scan now
"what's setting up" → filtered to high-conviction setups only
"check my positions" → IBKR portfolio health only

**Trigger phrases:**
- "market digest" / "trading alerts" / "pre-market scan"
- "watchlist check" / "what's setting up"
- "trading morning brief" / "market open prep"
- "check my positions" / "position health"
</quick_start>

<success_criteria>
- All watchlist tickers scanned with regime + technical analysis
- Open IBKR positions checked for risk/expiry/Greeks health
- High-conviction setups (confluence ≥ 0.7) surfaced at top
- Position risk alerts flagged (approaching max loss, expiry, assignment risk)
- Digest scannable in under 3 minutes
- No intraday interruptions — one daily read covers everything
- Missed setup rate reduced vs manual checking
</success_criteria>

<workflow>

## Architecture

```
SCHEDULED (7am CST)          ANALYSIS                       OUTPUT
──────────────────────────────────────────────────────────────────────
Watchlist tickers     →  Regime detection (Markov)    →  Daily Digest
IBKR open positions   →  Technical scan (5 methods)   →  Action List
Market internals      →  Options flow anomalies       →  Position Alerts
Economic calendar     →  Greeks/risk check positions   →  Risk Dashboard
```

## Stage 1: Data Collection

### 1a. Watchlist Tickers
Tim's default watchlist (update in `reference/watchlist.json`):

**Core positions:** SPY, QQQ, IWM, TLT, GLD, SLV, USO, VIX
**Individual stocks:** AAPL, MSFT, NVDA, TSLA, AMZN, META, GOOG, AMD, PLTR, COIN
**Crypto proxies:** BITO, MSTR
**Sector ETFs:** XLF, XLE, XLK, ARKK, SMH

For each ticker, use web search to pull:
- Current price + pre-market move
- 5-day price action summary
- Volume vs average
- Key support/resistance levels
- Any overnight news/catalysts

### 1b. IBKR Portfolio Positions
Use IBKR API skill tools to pull:
- All open positions across accounts (Roth IRA, personal brokerage, business)
- Current P&L per position
- Options positions: strike, expiry, current Greeks
- Margin utilization
- Cash available

### 1c. Market Internals
Web search for:
- S&P 500 advance/decline
- VIX level + term structure (contango/backwardation)
- Put/call ratio
- 10Y Treasury yield
- DXY (dollar index)
- Fed funds futures (rate expectations)
- Economic calendar events for today

## Stage 2: Analysis (Using trading-signals Framework)

### 2a. Regime Detection
For SPY (market proxy), run Markov 7-state regime model:

| State | Description | Strategy Bias |
|-------|-------------|--------------|
| 0 | Strong bull | Long bias, sell puts |
| 1 | Moderate bull | Long bias, covered calls |
| 2 | Weak bull / consolidation | Neutral, iron condors |
| 3 | Transition / chop | Reduce size, wait |
| 4 | Weak bear | Hedge, reduce long |
| 5 | Moderate bear | Short bias, buy puts |
| 6 | Crash / high vol | Protection mode, VIX plays |

### 2b. Per-Ticker Technical Scan
For each watchlist ticker, score on 5 methodologies:

| Method | Signal | Weight (regime-adjusted) |
|--------|--------|------------------------|
| Elliott Wave | Wave position + projected target | 20-30% |
| Wyckoff | Accumulation/distribution phase | 15-25% |
| Fibonacci | Key retracement/extension levels | 15-20% |
| Turtle | Donchian breakout signals | 10-20% |
| Markov Regime | Regime-appropriate strategy | 20-30% |

**Confluence Score:** Weighted average across methods
- ≥ 0.7: **HIGH** — Flag as actionable setup
- 0.4-0.7: **MODERATE** — Watch list, note trigger level
- < 0.4: **LOW** — No action, skip from digest

### 2c. Options Flow Scan
For tickers with options positions or high confluence:
- Unusual volume (>2x avg) on specific strikes
- Put/call ratio shifts
- Implied volatility rank (IVR) — is premium rich or cheap?
- Earnings dates within 14 days

### 2d. Position Health Check
For each open IBKR position:

| Check | Alert Threshold |
|-------|----------------|
| Days to expiry | < 7 DTE on options → ROLL/CLOSE decision |
| Delta exposure | Portfolio delta > ±50 → hedge needed |
| Max loss approaching | Position down > 50% of max loss → manage |
| Assignment risk | ITM short options near expiry → close or roll |
| Theta decay | Positive theta across portfolio? |
| Margin utilization | > 50% → reduce risk |
| Concentrated position | Any single position > 15% of portfolio → flag |

## Stage 3: Output — Daily Trading Digest

```
╔══════════════════════════════════════════════════════════════╗
║  TRADING DIGEST — [Date] | Pre-Market                        ║
║  Market Regime: [STATE] | VIX: [level] | Futures: [ES move]  ║
╠══════════════════════════════════════════════════════════════╣

MARKET OVERVIEW:
- ES Futures: [+/-X.XX%] | NQ: [+/-X.XX%]
- VIX: [level] ([contango/backwardation])
- 10Y: [yield] | DXY: [level]
- Key event today: [economic calendar item]

═══════════════════════════════════════════════════════════════

🎯 HIGH-CONVICTION SETUPS (confluence ≥ 0.7):

1. [TICKER] — [Direction] | Confluence: [0.XX]
   Setup: [description — e.g., "Wyckoff spring at $185 support,
          Elliott wave 3 launching, Turtle breakout confirmed"]
   Entry: $[XX.XX] | Target: $[XX.XX] | Stop: $[XX.XX]
   Options play: [specific strategy — e.g., "Apr 190C @ $3.20,
                  delta 0.45, 3:1 R:R"]
   Why: [1-2 sentence reasoning]

2. [TICKER] — [Direction] | Confluence: [0.XX]
   ...

═══════════════════════════════════════════════════════════════

⚠️ POSITION ALERTS (action needed):

1. [TICKER] [STRIKE] [EXPIRY] — [ALERT TYPE]
   Current P&L: [+/-$XXX] | Days to expiry: [X]
   Recommended action: [ROLL to [new strike/expiry] | CLOSE | HOLD]
   Why: [reason]

═══════════════════════════════════════════════════════════════

👀 WATCHLIST (confluence 0.4-0.7, not yet actionable):

| Ticker | Direction | Confluence | Trigger Level | Note |
|--------|-----------|------------|---------------|------|
| NVDA | Long | 0.55 | Break $950 | Needs volume confirm |
| TLT | Long | 0.48 | Hold $88 | Rate decision Thurs |

═══════════════════════════════════════════════════════════════

📊 PORTFOLIO SNAPSHOT:
| Account | Value | Day P&L | Margin Used |
|---------|-------|---------|-------------|
| Roth IRA | $XX,XXX | +/-$XXX | N/A |
| Personal | $XX,XXX | +/-$XXX | XX% |
| Business | $XX,XXX | +/-$XXX | XX% |

Net Delta: [+/-XX] | Net Theta: [+/-$XX/day] | IVR avg: [XX%]

═══════════════════════════════════════════════════════════════

📅 THIS WEEK:
- [Earnings/events that affect watchlist]
- [Fed speakers / economic data]
- [Options expiration dates]

╚══════════════════════════════════════════════════════════════╝
```

## Rules
- **No intraday alerts.** This runs ONCE at 7am. Tim checks it, makes decisions, then focuses on BDR work.
- **Actionable only.** Don't list 30 tickers with "neutral" signals. Only surface what needs attention.
- **Position management first.** Alerts on existing positions before new setups.
- **Risk management always.** Every setup includes stop loss. Portfolio delta/margin always visible.
- **2% rule enforced.** Flag if any suggested trade exceeds 2% portfolio risk.
- **15% concentration rule.** Flag if any position exceeds 15% of account.

</workflow>

<dependencies>
## Required Skills
- `trading-signals-skill` — Core analysis framework (regime detection, 5 methodologies, options strategies, Greeks)
- `ibkr-api-skill` — IBKR portfolio data (positions, P&L, margin, account values)

## Required Tools
- **Web Search:** Pre-market data, news, economic calendar, options flow (primary data source)
- **IBKR MCP (optional):** Portfolio positions, account balances, order status — requires IBKR MCP server (e.g., `rcontesti/IB_MCP` or `xiao81/IBKR-MCP-Server`) connected to running IB Gateway. If not available, web search covers market data; portfolio section shows "IBKR not connected" placeholder.
- **Scheduling:** CronCreate `"53 6 * * 1-5"` for session-based 7am CST runs (3-day auto-expire)

## Data Sources (via web search)
- Yahoo Finance / TradingView: Price data, technicals
- CBOE: VIX, put/call ratios
- CME: Futures, Fed funds
- Finviz: Screener, market internals
- Unusual Whales / Barchart: Options flow
</dependencies>
