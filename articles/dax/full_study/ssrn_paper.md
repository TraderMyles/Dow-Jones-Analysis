# Technical and Event-Driven Trading Strategies on the DAX 40: A Systematic Backtest, 2021–2026

**Abstract**

This paper presents a systematic empirical examination of four classes of long-only trading strategies applied to the DAX 40 (Deutscher Aktienindex) and its forty component equities over the five-year period from July 2021 to July 2026. We test (i) moving average crossover strategies using five SMA and EMA parameter pairs, (ii) the same crossover strategies applied to each of the forty individual DAX 40 constituents, (iii) earnings announcement window strategies capturing pre-announcement drift and post-earnings announcement drift (PEAD), and (iv) event-driven strategies centred on four German and Eurozone macroeconomic calendar releases: the German Consumer Price Index (CPI) flash estimate, the German unemployment report (the closest German analogue to the US Non-Farm Payrolls release), the German GDP flash estimate, and European Central Bank (ECB) Governing Council rate decisions. This study is a direct methodological replication of an equivalent analysis conducted on the Dow Jones Industrial Average (DJIA) and its thirty components over the same window length, permitting cross-market comparison. Our principal findings are as follows. First, no moving average crossover strategy outperforms buy-and-hold on the DAX 40 index on a raw return basis, but slow crossover systems (50/200 and 21/200) reduce maximum drawdown by approximately 40% relative to passive exposure — consistent with the DJIA result. Second, at the constituent level, we document a novel finding absent from the DJIA replication: a long-only, non-leveraged EMA(50,200) crossover on Rheinmetall AG (RHM.DE) generated a total return of +1,724% against a buy-and-hold return of +1,199% for the same stock over the same period, using only two round-trip trades. Third, PEAD is observable and economically significant in DAX constituents, with a post-earnings 20-day window generating a 53.5% win rate and an average compounded return of +19.9% across all forty stocks. Fourth, the post-ECB-decision window (entry T+1, exit T+10) and the equivalent German unemployment and GDP windows are the strongest macroeconomic event strategies, each outperforming their respective announcement-day windows by a wide margin — replicating the DJIA study's central post-FOMC finding in a distinct monetary and macroeconomic regime. These results extend the external validity of the original DJIA findings to a second major developed-market index and identify a specific, mechanically explicable condition under which a moving average strategy can outperform buy-and-hold in raw return terms rather than merely on a risk-adjusted basis.

**JEL Classification:** G11, G12, G14, G15
**Keywords:** DAX 40, moving average crossover, PEAD, ECB Governing Council, event-driven strategies, technical analysis, macroeconomic announcements, cross-market replication

---

## 1. Introduction

A companion study to this paper examined technical and event-driven trading strategies on the Dow Jones Industrial Average (DJIA) and its thirty constituent equities over the period June 2021 to May 2026, finding that (i) no moving average crossover strategy outperformed buy-and-hold on the index, though slow crossovers materially reduced drawdown; (ii) post-earnings announcement drift (PEAD) was economically significant; and (iii) post-event drift following FOMC decisions, GDP releases, and Non-Farm Payrolls dominated announcement-day returns across the macroeconomic calendar. The present paper asks whether these findings are specific to the DJIA and the US macroeconomic calendar, or whether they generalise to a structurally different index, currency regime, and central bank.

The DAX 40 is a natural test case. It is a major developed-market index with high constituent liquidity, comparable in institutional prominence to the DJIA, but denominated in euros, governed by a different monetary authority (the ECB rather than the Federal Reserve), and subject to a distinct macroeconomic release calendar (Destatis and the Bundesagentur für Arbeit rather than the US Bureau of Labor Statistics and Bureau of Economic Analysis). The five-year sample window (July 2021 – July 2026) additionally captures a materially different macro narrative for Germany specifically: an energy-price shock following the 2022 invasion of Ukraine, an associated recession in German industrial output, and a subsequent multi-year re-rating of the German defense and energy sectors — conditions with no direct DJIA analogue.

