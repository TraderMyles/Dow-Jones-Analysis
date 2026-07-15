"""
DJIA / DAX Strategy Backtest — Streamlit Showcase App

Presents results from systematic backtesting scripts on the Dow Jones
Industrial Average (30 components) and the DAX 40 (40 components).
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR      = Path(__file__).parent
OUTPUTS       = BASE_DIR / "outputs"
ARTICLES      = BASE_DIR / "articles"
DAX_ARTICLES  = ARTICLES / "dax"
DAX_FULL_ARTICLES = DAX_ARTICLES / "full_study"

# ---------------------------------------------------------------------------
# Page config  (theme is set in .streamlit/config.toml)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DJIA / DAX Backtest Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Minimal CSS — only things the theme can't handle
st.markdown("""
<style>
    [data-testid="stMetric"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px 18px;
    }
    .article-body { max-width: 760px; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@st.cache_data
def load_csv(name):
    path = OUTPUTS / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)


def show_chart(name):
    path = OUTPUTS / name
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.warning(f"Chart not found: {name} — run the corresponding script first.")


def load_article(dir_path, filename):
    path = dir_path / filename
    return path.read_text() if path.exists() else "_Article file not found._"


def colour_returns(df, return_cols):
    """Apply green/red colour styling to return columns."""
    def _style(row):
        styles = []
        for col in row.index:
            if col in return_cols:
                try:
                    v = float(row[col])
                    styles.append("color: #3fb950" if v > 0 else ("color: #f85149" if v < 0 else ""))
                except Exception:
                    styles.append("")
            else:
                styles.append("")
        return styles
    return df.style.apply(_style, axis=1)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
DOW_PAGES = {
    "🏠  Overview":                   "dow_overview",
    "📈  Script 1 — MA on DJIA":      "dow_s1",
    "📊  Script 2 — MA on 30 Stocks": "dow_s2",
    "💼  Script 3 — Earnings Effect":  "dow_s3",
    "📅  Script 4 — Economic Calendar":"dow_s4",
    "📝  Research Articles":           "dow_articles",
}

DAX_PAGES = {
    "🏠  Overview":                    "dax_overview",
    "📈  Script 1 — MA on ^GDAXI":     "dax_s1",
    "📊  Script 2 — MA on 40 Stocks":  "dax_s2",
    "💼  Script 3 — Earnings Effect":   "dax_s3",
    "📅  Script 4 — Economic Calendar": "dax_s4",
    "🗓️  Seasonal Analysis":            "dax_seasonal",
    "📝  Research Articles":            "dax_articles",
}

with st.sidebar:
    st.markdown("## 📈 Backtest Research")
    st.caption("Systematic strategy research")
    st.divider()
    market = st.radio(
        "Market", ["🇺🇸  Dow Jones (DJIA)", "🇩🇪  DAX 40"],
        label_visibility="collapsed", horizontal=True,
    )
    st.divider()

    PAGES = DOW_PAGES if market.startswith("🇺🇸") else DAX_PAGES
    selected = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()

    if market.startswith("🇺🇸"):
        st.caption(
            "Period: Jun 2021 – May 2026  \n"
            "Data: yfinance · Long only  \n"
            "Capital: $10,000 per strategy"
        )
    else:
        st.caption(
            "Period: Jul 2021 – Jul 2026  \n"
            "Data: yfinance · Long only  \n"
            "Capital: $10,000 per strategy"
        )

page = PAGES[selected]


# ===========================================================================
# DOW: OVERVIEW
# ===========================================================================
if page == "dow_overview":
    st.title("DJIA Strategy Backtest Research")
    st.markdown(
        "A systematic empirical study across **four strategy classes** applied to the "
        "Dow Jones Industrial Average and its 30 component stocks over five years."
    )
    st.divider()

    metric_row([
        ("Backtest Period",      "Jun 2021 – May 2026", "5 years"),
        ("Stocks Covered",       "30 DJIA Components",  "Plus ^DJI index"),
        ("Individual Backtests", "1,200+",              "Strategies tested"),
        ("DJIA Buy & Hold",      "+46.5%",              "Benchmark return"),
    ])

    st.divider()
    st.subheader("What was tested")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Script 1 — MA on DJIA Index**
- 10 crossover strategies (SMA + EMA)
- Pairs: (9/21), (20/50), (50/200), (9/50), (21/200)
- Long only, signal lagged 1 day

**Script 2 — MA on 30 Stocks**
- Same 10 strategies on each DJIA component
- 330 individual backtests
""")
    with col2:
        st.markdown("""
**Script 3 — Earnings Effect**
- 5 windows around each quarterly earnings date
- Pre-drift, announcement, PEAD-Short, PEAD-Long, Full
- ~600 events across 30 stocks

