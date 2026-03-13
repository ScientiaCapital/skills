# Backtesting Patterns

Backtesting answers the question every trader should ask before risking real money: **does this strategy actually work on historical data?** A strategy that "feels right" but hasn't been backtested is just a hunch. These patterns come from the SwaggyStacks backtesting engine.

## Architecture

The SwaggyStacks backtesting system (`backend/app/backtesting/`) uses three components that separate concerns cleanly:

```
BacktestEngine (orchestrator)
├── SignalGenerator    — produces buy/sell signals from strategy rules
├── PortfolioManager   — tracks trades, manages capital, handles correlations
└── PerformanceAnalyzer — computes metrics from completed trade history
```

**Why this separation matters:** You can swap signal generators without touching portfolio logic. You can test the same signals with different position sizing. You can compute metrics on any trade history, not just backtests.

## Backtest Modes

### Full Backtest

Complete historical simulation from start to end date. Every bar processed sequentially. Good for initial validation, but dangerous alone — it shows you what happened, not what will happen.

### Walk-Forward

Rolling train/test windows that prevent overfitting. The model trains on window N, tests on window N+1, then slides forward. This is the gold standard — if a strategy only works in-sample, walk-forward exposes it.

```python
# Walk-forward: train on 252 days, test on 63 days, slide by 63
for train_start in range(0, len(data) - train_window - test_window, step):
    train = data[train_start : train_start + train_window]
    test = data[train_start + train_window : train_start + train_window + test_window]
    model.fit(train)
    results.append(model.predict(test))
```

### Monte Carlo

Random sampling of trade sequences to build confidence intervals. Answers: "given this set of trades, what's the range of possible outcomes?" Essential for understanding tail risk — your backtest shows one path, Monte Carlo shows thousands.

### Optimization

Parameter grid search across strategy variables. Use with caution — optimization without walk-forward confirmation is curve-fitting, not discovery.

## Implementation Pattern

```python
class BacktestEngine:
    """Core orchestrator — coordinates signal generation, execution, and analysis."""

    def __init__(self, initial_capital=100000, transaction_costs=0.001):
        self.signal_generator = SignalGenerator()
        self.portfolio_manager = PortfolioManager(initial_capital)
        self.analyzer = PerformanceAnalyzer()
        self.transaction_costs = transaction_costs

    def run(self, df, strategies, mode='full'):
        signals = self.signal_generator.generate(df, strategies)
        trades = self.portfolio_manager.execute(signals, costs=self.transaction_costs)
        return self.analyzer.compute_metrics(trades)

    def walk_forward(self, df, strategies, train_window=252, test_window=63):
        """Rolling window backtest — the only mode you should trust."""
        all_results = []
        for start in range(0, len(df) - train_window - test_window, test_window):
            train = df.iloc[start : start + train_window]
            test = df.iloc[start + train_window : start + train_window + test_window]
            self.signal_generator.fit(train, strategies)
            signals = self.signal_generator.generate(test, strategies)
            trades = self.portfolio_manager.execute(signals, costs=self.transaction_costs)
            all_results.append(self.analyzer.compute_metrics(trades))
        return self.analyzer.aggregate(all_results)
```

## Options Backtesting

From `swaggy-stacks/backend/app/backtesting/options_backtester.py`. Options introduce complexity that equity backtesting doesn't have.

**Key challenges:**
- **Expiration modeling:** Options expire. The backtester must handle exercise, assignment risk, and worthless expiry
- **Volatility surface simulation:** IV changes throughout the position lifecycle — a backtest using constant IV is fiction
- **Greeks evolution:** Delta/gamma/theta/vega shift as price moves and time passes. Track them per-bar, not just at entry
- **Early assignment:** American-style options can be assigned early, especially near ex-dividend dates or deep ITM

```python
class OptionsBacktester(BacktestEngine):
    """Extends base engine with options-specific lifecycle management."""

    def execute_option_trade(self, signal, vol_surface, days_to_expiry):
        greeks = self.compute_greeks(signal, vol_surface, days_to_expiry)
        # Track Greeks evolution bar-by-bar
        for bar in range(days_to_expiry):
            greeks = self.update_greeks(greeks, new_price, new_iv, bar)
            if self.check_early_assignment(greeks, bar):
                return self.handle_assignment(greeks)
        return self.handle_expiry(greeks)
```

## Ensemble Backtesting

From `swaggy-stacks/backend/app/backtesting/ensemble_backtest.py`. Tests multiple strategies running simultaneously in one portfolio.

**What it answers:**
- Do these strategies actually diversify each other, or do they all lose money at the same time?
- What's the optimal allocation across strategies?
- Which strategy pairs have negative correlation (the holy grail)?

