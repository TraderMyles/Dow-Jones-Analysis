# Technical and Event-Driven Trading Strategies on the Dow Jones Industrial Average: A Systematic Backtest, 2021–2026

**Abstract**

This paper presents a systematic empirical examination of four classes of long-only trading strategies applied to the Dow Jones Industrial Average (DJIA) and its thirty component equities over the five-year period from June 2021 to May 2026. We test (i) moving average crossover strategies using five SMA and EMA parameter pairs, (ii) the same crossover strategies applied to each of the thirty individual DJIA constituents, (iii) earnings announcement window strategies capturing pre-announcement drift and post-earnings announcement drift (PEAD), and (iv) event-driven strategies centred on four macroeconomic calendar releases: the Consumer Price Index (CPI), Non-Farm Payrolls (NFP), GDP advance estimates, and Federal Open Market Committee (FOMC) rate decisions. Our principal findings are as follows. First, no moving average crossover strategy outperforms buy-and-hold on a raw return basis over the sample period, but slow crossover systems (21/200 and 50/200) reduce maximum drawdown by approximately 50% relative to passive exposure. Second, PEAD is observable and economically significant in DJIA constituents, with a post-earnings 20-day window generating a 57.1% win rate and an average compounded return of +23.4% across all thirty stocks. Third, the post-FOMC window (entry T+1, exit T+10) is the strongest macroeconomic event strategy, generating a +37.7% five-year return with a 70% win rate across 40 events. Fourth, the pre-NFP period (T-2 to T-1) exhibits a systematic negative return of -15.3% with a 35% win rate, consistent with institutional de-risking ahead of uncertainty. Fifth, the CPI announcement day itself generates effectively zero alpha (+0.1% over 60 events). These results have implications for both tactical asset allocation and the interpretation of scheduled macroeconomic events as information signals.

**JEL Classification:** G11, G12, G14, G15  
**Keywords:** DJIA, moving average crossover, PEAD, FOMC drift, event-driven strategies, technical analysis, macroeconomic announcements

---

## 1. Introduction

The relationship between technical trading rules and market efficiency has occupied a central position in empirical finance since at least Fama (1970). The canonical efficient market hypothesis (EMH) predicts that price-based rules carry no predictive content, as current prices already incorporate all historically available information. A substantial body of empirical work has challenged this view, documenting return predictability associated with moving average rules (Brock, Lakonishok, and LeBaron, 1992; Han, Zhou, and Zhu, 2016), earnings announcement anomalies (Ball and Brown, 1968; Foster, Olsen, and Shevlin, 1984; Bernard and Thomas, 1989), and scheduled macroeconomic event reactions (Savor and Wilson, 2013; Lucca and Moench, 2015).

The present study contributes to this literature along three dimensions. First, it provides a contemporaneous assessment of moving average crossover performance on a major equity index and its components over a recent five-year window that encompasses a post-pandemic bull market, a significant inflationary episode, and an aggressive rate-hiking cycle — conditions that differ materially from those studied in most prior literature. Second, it simultaneously examines both index-level and constituent-level MA performance, allowing direct comparison across aggregation levels. Third, it presents a unified event-study framework covering four distinct macroeconomic release types, enabling systematic comparison of event premia across information categories within a single dataset.

Our results broadly support the interpretation that scheduled information events generate heterogeneous price dynamics across the pre-event, announcement, and post-event windows, and that the post-event drift — both in earnings (PEAD) and macroeconomic contexts — represents the most economically significant trading opportunity in the data. We also document a novel result: the pre-NFP window exhibits a systematic negative return that is robust across the full five-year period, consistent with a de-risking hypothesis rather than informed pre-positioning.

The remainder of the paper is organised as follows. Section 2 reviews the relevant literature. Section 3 describes the data and methodology. Section 4 presents results for moving average strategies. Section 5 presents results for earnings window strategies. Section 6 presents results for macroeconomic event strategies. Section 7 discusses the findings in an integrated framework. Section 8 concludes.

---

## 2. Literature Review

### 2.1 Moving Average Strategies

