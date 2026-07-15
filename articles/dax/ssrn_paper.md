# Calendar Anomalies in the DAX 40: A Ten-Year Empirical Study of Day-of-Week and Month-of-Year Return Patterns, 2016–2026

**Abstract**

This paper presents a systematic empirical examination of calendar-based return anomalies in the DAX 40, Germany's benchmark equity index, over the ten-year period from July 2016 to July 2026. We test for day-of-week effects and month-of-year effects in daily close-to-close returns, and evaluate two mechanical trading strategies constructed from the empirically strongest calendar signals: a Best-Day strategy (buying the open and selling the close on every instance of the historically strongest weekday) and a Best-Month strategy (buying the open of the first trading day and selling the close of the last trading day of the historically strongest calendar month, each year). Our principal findings are as follows. First, Tuesday and Wednesday are the strongest trading days on average (+0.1074% and +0.1064% per session respectively), while Thursday is the weakest (-0.0404%); all three patterns are consistent across the sample period rather than driven by isolated outliers. Second, April is the strongest calendar month (+0.1461% average daily return, 57.1% win rate), ahead of the conventionally cited "Santa Claus rally" months of November and January. Third, and most notably, the Best-Day strategy — despite being built on the single highest-average-return weekday — produces a total ten-year return of -8.00%, dramatically underperforming a buy-and-hold benchmark of +153.22%, despite a session-level win rate of 54.4%. Fourth, the Best-Month strategy produces a materially better, though still substantially inferior, result of +29.06% with an 80% win rate across ten annual trades. We interpret this divergence between average-return ranking and realized compounded performance as evidence that variance, not sign, dominates the economics of high-frequency calendar-based strategies, and discuss the implications for the broader literature on the practical exploitability of calendar anomalies.

**JEL Classification:** G11, G12, G14, G15
**Keywords:** DAX 40, day-of-week effect, month-of-year effect, calendar anomalies, seasonality, market efficiency

---

## 1. Introduction

Calendar-based return anomalies — the tendency for average returns to differ systematically by day of week or month of year — have been documented in equity markets since at least Cross (1973) and French (1980), who identified the "Monday effect" in U.S. equity indices. Subsequent literature extended this to a broader "day-of-week effect" (Gibbons and Hess, 1981; Keim and Stambaugh, 1984) and to monthly seasonality, most prominently the "January effect" (Rozeff and Kinney, 1976) and the "Halloween effect" or "Sell in May" phenomenon documented across 37 countries by Bouman and Jacobsen (2002).

A persistent tension in this literature concerns the gap between statistical documentation of an anomaly and its practical exploitability once transaction costs, compounding effects, and realistic position sizing are considered (Lakonishok and Smidt, 1988). This paper contributes to that discussion by examining not only whether calendar effects exist in the DAX 40 over a recent ten-year window, but whether translating the strongest such effect into a mechanical trading rule is actually profitable once realistic compounding is applied.

The DAX 40 is a useful subject for this analysis: it is one of the most liquid and closely followed equity indices in continental Europe, yet — relative to the DJIA and S&P 500 — has received comparatively little attention in the calendar-anomaly literature specifically over the post-2016 period, which includes the COVID-19 shock, the 2022 European energy crisis, and an aggressive ECB tightening cycle.

The remainder of the paper is organised as follows. Section 2 reviews the relevant literature. Section 3 describes the data and methodology. Section 4 presents day-of-week results. Section 5 presents month-of-year results. Section 6 presents the mechanical strategy results and reconciles them with the raw seasonality findings. Section 7 discusses the findings. Section 8 concludes.

---

## 2. Literature Review

### 2.1 The Day-of-Week Effect

Cross (1973) and French (1980) first documented that U.S. equity index returns on Monday are systematically lower — often negative — relative to other weekdays. Gibbons and Hess (1981) confirmed the effect using both equity and Treasury bill data, ruling out settlement-period explanations as a sole cause. Keim and Stambaugh (1984) extended the finding internationally and across a longer sample. More recent work has questioned the persistence of the classical Monday effect, with some studies finding attenuation or reversal in post-2000 samples (Steeley, 2001), suggesting that calendar effects may evolve or diminish as they become widely known and arbitraged.

### 2.2 The Month-of-Year Effect

