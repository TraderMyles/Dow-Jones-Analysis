"""
seasonal_analysis_dax.py
========================
Seasonal pattern analysis of the DAX 40 (^GDAXI).

Period  : 10 years back from today
Ticker  : ^GDAXI via yfinance (daily OHLCV, auto-adjusted)

Analyses
--------
  1. Day-of-week  — avg return, win rate, median, std, sample size; ranked best→worst
  2. Month        — same metrics grouped by calendar month; ranked best→worst
  3. Day × Year   — avg daily return per weekday per calendar year (heatmap)
  4. Month × Year — total compounded return per month per calendar year (heatmap)

Strategy (long-only, $10k start, no costs)
  • Best-day strategy  : buy open / sell close on every instance of the
                         historically most bullish weekday
  • Best-month strategy: buy open of first trading day / sell close of last
                         trading day of the historically most bullish calendar month
  Both compared against buy-and-hold.

Outputs
-------
  ../outputs/seasonal_analysis_dax_results.csv
  ../outputs/seasonal_analysis_dax_chart1_dow.png        — day-of-week bar chart
  ../outputs/seasonal_analysis_dax_chart2_month.png      — month bar chart
  ../outputs/seasonal_analysis_dax_chart3_dow_year.png   — day × year heatmap
  ../outputs/seasonal_analysis_dax_chart4_month_year.png — month × year heatmap
"""

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

# ── Constants ──────────────────────────────────────────────────────────────────
TICKER        = "^GDAXI"
START_CAPITAL = 10_000
OUTPUTS       = Path(__file__).parent.parent / "outputs"
OUTPUTS.mkdir(exist_ok=True)

DAY_NAMES   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

DARK_BG     = "#0d1117"
PANEL_BG    = "#161b22"
TEXT_COLOR  = "#c9d1d9"
GRID_COLOR  = "#30363d"

# ── Helpers ────────────────────────────────────────────────────────────────────

def compute_metrics(series):
    """Aggregate statistics for a series of decimal returns."""
    pct = series * 100
    return {
        "Avg Return %":    round(pct.mean(), 4),
        "Win Rate %":      round((pct > 0).mean() * 100, 2),
        "Median Return %": round(pct.median(), 4),
        "Std Dev %":       round(pct.std(), 4),
        "Count":           int(len(pct)),
    }


