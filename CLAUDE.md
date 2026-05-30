# Dow Jones Analysis Project

## Project overview
Five independent backtesting scripts for analysing the Dow Jones Industrial Average (YM futures).
Each script is standalone — do not import between them or create shared modules unless explicitly asked.

## Setup commands
pip install yfinance pandas numpy matplotlib seaborn scipy

## Project structure
scripts/
  ma_backtest_dow.py          # Script 1 — MA backtest on DJIA index
  ma_backtest_stocks.py       # Script 2 — MA backtest on all 30 components
  earnings_backtest.py        # Script 3 — Earnings announcement effect
  economic_calendar_backtest.py  # Script 4 — CPI, NFP, GDP, FOMC impact
  correlation_trading.py      # Script 5 — Correlation vs NQ, ES, VIX, yields
outputs/                      # All charts and CSV results go here

## Workflow
- Run /init before starting any script task
- Always verify the script runs end to end before finishing
- After each script is complete, output a summary of results to the terminal
- IMPORTANT: never modify a completed script unless explicitly asked

## Data source
- All market data via yfinance only
- Date range: 5 years back from today unless stated otherwise
- DJIA ticker: ^DJI
- YM futures proxy: use ^DJI (cash) since yfinance has limited futures history

@scripts/CLAUDE.md