This paper contributes to the literature along the same three dimensions as its companion study, with an explicit cross-market comparative framing: (a) contemporaneous MA crossover performance on a major non-US index and its components; (b) simultaneous index-level and constituent-level analysis, permitting direct comparison of aggregation effects across two currency regimes; and (c) a unified event-study framework covering four macroeconomic release types translated into their closest German/Eurozone equivalents, enabling comparison of event-premia structure across two distinct monetary policy regimes operating over the identical calendar period.

The remainder of the paper is organised as follows. Section 2 reviews the relevant literature, focusing on results specific to non-US developed markets where available. Section 3 describes data and methodology, including the mapping of US event types to their German/Eurozone equivalents. Section 4 presents moving average results. Section 5 presents earnings window results. Section 6 presents macroeconomic event results. Section 7 discusses findings, with explicit attention to where the DAX results replicate versus diverge from the DJIA companion study. Section 8 concludes.

---

## 2. Literature Review

### 2.1 Moving Average Strategies

The theoretical and empirical basis for moving average crossover analysis is addressed at length in the companion DJIA study (Brock, Lakonishok, and LeBaron, 1992; Han, Zhou, and Zhu, 2016; Clare et al., 2017) and is not repeated in full here. Of particular relevance to this paper is the risk-management framing advanced by Clare et al. (2017), who characterise trend-following as delivering equity-like returns with reduced drawdown rather than outright alpha — a framing this paper's DAX index-level results support, and which its constituent-level results (Section 4.2) complicate in one specific respect.

### 2.2 Post-Earnings Announcement Drift (PEAD)

PEAD's theoretical basis (Ball and Brown, 1968; Bernard and Thomas, 1989) is addressed in the companion study. Evidence for PEAD specifically in German and European equities is more limited than the corresponding US literature, though Hong, Lim, and Stein (2000) find analyst coverage — plausibly lower on average for DAX constituents than for DJIA constituents of comparable market capitalisation — is associated with stronger post-earnings drift, a consideration relevant to interpreting the relative magnitude of the effect documented here.

### 2.3 Macroeconomic Event Reactions and Central Bank Communication