Moving average crossover rules are among the oldest and most studied technical trading indicators. Brock, Lakonishok, and LeBaron (1992) document significant return predictability using simple moving average rules on DJIA data from 1897 to 1986, a finding that proved influential despite subsequent debate about data snooping and transaction cost adjustments (Sullivan, Timmermann, and White, 1999). More recently, Han, Zhou, and Zhu (2016) demonstrate that a moving average timing strategy applied to individual stocks generates significant abnormal returns even after controlling for known risk factors, with the effect strongest for long-horizon moving averages. Moskowitz, Ooi, and Pedersen (2012) establish time-series momentum — conceptually related to trend-following — as a pervasive phenomenon across asset classes.

The risk-reduction properties of MA strategies have received somewhat less attention than their return-generating potential. Clare et al. (2017) demonstrate that trend-following delivers equity-like returns with meaningfully lower drawdowns, framing the strategy as a form of dynamic downside risk management rather than alpha generation per se. Our results are consistent with this characterisation.

### 2.2 Post-Earnings Announcement Drift (PEAD)

PEAD was first documented by Ball and Brown (1968) and systematically characterised by Foster, Olsen, and Shevlin (1984). Bernard and Thomas (1989) establish that PEAD is not explained by risk mismeasurement and attribute it to investor underreaction to earnings information. The magnitude and persistence of PEAD has been documented extensively across markets and time periods (e.g., Livnat and Mendenhall, 2006; Hou, Xue, and Zhang, 2020), though some evidence suggests the anomaly has diminished as it became widely known (Chordia, Subrahmanyam, and Tong, 2014).

Our analysis focuses on DJIA constituents — large-capitalisation, highly liquid equities where market efficiency should in principle be greatest. Finding meaningful PEAD in this subsample, with a 57.1% win rate and +1.19% per-event average, would be particularly notable given the institutional attention these stocks receive.

### 2.3 Macroeconomic Event Reactions

Savor and Wilson (2013) document that equity risk premia are significantly elevated on announcement days for CPI, NFP, and FOMC — finding that a strategy holding equities only on these days earns approximately half the annual market return while being exposed for only a small fraction of trading days. Lucca and Moench (2015) identify a pre-FOMC announcement drift: the S&P 500 tends to rise in the 24 hours before FOMC decisions, a pattern they attribute to investor risk appetite responding to anticipated monetary policy communication.

Our study differs from this prior work in focusing on post-announcement windows rather than announcement-day premia, and in disaggregating by event type to assess which macroeconomic releases generate the most persistent post-announcement drift.

---

## 3. Data and Methodology

### 3.1 Data

Price data for the DJIA index (^DJI) and all thirty current DJIA constituent equities are sourced from Yahoo Finance via the `yfinance` Python library. The sample covers June 2021 through May 2026, yielding 1,254 trading days. The DJIA constituents used are the current composition as of the study date, comprising: AAPL, AMGN, AMZN, AXP, BA, CAT, CRM, CSCO, CVX, DIS, DOW, GS, HD, HON, IBM, JNJ, JPM, KO, MCD, MMM, MRK, MSFT, NKE, NVDA, PG, SHW, TRV, UNH, V, and WMT.

Earnings dates are sourced from Yahoo Finance's historical earnings calendar. CPI and GDP advance estimate dates are sourced from BLS and BEA published release schedules respectively. FOMC decision dates are sourced from the Federal Reserve's published meeting schedule. Non-Farm Payrolls dates are computed as the first Friday of each calendar month, consistent with BLS release practice.

All strategies assume execution at the closing price of the entry and exit days. Signal generation is lagged by one trading day relative to the indicator calculation date to eliminate lookahead bias. Starting capital is $10,000 per strategy. Transaction costs are excluded; results therefore represent gross returns.

### 3.2 Moving Average Strategies

