"""
Task 2: Crypto Price Tracker using CoinGecko API
Build a small Python script that fetches the latest price of Bitcoin and Ethereum
from the CoinGecko API and displays them with the current date and time.
"""

from datetime import datetime
import requests


def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd,inr",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    headers = {
        "Accept": "application/json",
        "User-Agent": "CryptoTrackerMiniProject/1.0"
    }

    print("=" * 65)
    print("Task 2: Real-Time Cryptocurrency Prices (CoinGecko API)")
    print("=" * 65)
    print(f"Endpoint : {url}")
    print("Querying : Bitcoin (BTC), Ethereum (ETH) in USD and INR")
    print("=" * 65)

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nResponse Status Code : {response.status_code}")
        print(f"Timestamp of Fetch   : {current_time}\n")

        if response.status_code == 200:
            data = response.json()
            btc = data.get("bitcoin", {})
            eth = data.get("ethereum", {})

            print("=" * 65)
            print(f"LIVE CRYPTO MARKET OVERVIEW [{current_time}]")
            print("=" * 65)
            print(f"{'Asset':<15} | {'Price (USD)':<15} | {'Price (INR)':<15} | {'24h Change':<10}")
            print("-" * 65)

            btc_usd = f"${btc.get('usd', 0):,}"
            btc_inr = f"Rs. {btc.get('inr', 0):,}"
            btc_chg = f"{btc.get('usd_24h_change', 0):+.2f}%"
            print(f"{'Bitcoin (BTC)':<15} | {btc_usd:<15} | {btc_inr:<15} | {btc_chg:<10}")

            eth_usd = f"${eth.get('usd', 0):,}"
            eth_inr = f"Rs. {eth.get('inr', 0):,}"
            eth_chg = f"{eth.get('usd_24h_change', 0):+.2f}%"
            print(f"{'Ethereum (ETH)':<15} | {eth_usd:<15} | {eth_inr:<15} | {eth_chg:<10}")
            print("=" * 65)
            print("[SUCCESS] Live prices fetched from CoinGecko successfully!")

            return data

        elif response.status_code == 429:
            print("[WARNING] CoinGecko rate limit exceeded (HTTP 429). Please wait a moment.")
        else:
            print(f"[ERROR] Failed to fetch prices. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")


if __name__ == "__main__":
    fetch_crypto_prices()
