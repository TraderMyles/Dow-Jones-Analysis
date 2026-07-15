# A Two-Trade Strategy Just Beat Buy-and-Hold on a DAX Stock. Here's How That's Even Possible.

*A systematic backtest on the DAX 40 — and the one result that doesn't show up anywhere in the equivalent US study.*

---

I already ran this exact backtest on the Dow Jones: moving averages, all 30 components, earnings windows, macro events. Roughly 1,200 backtests. The headline finding there was clean and a little humbling — nothing beat buy-and-hold, ever, not on the index and not on average across the components.

So I ran the identical study on Germany's DAX 40. Same five-year window, same rules, same $10,000 starting capital. Almost everything repeated. One thing didn't, and it's worth explaining because it sounds impossible until you see the mechanism.

---

## The Strategy That Beat Buy-and-Hold (Without Leverage, Without Shorting)

Rheinmetall, the German defense contractor, returned **+1,199% buy-and-hold** over the five-year window — Europe's post-2022 defense spending re-rating, concentrated in one stock.

A simple EMA(50,200) crossover — buy when the 50-day average crosses above the 200-day, sell when it crosses below, nothing fancier than that — made exactly **two trades** on Rheinmetall over five years and returned **+1,724%**.

Let that sit for a second: a long-only strategy, no leverage, no shorting, two trades total, beat continuously holding a stock that itself went up thirteen-fold.

Here's how that's mathematically possible. Rheinmetall's five-year run wasn't a straight line — it included a sharp intermediate drawdown along the way. The 200-day moving average signal got the strategy *out* before that drawdown and back *in* before the next leg of the rally started. Because the strategy's total return is the product of only the returns during the periods it was actually invested, skipping a large percentage decline and then riding the full recovery from a lower re-entry price compounds to a higher number than never leaving the position at all. No leverage needed — just avoiding one bad stretch at the right moment.

This never happened once in the Dow study, across 30 stocks and ten years of combined MA/stock combinations tested there. It happened here because Rheinmetall's five-year chart has exactly the shape — one big elevator down, then a bigger elevator up — where this kind of timing pays off. Siemens Energy shows a smaller version of the same thing: SMA(21,200) returned +855% against a +585% buy-and-hold.

**The lesson isn't "moving averages secretly work now."** It's that the "MA strategies never beat buy-and-hold" finding from the Dow study was really a statement about *typical* large-cap stocks in a *steady* bull market. Put a moving average filter in front of a stock with one violent boom-bust-boom cycle, and the math can flip.

---

## Everything Else Repeats — Almost Exactly

**On the index itself**, nothing beat buy-and-hold. ^GDAXI returned +61.8% over five years; the best MA strategy, SMA(50,200), returned +50.2% with a max drawdown of -16.0% versus buy-and-hold's -26.4%. Same shape as the Dow: slow crossovers cut your drawdown by ~40% at the cost of some upside.

**Post-Earnings Announcement Drift is alive and well.** Buying the day after earnings and holding 20 days across all 40 DAX stocks returned +19.9% compounded with a 53.5% win rate — while the announcement window itself (one day before to one day after) returned a coin-flip +1.3% at 52.3%. Siemens Energy's full earnings window returned +147.6%; Commerzbank hit a 73.7% win rate, the highest in the study.

**The German macro calendar behaves exactly like the US one.** I swapped CPI/NFP/GDP/FOMC for their direct German and Eurozone equivalents — German CPI flash releases, German unemployment reports (the closest thing to an NFP moment), German GDP flash estimates, and ECB rate decisions. In every single case, the ten-day post-event window was the best-performing strategy, and the announcement-day window was flat or negative:

- **ECB Post-Long (T+1 to T+10)**: +29.5%, 60% win rate, 40 events
- **ECB Day-of**: **-4.2%** — the worst ECB window, dragged down by 2022's hawkish pivot
- **German unemployment Post-Long**: +38.8%, 58.3% win rate — the single strongest macro strategy in the whole study
- **German GDP Post-Long**: +29.0% at a **70% win rate**, the highest of any macro window

That's the same "markets drift after the news, not on the news" pattern from the Dow study, reproduced almost data-point-for-data-point on a different continent, in a different currency, with a different central bank.

---

## What Actually Holds Up Across Two Markets

1. **Post-event drift is the real, repeatable edge** — true for earnings on both continents, true for every macro event type tested on both continents. If there's one thing this whole exercise (Dow and DAX combined) has convinced me of, it's this.

2. **Moving averages are risk managers first.** On the index level and for the average stock, they cut drawdown substantially and give up some return. That's true in Frankfurt exactly as it's true in New York.

3. **But "average stock" hides real exceptions**, and now I have proof instead of just a theoretical argument: give a slow MA crossover a stock with one big boom-bust-boom cycle, and it can beat buy-and-hold outright. Rheinmetall and Siemens Energy are the exceptions that prove the rule — and the rule is really about *typical* price paths, not *all* price paths.

4. **The announcement moment is priced in fast, everywhere.** CPI, NFP/unemployment, GDP, FOMC/ECB, earnings — the day-of window is close to noise in every single category tested, on both the Dow and the DAX. If you're trading the reaction, you're arriving after it already happened.

---

*All data via yfinance, ^GDAXI and 40 DAX component stocks, July 2021 – July 2026. Long only, $10,000 starting capital, no transaction costs. Event dates sourced from ECB, Destatis, and Bundesagentur für Arbeit official calendars. Past performance does not predict future results.*
