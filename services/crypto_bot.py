# services/crypto_bot.py
import requests

class CryptoBot:
    def get_price(self, currency: str):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data.get(currency, {}).get("usd", "Price not available")