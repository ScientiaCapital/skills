# Risk Management -- Position Sizing, Greeks Gates & Drawdown

## Why This Matters

Every successful trader will tell you the same thing: risk management is
the only edge that compounds. A brilliant signal generator with poor risk
management will blow up. A mediocre signal generator with excellent risk
management will survive and compound. This reference covers the specific
rules and formulas that ThetaRoom v2 uses to protect capital.

---

## Core Position Sizing Rules

These three numbers from the ThetaRoom v2 config define the risk envelope.
Every trade must fit inside them before execution.

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `max_portfolio_risk_pct` | 0.15 (15%) | Maximum total portfolio value at risk across all positions |
| `max_per_trade_risk_pct` | 0.02 (2%) | Maximum risk on any single trade |
| `max_drawdown_halt_pct` | 0.08 (8%) | If portfolio drops 8% from peak, halt all trading |

### Why These Specific Numbers

**15% max portfolio risk**: With 15% at risk, even a catastrophic scenario
where every position hits max loss simultaneously leaves you with 85% of
your capital. That is recoverable. At 30% portfolio risk, a correlated
selloff can take you down 30%, which requires a 43% gain to recover.

**2% per trade**: The 2% rule ensures no single trade can meaningfully
damage the portfolio. If you have a string of 5 consecutive losers (which
happens), you lose 10%. Painful but survivable. At 5% per trade, five
losers costs you 25% -- now you need a 33% gain just to break even.

**8% drawdown halt**: This is the circuit breaker. When you are in drawdown,
your judgment is compromised. Stopping at 8% forces you to step back,
analyze what went wrong, and return with a plan. Without this rule, traders
in drawdown increase size to "make it back" and accelerate their losses.

---

## Kelly Criterion

The Kelly Criterion calculates the mathematically optimal fraction of your
bankroll to bet on each wager, given your edge.

### The Formula

```python
kelly_fraction = (win_prob * avg_win - (1 - win_prob) * avg_loss) / avg_win
position_size = kelly_fraction * 0.5  # Half Kelly for safety
```

### Why Half Kelly Is Standard

Full Kelly maximizes the geometric growth rate of your portfolio. That
sounds ideal until you see the drawdown profile. Full Kelly produces
drawdowns of 50-70% that can last months. Psychologically, almost no one
can hold through that.

Half Kelly gives you approximately 75% of the growth rate with roughly
half the maximum drawdown. The math is favorable: you give up 25% of
theoretical growth to cut your worst-case pain in half.

### When Kelly Breaks Down

Kelly assumes you know your exact win probability and payoff ratio. In
trading, you never do. Your estimates are always approximations based on
historical data that may not repeat. When your inputs are uncertain, Full
Kelly overbets. Half Kelly provides a margin of safety for estimation error.

### Practical Kelly Example

```
Strategy: Vertical credit spreads on SPY
Historical win rate: 72%
Average win: $150 (credit received)
Average loss: $350 (max loss - credit)

kelly = (0.72 * 150 - 0.28 * 350) / 150
     = (108 - 98) / 150
     = 0.067 (6.7%)

half_kelly = 0.067 * 0.5 = 0.033 (3.3% of portfolio per trade)
```

Notice how even a 72% win rate strategy only warrants 3.3% per trade at
Half Kelly. This is why experienced traders use small position sizes --
the math demands it.

---

## Portfolio Greeks Gates

Before any new position is opened, the system checks whether it would push
portfolio-level Greeks beyond safe limits. If it would, the trade is denied.
This prevents concentration risk that individual position limits cannot catch.

### The Limits

| Greek | Limit | What It Protects Against |
|-------|-------|------------------------|
| **Portfolio Delta** | +/-300 (beta-weighted to SPY) | Directional blowup if market gaps |
| **Portfolio Gamma** | Monitor near expiration | Rapid delta changes causing uncontrolled exposure |
| **Portfolio Theta** | Must be positive (for premium sellers) | Ensures time decay works for you, not against you |
| **Portfolio Vega** | Watch for concentration | A vol crush or spike hitting all positions at once |

### Why Beta-Weighted Delta

A delta of 50 on AAPL is not the same as a delta of 50 on a $20 stock. Beta
weighting converts all deltas to SPY-equivalent units so you can compare
apples to apples (pun intended). A portfolio with +300 beta-weighted delta
behaves roughly like being long 300 shares of SPY.

### Gamma Risk Near Expiration

Gamma spikes as options approach expiration. A position that had manageable
gamma at 30 DTE can have extreme gamma at 1 DTE. The system monitors for
this and will flag positions that need to be closed or rolled before
expiration week. Short gamma near expiration is one of the most common ways
traders blow up.