**Script 4 — Economic Calendar**
- CPI, NFP, GDP, FOMC event windows
- 5 entry/exit windows per event type
- 60 CPI · 60 NFP · 20 GDP · 40 FOMC events
""")

    st.divider()
    st.subheader("Key findings at a glance")

    findings = pd.DataFrame([
        {"Script": "MA — DJIA Index",    "Best Strategy": "SMA(21,200)",
         "Return": "+30.6%", "vs Buy & Hold": "+46.5%",
         "Key Insight": "Halves max drawdown (−10% vs −22%) at ⅔ of B&H return"},
        {"Script": "MA — 30 Stocks",     "Best Strategy": "EMA(21,200) avg",
         "Return": "+60.6%", "vs Buy & Hold": "+106.3% avg",
         "Key Insight": "NVDA+EMA(21,200) = +991%; slow MAs dominate trending stocks"},
        {"Script": "Earnings Effect",    "Best Strategy": "PEAD-Long [+1,+20]",
         "Return": "+23.4% avg", "vs Buy & Hold": "+106.3% avg",
         "Key Insight": "57% win rate · +1.19%/event · GS: +159%, 70% win rate"},
        {"Script": "Economic Calendar",  "Best Strategy": "FOMC Post-Long [+1,+10]",
         "Return": "+37.7%", "vs Buy & Hold": "+46.5%",
         "Key Insight": "70% win rate over 40 Fed decisions · GDP post-long: 75%"},
    ])
    st.dataframe(findings, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("The central finding")

    st.success(
        "**Post-event drift is the most consistent source of edge across every strategy class.**\n\n"
        "Whether from earnings (PEAD), FOMC decisions, or NFP releases — markets underprice the "
        "follow-through. The announcement itself is processed almost immediately; the residual "
        "adjustment over the following 5–20 trading days is where measurable signal exists."
    )
    st.error(
        "**Pre-NFP positioning is the worst identifiable strategy in the entire study.**\n\n"
        "Owning the Dow in the two days before each jobs report returned −15.3% over 60 events "
        "(35% win rate). The market systematically de-risks ahead of scheduled uncertainty."
    )
    st.warning(
        "**Moving average crossovers don't beat buy-and-hold — but they cut drawdowns in half.**\n\n"
        "The SMA(21,200) returned +30.6% vs +46.5% for B&H, with a max drawdown of just −10.0% "
        "vs −21.9%. Four trades in five years. The right framing is risk management, not alpha."
    )


# ===========================================================================
# DOW: SCRIPT 1 — MA on DJIA
# ===========================================================================
elif page == "dow_s1":
    st.title("Script 1 — Moving Average Crossover on ^DJI")
    st.markdown(
        "Ten SMA and EMA crossover strategies on the Dow Jones Industrial Average index, "
        "five-year backtest."
    )

    df = load_csv("ma_backtest_dow_results.csv")

    if not df.empty:
        bah     = df[df.Strategy == "Buy & Hold"].iloc[0]
        best    = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]
        best_dd = df[df.Strategy != "Buy & Hold"].sort_values("Max Drawdown %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold Return",    f"{bah['Total Return %']:+.1f}%",    "Benchmark"),
            ("Best Strategy Return", f"{best['Total Return %']:+.1f}%",   best["Strategy"]),
            ("Lowest Max Drawdown",  f"{best_dd['Max Drawdown %']:.1f}%", best_dd["Strategy"]),
            ("B&H Max Drawdown",     f"{bah['Max Drawdown %']:.1f}%",     "Benchmark"),
        ])

    st.divider()
    show_chart("ma_backtest_dow_chart.png")
    st.divider()
    st.subheader("All strategy results")

    if not df.empty:
        year_cols = [c for c in df.columns if c.isdigit()]
        fmt = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
        st.dataframe(
            colour_returns(df, ["Total Return %"] + year_cols).format(fmt),
            use_container_width=True, hide_index=True, height=420,
        )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**SMA(21,200) — best risk-adjusted strategy**\n\n"
        "+30.6% total return · −10.0% max drawdown · Only 4 trades in 5 years. "
        "Captures 66% of buy-and-hold return while absorbing less than half the drawdown."
    )
    st.warning(
        "**Slow crossovers consistently outperform fast ones**\n\n"
        "50/200 and 21/200 pairs outperform the 9/21, 9/50, and 20/50 pairs on both return "
        "and drawdown. Fast signals (EMA 9-day) add transaction noise without adding edge."
    )
    st.error(
        "**No strategy beats buy-and-hold on raw return**\n\n"
        "The DJIA's sustained uptrend (+46.5% net) penalises strategies that spend time in cash. "
        "MA crossovers earn their keep as drawdown managers, not alpha engines."
    )


# ===========================================================================
# DOW: SCRIPT 2 — MA on 30 Stocks
# ===========================================================================
elif page == "dow_s2":
    st.title("Script 2 — Moving Average Crossover on All 30 DJIA Stocks")
    st.markdown("Same ten strategies applied to each component independently — 330 individual backtests.")

    df = load_csv("ma_backtest_stocks_results.csv")

    if not df.empty:
        bah_avg       = df[df.Strategy == "Buy & Hold"]["Total Return %"].mean()
        strat_avgs    = df[df.Strategy != "Buy & Hold"].groupby("Strategy")["Total Return %"].mean()
        top_strat     = strat_avgs.idxmax()
        top_val       = strat_avgs.max()
        top_combo     = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]

        metric_row([
            ("Avg B&H (30 stocks)",  f"{bah_avg:+.1f}%",                    "Benchmark"),
            ("Best Strategy Avg",    f"{top_val:+.1f}%",                     top_strat),
            ("Top Single Combo",     f"{top_combo['Total Return %']:+.1f}%", f"{top_combo['Ticker']} · {top_combo['Strategy']}"),
            ("Strategies Tested",    "10",                                    "× 30 stocks = 330"),
        ])

    st.divider()
    show_chart("ma_backtest_stocks_chart.png")
    st.divider()
    st.subheader("Results explorer")

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            sel_strat  = st.selectbox("Filter by strategy", ["All"] + sorted(df.Strategy.unique()), key="dow_s2_strat")
        with col2:
            sel_ticker = st.selectbox("Filter by ticker",   ["All"] + sorted(df.Ticker.unique()), key="dow_s2_ticker")

        filtered = df.copy()
        if sel_strat  != "All": filtered = filtered[filtered.Strategy == sel_strat]
        if sel_ticker != "All": filtered = filtered[filtered.Ticker   == sel_ticker]

        year_cols = [c for c in df.columns if c.isdigit()]
        show_cols = ["Ticker", "Strategy", "Total Return %", "Max Drawdown %", "Trades"] + year_cols
        fmt = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}

        st.dataframe(
            colour_returns(filtered[show_cols], ["Total Return %"] + year_cols).format(fmt),
            use_container_width=True, hide_index=True, height=460,
        )
        st.caption(f"Showing {len(filtered)} of {len(df)} rows")

    st.divider()
    st.subheader("Strategy leaderboard (avg across all 30 stocks)")
    if not df.empty:
        lb = df.groupby("Strategy")["Total Return %"].mean().sort_values(ascending=False).reset_index()
        lb.columns = ["Strategy", "Avg Total Return %"]
        st.dataframe(
            lb.style.format({"Avg Total Return %": "{:+.1f}%"})
              .background_gradient(subset=["Avg Total Return %"], cmap="RdYlGn"),
            use_container_width=True, hide_index=True,
        )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**EMA(21,200) best on average — and dominant on NVDA**\n\n"
        "Avg +60.6% across 30 stocks · NVDA+EMA(21,200): +991% in 5 years, just 4 trades. "
        "The 200-day EMA kept exposure during the rally while sidestepping the corrections."
    )
    st.info(
        "**Slow crossovers beat buy-and-hold on 27% of individual stocks**\n\n"
        "SMA(50,200) and SMA(21,200) had the highest hit rate. Goldman Sachs, AXP, and IBM "
        "are among stocks where the MA filter genuinely added value."
    )
    st.error(
        "**The B&H average (+106%) is distorted by NVDA (+1,800%)**\n\n"
        "Remove NVIDIA and the universe average is far more modest. On the median Dow stock, "
        "slow MA crossovers come much closer to matching buy-and-hold."
    )


# ===========================================================================
# DOW: SCRIPT 3 — Earnings Effect
# ===========================================================================
elif page == "dow_s3":
    st.title("Script 3 — Earnings Announcement Effect")
    st.markdown(
        "Five trading windows around each quarterly earnings date for all 30 DJIA stocks. "
        "~600 earnings events."
    )

    df = load_csv("earnings_backtest_results.csv")

    if not df.empty:
        bah_avg      = df[df.Window == "Buy & Hold"]["Total Return %"].mean()
        non_bah      = df[df.Window != "Buy & Hold"]
        best_window  = non_bah.groupby("Window")["Total Return %"].mean().idxmax()
        best_val     = non_bah.groupby("Window")["Total Return %"].mean().max()
        top_combo    = non_bah.sort_values("Total Return %", ascending=False).iloc[0]
        wr_num       = pd.to_numeric(non_bah["Win Rate %"], errors="coerce")
        best_wr_row  = non_bah.loc[wr_num.idxmax()]

        metric_row([
            ("Avg B&H (30 stocks)", f"{bah_avg:+.1f}%",                        "Benchmark"),
            ("Best Window Avg",     f"{best_val:+.1f}%",                        best_window),
            ("Top Combo",           f"{top_combo['Total Return %']:+.1f}%",     f"{top_combo['Ticker']} · {top_combo['Window']}"),
            ("Best Win Rate",       f"{float(best_wr_row['Win Rate %']):.0f}%", f"{best_wr_row['Ticker']} · {best_wr_row['Window']}"),
        ])

    st.divider()
    show_chart("earnings_backtest_chart.png")
    st.divider()
    st.subheader("Results explorer")

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            sel_win  = st.selectbox("Filter by window", ["All"] + [w for w in df.Window.unique() if w != "Buy & Hold"], key="dow_s3_win")
        with col2:
            sel_tick = st.selectbox("Filter by ticker", ["All"] + sorted(df.Ticker.unique()), key="dow_earn_tick")

        filt = df.copy()
        if sel_win  != "All": filt = filt[filt.Window == sel_win]
        if sel_tick != "All": filt = filt[filt.Ticker == sel_tick]

        year_cols = [c for c in df.columns if c.isdigit()]
        show_cols = ["Ticker", "Window", "Total Return %", "Max Drawdown %", "Win Rate %", "Trades"] + year_cols

        st.dataframe(
            filt[show_cols].sort_values("Total Return %", ascending=False),
            use_container_width=True, hide_index=True, height=460,
        )
        st.caption(f"Showing {len(filt)} rows")

    st.divider()
    st.subheader("Window summary (averaged across 30 stocks)")
    if not df.empty:
        non_bah = df[df.Window != "Buy & Hold"]
        summary = non_bah.groupby("Window").agg(
            Avg_Return  =("Total Return %", "mean"),
            Avg_MaxDD   =("Max Drawdown %", "mean"),
            Avg_WinRate =("Win Rate %", lambda x: pd.to_numeric(x, errors="coerce").mean()),
            Total_Events=("Trades", "sum"),
        ).reset_index()
        summary["Avg_Return"]   = summary["Avg_Return"].map(lambda x: f"{x:+.1f}%")
        summary["Avg_MaxDD"]    = summary["Avg_MaxDD"].map(lambda x: f"{x:.1f}%")
        summary["Avg_WinRate"]  = summary["Avg_WinRate"].map(lambda x: f"{x:.1f}%")
        st.dataframe(summary, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**PEAD-Long [+1,+20] — the strongest earnings window**\n\n"
        "Avg +23.4% compounded · 57.1% win rate · +1.19% per event across ~600 earnings dates. "
        "Post-Earnings Announcement Drift is alive and well in Dow components."
    )
    st.success(
        "**Goldman Sachs — best single stock for earnings strategies**\n\n"
        "GS PEAD-Long: +158.7% · 70% win rate · −10.7% max drawdown. "
        "JPMorgan: +82.6%, 75% win rate. Financial sector shows the strongest drift effect."
    )
    st.error(
        "**Announcement day is a coin flip**\n\n"
        "Holding over the earnings print (−1 to +1) returned +3.2% average with a 51.7% win rate. "
        "If you're trading the reaction on the day, you're not trading PEAD — you're gambling."
    )


# ===========================================================================
# DOW: SCRIPT 4 — Economic Calendar
# ===========================================================================
elif page == "dow_s4":
    st.title("Script 4 — Economic Calendar Event Backtest")
    st.markdown(
        "CPI, NFP, GDP, FOMC × five trading windows applied to ^DJI. "
        "20 strategy combinations across 180 events."
    )

    df = load_csv("economic_calendar_backtest_results.csv")

    if not df.empty:
        bah_row   = df[df.Window == "Buy & Hold"].iloc[0]
        non_bah   = df[df.Window != "Buy & Hold"].copy()
        non_bah["Win Rate %"] = pd.to_numeric(non_bah["Win Rate %"], errors="coerce")
        best_row  = non_bah.sort_values("Total Return %", ascending=False).iloc[0]
        worst_row = non_bah.sort_values("Total Return %").iloc[0]
        best_wr   = non_bah.sort_values("Win Rate %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold",       f"{bah_row['Total Return %']:+.1f}%",  "Benchmark"),
            ("Best Strategy",    f"{best_row['Total Return %']:+.1f}%", f"{best_row['Event Type']} {best_row['Window']}"),
            ("Highest Win Rate", f"{best_wr['Win Rate %']:.0f}%",       f"{best_wr['Event Type']} {best_wr['Window']}"),
            ("Worst Strategy",   f"{worst_row['Total Return %']:+.1f}%",f"{worst_row['Event Type']} {worst_row['Window']}"),
        ])

    st.divider()
    show_chart("economic_calendar_backtest_chart.png")
    st.divider()
    st.subheader("Full results by event type")

    if not df.empty:
        for tab, name in zip(st.tabs(["All", "CPI", "NFP", "GDP", "FOMC"]),
                             ["All", "CPI", "NFP", "GDP", "FOMC"]):
            with tab:
                subset    = df if name == "All" else df[(df["Event Type"] == name) | (df["Window"] == "Buy & Hold")]
                year_cols = [c for c in df.columns if c.isdigit()]
                show_cols = ["Event Type", "Window", "Total Return %", "Max Drawdown %", "Win Rate %", "Events"] + year_cols
                fmt       = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
                st.dataframe(
                    colour_returns(subset[show_cols], ["Total Return %"] + year_cols).format(fmt),
                    use_container_width=True, hide_index=True,
                )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**FOMC Post-Long [+1,+10] — the standout macro strategy**\n\n"
        "+37.7% over 5 years · 70% win rate · 40 events. In the market ~32% of available "
        "trading days, capturing 81% of buy-and-hold return. The 10 days after a Fed decision "
        "are consistently positive regardless of whether the Fed hiked, cut, or held."
    )
    st.success(
        "**GDP Post-Long has the highest win rate of any strategy in the study**\n\n"
        "75% win rate · +20.8% compounded · +1.04% per event. Quarterly GDP data drives "
        "sustained positioning adjustments over the following two weeks."
    )
    st.error(
        "**NFP Pre-window: the worst strategy in the entire study**\n\n"
        "−15.3% over 5 years · Only 35% win rate across 60 events. The Dow systematically "
        "sells off in the two days before Non-Farm Payrolls — institutional de-risking, not informed positioning."
    )
    st.warning(
        "**CPI day-of: five years of inflation headlines, net result = noise**\n\n"
        "60 CPI releases · +0.1% total · 51.7% win rate. The dominant macro narrative of "
        "2022–2024 generated essentially zero directional edge on announcement day."
    )


# ===========================================================================
# DOW: ARTICLES
# ===========================================================================
elif page == "dow_articles":
    st.title("Research Articles")
    st.markdown("Three articles from the same data — each targeting a different audience and format.")

    tab_medium, tab_substack, tab_ssrn = st.tabs([
        "📰  Medium — General Audience",
        "✉️  Substack — Newsletter",
        "🎓  SSRN — Academic Paper",
    ])

    with tab_medium:
        with st.container():
            st.markdown(load_article(ARTICLES, "medium_article.md"))

    with tab_substack:
        with st.container():
            st.markdown(load_article(ARTICLES, "substack_article.md"))

    with tab_ssrn:
        with st.container():
            st.markdown(load_article(ARTICLES, "ssrn_paper.md"))


# ===========================================================================
# DAX: OVERVIEW
# ===========================================================================
elif page == "dax_overview":
    st.title("DAX 40 Strategy Backtest Research")
    st.markdown(
        "The same systematic study — **four strategy classes** plus a seasonality pass — "
        "flexed for Germany's DAX 40 and its 40 component stocks over five years, "
        "with macro events swapped for their German/Eurozone equivalents (ECB, Destatis, "
        "Bundesagentur für Arbeit)."
    )
    st.divider()

    metric_row([
        ("Backtest Period",      "Jul 2021 – Jul 2026", "5 years"),
        ("Stocks Covered",       "40 DAX Components",   "Plus ^GDAXI index"),
        ("Individual Backtests", "700+",                "Strategies tested"),
        ("DAX Buy & Hold",       "+61.8%",               "Benchmark return"),
    ])

    st.divider()
    st.subheader("What was tested")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Script 1 — MA on ^GDAXI Index**
- 10 crossover strategies (SMA + EMA)
- Pairs: (9/21), (20/50), (50/200), (9/50), (21/200)
- Long only, signal lagged 1 day

**Script 2 — MA on 40 Stocks**
- Same 10 strategies on each DAX 40 component
- 440 individual backtests
""")
    with col2:
        st.markdown("""
**Script 3 — Earnings Effect**
- 5 windows around each quarterly earnings date
- Pre-drift, announcement, PEAD-Short, PEAD-Long, Full
- ~700 events across 36 stocks with earnings data

**Script 4 — Economic Calendar (German/ECB)**
- German CPI, German unemployment, German GDP, ECB rate decisions
- 5 entry/exit windows per event type
- 60 CPI · 60 Unemployment · 20 GDP · 40 ECB events
""")

    st.divider()
    st.subheader("Key findings at a glance")

    findings = pd.DataFrame([
        {"Script": "MA — DAX Index",     "Best Strategy": "SMA(50,200)",
         "Return": "+50.2%", "vs Buy & Hold": "+61.8%",
         "Key Insight": "Cuts max drawdown by ~39% (−16.0% vs −26.4%) at 81% of B&H return"},
        {"Script": "MA — 40 Stocks",     "Best Strategy": "EMA(50,200) avg",
         "Return": "+92.1%", "vs Buy & Hold": "+101.1% avg",
         "Key Insight": "Rheinmetall+EMA(50,200) = +1,724% — actually beats its own +1,199% B&H"},
        {"Script": "Earnings Effect",    "Best Strategy": "PEAD-Long [+1,+20]",
         "Return": "+19.9% avg", "vs Buy & Hold": "+101.1% avg",
         "Key Insight": "53.5% win rate · Siemens Energy Full window: +147.6%, 65% win rate"},
        {"Script": "Economic Calendar",  "Best Strategy": "Unemployment Post-Long [+1,+10]",
         "Return": "+38.8%", "vs Buy & Hold": "+61.8%",
         "Key Insight": "58.3% win rate · GDP post-long: 70% win rate, highest in study"},
    ])
    st.dataframe(findings, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("The central finding")

    st.success(
        "**Post-event drift replicates almost exactly across the Atlantic.**\n\n"
        "Every one of the four German/Eurozone macro event types (CPI, unemployment, GDP, ECB) "
        "shows its Post-Long [+1,+10] window as the single best-performing strategy — the same "
        "shape as the Dow's FOMC/CPI/NFP/GDP result, reproduced under a different central bank "
        "and a different statistical agency."
    )
    st.info(
        "**One result the Dow study never produced: a moving average beating buy-and-hold outright.**\n\n"
        "Rheinmetall returned +1,199% buy-and-hold on defense-sector re-rating. A 2-trade "
        "EMA(50,200) crossover on it returned +1,724% — sidestepping one sharp intermediate "
        "drawdown and riding the recovery from a lower re-entry price. No leverage, no shorting."
    )
    st.warning(
        "**Moving average crossovers still don't beat buy-and-hold on the index — but cut drawdown ~39%.**\n\n"
        "SMA(50,200) returned +50.2% vs +61.8% for B&H, with a max drawdown of −16.0% vs −26.4%. "
        "Only 3 trades in 5 years. Same risk-management framing as the Dow."
    )


# ===========================================================================
# DAX: SCRIPT 1 — MA on ^GDAXI
# ===========================================================================
elif page == "dax_s1":
    st.title("Script 1 — Moving Average Crossover on ^GDAXI")
    st.markdown(
        "Ten SMA and EMA crossover strategies on the DAX 40 index, five-year backtest."
    )

    df = load_csv("ma_backtest_dax_results.csv")

    if not df.empty:
        bah     = df[df.Strategy == "Buy & Hold"].iloc[0]
        best    = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]
        best_dd = df[df.Strategy != "Buy & Hold"].sort_values("Max Drawdown %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold Return",    f"{bah['Total Return %']:+.1f}%",    "Benchmark"),
            ("Best Strategy Return", f"{best['Total Return %']:+.1f}%",   best["Strategy"]),
            ("Lowest Max Drawdown",  f"{best_dd['Max Drawdown %']:.1f}%", best_dd["Strategy"]),
            ("B&H Max Drawdown",     f"{bah['Max Drawdown %']:.1f}%",     "Benchmark"),
        ])

    st.divider()
    show_chart("ma_backtest_dax_chart.png")
    st.divider()
    st.subheader("All strategy results")

    if not df.empty:
        year_cols = [c for c in df.columns if c.isdigit()]
        fmt = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
        st.dataframe(
            colour_returns(df, ["Total Return %"] + year_cols).format(fmt),
            use_container_width=True, hide_index=True, height=420,
        )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**SMA(50,200) — best risk-adjusted strategy**\n\n"
        "+50.2% total return · −16.0% max drawdown · Only 3 trades in 5 years. "
        "Captures 81% of buy-and-hold return while cutting drawdown by ~39%."
    )
    st.warning(
        "**All three 200-day-anchored strategies converge on the same drawdown**\n\n"
        "SMA(50,200), SMA(21,200), and EMA(50,200) all cap max drawdown at exactly −16.0% — "
        "each one avoided the same event: the 2022 European energy-price shock selloff."
    )
    st.error(
        "**No strategy beats buy-and-hold on the index itself**\n\n"
        "The DAX's sustained five-year run (+61.8% net) still penalises strategies that spend "
        "time in cash. On the index, MA crossovers remain drawdown managers, not alpha engines."
    )