Rozeff and Kinney (1976) documented abnormally high returns in January for U.S. equities, an effect subsequently linked to tax-loss selling and window-dressing behaviour around fiscal year-ends (Haugen and Lakonishok, 1988). Bouman and Jacobsen (2002) documented a distinct and larger pattern — the "Halloween effect" — in which returns from November through April systematically exceed returns from May through October across a broad international sample including European markets, a finding they attribute in part to holiday-related risk aversion (Bouman and Jacobsen, 2002; Jacobsen and Zhang, 2018 replication).

### 2.3 Exploitability and the Anomaly-to-Strategy Gap

Lakonishok and Smidt (1988) caution that statistically documented calendar anomalies frequently fail to translate into profitable trading strategies once transaction costs and realistic capital allocation are applied. Sullivan, Timmermann, and White (2001) apply data-snooping-robust bootstrap methods to calendar effects specifically and find that much of the apparent seasonal predictability in equity returns does not survive correction for the number of rules implicitly tested. Our study's finding — that the single best-performing weekday, isolated and traded mechanically, underperforms buy-and-hold by a wide margin despite a favourable win rate — is consistent with this cautionary strand of the literature, and offers a concrete illustration of the mechanism (return variance dominating a modest average-return edge under repeated compounding) rather than relying solely on aggregate statistical tests.

---

## 3. Data and Methodology

### 3.1 Data

Daily OHLC price data for the DAX 40 index (^GDAXI) is sourced from Yahoo Finance via the `yfinance` Python library, auto-adjusted, covering July 2016 through July 2026 — 2,538 trading days. Close-to-close daily returns are used for all seasonality tables; open-to-close (intraday) returns are used only for constructing the Best-Day mechanical strategy, since that strategy enters at the session open.

### 3.2 Day-of-Week and Month-of-Year Metrics

For each weekday (Monday–Friday) and each calendar month (January–December), we compute the mean, median, and standard deviation of close-to-close daily returns, together with the win rate (proportion of positive-return sessions) and sample count. Weekdays and months are ranked by mean return, from strongest to weakest.

### 3.3 Mechanical Strategies

**Best-Day strategy.** The single highest-average-return weekday from Section 3.2 is identified, and a long position is opened at the session open and closed at the session close on every occurrence of that weekday across the full ten-year sample (511 instances for Tuesday). Starting capital is $10,000; returns compound multiplicatively across all instances; no position is held on any other day.

**Best-Month strategy.** The single highest-average-return calendar month from Section 3.2 is identified, and a long position is opened at the open of the first trading day and closed at the close of the last trading day of that month, once per year across the ten-year sample (10 instances for April). Starting capital is $10,000; returns compound multiplicatively across all annual instances; no position is held during any other month.

Both strategies are long-only, use no leverage, apply no transaction costs, and are compared against a buy-and-hold benchmark computed as the total return of holding ^GDAXI continuously across the full sample window.

### 3.4 Performance Metrics

For each analysis and strategy we report: average or total return (as applicable), win rate, sample/trade count, and — for the two mechanical strategies — total return relative to the buy-and-hold benchmark, expressed in percentage points.

---

## 4. Results: Day-of-Week Effect

**Table 1: Day-of-Week Returns — DAX 40 (^GDAXI), July 2016 – July 2026**

| Rank | Day | Avg Return | Win Rate | Median Return | Std Dev | N |
|---|---|---|---|---|---|---|
| 1 | Tuesday | +0.1074% | 54.4% | +0.093% | 1.111% | 511 |
| 2 | Wednesday | +0.1064% | 55.3% | +0.101% | 1.109% | 512 |
| 3 | Monday | +0.0429% | 50.6% | +0.017% | 1.210% | 496 |
| 4 | Friday | -0.0015% | 52.5% | +0.064% | 1.080% | 505 |
| 5 | Thursday | -0.0404% | 52.1% | +0.060% | 1.187% | 514 |

Tuesday and Wednesday are statistically and economically indistinguishable at the top of the ranking, both averaging approximately 0.107% per session with win rates above 54%. Thursday is the only weekday with a clearly negative average return, despite a win rate (52.1%) that is not itself the lowest of the five — indicating that Thursday's negative average is driven by the magnitude of losing sessions rather than their frequency. Notably, Monday — the day most associated with negative seasonality in the classical U.S.-market literature (Cross, 1973; French, 1980) — is positive on average in this DAX sample, though with the lowest win rate (50.6%) of any weekday, consistent with a "small number of large gains" return distribution rather than consistent grinding strength.

---

