"""
================================================================================
Task 3: Food Delivery Fee Calculator with Functional Tools
Assessment Code: M2-A1 | Python for Data Science
================================================================================
"""

from functools import reduce

def calculate_tiered_commission(amount: float) -> float:
    """
    Applies a tiered commission percentage based on order amount:
      - Tier 1: Up to Rs. 200.00        -> 10% commission
      - Tier 2: Rs. 201.00 to Rs. 500.00 -> 15% commission
      - Tier 3: Above Rs. 500.00         -> 20% commission
    """
    if amount <= 200.00:
        return amount * 0.10
    elif amount <= 500.00:
        return amount * 0.15
    else:
        return amount * 0.20

def run_fee_calculator():
    restaurants = [
        {"id": 101, "name": "Royal Biryani House", "amount": 180.00},
        {"id": 102, "name": "Spice Garden Bistro", "amount": 350.50},
        {"id": 103, "name": "Pizza Palace Express", "amount": 620.00},
        {"id": 104, "name": "Burger King Corner", "amount": 140.25},
        {"id": 105, "name": "Urban Wok Asian", "amount": 480.00},
        {"id": 106, "name": "Cafe Mocha Lounge", "amount": 750.00},
        {"id": 107, "name": "Tandoor Nights", "amount": 290.00},
    ]

    print("=" * 76)
    print("           FOOD DELIVERY COMMISSION CALCULATOR (FUNCTIONAL)")
    print("=" * 76)

    records_with_fee = list(map(
        lambda r: {
            "id": r["id"],
            "name": r["name"],
            "amount": r["amount"],
            "fee": round(calculate_tiered_commission(r["amount"]), 2)
        },
        restaurants
    ))

    print(f"{'ID':<6} | {'Restaurant Name':<26} | {'Order Amount':<16} | {'Commission Fee':<16}")
    print("-" * 76)
    for rec in records_with_fee:
        print(f"#{rec['id']:<5} | {rec['name']:<26} | Rs. {rec['amount']:>9.2f}    | Rs. {rec['fee']:>9.2f}")
    print("=" * 76)

    AUDIT_THRESHOLD = 45.00
    audit_records = list(filter(lambda r: r["fee"] > AUDIT_THRESHOLD, records_with_fee))

    print(f"\n>>> AUDIT REPORT: Records Exceeding Fee Threshold of Rs. {AUDIT_THRESHOLD:.2f}")
    print("-" * 76)
    print(f"{'ID':<6} | {'Restaurant Name':<26} | {'Order Amount':<16} | {'Audit Fee (INR)':<16}")
    print("-" * 76)
    for rec in audit_records:
        print(f"#{rec['id']:<5} | {rec['name']:<26} | Rs. {rec['amount']:>9.2f}    | Rs. {rec['fee']:>9.2f}  [FLAGGED]")
    print(f"Total records flagged for audit: {len(audit_records)}")
    print("-" * 76)

    total_fee = reduce(lambda acc, r: acc + r["fee"], records_with_fee, 0.0)

    print("\n" + "=" * 76)
    print(f"  * Grand Total Commission Fee (reduce): Rs. {total_fee:.2f}")
    print(f"  * Total Evaluated Restaurants        : {len(records_with_fee)}")
    print("=" * 76)

    return records_with_fee, audit_records, total_fee

if __name__ == "__main__":
    run_fee_calculator()
