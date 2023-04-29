import MetaTrader5 as mt5
from .mt5_utils import UtilsMT5
import pandas as pd
import datetime
import os

utils = UtilsMT5()


class Indicators:
    def __init__(self):
        """This class contains indicators needed for the trade signals"""

    def i_sma(self, symbol, time_frame, period, price_type="close"):
        """This is an indicator that calculates the simple moving average for the specified period"""

        bar_count = period
        bars_df = utils.symbol_rates_df(symbol, time_frame, bar_count)
        bars_df[f"sma_{period}"] = bars_df[price_type].rolling(period).mean()
        sma = round(bars_df.iloc[-1][-1], 5)

        return sma

    def i_ema(self, symbol, time_frame, period, price_type="close"):
        """This is an indicator that calculates the exponential moving average for the specified period"""

        bar_count = period
        bars_df = utils.symbol_rates_df(symbol, time_frame, bar_count)
        bars_df[f"ema_{period}"] = (
            bars_df[price_type].ewm(span=period, min_periods=period).mean()
        )
        ema = round(bars_df.iloc[-1][-1], 5)

        return ema

    def i_atr(self, symbol, time_frame, period, price_type="close"):
        """This indicator calculates the range of the specified symbol over the specified period"""

        bar_count = period
        bars_df = utils.symbol_rates_df(symbol, time_frame, bar_count)

        bars_df["range"] = bars_df["high"] - bars_df["low"]
        bars_df[f"range_{period}"] = bars_df["range"].rolling(period).mean()
        atr = round(bars_df.iloc[-1][-1], 5)

        return atr

    def i_std_dev(self, symbol, time_frame, period, price_type="close"):
        """This indicator calculates the standard deviation of the specified symbol over the specified period"""

        bar_count = period
        bars_df = utils.symbol_rates_df(symbol, time_frame, bar_count)
        bars_df[f"std_dev_{period}"] = bars_df[price_type].rolling(period).mean()
        std_dev = round(bars_df.iloc[-1][-1], 5)

        return std_dev

    def calc_rsi_ma(self, ma_type, bars_df, period):
        """This indicator calculates the relative strength of the specified symbol over the specified period"""

        if ma_type == "sma":
            bars_df[f"{ma_type}_gain"] = bars_df["gain"].rolling(period).mean()
            bars_df[f"{ma_type}_loss"] = bars_df["loss"].rolling(period).mean()
        elif ma_type == "ema":
            bars_df[f"{ma_type}_gain"] = (
                bars_df["gain"].ewm(span=period, min_periods=period).mean()
            )
            bars_df[f"{ma_type}_loss"] = (
                bars_df["loss"].ewm(span=period, min_periods=period).mean()
            )
        else:
            print("Unsuported Moving Average type")

        return bars_df

    def i_rsi(self, symbol, time_frame, period, ma_type="sma", price_type="close"):

        bar_count = period + 1

        bars_df = utils.symbol_rates_df(symbol, time_frame, bar_count)
        bars_df["gain"] = (bars_df["close"] - bars_df["open"]).apply(
            lambda x: x if x > 0 else 0
        )
        bars_df["loss"] = (bars_df["close"] - bars_df["open"]).apply(
            lambda x: -x if x < 0 else 0
        )

        bars_df = self.calc_rsi_ma(ma_type, bars_df, period)
        bars_df["rs"] = (
            bars_df[f"{ma_type}_gain"] / bars_df[f"{ma_type}_loss"]
        )  # ma_gain/ ma_loss
        bars_df[f"rsi_{period}"] = 100 - (100 / (bars_df["rs"] + 1))
        rsi = round(bars_df.iloc[-1][-1], 2)
        print(rsi)
        print(bars_df.head(bar_count))

        return rsi
