from .indicators import Indicators
from .mt5_utils import UtilsMT5
import MetaTrader5 as mt5

utils = UtilsMT5()
i = Indicators()


class Strategies:
    def __init__(self):
        self.strat = "Elliott"
        self.jpy_multiplier = 1000
        self.other_multiplier = 100000
        self.std_lot_contract = 100000

    def high_frequency(
        self,
        symbol: str,
        time_frame: str,

    ):
        """High frequency strategy that tries to find quick entries for the current trend"""
        
        bars_df = utils.get_symbol_rates_df(symbol, time_frame, bars_count=24)
        
        average_price_move = bars_df['close'].mean()

        
        if average_price_move < -200 / self.other_multiplier:
            trend = "down"
        elif average_price_move > 200 / self.other_multiplier: 
            trend = "up"

        # TODO stop_loss is at previous candle in opposite direction of trend 

        while True:
            positions = mt5.positions_get(symbol=symbol)
            if len(positions) == 0:
                if trend == "down":
                    utils.place_order('SELL', symbol, sl_points=200, trade_reason='trend', rr=0.5, risk_perc=2)

                if trend == "down":
                    utils.place_order('BUY', symbol, sl_points=200, trade_reason='trend', rr=0.5, risk_perc=2)

        return

    def mean_revert(self):
        """Sell when RSI overbought/Buy when RSI , ATR is low, std_dev is low"""

    def trend(self):
        """Trade a new trend that starts"""

    def test_strat(
        self,
        symbol,
        time_frame,
        period,
        sl_points,
        risk_perc=2,
        rr=2,
        ma_type="sma",
        price_type="close",
    ):
        rsi = i.i_rsi(symbol, time_frame, period, ma_type)
        # sma = i.i_sma(self, symbol, time_frame, period, price_type)

        while True:
            if rsi > 70:
                positions = mt5.positions_get(symbol=symbol)
                if len(positions) == 0:
                    signal = "sell"
                    trade_type, symbol, lots, sl_points, rr = utils.get_lot_size(
                        signal, sl_points, risk_perc, symbol, rr
                    )
                    utils.place_order(trade_type, symbol, lots, sl_points, rr)
                    print(f"Successfully opened a {signal} order")
            elif rsi < 30:
                positions = mt5.positions_get(symbol=symbol)
                if len(positions) == 0:
                    signal = "buy"
                    trade_type, symbol, lots, sl_points, rr = utils.get_lot_size(
                        signal, 400, 2, symbol, rr
                    )
                    utils.place_order(trade_type, symbol, lots, sl_points, rr)
                    print(f"Successfully opened a {signal} order")
