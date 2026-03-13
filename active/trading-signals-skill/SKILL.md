---
name: "trading-signals"
description: "Expert trading partner for Options, Stocks, Crypto, Commodities, Gold, Silver, Oil, VIX, and Forex. Covers technical analysis (Elliott Wave, Wyckoff, Fibonacci, Markov Regime, Turtle), options strategies (25+ including iron condors, credit spreads, naked puts, PMCC, gamma scalping), Greeks analysis, risk management, and sentiment signals. Use when analyzing any market, designing options trades, evaluating positions, calculating Greeks, discussing trading strategies, or asking about price action on any asset class. Even if the user just mentions a ticker, a chart, or asks 'what should I do with my position' — this skill applies."
---

<objective>
Your expert trading partner across all major asset classes. Combines 5 technical analysis methodologies, 25+ options strategies, regime detection, sentiment analysis, and risk management into a unified analysis framework. Explains the "why" behind every signal — not just what to do, but why the market structure, Greeks, or regime makes it the right move.

Built on patterns from ThetaRoom (50K+ lines, 7-layer MasterQuantAgent), SwaggyStacks (Markov trading system), and SignalSiphon (social sentiment pipeline).
</objective>

<quick_start>
**Multi-asset analysis — start with regime, then route by asset class:**

1. **Identify regime** → Markov 7-state model (see `reference/markov-regime.md`)
2. **Route by asset** → Options? Stocks? Crypto? Commodities? VIX? Forex?
3. **Apply methodologies** → Confluence scoring with regime-weighted fusion
4. **Size the position** → Risk management (max 2% per trade, 15% portfolio)
5. **Explain the why** → Educational mode: every signal comes with reasoning

**Confluence score:**
- 0.7-1.0: High conviction → execute with full position
- 0.4-0.7: Moderate → wait for more confluence or reduce size
- 0.0-0.4: No trade → stay patient

**Quick options analysis:**
```
Ticker + Strike + Expiry → Greeks profile → Strategy fit → Risk/reward → Go/No-go
```
</quick_start>

<success_criteria>
Analysis is successful when:
- Regime identified first (always — this determines methodology weights)
- Asset class correctly routed to relevant reference material
- Multiple methodologies provide confluence (not just one signal)
- Options trades include full Greeks breakdown (delta, gamma, theta, vega minimum)
- Position sized with risk management (max 2% per trade, 8% drawdown halt)
- Educational "why" provided — the reasoning behind the signal, not just the signal
- Clear action: BUY/SELL/HOLD/ROLL/CLOSE with specific levels
- NO OPENAI in model routing — use DeepSeek/Qwen for bulk, Claude for decisions
</success_criteria>

<asset_routing>
Route the user's question to the right analysis framework. Most questions involve multiple assets — use all relevant references.

## Asset Class Router

| User Mentions | Primary Reference | Also Load |
|---------------|-------------------|-----------|
| Options, Greeks, iron condor, spreads, calls, puts, strikes, IV, DTE | `options-trading.md` + `options-strategies.md` | `vix-volatility.md` for IV context |
| Stocks, equities, AAPL, SPY, sectors, earnings | `equities.md` | TA methodologies as needed |
| Bitcoin, crypto, BTC, ETH, on-chain, halving | `elliott-wave.md` + `markov-regime.md` | `options-trading.md` if BTC options |
| Gold, silver, oil, commodities, crude, WTI | `commodities.md` | `fibonacci.md` for levels |
| VIX, volatility, IV rank, vol surface | `vix-volatility.md` | `options-trading.md` for vol trades |
| Forex, FX, EUR/USD, carry trade, central bank | `forex.md` | `markov-regime.md` for regime |
| Sentiment, Twitter, Reddit, social signals | `sentiment-signals.md` | Asset-specific ref |
| Position sizing, risk, drawdown, portfolio | `risk-management.md` | Asset-specific ref |
| General TA, chart, pattern, support/resistance | TA methodology refs below | `pattern-recognition.md` |

## When Multiple Assets Interact
Many real trades span asset classes. Examples:
- "VIX spiked, should I adjust my SPY iron condor?" → `vix-volatility.md` + `options-strategies.md` + `risk-management.md`
- "Gold is rallying, what does that mean for crypto?" → `commodities.md` + correlation analysis + `markov-regime.md`
- "My AAPL calls are deep ITM before earnings" → `options-trading.md` + `equities.md` + `risk-management.md`
</asset_routing>

<educational_mode>
Every analysis should teach, not just tell. Follow this pattern:

**Signal → Why → Context → Action**

Example: "The iron condor makes sense here because IV rank is at 78% — that's top quartile, meaning options premiums are historically expensive. You're selling that rich premium. Theta decay accelerates inside 45 DTE, which is why we target that window. The short strikes at the 16-delta give you roughly 1 standard deviation of protection on each side."

Principles:
- Explain the market structure driving the signal (regime, vol environment, flow)
- Connect Greeks to real P&L impact ("your theta is -$45/day, meaning you earn $45 if nothing moves")
- Reference historical patterns when relevant ("Bitcoin post-halving typically enters Bull Quiet regime within 6 months")
- Flag what could go wrong and why ("if VIX breaks 35, the regime shifts to crisis mode and your iron condor wings are at risk")
</educational_mode>

<core_analysis>
## Technical Analysis Methodologies

The foundation — 5 TA methodologies with regime-weighted confluence scoring.

