import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.exchange.com")

class Trade:
    def __init__(self, symbol, trade_type, amount):
        self.symbol = symbol
        self.trade_type = trade_type
        self.amount = amount

def place_order(trade):
    endpoint = f"{BASE_URL}/order"
    payload = {
        "symbol": trade.symbol,
        "side": trade.trade_type,
        "type": "market",
        "quantity": trade.amount,
    }
    headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def check_balance():
    endpoint = f"{BASE_URL}/balance"
    headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def trade_logic():
    balance_info = check_balance()
    if balance_info and balance_info.get('USD', 0) > 1000:
        trade = Trade("BTCUSD", "buy", 0.01)
        place_order(trade)

if __name__ == "__main__":
    trade_logic()