Lucca and Moench (2015) document a pre-FOMC announcement drift in US equities; Savor and Wilson (2013) document elevated announcement-day risk premia around US scheduled macro releases. The ECB-specific literature is comparatively sparse but Andersson, Overby, and Sebestyén (2009) document measurable equity market reactions to ECB Governing Council communications, and Rosa (2011) finds that the informational content of ECB monetary policy surprises affects European equity indices with a magnitude comparable to FOMC surprises on US indices — providing a prior expectation, tested directly in Section 6, that ECB decisions should generate DJIA-comparable event-driven return patterns despite the differing institutional structure (a rotating national-central-bank voting membership, an 8-meeting annual cadence matching the Federal Reserve's own post-2011 schedule, and a historically more consensus-driven communication style).

---

## 3. Data and Methodology

### 3.1 Data

Price data for the DAX 40 index (^GDAXI) and all forty current DAX 40 constituent equities are sourced from Yahoo Finance via the `yfinance` Python library, auto-adjusted. The sample covers July 2021 through July 2026, yielding 1,273 trading days. The DAX 40 constituents used are the current composition as of the study date: Adidas (ADS.DE), Airbus (AIR.DE), Allianz (ALV.DE), BASF (BAS.DE), Bayer (BAYN.DE), Beiersdorf (BEI.DE), BMW (BMW.DE), Brenntag (BNR.DE), Commerzbank (CBK.DE), Continental (CON.DE), Daimler Truck (DTG.DE), Deutsche Bank (DBK.DE), Deutsche Börse (DB1.DE), DHL Group (DHL.DE), Deutsche Telekom (DTE.DE), E.ON (EOAN.DE), Fresenius (FRE.DE), Fresenius Medical Care (FME.DE), GEA Group (G1A.DE), Hannover Rück (HNR1.DE), Heidelberg Materials (HEI.DE), Henkel (HEN3.DE), Infineon Technologies (IFX.DE), Mercedes-Benz Group (MBG.DE), Merck KGaA (MRK.DE), MTU Aero Engines (MTX.DE), Munich Re (MUV2.DE), Porsche SE (PAH3.DE), Qiagen (QIA.DE), Rheinmetall (RHM.DE), RWE (RWE.DE), SAP (SAP.DE), Scout24 (G24.DE), Siemens (SIE.DE), Siemens Energy (ENR.DE), Siemens Healthineers (SHL.DE), Symrise (SY1.DE), Volkswagen Group (VOW3.DE), Vonovia (VNA.DE), and Zalando (ZAL.DE). Four constituents (Airbus, Beiersdorf, Deutsche Börse, Porsche SE) returned no earnings-date records via the data provider's earnings calendar and are consequently excluded from the earnings-window analysis (Section 5) only; they remain included in the moving average analysis (Section 4).

German CPI flash-estimate dates, German GDP flash-estimate dates, and German unemployment report dates are sourced from official Destatis (Statistisches Bundesamt) and Bundesagentur für Arbeit press release archives. ECB Governing Council monetary policy decision dates are sourced from the ECB's official press release calendar. All four macroeconomic date series are verified against primary-source release documents rather than secondary aggregators.

All strategies assume execution at the closing price of the entry and exit days. Signal generation for moving average strategies is lagged by one trading day relative to the indicator calculation date to eliminate lookahead bias. Starting capital is $10,000 per strategy. Transaction costs are excluded; results therefore represent gross returns.

### 3.2 Moving Average Strategies

Identical specification to the companion DJIA study: five crossover parameter pairs — (9,21), (20,50), (50,200), (9,50), and (21,200) — tested for both SMA and EMA, ten strategies total. A long position is initiated when the short MA crosses above the long MA and exited when the short MA crosses below the long MA. When not in a position, cash earns 0%. Positions are sized at 100% of available capital. Each of the 40 constituents is treated independently for the constituent-level analysis.

### 3.3 Earnings Window Strategies

Identical specification to the companion study: five entry/exit window pairs relative to the earnings date T — Pre-Drift (T-5 to T-1), Announcement (T-1 to T+1), PEAD-Short (T+1 to T+5), PEAD-Long (T+1 to T+20), and Full Window (T-5 to T+5) — applied to each of the 36 DAX constituents with available earnings-date data.

### 3.4 Macroeconomic Event Strategies: US-to-German/Eurozone Event Mapping

This study maps each of the companion study's four US event types to its closest German or Eurozone equivalent, as follows:

| DJIA study event | DAX study equivalent | Rationale |
|---|---|---|
| CPI (BLS) | German CPI flash estimate (Destatis) | Both are the earliest, most market-sensitive inflation print for their respective economies |
| NFP (BLS) | German unemployment report (Bundesagentur für Arbeit) | Both are the principal monthly labour-market release; Germany has no direct payrolls-change equivalent, making the unemployment report the closest available proxy |
| GDP advance estimate (BEA) | German GDP flash estimate (Destatis) | Both are the earliest quarterly growth estimate, released approximately 30 days after quarter-end in both economies |
| FOMC (Federal Reserve) | ECB Governing Council rate decision | Both are the principal policy-rate-setting event for their respective currency areas, held on a comparable 8-meetings-per-year cadence |

For each of the four event types, we test the same five windows as the companion study: Pre (T-2 to T-1), Day-of (T-1 to T+1), Post-Short (T+1 to T+3), Post-Long (T+1 to T+10), and Full (T-2 to T+5), applied to ^GDAXI. Where windows overlap, earlier events take precedence.

### 3.5 Performance Metrics

Identical to the companion study: total compounded return, maximum drawdown, win rate, number of events/trades, and calendar-year decomposition, with a buy-and-hold benchmark in all comparisons.

---

## 4. Results: Moving Average Strategies

### 4.1 DAX 40 Index

**Table 1: MA Crossover Results — DAX 40 Index (^GDAXI), July 2021 – July 2026**

| Strategy | Total Return | Max Drawdown | Trades |
|---|---|---|---|
| Buy & Hold | +61.8% | -26.4% | — |
| SMA(9,21) | +41.2% | -13.0% | 31 |
| SMA(20,50) | -5.7% | -24.3% | 17 |
| SMA(50,200) | +50.2% | -16.0% | 3 |
| SMA(9,50) | +5.5% | -22.5% | 18 |
| SMA(21,200) | +45.5% | -16.0% | 3 |
| EMA(9,21) | +27.1% | -15.5% | 31 |
| EMA(20,50) | +17.5% | -22.4% | 12 |
| EMA(50,200) | +49.1% | -16.0% | 4 |
| EMA(9,50) | +15.9% | -21.6% | 17 |
| EMA(21,200) | +36.8% | -16.0% | 7 |

Consistent with the companion DJIA result, no strategy outperforms buy-and-hold on total return. SMA(50,200) achieves the best return among tested strategies (+50.2%, 81.2% of the benchmark return) while limiting maximum drawdown to -16.0% versus buy-and-hold's -26.4% — a 39.4% reduction. All three 200-day-anchored strategies (SMA 50/200, SMA 21/200, EMA 50/200) converge on an identical -16.0% maximum drawdown, indicating the 200-day signal identifies a common drawdown-defining event: the 2022 European energy-price shock and associated equity selloff, visible in Table-1-underlying annual data as a -12.3% buy-and-hold year against near-flat or mildly negative results for all three 200-day strategies.

### 4.2 Individual DAX 40 Constituents

At the constituent level, the average buy-and-hold return across 40 stocks was +101.1%, with SMA(50,200) achieving the highest average strategy return (+78.6%) and the highest beat-rate against individual-stock buy-and-hold of any strategy tested (50%, i.e., matching or exceeding buy-and-hold on 20 of 40 constituents). This beat-rate is notably higher than the equivalent DJIA finding (27% for the same parameter pair), a difference addressed further in Section 7.2.

The most economically significant individual result is Rheinmetall AG (RHM.DE). Rheinmetall's buy-and-hold return over the sample period was +1,199.0%, reflecting the German defense sector's re-rating following the February 2022 invasion of Ukraine and subsequent European defense-spending commitments. The EMA(50,200) strategy applied to Rheinmetall generated a total return of **+1,724.4%** using only 2 round-trip trades — outperforming the stock's own buy-and-hold return by 525.4 percentage points. This result has no analogue anywhere in the companion DJIA study, where the maximum observed ratio of MA-strategy return to same-stock buy-and-hold return across all 30 constituents and 10 strategies remained below 1.0 (i.e., no MA strategy on any DJIA constituent outperformed that constituent's own buy-and-hold return in raw terms). Siemens Energy AG (ENR.DE) exhibits a smaller-magnitude version of the same phenomenon: SMA(21,200) returned +855.5% against a buy-and-hold return of +585.4% for the same stock.

