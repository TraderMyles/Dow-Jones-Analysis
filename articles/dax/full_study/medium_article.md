# I Backtested Every Classic Trading Strategy on the DAX 40. Here's What Germany's Index Actually Does Differently From the Dow.

*Five years of price data, 40 stocks, quarterly earnings, and four German/Eurozone macro events — plus one result the Dow study never produced.*

---

I ran the same systematic backtest I'd already run on the Dow Jones — moving average crossovers, all index components, earnings announcements, and macroeconomic events — on Germany's DAX 40. Same rules, same five-year window (July 2021 – July 2026), same $10,000 starting capital, long only, no transaction costs. The goal was simple: does the German market behave the same way, or does it break the pattern?

Mostly it confirms the pattern. But one result — a moving average strategy on an individual stock that actually beat buy-and-hold in raw dollar terms, not just risk-adjusted — never showed up anywhere in the Dow data.

---

## Part 1: Moving Averages on the DAX Index — Same Story as the Dow

I tested the same five crossover pairs (9/21, 20/50, 50/200, 9/50, 21/200) for both SMA and EMA against buy-and-hold on ^GDAXI.

**No strategy beat buy-and-hold.** The index returned +61.8% over the period. The best MA strategy, SMA(50,200), returned +50.2%. SMA(21,200) was close behind at +45.5%.

Look at the drawdown column, though. Buy-and-hold's maximum drawdown was -26.4%. SMA(50,200) and SMA(21,200) both capped their drawdown at -16.0% — roughly 40% shallower — while making only 3 trades each across five years.

The fast crossover, EMA(9,21), returned +27.1% with -15.5% max drawdown across 31 trades — less than half the return of the slow strategies, for ten times the trading activity.

