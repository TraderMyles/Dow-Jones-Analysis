# The DAX's Best Trading Day Loses Money. Here's the Data.

*A ten-year seasonality study on Germany's benchmark index — and why "the best day" and "the best day to trade" turn out to be two very different things.*

---

I want to show you a result that initially looked like a bug.

I pulled ten years of daily price data for the DAX 40 (^GDAXI) — July 2016 through July 2026 — and broke it down by weekday and calendar month, then built mechanical strategies around whatever came out on top. The seasonality is real. The strategy built on top of it is not what you'd expect.

---

## Tuesday Is the DAX's Best Day. Trading It Loses 8%.

Ranked by average close-to-close return, Tuesday comes out on top: **+0.1074% average, 54.4% win rate, across 511 sessions over ten years**. Wednesday is right behind it at +0.1064%. Both comfortably beat the rest of the week.

So I tested the obvious idea: buy the open, sell the close, every Tuesday, for ten years.

**Result: -8.00%.** Not a typo. A strategy built on the single best-performing day of the week, with a win rate above 54%, lost money over a decade — while buy-and-hold returned **+153.22%** over the same period.

Here's why. Average return and compounded return are not the same thing when you're taking on full exposure 511 separate times. Tuesday's daily standard deviation is over 1.1% — wider than its average edge by a factor of ten. A handful of genuinely bad Tuesdays (there will always be a handful, over 511 of them) erase years of small, grinding wins. This is the same mechanism that turns "72% of days are green" into "the fund lost 30% this year" — variance eats averages alive when you compound through it with no risk management.

**The lesson**: a positive average and a win rate above 50% tell you almost nothing about whether a mechanical strategy built on it will make money. You have to actually run the compounding.

---

## Thursday Is the Quiet Loser

While everyone talks about Monday blues, the data says Thursday is where the DAX actually struggles: **-0.0404% average, the only clearly negative day of the week**, with a below-average win rate of 52.1%. Monday, despite its reputation, comes in third at a modestly positive +0.0429%.

Nothing dramatic here — no single Thursday crash driving the number — just a decade of quiet underperformance on one specific day. Structurally unglamorous, but persistent.

---

## April Beats the Santa Claus Rally

Calendar folklore says December and January are the strong months. The data says otherwise for the DAX: **April is the strongest month of the year**, averaging +0.1461% per day with a 57.1% win rate — ahead of November (+0.1402%) and January (+0.0948%).

March is the worst month on the list, at -0.0485% average. But that number is doing a lot of work off the back of one event: **March 2020 alone was -16.4%**, the COVID crash. Ten years of monthly data means ten observations per month — one outlier can drag a whole month's ranking down. Treat single-month rankings from a ten-year sample with real skepticism; they're thinner than they look.

---

## The Best-Month Strategy Actually Works Better — But Still Loses to Doing Nothing

Buying the open on day one of April and selling the close on the last day of April, every year for ten years, returned **+29.06% with an 80% win rate across just 10 trades**. That's a much healthier result than the Tuesday strategy — fewer trades means less exposure to the variance problem that sank it.

But 29% over a decade, against buy-and-hold's 153%, tells you the real cost of a calendar-timing strategy: you're paying for the other eleven months of compounding you didn't participate in, and no single "best month" makes up for that.

---

## What Actually Holds Up

1. **The patterns are statistically real, not noise** — Tuesday/Wednesday strength, Thursday weakness, and an April/November seasonal tilt all persist consistently across ten years of daily data on a major index.

2. **Average return does not equal tradeable edge.** The Tuesday strategy is the cleanest demonstration I've seen of why: a 54% win rate and a positive mean return produced a losing decade-long strategy once you actually compound through 511 trades.

3. **Fewer, well-timed trades beat frequent small-edge trades.** The 10-trade April strategy meaningfully outperformed the 511-trade Tuesday strategy, despite Tuesday having the better "average" statistic on paper.

4. **Nothing tested here beats simply holding the index.** Buy-and-hold's +153.22% over ten years dwarfs every calendar-based variant. Seasonality is a real feature of how the DAX trades. It is not, by itself, a reason to time your entries and exits around it.

---

*All data via yfinance, ^GDAXI daily OHLC, July 2016 – July 2026. Long only, $10,000 starting capital, no transaction costs. Past performance does not predict future results.*