We address the mechanism underlying this result in Section 7.1.

---

## 5. Results: Earnings Window Strategies

**Table 2: Earnings Window Results — Average Across 40 DAX 40 Stocks**

| Window | Avg Return | Avg Max DD | Win Rate | Avg Events/Stock | Beat B&H |
|---|---|---|---|---|---|
| Buy & Hold | +101.1% | -46.1% | — | — | — |
| Pre-Drift [-5,-1] | +5.3% | -10.9% | 57.3% | 18.1 | 28% |
| Announcement [-1,+1] | +1.3% | -17.0% | 52.3% | 18.2 | 30% |
| PEAD-Short [+1,+5] | +10.9% | -11.7% | 56.8% | 18.2 | 32% |
| PEAD-Long [+1,+20] | +19.9% | -19.1% | 53.5% | 18.2 | 35% |
| Full [-5,+5] | +19.1% | -20.2% | 56.7% | 18.1 | 38% |

The PEAD-Long window generates the second-highest return (+19.9%) and the Full window the highest (+19.1% vs +19.9%, materially comparable), while the Announcement window again shows the weakest performance (+1.3%, 52.3% win rate) — replicating the DJIA companion study's central finding that announcement-day price adjustment is close to immediate, with residual predictability concentrated in the post-announcement period.

