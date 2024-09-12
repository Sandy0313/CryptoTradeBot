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
        response.raise_for_status()  # Raises error for 4XX or 5XX status codes
        return response.json()
        
    except requests.exceptions.RequestException as e:  # This method catches all requests related exceptions
        print(f"Request error: {e}")
        return None

def retrieve_account_balance():
    balance_endpoint = f"{BASE_URL}/balance"
    balance_headers = {"X-API-KEY": API_KEY}
    
    try:
        response = requests.get(balance_endpoint, headers=balance_headers)
        response.raise_for_status()  # Raises error for 4XX or 5XX status codes
        return response.json()
        
    except requests.exceptions.RequestException as e:  # This method catches all requests related exceptions
        print(f"Request error: {e}")
        return None

def exchange_logic():
    current_balance = retrieve_account_balance()
    # Ensure the balance is retrieved successfully and USD balance is more than 1000.
    if current_balance and current_balance.get('USD', 0) > 1000:
        new_trade_order = TradeOrder("BTCUSD", "buy", 0.01)
        trade_response = submit_trade_order(new_trade_order)
        if trade_response:
            print("Trade order submitted successfully:", trade_response)
        else:
            print("Failed to submit trade order.")
    else:
        print("Insufficient balance or failed to retrieve balance.")

if __name__ == "__main__":
    exchange_logic()