**Same conclusion as the Dow**: slower crossovers act as risk managers, not alpha generators. The 200-day pairs sidestep sustained drawdowns (2022's rate-hiking selloff shows up clearly — every strategy in the table posted a negative or flat 2022 except the two 200-day pairs, which were essentially flat) at the cost of underperforming in strong bull years.

## Part 2: The Same Strategies on All 40 Components — Where the DAX Diverges From the Dow

This is where it gets interesting. Running the identical strategies on each of the 40 DAX components, the average buy-and-hold return was **+101.1%** over five years — pulled up by one stock in a way that will feel familiar to anyone who read the Dow version of this study, except the driver here is completely different.

**Rheinmetall (RHM.DE)** returned **+1,199% buy-and-hold** over five years — Germany's defense-sector re-rating following 2022. That alone is remarkable. What's more remarkable: the **EMA(50,200) strategy on Rheinmetall returned +1,724%** — beating its own buy-and-hold benchmark, in raw dollar terms, with just two trades.

That doesn't happen in the Dow study. Every MA strategy there underperformed its buy-and-hold benchmark, on the index and (on average) across the 30 components. Here, a long-only, no-leverage, two-trade strategy actually out-earned holding the stock continuously. The mechanism is straightforward once you see it: the 200-day signal kept the strategy out of Rheinmetall during a sharp intermediate drawdown, then re-entered before the next leg of the rally. Skipping a large percentage decline and then compounding the subsequent recovery from a lower entry point can mathematically produce a higher total return than never leaving the position — no leverage required, just correct timing around one big drawdown.

Siemens Energy (ENR.DE) shows the same pattern at smaller scale: SMA(21,200) returned +855.5% against a buy-and-hold of +585.4%.

Across the full 40-stock universe, SMA(50,200) had the highest beat-rate against buy-and-hold — **50% of stocks** — meaning half the time, this single slow crossover matched or beat simply holding the stock. That's a meaningfully higher hit rate than the Dow study's best crossover (27%).

**The takeaway**: on stocks with one dominant, trend-driven re-rating — Rheinmetall and Siemens Energy both rode Europe's 2022–2025 defense and energy-transition themes — a 200-day filter doesn't just protect you on the way down, it can outright beat the stock's own buy-and-hold return.

## Part 3: Earnings Effect — PEAD Confirmed, Right Down to the Sector

For each of the 40 DAX stocks, I tracked quarterly earnings dates and tested five windows around each announcement, exactly as in the Dow study.

The announcement window itself — one day before to one day after — returned just **+1.3%** over five years with a **52.3% win rate**. A coin flip, same as the Dow.

**PEAD (Post-Earnings Announcement Drift)** shows up clearly: entering the day after earnings and holding 20 trading days returned **+19.9% compounded** across all 40 stocks, with a **53.5% win rate** — a per-event average of +0.88%. Notably, PEAD-Long had the highest beat-rate against buy-and-hold of any window (35%), and the Full window [-5,+5] beat buy-and-hold on **38%** of stocks — again a modestly stronger showing than the equivalent Dow numbers.

The strongest individual combination: **Siemens Energy, Full window, +147.6%** with a 65% win rate. Infineon's Full window returned +136.3% at a 70% win rate. Commerzbank's Full window: +96.3% at 73.7% win rate — the highest win rate of any top-10 combination in the dataset.

Just as in the Dow study, the financials and industrials with heavy forward guidance (Commerzbank, Infineon, Rheinmetall) show the cleanest drift — support for the idea that PEAD is strongest where post-earnings guidance takes longer for the market to fully digest.

## Part 4: The German Macro Calendar — ECB, CPI, Unemployment, GDP

I replaced the US CPI/NFP/GDP/FOMC calendar with its direct German and Eurozone equivalents: **German CPI flash estimates** (Destatis), **German unemployment reports** (Bundesagentur für Arbeit — the closest thing Germany has to a Non-Farm Payrolls moment), **German GDP flash estimates** (Destatis), and **ECB Governing Council rate decisions**.

The pattern from the Dow study repeats almost exactly: **post-event drift dominates, announcement-day reaction is noise or worse.**

- **ECB Post-Long** (entering the day after a rate decision, holding 10 days): **+29.5%** over 40 events, 60% win rate.
- **ECB Day-of** [-1,+1]: **-4.2%**, 57.5% win rate — the announcement window is actually the worst-performing ECB strategy, dragged down hard by 2022's hawkish pivot (-11.1% in that single year).
- **German Unemployment Post-Long**: **+38.8%**, 58.3% win rate — the strongest single macro strategy in the entire study, on par with the Dow's post-FOMC result.
- **German GDP Post-Long**: **+29.0%**, **70% win rate** — the highest win rate of any macro window, on only 20 events.
- **German CPI Post-Long**: **+36.5%**, 60% win rate.

Every single one of the four event types shows the same shape: the Post-Long [T+1, T+10] window is the best-performing window, by a wide margin, in every category. The Day-of window is the weakest or negative in three of the four (ECB, CPI, Unemployment all show a negative or barely-positive day-of return). This is the single cleanest confirmation across the whole DAX study that the Dow's central finding — markets process scheduled information over the following days and weeks, not on the day itself — travels intact across the Atlantic.

---

## What This Actually Tells You

**The core lesson repeats**: moving averages are risk managers, not return generators; post-event drift (earnings, ECB, macro data) is where the real, persistent edge lives; and the announcement moment itself is close to noise.

**But the DAX adds one genuinely new data point**: on stocks undergoing a structural, multi-year re-rating — Rheinmetall's defense-spending story, Siemens Energy's grid/renewables recovery — a slow moving average crossover doesn't just reduce your drawdown, it can beat buy-and-hold outright, because avoiding one severe intermediate crash and re-entering before the next leg up is worth more, compounded, than continuous exposure. That never happened anywhere in the Dow's 30 stocks over the same window. It's a reminder that "moving averages don't beat buy-and-hold" is a statement about *typical* stocks, not *all* stocks — the exceptions cluster exactly where you'd expect: violent, single-theme re-ratings with a sharp intermediate drawdown baked in.

None of this is investment advice. Five years covers one bull market, one bear market, and one geopolitically driven sector rotation — it is not enough data to declare any of this permanent. But the parts that repeat across two entirely different markets, indices, and currencies (post-event drift, MA-as-risk-manager) are the parts worth taking seriously.

---

*All backtests conducted on ^GDAXI and 40 DAX component stocks using five years of price data via yfinance, July 2021 – July 2026. Long only, $10,000 starting capital, no transaction costs. Event dates sourced from ECB, Destatis, and Bundesagentur für Arbeit official release calendars.*
