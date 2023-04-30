import requests
from enum import Enum
from typing import List, Dict

symbols_endpoint = "https://api.twelvedata.com/forex_pairs"
api_key = ""

data = {}

response = requests.get(
    url=symbols_endpoint,
    data=data,
    headers={f"Authorization={api_key}"}
)

symbol_data : List[Dict] = response.json()


class SymbolsEnum(Enum):
    
    for sym_dict in symbol_data:
        locals()[sym_dict.get("symbol")] = sym_dict.get("symbol")


class OrderTypesEnum(Enum):
    "Distinct order types"
    buy = "buy"
    sell = "sell"


class AlgosEnum(Enum):
    mean_reversion = "mean_reversion"
    trending = "trending"
    high_frequency= "high_frequency"