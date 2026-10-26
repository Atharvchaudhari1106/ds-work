"""
================================================================================
Task 2: Food Delivery Record Cleaning Script
Assessment Code: M2-A1 | Python for Data Science
================================================================================
"""

def clean_and_process_records():
    raw_restaurants = [
        "   royal biryani house   ",
        "SPICE--GARDEN_BISTRO   ",
        "",
        "998877",
        "   pizza_palace_express   ",
        "     ",
        "burger king-corner   ",
        "12345",
        "urban_wok--asian cuisine  ",
        "   cafe mocha lounge "
    ]

    raw_amounts = [
        "Rs 250.00",
        "Rs. 420.50",
        "Rs 0",
        "500",
        "310.75",
        "Rs 150",
        "180.25",
        "850",
        "540.00",
        "Rs. 225.50"
    ]

    print("=" * 70)
    print("      FOOD DELIVERY DATA PIPELINE: RECORD CLEANING & VALIDATION")
    print("=" * 70)
    print(f"{'Index':<6} | {'Raw Input':<28} | {'Status / Cleaned Name':<28} | {'Amount (INR)':<12}")
    print("-" * 78)

    valid_records = []
    total_valid = 0
    total_skipped = 0
    running_total = 0.0

    for idx, (raw_name, raw_amt) in enumerate(zip(raw_restaurants, raw_amounts), start=1):
        initial_stripped = raw_name.strip()

        if not initial_stripped:
            print(f"[{idx:02d}]  | {repr(raw_name):<28} | [SKIPPED: Empty Entry]       | {'-':<12}")
            total_skipped += 1
            continue

        if initial_stripped.isdigit():
            print(f"[{idx:02d}]  | {raw_name.strip():<28} | [SKIPPED: Purely Numeric]   | {'-':<12}")
            total_skipped += 1
            continue

        cleaned_name = (
            initial_stripped
            .replace("--", " ")
            .replace("_", " ")
            .replace("-", " ")
            .strip()
            .title()
        )

        clean_amt_str = (
            raw_amt.replace("Rs.", "")
            .replace("Rs", "")
            .replace(",", "")
            .strip()
        )
        amount_float = float(clean_amt_str)

        running_total += amount_float
        total_valid += 1
        valid_records.append((cleaned_name, amount_float))

        print(f"[{idx:02d}]  | {raw_name.strip():<28} | {cleaned_name:<28} | Rs. {amount_float:>7.2f} (Running: Rs. {running_total:>8.2f})")

    print("=" * 78)
    print("                           PROCESSING SUMMARY")
    print("=" * 78)
    print(f"  * Total Input Records Evaluated : {len(raw_restaurants)}")
    print(f"  * Total Valid Records Cleaned   : {total_valid}")
    print(f"  * Total Invalid Records Skipped : {total_skipped}")
    print(f"  * Final Cumulative Total Amount : Rs. {running_total:,.2f}")
    print("=" * 78)

    return valid_records, total_valid, total_skipped, running_total

if __name__ == "__main__":
    clean_and_process_records()
