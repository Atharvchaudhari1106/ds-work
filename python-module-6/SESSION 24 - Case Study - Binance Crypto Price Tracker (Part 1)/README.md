# SESSION 24: Case Study - Binance Crypto Price Tracker (Part 1)

## Overview
This session implements the first part of a Cryptocurrency Price Tracker case study using REST APIs (`requests` library), parsing responses, computing key market statistics, exporting structured results to CSV, and handling errors cleanly.

---

## Tasks Implemented

### Task 1: Fetch Top 10 Cryptocurrencies
- Hits CoinGecko API `https://api.coingecko.com/api/v3/coins/markets`
- Query parameters: `vs_currency=usd`, `order=market_cap_desc`, `per_page=10`, `page=1`
- Prints coin name and price for each coin.

### Task 2: 24-Hour Price Statistics
- Extends the display to present:
  - 24-Hour Price Change %
  - 24-Hour High Price ($)
  - 24-Hour Low Price ($)

### Task 3: Save Data to CSV
- Exports all fetched coin records (`Name`, `Current Price ($)`, `24h Change (%)`, `24h High ($)`, `24h Low ($)`) into `crypto_prices.csv` using Python's standard `csv.DictWriter`.

### Task 4: Robust Error Handling
- Checks HTTP status code (handling rate limits like `429 Too Many Requests`).
- Employs `try-except` blocks catching `requests.exceptions.RequestException` to ensure scripts never crash unexpectedly.

---

## Files
- `crypto_tracker_part1.py` - Complete executable solution covering Tasks 1 to 4.
- `crypto_prices.csv` - Generated CSV export of the top 10 cryptocurrencies.
