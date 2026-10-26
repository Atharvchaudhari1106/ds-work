# Section D — AI-Augmented Learning

**Assessment Code**: M2-A1  
**Program**: Data Science | Python for Data Science  

---

## 1. Exact Prompt Provided to the AI Tool

```text
Write a standalone Python program for a Food Delivery platform that:
1. Fetches the first 5 records from https://jsonplaceholder.typicode.com/posts?_limit=5 (treating them as mock restaurants) and prints each record's id and title.
2. Applies a tiered commission — 10% for orders up to Rs 200, 15% for Rs 201–Rs 500, and 20% above Rs 500 — to a hardcoded list of 6 order amounts [150.0, 200.0, 320.0, 500.0, 650.0, 1200.0] using map() and a lambda, and prints each original value alongside its calculated result.
3. Handles an API failure (any status code other than 200) by printing a descriptive error message and stopping execution — without raising an unhandled exception that crashes the script.
4. Saves the 5 fetched records to a file called data/processed/records.json using json.dump() inside a with open() context manager, with an indent of 2 for readability.
```

---

## 2. Code Comparison: AI's Original Code vs. Corrected Version

### A. The AI's Original Code (with Flaws & Bugs)

```python
import json
import requests

# 1. API Fetch
url = "https://jsonplaceholder.typicode.com/posts?_limit=5"
response = requests.get(url)

# BUG 1: Calls .json() BEFORE checking status_code; crashes on HTML error pages
data = response.json()

if response.status_code != 200:
    print(f"Error fetching data: {response.status_code}")
    exit()

print("Fetched Restaurants:")
for item in data:
    print(f"ID: {item['id']}, Title: {item['title']}")

# 2. Tiered Commission Calculation
order_amounts = [150.0, 200.0, 320.0, 500.0, 650.0, 1200.0]

# BUG 2: Uses integer division (//) discarding fractional currency paise/cents
commissions = list(map(
    lambda amt: amt * 10 // 100 if amt <= 200 else (amt * 15 // 100 if amt <= 500 else amt * 20 // 100),
    order_amounts
))

print("\nCommission Calculations:")
for amt, comm in zip(order_amounts, commissions):
    print(f"Order: Rs {amt} -> Commission: Rs {comm}")

# 3. Persistence
# BUG 3: Does not check or create parent directory; crashes if data/processed/ is missing
# BUG 4: Missing indent parameter in json.dump(), producing minified unreadable output
with open("data/processed/records.json", "w") as f:
    json.dump(data, f)

print("\nSaved records to data/processed/records.json")
```

---

### B. Corrected Production-Ready Version (`section_d_corrected.py`)

```python
"""
Section D: AI-Augmented Learning — Corrected Script
Fixes status code pre-check, float arithmetic precision, directory creation,
and formatted JSON persistence with indent=2.
"""

import os
import sys
import json
import requests

def main():
    print("=" * 72)
    print("       FOOD DELIVERY PLATFORM - AI-AUGMENTED PIPELINE (CORRECTED)")
    print("=" * 72)

    # 1. Safe API Ingestion
    url = "https://jsonplaceholder.typicode.com/posts?_limit=5"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        print(f"[API ERROR] Network connection error occurred: {exc}")
        print("[NOTICE] Halting execution safely without unhandled crash.")
        sys.exit(0)

    # FIX 1: Verify HTTP status code BEFORE attempting response.json()
    if response.status_code != 200:
        print(f"[API ERROR] Received non-success HTTP status code: {response.status_code}")
        print("[NOTICE] Aborting pipeline gracefully without crashing.")
        sys.exit(0)

    try:
        data = response.json()
    except ValueError as val_err:
        print(f"[PARSE ERROR] Failed to parse JSON response payload: {val_err}")
        sys.exit(0)

    print("\n--- Fetched Mock Restaurants ---")
    for item in data:
        print(f"  * Restaurant ID: #{item['id']:<2} | Name: {item['title'][:40].strip().title()}")

    # 2. Tiered Commission Calculation with True Floating-Point Math
    order_amounts = [150.0, 200.0, 320.0, 500.0, 650.0, 1200.0]

    # FIX 2: Replaced integer division (//) with float multiplication (/ 100.0)
    commissions = list(map(
        lambda amt: round(amt * 0.10, 2) if amt <= 200.0
        else (round(amt * 0.15, 2) if amt <= 500.0
              else round(amt * 0.20, 2)),
        order_amounts
    ))

    print("\n--- Commission Payout Calculations ---")
    print(f"{'Order Amount':<16} | {'Tier Rate':<12} | {'Commission Payout':<18}")
    print("-" * 52)
    for amt, comm in zip(order_amounts, commissions):
        rate = "10%" if amt <= 200 else ("15%" if amt <= 500 else "20%")
        print(f"Rs. {amt:>8.2f}        | {rate:<12} | Rs. {comm:>8.2f}")
    print("-" * 52)

    # 3. Resilient File Persistence
    target_path = os.path.join("data", "processed", "records.json")

    # FIX 3: Automatically ensure parent directory structure exists
    parent_dir = os.path.dirname(target_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # FIX 4: Explicit indent=2 parameter as specified in assessment requirements
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\n[PERSISTENCE] Successfully saved 5 formatted records to '{target_path}' with indent=2.")
    print("=" * 72)

if __name__ == "__main__":
    main()
```

---

## 3. Analytical Diagnostic Note (3–4 Lines)

> The AI's original code attempted to call `response.json()` prior to validating `response.status_code`, which causes an unhandled `JSONDecodeError` whenever an API gateway returns non-200 HTML error pages (such as 500 or 502). Additionally, its commission calculation used integer division (`// 100`), truncating fractional currency values (paise) and causing accounting errors across the payout ledger. Finally, it failed to verify that the `data/processed` directory existed before opening the output file, which triggers a fatal `FileNotFoundError` on pristine environments, and omitted the mandatory `indent=2` argument. To fix these issues, I implemented a strict `status_code == 200` gate prior to decoding, converted commission calculations to precise float arithmetic with rounding, added automated directory creation via `os.makedirs()`, and passed `indent=2` to `json.dump()`.
