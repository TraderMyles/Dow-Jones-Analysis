# I Backtested Every Classic Trading Strategy on the Dow Jones. Here's What the Data Actually Says.

*Five years of price data, 30 stocks, four event types, and one uncomfortable conclusion about buy-and-hold.*

---

There's a version of this article where I tell you I found a secret strategy that beats the market. This isn't that article.

What I actually found is more interesting — and more useful — than another "I found the holy grail" story. I ran a systematic backtest across the Dow Jones Industrial Average: every major moving average crossover pair, all 30 component stocks, earnings announcements, and four macroeconomic event types (CPI, NFP, GDP, and FOMC). Five years of data, over a thousand individual backtests. Here's what came back.

---

## Part 1: Moving Averages on the Dow — The Boring Truth

The first thing I tested was the simplest category: moving average crossover strategies on the DJIA index itself. The rule is classical — buy when the short moving average crosses above the long one, sell when it crosses below. Long only, no shorting.

I tested five crossover pairs (9/21, 20/50, 50/200, 9/50, 21/200) for both SMA and EMA — ten strategies in total — against a five-year buy-and-hold benchmark on ^DJI from mid-2021 through May 2026.

The headline result: **no strategy beat buy-and-hold**. The index returned +46.5% over the period. The best MA strategy, SMA(21,200), returned +30.6%. That's a 16-percentage-point gap over five years.

So it's game over for moving averages? Not quite.

Look at the drawdown column. Buy-and-hold had a maximum drawdown of -21.9% — nearly a quarter of your portfolio gone at the worst point. SMA(21,200)? Just -10.0%. That's less than half the pain, for a strategy that only made four trades in five years.

The EMA(9,21) — a much faster, more reactive strategy — returned +25.6% with a -15.2% max drawdown and made 22 trades. It captured less upside than the slow crossovers and generated far more transaction noise.

**The pattern is clear**: the slower the crossover, the better the risk-adjusted return. The 50/200 and 21/200 combinations are doing something real — they're keeping you in the market during sustained trends and pulling you out during major bear markets. They just can't keep up with a ripping bull run.

---

## Part 2: The Same Strategies on 30 Individual Stocks — A Different Story

Running the same strategies on each of the 30 Dow components individually produced a dramatically different picture — mostly because of one stock.

Across all 30 stocks, the average buy-and-hold return was **+106.3%** over five years. That number is pulled skyward by NVIDIA, which added over 1,800% during this period. The EMA(21,200) averaged +60.6% across the universe — still a significant underperformance.

But here's what's interesting: the slow 200-day crossover strategies consistently had the highest beat rate against buy-and-hold. SMA(50,200) and SMA(21,200) both beat buy-and-hold on **27% of stocks** — the highest hit rate of any strategy. And the individual cases are striking. NVDA combined with EMA(21,200) returned +991% (versus the stock's +1,800% buy-and-hold), which means the strategy captured more than half the monster move while sidestepping the violent corrections along the way.

Goldman Sachs with EMA(21,200) returned +246%, versus its buy-and-hold of +193%. The strategy actually won there.

The broader lesson: on stocks with persistent, trending moves, slow long-period crossovers tend to capture most of the upside while meaningfully reducing drawdowns. On stocks that chop sideways or reverse sharply, they underperform. The 200-day MA is essentially a momentum filter — it keeps you in the winners and gets you out of the losers, eventually.

---

## Part 3: What Actually Happens Around Earnings

For each of the 30 Dow stocks, I tracked every quarterly earnings date and tested five trading windows — from the pre-earnings drift period through twenty days post-announcement.

The weakest result: the announcement window itself. Entering one day before the earnings print and exiting one day after returned an average of just +3.2% over five years, with a **win rate of 51.7%** — essentially a coin flip. If you've been holding a stock over earnings hoping for a positive reaction, the data suggests you're mostly getting lucky.

The strongest result: **PEAD** (Post-Earnings Announcement Drift). Entering the day after earnings and holding for 20 days returned an average of +23.4% compounded over five years, with a 57.1% win rate. That's 1.19% per event, averaged across 30 stocks and roughly 600 earnings events.

PEAD is one of the most documented anomalies in academic finance — the tendency for stocks to continue drifting in the direction of an earnings surprise for weeks after the announcement. The data here confirms it is alive and well in Dow components.

The best individual combo: **Goldman Sachs PEAD-Long** returned +158.7% over five years with a 70% win rate and a max drawdown of just -10.7%. JPMorgan PEAD-Long wasn't far behind at +82.6% with a 75% win rate. The financials appear to be where this effect is strongest in the Dow.

---

## Part 4: The Most Interesting Finding — What Happens After the Fed Speaks

This is the part that surprised me most.

I tested four macroeconomic event types against ^DJI — CPI releases, Non-Farm Payrolls, GDP advance estimates, and FOMC rate decisions — across five trading windows for each.

The FOMC Post-Long window (entering the day after a Fed decision, holding ten days) returned **+37.7% over five years** with a **70% win rate**. That's 40 FOMC events at +0.94% per event average, compounding to within striking distance of buy-and-hold (+46.5%) while only being in the market for roughly 400 trading days out of 1,254.

GDP Post-Long had the highest win rate of anything tested: **75%** across 20 events, with a +1.04% average per event.

Two things that didn't work at all:

**NFP Pre-window** (-15.3%, 35% win rate). The two days before Non-Farm Payrolls are the worst single strategy in the entire study. The market actively fades in the run-up to jobs data — possibly because institutional players reduce exposure ahead of uncertainty, or because crowded long positions get unwound.

**CPI Day-of** (+0.1%, 51.7% win rate). Five years of monthly CPI reactions, and the net result is essentially nothing. The inflation numbers that dominated every headline from 2022 to 2024 produced noise in both directions that largely cancelled out.

---

## What Should You Actually Do With This?

The honest answer is: use these findings to inform how you think about risk, not as a trading system to copy blindly. A few practical takeaways:

**If you're worried about drawdown** more than missing upside, the SMA(21,200) on the Dow deserves a look. Four trades in five years, half the maximum drawdown of buy-and-hold, two-thirds of the return.

**If you trade individual stocks**, the post-earnings period is more interesting than the earnings day itself. The announcement is priced in almost immediately; the drift that follows is where edge has historically existed.

**The ten days after a Fed meeting** have been consistently positive for the Dow over this period. Whether that's the market "relief rally" phenomenon or something structural is an open question, but the win rate of 70% over 40 events is hard to dismiss.

**Don't position ahead of NFP**. The data is unambiguous on this one.

None of this is investment advice, and five years is not an eternity — these patterns could change. But patterns that have a plausible behavioural or structural explanation (PEAD, post-FOMC drift) tend to be more durable than those that don't. The ones with real-world logic behind them are the ones worth watching.

---

*All backtests conducted on ^DJI and 30 DJIA component stocks using five years of price data via yfinance. Long only, $10,000 starting capital, no transaction costs. Lookback period: June 2021 — May 2026.*