# ===========================================================================
# DAX: SCRIPT 2 — MA on 40 Stocks
# ===========================================================================
elif page == "dax_s2":
    st.title("Script 2 — Moving Average Crossover on All 40 DAX Stocks")
    st.markdown("Same ten strategies applied to each component independently — 440 individual backtests.")

    df = load_csv("ma_backtest_stocks_dax_results.csv")

    if not df.empty:
        bah_avg       = df[df.Strategy == "Buy & Hold"]["Total Return %"].mean()
        strat_avgs    = df[df.Strategy != "Buy & Hold"].groupby("Strategy")["Total Return %"].mean()
        top_strat     = strat_avgs.idxmax()
        top_val       = strat_avgs.max()
        top_combo     = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]

        metric_row([
            ("Avg B&H (40 stocks)",  f"{bah_avg:+.1f}%",                    "Benchmark"),
            ("Best Strategy Avg",    f"{top_val:+.1f}%",                     top_strat),
            ("Top Single Combo",     f"{top_combo['Total Return %']:+.1f}%", f"{top_combo['Ticker']} · {top_combo['Strategy']}"),
            ("Strategies Tested",    "10",                                    "× 40 stocks = 440"),
        ])

    st.divider()
    show_chart("ma_backtest_stocks_dax_chart.png")
    st.divider()
    st.subheader("Results explorer")

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            sel_strat  = st.selectbox("Filter by strategy", ["All"] + sorted(df.Strategy.unique()), key="dax_s2_strat")
        with col2:
            sel_ticker = st.selectbox("Filter by ticker",   ["All"] + sorted(df.Ticker.unique()), key="dax_s2_ticker")

        filtered = df.copy()
        if sel_strat  != "All": filtered = filtered[filtered.Strategy == sel_strat]
        if sel_ticker != "All": filtered = filtered[filtered.Ticker   == sel_ticker]

        year_cols = [c for c in df.columns if c.isdigit()]
        show_cols = ["Ticker", "Strategy", "Total Return %", "Max Drawdown %", "Trades"] + year_cols
        fmt = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}

        st.dataframe(
            colour_returns(filtered[show_cols], ["Total Return %"] + year_cols).format(fmt),
            use_container_width=True, hide_index=True, height=460,
        )
        st.caption(f"Showing {len(filtered)} of {len(df)} rows")

    st.divider()
    st.subheader("Strategy leaderboard (avg across all 40 stocks)")
    if not df.empty:
        lb = df.groupby("Strategy")["Total Return %"].mean().sort_values(ascending=False).reset_index()
        lb.columns = ["Strategy", "Avg Total Return %"]
        st.dataframe(
            lb.style.format({"Avg Total Return %": "{:+.1f}%"})
              .background_gradient(subset=["Avg Total Return %"], cmap="RdYlGn"),
            use_container_width=True, hide_index=True,
        )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**EMA(50,200) beats Rheinmetall's own buy-and-hold — a first in this research series**\n\n"
        "Rheinmetall (RHM.DE) buy-and-hold: +1,199%. EMA(50,200) on the same stock: +1,724%, "
        "using just 2 trades. Sidestepping one deep intermediate drawdown and re-entering before "
        "the recovery can out-compound continuous holding — no leverage required."
    )
    st.info(
        "**SMA(50,200) beats buy-and-hold on 50% of DAX stocks — the highest hit rate in either study**\n\n"
        "Nearly double the Dow's equivalent hit rate (27%). Siemens Energy is the other standout: "
        "SMA(21,200) returned +855% against a +585% buy-and-hold on the same stock."
    )
    st.error(
        "**The B&H average (+101%) is distorted by one theme, not one stock**\n\n"
        "Rheinmetall and Siemens Energy both rode Europe's 2022–2025 defense/energy re-rating. "
        "Remove them and the DAX 40's average buy-and-hold return looks far more ordinary."
    )