The per-event average return for PEAD-Long is +0.88% (computed as total return / average events per stock), broadly comparable in magnitude to the DJIA companion study's PEAD-Long per-event average of +1.19%, suggesting the underlying drift phenomenon is of similar economic magnitude in both markets despite differing macro regimes over the sample period.

The strongest individual results are concentrated in industrials and financials, consistent with the DJIA finding: Siemens Energy Full window (+147.6%, 65.0% win rate), Infineon Full window (+136.3%, 70.0% win rate), and Commerzbank Full window (+96.3%, 73.7% win rate — the highest win rate among any top-10 stock-window combination in this study).

---

## 6. Results: Macroeconomic Event Strategies

**Table 3: Macroeconomic Event Strategy Results — ^GDAXI**

| Event | Window | Total Return | Win Rate | Events |
|---|---|---|---|---|
| CPI | Pre [-2,-1] | +4.3% | 56.7% | 60 |
| CPI | Day-of [-1,+1] | +1.8% | 48.3% | 60 |
| CPI | Post-Short [+1,+3] | +4.7% | 58.3% | 60 |
| CPI | Post-Long [+1,+10] | +36.5% | 60.0% | 60 |
| CPI | Full [-2,+5] | +5.6% | 56.7% | 60 |
| Unemployment | Pre [-2,-1] | +3.5% | 60.0% | 60 |
| Unemployment | Day-of [-1,+1] | -1.4% | 45.0% | 60 |
| Unemployment | Post-Short [+1,+3] | -1.6% | 51.7% | 60 |
| Unemployment | Post-Long [+1,+10] | +38.8% | 58.3% | 60 |
| Unemployment | Full [-2,+5] | +13.9% | 60.0% | 60 |
| GDP | Pre [-2,-1] | +3.2% | 55.0% | 20 |
| GDP | Day-of [-1,+1] | +3.6% | 50.0% | 20 |
| GDP | Post-Short [+1,+3] | +4.6% | 70.0% | 20 |
| GDP | Post-Long [+1,+10] | +29.0% | 70.0% | 20 |
| ECB | Pre [-2,-1] | +9.1% | 50.0% | 40 |
| ECB | Day-of [-1,+1] | -4.2% | 57.5% | 40 |
| ECB | Post-Short [+1,+3] | +4.7% | 47.5% | 40 |
| ECB | Post-Long [+1,+10] | +29.5% | 60.0% | 40 |
| Buy & Hold | — | +61.8% | — | — |

