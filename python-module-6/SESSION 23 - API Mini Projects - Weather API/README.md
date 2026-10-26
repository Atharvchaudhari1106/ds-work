# SESSION 23: API Mini Projects

> **Concepts Covered:** Practical API Integrations • OpenWeatherMap • CoinGecko Crypto Market Rates • NASA APOD Image Streaming • Global Health Statistics (COVID-19) • Multi-API Aggregation & Graceful Fallback Strategies

---

## 📖 Project Highlights

### 1. Handling Real-World Public APIs
- **OpenWeatherMap**: Standard for meteorological data. Requires API keys, query parameter structuring (`q=City`, `units=metric`), and error handling for unauthenticated requests (`401 Unauthorized`).
- **CoinGecko**: Premier open cryptocurrency pricing API. Demonstrates currency conversions (`usd`, `inr`) and 24-hour rate fluctuation calculations without mandatory API key overhead.
- **NASA APOD**: Demonstrates media streaming using `requests.get(url, stream=True)` and chunked binary writes (`iter_content()`) to save high-resolution space photography locally.
- **Disease.sh (COVID-19)**: Ingests global public health datasets and reformats complex numerical structures into readable ASCII tables.
- **Multi-API Dashboard**: Connects multiple external services in a single workflow, using defensive programming so failure of one API does not crash the overall application.

---

## 📝 Tasks & Solutions Summary

| File | Task Summary | Concepts Demonstrated |
| :--- | :--- | :--- |
| [`task1_weather_api.py`](task1_weather_api.py) | Fetch temperature & weather description for city via OpenWeatherMap | Query params (`q`, `units=metric`), extracting `temp` and `description` |
| [`task2_crypto_prices_coingecko.py`](task2_crypto_prices_coingecko.py) | Fetch Bitcoin & Ethereum live prices with timestamps from CoinGecko | Financial data parsing, multi-currency values (`USD`, `INR`), timestamps |
| [`task3_nasa_apod_downloader.py`](task3_nasa_apod_downloader.py) | Fetch NASA APOD title & explanation, download image locally | Binary streaming with `requests.get(..., stream=True)`, file I/O |
| [`task4_covid_statistics_india.py`](task4_covid_statistics_india.py) | Fetch COVID-19 statistics for India and display in tabular format | Health data ingestion, numerical formatting (`{:,}`), ASCII tables |
| [`task5_multi_api_dashboard.py`](task5_multi_api_dashboard.py) | Combine Mumbai weather and Bitcoin price into a unified dashboard | Multi-API aggregation, graceful fallback handling, robust architecture |

---

## 📸 Downloaded Artifacts

- [`nasa_apod.jpg`](nasa_apod.jpg): High-resolution NASA Astronomy Picture of the Day saved directly by Task 3.

---

## 🚀 How to Run

```bash
# Task 1: City weather reporter
python task1_weather_api.py

# Task 2: Live Bitcoin & Ethereum tracker
python task2_crypto_prices_coingecko.py

# Task 3: NASA APOD image downloader
python task3_nasa_apod_downloader.py

# Task 4: COVID-19 India statistics table
python task4_covid_statistics_india.py

# Task 5: Multi-API combined dashboard
python task5_multi_api_dashboard.py
```