```python
class EnsembleBacktester:
    def test_portfolio(self, df, strategy_list, allocations):
        """Run all strategies simultaneously, track portfolio-level metrics."""
        strategy_results = {}
        for strategy, allocation in zip(strategy_list, allocations):
            engine = BacktestEngine(initial_capital=self.capital * allocation)
            strategy_results[strategy.name] = engine.run(df, [strategy])

        correlation_matrix = self.compute_correlations(strategy_results)
        combined = self.merge_equity_curves(strategy_results)
        return self.analyzer.compute_metrics(combined), correlation_matrix
```

## Combinatorial Alpha Discovery

From `swaggy-stacks/backend/app/backtesting/combinatorial/`. The idea: some strategies work better together than alone. Combinatorial testing finds those synergies.

**Synergy matrix:** Test all pairwise (and higher-order) strategy combinations. A pair has positive synergy when the combined Sharpe exceeds the weighted average of individual Sharpes.

**Statistical validation:** With enough combinations, you will find "winners" by chance (p-hacking). Guard against this:
- Bonferroni correction for multiple comparisons
- Minimum sample size per combination (100+ trades)
- Out-of-sample confirmation required before any combination is "validated"

**Walk-forward confirmation:** Any synergy discovered in-sample must survive walk-forward testing. If it doesn't, it's noise.

## Performance Metrics

| Metric | Formula / Description | Good Target | Why It Matters |
|--------|----------------------|-------------|----------------|
| Sharpe Ratio | (Return - Rf) / StdDev | > 1.5 | Risk-adjusted return — the universal benchmark |
| Sortino Ratio | (Return - Rf) / DownsideDev | > 2.0 | Like Sharpe but only penalizes downside volatility |
| Max Drawdown | Peak-to-trough decline | < 15% | Can you stomach the worst losing streak? |
| Calmar Ratio | Annual Return / Max DD | > 1.0 | Return per unit of drawdown pain |
| Win Rate | Winning trades / Total | > 55% | Higher is better, but meaningless without risk/reward |
| Profit Factor | Gross Profit / Gross Loss | > 1.5 | How much you win vs how much you lose |
| Avg Win/Loss | Mean winner / Mean loser | > 1.5 | A 40% win rate works if winners are 3x losers |
| Recovery Factor | Net Profit / Max DD | > 3.0 | How fast the strategy recovers from drawdowns |

**Warning:** No single metric tells the whole story. A strategy with 2.0 Sharpe but 40% max drawdown will destroy your sleep. Always look at Sharpe + Max Drawdown + Recovery Factor together.

## Best Practices

**Always use walk-forward.** In-sample-only backtests are worthless for predicting future performance. If someone shows you a beautiful equity curve without walk-forward, they've curve-fit.

**Transaction costs matter.** Default 0.1% for equities, but options can be 0.5-2% depending on bid-ask spread. A strategy that's profitable at zero cost often dies at realistic costs.

**Model slippage.** Illiquid instruments (small-cap options, crypto altcoins) have wide spreads. Your backtest assumes you get the mid-price — you won't. Add 1-3 ticks of slippage.

**Survivorship bias.** If your historical data only includes stocks that still exist today, you're missing all the ones that went to zero. Include delisted securities.

**Look-ahead bias.** The most subtle bug: using data that wouldn't have been available at the time of the signal. Examples: using today's close to make today's decision, or using a fundamental ratio that gets restated.

**Minimum trade count.** 30 trades is too few for statistical significance. Target 100+ trades before drawing conclusions. Monte Carlo simulation helps when trade count is low.

**Regime-aware testing.** A trend-following strategy will show terrible results in ranging markets — that's expected. Test within each regime separately (see `reference/markov-regime.md`) to understand when the strategy works vs when it should be turned off.

## Code References

| Component | SwaggyStacks Path |
|-----------|-------------------|
| Backtest engine | `backend/app/backtesting/engine.py` |
| Signal generator | `backend/app/backtesting/signal_generator.py` |
| Portfolio manager | `backend/app/backtesting/portfolio_manager.py` |
| Performance analyzer | `backend/app/backtesting/performance_analyzer.py` |
| Options backtester | `backend/app/backtesting/options_backtester.py` |
| Ensemble backtester | `backend/app/backtesting/ensemble_backtest.py` |
| Combinatorial discovery | `backend/app/backtesting/combinatorial/` |
| Strategy definitions | `backend/app/strategies/` |

## Integration with Other References

- **Markov regime:** `reference/markov-regime.md` — regime-aware backtesting requires regime labels on historical data
- **Turtle trading:** `reference/turtle-trading.md` — Donchian channel breakout is a natural backtest candidate (fully rule-based)
- **Options strategies:** `reference/options-strategies.md` — each of the 25+ strategies can be backtested using the options backtester
- **Risk management:** `reference/risk-management.md` — position sizing rules are tested as part of the portfolio manager