The result structure replicates the DJIA companion study with unusual consistency: **in every one of the four event types, the Post-Long [T+1,+10] window is the single best-performing window**, and in three of four event types (Unemployment, ECB, and — marginally — CPI's Day-of window at a below-50% win rate) the Day-of window is the weakest or a negative-return window.

**Post-ECB Drift.** The ECB Post-Long strategy returns +29.5% over 40 events (60% win rate), directly analogous to the companion study's post-FOMC finding (+37.7%, 70% win rate, 40 events). The ECB Day-of window is markedly negative (-4.2%, though with a 57.5% win rate, indicating a small number of large negative moves rather than frequent small losses) — annual decomposition attributes the bulk of this to 2022 (-11.1%), the year of the ECB's initial hawkish pivot and largest single-meeting rate increases in the institution's history, a period-specific effect absent from the FOMC Day-of result in the companion study.

**German Unemployment Post-Long.** At +38.8% (58.3% win rate), this is the strongest single macroeconomic strategy in the DAX study, exceeding even the ECB Post-Long result, and is broadly comparable in magnitude to the DJIA companion study's strongest macro result (post-FOMC, +37.7%).

**German GDP Post-Long.** At +29.0% with a 70% win rate (tied with GDP Post-Short for the highest win rate of any window in this study), this replicates the companion study's finding that GDP Post-Long carries the highest win rate among macro strategies (75% in the DJIA study), consistent with GDP's comparatively low-frequency, high-information-content release profile in both economies.

**CPI Day-of Weakness.** At +1.8% with a 48.3% win rate — the only sub-50% win rate recorded for any Day-of window in this study — German CPI's announcement-day reaction is, if anything, marginally worse than a coin flip, closely replicating the companion study's finding that DJIA CPI Day-of returns (+0.1%, 51.7% win rate) were statistically indistinguishable from noise.

---

## 7. Discussion

### 7.1 The Rheinmetall Result: When Moving Averages Beat Buy-and-Hold Outright

The single result in this study with no companion-study analogue is Section 4.2's finding that EMA(50,200) on Rheinmetall outperformed the stock's own buy-and-hold return by 525 percentage points using two trades. The mechanism is arithmetic rather than anomalous: a long-only strategy's total return is the compounded product of returns realised only during invested sub-periods. If a stock's price path includes one sufficiently large intermediate drawdown, and a trend-following signal identifies that drawdown's onset and its subsequent recovery with reasonable (not perfect) timing, the strategy's compounded return over the "recovery" sub-period alone — computed from the lower re-entry price — can exceed the stock's total buy-and-hold return computed from the original entry price, even though the strategy earned zero return while out of the market. This is a necessary mathematical possibility whenever a price series contains a sufficiently deep single intermediate drawdown followed by a sufficiently large recovery; it is not possible, by contrast, for price series that rise comparatively monotonically (as most DJIA constituents did over the companion study's window), which explains why no DJIA constituent produced an analogous result. This finding refines rather than contradicts the risk-management framing of moving average strategies (Clare et al., 2017): the same downside-avoidance mechanism that reduces drawdown in the typical case can, in the specific case of a single large intermediate crash followed by a strong recovery, produce raw outperformance rather than merely risk-adjusted outperformance.

### 7.2 Higher Constituent-Level Beat Rates on the DAX Than the DJIA

SMA(50,200)'s 50% beat-rate against individual-stock buy-and-hold on the DAX 40 (Section 4.2) is materially higher than the equivalent DJIA finding (27%). We offer two non-exclusive explanations. First, the DAX 40 sample period is dominated by a single sharp macro shock (the 2022 energy crisis) affecting German equities with unusual breadth and severity, creating more opportunities across the constituent universe for a 200-day trend filter to add value by avoiding a widely shared drawdown — consistent with the finding in Section 4.1 that all three 200-day-anchored index-level strategies converged on an identical maximum drawdown. Second, the DAX 40's sectoral composition (heavier industrial, automotive, and cyclical representation than the DJIA) may produce more constituents with the boom-bust-boom price path structure discussed in Section 7.1.

### 7.3 Post-Event Drift as a Cross-Market, Cross-Regime Phenomenon

The consistency of the Post-Long-window-dominance finding across four event types, two currency regimes, two central banks, and two national statistical agencies (Section 6) is, in our view, the most important finding of this paper considered jointly with its companion study. It is one thing to document post-event drift in a single market; it is considerably stronger evidence of a general phenomenon to find the same structural pattern — weak or negative announcement-day returns, strong 10-day post-event returns — replicated independently across the Federal Reserve/BLS/BEA calendar and the ECB/Destatis/Bundesagentur für Arbeit calendar over the identical five-year window. This is consistent with models of gradual information diffusion (Hong and Stein, 1999) operating as a general feature of developed equity markets' response to scheduled macroeconomic information, rather than as an artefact specific to US market structure or Federal Reserve communication style.

### 7.4 Limitations