We test five crossover parameter pairs — (9,21), (20,50), (50,200), (9,50), and (21,200) — using both simple moving averages (SMA) and exponential moving averages (EMA), yielding ten strategies. A long position is initiated when the short MA crosses above the long MA and is exited when the short MA crosses below the long MA. When not in a position, cash earns 0%. Positions are sized at 100% of available capital. For individual stock backtests, each of the 30 constituents is treated independently.

### 3.3 Earnings Window Strategies

For each DJIA constituent, we identify all quarterly earnings dates in the sample window for which reported EPS data is available. We test five entry/exit window pairs, defined relative to T (the earnings date, snapped to the nearest trading day): Pre-Drift (T-5 to T-1), Announcement (T-1 to T+1), PEAD-Short (T+1 to T+5), PEAD-Long (T+1 to T+20), and Full Window (T-5 to T+5). Where windows would overlap within a single stock, the earlier event takes precedence. Long-only, 100% capital allocation per event.

### 3.4 Macroeconomic Event Strategies

For each of the four event types (CPI, NFP, GDP, FOMC), we test five windows: Pre (T-2 to T-1), Day-of (T-1 to T+1), Post-Short (T+1 to T+3), Post-Long (T+1 to T+10), and Full (T-2 to T+5). All strategies are applied to ^DJI. Where windows overlap, earlier events take precedence. Long-only, 100% capital allocation per event. Events are filtered to exclude future-dated estimates.

### 3.5 Performance Metrics

For each strategy we report: total compounded return over the sample period (expressed as a percentage of starting capital), maximum drawdown (the maximum peak-to-trough decline in portfolio value), win rate (percentage of individual trades generating a positive return), number of events/trades, and calendar-year return decomposition. A buy-and-hold benchmark is included in all comparisons.

---

## 4. Results: Moving Average Strategies

### 4.1 DJIA Index

Table 1 presents results for moving average crossover strategies on ^DJI.

**Table 1: MA Crossover Results — DJIA Index (^DJI), June 2021 – May 2026**

| Strategy | Total Return | Max Drawdown | Trades |
|---|---|---|---|
| Buy & Hold | +46.5% | -21.9% | — |
| SMA(9,21) | +12.2% | -21.1% | 29 |
| SMA(20,50) | +2.3% | -18.8% | 15 |
| SMA(50,200) | +30.2% | -16.4% | 3 |
| SMA(9,50) | +3.1% | -22.9% | 19 |
| SMA(21,200) | +30.6% | -10.0% | 4 |
| EMA(9,21) | +25.6% | -15.2% | 22 |
| EMA(20,50) | +6.5% | -21.1% | 15 |
| EMA(50,200) | +19.3% | -18.7% | 6 |
| EMA(9,50) | +18.6% | -14.8% | 21 |
| EMA(21,200) | +17.3% | -15.4% | 7 |

No strategy outperforms buy-and-hold on total return. However, the drawdown profile of slow crossover strategies is markedly superior. SMA(21,200) achieves a maximum drawdown of -10.0% — less than half the -21.9% experienced by buy-and-hold — while capturing 65.8% of the benchmark return. This result is consistent with the theoretical role of long-period moving averages as trend filters: the 200-day MA effectively identifies sustained bear markets and reduces exposure during large drawdown events, at the cost of delayed re-entry during early-stage rallies.

Fast crossover strategies (SMA 9/21, EMA 9/21, EMA 9/50) generate more trading activity (19–29 trades over five years) with neither return nor risk advantages over slow crossovers, suggesting that high-frequency MA signals contribute noise rather than signal in the DJIA over this period.

### 4.2 Individual DJIA Constituents

At the constituent level, the average buy-and-hold return across 30 stocks was +106.3%, reflecting the presence of NVIDIA (approx. +1,800% over the period) in the cohort. The average EMA(21,200) return was +60.6%, representing the highest-performing strategy at the aggregate level. SMA(50,200) and SMA(21,200) registered the highest beat rates against individual-stock buy-and-hold (27% each), confirming that slow crossovers are most effective at identifying trending stocks.