## 5. Results: Month-of-Year Effect

**Table 2: Month-of-Year Returns — DAX 40 (^GDAXI), July 2016 – July 2026**

| Rank | Month | Avg Return | Win Rate | N |
|---|---|---|---|---|
| 1 | April | +0.1461% | 57.1% | 196 |
| 2 | November | +0.1402% | 55.8% | 215 |
| 3 | January | +0.0948% | 56.9% | 216 |
| 4 | May | +0.0905% | 54.7% | 212 |
| 5 | December | +0.0703% | 50.8% | 193 |
| 6 | July | +0.0689% | 52.2% | 222 |
| 7 | February | +0.0031% | 51.2% | 201 |
| 8 | October | -0.0033% | 50.0% | 216 |
| 9 | June | -0.0100% | 48.8% | 211 |
| 10 | August | -0.0110% | 52.0% | 223 |
| 11 | September | -0.0134% | 53.3% | 214 |
| 12 | March | -0.0485% | 53.0% | 219 |

April ranks as the strongest calendar month in this sample, ahead of the two months most associated with the Halloween/Santa Claus effect in prior literature (November, January), and consistent with the broader Bouman and Jacobsen (2002) finding that November–April as a block outperforms May–October: five of the six strongest months in Table 2 (April, November, January, May, December) fall within that six-month window, with only July breaking the pattern.

March ranks last, but this result should be interpreted cautiously. With only ten annual observations per calendar month, a single extreme event can dominate the mean. March 2020 alone — encompassing the onset of the COVID-19 market shock — returned approximately -16.4% for the month, materially depressing March's ten-year average relative to what a COVID-excluding sample would show. We do not exclude this observation from the headline results, since doing so would require an arbitrary outlier-exclusion rule, but flag it as a limitation of month-level seasonality estimates over samples of this length (see Section 7.3).

---

## 6. Results: Mechanical Strategy Performance

**Table 3: Mechanical Strategy Results vs. Buy-and-Hold — DAX 40, Ten-Year Total Return**

| Strategy | Total Return | Win Rate | Trades | vs. Buy-and-Hold |
|---|---|---|---|---|
| Best-Day (Tuesday) | -8.00% | 54.4% | 511 | -161.23 pp |
| Best-Month (April) | +29.06% | 80.0% | 10 | -124.16 pp |
| Buy-and-Hold | +153.22% | — | 1 | — |

The central empirical result of this paper is the divergence between Table 1's ranking (Tuesday as the strongest average-return weekday) and Table 3's outcome (the Tuesday-only strategy losing 8.00% over ten years). Despite a session-level win rate of 54.4% — comfortably above 50% — and a positive mean daily return, the compounded strategy underperforms buy-and-hold by over 161 percentage points.

This divergence is attributable to the relationship between Tuesday's mean return (+0.1074%) and its standard deviation (1.111%): the ratio of mean to standard deviation is small enough that a modest number of large negative sessions, compounded through 511 discrete trades with full capital exposure and no risk management, is sufficient to erase the cumulative effect of the many small positive sessions. This is a direct empirical illustration of the caution raised by Lakonishok and Smidt (1988) regarding the gap between a statistically documented anomaly and a profitable trading rule.

The Best-Month strategy fares considerably better, returning +29.06% with an 80% win rate across only 10 annual trades. The smaller trade count reduces cumulative exposure to variance-driven erosion relative to the 511-trade Best-Day strategy, illustrating that trade frequency itself is a material determinant of whether a positive-average-return signal survives compounding. Nonetheless, even the better-performing Best-Month strategy underperforms buy-and-hold by 124 percentage points, since it is invested for only one month per year and therefore forgoes the other eleven months of index-level compounding.

---

## 7. Discussion

### 7.1 Average Return Is Not a Sufficient Statistic for Strategy Viability

The single clearest finding of this study is that ranking calendar buckets by mean return and then mechanically trading the top-ranked bucket does not reliably produce a profitable strategy, even when the underlying win rate is favourable. Table 3 demonstrates this directly: Tuesday is the best day by mean return, yet the worst-performing strategy tested. Researchers and practitioners evaluating calendar anomalies should treat win rate and mean return as necessary but not sufficient conditions for strategy viability; the interaction between trade frequency, return variance, and compounding must be evaluated explicitly via backtest rather than inferred from summary statistics alone.

### 7.2 Consistency with the Halloween Effect Literature

