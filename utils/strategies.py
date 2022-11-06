from .indicators import Indicators
from .mt5_utils import UtilsMT5
import MetaTrader5 as mt5

utils = UtilsMT5()
i = Indicators()


class Strategies:
    def __init__(self):
        self.strat = "Elliott"

    def high_frequency(self):
        strat_dict = {}
        return strat_dict

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