### Why Theta Must Be Positive

For premium-selling strategies (the core of ThetaRoom), time decay is your
edge. Every day that passes, your short options lose value. If portfolio
theta is negative, you are paying for time decay instead of collecting it.
A negative theta portfolio means you have drifted from the strategy.

---

## Correlation Risk

Position limits alone are not sufficient. Five 2% positions in AAPL, MSFT,
GOOGL, META, and AMZN look like 10% total risk. But these stocks are
correlated at 0.7+ during selloffs. In a tech crash, all five move together,
and your real risk is closer to 8-10% on a single factor (mega-cap tech).

### Correlation Rules

```
- Max 3 positions in same sector
- Max 2 positions in same industry group
- If correlation > 0.75 between two holdings, treat them as one position
  for risk calculation purposes
- Run correlation check weekly (correlations shift over time)
```

### Why Correlations Spike in Crises

During normal markets, stocks have moderate correlations based on their
individual fundamentals. During panics, correlations converge toward 1.0
because all stocks become "risk assets" and get sold together. Your
diversification benefit disappears exactly when you need it most. This is
why the drawdown rules below apply to total portfolio, not per-position.

---

## Drawdown Management

A predefined, mechanical drawdown protocol removes emotion from the worst
moments.

### The Escalation Ladder

| Drawdown Level | Action | Rationale |
|---------------|--------|-----------|
| **0-3%** | Normal trading, no changes | Normal fluctuation |
| **3-5%** | Review all positions, tighten stops | Early warning, increase attention |
| **5%** | Reduce all position sizes by 50% | Capital preservation mode |
| **8%** | Halt all trading, close discretionary positions | Circuit breaker engaged |
| **Recovery** | Start at 25% normal size, scale up over 2-4 weeks | Rebuild confidence and capital gradually |

### Why 5% Triggers Size Reduction

At 5% drawdown, you need a 5.3% gain to recover. Still easy. But if you
maintain full size and the drawdown continues to 15%, you now need 17.6%
to recover. The 50% size reduction at 5% limits your worst case: even if
you keep losing at half size, reaching 8% halt takes twice as many losing
trades, giving you more time to recognize the problem.

### Recovery Protocol

After a halt, the temptation is to "get it all back." This is the most
dangerous moment. The recovery protocol forces gradual re-entry:

```
Week 1: 25% normal position size
Week 2: 50% normal position size (if profitable)
Week 3: 75% normal position size (if still profitable)
Week 4: 100% normal position size (if cumulative recovery is positive)

If any week is negative, stay at that size level for another week.
```

---

## Smart Order Execution

How you enter a trade matters. In options, bid-ask spreads are wide enough
that sloppy execution costs more than most people realize.

### Fill Improvement Protocol (from ThetaRoom)

```
Step 1: Place limit order at midpoint of bid-ask
Step 2: Wait 120 seconds
Step 3: If not filled, move 0.05 toward the natural side
Step 4: Wait 120 seconds
Step 5: If not filled, move another 0.05 toward natural side
Step 6: If not filled after 3 attempts, cancel and reassess

fill_improvement_step = 0.05
max_fill_attempts = 3
```

### Why Never Market-Order Options

Options spreads are wide. A stock with a $0.01 spread might have options
with a $0.20 spread. If you market-order, you give up that entire spread.
On a $2.00 option with a $0.20 spread, that is 10% of the option's value
lost on entry. Multiply that across hundreds of trades and it destroys
your edge.

The fill improvement protocol typically gets fills within $0.05-$0.10 of
midpoint. On the same $2.00 option, that is 2.5-5% instead of 10%.

---

## Risk Per Strategy Type

Different strategies have different risk profiles. Size accordingly.

| Strategy | Max Risk Per Trade | Why |
|----------|-------------------|-----|
| **Defined risk** (verticals, iron condors, butterflies) | 2-3% of account | Loss is capped at spread width minus credit. You know your max loss at entry. |
| **Undefined risk** (naked puts, naked calls, strangles) | 1-2% of account | Tail risk exists. A 3-sigma move can produce losses far exceeding expected. |
| **Concentrated stock** (single equity position) | 5% of account | Less leverage than options but single-name risk (fraud, earnings disaster). |

### Why Defined Risk Gets More Allocation

When you sell a put credit spread, your maximum loss is the width of the
spread minus the credit received. You know this number before you enter. This
certainty allows larger position sizes because there are no surprises.

