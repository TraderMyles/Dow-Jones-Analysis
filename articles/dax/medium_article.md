# I Ran a Ten-Year Seasonality Study on the DAX 40. The Calendar Has Opinions — But Not the Ones You'd Trade On.

*Day-of-week returns, monthly patterns, and what happens when you actually try to trade the "best" day.*

---

There's a persistent belief in trading circles that certain days and months are just better for stocks — "sell in May," Monday blues, a strong Santa Claus rally. I wanted to know whether any of that shows up in the numbers for Germany's benchmark index, so I pulled ten years of daily price data for the DAX 40 (^GDAXI) — July 2016 through July 2026, 2,538 trading days — and broke it down by weekday and by calendar month.

The patterns are real. Whether they're tradeable is a different question, and the answer surprised me.

---

## Part 1: The DAX Has a Favourite Day — Tuesday

Ranked by average close-to-close return over the full ten years:

1. **Tuesday**: +0.1074%, 54.4% win rate (511 sessions)
2. **Wednesday**: +0.1064%, 55.3% win rate (512 sessions)
3. **Monday**: +0.0429%, 50.6% win rate (496 sessions)
4. **Friday**: -0.0015%, 52.5% win rate (505 sessions)
5. **Thursday**: -0.0404%, 52.1% win rate (514 sessions) — the worst day of the week

Tuesday and Wednesday are essentially tied at the top, and both comfortably ahead of the rest of the week. Thursday is the quiet underperformer — not a crash-day, just a session that has consistently drifted negative for a decade.

This lines up loosely with a pattern seen in other developed markets: early-to-mid week strength, late-week fade. Nothing shocking here.

## Part 2: April Is the DAX's Best Month, March Is Its Worst

Ranked by average daily return within each calendar month:

1. **April**: +0.1461% avg, 57.1% win rate
2. **November**: +0.1402% avg, 55.8% win rate
3. **January**: +0.0948% avg, 56.9% win rate
4. **May**: +0.0905% avg, 54.7% win rate
5. **December**: +0.0703% avg, 50.8% win rate
...
12. **March**: -0.0485% avg, 53.0% win rate — the worst month

April edges out the classic "Santa Claus rally" months (November, January) as the single best-performing month over the decade. March, meanwhile, is dragged down hard by one data point: **March 2020, -16.4%**, the COVID crash. Strip that one month out and March looks a lot more ordinary — a reminder that ten years of monthly data is really only ten observations per month, and a single tail event can swing the ranking.

## Part 3: Trading the "Best Day" Loses Money

This is the part that should give anyone pause before building a calendar-based strategy.

I tested a mechanical strategy: buy the DAX at the open and sell at the close, every single Tuesday, for ten years. Tuesday has the best average daily return of any weekday. Surely that translates into a profitable strategy?

**It returned -8.00%** over ten years, despite a 54.4% win rate on individual trades — badly trailing buy-and-hold's **+153.22%**.

How does a strategy with a positive average return and a win rate above 54% lose money overall? Compounding punishes variance. A small number of sharply negative Tuesdays (the standard deviation on Tuesday returns is over 1.1%) outweigh the accumulated edge from many small winning days, especially with no risk management and full capital exposure on every single trade — 511 of them. The "best day" is a statistical artifact of the *average*, not a reliable, repeatable source of profit once you actually put capital behind it every week for a decade.

## Part 4: The Best-Month Strategy Fares Better, But Still Loses to Buy-and-Hold

Buying the DAX at the open of the first trading day of April and selling at the close of the last trading day of April, every year for ten years, returned **+29.06%** with an **80% win rate** across 10 trades — a much cleaner result than the Tuesday strategy, since it trades ten times instead of five hundred.

But it's still nowhere close to buy-and-hold's +153.22%. Being invested for one month a year, even the *best* month, means missing the other eleven — including whatever compounding the index does the rest of the time.

---

## What This Actually Tells You

The honest takeaway is uncomfortable for anyone hoping to find a calendar-based edge: **the DAX does show real day-of-week and month-of-year patterns, but neither survives contact with an actual trading strategy.**

**If you're curious about market structure**, the Tuesday/Wednesday strength and Thursday weakness are persistent enough over ten years to be more than noise. Same with April and November as historically strong months.

**If you're looking for something to trade**, this isn't it. The best single day of the week, traded mechanically for a decade, lost money. The best single month beat nothing except being fully out of the market.

**Buy-and-hold on the DAX 40 returned +153.22%** over this ten-year window — comfortably ahead of every calendar-timing variant tested here. Seasonality is a real, measurable feature of the data. It is not, on its own, a strategy.

---

*All data via yfinance, ^GDAXI daily OHLC, July 2016 – July 2026. Long only, $10,000 starting capital, no transaction costs. Past performance does not predict future results.*
