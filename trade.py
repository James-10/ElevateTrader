from utils.indicators import Indicators
from utils.mt5_utils import UtilsMT5
from utils.strategies import Strategies
from journaling.journal import TradeJournal
import MetaTrader5 as mt5
from datetime import datetime as dt

environment = 'mt5_exe'
i_mt5 = Indicators()
utils = UtilsMT5()
strat_obj = Strategies()
journal = TradeJournal()

utils.mt5_init(environment)
print(utils.close_all_orders())

# now = dt.now()
# start_date = journal.get_last_hist_run()
print(utils.get_lot_size(trade_type='BUY', symbol='EURUSD', sl_points=320, rr=4, risk_perc=2))
# utils.place_order(trade_type='BUY', symbol='EURUSD', sl_points=145, trade_reason='wave5', rr=3, risk_perc=2)
# trade_hist = mt5.history_deals_get(start_date, now)
# journal.update_ledger(trade_hist)





