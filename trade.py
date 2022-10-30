from utils.indicators import Indicators
from utils.mt5_utils import UtilsMT5
from utils import Strategies

environment = 'mt5_exe'
i_mt5 = Indicators()
utils = UtilsMT5()
strat_obj = Strategies()

utils.mt5_init(environment)
# print(utils.close_all_orders())

# print(utils.get_lot_size(trade_type='BUY', symbol='EURUSD', sl_points=320, rr=4, risk_perc=2))

# Initialize test_strat bot
strat_obj.test_strat(
    symbol='EURUSD',
    time_frame=15,
    period=14,
    sl_points=300
)



