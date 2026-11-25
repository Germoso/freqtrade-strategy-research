"""Send alerts when four EMAs first align on a closed candle."""

import logging

import talib.abstract as ta
from freqtrade.enums import RunMode
from freqtrade.exceptions import OperationalException
from freqtrade.strategy import IStrategy
from pandas import DataFrame

logger = logging.getLogger(__name__)


class EMAAlignmentAlerts(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "5m"
    startup_candle_count = 400
    minimal_roi = {}
    stoploss = -0.99

    def bot_start(self, **kwargs):
        if self.config.get("runmode") != RunMode.DRY_RUN:
            raise OperationalException("EMAAlignmentAlerts requires dry-run mode.")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for period in (10, 20, 50, 200):
            dataframe[f"ema{period}"] = ta.EMA(dataframe, timeperiod=period)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0
        if len(dataframe) < 2 or self.dp.runmode != RunMode.DRY_RUN:
            return dataframe

        candles = dataframe.iloc[-2:]
        fast, short, medium, slow = (candles[f"ema{period}"] for period in (10, 20, 50, 200))
        bullish = (fast > short) & (short > medium) & (medium > slow)
        bearish = (fast < short) & (short < medium) & (medium < slow)

        for alignment, direction, order in (
            (bullish, "alcista", "EMA10 > EMA20 > EMA50 > EMA200"),
            (bearish, "bajista", "EMA10 < EMA20 < EMA50 < EMA200"),
        ):
            if alignment.iloc[-1] and not alignment.iloc[-2]:
                candle = candles["date"].iloc[-1]
                pair = metadata["pair"]
                message = f"{pair} {self.timeframe} | Alineación {direction} | {order} | Vela {candle}"
                logger.info(message)
                self.dp.send_msg(message)
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0
        return dataframe