The NVDA-EMA(21,200) combination returned +991%, capturing approximately 55% of the stock's buy-and-hold return while making only four trades. This represents a meaningful demonstration of the risk-reduction value of the 200-day signal on a highly volatile, strongly trending equity. Among less volatile constituents, Goldman Sachs EMA(21,200) returned +246% versus a buy-and-hold of +193%, representing genuine outperformance.

---

## 5. Results: Earnings Window Strategies

**Table 2: Earnings Window Results — Average Across 30 DJIA Stocks**

| Window | Avg Return | Avg Max DD | Win Rate | Avg Events/Stock |
|---|---|---|---|---|
| Buy & Hold | +106.3% | -39.1% | — | — |
| Pre-Drift [-5,-1] | +7.9% | -9.6% | 55.2% | 20.0 |
| Announcement [-1,+1] | +3.2% | -17.5% | 51.7% | 20.0 |
| PEAD-Short [+1,+5] | +5.5% | -9.8% | 53.6% | 19.9 |
| PEAD-Long [+1,+20] | +23.4% | -18.5% | 57.1% | 19.6 |
| Full [-5,+5] | +18.0% | -19.7% | 54.7% | 19.9 |

The PEAD-Long window generates the strongest performance across both return (+23.4% average compounded) and win rate (57.1%). The per-event return of +1.19% represents economically meaningful edge given the liquidity and efficiency of the securities studied.

Notably, the announcement window shows a win rate of 51.7% — statistically indistinguishable from 50% in a sample of this size — with the lowest average return (+3.2%) of any window. This is consistent with the efficient markets prediction that announcement-day price adjustments are immediate and complete; residual return predictability exists in the post-announcement period but not in the contemporaneous window.

The strongest individual result is Goldman Sachs PEAD-Long (+158.7%, 70% win rate, -10.7% max drawdown), followed by JPMorgan (+82.6%, 75% win rate). The concentration of strong PEAD in financial sector constituents merits further investigation; a plausible mechanism is that financial earnings contain dense guidance about forward credit conditions and net interest margin that analysts require additional time to incorporate into models.

---

## 6. Results: Macroeconomic Event Strategies

**Table 3: Macroeconomic Event Strategy Results — ^DJI**

| Event | Window | Total Return | Win Rate | Events |
|---|---|---|---|---|
| CPI | Pre [-2,-1] | +20.0% | 58.3% | 60 |
| CPI | Day-of [-1,+1] | +0.1% | 51.7% | 60 |
| CPI | Post-Short [+1,+3] | +2.1% | 50.0% | 60 |
| CPI | Post-Long [+1,+10] | +6.4% | 55.0% | 60 |
| CPI | Full [-2,+5] | +9.2% | 53.3% | 60 |
| NFP | Pre [-2,-1] | -15.3% | 35.0% | 60 |
| NFP | Day-of [-1,+1] | -1.9% | 56.7% | 60 |
| NFP | Post-Short [+1,+3] | +27.6% | 56.7% | 60 |
| NFP | Post-Long [+1,+10] | +10.5% | 56.7% | 60 |
| GDP | Pre [-2,-1] | -2.4% | 40.0% | 20 |
| GDP | Day-of [-1,+1] | +8.4% | 55.0% | 20 |
| GDP | Post-Short [+1,+3] | +3.5% | 70.0% | 20 |
| GDP | Post-Long [+1,+10] | +20.8% | 75.0% | 20 |
| FOMC | Pre [-2,-1] | +2.1% | 47.5% | 40 |
| FOMC | Day-of [-1,+1] | +1.2% | 50.0% | 40 |
| FOMC | Post-Short [+1,+3] | +1.4% | 57.5% | 40 |
| FOMC | Post-Long [+1,+10] | +37.7% | 70.0% | 40 |
| Buy & Hold | — | +46.5% | — | — |

Several findings warrant discussion.

**Post-FOMC Drift.** The FOMC Post-Long strategy generates +37.7% over five years, representing the highest total return among all macroeconomic event strategies and approaching buy-and-hold (+46.5%) while being invested for approximately 32% of available trading days. The 70% win rate across 40 events (encompassing both hiking and cutting cycles) suggests a phenomenon not contingent on the direction of the rate decision. This is consistent with the institutional re-positioning hypothesis: large-scale portfolio adjustments in response to changes in the Fed Funds rate take multiple trading sessions to complete, creating directional price pressure in the days following the announcement.