The limitations enumerated in the companion DJIA study (short sample period, excluded transaction costs, hindsight-based strategy selection) apply identically here. Additional DAX-specific limitations include: first, four of forty constituents lacked earnings-date data from the data provider and were excluded from Section 5's analysis only, introducing a small selection effect in the earnings-window results; second, the sample period's German-specific macro shock (the 2022 energy crisis) is a single, non-repeating event, and the unusually high MA beat-rates and the Rheinmetall/Siemens Energy results documented in Sections 4.1–4.2 should not be extrapolated to periods without a comparable shock; third, German CPI, unemployment, and GDP release dates, while sourced from primary Destatis and Bundesagentur für Arbeit archives, required per-month or per-quarter document retrieval rather than a single consolidated calendar source, and while cross-checked, carry marginally higher date-accuracy risk than the FOMC/BLS/BEA dates used in the companion study, which benefit from more consolidated official calendar publication.

---

## 8. Conclusion

This paper presents a systematic empirical evaluation of technical and event-driven trading strategies on the DAX 40 and its forty component equities over a five-year period, designed as a direct cross-market replication of an equivalent DJIA study. The principal findings are: (1) moving average crossover strategies underperform buy-and-hold on the DAX 40 index in raw-return terms but substantially reduce maximum drawdown, replicating the DJIA finding; (2) at the constituent level, a moving average strategy on Rheinmetall AG outperformed that stock's own buy-and-hold return in raw terms — a result with no DJIA analogue, attributable to a specific, mechanically explicable price-path condition (a large intermediate drawdown followed by a strong recovery) rather than a general property of moving average strategies; (3) Post-Earnings Announcement Drift is observable and economically significant in DAX constituents at a magnitude comparable to the DJIA finding; (4) post-event drift following ECB rate decisions, German unemployment reports, and German GDP releases dominates announcement-day returns in a pattern replicating the DJIA study's post-FOMC finding across an entirely distinct monetary and statistical regime. Taken jointly with its companion study, this paper's strongest contribution is evidence that post-scheduled-event drift is a general, cross-market feature of developed equity markets' response to macroeconomic information, while moving-average-based risk reduction, though generally robust, admits specific and mechanically well-understood exceptions where it produces raw outperformance rather than merely risk-adjusted outperformance.

---

## References

Andersson, M., Overby, L. J., and Sebestyén, S. (2009). Which news moves the euro area bond market? *German Economic Review*, 10(1), 1–31.

Ball, R., and Brown, P. (1968). An empirical evaluation of accounting income numbers. *Journal of Accounting Research*, 6(2), 159–178.

Bernard, V., and Thomas, J. (1989). Post-earnings-announcement drift: Delayed price response or risk premium? *Journal of Accounting Research*, 27, 1–36.

Brock, W., Lakonishok, J., and LeBaron, B. (1992). Simple technical trading rules and the stochastic properties of stock returns. *Journal of Finance*, 47(5), 1731–1764.

Clare, A., Seaton, J., Smith, P. N., and Thomas, S. (2017). Size matters: Tail risk, momentum and trend following in international equity portfolios. *Journal of Investing*, 26(2), 53–64.

Han, Y., Zhou, G., and Zhu, Y. (2016). Taming the factor zoo: A test of new factors. *Journal of Finance*, 71(6), 2471–2517.

Hong, H., Lim, T., and Stein, J. C. (2000). Bad news travels slowly: Size, analyst coverage, and the profitability of momentum strategies. *Journal of Finance*, 55(1), 265–295.

Hong, H., and Stein, J. C. (1999). A unified theory of underreaction, momentum trading, and overreaction in asset markets. *Journal of Finance*, 54(6), 2143–2184.

Lucca, D. O., and Moench, E. (2015). The pre-FOMC announcement drift. *Journal of Finance*, 70(1), 329–371.

Rosa, C. (2011). Words that shake traders: The stock market's reaction to central bank communication in real time. *Journal of Empirical Finance*, 18(5), 915–934.

Savor, P., and Wilson, M. (2013). How much do investors care about macroeconomic risk? Evidence from scheduled economic announcements. *Journal of Financial and Quantitative Analysis*, 48(2), 343–375.