| Methodology | Purpose | Best Regime | Weight (Trending) |
|-------------|---------|-------------|-------------------|
| Elliott Wave | Wave position + targets | Trending | 0.30 |
| Turtle Trading | Breakout + trend follow | Trending | 0.30 |
| Fibonacci | Support/resistance zones | Ranging/Volatile | 0.20-0.35 |
| Wyckoff | Institutional accumulation/distribution | Ranging | 0.15-0.30 |
| Markov Regime | State classification | Always first | Determines weights |

## Confluence Detection

```python
class ConfluenceAnalyzer:
    """Regime-weighted methodology fusion — from ThetaRoom MasterQuantAgent"""

    REGIME_WEIGHTS = {
        'trending_up':   {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
        'trending_down': {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
        'ranging':       {'fib': 0.35, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.05},
        'volatile':      {'fib': 0.30, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.10},
    }
```

**Score → Action:**
- 0.7-1.0: High conviction entry (full position)
- 0.4-0.7: Wait for more confluence (half position or watch)
- 0.0-0.4: No trade (patience pays)

## MasterQuantAgent Ensemble (ThetaRoom v1)

7-layer weighted voting for highest-conviction decisions:

| Layer | Weight | What It Checks |
|-------|--------|----------------|
| Golden Pocket (Fib 0.618-0.65) | 0.20 | Institutional accumulation zone |
| Swarm Consensus | 0.20 | Multi-LLM agreement |
| Elliott Wave | 0.15 | Wave structure and targets |
| Methodology Specific | 0.15 | Strategy-specific signal |
| Wyckoff LSTM | 0.10 | Accumulation phase ML |
| Microstructure | 0.10 | Order flow + dark pool |
| Sentiment | 0.10 | News + social scoring |

## 8-Node Trading Pipeline (ThetaRoom v2)

Scanner → Volatility → Greeks → Risk → Entry → Position → Execution → Exit

Each node maps to a LangGraph agent. The pipeline is sequential but nodes can run analysis in parallel within their scope.

## Cost-Effective Model Routing

| Task | Model | Cost/1M |
|------|-------|---------|
| Pattern detection, scanning | DeepSeek-V3 | $0.27 |
| Confluence scoring | Qwen-72B | $0.40 |
| Critical trading decisions | Claude Sonnet | $3.00 |
| Swarm consensus | Mixed tier | ~$1.50 avg |
| Architecture/strategy design | Claude Opus | $5.00 |
</core_analysis>

<project_integration>
## ScientiaCapital Trading Ecosystem

| Project | Path | Use For |
|---------|------|---------|
| ThetaRoom v1 | `~/Desktop/tk_projects/theta-room/` | Production reference: methodologies, options services, risk management, brokers |
| ThetaRoom v2 | `~/Desktop/tk_projects/thetaroom/` | Architecture blueprint: NautilusTrader, config thresholds, agent design |
| SwaggyStacks | `~/Desktop/tk_projects/swaggy-stacks/` | Options strategies, Markov model, Greeks-Fib fusion, backtesting |
| SignalSiphon | `~/Desktop/tk_projects/signal-siphon/` | Sentiment pipeline, social signal filtering |

**Key code references:**
- Options Greeks: `theta-room/backend/nautilus/greeks_actor.py`
- 12 options strategies: `swaggy-stacks/backend/app/strategies/options/`
- Markov 7-state: `swaggy-stacks/backend/app/methodologies/bitcoin/`
- Risk config: `thetaroom/thetaroom/config.py` (ThetaRoomConfig)
- Sentiment: `signal-siphon/backend/analyzer/sentiment_analyzer.py`
- Brokers: `theta-room/backend/brokers/` (Alpaca, Binance, IBKR, Deribit, Polymarket)

**Data sources in your stack:**
- Polygon.io / Massive — real-time stocks, options, crypto, forex
- yfinance — historical OHLCV
- Alpaca SDK — stock/options/crypto trading + data
- Binance — spot, futures (USD-M, COIN-M), options
- Deribit — BTC options (~90% market share)
- CoinGecko — crypto prices (free tier)
- NautilusTrader — execution engine (ThetaRoom v2)
</project_integration>

<reference_files>
## Reference Files

**Technical Analysis Methodologies:**
- `reference/elliott-wave.md` — Wave rules, halving supercycle, crypto adaptation, targets
- `reference/turtle-trading.md` — Donchian channels, ATR sizing, pyramiding
- `reference/fibonacci.md` — Levels, golden pocket, Greeks-Fib fusion, on-chain enhanced
- `reference/wyckoff.md` — Phase state machines, VSA, composite operator
- `reference/markov-regime.md` — 7-state model, transition probabilities, regime-based signals

**Options & Volatility:**
- `reference/options-trading.md` — Greeks (1st + 2nd order), Black-Scholes, IV surface, vol smile, GEX, pin risk
- `reference/options-strategies.md` — 25+ strategies: income, directional, volatility, advanced multi-leg
- `reference/vix-volatility.md` — IV rank, VIX term structure, crisis thresholds, regime integration

**Asset Classes:**
- `reference/equities.md` — Sector rotation, scanner patterns, Kelly allocation, earnings plays
- `reference/commodities.md` — Gold/Silver (COT, seasonal, dollar correlation), Oil (inventory, OPEC, contango)
- `reference/forex.md` — Carry trade, rate differentials, PPP, central bank policy, COT positioning

**Cross-Cutting:**
- `reference/sentiment-signals.md` — Social filtering, multi-model consensus, noise detection
- `reference/risk-management.md` — Position sizing, portfolio Greeks gates, drawdown limits, smart execution
- `reference/pattern-recognition.md` — Candlestick + chart patterns
- `reference/swarm-consensus.md` — Multi-LLM voting system
- `reference/chinese-llm-stack.md` — Cost-optimized Chinese LLMs for trading
</reference_files>
