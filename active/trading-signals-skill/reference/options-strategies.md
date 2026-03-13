# Options Strategies — 25+ Playbook

Every strategy includes: what it is, when to use it, Greeks profile, max profit/loss, ideal conditions, and the reasoning behind it. Organized by intent.

---

## Income / Theta Strategies

These profit from time decay. You're the house — collecting premium and hoping price stays in your zone.

### Covered Call
**What:** Own 100 shares + sell 1 OTM call against them.
**When:** Mildly bullish, willing to cap upside for income. Works in ranging or slow-grinding markets.
**Greeks:** Positive theta, negative vega, reduced delta (shares minus short call delta).
**Max Profit:** Strike - entry price + premium received.
**Max Loss:** Share price to zero minus premium (same as owning stock, but slightly cushioned).
**Sweet Spot:** 30-45 DTE, 0.20-0.30 delta short call. Roll before 14 DTE if untested.
**Why it works:** You're selling time. The covered call converts unrealized appreciation into realized income. Works best when you'd be happy selling at the strike price anyway.

### Cash-Secured Put (CSP)
**What:** Sell 1 OTM put, secured by cash equal to 100 × strike price.
**When:** Bullish — you want to buy the stock but at a lower price. If assigned, you own shares at an effective discount.
**Greeks:** Positive theta, negative vega, positive delta.
**Max Profit:** Premium received (put expires worthless).
**Max Loss:** Strike × 100 - premium (if stock goes to zero — extremely unlikely for quality names).
**Sweet Spot:** IV rank > 30%, sell at the price you'd actually want to own shares. 30-45 DTE.
**Why it works:** Getting paid to wait for your price. If the stock drops to your strike, you buy at a discount (strike minus premium). If it doesn't, you keep the premium and try again.

### Wheel Strategy
**What:** CSP → get assigned → covered call → get called away → repeat.
**When:** On high-quality names you're happy to own. Consistent income generation.
**Greeks:** Alternating between CSP and CC Greeks profiles.
**Why it works:** Combines CSP and CC into a perpetual income engine. You're always either getting paid to wait (CSP) or getting paid to hold (CC). Works best on liquid stocks with moderate IV.

### Iron Condor
**What:** Short OTM put spread + short OTM call spread, same expiration.
**When:** Neutral — expect price to stay in a range. IV rank > 50% (selling expensive premium).
**Greeks:** Positive theta, negative vega, near-zero delta (market-neutral).
**Max Profit:** Net credit received.
**Max Loss:** Width of wider spread - net credit.
**Sweet Spot:** IV rank > 50%, 30-45 DTE, short strikes at ~16 delta (1 SD). Exit at 50% max profit.
**Why it works:** You're selling a probability — roughly 68% chance price stays within 1 SD. High IV rank means you're collecting more premium for the same probability. ThetaRoom targets 45 DTE entry, exits at 50% profit or 21 DTE (whichever first).

### Iron Butterfly
**What:** Short ATM straddle + long OTM strangle (protective wings).
**When:** Strongly neutral — expect price to pin near current level.
**Greeks:** High positive theta, high negative vega, zero delta at center.
**Max Profit:** Net credit (larger than iron condor because ATM premium is richest).
**Max Loss:** Width of wing - net credit.
**Why it works:** Maximum theta capture at ATM, but very tight profit zone. Use when you have strong conviction price will consolidate (e.g., after an earnings move has resolved).

### Credit Spreads (Bull Put / Bear Call)
**What:** Sell near OTM option + buy further OTM option (same type, same expiry).
**When:** Directional bias with defined risk. Bull put = bullish. Bear call = bearish.
**Greeks:** Positive theta, defined risk (spread width limits loss).
**Max Profit:** Net credit.
**Max Loss:** Spread width - credit.
**Sweet Spot:** 30-45 DTE, short strike at ~30 delta for directional conviction, ~16 delta for high-probability.
**Why it works:** Defined risk version of naked selling. The long option caps your loss at the spread width. You sacrifice some credit for the peace of mind.

