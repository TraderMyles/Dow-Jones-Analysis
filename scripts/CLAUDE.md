# Backtesting scripts — rules

## Strategy logic (IMPORTANT — YOU MUST follow this exactly)
- Buy signal: short MA crosses ABOVE long MA
- Sell/exit signal: short MA crosses BELOW long MA
- Long only — no shorting under any circumstances
- When not in a position, cash earns 0% (no risk-free rate)
- Assume $10,000 starting capital per backtest
- No transaction costs unless explicitly added later

## MA pairs to test
SMA: 20, 50, 100, 200
EMA: 9, 21, 50, 200
Crossover pairs: (9,21), (20,50), (50,200), (9,50), (21,200)

## Output format — every script must produce all three
1. Terminal summary table (print to console)
2. CSV saved to ../outputs/<script_name>_results.csv
3. Chart saved to ../outputs/<script_name>_chart.png

## Year-by-year breakdown
Every backtest must show results split by calendar year (2020, 2021, 2022, 2023, 2024)
as well as an overall 5-year total. Include a buy-and-hold benchmark column in every table.

## Code style
- Use pandas for all data manipulation
- Use matplotlib for charts — no plotly or other libraries
- Add a comment block at the top of each script explaining what it does
- Use clear variable names — no single letter variables except i in loops
- IMPORTANT: add print statements so the user can see progress while running