# ===========================================================================
# DAX: SCRIPT 3 — Earnings Effect
# ===========================================================================
elif page == "dax_s3":
    st.title("Script 3 — Earnings Announcement Effect")
    st.markdown(
        "Five trading windows around each quarterly earnings date for 36 of the 40 DAX stocks "
        "(4 constituents had no earnings-date data available)."
    )

    df = load_csv("earnings_backtest_dax_results.csv")

    if not df.empty:
        bah_avg      = df[df.Window == "Buy & Hold"]["Total Return %"].mean()
        non_bah      = df[df.Window != "Buy & Hold"]
        best_window  = non_bah.groupby("Window")["Total Return %"].mean().idxmax()
        best_val     = non_bah.groupby("Window")["Total Return %"].mean().max()
        top_combo    = non_bah.sort_values("Total Return %", ascending=False).iloc[0]
        wr_num       = pd.to_numeric(non_bah["Win Rate %"], errors="coerce")
        best_wr_row  = non_bah.loc[wr_num.idxmax()]

        metric_row([
            ("Avg B&H (40 stocks)", f"{bah_avg:+.1f}%",                        "Benchmark"),
            ("Best Window Avg",     f"{best_val:+.1f}%",                        best_window),
            ("Top Combo",           f"{top_combo['Total Return %']:+.1f}%",     f"{top_combo['Ticker']} · {top_combo['Window']}"),
            ("Best Win Rate",       f"{float(best_wr_row['Win Rate %']):.0f}%", f"{best_wr_row['Ticker']} · {best_wr_row['Window']}"),
        ])

    st.divider()
    show_chart("earnings_backtest_dax_chart.png")
    st.divider()
    st.subheader("Results explorer")

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            sel_win  = st.selectbox("Filter by window", ["All"] + [w for w in df.Window.unique() if w != "Buy & Hold"], key="dax_s3_win")
        with col2:
            sel_tick = st.selectbox("Filter by ticker", ["All"] + sorted(df.Ticker.unique()), key="dax_earn_tick")

        filt = df.copy()
        if sel_win  != "All": filt = filt[filt.Window == sel_win]
        if sel_tick != "All": filt = filt[filt.Ticker == sel_tick]

        year_cols = [c for c in df.columns if c.isdigit()]
        show_cols = ["Ticker", "Window", "Total Return %", "Max Drawdown %", "Win Rate %", "Trades"] + year_cols

        st.dataframe(
            filt[show_cols].sort_values("Total Return %", ascending=False),
            use_container_width=True, hide_index=True, height=460,
        )
        st.caption(f"Showing {len(filt)} rows")

    st.divider()
    st.subheader("Window summary (averaged across 40 stocks)")
    if not df.empty:
        non_bah = df[df.Window != "Buy & Hold"]
        summary = non_bah.groupby("Window").agg(
            Avg_Return  =("Total Return %", "mean"),
            Avg_MaxDD   =("Max Drawdown %", "mean"),
            Avg_WinRate =("Win Rate %", lambda x: pd.to_numeric(x, errors="coerce").mean()),
            Total_Events=("Trades", "sum"),
        ).reset_index()
        summary["Avg_Return"]   = summary["Avg_Return"].map(lambda x: f"{x:+.1f}%")
        summary["Avg_MaxDD"]    = summary["Avg_MaxDD"].map(lambda x: f"{x:.1f}%")
        summary["Avg_WinRate"]  = summary["Avg_WinRate"].map(lambda x: f"{x:.1f}%")
        st.dataframe(summary, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**PEAD-Long [+1,+20] — the strongest earnings window, same as the Dow**\n\n"
        "Avg +19.9% compounded · 53.5% win rate · +0.88% per event across 40 DAX stocks. "
        "Post-Earnings Announcement Drift travels intact from Wall Street to Frankfurt."
    )
    st.success(
        "**Siemens Energy and Infineon — best individual stocks for earnings strategies**\n\n"
        "Siemens Energy Full window: +147.6%, 65% win rate. Infineon Full window: +136.3%, "
        "70% win rate. Commerzbank hit 73.7% win rate — the highest in the whole study."
    )
    st.error(
        "**Announcement day is a coin flip, exactly as on the Dow**\n\n"
        "Holding over the earnings print (−1 to +1) returned +1.3% average with a 52.3% win rate. "
        "The print itself is priced in almost immediately; the drift is where the edge lives."
    )