### Short Strangle
**What:** Sell OTM put + sell OTM call, same expiration. No protective wings.
**When:** Neutral, high IV, large account (margin required). Undefined risk.
**Greeks:** High positive theta, high negative vega, near-zero delta.
**Max Profit:** Total premium collected.
**Max Loss:** Theoretically unlimited (naked call side).
**Sweet Spot:** IV rank > 60%, 45 DTE, 16-delta strikes. Requires active management.
**Why it works:** No wings means you keep all the premium. Higher reward but requires discipline — you must manage losers aggressively. Roll the tested side before it goes ITM.
**Risk warning:** Undefined risk. Never use on earnings/binary events. Size small (1-3% of account per strangle).

### Short Straddle
**What:** Sell ATM put + sell ATM call. Maximum premium, tightest profit zone.
**When:** Extremely high IV, very strong pinning conviction. Rare.
**Greeks:** Massive theta, massive negative vega, zero delta at entry.
**Why it works:** Extracts maximum time value. But the breakeven zone is narrow and undefined risk is on both sides. For experienced traders only.

### Jade Lizard
**What:** Short OTM put + short call spread (bear call credit spread). No upside risk.
**When:** Neutral to bullish. You want premium income with no risk to the upside.
**Greeks:** Positive theta, slightly positive delta, no upside risk if credit > call spread width.
**Max Profit:** Net credit received.
**Max Loss:** Strike of short put × 100 - credit (downside only).
**Why it works:** If the total credit received exceeds the width of the call spread, you have zero risk on the upside. Downside is like a CSP. It's a more elegant income trade than a plain strangle.

---

## Directional Strategies