When you sell a naked put, your maximum loss is the strike price times 100
(the stock goes to zero). While unlikely, tail events happen. The smaller
allocation accounts for this unbounded downside.

---

## Regime-Based Risk Adjustment

Position sizing should not be static. Market conditions change, and your
risk parameters should adapt. ThetaRoom uses the Markov regime detector
to scale position sizes.

| Regime | VIX Range | Position Size Adjustment | Rationale |
|--------|-----------|------------------------|-----------|
| **Bull Quiet** | VIX < 18 | 100% (full size) | Low vol, trending market, conditions favor premium selling |
| **Bull Volatile** | VIX 18-25 | 75% (reduce by 25%) | Trend intact but choppier, wider swings can hit stops |
| **Distribution / Bear** | VIX 25-35 | 50% (reduce by 50%) | Elevated risk of trend change, protect capital |
| **Crisis** | VIX > 35 | Halt or hedges only | Capital preservation is the only goal |

### Why VIX Thresholds

VIX is not a perfect regime indicator, but it is the most responsive.
When VIX spikes above 35, historical data shows that average daily moves
in the S&P 500 triple compared to a VIX of 15. Your position sizing
model, backtested at VIX 15, will massively underestimate risk at VIX 35.
Scaling down proportionally keeps your actual dollar risk roughly constant
across regimes.

### How Regime Adjustment Stacks with Other Rules

Regime adjustment modifies the base position size before other checks:

```python
base_size = half_kelly_size(win_rate, avg_win, avg_loss)
regime_adjusted = base_size * regime_multiplier  # 1.0, 0.75, 0.50, or 0.0
final_size = min(regime_adjusted, max_per_trade_risk)  # Never exceed 2%

# Then check portfolio-level gates:
if portfolio_risk + final_size > max_portfolio_risk:
    final_size = max_portfolio_risk - portfolio_risk  # Cap at remaining budget
    if final_size <= 0:
        reject_trade("Portfolio risk budget exhausted")
```

This layered approach ensures that no single rule can be circumvented. Even
if Kelly says 5% and regime says full size, the 2% per-trade cap prevents
oversizing. Every layer is a safety net for the layers above it.

---

## Strategy-Aware Risk Classification (from ThetaRoom v1)
Source: `theta-room/backend/services/risk/strategy_aware_risk_manager.py`

| Strategy Type | Max Position % | Stop Loss | Hold Period | Special Rules |
|--------------|:---:|:---:|:---:|------|
| Day Trade | 5% | 1% of account | Intraday only | Fail-safe closure at 3:59 PM |
| Swing | 3% | 2% of account | 2-10 days | Overnight gap risk check |
| Momentum | 4% | 1.5% | 1-5 days | Requires trend confirmation |
| Gap Play | 2% | 0.5% | Intraday | Pre-market liquidity check |
| Earnings | 2% | Defined risk (spreads) | Through event | IV crush expected |

---

## Fail-Safe Closure System (from ThetaRoom v1)
Source: `theta-room/backend/services/risk/failsafe_closure_system.py`

Multi-stage position closure to prevent unintended overnight exposure:

```
3:30 PM ET -> WARNING: Review all day-trade positions
3:45 PM ET -> ALERT: Close positions > 50% of day-trade allocation
3:55 PM ET -> URGENT: Close ALL day-trade positions at market
3:59:30 PM -> PANIC: Emergency market orders for anything remaining
```

**Why:** Day trade positions held overnight violate the strategy classification AND incur overnight gap risk. The multi-stage approach gives you time to close cleanly at limit prices before resorting to market orders.

---

## Account Isolation (from ThetaRoom v2)
Source: `thetaroom/thetaroom/config.py`

| Account | Access Level | Trading | Notes |
|---------|:---:|:---:|------|
| Personal IBKR | FULL | Paper (default) / Live | All strategies allowed |
| Roth IRA | READ-ONLY | Reference only | No options selling, no margin |

**Non-negotiable:** Roth IRA signals are dropped at the strategy acceptance layer. Even if analysis suggests a trade, the account gate prevents execution.

---

## Anomaly-Adjusted Risk Multipliers (from SwaggyStacks)
Source: `swaggy-stacks/backend/app/trading/risk_manager.py`

| Threat Level | Risk Multiplier | Position Size Adjustment |
|:---:|:---:|------|
| Normal | 1.0x | Standard sizing |
| Elevated | 1.5x | Widen stops 50%, reduce size 33% |
| High | 2.0x | Double stops, halve position size |

Triggered by: VIX spike > 25%, unusual options flow divergence, exchange outflow anomaly, or multiple methodology disagreement.