# ===========================================================================
# DAX: SCRIPT 4 — Economic Calendar
# ===========================================================================
elif page == "dax_s4":
    st.title("Script 4 — Economic Calendar Event Backtest (German / ECB)")
    st.markdown(
        "German CPI, German unemployment, German GDP, ECB rate decisions × five trading "
        "windows applied to ^GDAXI — the German/Eurozone equivalents of the Dow study's "
        "CPI/NFP/GDP/FOMC calendar."
    )

    df = load_csv("economic_calendar_backtest_dax_results.csv")

    if not df.empty:
        bah_row   = df[df.Window == "Buy & Hold"].iloc[0]
        non_bah   = df[df.Window != "Buy & Hold"].copy()
        non_bah["Win Rate %"] = pd.to_numeric(non_bah["Win Rate %"], errors="coerce")
        best_row  = non_bah.sort_values("Total Return %", ascending=False).iloc[0]
        worst_row = non_bah.sort_values("Total Return %").iloc[0]
        best_wr   = non_bah.sort_values("Win Rate %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold",       f"{bah_row['Total Return %']:+.1f}%",  "Benchmark"),
            ("Best Strategy",    f"{best_row['Total Return %']:+.1f}%", f"{best_row['Event Type']} {best_row['Window']}"),
            ("Highest Win Rate", f"{best_wr['Win Rate %']:.0f}%",       f"{best_wr['Event Type']} {best_wr['Window']}"),
            ("Worst Strategy",   f"{worst_row['Total Return %']:+.1f}%",f"{worst_row['Event Type']} {worst_row['Window']}"),
        ])

    st.divider()
    show_chart("economic_calendar_backtest_dax_chart.png")
    st.divider()
    st.subheader("Full results by event type")

    if not df.empty:
        for tab, name in zip(st.tabs(["All", "CPI", "UNEMP", "GDP", "ECB"]),
                             ["All", "CPI", "UNEMP", "GDP", "ECB"]):
            with tab:
                subset    = df if name == "All" else df[(df["Event Type"] == name) | (df["Window"] == "Buy & Hold")]
                year_cols = [c for c in df.columns if c.isdigit()]
                show_cols = ["Event Type", "Window", "Total Return %", "Max Drawdown %", "Win Rate %", "Events"] + year_cols
                fmt       = {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
                st.dataframe(
                    colour_returns(subset[show_cols], ["Total Return %"] + year_cols).format(fmt),
                    use_container_width=True, hide_index=True,
                )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**German Unemployment Post-Long [+1,+10] — the standout macro strategy**\n\n"
        "+38.8% over 5 years · 58.3% win rate · 60 events. The closest German equivalent to "
        "US Non-Farm Payrolls, and — unlike the Dow's NFP result — this is the *best* window, "
        "not the worst."
    )
    st.success(
        "**GDP Post-Long has the highest win rate of any strategy in the study**\n\n"
        "70% win rate · +29.0% compounded, on just 20 events. German GDP flash estimates drive "
        "sustained positioning adjustments over the following two weeks, same as the Dow's GDP result."
    )
    st.error(
        "**ECB Day-of is the worst-performing ECB window**\n\n"
        "−4.2% over 5 years · 57.5% win rate across 40 events — dragged down almost entirely by "
        "2022 (−11.1%), the year of the ECB's first hawkish pivot and largest single-meeting hikes "
        "in its history."
    )
    st.warning(
        "**Post-event drift dominates every single German/ECB event type tested**\n\n"
        "CPI, Unemployment, GDP, and ECB all show their Post-Long [+1,+10] window as the single "
        "best-performing strategy — the cleanest cross-market confirmation of the Dow study's "
        "central finding: markets drift after scheduled news, not on it."
    )


