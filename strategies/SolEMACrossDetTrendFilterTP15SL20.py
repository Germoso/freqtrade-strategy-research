"""SolEMACrossDetTrendFilterTP15SL20

Deterministic EMA10/EMA20 crossover entries, filtered by EMA200 (trend alignment),
with fixed TP 1.5% / SL 2.0% brackets. Research-only.

Replicates the best-performing variant found in the SOL/LINK/XAU studies.
"""
from freqtrade.strategy import IStrategy
from freqtrade.enums import RunMode
from freqtrade.exceptions import OperationalException
import talib.abstract as ta
from pandas import DataFrame


class SolEMACrossDetTrendFilterTP15SL20(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '5m'
    can_short = True
    startup_candle_count = 250
    stoploss = -0.020
    minimal_roi = {}
    use_custom_roi = True
    use_exit_signal = False
    trailing_stop = False
    position_adjustment_enable = False
    order_types = {'entry': 'market', 'exit': 'market', 'stoploss': 'market',
                   'stoploss_on_exchange': False}

    def bot_start(self, **kwargs):
        if self.config.get('runmode') not in (RunMode.BACKTEST, RunMode.WEBSERVER):
            raise OperationalException('SolEMACrossDetTrendFilterTP15SL20 is research only.')

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 1.0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        valid = ((dataframe['volume'] > 0)
                 & dataframe['ema10'].notna()
                 & dataframe['ema20'].notna()
                 & dataframe['ema200'].notna())
        cross_up = ((dataframe['ema10'] > dataframe['ema20'])
                    & (dataframe['ema10'].shift(1) <= dataframe['ema20'].shift(1)))
        cross_down = ((dataframe['ema10'] < dataframe['ema20'])
                      & (dataframe['ema10'].shift(1) >= dataframe['ema20'].shift(1)))
        aligned_long = cross_up & (dataframe['close'] > dataframe['ema200'])
        aligned_short = cross_down & (dataframe['close'] < dataframe['ema200'])
        dataframe['enter_long'] = (valid & aligned_long).astype(int)
        dataframe['enter_short'] = (valid & aligned_short).astype(int)
        dataframe['enter_tag'] = 'cross_aligned'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_roi(self, pair, trade, current_time, trade_duration, entry_tag, side, **kwargs):
        target = trade.open_rate * (1.015 if not trade.is_short else 0.985)
        return trade.calc_profit_ratio(target)
PY
echo done