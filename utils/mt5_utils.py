import MetaTrader5 as mt5
import configparser
import pandas as pd
from datetime import datetime as dt
import sys
import os


config = configparser.ConfigParser()
config_path = os.path.dirname(os.path.dirname(__file__))
config.read(f"{config_path}/config.ini")


class UtilsMT5:
    def __init__(self):
        self.jpy_multiplier = 1000
        self.other_multiplier = 100000
        self.std_lot_contract = 100000

    def mt5_init(self, environment):
        path = config[environment]["path"]
        login = config[environment]["login"]
        password = config[environment]["password"]
        server = config[environment]["server"]

        if not mt5.initialize(
            path=path, login=int(login), password=password, server=server
        ):
            print("initialize() failed, error code =", mt5.last_error())
            quit()

    def get_stop_loss(self, trade_type, symbol, order_price, points):

        if trade_type == mt5.ORDER_TYPE_BUY:
            if "JPY" in symbol:
                stop_loss = order_price - points / self.jpy_multiplier
            else:
                stop_loss = order_price - points / self.other_multiplier
        else:
            if "JPY" in symbol:
                stop_loss = order_price + points / self.jpy_multiplier
            else:
                stop_loss = order_price + points / self.other_multiplier

        return stop_loss

    def get_mt5_time_frame(self, time_frame):
        """This function takes the core Metatrader application time_frames( M1, M5, M15, H1, H4, D1, W1) and converts it into mt5 code time_frames"""

        if time_frame.lower() == "m1":
            mt5_time_frame = mt5.TIMEFRAME_M1
        elif time_frame.lower() == "m5":
            mt5_time_frame = mt5.TIMEFRAME_M5
        elif time_frame.lower() == "m15":
            mt5_time_frame = mt5.TIMEFRAME_M15
        elif time_frame.lower() == "h1":
            mt5_time_frame = mt5.TIMEFRAME_H1
        elif time_frame.lower() == "h4":
            mt5_time_frame = mt5.TIMEFRAME_H4
        elif time_frame.lower() == "d1":
            mt5_time_frame = mt5.TIMEFRAME_D1
        elif time_frame.lower() == "w1":
            mt5_time_frame = mt5.TIMEFRAME_W1
        else:
            print("Timeframe not supported")
            exit(1)
        return mt5_time_frame

    def get_take_profit(self, trade_type, symbol, order_price, sl_points, risk_reward):

        if trade_type == mt5.ORDER_TYPE_BUY:
            if "JPY" in symbol:
                take_profit = order_price + (
                    sl_points / self.jpy_multiplier * risk_reward
                )
            else:
                take_profit = order_price + (
                    sl_points / self.other_multiplier * risk_reward
                )
        else:
            if "JPY" in symbol:
                take_profit = order_price - (
                    sl_points / self.jpy_multiplier * risk_reward
                )
            else:
                take_profit = order_price - (
                    sl_points / self.other_multiplier * risk_reward
                )

        return take_profit

    @staticmethod
    def validate_sl_tp(trade_type, order_price, stop_loss, take_profit):

        if trade_type.lower() == "buy":
            if stop_loss > order_price:
                print("Invalid Stop Loss")
                exit(1)
            if take_profit < order_price:
                print("Invalid Take Profit")
                exit(1)
        elif trade_type.lower() == "sell":
            if stop_loss < order_price:
                print("Invalid Stop Loss")
                exit(0)
            if take_profit > order_price:
                print("Invalid Take Profit")
                exit(1)

    @staticmethod
    def set_order_price(trade_type, symbol):
        if trade_type.lower() == "buy":
            order_price = mt5.symbol_info_tick(symbol).ask
        elif trade_type.lower() == "sell":
            order_price = mt5.symbol_info_tick(symbol).bid
        else:
            "Not a valid trade type"
            exit(0)
        return order_price

    @staticmethod
    def set_order_type(trade_type):
        if trade_type.lower() == "buy":
            order_type = mt5.ORDER_TYPE_BUY
        elif trade_type.lower() == "sell":
            order_type = mt5.ORDER_TYPE_SELL
        else:
            "Not a valid trade type"
            exit(1)
        return order_type

    def get_currency_pair(self, base):
        quote = str(mt5.account_info().currency)
        base = str(base)
        symbols = [symb.name for symb in mt5.symbols_get()]
        for symb in symbols:
            if base + quote == symb:
                symbol = symb
                break
            elif quote + base == symb:
                symbol = symb
                break
            else:
                symbol = None

        if base == symbol[-3:]:
            reciprocate = True
        else:
            reciprocate = False
        return symbol, reciprocate

    def symbol_std_lot_pip(self, symbol, order_price):
        """This function gets the pip value for the symbol when the volume is 1 standard lot (1.00)"""

        if "JPY" not in symbol:
            symbol_std_lot_pip = (0.0001 * self.std_lot_contract) / round(
                order_price, 5
            )
        else:
            symbol_std_lot_pip = (0.01 * self.std_lot_contract) / round(order_price, 5)

        return symbol_std_lot_pip

    def get_pip_value(self, trade_type, symbol, order_price):
        """This function returns the standard lot pip value of a trading_pair in the account's currency value.
        e.g for GBPCAD the pip value will be returned in USD if the account is in USD"""

        acc_currency = mt5.account_info().currency
        symbol_std_lot_pip = self.symbol_std_lot_pip(symbol, order_price)

        if symbol[:3] == acc_currency:
            acc_curr_pip_value = symbol_std_lot_pip
        else:
            symbol_check, reciprocate = self.get_currency_pair(symbol[:3])

            if reciprocate:
                multiplier = self.set_order_price(trade_type, symbol_check) ** -1
            else:
                multiplier = self.set_order_price(trade_type, symbol_check)

            acc_curr_pip_value = symbol_std_lot_pip * multiplier

        return acc_curr_pip_value

    def place_order(self, trade_type, symbol, sl_points, trade_reason, rr=2, risk_perc=1):
        """Place an order with desired stop loss points distance from the current ask or bid price

        trade_type: buy/sell
        symbol: one of the trading pairs supported by the broker
        sl_points: points distance from entry point
        risk_perc:  default 1%
        rr: risk:reward ratio
        """

        vol = self.get_lot_size(trade_type, symbol, sl_points, risk_perc, rr)
        order_price = self.set_order_price(trade_type, symbol)
        order_type = self.set_order_type(trade_type)
        stop_loss = self.get_stop_loss(order_type, symbol, order_price, sl_points)
        take_profit = self.get_take_profit(
            order_type, symbol, order_price, rr, sl_points
        )
        self.validate_sl_tp(trade_type, order_price, stop_loss, take_profit)

        print(f"stop loss at : {round(stop_loss, 5)}")
        print(f"take profit at : {round(take_profit, 5)}")

        trade_comment = journal.trade_reason(trade_reason)
        print(trade_comment)

        order_result = mt5.order_send(
            action=mt5.TRADE_ACTION_DEAL,
            symbol=symbol,
            volume=vol,
            price=order_price,
            sl=stop_loss,
            tp=take_profit,
            type=order_type,
        )
        print(f"{symbol} order sent with lot size {vol} at {round(order_price, 5)}")
        if not order_result:
            print("Order could not be placed")
            sys.exit(1)

        order_place_dict = order_result._asdict()
        request_dict = order_place_dict["request"]._asdict()
        req_vals = [request_dict[key] for key in request_dict]
        sql_values = [order_place_dict[key] for key in order_place_dict][:3] + req_vals + [trade_reason]
        journal.insert_into(sql_values)

    def get_lot_size(self, trade_type, symbol, sl_points, risk_perc, rr):

        account_size = mt5.account_info().balance
        order_price = self.set_order_price(trade_type, symbol)
        risk_amount = account_size * (risk_perc / 100)
        pips_risked = sl_points / 10
        amount_per_pip = risk_amount / pips_risked
        acc_std_pip_val = self.get_pip_value(trade_type, symbol, order_price)
        lots = round(amount_per_pip / acc_std_pip_val, 2)

        return lots

    @staticmethod
    def close_all_orders():
        orders = {}
        order_results = []
        for position in mt5.positions_get():
            if position.type == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                order_price = mt5.symbol_info_tick(position.symbol).bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                order_price = mt5.symbol_info_tick(position.symbol).ask

            result = mt5.order_send(
                action=mt5.TRADE_ACTION_DEAL,
                symbol=position.symbol,
                volume=position.volume,
                position=position.ticket,
                type=order_type,
                price=order_price,
            )
            order_results.append(result._asdict())
            orders[position.ticket] = position.symbol

        print(f"Successfully closed the following position(s): ")
        for i in orders:
            print(f"{i} : {orders[i]}")

    @staticmethod
    def close_orders_for_symbol(symbol):
        tickets = []
        for position in mt5.positions_get(symbol=symbol):

            if position.type == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                order_price = mt5.symbol_info_tick(position.symbol).bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                order_price = mt5.symbol_info_tick(position.symbol).ask

            mt5.order_send(
                action=mt5.TRADE_ACTION_DEAL,
                symbol=position.symbol,
                volume=position.volume,
                position=position.ticket,
                type=order_type,
                price=order_price,
            )

            tickets.append(position.ticket)

        print(f"Successfully closed position(s) {tickets} on {symbol}")

    def symbol_rates_df(self, symbol, time_frame, bars_count, start_pos=0):

        mt5_time_frame = self.get_mt5_time_frame(time_frame)

        bars = mt5.copy_rates_from_pos(symbol, mt5_time_frame, start_pos, bars_count)
        columns = ["time", "open", "high", "low", "close"]

        df = pd.DataFrame(bars, columns=columns)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", drop=True, inplace=True)
        df.sort_values(by="time", ascending=False)

        return df
