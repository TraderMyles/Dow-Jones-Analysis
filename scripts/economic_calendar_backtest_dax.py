"""
Script 4 (DAX) — Economic Calendar Event Backtest on ^GDAXI

Tests how the DAX 40 index reacts around four major German/Eurozone
macro-economic release types (the German/ECB equivalents of Script 4's
US CPI/NFP/GDP/FOMC):

  CPI    — German CPI preliminary/flash estimate (monthly, Destatis)
  UNEMP  — German unemployment report (monthly, Bundesagentur fuer Arbeit —
           the closest German equivalent to US Non-Farm Payrolls)
  GDP    — German GDP flash estimate (quarterly, Destatis, ~30 days after
           quarter-end)
  ECB    — ECB Governing Council monetary policy rate decision (8x per
           year, decision announced 14:15 CET on day 2 of the meeting)

Five entry/exit windows are tested for each event type:

  1. Pre        [T-2 → T-1]  : enter 2 days before, exit 1 day before
  2. Day-of     [T-1 → T+1]  : enter 1 day before, exit 1 day after
  3. Post-Short [T+1 → T+3]  : enter 1 day after, exit 3 days after
  4. Post-Long  [T+1 → T+10] : enter 1 day after, exit 10 days after
  5. Full       [T-2 → T+5]  : enter 2 days before, exit 5 days after

T = release/decision date, mapped to nearest trading day.
Long only, $10,000 starting capital per strategy, no transaction costs.

Note: All four date lists are hardcoded from the primary-source release
      calendars (ECB, Destatis, Bundesagentur fuer Arbeit).

Outputs:
  - Terminal summary tables
  - ../outputs/economic_calendar_backtest_dax_results.csv
  - ../outputs/economic_calendar_backtest_dax_chart.png
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
END_DATE   = datetime.today()
START_DATE = END_DATE - timedelta(days=5 * 365)

WINDOWS = {
    'Pre [-2,-1]':       (-2, -1),
    'Day-of [-1,+1]':    (-1, +1),
    'Post-Short [+1,+3]':(+1, +3),
    'Post-Long [+1,+10]':(+1, +10),
    'Full [-2,+5]':      (-2, +5),
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH   = os.path.join(OUTPUT_DIR, 'economic_calendar_backtest_dax_results.csv')
CHART_PATH = os.path.join(OUTPUT_DIR, 'economic_calendar_backtest_dax_chart.png')

# ---------------------------------------------------------------------------
# Event date definitions
# ---------------------------------------------------------------------------

# Destatis German CPI preliminary/flash release dates (actual published schedule)
CPI_DATES_RAW = [
    # 2021
    '2021-06-29','2021-07-29','2021-08-30','2021-09-30','2021-10-28','2021-11-29',
    # 2022
    '2022-01-06','2022-01-31','2022-03-01','2022-03-30','2022-04-28','2022-05-30',
    '2022-06-29','2022-07-28','2022-08-30','2022-09-29','2022-10-28','2022-11-29',
    # 2023
    '2023-01-03','2023-02-09','2023-03-01','2023-03-30','2023-04-28','2023-05-31',
    '2023-06-29','2023-07-28','2023-08-30','2023-09-28','2023-10-30','2023-11-29',
    # 2024
    '2024-01-04','2024-02-08','2024-02-29','2024-04-02','2024-04-29','2024-05-29',
    '2024-07-01','2024-07-30','2024-08-29','2024-09-30','2024-10-30','2024-11-28',
    # 2025
    '2025-01-07','2025-01-31','2025-02-28','2025-03-31','2025-04-30','2025-05-30',
    '2025-06-30','2025-07-31','2025-08-29','2025-09-30','2025-10-30','2025-11-28',
    # 2026
    '2026-01-06','2026-01-30','2026-02-27','2026-03-30','2026-04-29','2026-05-29','2026-06-30',
]

# Bundesagentur fuer Arbeit monthly unemployment report dates (actual published schedule)
UNEMPLOYMENT_DATES_RAW = [
    # 2021
    '2021-06-01','2021-06-30','2021-07-29','2021-08-31','2021-09-30','2021-10-28','2021-11-30',
    # 2022
    '2022-01-04','2022-02-01','2022-03-02','2022-03-31','2022-05-03','2022-05-31',
    '2022-06-30','2022-07-29','2022-08-31','2022-09-30','2022-11-02','2022-11-30',
    # 2023
    '2023-01-03','2023-01-31','2023-03-01','2023-03-31','2023-04-28','2023-05-31',
    '2023-06-30','2023-08-01','2023-08-31','2023-09-29','2023-11-02','2023-11-30',
    # 2024
    '2024-01-03','2024-01-31','2024-02-29','2024-03-28','2024-04-30','2024-06-04',
    '2024-06-28','2024-07-31','2024-08-30','2024-09-27','2024-10-30','2024-11-29',
    # 2025
    '2025-01-03','2025-01-31','2025-02-28','2025-03-28','2025-04-30','2025-05-28',
    '2025-07-01','2025-07-31','2025-08-29','2025-09-30','2025-10-30','2025-11-28',
    # 2026
    '2026-01-07','2026-01-30','2026-02-27','2026-03-31','2026-04-30','2026-05-29','2026-06-30','2026-07-31',
]

# Destatis German GDP flash/preliminary quarterly estimate dates (~30 days after quarter-end)
GDP_DATES_RAW = [
    # 2021
    '2021-07-30','2021-10-29',
    # 2022
    '2022-01-28','2022-04-29','2022-07-29','2022-10-28',
    # 2023
    '2023-01-30','2023-04-28','2023-07-28','2023-10-30',
    # 2024
    '2024-01-30','2024-04-30','2024-07-30','2024-10-30',
    # 2025
    '2025-01-30','2025-04-30','2025-07-30','2025-10-30',
    # 2026
    '2026-01-30','2026-04-30',
]

# ECB Governing Council monetary policy rate decision dates (day 2 of meeting)
ECB_DATES_RAW = [
    # 2021
    '2021-06-10','2021-07-22','2021-09-09','2021-10-28','2021-12-16',
    # 2022
    '2022-02-03','2022-03-10','2022-04-14','2022-06-09','2022-07-21','2022-09-08','2022-10-27','2022-12-15',
    # 2023
    '2023-02-02','2023-03-16','2023-05-04','2023-06-15','2023-07-27','2023-09-14','2023-10-26','2023-12-14',
    # 2024
    '2024-01-25','2024-03-07','2024-04-11','2024-06-06','2024-07-18','2024-09-12','2024-10-17','2024-12-12',
    # 2025
    '2025-01-30','2025-03-06','2025-04-17','2025-06-05','2025-07-24','2025-09-11','2025-10-30','2025-12-18',
    # 2026
    '2026-02-05','2026-03-19','2026-04-30','2026-06-11','2026-07-23',
]


def parse_dates(raw_list):
    return sorted(
        pd.Timestamp(d).normalize()
        for d in raw_list
        if START_DATE.date() <= pd.Timestamp(d).date() <= END_DATE.date()
    )


EVENT_DATES = {
    'CPI':   parse_dates(CPI_DATES_RAW),
    'UNEMP': parse_dates(UNEMPLOYMENT_DATES_RAW),
    'GDP':   parse_dates(GDP_DATES_RAW),
    'ECB':   parse_dates(ECB_DATES_RAW),
}

EVENT_COLORS = {
    'CPI':  '#58a6ff',
    'UNEMP':  '#3fb950',
    'GDP':  '#ffa657',
    'ECB': '#f85149',
}

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_data():
    print(f"Fetching {TICKER} data ({START_DATE.date()} → {END_DATE.date()}) ...")
    raw = yf.download(TICKER, start=START_DATE.strftime('%Y-%m-%d'),
                      end=END_DATE.strftime('%Y-%m-%d'), progress=False)
    if raw.empty:
        sys.exit("ERROR: no data from yfinance")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    close = raw['Close'].dropna()
    print(f"  {len(close)} trading days  "
          f"({close.index[0].date()} – {close.index[-1].date()})")
    return close


# ---------------------------------------------------------------------------
# Backtest engine
# ---------------------------------------------------------------------------
def nearest_trading_day(target, trading_days):
    target = pd.Timestamp(target).normalize()
    if target in trading_days:
        return target
    future = trading_days[trading_days >= target]
    return future[0] if len(future) else None


def offset_day(base, offset, trading_days):
    idx = trading_days.searchsorted(base)
    if idx >= len(trading_days) or trading_days[idx] != base:
        return None
    new_idx = idx + offset
    return trading_days[new_idx] if 0 <= new_idx < len(trading_days) else None


def run_event_backtest(close, event_dates, entry_offset, exit_offset):
    """
    Simulate long-only trades around a list of event dates.
    Returns equity Series (keyed by exit date), trade list, yearly returns dict.
    """
    trading_days = close.index

    events = []
    for raw_date in event_dates:
        t_day     = nearest_trading_day(raw_date, trading_days)
        if t_day is None:
            continue
        entry_day = offset_day(t_day, entry_offset, trading_days)
        exit_day  = offset_day(t_day, exit_offset,  trading_days)
        if entry_day is None or exit_day is None or entry_day >= exit_day:
            continue
        events.append((entry_day, exit_day))

    if not events:
        return None, [], {}

    events.sort(key=lambda x: x[0])

    # Remove overlapping windows (keep earlier trade)
    clean = []
    last_exit = pd.Timestamp.min
    for entry_day, exit_day in events:
        if entry_day > last_exit:
            clean.append((entry_day, exit_day))
            last_exit = exit_day

    capital    = START_CAPITAL
    trades     = []
    yr_returns = {}
    equity_pts = {}

    for entry_day, exit_day in clean:
        ep = close.loc[entry_day]
        xp = close.loc[exit_day]
        if pd.isna(ep) or pd.isna(xp) or ep <= 0:
            continue
        ret     = xp / ep - 1
        capital *= (1 + ret)
        yr = entry_day.year
        yr_returns.setdefault(yr, []).append(ret)
        equity_pts[exit_day] = capital
        trades.append({'entry': entry_day, 'exit': exit_day,
                       'return_pct': round(ret * 100, 4)})

    if not trades:
        return None, [], {}

    equity = pd.Series(equity_pts).sort_index()
    yearly = {yr: round((np.prod([1 + r for r in rets]) - 1) * 100, 2)
              for yr, rets in yr_returns.items()}
    return equity, trades, yearly


def calc_max_drawdown(equity_series):
    arr     = equity_series.values
    run_max = np.maximum.accumulate(arr)
    dds     = (arr - run_max) / run_max
    return round(dds.min() * 100, 2)


def buy_and_hold_metrics(close):
    rets    = close.pct_change().fillna(0)
    equity  = START_CAPITAL * (1 + rets).cumprod()
    total   = round((equity.iloc[-1] / START_CAPITAL - 1) * 100, 2)
    run_max = equity.expanding().max()
    max_dd  = round(((equity - run_max) / run_max).min() * 100, 2)
    yearly  = {yr: round(((1 + rets[rets.index.year == yr]).prod() - 1) * 100, 2)
               for yr in sorted(rets.index.year.unique())}
    return total, max_dd, yearly, equity


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    close = fetch_data()

    for etype, dates in EVENT_DATES.items():
        print(f"  {etype}: {len(dates)} events in window")
    print()

    bah_total, bah_dd, bah_yearly, bah_equity = buy_and_hold_metrics(close)
    year_cols_set = set(str(y) for y in bah_yearly)

    all_rows = []

    # B&H row
    bah_row = {
        'Event Type': '—', 'Window': 'Buy & Hold',
        'Total Return %': bah_total, 'Max Drawdown %': bah_dd,
        'Win Rate %': '—', 'Events': 0,
    }
    bah_row.update({str(yr): ret for yr, ret in bah_yearly.items()})
    all_rows.append(bah_row)

    equity_store = {}   # (event_type, window_name) -> equity Series

    for event_type in ['CPI', 'UNEMP', 'GDP', 'ECB']:
        event_dates = EVENT_DATES[event_type]
        print(f"Running {event_type} ({len(event_dates)} events) ...")
        for window_name, (entry_off, exit_off) in WINDOWS.items():
            equity, trades, yearly = run_event_backtest(
                close, event_dates, entry_off, exit_off
            )
            if equity is None or not trades:
                row = {
                    'Event Type': event_type, 'Window': window_name,
                    'Total Return %': 0.0, 'Max Drawdown %': 0.0,
                    'Win Rate %': 0.0, 'Events': 0,
                }
            else:
                total_ret = round((equity.iloc[-1] / START_CAPITAL - 1) * 100, 2)
                max_dd    = calc_max_drawdown(equity)
                win_rate  = round(
                    sum(1 for t in trades if t['return_pct'] > 0) / len(trades) * 100, 1
                )
                row = {
                    'Event Type':    event_type,
                    'Window':        window_name,
                    'Total Return %': total_ret,
                    'Max Drawdown %': max_dd,
                    'Win Rate %':    win_rate,
                    'Events':        len(trades),
                }
                row.update({str(yr): ret for yr, ret in yearly.items()})
                year_cols_set.update(str(yr) for yr in yearly)
                equity_store[(event_type, window_name)] = equity

            all_rows.append(row)

    # ---------------------------------------------------------------------------
    # Build DataFrame
    # ---------------------------------------------------------------------------
    results_df = pd.DataFrame(all_rows)
    year_cols  = sorted(year_cols_set)
    for yc in year_cols:
        if yc not in results_df.columns:
            results_df[yc] = np.nan

    fixed = ['Event Type', 'Window', 'Total Return %', 'Max Drawdown %',
             'Win Rate %', 'Events']
    results_df = results_df[fixed + year_cols]

    # ---------------------------------------------------------------------------
    # Terminal summary
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 110)
    print("DAX 40 (^GDAXI) — ECONOMIC CALENDAR EVENT BACKTEST")
    print(f"Period: {close.index[0].date()} to {close.index[-1].date()}  "
          f"|  Capital: ${START_CAPITAL:,}  |  Instrument: {TICKER}")
    print("=" * 110)

    for event_type in ['CPI', 'UNEMP', 'GDP', 'ECB']:
        print(f"\n--- {event_type} ---")
        subset = results_df[results_df['Event Type'] == event_type].copy()
        disp   = subset.copy()
        for col in ['Total Return %', 'Max Drawdown %'] + year_cols:
            if col in disp.columns:
                disp[col] = disp[col].map(
                    lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A"
                )
        print(disp.drop(columns=['Event Type']).to_string(index=False))

    print("\n--- BUY & HOLD (reference) ---")
    bah_disp = results_df[results_df['Window'] == 'Buy & Hold'].copy()
    for col in ['Total Return %', 'Max Drawdown %'] + year_cols:
        if col in bah_disp.columns:
            bah_disp[col] = bah_disp[col].map(
                lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A"
            )
    print(bah_disp.to_string(index=False))

    # Best window per event type
    print("\n--- BEST WINDOW PER EVENT TYPE ---\n")
    non_bah = results_df[results_df['Window'] != 'Buy & Hold']
    for event_type in ['CPI', 'UNEMP', 'GDP', 'ECB']:
        sub     = non_bah[non_bah['Event Type'] == event_type]
        best    = sub.loc[sub['Total Return %'].idxmax()]
        per_evt = round(best['Total Return %'] / best['Events'], 2) if best['Events'] > 0 else 0
        print(f"  {event_type:<6} best window: {best['Window']:<22} "
              f"total={best['Total Return %']:+.1f}%  "
              f"win_rate={best['Win Rate %']}%  "
              f"per_event={per_evt:+.2f}%  "
              f"events={int(best['Events'])}")

    print(f"\n  B&H total: {bah_total:+.1f}%\n")
    print("=" * 110)

    # ---------------------------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------------------------
    results_df.to_csv(CSV_PATH, index=False)
    print(f"\nResults saved → {CSV_PATH}  ({len(results_df)} rows)")

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

    ax_price = fig.add_subplot(gs[0, :])   # price + event markers
    ax_heat  = fig.add_subplot(gs[1, :])   # heatmap: event×window returns
    ax_yr    = fig.add_subplot(gs[2, 0])   # year-by-year for day-of window
    ax_win   = fig.add_subplot(gs[2, 1])   # win rate bar chart

    # --- Panel 1: DAX 40 price with event date markers ---
    style_ax(ax_price)
    ax_price.plot(close.index, close.values, color='#58a6ff',
                  linewidth=1.0, label='^GDAXI Close', zorder=3)

    for event_type, color in EVENT_COLORS.items():
        dates = EVENT_DATES[event_type]
        valid = [d for d in dates if d in close.index or
                 nearest_trading_day(d, close.index) is not None]
        snapped = [nearest_trading_day(d, close.index) for d in valid]
        snapped = [d for d in snapped if d is not None]

        for i, d in enumerate(snapped):
            ax_price.axvline(d, color=color, linewidth=0.55, alpha=0.35, zorder=2)
        # Invisible dummy line for legend entry
        if snapped:
            ax_price.axvline(snapped[0], color=color, linewidth=1.5, alpha=0.9,
                             label=f'{event_type} ({len(snapped)})', zorder=2)

    ax_price.set_title(f'^GDAXI Close Price with Economic Event Dates',
                       fontsize=11, fontweight='bold', pad=8)
    ax_price.set_ylabel('Index Level', fontsize=9)
    ax_price.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax_price.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax_price.legend(fontsize=8, loc='upper left', facecolor=panel_bg,
                    edgecolor=grid_col, labelcolor=text_col, ncol=5)

    # --- Panel 2: Heatmap — event types × windows (total return %) ---
    style_ax(ax_heat)
    event_types   = ['CPI', 'UNEMP', 'GDP', 'ECB']
    window_names  = list(WINDOWS.keys())
    heat_matrix   = np.full((len(event_types), len(window_names)), np.nan)

    for row_idx, etype in enumerate(event_types):
        for col_idx, wname in enumerate(window_names):
            val = results_df.loc[
                (results_df['Event Type'] == etype) &
                (results_df['Window'] == wname),
                'Total Return %'
            ]
            if not val.empty:
                heat_matrix[row_idx, col_idx] = val.values[0]

    vmax = max(np.nanmax(np.abs(heat_matrix)), 5)
    im   = ax_heat.imshow(heat_matrix, aspect='auto', cmap='RdYlGn',
                          vmin=-vmax, vmax=vmax, interpolation='nearest')
    ax_heat.set_xticks(range(len(window_names)))
    ax_heat.set_xticklabels(window_names, fontsize=10)
    ax_heat.set_yticks(range(len(event_types)))
    ax_heat.set_yticklabels(event_types, fontsize=11, fontweight='bold')
    ax_heat.tick_params(colors=text_col)
    for spine in ax_heat.spines.values():
        spine.set_edgecolor(grid_col)
    ax_heat.set_title('Total Return % by Event Type × Window  (5-yr compounded, $10k start)',
                      fontsize=11, fontweight='bold', color=text_col, pad=10)

    for row_idx in range(len(event_types)):
        for col_idx in range(len(window_names)):
            val = heat_matrix[row_idx, col_idx]
            if not np.isnan(val):
                txt_c = 'black' if abs(val) < vmax * 0.5 else 'white'
                ax_heat.text(col_idx, row_idx, f'{val:+.1f}%',
                             ha='center', va='center', fontsize=11,
                             color=txt_c, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.025, pad=0.01,
                        orientation='vertical')
    cbar.ax.tick_params(colors=text_col, labelsize=8)
    cbar.set_label('Total Return %', color=text_col, fontsize=9)
    # B&H reference line on colorbar
    cbar.ax.axhline((bah_total + vmax) / (2 * vmax), color='white',
                    linewidth=1.5, linestyle='--')

    # --- Panel 3: Year-by-year for Day-of window ---
    style_ax(ax_yr)
    years     = [int(y) for y in year_cols]
    day_of_wn = 'Day-of [-1,+1]'
    palette   = [EVENT_COLORS[et] for et in event_types]

    for etype, color in zip(event_types, palette):
        row_data = results_df[
            (results_df['Event Type'] == etype) &
            (results_df['Window'] == day_of_wn)
        ]
        if row_data.empty:
            continue
        yr_vals = [
            float(row_data[str(yr)].values[0])
            if str(yr) in row_data.columns and pd.notna(row_data[str(yr)].values[0])
            else np.nan
            for yr in years
        ]
        ax_yr.plot(years, yr_vals, marker='o', markersize=5,
                   linewidth=1.6, color=color, label=etype, alpha=0.9)

    # B&H reference
    bah_yr_vals = [bah_yearly.get(yr, np.nan) for yr in years]
    ax_yr.plot(years, bah_yr_vals, marker='s', markersize=4,
               linewidth=1.4, color='white', linestyle='--',
               label='Buy & Hold', alpha=0.7)

    ax_yr.axhline(0, color=grid_col, linewidth=0.8, alpha=0.7)
    ax_yr.set_xticks(years)
    ax_yr.set_xticklabels([str(y) for y in years], fontsize=8)
    ax_yr.set_ylabel('Annual Return %', fontsize=9)
    ax_yr.set_title(f'Year-by-Year Return — "{day_of_wn}" Window',
                    fontsize=9, fontweight='bold', pad=6)
    ax_yr.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax_yr.legend(fontsize=8, facecolor=panel_bg, edgecolor=grid_col,
                 labelcolor=text_col, ncol=2)

    # --- Panel 4: Win rate by event × window (grouped bar) ---
    style_ax(ax_win)
    x      = np.arange(len(event_types))
    width  = 0.16
    wnames = list(WINDOWS.keys())
    win_palette = plt.cm.plasma(np.linspace(0.15, 0.85, len(wnames)))

    offsets = np.linspace(-(len(wnames) - 1) * width / 2,
                          (len(wnames) - 1) * width / 2,
                          len(wnames))

    for idx, (wname, offset) in enumerate(zip(wnames, offsets)):
        win_rates = []
        for etype in event_types:
            val = results_df.loc[
                (results_df['Event Type'] == etype) &
                (results_df['Window'] == wname),
                'Win Rate %'
            ]
            wr = float(val.values[0]) if not val.empty and val.values[0] != '—' else 50.0
            win_rates.append(wr)
        ax_win.bar(x + offset, win_rates, width=width,
                   color=win_palette[idx], alpha=0.85, label=wname)

    ax_win.axhline(50, color=text_col, linewidth=1.0, linestyle='--',
                   alpha=0.5, label='50% (random)')
    ax_win.set_xticks(x)
    ax_win.set_xticklabels(event_types, fontsize=10, fontweight='bold')
    ax_win.set_ylabel('Win Rate %', fontsize=9)
    ax_win.set_title('Win Rate by Event Type and Window',
                     fontsize=9, fontweight='bold', pad=6)
    ax_win.set_ylim(0, 100)
    ax_win.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    ax_win.legend(fontsize=6.5, facecolor=panel_bg, edgecolor=grid_col,
                  labelcolor=text_col, ncol=2, loc='lower right')

    fig.suptitle('DAX 40 — Economic Calendar Event Backtest (Script 4)',
                 fontsize=14, fontweight='bold', color=text_col, y=0.99)
    plt.savefig(CHART_PATH, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    print(f"Chart saved    → {CHART_PATH}")
    print("\nDone.")


if __name__ == '__main__':
    main()