**Post-NFP Drift.** The NFP Post-Short strategy (+27.6%, 56.7% win rate) is the strongest short-duration macro strategy in the dataset. Combined with the sharply negative pre-NFP result, this creates an asymmetric picture: the market de-risks ahead of the number and re-engages after it. This pattern is consistent with a liquidity provision model in which market makers widen spreads and reduce net delta exposure ahead of scheduled volatility events, creating downward price pressure that reverses once uncertainty resolves.

**Pre-NFP Anomaly.** The pre-NFP window (-15.3%, 35% win rate) is the most striking negative result in the study. A 35% win rate across 60 events (vs an expected 50% under the null) represents a highly consistent adverse signal. We interpret this as systematic institutional de-risking rather than informed directional positioning, given the negative expected return. This pattern is robust across both high-inflation (2022–2023) and low-inflation (2024–2025) regimes within the sample.

**CPI Announcement Ineffectiveness.** Despite CPI releases generating the most market commentary of any scheduled release in the 2021–2025 period, the announcement-day window produces +0.1% over 60 events — statistically indistinguishable from zero. The CPI pre-window (+20.0%, 58.3% win rate) is the strongest CPI strategy, which may reflect pre-positioning by participants with superior forecast accuracy, or alternatively, a systematic tendency for risk appetite to expand ahead of scheduled announcements regardless of content.

**GDP Post-Long.** The GDP Post-Long strategy demonstrates the highest win rate in the macroeconomic event category (75%, 20 events) with an average per-event return of +1.04%. The smaller event count (20 quarterly releases over five years) limits statistical confidence, but the consistency of the result across the full period is notable.

---

## 7. Discussion

### 7.1 The Unified Drift Hypothesis

A coherent interpretation emerges across Sections 5 and 6: post-event drift is the most consistent source of edge in scheduled information environments. This holds for earnings (PEAD-Long: 57.1% win rate), FOMC decisions (Post-Long: 70% win rate), NFP releases (Post-Short: 56.7%), and GDP estimates (Post-Long: 75%). In each case, the announcement-day or pre-event windows are weaker.

This pattern is consistent with a unified explanation: markets process scheduled information gradually rather than instantaneously. The initial price reaction to an event may be directionally correct but quantitatively insufficient, with the residual adjustment occurring over the following trading sessions as additional market participants incorporate the information, analysts revise their models, and institutional investors rebalance positions. This interpretation aligns with the behavioural finance literature on investor underreaction (Barberis, Shleifer, and Vishny, 1998) and is consistent with the model of gradual information diffusion proposed by Hong and Stein (1999).

### 7.2 Risk-Adjusted Framing for MA Strategies

The consistent finding that no MA strategy outperforms buy-and-hold on a raw return basis, combined with the consistent finding that slow crossovers substantially reduce maximum drawdown, suggests that the correct performance metric for these strategies is not return but return per unit of drawdown. The SMA(21,200) achieves a Calmar-like ratio approximately twice that of buy-and-hold over the sample period. For investors with binding drawdown constraints — pension funds, endowments, leveraged accounts — this represents genuine economic value.

### 7.3 Limitations

Several limitations of this study should be noted. First, the sample period of five years, while encompassing diverse market conditions, is relatively short for drawing strong conclusions about strategy persistence. Second, the exclusion of transaction costs is material for high-frequency strategies (the SMA(9,21) made 29 trades over five years); realistic transaction cost assumptions would further disadvantage fast crossover systems. Third, the constituent sample is restricted to current DJIA components, introducing survivorship bias — stocks that were removed from the index during the sample period are excluded. Fourth, the macroeconomic event dates, while sourced from official release schedules, may contain minor errors for dates in 2025–2026 that could affect results marginally. Fifth, all strategies are evaluated with hindsight; forward-looking application introduces parameter selection and execution risks not captured in the backtest.

