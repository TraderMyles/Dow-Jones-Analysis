"""
Script 3 — Earnings Announcement Effect Backtest on DJIA 30 Components

For each of the 30 Dow Jones stocks, fetches historical quarterly earnings dates
via yfinance and simulates five long-only trading windows around each announcement:

  1. Pre-Drift     [T-5  → T-1 ] — buy 5 days before, sell 1 day before
  2. Announcement  [T-1  → T+1 ] — buy 1 day before, sell 1 day after (hold the print)
  3. PEAD-Short    [T+1  → T+5 ] — buy 1 day after, sell 5 days after
  4. PEAD-Long     [T+1  → T+20] — buy 1 day after, sell 20 days after
  5. Full Window   [T-5  → T+5 ] — buy 5 days before, sell 5 days after

T = earnings date (mapped to nearest trading day).
Long only, $10,000 starting capital per stock per window, no transaction costs.
Cash earns 0% when not in a position.

Outputs:
  - Terminal summary (strategy aggregates across 30 stocks + top combos)
  - ../outputs/earnings_backtest_results.csv
  - ../outputs/earnings_backtest_chart.png
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
DJIA_30 = [
    'AAPL', 'AMGN', 'AMZN', 'AXP',  'BA',   'CAT',  'CRM',  'CSCO',
    'CVX',  'DIS',  'DOW',  'GS',   'HD',   'HON',  'IBM',  'JNJ',
    'JPM',  'KO',   'MCD',  'MMM',  'MRK',  'MSFT', 'NKE',  'NVDA',
    'PG',   'SHW',  'TRV',  'UNH',  'V',    'WMT',
]

# (entry_offset, exit_offset) in trading days relative to earnings date T
WINDOWS = {
    'Pre-Drift [-5,-1]':    (-5, -1),
    'Announcement [-1,+1]': (-1, +1),
    'PEAD-Short [+1,+5]':   (+1, +5),
    'PEAD-Long [+1,+20]':   (+1, +20),
    'Full [-5,+5]':         (-5, +5),
}

START_CAPITAL = 10_000
END_DATE   = datetime.today()
START_DATE = END_DATE - timedelta(days=5 * 365)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH   = os.path.join(OUTPUT_DIR, 'earnings_backtest_results.csv')
CHART_PATH = os.path.join(OUTPUT_DIR, 'earnings_backtest_chart.png')


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
def fetch_price_data():
    print(f"Fetching price data for {len(DJIA_30)} tickers "
          f"({START_DATE.date()} → {END_DATE.date()}) ...")
    raw = yf.download(
        DJIA_30,
        start=START_DATE.strftime('%Y-%m-%d'),
        end=END_DATE.strftime('%Y-%m-%d'),
        progress=False,
        auto_adjust=True,
    )
    if raw.empty:
        sys.exit("ERROR: no price data from yfinance")
    if isinstance(raw.columns, pd.MultiIndex):
        close_df = raw['Close']
    else:
        close_df = raw[['Close']]
    close_df = close_df.dropna(how='all')
    print(f"  {len(close_df)} trading days "
          f"({close_df.index[0].date()} – {close_df.index[-1].date()})")
    return close_df


def fetch_earnings_dates(ticker):
    """Return sorted list of tz-naive earnings dates within our backtest window."""
    try:
        obj  = yf.Ticker(ticker)
        # get_earnings_dates returns a DataFrame indexed by date; limit=40 ~ 10 years
        df   = obj.get_earnings_dates(limit=40)
        if df is None or df.empty:
            return []
        dates = df.index
        # Strip timezone if present
        if hasattr(dates, 'tz') and dates.tz is not None:
            dates = dates.tz_localize(None)
        else:
            dates = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(None) for d in dates])
        dates = dates.normalize()
        # Keep only dates within our window
        dates = dates[(dates >= pd.Timestamp(START_DATE)) &
                      (dates <= pd.Timestamp(END_DATE))]
        # Drop future estimates (EPS Actual is NaN for future dates)
        if 'EPS Actual' in df.columns:
            reported = df[df['EPS Actual'].notna()].index
            if hasattr(reported, 'tz') and reported.tz is not None:
                reported = reported.tz_localize(None)
            else:
                reported = pd.DatetimeIndex(
                    [pd.Timestamp(d).tz_localize(None) for d in reported]
                )
            reported = reported.normalize()
            dates = dates[dates.isin(reported)]
        return sorted(dates.tolist())
    except Exception:
        return []


def nearest_trading_day(target, trading_days, direction='forward'):
    """Snap a date to the nearest trading day."""
    target = pd.Timestamp(target).normalize()
    if target in trading_days:
        return target
    if direction == 'forward':
        candidates = trading_days[trading_days >= target]
        return candidates[0] if len(candidates) else None
    else:
        candidates = trading_days[trading_days <= target]
        return candidates[-1] if len(candidates) else None


def offset_trading_day(base_date, offset, trading_days):
    """Return the trading day base_date + offset (in trading days)."""
    idx_arr = trading_days.searchsorted(base_date)
    if idx_arr >= len(trading_days) or trading_days[idx_arr] != base_date:
        return None
    new_idx = idx_arr + offset
    if 0 <= new_idx < len(trading_days):
        return trading_days[new_idx]
    return None


# ---------------------------------------------------------------------------
# Backtest engine
# ---------------------------------------------------------------------------
def run_earnings_window(close, earnings_dates_raw, entry_offset, exit_offset):
    """
    Simulate a long-only earnings window strategy for one stock.

    Returns:
        equity       — Series of portfolio value keyed by exit date
        trades       — list of dicts with per-trade detail
        yearly_rets  — dict {year: total_return_pct} based on entry year
    """
    trading_days = close.index

    # Resolve earnings dates to actual trading days
    events = []
    for raw_date in earnings_dates_raw:
        t_day = nearest_trading_day(raw_date, trading_days, direction='forward')
        if t_day is None:
            continue
        entry_day = offset_trading_day(t_day, entry_offset, trading_days)
        exit_day  = offset_trading_day(t_day, exit_offset,  trading_days)
        if entry_day is None or exit_day is None:
            continue
        if entry_day >= exit_day:
            continue
        if entry_day not in close.index or exit_day not in close.index:
            continue
        events.append((entry_day, exit_day))

    if not events:
        return None, [], {}

    # Sort by entry date and remove overlapping windows
    events.sort(key=lambda x: x[0])
    clean_events = []
    last_exit = pd.Timestamp.min
    for entry_day, exit_day in events:
        if entry_day > last_exit:
            clean_events.append((entry_day, exit_day))
            last_exit = exit_day

    if not clean_events:
        return None, [], {}

    capital = START_CAPITAL
    trade_list  = []
    yearly_pnl  = {}  # year -> list of trade returns

    equity_points = {}

    for entry_day, exit_day in clean_events:
        entry_price = close.loc[entry_day]
        exit_price  = close.loc[exit_day]

        if entry_price <= 0 or pd.isna(entry_price) or pd.isna(exit_price):
            continue

        trade_ret = exit_price / entry_price - 1
        capital  *= (1 + trade_ret)

        yr = entry_day.year
        yearly_pnl.setdefault(yr, []).append(trade_ret)
        equity_points[exit_day] = capital
        trade_list.append({
            'entry': entry_day, 'exit': exit_day,
            'entry_price': entry_price, 'exit_price': exit_price,
            'return_pct': round(trade_ret * 100, 4),
        })

    if not trade_list:
        return None, [], {}

    equity = pd.Series(equity_points).sort_index()
    yearly_rets = {
        yr: round((np.prod([1 + r for r in rets]) - 1) * 100, 2)
        for yr, rets in yearly_pnl.items()
    }

    return equity, trade_list, yearly_rets


def buy_and_hold_metrics(close):
    price_returns = close.pct_change().fillna(0)
    equity = START_CAPITAL * (1 + price_returns).cumprod()
    total_return = round((equity.iloc[-1] / START_CAPITAL - 1) * 100, 2)

    rolling_max = equity.expanding().max()
    max_dd = round(((equity - rolling_max) / rolling_max).min() * 100, 2)

    yearly = {}
    for yr in sorted(price_returns.index.year.unique()):
        yr_rets = price_returns[price_returns.index.year == yr]
        yearly[yr] = round(((1 + yr_rets).prod() - 1) * 100, 2)

    return total_return, max_dd, yearly


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    close_df = fetch_price_data()
    all_rows = []
    year_cols_set = set()

    # Cache earnings dates — one API call per ticker
    print(f"Fetching earnings dates for {len(DJIA_30)} tickers ...")
    earnings_cache = {}
    for ticker in DJIA_30:
        dates = fetch_earnings_dates(ticker)
        earnings_cache[ticker] = dates
        n = len(dates)
        if n == 0:
            print(f"  {ticker}: no earnings dates found")
        # Brief progress every 10 tickers
    earned_counts = [len(v) for v in earnings_cache.values() if v]
    print(f"  Done. Avg {np.mean(earned_counts):.1f} events/stock "
          f"(range {min(earned_counts)}–{max(earned_counts)})\n")

    total_tickers = len(DJIA_30)
    for ticker_idx, ticker in enumerate(DJIA_30):
        print(f"  [{ticker_idx+1}/{total_tickers}] {ticker} "
              f"({len(earnings_cache[ticker])} earnings events) ...")

        if ticker not in close_df.columns:
            print(f"    WARNING: no price data, skipping")
            continue

        close = close_df[ticker].dropna()
        if len(close) < 50:
            print(f"    WARNING: too little price data, skipping")
            continue

        earnings_dates = earnings_cache[ticker]

        # Buy-and-hold row
        bah_total, bah_dd, bah_yearly = buy_and_hold_metrics(close)
        bah_row = {
            'Ticker':         ticker,
            'Window':         'Buy & Hold',
            'Total Return %': bah_total,
            'Max Drawdown %': bah_dd,
            'Win Rate %':     '—',
            'Trades':         0,
        }
        bah_row.update({str(yr): ret for yr, ret in bah_yearly.items()})
        year_cols_set.update(str(yr) for yr in bah_yearly)
        all_rows.append(bah_row)

        if not earnings_dates:
            continue

        # Earnings window strategies
        for window_name, (entry_off, exit_off) in WINDOWS.items():
            equity, trades, yearly_rets = run_earnings_window(
                close, earnings_dates, entry_off, exit_off
            )

            if equity is None or len(trades) == 0:
                row = {
                    'Ticker': ticker, 'Window': window_name,
                    'Total Return %': 0.0, 'Max Drawdown %': 0.0,
                    'Win Rate %': 0.0, 'Trades': 0,
                }
            else:
                final_capital = equity.iloc[-1]
                total_ret = round((final_capital / START_CAPITAL - 1) * 100, 2)

                # Max drawdown on the equity snapshots
                eq_arr = equity.values
                running_max = np.maximum.accumulate(eq_arr)
                dds = (eq_arr - running_max) / running_max
                max_dd = round(dds.min() * 100, 2)

                win_rate = round(
                    sum(1 for t in trades if t['return_pct'] > 0) / len(trades) * 100, 1
                )

                row = {
                    'Ticker':         ticker,
                    'Window':         window_name,
                    'Total Return %': total_ret,
                    'Max Drawdown %': max_dd,
                    'Win Rate %':     win_rate,
                    'Trades':         len(trades),
                }
                row.update({str(yr): ret for yr, ret in yearly_rets.items()})
                year_cols_set.update(str(yr) for yr in yearly_rets)

            all_rows.append(row)

    print(f"\n  All backtests complete.\n")

    # ---------------------------------------------------------------------------
    # Build DataFrame
    # ---------------------------------------------------------------------------
    results_df = pd.DataFrame(all_rows)
    year_cols  = sorted(year_cols_set)
    for yc in year_cols:
        if yc not in results_df.columns:
            results_df[yc] = np.nan

    fixed_cols = ['Ticker', 'Window', 'Total Return %', 'Max Drawdown %',
                  'Win Rate %', 'Trades']
    results_df = results_df[fixed_cols + year_cols]

    # ---------------------------------------------------------------------------
    # Strategy aggregate summary
    # ---------------------------------------------------------------------------
    window_order = ['Buy & Hold'] + list(WINDOWS.keys())
    bah_per_ticker = (
        results_df[results_df['Window'] == 'Buy & Hold']
        .set_index('Ticker')['Total Return %']
    )

    summary_rows = []
    for window_name in window_order:
        subset = results_df[results_df['Window'] == window_name]
        if subset.empty:
            continue

        avg_ret    = round(subset['Total Return %'].mean(), 1)
        avg_dd     = round(subset['Max Drawdown %'].mean(), 1)
        avg_trades = round(subset['Trades'].mean(), 1)

        if window_name == 'Buy & Hold':
            win_rate_avg = '—'
            beat_bah     = '—'
        else:
            numeric_wr = pd.to_numeric(subset['Win Rate %'], errors='coerce')
            win_rate_avg = f"{numeric_wr.mean():.1f}%"
            beat = subset.set_index('Ticker')['Total Return %'].subtract(
                bah_per_ticker, fill_value=np.nan
            )
            beat_bah = f"{(beat > 0).mean() * 100:.0f}%"

        yr_avgs = {}
        for yc in year_cols:
            if yc in subset.columns:
                yr_avgs[yc] = round(pd.to_numeric(subset[yc], errors='coerce').mean(), 1)

        summary_rows.append({
            'Window':      window_name,
            'Avg Ret %':   avg_ret,
            'Avg DD %':    avg_dd,
            'Avg Trades':  avg_trades,
            'Win Rate':    win_rate_avg,
            'Beat B&H':    beat_bah,
            **{yc: yr_avgs.get(yc, np.nan) for yc in year_cols},
        })

    summary_df = pd.DataFrame(summary_rows)

    # ---------------------------------------------------------------------------
    # Print terminal summary
    # ---------------------------------------------------------------------------
    print("=" * 105)
    print("DJIA 30 — EARNINGS ANNOUNCEMENT EFFECT BACKTEST")
    print(f"Period: {close_df.index[0].date()} to {close_df.index[-1].date()}  "
          f"|  Capital: ${START_CAPITAL:,}/stock  |  Stocks: {len(DJIA_30)}")
    print("=" * 105)
    print("\n--- WINDOW STRATEGY AGGREGATES (averaged across 30 stocks) ---\n")

    disp = summary_df.copy()
    for col in ['Avg Ret %', 'Avg DD %'] + year_cols:
        if col in disp.columns:
            disp[col] = disp[col].map(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    print(disp.to_string(index=False))

    bah_avg = summary_df.loc[summary_df['Window'] == 'Buy & Hold', 'Avg Ret %_raw'] \
        if 'Avg Ret %_raw' in summary_df.columns \
        else float(summary_df.loc[summary_df['Window'] == 'Buy & Hold', 'Avg Ret %'].iloc[0])

    # Per-event avg return (total return / number of events)
    print("\n--- PER-EVENT AVERAGE RETURN (total return ÷ number of events) ---\n")
    event_rows = []
    for window_name in WINDOWS.keys():
        subset = results_df[results_df['Window'] == window_name]
        trades_total = subset['Trades'].sum()
        if trades_total > 0:
            avg_per_event = round(
                (subset['Total Return %'] / subset['Trades'].replace(0, np.nan)).mean(), 3
            )
        else:
            avg_per_event = 0.0
        event_rows.append({'Window': window_name, 'Avg Return per Event %': avg_per_event,
                           'Total Events': int(trades_total)})
    print(pd.DataFrame(event_rows).to_string(index=False))

    # Top 10 stock × window combinations
    non_bah = results_df[results_df['Window'] != 'Buy & Hold']
    top10 = non_bah.nlargest(10, 'Total Return %')[
        ['Ticker', 'Window', 'Total Return %', 'Max Drawdown %', 'Win Rate %', 'Trades']
    ]
    print("\n--- TOP 10 STOCK × WINDOW COMBINATIONS ---\n")
    print(top10.to_string(index=False))
    print("\n" + "=" * 105)

    # ---------------------------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------------------------
    results_df.to_csv(CSV_PATH, index=False)
    print(f"\nFull results saved → {CSV_PATH}  ({len(results_df)} rows)")

    # ---------------------------------------------------------------------------
    # Chart
    # ---------------------------------------------------------------------------
    print("Generating chart ...")

    bg       = '#0d1117'
    panel_bg = '#161b22'
    text_col = '#c9d1d9'
    grid_col = '#30363d'

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
    gs = fig.add_gridspec(3, 2, height_ratios=[1.8, 1.6, 1.4],
                          hspace=0.52, wspace=0.38)

    ax_heat  = fig.add_subplot(gs[0, :])   # heatmap: stocks × windows
    ax_bar   = fig.add_subplot(gs[1, :])   # avg return per window bar chart
    ax_yr    = fig.add_subplot(gs[2, 0])   # year-by-year line chart
    ax_event = fig.add_subplot(gs[2, 1])   # per-event avg return comparison

    window_names = list(WINDOWS.keys())

    # --- Panel 1: Heatmap — total return by ticker × window ---
    tickers_sorted = sorted(DJIA_30)
    heat_matrix = np.full((len(window_names), len(tickers_sorted)), np.nan)

    for col_idx, ticker in enumerate(tickers_sorted):
        for row_idx, wname in enumerate(window_names):
            val = results_df.loc[
                (results_df['Ticker'] == ticker) & (results_df['Window'] == wname),
                'Total Return %'
            ]
            if not val.empty:
                heat_matrix[row_idx, col_idx] = val.values[0]

    # Symmetric colour scale around 0 — but use B&H magnitude as reference
    bah_vals = np.array([
        results_df.loc[(results_df['Ticker'] == t) &
                       (results_df['Window'] == 'Buy & Hold'), 'Total Return %'].values[0]
        for t in tickers_sorted
        if not results_df.loc[(results_df['Ticker'] == t) &
                               (results_df['Window'] == 'Buy & Hold'), 'Total Return %'].empty
    ])
    vmax = max(np.nanpercentile(np.abs(heat_matrix), 90), 20)

    im = ax_heat.imshow(heat_matrix, aspect='auto', cmap='RdYlGn',
                        vmin=-vmax, vmax=vmax, interpolation='nearest')
    ax_heat.set_xticks(range(len(tickers_sorted)))
    ax_heat.set_xticklabels(tickers_sorted, rotation=45, ha='right', fontsize=7.5)
    ax_heat.set_yticks(range(len(window_names)))
    ax_heat.set_yticklabels(window_names, fontsize=8)
    ax_heat.tick_params(colors=text_col)
    ax_heat.set_facecolor(panel_bg)
    for spine in ax_heat.spines.values():
        spine.set_edgecolor(grid_col)
    ax_heat.set_title(
        'Total Return % — Each Earnings Window Strategy × All 30 DJIA Stocks',
        fontsize=11, fontweight='bold', color=text_col, pad=10
    )

    for row_idx in range(len(window_names)):
        for col_idx in range(len(tickers_sorted)):
            val = heat_matrix[row_idx, col_idx]
            if not np.isnan(val):
                txt_c = 'black' if abs(val) < vmax * 0.55 else 'white'
                ax_heat.text(col_idx, row_idx, f'{val:.0f}',
                             ha='center', va='center', fontsize=5.5,
                             color=txt_c, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.012, pad=0.01)
    cbar.ax.tick_params(colors=text_col, labelsize=7)
    cbar.set_label('Total Return %', color=text_col, fontsize=8)

    # B&H reference bar above heatmap
    ax_bah = ax_heat.inset_axes([0, 1.04, 1, 0.1])
    bah_colors = plt.cm.RdYlGn(np.clip((bah_vals + vmax) / (2 * vmax), 0, 1))
    ax_bah.bar(range(len(tickers_sorted)), bah_vals, color=bah_colors, width=0.85)
    ax_bah.set_xlim(-0.5, len(tickers_sorted) - 0.5)
    ax_bah.set_xticks([])
    ax_bah.set_yticks([])
    ax_bah.set_facecolor(panel_bg)
    for spine in ax_bah.spines.values():
        spine.set_edgecolor(grid_col)
    ax_bah.set_title('Buy & Hold Total Return % (reference)', color=text_col,
                     fontsize=7.5, pad=3)

    # --- Panel 2: Average total return per window (bar) + B&H reference ---
    style_ax(ax_bar)
    bah_avg_val = summary_df.loc[
        summary_df['Window'] == 'Buy & Hold', 'Avg Ret %'
    ].values[0]

    window_avgs = [
        summary_df.loc[summary_df['Window'] == w, 'Avg Ret %'].values[0]
        for w in window_names
    ]
    palette = ['#3fb950', '#58a6ff', '#f0883e', '#d2a8ff', '#ffa657']
    bars = ax_bar.bar(range(len(window_names)), window_avgs, color=palette, alpha=0.85, width=0.55)
    ax_bar.axhline(bah_avg_val, color='white', linewidth=1.5, linestyle='--', alpha=0.7,
                   label=f'Buy & Hold avg ({bah_avg_val:+.1f}%)')
    ax_bar.set_xticks(range(len(window_names)))
    ax_bar.set_xticklabels(window_names, fontsize=9)
    ax_bar.set_ylabel('Avg Total Return % (5-yr compounded)', fontsize=9)
    ax_bar.set_title('Average Total Return per Earnings Window Strategy Across 30 Stocks',
                     fontsize=10, fontweight='bold', pad=8)
    ax_bar.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax_bar.legend(fontsize=8.5, facecolor=panel_bg, edgecolor=grid_col, labelcolor=text_col)
    for bar, val in zip(bars, window_avgs):
        ax_bar.text(bar.get_x() + bar.get_width() / 2,
                    val + (0.5 if val >= 0 else -1.5),
                    f'{val:+.1f}%', ha='center', va='bottom', fontsize=8, color=text_col)

    # --- Panel 3: Year-by-year average return per window ---
    style_ax(ax_yr)
    years = [int(y) for y in year_cols]
    for idx, (wname, color) in enumerate(zip(window_names, palette)):
        row_data = summary_df[summary_df['Window'] == wname]
        if row_data.empty:
            continue
        yr_vals = [
            float(row_data[str(yr)].values[0])
            if str(yr) in row_data.columns and pd.notna(row_data[str(yr)].values[0])
            else np.nan
            for yr in years
        ]
        ax_yr.plot(years, yr_vals, marker='o', markersize=5, linewidth=1.6,
                   color=color, label=wname, alpha=0.9)

    # B&H year line
    bah_row_yr = summary_df[summary_df['Window'] == 'Buy & Hold']
    bah_yr_vals = [
        float(bah_row_yr[str(yr)].values[0])
        if str(yr) in bah_row_yr.columns and not bah_row_yr.empty
        else np.nan
        for yr in years
    ]
    ax_yr.plot(years, bah_yr_vals, marker='s', markersize=5, linewidth=1.6,
               color='white', linestyle='--', label='Buy & Hold avg', alpha=0.8)
    ax_yr.axhline(0, color=grid_col, linewidth=0.8, alpha=0.7)
    ax_yr.set_xticks(years)
    ax_yr.set_xticklabels([str(y) for y in years], fontsize=8)
    ax_yr.set_ylabel('Avg Annual Return %', fontsize=9)
    ax_yr.set_title('Year-by-Year Avg Return per Window (across 30 stocks)',
                    fontsize=9, fontweight='bold', pad=6)
    ax_yr.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax_yr.legend(fontsize=7, facecolor=panel_bg, edgecolor=grid_col,
                 labelcolor=text_col, ncol=2)

    # --- Panel 4: Per-event avg return (how much does each individual event earn?) ---
    style_ax(ax_event)
    event_avgs = []
    event_stds = []
    for wname in window_names:
        subset = results_df[results_df['Window'] == wname]
        per_event_rets = (
            subset['Total Return %'] / subset['Trades'].replace(0, np.nan)
        ).dropna()
        event_avgs.append(per_event_rets.mean())
        event_stds.append(per_event_rets.std())

    x = np.arange(len(window_names))
    bars2 = ax_event.bar(x, event_avgs, color=palette, alpha=0.85, width=0.55,
                         yerr=event_stds, capsize=4,
                         error_kw=dict(ecolor=text_col, elinewidth=1, capthick=1))
    ax_event.axhline(0, color=text_col, linewidth=0.6, alpha=0.5)
    ax_event.set_xticks(x)
    ax_event.set_xticklabels(window_names, fontsize=7.5, rotation=15, ha='right')
    ax_event.set_ylabel('Avg Return per Event %', fontsize=9)
    ax_event.set_title('Average Return per Individual Earnings Event\n(±1 std dev)',
                       fontsize=9, fontweight='bold', pad=6)
    ax_event.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.1f}%'))
    for bar, val in zip(bars2, event_avgs):
        if not np.isnan(val):
            ax_event.text(bar.get_x() + bar.get_width() / 2,
                          val + (0.05 if val >= 0 else -0.12),
                          f'{val:+.2f}%', ha='center', va='bottom',
                          fontsize=7.5, color=text_col)

    fig.suptitle('DJIA 30 — Earnings Announcement Effect Backtest (Script 3)',
                 fontsize=14, fontweight='bold', color=text_col, y=0.99)
    plt.savefig(CHART_PATH, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    print(f"Chart saved    → {CHART_PATH}")
    print("\nDone.")


if __name__ == '__main__':
    main()
