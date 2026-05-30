"""
DJIA Strategy Backtest — Streamlit Showcase App

Presents results from four systematic backtesting scripts on the
Dow Jones Industrial Average and its 30 component stocks.
"""

import os
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
OUTPUTS  = BASE_DIR / "outputs"
ARTICLES = BASE_DIR / "articles"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DJIA Backtest Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Sidebar nav links */
    section[data-testid="stSidebar"] { background-color: #0d1117; }
    section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #8b949e !important; }
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; }

    /* Section header rule */
    hr { border-color: #30363d; }

    /* Finding callout boxes */
    .finding-box {
        background: #161b22;
        border-left: 4px solid #58a6ff;
        border-radius: 4px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .finding-positive { border-left-color: #3fb950; }
    .finding-negative { border-left-color: #f85149; }
    .finding-neutral  { border-left-color: #ffa657; }

    /* Article rendering */
    .article-body { max-width: 740px; line-height: 1.75; font-size: 1.0rem; }
    .article-body h1 { font-size: 1.8rem; margin-bottom: 0.3rem; }
    .article-body h2 { font-size: 1.3rem; margin-top: 1.6rem; }
    .article-body blockquote {
        border-left: 3px solid #58a6ff;
        padding-left: 14px;
        color: #8b949e;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@st.cache_data
def load_csv(name):
    path = OUTPUTS / name
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def metric_row(items):
    """items = list of (label, value, delta) tuples."""
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)


def show_chart(name, caption=None):
    path = OUTPUTS / name
    if path.exists():
        st.image(str(path), use_container_width=True, caption=caption or "")
    else:
        st.warning(f"Chart not found: {name}. Run the corresponding script first.")


def fmt_pct(val):
    try:
        v = float(val)
        return f"{v:+.1f}%"
    except Exception:
        return str(val)


def colour_return(val):
    try:
        v = float(val)
        if v > 0:
            return "color: #3fb950"
        elif v < 0:
            return "color: #f85149"
    except Exception:
        pass
    return ""


def load_article(filename):
    path = ARTICLES / filename
    if path.exists():
        return path.read_text()
    return "_Article file not found._"


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
PAGES = {
    "🏠  Overview":                  "overview",
    "📈  Script 1 — MA on DJIA":     "s1",
    "📊  Script 2 — MA on 30 Stocks":"s2",
    "💼  Script 3 — Earnings Effect": "s3",
    "📅  Script 4 — Economic Calendar":"s4",
    "📝  Research Articles":          "articles",
}

with st.sidebar:
    st.markdown("## 📈 DJIA Backtest\n*Systematic research on the Dow*")
    st.markdown("---")
    selected = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.caption(
        "Backtest period: Jun 2021 – May 2026  \n"
        "Data: yfinance · Long only · No costs  \n"
        "Capital: $10,000 per strategy"
    )

page = PAGES[selected]


# ===========================================================================
# OVERVIEW
# ===========================================================================
if page == "overview":
    st.title("DJIA Strategy Backtest Research")
    st.markdown(
        "A systematic empirical study across **four strategy classes** applied to the "
        "Dow Jones Industrial Average and its 30 component stocks over five years."
    )

    st.markdown("---")

    # Top-line numbers
    metric_row([
        ("Backtest Period",       "Jun 2021 – May 2026", "5 years"),
        ("Stocks Covered",        "30 DJIA Components",  "Plus ^DJI index"),
        ("Individual Backtests",  "1,200+",              "Strategies tested"),
        ("DJIA Buy & Hold",       "+46.5%",              "Benchmark return"),
    ])

    st.markdown("---")
    st.subheader("What was tested")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Script 1 — MA on DJIA Index**
- 10 crossover strategies (SMA + EMA)
- Pairs: (9/21), (20/50), (50/200), (9/50), (21/200)
- Long only, signal lagged 1 day

**Script 2 — MA on 30 Stocks**
- Same 10 strategies applied to each DJIA component
- 330 individual backtests
- Aggregated by strategy + individual stock detail
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
- 60 CPI, 60 NFP, 20 GDP, 40 FOMC events
""")

    st.markdown("---")
    st.subheader("Key findings at a glance")

    findings = pd.DataFrame([
        {
            "Script": "MA — DJIA Index",
            "Best Strategy":     "SMA(21,200)",
            "Return":            "+30.6%",
            "vs Buy & Hold":     "+46.5%",
            "Key Insight":       "Halves max drawdown (-10% vs -22%) at ⅔ of B&H return"
        },
        {
            "Script": "MA — 30 Stocks",
            "Best Strategy":     "EMA(21,200) avg",
            "Return":            "+60.6%",
            "vs Buy & Hold":     "+106.3% avg",
            "Key Insight":       "NVDA+EMA(21,200) = +991%; slow MAs dominate on trending stocks"
        },
        {
            "Script": "Earnings Effect",
            "Best Strategy":     "PEAD-Long [+1,+20]",
            "Return":            "+23.4% avg",
            "vs Buy & Hold":     "+106.3% avg",
            "Key Insight":       "57% win rate, +1.19%/event · GS alone: +159%, 70% win rate"
        },
        {
            "Script": "Economic Calendar",
            "Best Strategy":     "FOMC Post-Long [+1,+10]",
            "Return":            "+37.7%",
            "vs Buy & Hold":     "+46.5%",
            "Key Insight":       "70% win rate over 40 Fed decisions · GDP post-long: 75% win rate"
        },
    ])
    st.dataframe(findings, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("The central finding")
    st.markdown("""
<div class="finding-box finding-positive">
<strong>Post-event drift is the most consistent source of edge across every strategy class.</strong><br>
Whether from earnings (PEAD), FOMC decisions, or NFP releases — markets appear to underprice
the follow-through. The announcement itself is processed almost immediately; the residual
adjustment over the following 5–20 trading days is where measurable signal exists.
</div>

<div class="finding-box finding-negative">
<strong>Pre-NFP positioning is the worst identifiable strategy in the entire study.</strong><br>
Owning the Dow in the two days before each jobs report returned –15.3% over 60 events (35% win rate).
The market systematically de-risks ahead of scheduled uncertainty.
</div>

<div class="finding-box finding-neutral">
<strong>Moving average crossovers don't beat buy-and-hold — but they cut drawdowns in half.</strong><br>
The SMA(21,200) returned +30.6% vs +46.5% for B&H, with a max drawdown of just –10.0% vs –21.9%.
Four trades in five years. The right framing is risk management, not alpha generation.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# SCRIPT 1 — MA on DJIA
# ===========================================================================
elif page == "s1":
    st.title("Script 1 — Moving Average Crossover on ^DJI")
    st.markdown(
        "Ten SMA and EMA crossover strategies tested on the Dow Jones Industrial Average "
        "index over a five-year period."
    )

    df = load_csv("ma_backtest_dow_results.csv")

    if not df.empty:
        bah = df[df.Strategy == "Buy & Hold"].iloc[0]
        best = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]
        best_dd = df[df.Strategy != "Buy & Hold"].sort_values("Max Drawdown %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold Return",     f"{bah['Total Return %']:+.1f}%",   "Benchmark"),
            ("Best Strategy Return",  f"{best['Total Return %']:+.1f}%",  best["Strategy"]),
            ("Lowest Drawdown",       f"{best_dd['Max Drawdown %']:.1f}%",best_dd["Strategy"]),
            ("Buy & Hold Max DD",     f"{bah['Max Drawdown %']:.1f}%",    "Benchmark"),
        ])

    st.markdown("---")
    show_chart("ma_backtest_dow_chart.png")

    st.markdown("---")
    st.subheader("All strategy results")

    if not df.empty:
        year_cols = [c for c in df.columns if c.isdigit()]

        def highlight(row):
            is_bah = row["Strategy"] == "Buy & Hold"
            styles = []
            for col in row.index:
                if col in ["Total Return %"] + year_cols:
                    try:
                        v = float(row[col])
                        if is_bah:
                            styles.append("font-weight: bold; color: #58a6ff")
                        elif v > 0:
                            styles.append("color: #3fb950")
                        else:
                            styles.append("color: #f85149")
                    except Exception:
                        styles.append("")
                elif col == "Max Drawdown %":
                    try:
                        v = float(row[col])
                        styles.append("color: #ffa657" if v < -15 else "")
                    except Exception:
                        styles.append("")
                else:
                    styles.append("")
            return styles

        st.dataframe(
            df.style.apply(highlight, axis=1).format(
                {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
            ),
            use_container_width=True,
            hide_index=True,
            height=420,
        )

    st.markdown("---")
    st.subheader("Key findings")
    st.markdown("""
<div class="finding-box finding-positive">
<strong>SMA(21,200) — best risk-adjusted strategy</strong><br>
+30.6% total return · −10.0% max drawdown · Only 4 trades in 5 years.<br>
Captures 66% of buy-and-hold return while absorbing less than half the drawdown.
</div>

<div class="finding-box finding-neutral">
<strong>Slow crossovers consistently outperform fast ones</strong><br>
50/200 and 21/200 pairs outperform the 9/21, 9/50, and 20/50 pairs on both return and drawdown.
High-frequency signals (EMA 9-day) add transaction noise without adding edge.
</div>

<div class="finding-box finding-negative">
<strong>No strategy beats buy-and-hold on raw return</strong><br>
The DJIA's sustained uptrend (2021–2026 net +46.5%) penalises strategies that spend
time in cash. The MA crossover earns its keep as a drawdown manager, not an alpha engine.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# SCRIPT 2 — MA on 30 Stocks
# ===========================================================================
elif page == "s2":
    st.title("Script 2 — Moving Average Crossover on All 30 DJIA Stocks")
    st.markdown(
        "Same ten crossover strategies applied to each of the 30 Dow component stocks independently. "
        "330 individual backtests."
    )

    df = load_csv("ma_backtest_stocks_results.csv")

    if not df.empty:
        bah_avg = df[df.Strategy == "Buy & Hold"]["Total Return %"].mean()
        best_strat_avg = df[df.Strategy != "Buy & Hold"].groupby("Strategy")["Total Return %"].mean()
        top_strat = best_strat_avg.idxmax()
        top_val   = best_strat_avg.max()
        top_combo = df[df.Strategy != "Buy & Hold"].sort_values("Total Return %", ascending=False).iloc[0]

        metric_row([
            ("Avg B&H (30 stocks)",     f"{bah_avg:+.1f}%",    "Benchmark"),
            ("Best Strategy Avg",       f"{top_val:+.1f}%",    top_strat),
            ("Top Single Combo",        f"{top_combo['Total Return %']:+.1f}%",
             f"{top_combo['Ticker']} · {top_combo['Strategy']}"),
            ("Strategies Tested",       "10",                  "× 30 stocks = 330"),
        ])

    st.markdown("---")
    show_chart("ma_backtest_stocks_chart.png")

    st.markdown("---")
    st.subheader("Results explorer")

    if not df.empty:
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            strats = ["All"] + sorted(df.Strategy.unique().tolist())
            sel_strat = st.selectbox("Filter by strategy", strats)
        with col_filter2:
            tickers = ["All"] + sorted(df.Ticker.unique().tolist())
            sel_ticker = st.selectbox("Filter by ticker", tickers)

        filtered = df.copy()
        if sel_strat != "All":
            filtered = filtered[filtered.Strategy == sel_strat]
        if sel_ticker != "All":
            filtered = filtered[filtered.Ticker == sel_ticker]

        year_cols = [c for c in df.columns if c.isdigit()]
        show_cols = ["Ticker", "Strategy", "Total Return %", "Max Drawdown %", "Trades"] + year_cols

        def hl(row):
            styles = []
            for col in row.index:
                if col == "Total Return %":
                    try:
                        v = float(row[col])
                        if row.get("Strategy") == "Buy & Hold":
                            styles.append("font-weight: bold; color: #58a6ff")
                        elif v > 0:
                            styles.append("color: #3fb950")
                        else:
                            styles.append("color: #f85149")
                    except Exception:
                        styles.append("")
                else:
                    styles.append("")
            return styles

        st.dataframe(
            filtered[show_cols].style.apply(hl, axis=1).format(
                {c: "{:+.1f}%" for c in ["Total Return %", "Max Drawdown %"] + year_cols}
            ),
            use_container_width=True,
            hide_index=True,
            height=460,
        )
        st.caption(f"Showing {len(filtered)} of {len(df)} rows")

    st.markdown("---")
    st.subheader("Strategy leaderboard (avg across all 30 stocks)")
    if not df.empty:
        lb = df.groupby("Strategy")["Total Return %"].mean().sort_values(ascending=False).reset_index()
        lb.columns = ["Strategy", "Avg Total Return %"]
        st.dataframe(
            lb.style.format({"Avg Total Return %": "{:+.1f}%"})
              .background_gradient(subset=["Avg Total Return %"], cmap="RdYlGn"),
            use_container_width=True, hide_index=True,
        )

    st.markdown("---")
    st.subheader("Key findings")
    st.markdown("""
<div class="finding-box finding-positive">
<strong>EMA(21,200) best on average — and best on NVDA by a wide margin</strong><br>
Avg +60.6% across 30 stocks · NVDA+EMA(21,200): +991% in 5 years, 4 trades.<br>
The 200-day EMA kept exposure during NVDA's sustained rally while sidestepping its corrections.
</div>

<div class="finding-box finding-neutral">
<strong>Slow crossovers beat buy-and-hold on 27% of individual stocks</strong><br>
SMA(50,200) and SMA(21,200) had the highest hit rate: 27% of stocks outperformed their own B&H.
Goldman Sachs, American Express, and IBM are among stocks where the MA filter added real value.
</div>

<div class="finding-box finding-negative">
<strong>B&H average (+106%) is inflated by NVDA — remove it and the picture changes</strong><br>
NVIDIA's +1,800% dominates the universe average. On the median Dow stock,
slow MA crossovers come much closer to matching buy-and-hold.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# SCRIPT 3 — Earnings Effect
# ===========================================================================
elif page == "s3":
    st.title("Script 3 — Earnings Announcement Effect")
    st.markdown(
        "Five trading windows tested around each quarterly earnings date for all 30 DJIA stocks. "
        "~600 earnings events, 150 strategy × stock combinations."
    )

    df = load_csv("earnings_backtest_results.csv")

    if not df.empty:
        bah_avg = df[df.Window == "Buy & Hold"]["Total Return %"].mean()
        best_window_df = df[df.Window != "Buy & Hold"]
        best_window = best_window_df.groupby("Window")["Total Return %"].mean().idxmax()
        best_val    = best_window_df.groupby("Window")["Total Return %"].mean().max()
        top_combo   = best_window_df.sort_values("Total Return %", ascending=False).iloc[0]
        wr_col      = pd.to_numeric(best_window_df["Win Rate %"], errors="coerce")
        best_wr_idx = wr_col.idxmax()
        best_wr_row = best_window_df.loc[best_wr_idx]

        metric_row([
            ("Avg B&H (30 stocks)",    f"{bah_avg:+.1f}%",   "Benchmark"),
            ("Best Window Avg",        f"{best_val:+.1f}%",  best_window),
            ("Top Combo",              f"{top_combo['Total Return %']:+.1f}%",
             f"{top_combo['Ticker']} · {top_combo['Window']}"),
            ("Best Win Rate",          f"{float(best_wr_row['Win Rate %']):.0f}%",
             f"{best_wr_row['Ticker']} · {best_wr_row['Window']}"),
        ])

    st.markdown("---")
    show_chart("earnings_backtest_chart.png")

    st.markdown("---")
    st.subheader("Results explorer")

    if not df.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            windows = ["All"] + [w for w in df.Window.unique() if w != "Buy & Hold"]
            sel_win = st.selectbox("Filter by window", windows)
        with col_f2:
            tickers2 = ["All"] + sorted(df.Ticker.unique().tolist())
            sel_tick2 = st.selectbox("Filter by ticker", tickers2, key="earn_ticker")

        filt2 = df.copy()
        if sel_win != "All":
            filt2 = filt2[filt2.Window == sel_win]
        if sel_tick2 != "All":
            filt2 = filt2[filt2.Ticker == sel_tick2]

        year_cols2 = [c for c in df.columns if c.isdigit()]
        show_cols2 = ["Ticker", "Window", "Total Return %", "Max Drawdown %",
                      "Win Rate %", "Trades"] + year_cols2

        st.dataframe(
            filt2[show_cols2].sort_values("Total Return %", ascending=False),
            use_container_width=True, hide_index=True, height=460,
        )
        st.caption(f"Showing {len(filt2)} rows")

    st.markdown("---")
    st.subheader("Window summary (averaged across 30 stocks)")
    if not df.empty:
        non_bah = df[df.Window != "Buy & Hold"]
        summary = non_bah.groupby("Window").agg(
            Avg_Return=("Total Return %", "mean"),
            Avg_MaxDD=("Max Drawdown %", "mean"),
            Avg_WinRate=("Win Rate %", lambda x: pd.to_numeric(x, errors="coerce").mean()),
            Total_Events=("Trades", "sum"),
        ).reset_index()
        summary["Avg_Return"]  = summary["Avg_Return"].map(lambda x: f"{x:+.1f}%")
        summary["Avg_MaxDD"]   = summary["Avg_MaxDD"].map(lambda x: f"{x:.1f}%")
        summary["Avg_WinRate"] = summary["Avg_WinRate"].map(lambda x: f"{x:.1f}%")
        st.dataframe(summary, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Key findings")
    st.markdown("""
<div class="finding-box finding-positive">
<strong>PEAD-Long [+1,+20] — the strongest earnings window</strong><br>
Avg +23.4% compounded · 57.1% win rate · +1.19% per event across ~600 earnings dates.<br>
Post-Earnings Announcement Drift is alive and well in Dow components.
</div>

<div class="finding-box finding-positive">
<strong>Goldman Sachs — best single stock for earnings strategies</strong><br>
GS PEAD-Long: +158.7% · 70% win rate · −10.7% max drawdown.<br>
JPMorgan: +82.6%, 75% win rate. Financial sector shows strongest drift effect.
</div>

<div class="finding-box finding-negative">
<strong>Announcement day is a coin flip</strong><br>
Holding over the earnings print (−1 to +1) returned +3.2% average with a 51.7% win rate.<br>
If you're trading the reaction on the day, you're not trading PEAD — you're gambling.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# SCRIPT 4 — Economic Calendar
# ===========================================================================
elif page == "s4":
    st.title("Script 4 — Economic Calendar Event Backtest")
    st.markdown(
        "Four macroeconomic release types (CPI, NFP, GDP, FOMC) × five trading windows, "
        "applied to ^DJI. 180 events across 20 strategy combinations."
    )

    df = load_csv("economic_calendar_backtest_results.csv")

    if not df.empty:
        bah_row  = df[df.Window == "Buy & Hold"].iloc[0]
        non_bah  = df[df.Window != "Buy & Hold"]
        best_row = non_bah.sort_values("Total Return %", ascending=False).iloc[0]
        worst_row = non_bah.sort_values("Total Return %").iloc[0]
        best_wr  = non_bah.sort_values("Win Rate %", ascending=False).iloc[0]

        metric_row([
            ("Buy & Hold",          f"{bah_row['Total Return %']:+.1f}%",  "Benchmark"),
            ("Best Strategy",       f"{best_row['Total Return %']:+.1f}%",
             f"{best_row['Event Type']} {best_row['Window']}"),
            ("Highest Win Rate",    f"{best_wr['Win Rate %']:.0f}%",
             f"{best_wr['Event Type']} {best_wr['Window']}"),
            ("Worst Strategy",      f"{worst_row['Total Return %']:+.1f}%",
             f"{worst_row['Event Type']} {worst_row['Window']}"),
        ])

    st.markdown("---")
    show_chart("economic_calendar_backtest_chart.png")

    st.markdown("---")
    st.subheader("Full results by event type")

    if not df.empty:
        event_tab_names = ["All", "CPI", "NFP", "GDP", "FOMC"]
        tabs = st.tabs(event_tab_names)
        year_cols3 = [c for c in df.columns if c.isdigit()]

        for tab, name in zip(tabs, event_tab_names):
            with tab:
                subset = df if name == "All" else df[
                    (df["Event Type"] == name) | (df["Window"] == "Buy & Hold")
                ]
                show_cols3 = ["Event Type", "Window", "Total Return %",
                              "Max Drawdown %", "Win Rate %", "Events"] + year_cols3

                def style_ec(row):
                    styles = []
                    for col in row.index:
                        if col == "Total Return %":
                            try:
                                v = float(row[col])
                                if row["Window"] == "Buy & Hold":
                                    styles.append("font-weight: bold; color: #58a6ff")
                                elif v > 0:
                                    styles.append("color: #3fb950")
                                else:
                                    styles.append("color: #f85149")
                            except Exception:
                                styles.append("")
                        else:
                            styles.append("")
                    return styles

                st.dataframe(
                    subset[show_cols3].style.apply(style_ec, axis=1),
                    use_container_width=True, hide_index=True,
                )

    st.markdown("---")
    st.subheader("Key findings")
    st.markdown("""
<div class="finding-box finding-positive">
<strong>FOMC Post-Long [+1,+10] — the standout macro strategy</strong><br>
+37.7% over 5 years · 70% win rate · 40 events.<br>
In the market ~32% of available trading days; captures 81% of buy-and-hold return.
The 10 days <em>after</em> a Fed decision are consistently positive regardless of whether the Fed hiked, cut, or held.
</div>

<div class="finding-box finding-positive">
<strong>GDP Post-Long has the highest win rate of any strategy in the study</strong><br>
75% win rate · +20.8% compounded · +1.04% per event average.<br>
Quarterly GDP data appears to drive sustained positioning adjustments over the following two weeks.
</div>

<div class="finding-box finding-negative">
<strong>NFP Pre-window: the worst strategy in the entire study</strong><br>
−15.3% over 5 years · Only 35% win rate across 60 events.<br>
The Dow systematically sells off in the two days before Non-Farm Payrolls — a de-risking signal, not informed positioning.
</div>

<div class="finding-box finding-neutral">
<strong>CPI day-of: five years of inflation headlines, net result = noise</strong><br>
60 CPI releases · +0.1% total · 51.7% win rate.<br>
The dominant macro narrative of 2022–2024 generated essentially zero directional edge on announcement day.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# ARTICLES
# ===========================================================================
elif page == "articles":
    st.title("Research Articles")
    st.markdown(
        "Three articles written from the same underlying data, each targeting a different audience and format."
    )

    tab_medium, tab_substack, tab_ssrn = st.tabs([
        "📰  Medium — General Audience",
        "✉️  Substack — Newsletter",
        "🎓  SSRN — Academic Paper",
    ])

    with tab_medium:
        st.markdown('<div class="article-body">', unsafe_allow_html=True)
        st.markdown(load_article("medium_article.md"))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_substack:
        st.markdown('<div class="article-body">', unsafe_allow_html=True)
        st.markdown(load_article("substack_article.md"))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_ssrn:
        st.markdown('<div class="article-body">', unsafe_allow_html=True)
        st.markdown(load_article("ssrn_paper.md"))
        st.markdown('</div>', unsafe_allow_html=True)
