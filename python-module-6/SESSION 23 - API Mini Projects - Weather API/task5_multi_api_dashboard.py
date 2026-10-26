"""
Task 5: Multi-API Aggregator (Weather + Cryptocurrency)
Combine data from two APIs: fetch the current temperature in Mumbai from OpenWeatherMap
and the latest Bitcoin price from CoinGecko, then display both results together in a single output.

Constraint: Handle errors gracefully if either API call fails and show an appropriate message.
"""

from datetime import datetime
import os
import requests


def fetch_mumbai_weather():
    """Fetches Mumbai temperature from OpenWeatherMap with graceful error handling."""
    api_key = os.getenv("OPENWEATHER_API_KEY", "demo_or_unregistered_key")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "Mumbai", "appid": api_key, "units": "metric"}

    result = {
        "status": "error",
        "city": "Mumbai",
        "temp": None,
        "desc": None,
        "message": ""
    }

    try:
        response = requests.get(url, params=params, timeout=8)

        if response.status_code == 200:
            data = response.json()
            result["status"] = "success"
            result["temp"] = data["main"]["temp"]
            result["desc"] = data["weather"][0]["description"].title()
            result["message"] = "Live data from OpenWeatherMap"
        elif response.status_code == 401:
            result["status"] = "fallback"
            result["temp"] = 30.5  # Typical Mumbai seasonal temperature
            result["desc"] = "Warm & Humid (Simulated)"
            result["message"] = "API key missing/invalid. Displaying estimated seasonal baseline."
        else:
            result["message"] = f"OpenWeatherMap returned HTTP {response.status_code}"

    except requests.exceptions.RequestException as e:
        result["message"] = f"Weather network error: {e}"

    return result


def fetch_bitcoin_price():
    """Fetches Bitcoin price from CoinGecko with graceful error handling."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd,inr"}
    headers = {"User-Agent": "MultiAPIDashboard/1.0"}

    result = {
        "status": "error",
        "usd": None,
        "inr": None,
        "message": ""
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=8)

        if response.status_code == 200:
            data = response.json()
            btc = data.get("bitcoin", {})
            result["status"] = "success"
            result["usd"] = btc.get("usd")
            result["inr"] = btc.get("inr")
            result["message"] = "Live data from CoinGecko API"
        elif response.status_code == 429:
            result["message"] = "CoinGecko rate limit reached (HTTP 429). Try again shortly."
        else:
            result["message"] = f"CoinGecko returned HTTP {response.status_code}"

    except requests.exceptions.RequestException as e:
        result["message"] = f"CoinGecko network error: {e}"

    return result


def display_dashboard():
    print("=" * 70)
    print("Task 5: Unified Multi-API Dashboard (Weather & Crypto)")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("[1/2] Fetching Mumbai weather from OpenWeatherMap...")
    weather = fetch_mumbai_weather()

    print("[2/2] Fetching latest Bitcoin price from CoinGecko...")
    crypto = fetch_bitcoin_price()

    print("\n" + "=" * 70)
    print("                      COMBINED DATA FEED                       ")
    print("=" * 70)

    # Display Weather Section
    print("A. MUMBAI WEATHER:")
    if weather["status"] in ("success", "fallback"):
        status_tag = "[LIVE]" if weather["status"] == "success" else "[ESTIMATED]"
        print(f"   {status_tag} Temperature : {weather['temp']} deg C")
        print(f"   {status_tag} Condition   : {weather['desc']}")
        print(f"   Note         : {weather['message']}")
    else:
        print(f"   [ERROR] Failed to fetch weather: {weather['message']}")

    print("-" * 70)

    # Display Crypto Section
    print("B. BITCOIN (BTC) MARKET VALUE:")
    if crypto["status"] == "success":
        print(f"   [LIVE] USD Price : ${crypto['usd']:,}")
        print(f"   [LIVE] INR Price : Rs. {crypto['inr']:,}")
        print(f"   Note             : {crypto['message']}")
    else:
        print(f"   [ERROR] Failed to fetch Bitcoin price: {crypto['message']}")

    print("=" * 70)
    print("[SUCCESS] Both API endpoints evaluated with graceful error handling.")


if __name__ == "__main__":
    display_dashboard()