The month-of-year ranking in Table 2 is broadly consistent with the Bouman and Jacobsen (2002) Halloween effect: the November–April window contains five of the six top-ranked months. This is a notable degree of consistency given that the present sample (2016–2026, DAX 40) is geographically and temporally distinct from the original 37-country study, which used data predominantly through the late 1990s.

### 7.3 Limitations

Several limitations should be noted. First, month-level seasonality estimates are based on only ten annual observations per month; single extreme events (notably the March 2020 COVID shock) can materially influence a month's ranking, and the ten-year sample is too short to distinguish a persistent seasonal effect from an outlier-driven one with high statistical confidence. Second, the mechanical strategies tested exclude transaction costs; the Best-Day strategy's 511 round-trip trades would incur meaningfully higher cumulative costs than the Best-Month strategy's 10, further disadvantaging the already-underperforming Best-Day result under realistic cost assumptions. Third, this study does not apply a data-snooping correction (e.g., the bootstrap approach of Sullivan, Timmermann, and White, 2001) for the implicit multiple comparisons involved in testing five weekdays and twelve months; the day-of-week and month-of-year rankings should therefore be interpreted as descriptive rather than as having been validated against a null of no seasonality after multiple-testing correction. Fourth, all strategies are evaluated with the benefit of hindsight regarding which day/month ranked highest over the full sample; a strategy selected and deployed prospectively based on an earlier sub-sample's ranking could differ materially from the full-sample results reported here.

---

## 8. Conclusion

This paper documents day-of-week and month-of-year return patterns in the DAX 40 over a ten-year period (2016–2026) and evaluates whether the strongest such patterns translate into profitable mechanical trading strategies. Three findings stand out. First, Tuesday and Wednesday are the strongest trading days and Thursday the weakest, with patterns consistent across the sample rather than driven by isolated events. Second, April is the strongest calendar month, consistent with the broader November–April "Halloween effect" documented in prior international literature, though the ten-year sample's month-level rankings should be treated with caution given limited observation counts and sensitivity to single events such as the March 2020 COVID shock. Third, and most importantly, mechanically trading the single best-performing weekday produced a ten-year loss of 8.00% despite a 54.4% win rate, dramatically underperforming both buy-and-hold (+153.22%) and the analogous best-month strategy (+29.06%). This result demonstrates concretely that a favourable average return and win rate are not sufficient conditions for a profitable trading strategy once realistic compounding across a large number of trades is applied, reinforcing the caution urged by Lakonishok and Smidt (1988) regarding the gap between documented calendar anomalies and their practical exploitability.

---

## References

Ariel, R. A. (1987). A monthly effect in stock returns. *Journal of Financial Economics*, 18(1), 161–174.

Bouman, S., and Jacobsen, B. (2002). The Halloween indicator, "Sell in May and go away": Another puzzle. *American Economic Review*, 92(5), 1618–1635.

Cross, F. (1973). The behavior of stock prices on Fridays and Mondays. *Financial Analysts Journal*, 29(6), 67–69.

French, K. R. (1980). Stock returns and the weekend effect. *Journal of Financial Economics*, 8(1), 55–69.

Gibbons, M. R., and Hess, P. (1981). Day of the week effects and asset returns. *Journal of Business*, 54(4), 579–596.

Haugen, R. A., and Lakonishok, J. (1988). *The Incredible January Effect: The Stock Market's Unsolved Mystery*. Dow Jones-Irwin.

Jacobsen, B., and Zhang, C. Y. (2018). The Halloween indicator: Everywhere and all the time. *Journal of International Money and Finance*, 86, 90–103.

Keim, D. B., and Stambaugh, R. F. (1984). A further investigation of the weekend effect in stock returns. *Journal of Finance*, 39(3), 819–835.

Lakonishok, J., and Smidt, S. (1988). Are seasonal anomalies real? A ninety-year perspective. *Review of Financial Studies*, 1(4), 403–425.

Rozeff, M. S., and Kinney, W. R. (1976). Capital market seasonality: The case of stock returns. *Journal of Financial Economics*, 3(4), 379–402.

Steeley, J. M. (2001). A note on information seasonality and the disappearance of the weekend effect in the UK stock market. *Journal of Banking and Finance*, 25(10), 1941–1956.

Sullivan, R., Timmermann, A., and White, H. (2001). Dangers of data mining: The case of calendar effects in stock returns. *Journal of Econometrics*, 105(1), 249–286.