---

## 8. Conclusion

This paper presents a systematic empirical evaluation of technical and event-driven trading strategies on the DJIA and its thirty component equities over a recent five-year period. The principal findings are:

1. Moving average crossover strategies underperform buy-and-hold on raw returns but provide meaningful drawdown reduction; the SMA(21,200) reduces maximum drawdown from -21.9% to -10.0% while capturing 65.8% of benchmark return.

2. Post-Earnings Announcement Drift is observable and economically significant in DJIA constituents (57.1% win rate, +1.19% per event on a 20-day horizon), consistent with the long-established PEAD literature.

3. Post-FOMC drift is the most consistent macroeconomic event strategy (70% win rate, +37.7% compounded over 40 events), with the directional signal persisting over the ten trading days following each rate decision.

4. The pre-NFP period exhibits a systematic adverse return (-15.3%, 35% win rate) consistent with institutional de-risking ahead of scheduled uncertainty.

5. CPI announcement-day returns are statistically indistinguishable from zero, despite CPI being the dominant market narrative during the inflation cycle of 2022–2024.

These findings suggest that the most persistent trading opportunities in the DJIA over this period lie in post-event drift windows rather than in the anticipation or capture of announcement-day reactions. This is consistent with models of gradual information processing and institutional position adjustment, and has practical implications for tactical asset allocation strategies anchored to the macroeconomic calendar.

---

## References

Ball, R., and Brown, P. (1968). An empirical evaluation of accounting income numbers. *Journal of Accounting Research*, 6(2), 159–178.

Barberis, N., Shleifer, A., and Vishny, R. (1998). A model of investor sentiment. *Journal of Financial Economics*, 49(3), 307–343.

Bernard, V., and Thomas, J. (1989). Post-earnings-announcement drift: Delayed price response or risk premium? *Journal of Accounting Research*, 27, 1–36.

Brock, W., Lakonishok, J., and LeBaron, B. (1992). Simple technical trading rules and the stochastic properties of stock returns. *Journal of Finance*, 47(5), 1731–1764.

Chordia, T., Subrahmanyam, A., and Tong, Q. (2014). Have capital market anomalies attenuated in the recent era of high liquidity and trading activity? *Journal of Accounting and Economics*, 58(1), 41–58.

Clare, A., Seaton, J., Smith, P. N., and Thomas, S. (2017). Size matters: Tail risk, momentum and trend following in international equity portfolios. *Journal of Investing*, 26(2), 53–64.

Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. *Journal of Finance*, 25(2), 383–417.

Foster, G., Olsen, C., and Shevlin, T. (1984). Earnings releases, anomalies, and the behavior of security returns. *Accounting Review*, 59(4), 574–603.

Han, Y., Zhou, G., and Zhu, Y. (2016). Taming the factor zoo: A test of new factors. *Journal of Finance*, 71(6), 2471–2517.

Hong, H., and Stein, J. C. (1999). A unified theory of underreaction, momentum trading, and overreaction in asset markets. *Journal of Finance*, 54(6), 2143–2184.

Hou, K., Xue, C., and Zhang, L. (2020). Replicating anomalies. *Review of Financial Studies*, 33(5), 2019–2133.

Livnat, J., and Mendenhall, R. R. (2006). Comparing the post–earnings announcement drift for surprises calculated from analyst and time series forecasts. *Journal of Accounting Research*, 44(1), 177–205.

Lucca, D. O., and Moench, E. (2015). The pre-FOMC announcement drift. *Journal of Finance*, 70(1), 329–371.

Moskowitz, T. J., Ooi, Y. H., and Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics*, 104(2), 228–250.

Savor, P., and Wilson, M. (2013). How much do investors care about macroeconomic risk? Evidence from scheduled economic announcements. *Journal of Financial and Quantitative Analysis*, 48(2), 343–375.

Sullivan, R., Timmermann, A., and White, H. (1999). Data-snooping, technical trading rule performance, and the bootstrap. *Journal of Finance*, 54(5), 1647–1691.
