# SESSION 25: Case Study - Binance Crypto Price Tracker (Part 2)

## Overview
This session advances our Cryptocurrency Analytics platform using the official **Binance 24hr Ticker API**. It includes data ingestion into JSON, algorithmic market analytics (volatility identification, market-average benchmarking, volume ranking), rate-limit resilience with exponential backoff, and automated background hourly scheduling.

---

## Tasks Implemented

### Task 1: Fetch 24-Hour Price & Volume via Binance API
- Endpoint: `https://api.binance.com/api/v3/ticker/24hr`
- Ingests latest 24hr statistics for 10 top trading pairs (`BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`, `DOGEUSDT`, `AVAXUSDT`, `DOTUSDT`, `MATICUSDT`).
- Saves the full raw structured response directly to `crypto_data.json`.

### Task 2: `find_most_volatile_coin(data)`
- Parses the coin records and computes the coin with the highest percentage price change over the last 24 hours based on `|priceChangePercent|`.

### Task 3: Below-Average Price Scanner
- Computes the aggregate arithmetic average price across all tracked coins.
- Filters and displays every cryptocurrency currently trading below this benchmark with percentage deviation.

### Task 4: `rank_coins_by_volume(data)`
- Sorts coins by total traded volume (`quoteVolume` in USDT) in descending order.
- Outputs an ASCII leaderboard of the top 5 most traded assets.

### Task 5: Hourly Automation & Rate Limit Resilience
- **Automated Scheduling**: Employs the `schedule` library in `scheduler_hourly.py` configured for `schedule.every(1).hours.do(job)`.
- **Rate Limit & Error Handling**: Intercepts HTTP 429 status codes, reads `Retry-After` response headers, and implements exponential backoff retry cycles.

---

## Files
- `crypto_tracker_part2.py` - Core engine solving Tasks 1, 2, 3, 4, and retry/rate-limit logic.
- `scheduler_hourly.py` - Task 5 hourly daemon runner.
- `crypto_data.json` - Serialized JSON response containing live market data from Binance.
