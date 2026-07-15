"""
Script 1 (DAX) — MA Crossover Backtest on DAX 40 Index (^GDAXI)

Tests moving average crossover strategies on the DAX 40 index.
Both SMA and EMA are tested for each crossover pair:
  (9, 21), (20, 50), (50, 200), (9, 50), (21, 200)

Rules:
  - Buy:  short MA crosses ABOVE long MA
  - Exit: short MA crosses BELOW long MA
  - Long only — no shorting
  - $10,000 starting capital, no transaction costs
  - Signal lagged 1 day to avoid lookahead bias

Outputs:
  - Terminal summary table
  - ../outputs/ma_backtest_dax_results.csv
  - ../outputs/ma_backtest_dax_chart.png
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
TICKER = '^GDAXI'
START_CAPITAL = 10_000
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=5 * 365)

CROSSOVER_PAIRS = [(9, 21), (20, 50), (50, 200), (9, 50), (21, 200)]
MA_TYPES = ['SMA', 'EMA']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH = os.path.join(OUTPUT_DIR, 'ma_backtest_dax_results.csv')
CHART_PATH = os.path.join(OUTPUT_DIR, 'ma_backtest_dax_chart.png')


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_data():
    print(f"Fetching {TICKER} data from {START_DATE.date()} to {END_DATE.date()} ...")
    df = yf.download(TICKER, start=START_DATE.strftime('%Y-%m-%d'),
                     end=END_DATE.strftime('%Y-%m-%d'), progress=False)
    if df.empty:
        sys.exit("ERROR: no data returned from yfinance")
    # Handle MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    close = df['Close'].dropna()
    print(f"  Got {len(close)} trading days  ({close.index[0].date()} – {close.index[-1].date()})")
    return close


# ---------------------------------------------------------------------------
# Backtest engine
# ---------------------------------------------------------------------------
def compute_ma(series, window, ma_type):
    if ma_type == 'SMA':
        return series.rolling(window=window).mean()
    return series.ewm(span=window, adjust=False).mean()


def run_backtest(close, short_window, long_window, ma_type):
    """
    Single crossover backtest.
    Returns equity curve, position series, strategy daily returns, entry count.
    """
    short_ma = compute_ma(close, short_window, ma_type)
    long_ma = compute_ma(close, long_window, ma_type)

    # 1 when short > long, else 0 — then shift 1 day to avoid lookahead bias
    raw_signal = (short_ma > long_ma).astype(int)
    position = raw_signal.shift(1).fillna(0)

    price_returns = close.pct_change().fillna(0)
    strategy_returns = position * price_returns

    equity = START_CAPITAL * (1 + strategy_returns).cumprod()

    # Count round-trip entries
    entries = int(((position == 1) & (position.shift(1) == 0)).sum())

    return equity, position, strategy_returns, entries, short_ma, long_ma


def buy_and_hold(close):
    price_returns = close.pct_change().fillna(0)
    equity = START_CAPITAL * (1 + price_returns).cumprod()
    strategy_returns = price_returns
    return equity, strategy_returns


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def calc_yearly_returns(strategy_returns, close):
    """Return dict of {year: pct_return} for strategy and buy-and-hold."""
    years = sorted(strategy_returns.index.year.unique())
    result = {}
    for yr in years:
        yr_rets = strategy_returns[strategy_returns.index.year == yr]
        result[yr] = round(((1 + yr_rets).prod() - 1) * 100, 2)
    return result


def calc_max_drawdown(equity):
    rolling_max = equity.expanding().max()
    drawdown = (equity - rolling_max) / rolling_max
    return round(drawdown.min() * 100, 2)


def build_metrics(label, equity, strategy_returns, close, entries):
    total_return = round((equity.iloc[-1] / START_CAPITAL - 1) * 100, 2)
    max_dd = calc_max_drawdown(equity)
    yearly = calc_yearly_returns(strategy_returns, close)
    row = {
        'Strategy': label,
        'Total Return %': total_return,
        'Max Drawdown %': max_dd,
        'Trades': entries,
    }
    row.update({str(yr): ret for yr, ret in yearly.items()})
    return row


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    close = fetch_data()
    all_results = []
    equity_curves = {}  # label -> equity Series

    # Buy-and-hold benchmark
    print("Running buy-and-hold benchmark ...")
    bah_equity, bah_returns = buy_and_hold(close)
    bah_row = build_metrics('Buy & Hold', bah_equity, bah_returns, close, 0)
    all_results.append(bah_row)
    equity_curves['Buy & Hold'] = bah_equity

    # MA crossover strategies
    total_strategies = len(CROSSOVER_PAIRS) * len(MA_TYPES)
    count = 0
    ma_data = {}  # (window, ma_type) -> Series

    for ma_type in MA_TYPES:
        for short_w, long_w in CROSSOVER_PAIRS:
            count += 1
            label = f"{ma_type}({short_w},{long_w})"
            print(f"  [{count}/{total_strategies}] Backtesting {label} ...")
            equity, position, strat_rets, entries, short_ma, long_ma = run_backtest(
                close, short_w, long_w, ma_type
            )
            row = build_metrics(label, equity, strat_rets, close, entries)
            all_results.append(row)
            equity_curves[label] = equity

            # Store MAs for chart (only keep the ones we'll plot)
            ma_data[(short_w, long_w, ma_type)] = (short_ma, long_ma)

    # ---------------------------------------------------------------------------
    # Build results DataFrame
    # ---------------------------------------------------------------------------
    results_df = pd.DataFrame(all_results)
    # Reorder: Strategy, Total Return, Max DD, Trades, then year columns
    year_cols = sorted([c for c in results_df.columns if c.isdigit()])
    fixed_cols = ['Strategy', 'Total Return %', 'Max Drawdown %', 'Trades']
    results_df = results_df[fixed_cols + year_cols]

    # ---------------------------------------------------------------------------
    # Print terminal summary
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 90)
    print("DAX 40 MA CROSSOVER BACKTEST — SUMMARY")
    print(f"Period: {close.index[0].date()} to {close.index[-1].date()}  |  Capital: ${START_CAPITAL:,}")
    print("=" * 90)

    # Format for display
    display_df = results_df.copy()
    for col in ['Total Return %', 'Max Drawdown %'] + year_cols:
        display_df[col] = display_df[col].map(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    display_df['Trades'] = display_df['Trades'].astype(str)

    print(display_df.to_string(index=False))
    print("=" * 90)

    # Best strategy by total return
    best_idx = results_df.loc[results_df['Strategy'] != 'Buy & Hold', 'Total Return %'].idxmax()
    best = results_df.loc[best_idx]
    print(f"\nBest strategy: {best['Strategy']}  →  {best['Total Return %']:+.1f}% total return")
    bah_total = results_df.loc[results_df['Strategy'] == 'Buy & Hold', 'Total Return %'].values[0]
    print(f"Buy & Hold benchmark:           {bah_total:+.1f}% total return\n")

    # ---------------------------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------------------------
    results_df.to_csv(CSV_PATH, index=False)
    print(f"Results saved → {CSV_PATH}")

    # ---------------------------------------------------------------------------
    # Chart
    # ---------------------------------------------------------------------------
    print("Generating chart ...")

    years = [int(y) for y in year_cols]
    n_strategies = len(equity_curves)

    fig = plt.figure(figsize=(18, 16))
    fig.patch.set_facecolor('#0d1117')

    gs = fig.add_gridspec(3, 2, height_ratios=[2, 2, 1.5], hspace=0.45, wspace=0.35)

    ax_price = fig.add_subplot(gs[0, :])   # full-width price panel
    ax_equity = fig.add_subplot(gs[1, :])  # full-width equity panel
    ax_bar_sma = fig.add_subplot(gs[2, 0]) # SMA year-by-year
    ax_bar_ema = fig.add_subplot(gs[2, 1]) # EMA year-by-year

    bg = '#0d1117'
    panel_bg = '#161b22'
    text_color = '#c9d1d9'
    grid_color = '#30363d'

    for ax in [ax_price, ax_equity, ax_bar_sma, ax_bar_ema]:
        ax.set_facecolor(panel_bg)
        ax.tick_params(colors=text_color, labelsize=8)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        for spine in ax.spines.values():
            spine.set_edgecolor(grid_color)
        ax.grid(True, color=grid_color, linewidth=0.5, alpha=0.7)

    # --- Panel 1: DAX 40 price + representative MAs ---
    ax_price.plot(close.index, close.values, color='#58a6ff', linewidth=1.0,
                  label='^GDAXI Close', zorder=3)

    # Overlay SMA(20,50) and SMA(50,200) as representative pairs
    rep_pairs = [(20, 50, 'SMA', '#f0883e', '#3fb950'),
                 (50, 200, 'SMA', '#d2a8ff', '#ff7b72')]
    for short_w, long_w, ma_t, c1, c2 in rep_pairs:
        short_ma, long_ma = ma_data[(short_w, long_w, ma_t)]
        ax_price.plot(short_ma.index, short_ma.values, color=c1, linewidth=0.9, alpha=0.85,
                      label=f'{ma_t}({short_w})')
        ax_price.plot(long_ma.index, long_ma.values, color=c2, linewidth=0.9, alpha=0.85,
                      label=f'{ma_t}({long_w})')

    ax_price.set_title(f'^GDAXI Price with Representative SMAs', fontsize=11, fontweight='bold', pad=8)
    ax_price.set_ylabel('Index Level', fontsize=9)
    ax_price.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax_price.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax_price.legend(fontsize=7, loc='upper left', facecolor=panel_bg, edgecolor=grid_color,
                    labelcolor=text_color, ncol=5)

    # --- Panel 2: Equity curves ---
    bah_line = equity_curves['Buy & Hold']
    ax_equity.plot(bah_line.index, bah_line.values, color='#ffffff', linewidth=2.0,
                   linestyle='--', label='Buy & Hold', zorder=5, alpha=0.9)

    sma_colors = plt.cm.Blues(np.linspace(0.45, 0.95, len(CROSSOVER_PAIRS)))
    ema_colors = plt.cm.Oranges(np.linspace(0.45, 0.95, len(CROSSOVER_PAIRS)))

    for idx, (short_w, long_w) in enumerate(CROSSOVER_PAIRS):
        for ma_type, palette in [('SMA', sma_colors), ('EMA', ema_colors)]:
            lbl = f"{ma_type}({short_w},{long_w})"
            eq = equity_curves[lbl]
            color = palette[idx]
            ls = '-' if ma_type == 'SMA' else '-.'
            ax_equity.plot(eq.index, eq.values, color=color, linewidth=0.85,
                           linestyle=ls, alpha=0.85, label=lbl)

    ax_equity.set_title('Portfolio Equity Curves — All Strategies vs Buy & Hold',
                         fontsize=11, fontweight='bold', pad=8)
    ax_equity.set_ylabel('Portfolio Value ($)', fontsize=9)
    ax_equity.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax_equity.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax_equity.legend(fontsize=6.5, loc='upper left', facecolor=panel_bg,
                     edgecolor=grid_color, labelcolor=text_color, ncol=4)

    # --- Panels 3 & 4: Year-by-year bar charts (SMA / EMA) ---
    bah_yearly = {int(yr): results_df.loc[results_df['Strategy'] == 'Buy & Hold', yr].values[0]
                  for yr in year_cols}
    x = np.arange(len(years))

    for ax, ma_type in [(ax_bar_sma, 'SMA'), (ax_bar_ema, 'EMA')]:
        width = 0.14
        offsets = np.linspace(-(len(CROSSOVER_PAIRS) - 1) * width / 2,
                              (len(CROSSOVER_PAIRS) - 1) * width / 2,
                              len(CROSSOVER_PAIRS))

        # Buy-and-hold bars (light grey background reference)
        bah_vals = [bah_yearly.get(yr, 0) for yr in years]
        ax.bar(x, bah_vals, width=width * len(CROSSOVER_PAIRS) * 1.15, color='#30363d',
               alpha=0.6, zorder=1, label='B&H')

        palette = plt.cm.Blues if ma_type == 'SMA' else plt.cm.Oranges
        colors = palette(np.linspace(0.45, 0.95, len(CROSSOVER_PAIRS)))

        for idx, (short_w, long_w) in enumerate(CROSSOVER_PAIRS):
            lbl = f"{ma_type}({short_w},{long_w})"
            yr_data = results_df.loc[results_df['Strategy'] == lbl, year_cols]
            if yr_data.empty:
                continue
            vals = [yr_data[str(yr)].values[0] if str(yr) in yr_data.columns else 0 for yr in years]
            bars = ax.bar(x + offsets[idx], vals, width=width, color=colors[idx],
                          alpha=0.88, zorder=2, label=f'({short_w},{long_w})')

        ax.axhline(0, color=text_color, linewidth=0.5, alpha=0.5)
        ax.set_title(f'{ma_type} Strategies — Annual Returns %', fontsize=9,
                     fontweight='bold', pad=6)
        ax.set_xticks(x)
        ax.set_xticklabels([str(yr) for yr in years], fontsize=7.5)
        ax.set_ylabel('Return %', fontsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f'{val:.0f}%'))
        ax.legend(fontsize=6.5, facecolor=panel_bg, edgecolor=grid_color,
                  labelcolor=text_color, ncol=3, loc='lower left')

    fig.suptitle('DAX 40 MA Crossover Backtest — Script 1', fontsize=14,
                 fontweight='bold', color=text_color, y=0.98)

    plt.savefig(CHART_PATH, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    print(f"Chart saved    → {CHART_PATH}")
    print("\nDone.")


if __name__ == '__main__':
    main()
