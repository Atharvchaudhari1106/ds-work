import json
import time
import requests

BINANCE_24HR_URL = "https://api.binance.com/api/v3/ticker/24hr"

# List of 10 popular cryptocurrency pairs quoted against USDT
TARGET_SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "DOTUSDT",
    "MATICUSDT"
]

def fetch_binance_24hr_data(symbols=TARGET_SYMBOLS, save_file="crypto_data.json", max_retries=3):
    """
    Task 1 & Task 5:
    Fetches latest 24-hour price and volume data for at least 10 popular crypto pairs
    using the Binance API and saves raw response to crypto_data.json.
    Includes exponential backoff for HTTP 429 rate limit errors and network exceptions.
    """
    headers = {"User-Agent": "CryptoTracker/1.0"}
    backoff = 1  # starting backoff in seconds

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[FETCH] Requesting 24hr ticker data from Binance API (Attempt {attempt}/{max_retries})...")
            response = requests.get(BINANCE_24HR_URL, headers=headers, timeout=10)

            # Task 5: Check for rate limits (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", backoff))
                print(f"[RATE LIMIT] Binance rate limit encountered (HTTP 429). Backing off for {retry_after}s...")
                time.sleep(retry_after)
                backoff *= 2
                continue

            response.raise_for_status()
            all_tickers = response.json()

            # Filter for our selected target popular cryptocurrencies
            filtered_data = [ticker for ticker in all_tickers if ticker.get("symbol") in symbols]

            # Save raw JSON response to file
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(filtered_data, f, indent=4)

            print(f"[SUCCESS] Saved {len(filtered_data)} coins 24hr data to '{save_file}'.")
            return filtered_data

        except requests.exceptions.RequestException as err:
            print(f"[NETWORK ERROR] Request failed on attempt {attempt}: {err}")
            if attempt < max_retries:
                print(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                print("[ERROR] Max retries reached. Using local cache/fallback data if available.")
                return load_crypto_data(save_file)

    return []

def load_crypto_data(filename="crypto_data.json"):
    """Loads cryptocurrency data from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] Could not load data from {filename}: {e}")
        return []

def find_most_volatile_coin(data):
    """
    Task 2:
    Takes the loaded Binance coin data and returns the symbol of the coin
    with the highest percentage price change in the last 24 hours.
    (Volatility measured by absolute percentage price change: |priceChangePercent|)
    """
    if not data:
        return None

    # Compare by absolute percentage price change over 24h
    most_volatile = max(
        data,
        key=lambda coin: abs(float(coin.get("priceChangePercent", 0.0)))
    )
    return most_volatile.get("symbol")

def analyze_prices_below_average(data):
    """
    Task 3:
    Calculates the average price of all coins in crypto_data.json,
    then prints a list of all coins currently trading below this average price.
    """
    if not data:
        print("[ANALYSIS] No coin data available to compute average price.")
        return

    prices = [float(coin.get("lastPrice", 0.0)) for coin in data]
    avg_price = sum(prices) / len(prices)

    print("\n" + "=" * 60)
    print(f"AVERAGE PRICE ANALYSIS (Across {len(data)} coins)")
    print(f"Average Price: ${avg_price:,.4f}")
    print("=" * 60)
    print(f"{'Symbol':<15} {'Last Price ($)':<18} {'Status'}")
    print("-" * 60)

    below_avg_coins = []
    for coin in data:
        price = float(coin.get("lastPrice", 0.0))
        if price < avg_price:
            below_avg_coins.append(coin)
            diff_pct = ((avg_price - price) / avg_price) * 100
            print(f"{coin.get('symbol'):<15} ${price:<17,.4f} Below avg by {diff_pct:.1f}%")

    print("=" * 60)
    print(f"Total coins trading below average: {len(below_avg_coins)}/{len(data)}")
    return avg_price, below_avg_coins

def rank_coins_by_volume(data):
    """
    Task 4:
    Sorts all coins by their total traded volume (quoteVolume in USDT) in descending order
    and prints the top 5 coins with their rank and volume.
    """
    if not data:
        print("[RANKING] No coin data available to rank by volume.")
        return

    # Sort coins by quoteVolume (USDT volume) descending
    sorted_coins = sorted(
        data,
        key=lambda coin: float(coin.get("quoteVolume", 0.0)),
        reverse=True
    )

    print("\n" + "=" * 65)
    print("TOP 5 COINS RANKED BY 24-HOUR TRADED VOLUME (USDT)")
    print("=" * 65)
    print(f"{'Rank':<6} {'Symbol':<12} {'24h Volume (USDT)':<22} {'Last Price ($)'}")
    print("-" * 65)

    top_5 = sorted_coins[:5]
    for rank, coin in enumerate(top_5, 1):
        volume = float(coin.get("quoteVolume", 0.0))
        price = float(coin.get("lastPrice", 0.0))
        print(f"{rank:<6} {coin.get('symbol'):<12} ${volume:<21,.2f} ${price:,.4f}")
    print("=" * 65)

    return top_5

def run_pipeline():
    """Executes the full pipeline: Fetch -> Analyze Volatility -> Average Price -> Volume Ranking."""
    print("\n" + "#" * 65)
    print("[RUNNING] BINANCE CRYPTO TRACKER PIPELINE")
    print("#" * 65)

    # 1. Fetch & save data
    data = fetch_binance_24hr_data()
    if not data:
        print("[ERROR] No data fetched or loaded.")
        return

    # 2. Find most volatile coin
    volatile_sym = find_most_volatile_coin(data)
    coin_dict = next((c for c in data if c.get("symbol") == volatile_sym), None)
    if coin_dict:
        chg = float(coin_dict.get("priceChangePercent", 0.0))
        print(f"\n[VOLATILITY] Most Volatile Coin: {volatile_sym} ({chg:+.2f}% change in 24h)")

    # 3. Coins below average price
    analyze_prices_below_average(data)

    # 4. Top 5 coins ranked by volume
    rank_coins_by_volume(data)

if __name__ == "__main__":
    run_pipeline()
