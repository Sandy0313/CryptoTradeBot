import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.exchange.com")

class TradeOrder:
    def __init__(self, asset_pair, buy_or_sell, quantity):
        self.asset_pair = asset_pair
        self.buy_or_sell = buy_or_sell
        self.quantity = quantity

def submit_trade_order(trade_order):
    order_endpoint = f"{BASE_URL}/order"
    order_payload = {
        "symbol": trade_order.asset_pair,
        "side": trade_order.buy_or_sell,
        "type": "market",
        "quantity": trade_order.quantity,
    }
    order_headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.post(order_endpoint, json=order_payload, headers=order_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

def retrieve_account_balance():
    balance_endpoint = f"{BASE_URL}/balance"
    balance_headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.get(balance_endpoint, headers=balance_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

def exchange_logic():
    current_balance = retrieve_account_balance()
    if current_balance and current_balance.get('USD', 0) > 1000:
        new_trade_order = TradeOrder("BTCUSD", "buy", 0.01)
        submit_trade_order(new_trade_order)

if __name__ == "__main__":
    exchange_logic()