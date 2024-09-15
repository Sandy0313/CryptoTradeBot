import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")  # Not used in this snippet, but it might be useful in future implementations.
EXCHANGE_API_URL = os.getenv("BASE_URL", "https://api.exchange.com")

class TradeOrder:
    def __init__(self, asset_pair, order_type, quantity):
        self.asset_pair = asset_pair
        self.order_type = order_type
        self.quantity = quantity

def submit_order(order):
    order_api_endpoint = f"{EXCHANGE_API_URL}/order"
    order_data = {
        "symbol": order.asset_pair,
        "side": order.order_type,  # 'side' represents if it's a buy or sell order
        "type": "market",  # This example uses a market order type; consider implementing other types like 'limit'
        "quantity": order.quantity,
    }
    api_headers = {"X-API-KEY": API_KEY}
    
    try:
        order_response = requests.post(order_api_endpoint, json=order_data, headers=api_headers)
        order_response.raise_for_status()  # Raises an error for 4XX or 5XX status codes
        return order_response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Order submission error: {e}")
        return None

def fetch_account_balance():
    balance_api_endpoint = f"{EXCHANGE_API_URL}/balance"
    api_headers = {"X-API-KEY": API_KEY}
    
    try:
        balance_response = requests.get(balance_api_endpoint, headers=api_headers)
        balance_response.raise_for_status()
        return balance_response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Balance retrieval error: {e}")
        return None

def trading_logic():
    account_balance = fetch_account_balance()
    # Ensure account balance is successfully retrieved and USD balance exceeds 1000.
    if account_balance and account_balance.get('USD', 0) > 1000:
        btc_trade_order = TradeOrder("BTCUSD", "buy", 0.01)  # Example: buying 0.01 BTC with USD
        trade_order_response = submit_order(btc_trade_order)
        if trade_order_response:
            print("Trade order successfully executed:", trade_order_response)
        else:
            print("Failed to execute trade order.")
    else:
        print("Insufficient funds or unable to fetch account balance.")

if __name__ == "__main__":
    trading_logic()