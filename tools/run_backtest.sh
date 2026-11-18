#!/usr/bin/env bash
# Example: run backtest for XAU on OKX 5m
set -euo pipefail
cd "${1:-.}"
freqtrade backtesting \
  --config config/config-xau-okx-5m.json \
  --strategy EMACrossDetTrendFilterTP15SL20 \
  --pairs "XAU/USDT:USDT" \
  --timeframe 5m \
  --datadir user_data/data/okx \
  --timerange 20250409-
PY
chmod +x /home/germoso/code/freqtrade-strategy-research/tools/run_backtest.sh
echo done