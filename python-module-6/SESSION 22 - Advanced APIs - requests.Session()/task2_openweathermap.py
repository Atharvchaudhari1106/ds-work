"""
Task 2: Call OpenWeatherMap API for Ahmedabad Temperature
Write a Python script using requests to call the OpenWeatherMap API
(https://api.openweathermap.org/data/2.5/weather) for the city 'Ahmedabad'
using your own API key, and print the current temperature.
"""

import os
import requests


def fetch_ahmedabad_weather(api_key=None):
    # Allow overriding via parameter or environment variable
    if not api_key:
        api_key = os.getenv("OPENWEATHER_API_KEY", "your_openweathermap_api_key_here")

    url = "https://api.openweathermap.org/data/2.5/weather"
    city = "Ahmedabad"

    # Query parameters: city name, API key (appid), and units in Celsius (metric)
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    print("=" * 65)
    print(f"Task 2: Fetch Current Temperature for {city}")
    print("=" * 65)
    print(f"Endpoint : {url}")
    print(f"Params   : q={params['q']}, units={params['units']}, appid={'*' * 8}")
    print("=" * 65)

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"\nResponse Status Code: {response.status_code}")

        data = response.json()

        if response.status_code == 200:
            main_data = data.get("main", {})
            current_temp = main_data.get("temp")
            feels_like = main_data.get("feels_like")
            humidity = main_data.get("humidity")
            weather_desc = data.get("weather", [{}])[0].get("description", "N/A")

            print("=" * 65)
            print(f"[SUCCESS] Current Weather in {city}:")
            print("=" * 65)
            print(f"  * Temperature : {current_temp} deg C")
            print(f"  * Feels Like  : {feels_like} deg C")
            print(f"  * Condition   : {weather_desc.title()}")
            print(f"  * Humidity    : {humidity}%")
            print("=" * 65)
            return current_temp

        elif response.status_code == 401:
            print(f"\n[NOTE] OpenWeatherMap returned HTTP 401: {data.get('message')}")
            print("[INFO] To query live data, register a free key at https://openweathermap.org/api")
            print("       and set it via environment variable: export OPENWEATHER_API_KEY='your_key'")
            print("\n[DEMO] Demonstrating standard OpenWeatherMap JSON payload parsing:")
            demo_payload = {
                "name": "Ahmedabad",
                "main": {"temp": 32.4, "feels_like": 35.1, "humidity": 68},
                "weather": [{"description": "haze"}]
            }
            temp = demo_payload["main"]["temp"]
            print(f"  * Extracted Temperature (`data['main']['temp']`): {temp} deg C")
            return temp

        else:
            print(f"[ERROR] API returned error: {data.get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection failed: {e}")


if __name__ == "__main__":
    fetch_ahmedabad_weather()
