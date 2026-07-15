"""
Script 2 (DAX) — MA Crossover Backtest on All 40 DAX Component Stocks

Runs the same crossover strategies as Script 1 but on each of the 40
individual DAX 40 component stocks rather than the index itself.

Crossover pairs tested for both SMA and EMA:
  (9, 21), (20, 50), (50, 200), (9, 50), (21, 200)

For each ticker and strategy the script records total return, max drawdown,
trade count, and annual returns.  Terminal output shows strategy-level
aggregates (avg return, hit rate vs B&H).  The CSV has full per-stock detail.

Rules (identical to Script 1):
  - Buy:  short MA crosses ABOVE long MA
  - Exit: short MA crosses BELOW long MA
  - Long only, $10,000 starting capital, no transaction costs
  - Signal lagged 1 day to avoid lookahead bias

Outputs:
  - Terminal summary tables
  - ../outputs/ma_backtest_stocks_dax_results.csv
  - ../outputs/ma_backtest_stocks_dax_chart.png
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import yfinance as yf

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DAX_40 = [
    'ADS.DE', 'AIR.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'BNR.DE',
    'CBK.DE', 'CON.DE', 'DTG.DE', 'DBK.DE', 'DB1.DE',  'DHL.DE', 'DTE.DE', 'EOAN.DE',
    'FRE.DE', 'FME.DE', 'G1A.DE', 'HNR1.DE','HEI.DE',  'HEN3.DE','IFX.DE', 'MBG.DE',
    'MRK.DE', 'MTX.DE', 'MUV2.DE','PAH3.DE','QIA.DE',  'RHM.DE', 'RWE.DE', 'SAP.DE',
    'G24.DE', 'SIE.DE', 'ENR.DE', 'SHL.DE', 'SY1.DE',  'VOW3.DE','VNA.DE', 'ZAL.DE',
]

START_CAPITAL = 10_000
END_DATE   = datetime.today()
START_DATE = END_DATE - timedelta(days=5 * 365)

CROSSOVER_PAIRS = [(9, 21), (20, 50), (50, 200), (9, 50), (21, 200)]
MA_TYPES = ['SMA', 'EMA']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH   = os.path.join(OUTPUT_DIR, 'ma_backtest_stocks_dax_results.csv')
CHART_PATH = os.path.join(OUTPUT_DIR, 'ma_backtest_stocks_dax_chart.png')


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_all_data():
    print(f"Fetching price data for {len(DAX_40)} tickers "
          f"({START_DATE.date()} → {END_DATE.date()}) ...")
    raw = yf.download(
        DAX_40,
        start=START_DATE.strftime('%Y-%m-%d'),
        end=END_DATE.strftime('%Y-%m-%d'),
        progress=False,
        auto_adjust=True,
    )
    if raw.empty:
        sys.exit("ERROR: no data returned from yfinance")

    # yfinance returns MultiIndex (field, ticker) — extract Close
    if isinstance(raw.columns, pd.MultiIndex):
        close_df = raw['Close']
    else:
        close_df = raw[['Close']]

    close_df = close_df.dropna(how='all')
    print(f"  {len(close_df)} trading days  "
          f"({close_df.index[0].date()} – {close_df.index[-1].date()})")
    print(f"  Tickers with full data: "
          f"{close_df.notna().all().sum()} / {len(DAX_40)}")
    return close_df


# ---------------------------------------------------------------------------
# Backtest engine  (same logic as Script 1)
# ---------------------------------------------------------------------------
def compute_ma(series, window, ma_type):
    if ma_type == 'SMA':
        return series.rolling(window=window).mean()
    return series.ewm(span=window, adjust=False).mean()


def run_backtest(close, short_window, long_window, ma_type):
    short_ma = compute_ma(close, short_window, ma_type)
    long_ma  = compute_ma(close, long_window, ma_type)

    position = (short_ma > long_ma).astype(int).shift(1).fillna(0)

    price_returns    = close.pct_change().fillna(0)
    strategy_returns = position * price_returns
    equity           = START_CAPITAL * (1 + strategy_returns).cumprod()

    entries = int(((position == 1) & (position.shift(1) == 0)).sum())
    return equity, strategy_returns, entries


def buy_and_hold(close):
    price_returns = close.pct_change().fillna(0)
    equity        = START_CAPITAL * (1 + price_returns).cumprod()
    return equity, price_returns


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def calc_max_drawdown(equity):
    rolling_max = equity.expanding().max()
    drawdown = (equity - rolling_max) / rolling_max
    return round(drawdown.min() * 100, 2)


def calc_yearly_returns(strategy_returns):
    result = {}
    for yr in sorted(strategy_returns.index.year.unique()):
        yr_rets = strategy_returns[strategy_returns.index.year == yr]
        result[yr] = round(((1 + yr_rets).prod() - 1) * 100, 2)
    return result


def build_row(ticker, label, equity, strategy_returns, entries):
    total_return = round((equity.iloc[-1] / START_CAPITAL - 1) * 100, 2)
    max_dd       = calc_max_drawdown(equity)
    yearly       = calc_yearly_returns(strategy_returns)
    row = {
        'Ticker':          ticker,
        'Strategy':        label,
        'Total Return %':  total_return,
        'Max Drawdown %':  max_dd,
        'Trades':          entries,
    }
    row.update({str(yr): ret for yr, ret in yearly.items()})
    return row


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    close_df = fetch_all_data()
    year_cols_set = set()

    all_rows = []
    total_combos = len(DAX_40) * (1 + len(CROSSOVER_PAIRS) * len(MA_TYPES))
    done = 0

    for ticker in DAX_40:
        if ticker not in close_df.columns:
            print(f"  WARNING: {ticker} not found in downloaded data, skipping")
            continue

        close = close_df[ticker].dropna()
        if len(close) < 210:
            print(f"  WARNING: {ticker} has too little data ({len(close)} days), skipping")
            continue

        # Buy-and-hold
        bah_equity, bah_returns = buy_and_hold(close)
        row = build_row(ticker, 'Buy & Hold', bah_equity, bah_returns, 0)
        year_cols_set.update(str(yr) for yr in calc_yearly_returns(bah_returns))
        all_rows.append(row)
        done += 1

        # MA strategies
        for ma_type in MA_TYPES:
            for short_w, long_w in CROSSOVER_PAIRS:
                label  = f"{ma_type}({short_w},{long_w})"
                equity, strat_rets, entries = run_backtest(close, short_w, long_w, ma_type)
                row = build_row(ticker, label, equity, strat_rets, entries)
                all_rows.append(row)
                done += 1

        if done % 60 == 0 or done >= total_combos - 5:
            print(f"  Progress: {done}/{total_combos} backtests complete ...")

    print(f"  All {done} backtests finished.\n")

    # ---------------------------------------------------------------------------
    # Build results DataFrame
    # ---------------------------------------------------------------------------
    results_df = pd.DataFrame(all_rows)
    year_cols  = sorted(year_cols_set)
    fixed_cols = ['Ticker', 'Strategy', 'Total Return %', 'Max Drawdown %', 'Trades']
    # Fill missing year columns with NaN then reorder
    for yc in year_cols:
        if yc not in results_df.columns:
            results_df[yc] = np.nan
    results_df = results_df[fixed_cols + year_cols]

    # ---------------------------------------------------------------------------
    # Strategy-level aggregate summary
    # ---------------------------------------------------------------------------
    strategy_labels = ['Buy & Hold'] + [
        f"{mt}({sw},{lw})"
        for mt in MA_TYPES
        for sw, lw in CROSSOVER_PAIRS
    ]

    summary_rows = []
    bah_returns_per_ticker = (
        results_df[results_df['Strategy'] == 'Buy & Hold']
        .set_index('Ticker')['Total Return %']
    )

    for label in strategy_labels:
        subset = results_df[results_df['Strategy'] == label]
        avg_ret   = round(subset['Total Return %'].mean(), 1)
        avg_dd    = round(subset['Max Drawdown %'].mean(), 1)
        avg_trades = round(subset['Trades'].mean(), 1)

        # Hit rate: % of stocks where this strategy beat B&H
        if label == 'Buy & Hold':
            hit_rate = '—'
        else:
            merged = subset.set_index('Ticker')['Total Return %'].subtract(
                bah_returns_per_ticker, fill_value=np.nan
            )
            hit_rate = f"{(merged > 0).mean() * 100:.0f}%"

        yr_avgs = {yr: round(subset[yr].mean(), 1) for yr in year_cols if yr in subset.columns}
        summary_rows.append({
            'Strategy':       label,
            'Avg Return %':   avg_ret,
            'Avg Max DD %':   avg_dd,
            'Avg Trades':     avg_trades,
            'Beat B&H':       hit_rate,
            **{yr: yr_avgs.get(yr, np.nan) for yr in year_cols},
        })

    summary_df = pd.DataFrame(summary_rows)

    # ---------------------------------------------------------------------------
    # Print terminal summary
    # ---------------------------------------------------------------------------
    print("=" * 100)
    print("DAX 40 COMPONENTS — MA CROSSOVER BACKTEST SUMMARY")
    print(f"Period: {close_df.index[0].date()} to {close_df.index[-1].date()}  |  "
          f"Capital: ${START_CAPITAL:,} per stock  |  Stocks: {len(DAX_40)}")
    print("=" * 100)
    print("\n--- STRATEGY AGGREGATES (averaged across all 40 stocks) ---\n")

    disp = summary_df.copy()
    for col in ['Avg Return %', 'Avg Max DD %'] + year_cols:
        if col in disp.columns:
            disp[col] = disp[col].map(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    print(disp.to_string(index=False))

    # Best strategy by average return (excluding B&H)
    best_row = summary_df[summary_df['Strategy'] != 'Buy & Hold'].sort_values(
        'Avg Return %', ascending=False
    ).iloc[0]
    bah_avg = summary_df.loc[summary_df['Strategy'] == 'Buy & Hold', 'Avg Return %'].values[0]
    print(f"\nBest strategy avg:  {best_row['Strategy']}  →  {best_row['Avg Return %']:+.1f}%  "
          f"(beat B&H on {best_row['Beat B&H']} of stocks)")
    print(f"Buy & Hold avg:     {bah_avg:+.1f}%\n")

    # Top 10 individual stock × strategy combos
    top10 = (
        results_df[results_df['Strategy'] != 'Buy & Hold']
        .nlargest(10, 'Total Return %')[['Ticker', 'Strategy', 'Total Return %', 'Max Drawdown %', 'Trades']]
    )
    print("--- TOP 10 INDIVIDUAL STOCK × STRATEGY COMBINATIONS ---\n")
    print(top10.to_string(index=False))
    print("\n" + "=" * 100)

    # ---------------------------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------------------------
    results_df.to_csv(CSV_PATH, index=False)
    print(f"\nFull results saved → {CSV_PATH}  ({len(results_df)} rows)")

    # ---------------------------------------------------------------------------
    # Chart
    # ---------------------------------------------------------------------------
    print("Generating chart ...")

    bg        = '#0d1117'
    panel_bg  = '#161b22'
    text_col  = '#c9d1d9'
    grid_col  = '#30363d'

    def style_ax(ax):
        ax.set_facecolor(panel_bg)
        ax.tick_params(colors=text_col, labelsize=8)
        ax.xaxis.label.set_color(text_col)
        ax.yaxis.label.set_color(text_col)
        ax.title.set_color(text_col)
        for spine in ax.spines.values():
            spine.set_edgecolor(grid_col)
        ax.grid(True, color=grid_col, linewidth=0.5, alpha=0.6)

    fig = plt.figure(figsize=(22, 20))
    fig.patch.set_facecolor(bg)
    gs = fig.add_gridspec(3, 2, height_ratios=[2.2, 1.4, 1.4],
                          hspace=0.55, wspace=0.38)

    ax_heat   = fig.add_subplot(gs[0, :])    # full-width heatmap
    ax_bar    = fig.add_subplot(gs[1, :])    # strategy avg bar chart
    ax_yr_sma = fig.add_subplot(gs[2, 0])   # year-by-year SMA
    ax_yr_ema = fig.add_subplot(gs[2, 1])   # year-by-year EMA

    # --- Panel 1: Heatmap of total returns (strategies × stocks) ---
    # Build matrix: rows = strategy labels (excl B&H), cols = tickers
    strat_labels_no_bah = [
        f"{mt}({sw},{lw})"
        for mt in MA_TYPES
        for sw, lw in CROSSOVER_PAIRS
    ]

    tickers_sorted = sorted(DAX_40)
    heat_data = np.full((len(strat_labels_no_bah), len(tickers_sorted)), np.nan)
    bah_vec   = np.full(len(tickers_sorted), np.nan)

    for col_idx, ticker in enumerate(tickers_sorted):
        bah_val = results_df.loc[
            (results_df['Ticker'] == ticker) & (results_df['Strategy'] == 'Buy & Hold'),
            'Total Return %'
        ]
        if not bah_val.empty:
            bah_vec[col_idx] = bah_val.values[0]

        for row_idx, label in enumerate(strat_labels_no_bah):
            val = results_df.loc[
                (results_df['Ticker'] == ticker) & (results_df['Strategy'] == label),
                'Total Return %'
            ]
            if not val.empty:
                heat_data[row_idx, col_idx] = val.values[0]

    # Colour scale: diverging around 0
    vmax = np.nanpercentile(np.abs(heat_data), 95)
    im = ax_heat.imshow(heat_data, aspect='auto', cmap='RdYlGn',
                        vmin=-vmax, vmax=vmax, interpolation='nearest')

    ax_heat.set_xticks(range(len(tickers_sorted)))
    ax_heat.set_xticklabels(tickers_sorted, rotation=45, ha='right', fontsize=7.5)
    ax_heat.set_yticks(range(len(strat_labels_no_bah)))
    ax_heat.set_yticklabels(strat_labels_no_bah, fontsize=7.5)
    ax_heat.tick_params(colors=text_col)
    ax_heat.set_facecolor(panel_bg)
    for spine in ax_heat.spines.values():
        spine.set_edgecolor(grid_col)
    ax_heat.set_title('Total Return % Heatmap — All Strategies × All 40 DAX Stocks',
                      fontsize=11, fontweight='bold', color=text_col, pad=10)

    # Annotate each cell with the return value
    for row_idx in range(len(strat_labels_no_bah)):
        for col_idx in range(len(tickers_sorted)):
            val = heat_data[row_idx, col_idx]
            if not np.isnan(val):
                txt_color = 'black' if abs(val) < vmax * 0.6 else 'white'
                ax_heat.text(col_idx, row_idx, f'{val:.0f}',
                             ha='center', va='center', fontsize=5.5,
                             color=txt_color, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax_heat, orientation='vertical', fraction=0.015, pad=0.01)
    cbar.ax.tick_params(colors=text_col, labelsize=7)
    cbar.set_label('Total Return %', color=text_col, fontsize=8)

    # B&H row above heatmap as a thin separate bar
    ax_bah = ax_heat.inset_axes([0, 1.04, 1, 0.12])
    bah_colors = plt.cm.RdYlGn(
        (bah_vec - (-vmax)) / (2 * vmax) if vmax > 0 else np.zeros_like(bah_vec)
    )
    ax_bah.bar(range(len(tickers_sorted)), bah_vec, color=bah_colors, width=0.85)
    ax_bah.set_xlim(-0.5, len(tickers_sorted) - 0.5)
    ax_bah.set_xticks([])
    ax_bah.set_yticks([])
    ax_bah.set_facecolor(panel_bg)
    for spine in ax_bah.spines.values():
        spine.set_edgecolor(grid_col)
    ax_bah.set_title('Buy & Hold Total Return % (reference)', color=text_col, fontsize=7.5, pad=3)

    # --- Panel 2: Average return per strategy bar chart ---
    style_ax(ax_bar)
    avg_rets  = summary_df['Avg Return %'].values
    labels_ax = summary_df['Strategy'].values
    bar_colors = ['#58a6ff' if lab == 'Buy & Hold' else
                  ('#3fb950' if avg_rets[idx] >= bah_avg else '#f85149')
                  for idx, lab in enumerate(labels_ax)]

    bars = ax_bar.bar(range(len(labels_ax)), avg_rets, color=bar_colors, alpha=0.85, width=0.65)
    ax_bar.axhline(bah_avg, color='#58a6ff', linewidth=1.2, linestyle='--', alpha=0.8,
                   label=f'Buy & Hold avg ({bah_avg:+.1f}%)')
    ax_bar.set_xticks(range(len(labels_ax)))
    ax_bar.set_xticklabels(labels_ax, rotation=35, ha='right', fontsize=8)
    ax_bar.set_ylabel('Avg Total Return %', fontsize=9)
    ax_bar.set_title('Average Total Return per Strategy Across All 40 Stocks',
                     fontsize=10, fontweight='bold', pad=8)
    ax_bar.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax_bar.legend(fontsize=8, facecolor=panel_bg, edgecolor=grid_col, labelcolor=text_col)

    # Add value labels on bars
    for idx, (bar, val) in enumerate(zip(bars, avg_rets)):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, val + 0.4,
                    f'{val:+.1f}%', ha='center', va='bottom', fontsize=6.5, color=text_col)

    # --- Panels 3 & 4: Year-by-year average returns (SMA / EMA) ---
    years = [int(y) for y in year_cols]
    x     = np.arange(len(years))

    bah_yr_avgs = [
        summary_df.loc[summary_df['Strategy'] == 'Buy & Hold', str(yr)].values[0]
        if str(yr) in summary_df.columns else 0
        for yr in years
    ]

    for ax, ma_type in [(ax_yr_sma, 'SMA'), (ax_yr_ema, 'EMA')]:
        style_ax(ax)
        width   = 0.14
        offsets = np.linspace(-(len(CROSSOVER_PAIRS) - 1) * width / 2,
                              (len(CROSSOVER_PAIRS) - 1) * width / 2,
                              len(CROSSOVER_PAIRS))
        palette = plt.cm.Blues(np.linspace(0.45, 0.95, len(CROSSOVER_PAIRS)))
        if ma_type == 'EMA':
            palette = plt.cm.Oranges(np.linspace(0.45, 0.95, len(CROSSOVER_PAIRS)))

        # B&H reference bars
        ax.bar(x, bah_yr_avgs, width=width * len(CROSSOVER_PAIRS) * 1.2,
               color='#30363d', alpha=0.55, zorder=1, label='B&H avg')

        for idx, (sw, lw) in enumerate(CROSSOVER_PAIRS):
            label = f"{ma_type}({sw},{lw})"
            row_data = summary_df[summary_df['Strategy'] == label]
            if row_data.empty:
                continue
            vals = [row_data[str(yr)].values[0] if str(yr) in row_data.columns else 0
                    for yr in years]
            ax.bar(x + offsets[idx], vals, width=width, color=palette[idx],
                   alpha=0.88, zorder=2, label=f'({sw},{lw})')

        ax.axhline(0, color=text_col, linewidth=0.5, alpha=0.4)
        ax.set_title(f'{ma_type} — Avg Annual Return % Across 40 Stocks',
                     fontsize=9, fontweight='bold', pad=6)
        ax.set_xticks(x)
        ax.set_xticklabels([str(yr) for yr in years], fontsize=8)
        ax.set_ylabel('Avg Return %', fontsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
        ax.legend(fontsize=6.5, facecolor=panel_bg, edgecolor=grid_col,
                  labelcolor=text_col, ncol=3, loc='lower left')

    fig.suptitle('DAX 40 Components — MA Crossover Backtest (Script 2)',
                 fontsize=14, fontweight='bold', color=text_col, y=0.99)

    plt.savefig(CHART_PATH, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    print(f"Chart saved    → {CHART_PATH}")
    print("\nDone.")


if __name__ == '__main__':
    main()