def style_axis(ax, fig):
    """Apply consistent dark-theme styling to a matplotlib axes."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(PANEL_BG)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)


def save_bar_chart(values, labels, title, xlabel, ylabel, filepath):
    """Horizontal-coloured bar chart: green for positive, red for negative."""
    fig, ax = plt.subplots(figsize=(11, 5))
    colors = ["#3fb950" if v >= 0 else "#f85149" for v in values]
    bars = ax.bar(labels, values, color=colors, edgecolor=GRID_COLOR, linewidth=0.6, width=0.6)
    ax.axhline(0, color=TEXT_COLOR, linewidth=0.8, linestyle="--", alpha=0.4)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, labelpad=8)
    ax.set_ylabel(ylabel, labelpad=8)
    style_axis(ax, fig)

    for bar, val in zip(bars, values):
        offset = 0.0003 if val >= 0 else -0.0003
        va     = "bottom" if val >= 0 else "top"
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + offset,
                f"{val:+.4f}%",
                ha="center", va=va, fontsize=8, color=TEXT_COLOR, fontweight="bold")

    plt.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  Saved: {filepath.name}")


def save_heatmap(matrix_df, title, filepath, fmt=".3f", unit_label="Avg Daily Return %"):
    """Diverging RdYlGn heatmap with annotated cells, dark theme."""
    n_rows = len(matrix_df)
    n_cols = len(matrix_df.columns)
    fig_w  = max(10, n_cols * 1.1)
    fig_h  = max(4,  n_rows * 0.6)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    data  = matrix_df.values.astype(float)
    valid = data[~np.isnan(data)]
    if valid.size == 0:
        return
    vmax  = float(np.percentile(np.abs(valid), 95))
    vmax  = vmax if vmax > 0 else 1.0

    cmap  = plt.cm.RdYlGn
    im    = ax.imshow(data, cmap=cmap, vmin=-vmax, vmax=vmax, aspect="auto")

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(matrix_df.columns, rotation=45, ha="right",
                       color=TEXT_COLOR, fontsize=9)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(matrix_df.index, color=TEXT_COLOR, fontsize=9)
    ax.tick_params(length=0)

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            val = data[row_idx, col_idx]
            if np.isnan(val):
                continue
            intensity = abs(val) / vmax
            txt_color = "white" if intensity > 0.55 else "black"
            ax.text(col_idx, row_idx, f"{val:{fmt}}",
                    ha="center", va="center", fontsize=7,
                    color=txt_color, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(unit_label, color=TEXT_COLOR, fontsize=9)
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR, labelcolor=TEXT_COLOR)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_COLOR)

    ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT_COLOR, pad=12)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(PANEL_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)

    plt.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  Saved: {filepath.name}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=365 * 10 + 5)

    print(f"\n{'='*65}")
    print(f"  DAX 40 Seasonal Analysis")
    print(f"  Period: {start_date.date()} → {end_date.date()}")
    print(f"{'='*65}\n")

    # ── Download ───────────────────────────────────────────────────────────────
    print("Downloading ^GDAXI (DAX 40) daily data (10 years)...")
    raw = yf.download(
        TICKER,
        start    = start_date.strftime("%Y-%m-%d"),
        end      = end_date.strftime("%Y-%m-%d"),
        auto_adjust = True,
        progress = False,
    )

    if raw.empty:
        print("ERROR: yfinance returned no data. Check internet connection.")
        return

    # Flatten MultiIndex columns that yfinance sometimes returns
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = pd.to_datetime(df.index)

    # Close-to-close daily return (used for all analysis tables)
    df["cc_return"] = df["Close"].pct_change()
    # Open-to-close intraday return (used only for the day strategy)
    df["oc_return"] = (df["Close"] - df["Open"]) / df["Open"]

    df["day_of_week"] = df.index.dayofweek        # 0 = Monday, 4 = Friday
    df["month"]       = df.index.month             # 1–12
    df["year"]        = df.index.year

    df = df.dropna(subset=["cc_return"])
    years = sorted(df["year"].unique())
    print(f"  Loaded {len(df):,} trading days | years: {years[0]}–{years[-1]}\n")

    # ══════════════════════════════════════════════════════════════════════════
    # Analysis 1 — Day of week
    # ══════════════════════════════════════════════════════════════════════════
    print("Running Analysis 1: Day of Week...")

    dow_rows = []
    for day_num, day_name in enumerate(DAY_NAMES):
        subset = df[df["day_of_week"] == day_num]["cc_return"]
        row    = {"Day": day_name}
        row.update(compute_metrics(subset))
        dow_rows.append(row)

    dow_df = (
        pd.DataFrame(dow_rows)
          .sort_values("Avg Return %", ascending=False)
          .reset_index(drop=True)
    )
    dow_df.insert(0, "Rank", range(1, len(dow_df) + 1))

    best_day  = dow_df.iloc[0]["Day"]
    worst_day = dow_df.iloc[-1]["Day"]

    print("\n  Day of Week — Average Returns (close-to-close, 10 years)")
    print("  " + "-" * 70)
    print(dow_df.to_string(index=False))
    print(f"\n  Best day: {best_day}   |   Worst day: {worst_day}")

    # ══════════════════════════════════════════════════════════════════════════
    # Analysis 2 — Month of year
    # ══════════════════════════════════════════════════════════════════════════
    print("\nRunning Analysis 2: Month of Year...")

    month_rows = []
    for month_num in range(1, 13):
        subset = df[df["month"] == month_num]["cc_return"]
        row    = {"Month": MONTH_NAMES[month_num - 1]}
        row.update(compute_metrics(subset))
        month_rows.append(row)

    month_df = (
        pd.DataFrame(month_rows)
          .sort_values("Avg Return %", ascending=False)
          .reset_index(drop=True)
    )
    month_df.insert(0, "Rank", range(1, len(month_df) + 1))

    best_month  = month_df.iloc[0]["Month"]
    worst_month = month_df.iloc[-1]["Month"]

    print("\n  Month of Year — Average Returns (close-to-close, 10 years)")
    print("  " + "-" * 70)
    print(month_df.to_string(index=False))
    print(f"\n  Best month: {best_month}   |   Worst month: {worst_month}")

    # ══════════════════════════════════════════════════════════════════════════
    # Analysis 3 — Day of week by year (avg daily return)
    # ══════════════════════════════════════════════════════════════════════════
    print("\nRunning Analysis 3: Day of Week × Year...")

    dow_year = (
        df.groupby(["year", "day_of_week"])["cc_return"]
          .mean()
          .mul(100)
          .unstack("day_of_week")
    )
    dow_year.columns = [DAY_NAMES[col] for col in dow_year.columns]
    dow_year = dow_year.round(4)

    print("\n  Day of Week × Year (Avg Daily Return %)")
    print("  " + "-" * 65)
    print(dow_year.to_string())

    # ══════════════════════════════════════════════════════════════════════════
    # Analysis 4 — Month by year (total compounded monthly return)
    # ══════════════════════════════════════════════════════════════════════════
    print("\nRunning Analysis 4: Month × Year (total monthly return)...")

    def monthly_total_return(series):
        return ((1 + series).prod() - 1) * 100

    month_year = (
        df.groupby(["year", "month"])["cc_return"]
          .apply(monthly_total_return)
          .unstack("month")
    )
    month_year.columns = [MONTH_NAMES[col - 1] for col in month_year.columns]
    month_year = month_year.round(3)

    print("\n  Month × Year (Total Compounded Monthly Return %)")
    print("  " + "-" * 65)
    print(month_year.to_string())

    # ══════════════════════════════════════════════════════════════════════════
    # Strategy — Best Day (buy open, sell close every instance of that weekday)
    # ══════════════════════════════════════════════════════════════════════════
    print(f"\nRunning Best-Day Strategy ({best_day})...")

    best_day_num   = DAY_NAMES.index(best_day)
    day_trades     = df[df["day_of_week"] == best_day_num]["oc_return"].fillna(0)

    day_equity = START_CAPITAL
    for ret in day_trades:
        day_equity *= (1 + ret)

    day_total_ret  = (day_equity / START_CAPITAL - 1) * 100
    day_win_rate   = (day_trades > 0).mean() * 100

    print(f"  Trades: {len(day_trades):,}  |  Win rate: {day_win_rate:.1f}%  |  Total return: {day_total_ret:+.2f}%")

    # ══════════════════════════════════════════════════════════════════════════
    # Strategy — Best Month (buy first day open, sell last day close, each year)
    # ══════════════════════════════════════════════════════════════════════════
    print(f"Running Best-Month Strategy ({best_month})...")

    best_month_num = MONTH_NAMES.index(best_month) + 1
    month_trades   = []

    for year in years:
        month_data = df[(df["year"] == year) & (df["month"] == best_month_num)]
        if len(month_data) < 2:
            continue
        entry = month_data["Open"].iloc[0]
        exit_ = month_data["Close"].iloc[-1]
        month_trades.append((exit_ - entry) / entry)

    month_equity = START_CAPITAL
    for ret in month_trades:
        month_equity *= (1 + ret)

    month_total_ret = (month_equity / START_CAPITAL - 1) * 100
    month_win_rate  = (np.array(month_trades) > 0).mean() * 100 if month_trades else 0

    print(f"  Trades: {len(month_trades)}  |  Win rate: {month_win_rate:.1f}%  |  Total return: {month_total_ret:+.2f}%")

    # ── Buy and hold ───────────────────────────────────────────────────────────
    bah_ret = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100

    strategy_df = pd.DataFrame([
        {
            "Strategy":        f"Best Day ({best_day})",
            "Total Return %":  round(day_total_ret, 2),
            "Win Rate %":      round(day_win_rate, 1),
            "# Trades":        len(day_trades),
            "vs B&H (pp)":     round(day_total_ret - bah_ret, 2),
        },
        {
            "Strategy":        f"Best Month ({best_month})",
            "Total Return %":  round(month_total_ret, 2),
            "Win Rate %":      round(month_win_rate, 1),
            "# Trades":        len(month_trades),
            "vs B&H (pp)":     round(month_total_ret - bah_ret, 2),
        },
        {
            "Strategy":        "Buy & Hold",
            "Total Return %":  round(bah_ret, 2),
            "Win Rate %":      "—",
            "# Trades":        1,
            "vs B&H (pp)":     0.0,
        },
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # Save CSV
    # ══════════════════════════════════════════════════════════════════════════
    print("\nSaving CSV...")

    sections = []

    dow_out = dow_df.copy()
    dow_out.insert(0, "Section", "Day of Week")
    sections.append(dow_out)

    month_out = month_df.copy()
    month_out.insert(0, "Section", "Month of Year")
    sections.append(month_out)

    strat_out = strategy_df.copy()
    strat_out.insert(0, "Section", "Strategy Comparison")
    sections.append(strat_out)

    csv_path = OUTPUTS / "seasonal_analysis_dax_results.csv"
    pd.concat(sections, ignore_index=True).to_csv(csv_path, index=False)
    print(f"  Saved: {csv_path.name}")

    # ══════════════════════════════════════════════════════════════════════════
    # Charts
    # ══════════════════════════════════════════════════════════════════════════
    print("\nGenerating charts...")

    # Chart 1 — Day of week (in calendar order, not ranked)
    dow_ordered = pd.DataFrame(dow_rows).set_index("Day").loc[DAY_NAMES]
    save_bar_chart(
        values   = dow_ordered["Avg Return %"].tolist(),
        labels   = DAY_NAMES,
        title    = "DAX 40 — Average Daily Return by Day of Week (10 Years)",
        xlabel   = "Day of Week",
        ylabel   = "Avg Return % (close-to-close)",
        filepath = OUTPUTS / "seasonal_analysis_dax_chart1_dow.png",
    )

    # Chart 2 — Month of year (in calendar order, not ranked)
    month_ordered = pd.DataFrame(month_rows).set_index("Month").loc[MONTH_NAMES]
    save_bar_chart(
        values   = month_ordered["Avg Return %"].tolist(),
        labels   = MONTH_NAMES,
        title    = "DAX 40 — Average Daily Return by Calendar Month (10 Years)",
        xlabel   = "Month",
        ylabel   = "Avg Return % (close-to-close)",
        filepath = OUTPUTS / "seasonal_analysis_dax_chart2_month.png",
    )

    # Chart 3 — Day × Year heatmap
    save_heatmap(
        matrix_df  = dow_year,
        title      = "DAX 40 — Day-of-Week Returns by Year (Avg Daily Return %)",
        filepath   = OUTPUTS / "seasonal_analysis_dax_chart3_dow_year.png",
        fmt        = ".3f",
        unit_label = "Avg Daily Return %",
    )

    # Chart 4 — Month × Year heatmap
    save_heatmap(
        matrix_df  = month_year,
        title      = "DAX 40 — Monthly Returns by Year (Total Compounded Monthly Return %)",
        filepath   = OUTPUTS / "seasonal_analysis_dax_chart4_month_year.png",
        fmt        = ".2f",
        unit_label = "Total Monthly Return %",
    )

    # ══════════════════════════════════════════════════════════════════════════
    # Final terminal summary
    # ══════════════════════════════════════════════════════════════════════════
    print(f"\n{'='*65}")
    print("  SEASONAL ANALYSIS — RESULTS SUMMARY")
    print(f"{'='*65}")
    print(f"  Period : {df.index[0].date()} → {df.index[-1].date()}")
    print(f"  Days   : {len(df):,}  |  Years: {years[0]}–{years[-1]}")
    print()

    print("  DAY OF WEEK (ranked best → worst):")
    for _, row in dow_df.iterrows():
        marker = " ◀ BEST" if row["Day"] == best_day else (" ◀ WORST" if row["Day"] == worst_day else "")
        print(f"    {row['Rank']}. {row['Day']:<12} avg {row['Avg Return %']:+.4f}%  "
              f"win {row['Win Rate %']:.1f}%  n={row['Count']}{marker}")

    print()
    print("  MONTH OF YEAR (ranked best → worst):")
    for _, row in month_df.iterrows():
        marker = " ◀ BEST" if row["Month"] == best_month else (" ◀ WORST" if row["Month"] == worst_month else "")
        print(f"    {row['Rank']:>2}. {row['Month']:<5} avg {row['Avg Return %']:+.4f}%  "
              f"win {row['Win Rate %']:.1f}%  n={row['Count']}{marker}")

    print()
    print("  STRATEGY COMPARISON (10 years, $10,000 start):")
    for _, row in strategy_df.iterrows():
        total = row["Total Return %"]
        vs    = row["vs B&H (pp)"]
        sign  = "+" if isinstance(vs, float) and vs >= 0 else ""
        print(f"    {row['Strategy']:<28} {total:+.2f}%  (vs B&H: {sign}{vs}pp)")

    print()
    print(f"  Outputs saved to: {OUTPUTS.resolve()}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
