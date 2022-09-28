from bin.Utils import UtilsMT5
from bin.Indicators import PriceUtils
import MetaTrader5 as mt5
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

environment = 'vault_markets_prod'

utils = UtilsMT5(environment)

print(mt5.account_info().balance)