# ===========================================================================
# DAX: SEASONAL ANALYSIS
# ===========================================================================
elif page == "dax_seasonal":
    st.title("Seasonal Analysis — Day-of-Week & Month-of-Year")
    st.markdown(
        "Ten years of ^GDAXI daily data (Jul 2016 – Jul 2026), broken down by weekday and "
        "calendar month, plus two mechanical calendar-timing strategies tested against buy-and-hold."
    )

    df = load_csv("seasonal_analysis_dax_results.csv")

    if not df.empty:
        dow_df   = df[df.Section == "Day of Week"]
        month_df = df[df.Section == "Month of Year"]
        strat_df = df[df.Section == "Strategy Comparison"]

        best_day    = dow_df.sort_values("Avg Return %", ascending=False).iloc[0]
        best_month  = month_df.sort_values("Avg Return %", ascending=False).iloc[0]
        bah_row     = strat_df[strat_df.Strategy == "Buy & Hold"].iloc[0]
        best_day_strat = strat_df[strat_df.Strategy.str.contains("Best Day")].iloc[0]

        metric_row([
            ("Best Day",           f"{best_day['Day']}",             f"{best_day['Avg Return %']:+.4f}% avg"),
            ("Best Month",         f"{best_month['Month']}",         f"{best_month['Avg Return %']:+.4f}% avg"),
            ("Best-Day Strategy",  f"{best_day_strat['Total Return %']:+.2f}%", "Mechanical, 511 trades"),
            ("10-Year Buy & Hold", f"{bah_row['Total Return %']:+.2f}%",        "Benchmark"),
        ])

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        show_chart("seasonal_analysis_dax_chart1_dow.png")
    with col2:
        show_chart("seasonal_analysis_dax_chart2_month.png")
    col3, col4 = st.columns(2)
    with col3:
        show_chart("seasonal_analysis_dax_chart3_dow_year.png")
    with col4:
        show_chart("seasonal_analysis_dax_chart4_month_year.png")

    st.divider()
    st.subheader("Day-of-week and month-of-year results")

    if not df.empty:
        tab_dow, tab_month, tab_strat = st.tabs(["Day of Week", "Month of Year", "Strategy Comparison"])
        with tab_dow:
            st.dataframe(
                dow_df[["Rank", "Day", "Avg Return %", "Win Rate %", "Median Return %", "Std Dev %", "Count"]],
                use_container_width=True, hide_index=True,
            )
        with tab_month:
            st.dataframe(
                month_df[["Rank", "Month", "Avg Return %", "Win Rate %", "Median Return %", "Std Dev %", "Count"]],
                use_container_width=True, hide_index=True,
            )
        with tab_strat:
            st.dataframe(
                strat_df[["Strategy", "Total Return %", "Win Rate %", "# Trades", "vs B&H (pp)"]],
                use_container_width=True, hide_index=True,
            )

    st.divider()
    st.subheader("Key findings")
    st.success(
        "**Tuesday and Wednesday are the DAX's strongest days; Thursday its weakest**\n\n"
        "Tuesday: +0.1074% avg, 54.4% win rate. Wednesday: +0.1064% avg, 55.3% win rate. "
        "Thursday: −0.0404% avg — the only clearly negative weekday over ten years."
    )
    st.success(
        "**April is the DAX's strongest month — ahead of the classic Santa Claus rally months**\n\n"
        "April: +0.1461% avg daily return, 57.1% win rate — narrowly ahead of November (+0.1402%) "
        "and January (+0.0948%)."
    )
    st.error(
        "**Trading the single best day of the week loses money**\n\n"
        "Buying the open and selling the close every Tuesday for 10 years returned **−8.00%** "
        "despite a 54.4% win rate — badly trailing buy-and-hold's +153.22%. A positive average "
        "return and a win rate above 50% do not guarantee a profitable compounded strategy once "
        "variance is taken into account across 511 trades."
    )
    st.warning(
        "**The best-month strategy fares better but still loses to doing nothing**\n\n"
        "Buying the open of April 1st and selling the close of April's last day, every year for "
        "10 years, returned +29.06% at an 80% win rate across just 10 trades — cleaner than the "
        "Tuesday strategy, but still far behind buy-and-hold's +153.22%."
    )


# ===========================================================================
# DAX: ARTICLES
# ===========================================================================
elif page == "dax_articles":
    st.title("Research Articles")
    st.markdown("DAX research is split into two studies, each written up in three formats.")

    study = st.radio(
        "Study", ["📊  Full Study (MA / Stocks / Earnings / Macro)", "🗓️  Seasonal Analysis"],
        horizontal=True,
    )
    st.divider()

    article_dir = DAX_FULL_ARTICLES if study.startswith("📊") else DAX_ARTICLES

    tab_medium, tab_substack, tab_ssrn = st.tabs([
        "📰  Medium — General Audience",
        "✉️  Substack — Newsletter",
        "🎓  SSRN — Academic Paper",
    ])

    with tab_medium:
        with st.container():
            st.markdown(load_article(article_dir, "medium_article.md"))

    with tab_substack:
        with st.container():
            st.markdown(load_article(article_dir, "substack_article.md"))

    with tab_ssrn:
        with st.container():
            st.markdown(load_article(article_dir, "ssrn_paper.md"))
