"""
================================================================================
Section D: AI-Augmented Learning — Corrected Script
Assessment Code: M2-A1 | Python for Data Science
================================================================================
"""

import os
import sys
import json
import requests

def main():
    print("=" * 72)
    print("       FOOD DELIVERY PLATFORM - AI-AUGMENTED PIPELINE (CORRECTED)")
    print("=" * 72)

    url = "https://jsonplaceholder.typicode.com/posts?_limit=5"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        print(f"[API ERROR] Network connection error occurred: {exc}")
        print("[NOTICE] Halting execution safely without unhandled crash.")
        sys.exit(0)

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

    order_amounts = [150.0, 200.0, 320.0, 500.0, 650.0, 1200.0]

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

    target_path = os.path.join("data", "processed", "records.json")

    parent_dir = os.path.dirname(target_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\n[PERSISTENCE] Successfully saved 5 formatted records to '{target_path}' with indent=2.")
    print("=" * 72)

if __name__ == "__main__":
    main()