### Debit Spreads (Bull Call / Bear Put)
**What:** Buy near ATM option + sell further OTM option. Pay a debit to enter.
**When:** Directional conviction with controlled cost. Lower IV environments preferred (buying cheap).
**Greeks:** Positive delta (bull call) or negative delta (bear put). Negative theta (you're paying time).
**Max Profit:** Spread width - debit paid.
**Max Loss:** Debit paid.
**Why it works:** Limits cost compared to buying a single option. The short leg reduces vega and theta drag. Best when you have a price target — the short strike should be at or near your target.

### Naked Puts
**What:** Sell a put with no protective long put below. Cash or margin secured.
**When:** Bullish, comfortable with assignment, high IV. Like a CSP but on margin (higher capital efficiency).
**Greeks:** Positive theta, positive delta, negative vega.
**Max Loss:** Strike × 100 - premium (stock to zero).
**Why it works:** Same as CSP conceptually, but margin lets you deploy more capital. Professional premium sellers use naked puts on indices (SPX) where assignment is cash-settled.
**Risk warning:** Undefined risk (but bounded by stock going to zero). Size conservatively.

### Naked Calls
**What:** Sell a call with no underlying shares or protective long call above.
**When:** Strongly bearish or confident price won't reach strike. Rare and risky.
**Greeks:** Negative delta, positive theta, negative vega.
**Max Loss:** Theoretically unlimited.
**Risk warning:** The most dangerous options position. A short squeeze or gap up can produce catastrophic losses. Almost never recommended. If you're bearish, use a bear call spread instead.

### PMCC (Poor Man's Covered Call)
**What:** Buy deep ITM LEAPS call (0.70+ delta) + sell short-term OTM call against it.
**When:** Bullish long-term, want covered-call-like income without owning shares. Much less capital required.
**Greeks:** Net positive delta, slightly positive theta (if short call theta > LEAPS theta drag).
**Max Profit:** Short strike - LEAPS strike - debit + credits collected.
**Max Loss:** Initial debit paid for LEAPS.
**Sweet Spot:** LEAPS at 0.70-0.80 delta (6-12 months out). Short calls at 30-45 DTE, 0.20-0.30 delta. Roll shorts every cycle.
**Why it works:** You're renting delta instead of buying shares. The LEAPS acts as a synthetic stock position at 10-20% of the capital cost. The short calls generate income that reduces your cost basis over time.

### Synthetic Long / Short
**What:** Buy ATM call + sell ATM put (synthetic long) or vice versa.
**When:** Replicating stock exposure with options. Used for leverage or when shorting is restricted.
**Greeks:** Delta ≈ +1.0 (synthetic long) or -1.0 (synthetic short). Near-zero theta if strikes match.
**Why it works:** Put-call parity guarantees this replicates the underlying. Useful for capital efficiency or accessing markets where direct stock trading is restricted.

### Risk Reversal
**What:** Sell OTM put + buy OTM call (bullish) or vice versa (bearish). Often for zero or near-zero cost.
**When:** Strong directional conviction. You fund the call by selling put premium (or vice versa).
**Greeks:** High delta in your conviction direction, variable theta (depends on strikes chosen).
**Why it works:** Zero-cost entry with directional exposure. The risk is being assigned on the short put if wrong. Institutional traders use these heavily.

### Collar
**What:** Own shares + buy OTM put + sell OTM call. Protective floor and income ceiling.
**When:** Protecting a large stock position through a risky period (earnings, macro event).
**Greeks:** Capped delta, limited downside, limited upside.
**Why it works:** Insurance. You give up some upside to eliminate downside below your put strike. Often done at near-zero cost (call premium funds the put).

---

## Volatility Strategies

### Long Straddle / Long Strangle
**What:** Buy ATM call + ATM put (straddle) or OTM call + OTM put (strangle).
**When:** Expect a big move but unsure of direction. Before earnings, FOMC, or binary events.
**Greeks:** Positive vega, positive gamma, negative theta.
**Max Profit:** Unlimited (either direction).
**Max Loss:** Total premium paid.
**Sweet Spot:** Buy when IV rank < 30% (cheap premiums). Avoid buying when IV is already high.
**Why it works:** You're buying movement. If the realized move exceeds the implied move priced into the straddle, you profit regardless of direction. The breakeven is the straddle cost added/subtracted from the strike.

### Calendar Spread (Time Spread)
**What:** Sell short-term option + buy same-strike longer-term option. Same type.
**When:** Expect near-term consolidation followed by a move. Exploits term structure steepness.
**Greeks:** Positive vega (long-dated leg dominates), positive theta (short-term leg decays faster).
**Why it works:** The short-term option decays faster than the long-term one. If price stays near the strike, the near-term option expires worthless while the long-term retains value. Also benefits from IV expansion in the back month.

### Diagonal Spread
**What:** Like a calendar but with different strikes. Combines directional bias with time spread.
**When:** You want calendar spread benefits plus directional lean.
**Greeks:** Mix of calendar and vertical spread Greeks. Adjustable by strike selection.
**Why it works:** More flexible than a pure calendar. Choosing a further OTM short strike adds directional bias while maintaining the time decay advantage.

### Gamma Scalping
**What:** Buy ATM straddle + delta-hedge continuously by trading the underlying.
**When:** You believe realized volatility will exceed implied volatility.
**Greeks:** Long gamma generates delta on moves; you sell that delta to lock in profits.
**How it works:** As price moves up, your delta goes positive (from gamma). You sell shares to flatten delta. When price moves back down, you buy shares. Each round-trip generates a small profit. The cost is theta decay on the straddle.
**Key metric:** Realized vol vs implied vol. If realized > implied, gamma scalping is profitable. SwaggyStacks implements this in `gamma_scalping_service.py`.

### Zero-DTE
**What:** Options expiring same day. Extreme gamma, near-zero extrinsic value.
**When:** Day-trading with options. High-conviction intraday moves.
**Greeks:** Explosive gamma, near-zero theta (already expired), minimal vega.
**Risk warning:** Gamma is a double-edged sword at 0 DTE. Your position can go from profitable to assignment in minutes. Size very small (0.5-1% of account max). Exit quickly — don't hold through the last hour unless you want assignment risk.

### Back Spread (Ratio)
**What:** Sell 1 ITM option + buy 2+ OTM options. Net debit or small credit.
**When:** Strongly directional with unlimited upside potential. Low IV environment.
**Greeks:** Positive vega, positive gamma on the far side. Limited risk on the near side.
**Why it works:** If the underlying makes a large move, the extra long options generate outsized returns. If it doesn't move, you lose the debit or a limited amount. It's a convexity bet.

### VIX Options Plays
**What:** Options on the VIX index itself.
**When:** Portfolio hedging, vol trading, macro events.
**Key differences:** VIX options are European-style, cash-settled, and priced off VIX futures (not spot VIX). VIX calls are the most common portfolio hedge.
**Common plays:** Long VIX calls as portfolio insurance. VIX put spreads when term structure is in steep contango. VIX call spreads before known events.
**Warning:** VIX options behave differently from equity options. Study the term structure before trading.

---

## Advanced / Multi-Leg Strategies

### Broken Wing Butterfly
**What:** Butterfly with unequal wing widths. Skews the risk/reward to one side.
**When:** Slightly directional bias with defined risk. Often placed for a credit.
**Why it works:** Eliminates risk on one side (the wider wing) while maintaining profit potential if price stays in the body zone. Popular on indices where you want a neutral-to-bullish position with no upside risk.

### Christmas Tree (Ladder)
**What:** Multiple short options at different strikes with a single long option. Creates a stepped payoff.
**When:** High IV, targeting multiple price levels for partial profits.
**Why it works:** Each short strike generates premium. If price stays below all strikes (for call tree), all expire worthless and you keep maximum premium.

### Ratio Spreads
**What:** Buy 1 option + sell 2+ options at a different strike. Creates unequal legs.
**When:** Moderate directional conviction + premium collection. Common in commodities.
**Greeks:** Variable — depends on ratio and strikes. Usually net positive theta with some undefined risk on the ratio side.
**Front ratio:** Sell more options further from money. Risk on the far side.
**Back ratio:** Buy more options further from money. Convexity play (like back spread).

### Box Spread
**What:** Bull call spread + bear put spread at the same strikes. Creates a synthetic loan.
**When:** Arbitrage — should equal the present value of strike width. Used for financing, not speculation.
**Why it matters:** If you see a box spread trading below PV, it's a risk-free return. Rarely available in liquid markets. More relevant as a concept for understanding put-call parity.

### LEAPS
**What:** Long-term options (>1 year to expiry). Calls for bullish, puts for bearish.
**When:** Long-term directional view with limited capital. Substitute for stock ownership.
**Greeks:** High delta for deep ITM LEAPS. Low theta (long-dated = slow decay). High vega.
**Sweet Spot:** Buy deep ITM (0.70-0.80 delta) for stock replacement. Buy ATM for maximum leverage.
**Why it works:** Time is on your side (relatively). A 12-month LEAPS loses much less theta per day than a 30-day option. Gives you time to be right on direction.

### Protective Put / Married Put
**What:** Own shares + buy OTM put. Insurance against downside.
**When:** Protecting unrealized gains through a risky period. Worried about a crash.
**Greeks:** Full upside participation, floored downside at put strike.
**Cost:** Premium paid for the put (often 1-3% of position value for 30-60 DTE).
**Why it works:** Sleep-at-night insurance. You keep all upside while your loss is capped at the put strike. The cost is the insurance premium. Compare to a collar if you want to reduce/eliminate the cost.

---

## Strategy Selection Framework

### By Market Outlook

| Outlook | IV Rank | Best Strategies |
|---------|---------|-----------------|
| Strongly Bullish | Low | LEAPS calls, debit spreads, PMCC |
| Strongly Bullish | High | CSP, bull put spread, risk reversal |
| Mildly Bullish | Low | Covered call, bull call spread |
| Mildly Bullish | High | CSP, jade lizard, wheel |
| Neutral | Low | Calendar spread, diagonal |
| Neutral | High | Iron condor, iron butterfly, short strangle |
| Mildly Bearish | Low | Bear put spread |
| Mildly Bearish | High | Bear call spread, naked put (on inverse) |
| Strongly Bearish | Low | Long puts, put back spread |
| Strongly Bearish | High | Bear call spread, put debit spread |
| Volatility Expansion | Low | Long straddle/strangle, back spread |
| Volatility Crush | High | Iron condor, iron butterfly, short straddle |

### By Account Size

| Account | Strategies Available | Notes |
|---------|---------------------|-------|
| < $5K | Debit spreads, CSP (low-priced), covered calls | Limited by buying power |
| $5K-$25K | All defined-risk strategies | Iron condors, credit spreads, PMCC |
| $25K-$100K | Add naked puts, strangles | Pattern day trader threshold ($25K) |
| $100K+ | All strategies including portfolio margin | Naked calls, large strangles |

### ThetaRoom v2 Risk Thresholds

```python
# From thetaroom/config.py — centralized, no magic numbers
max_portfolio_risk_pct = 0.15      # 15% max portfolio at risk
max_per_trade_risk_pct = 0.02      # 2% max per trade
max_drawdown_halt_pct = 0.08       # 8% drawdown = halt trading
min_iv_rank_entry = 20.0           # Don't sell premium below 20% IV rank
target_dte_entry = 45              # Enter at 45 DTE
min_dte_roll = 21                  # Roll/exit at 21 DTE
profit_target_pct = 0.50           # Exit at 50% max profit
stop_loss_pct = 2.0                # Exit at 2x credit received loss
```

### Zero DTE Strategy Details (from SwaggyStacks)
Source: `swaggy-stacks/backend/app/strategies/options/zero_dte_strategy.py`

```python
ZERO_DTE_CONFIG = {
    'short_delta_range': (-0.42, -0.38),    # Short strikes
    'long_delta_range': (-0.22, -0.18),     # Wing protection
    'profit_target': 0.50,                   # 50% of max profit
    'stop_loss_multiplier': 2.0,             # 2x credit received
    'iv_range': (0.15, 0.80),               # 15-80% IV
    'min_open_interest': 500,                # Liquidity requirement
    'monitoring_interval_minutes': 3,         # Check every 3 min (fast-moving!)
}
```

**Why 3-minute monitoring:** Zero DTE gamma is extreme. A 1% SPY move can turn a winning trade into max loss in minutes. The 3-minute interval catches gamma blowups before they become catastrophic.

### Wheel Strategy Two-Phase (from SwaggyStacks)
Source: `swaggy-stacks/backend/app/strategies/options/wheel_strategy.py`

**Phase 1: Cash-Secured Put**
- Delta: -0.42 to -0.18 (30-42 delta sweet spot)
- DTE: 7-35 days
- If assigned -> transition to Phase 2

**Phase 2: Covered Call**
- Delta: 0.18 to 0.42
- DTE: 7-35 days
- If called away -> back to Phase 1

**Roll Triggers:**
- Delta exceeds 0.80 -> roll to next expiry
- Profit reaches 50% -> close early
- Max position: 10% of portfolio per underlying

**Bollinger Band Enhancement:** 20-period, 2.0 std dev -- sell puts at lower band, sell calls at upper band.

### Strategy-to-Regime Factory (from SwaggyStacks options_strategy_factory.py)

| Market Regime | Recommended Strategies | Why |
|---------------|----------------------|-----|
| **High Volatility** | Long Straddle, Protective Put, Gamma Scalping | Expensive premium -> buy directional or hedge |
| **Low Volatility** | Iron Butterfly, Covered Call, Iron Condor | Cheap premium -> sell it, collect theta |
| **Bullish** | Bull Call Spread, Covered Call, Calendar Spread | Directional + income |
| **Bearish** | Bear Put Spread, Protective Put | Protection + directional profit |
| **Neutral/Ranging** | Iron Condor, Iron Butterfly, Wheel | Range-bound income collection |
