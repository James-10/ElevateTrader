import requests
from enum import Enum
from typing import List, Dict

from config import Config

SYMBOLS_CACHE = {}

class SymbolsEnum(Enum):

    #Majors
    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    AUDUSD = "AUDUSD"
    NZDUSD = "NZDUSD"
    USDCAD = "USDCAD"
    USDCHF = "USDCHF"
    USDJPY = "USDJPY"

    #Exotic
    USDZAR = "USDZAR"   

    #Commodities
    XAUUSD = "XAUUSD"
    XAGUSD = "XAGUSD"
    USOIL = "USOIL"
    UKOIL = "UKOIL"

    #Cryptos
    BTCUSD = "BTCUSD"
    ETHUSD = "ETHUSD"
    LTCUSD = "LTCUSD"
    XRPUSD = "XRPUSD"


class OrderTypesEnum(Enum):
    "Distinct order types"
    buy = "buy"
    sell = "sell"