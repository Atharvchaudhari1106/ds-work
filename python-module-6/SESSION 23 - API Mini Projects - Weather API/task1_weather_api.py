"""
Task 1: OpenWeatherMap Weather & Temperature Reporter
Fetch the current temperature and weather description for your city
using the OpenWeatherMap API and print the results in a readable format.
"""

import os
import requests


def get_city_weather(city_name="Ahmedabad", api_key=None):
    # Retrieve key from parameter or environment variable
    if not api_key:
        api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key_or_replace_with_yours")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Metric units return temperature in Celsius
    }

    print("=" * 65)
    print(f"Task 1: Current Weather Report for {city_name}")
    print("=" * 65)
    print(f"Target API Endpoint : {url}")
    print(f"Target City         : {city_name}")
    print("=" * 65)

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"\nAPI Response Status Code : {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            weather_desc = data["weather"][0]["description"].capitalize()
            wind_speed = data.get("wind", {}).get("speed", "N/A")

            print("\n" + "=" * 65)
            print(f"WEATHER REPORT: {city_name.upper()} (LIVE DATA)")
            print("=" * 65)
            print(f"  * Current Temperature : {temp} deg C")
            print(f"  * Feels Like          : {feels_like} deg C")
            print(f"  * Weather Condition   : {weather_desc}")
            print(f"  * Relative Humidity   : {humidity}%")
            print(f"  * Atmospheric Pressure: {pressure} hPa")
            print(f"  * Wind Speed          : {wind_speed} m/s")
            print("=" * 65)
            return data

        elif response.status_code == 401:
            print("\n[NOTE] OpenWeatherMap returned HTTP 401 (Invalid/Missing API Key).")
            print("[INFO] OpenWeatherMap requires a personal free API key from:")
            print("       https://home.openweathermap.org/users/sign_up")
            print("       You can supply it via: export OPENWEATHER_API_KEY='your_key'")
            print("\n[DEMO] Demonstrating clean parsing with simulated response for your city:")
            simulated = {
                "name": city_name,
                "main": {"temp": 31.8, "feels_like": 34.5, "humidity": 65, "pressure": 1012},
                "weather": [{"description": "scattered clouds"}],
                "wind": {"speed": 3.6}
            }
            print("-" * 65)
            print(f"  * City        : {simulated['name']}")
            print(f"  * Temperature : {simulated['main']['temp']} deg C")
            print(f"  * Description : {simulated['weather'][0]['description'].capitalize()}")
            print(f"  * Humidity    : {simulated['main']['humidity']}%")
            print("-" * 65)
            return simulated

        else:
            print(f"[ERROR] API call failed with status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error occurred: {e}")


if __name__ == "__main__":
    get_city_weather("Ahmedabad")
