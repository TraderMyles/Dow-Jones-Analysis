# The Fed Just Handed You 40 Free Trades. Most People Ignored All of Them.

*A systematic look at what actually moves the Dow — and what the consensus has completely wrong.*

---

I want to show you something that bothered me.

I ran a full systematic backtest on the Dow Jones Industrial Average and all 30 of its component stocks. Moving averages, earnings windows, macro event reactions — the works. Five years of data, roughly 1,200 individual backtests.

Most of what I found confirmed what you'd expect. But a few results were sharp enough that I've been thinking about them since. Let me start with the one that matters most.

---

## The Fed Meeting No One Is Trading Correctly

Here is a fact: over the last five years, buying ^DJI the day after a Federal Reserve rate decision and holding for ten trading days has returned **+37.7%** compounded. That's 40 FOMC events. Win rate: **70%**.

Buy-and-hold on the Dow over the same period returned +46.5%. The post-FOMC strategy was in the market for roughly 400 of the 1,254 available trading days — about a third of the time — and came within 9 percentage points of matching full exposure.

The financial media covers every FOMC meeting as a binary event. Will they hike? Will they cut? What did Powell's eyebrows do? And almost all of that energy is concentrated on the decision day itself.

But the day-of window — entering one day before, exiting one day after the announcement — returned just +1.2% over five years. Fifty percent win rate. Noise.

**The market processes FOMC decisions in the ten days that follow, not in the two days that surround them.** The knee-jerk reaction is mean-reverting. The drift that follows is where the actual signal is.

Why might this be? My best guess: institutional positioning. Large funds don't rotate their books overnight in response to a rate decision. The realignment happens over the following week or two as the new rate environment gets priced into bonds, then sectors, then individual equities. The Dow picks up the tail of that repositioning.

---

## The NFP Trade Everyone Is Getting Backwards

Non-Farm Payrolls is the most-watched economic release in the world. The two days before each jobs report are a ritual of positioning, guessing, and whisper numbers.

I tested what happens if you simply own the Dow in those two days.

**-15.3% over five years. 35% win rate.**

That's the worst result in the entire study — worse than any moving average combination, worse than any earnings window, worse than anything. The market doesn't just underperform before NFP; it actively sells off heading into the number. Systematically. Month after month.

The post-NFP window tells a completely different story. Buy the day after the jobs report, hold three days: **+27.6%, 56.7% win rate**. The best short-duration macro strategy in the data.

The pattern is coherent: uncertainty compresses prices ahead of the number. Relief (or at least resolution of uncertainty) lifts them after. Pre-NFP isn't a zone of informed positioning — it's a zone of defensive de-risking. Knowing that is worth something.

---

## On Moving Averages: They're Doing One Thing Very Well, and It's Not What You Think

The trading forums will tell you moving average crossovers are dead. The quantitative finance Twitter crowd will tell you they've never worked. The data says something more nuanced.

On the Dow index, the SMA(21,200) — buy when the 21-day crosses above the 200-day, sell when it crosses below — returned **+30.6%** against buy-and-hold's +46.5%. Underwhelming.

But it made **four trades in five years** and had a max drawdown of **-10.0%**, compared to buy-and-hold's -21.9%.

The MA crossover is not an alpha-generating machine. It never was. It's a drawdown manager that costs you approximately 15-20% of return in exchange for cutting your worst losses roughly in half. Whether that trade-off makes sense depends entirely on your risk tolerance — but framing it as "does it beat buy-and-hold?" is the wrong question. For a retiree or a capital-preservation account, giving up 16 points of return to halve your maximum loss is a rational decision.

The fast crossovers (9/21, 9/50) are worse on both dimensions — more churn, similar drawdowns. **If you're going to use moving averages at all, go slow.** The 200-day is doing real work. The 9-day is just making noise.

---

## The Earnings Effect Everyone Knows About — But Still Gets Wrong

Post-Earnings Announcement Drift has been documented in academic literature since the 1980s. The idea: stocks continue drifting in the direction of an earnings surprise for weeks after the print.

Does it still exist in Dow components? **Yes, and it's meaningful.**

Buying one day after earnings and holding twenty trading days returned an average of **+23.4%** across the 30 Dow stocks over five years. Win rate: 57.1%. Per-event average: +1.19%.

The announcement window itself (one day before to one day after) returned +3.2% with a 51.7% win rate — a coin flip with a slight upward drift. If you're holding a stock over earnings for the reaction, you're not trading PEAD. You're gambling.

Goldman Sachs is the standout: PEAD-Long returned +158.7% with a 70% win rate. JPMorgan: +82.6%, 75% win rate. The DJIA's financial heavyweights show the strongest post-earnings drift — possibly because their earnings contain forward guidance that takes time for analysts to fully reprice.

---

## The One Result That Should Change How You Think About CPI

CPI releases drove more market commentary from 2022 to 2024 than any other data point. Inflation. Rate expectations. Fed pivot. Every month felt like a market-moving event.

The day-of CPI window — own the Dow over the release day — returned **+0.1% over sixty events**. Win rate: 51.7%.

Sixty months of the most consequential inflation data in forty years. Net result: flat.

The CPI pre-drift window is actually the best CPI strategy: buying two days before and exiting one day before the release returned +20.0% with a 58.3% win rate. Something is happening in the pre-CPI period — possibly positioning from traders who think they can read the whisper numbers, or systematic funds that go risk-on ahead of scheduled events regardless of the content.

The release itself? Just noise.

---

## What This Adds Up To

There are four things I'd take away from this data:

1. **Post-event drift is real and consistent** — the clearest signals are in the ten days after FOMC, the days after NFP, and the twenty days after earnings. Markets underprice the follow-through.

2. **Pre-event positioning destroys value** — especially ahead of NFP. The consensus trade before scheduled uncertainty tends to be the wrong trade.

3. **Slow moving averages earn their keep as risk managers**, not alpha generators. The SMA(21,200) is a bear market filter with a modest cost in good times.

4. **The announcement itself is priced in almost immediately** — whether it's CPI, earnings, or FOMC. If you're trading the reaction, you're arriving at the party after the band has left.

The Dow doesn't reward people who react to news. It rewards people who understand what happens after everyone else has finished reacting.

---

*All data from yfinance. Five-year backtest on ^DJI and 30 DJIA component stocks, June 2021 — May 2026. Long only, $10,000 starting capital, no transaction costs. Past performance does not predict future results.*
