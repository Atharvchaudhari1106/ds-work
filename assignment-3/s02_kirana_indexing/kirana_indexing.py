"""
================================================================================
SESSION 2: NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)
Assignment Track 3: Data Science Foundations
Fictional Scenario: Apna Kirana Store Multi-Dimensional Inventory & Revenue Optimization
Author: Atharv Chaudhari (ds-work)
================================================================================
"""

import numpy as np


def main():
    print("=" * 80)
    print("SESSION 2: NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)")
    print("Apna Kirana Store Multi-Dimensional Inventory & Revenue Optimization Engine")
    print(f"NumPy Version: {np.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # TASK 4: Multi-Dimensional Slicing & Subarray Extractions
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 4: Multi-Dimensional Array Generation & Slicing Extractions")
    print("=" * 80)

    np.random.seed(42)

    # Items: rice, atta, sugar, tea, oil, dal
    units_sold = np.random.randint(5, 60, size=(6, 7))

    # month_units: 4 weeks x 6 items x 7 days
    month_units = np.random.randint(5, 60, size=(4, 6, 7))

    print("units_sold (6 items x 7 days):")
    print(units_sold)
    print(f"\nmonth_units shape: {month_units.shape} (4 weeks x 6 items x 7 days)")

    # 1. tea_week (row index 3)
    tea_week = units_sold[3, :].copy()

    # 2. day3_sales (column index 2: Wednesday, 0-indexed)
    day3_sales = units_sold[:, 2].copy()
    day3_sales_idx3 = units_sold[:, 3].copy()

    # 3. staple_block (first 3 items, last 4 days)
    staple_block = units_sold[0:3, 3:7].copy()

    # 4. alt_days (every second day)
    alt_days = units_sold[:, ::2].copy()

    # 5. dal_last (negative index -1)
    dal_last = units_sold[-1, :].copy()

    # 6. w3_tea_d6 (Week 3, Tea, Day 6)
    w3_tea_d6 = month_units[2, 3, 5]
    w3_tea_d6_raw_idx = month_units[3, 3, 6]

    print("\n--- Subarray Extractions ---")
    print(f"  tea_week (row index 3)           : {tea_week}")
    print(f"  day3_sales (column index 2: Wed) : {day3_sales}")
    print(f"  day3_sales (column index 3: Thu) : {day3_sales_idx3}")
    print(f"\n  staple_block (shape {staple_block.shape}):\n{staple_block}")
    print(f"\n  alt_days (shape {alt_days.shape}):\n{alt_days}")
    print(f"\n  dal_last (negative index -1)     : {dal_last}")
    print(f"  w3_tea_d6 (0-indexed [2, 3, 5])  : {w3_tea_d6}")
    print(f"  w3_tea_d6 (direct [3, 3, 6])     : {w3_tea_d6_raw_idx}")

    # -------------------------------------------------------------------------
    # TASK 1: Boolean Indexing, Fancy Indexing & Negative Masking
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 1: Boolean Indexing, Fancy Indexing & Stock Depletion Masking")
    print("=" * 80)

    # 1. high_mask (units_sold > 40)
    high_mask = units_sold > 40
    high_count = high_mask.sum()
    high_values = units_sold[high_mask]

    print(f"Count of True entries (sales > 40): {high_count} out of {units_sold.size}")
    print(f"Matching high sales values: {high_values}")

    # 2. Fancy indexing [0, 3, 5] for rice, tea, dal
    top_items = units_sold[[0, 3, 5]]
    print(f"\ntop_items shape (indices [0, 3, 5]): {top_items.shape}")
    print(top_items)

    # 3. stock_change and negative value rectification (NO LOOPS)
    stock_change = units_sold - 30
    stock_change_clean = stock_change.copy()
    neg_mask = stock_change_clean < 0
    num_changed = neg_mask.sum()
    stock_change_clean[neg_mask] = 0

    print(f"\nNumber of negative stock change values rectified to 0: {num_changed}")
    print("Cleaned stock_change matrix:\n", stock_change_clean)

    # -------------------------------------------------------------------------
    # TASK 2: Broadcasting Rules & Multi-Tier Revenue
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 2: Broadcasting Rules & Multi-Tier Revenue Engine")
    print("=" * 80)

    # 1. price_col (6, 1) from nested list
    price_col = np.array([[52], [44], [45], [380], [140], [120]])

    # Array-to-array broadcasting
    revenue_inr = units_sold * price_col
    print(f"units_sold shape: {units_sold.shape} | price_col shape: {price_col.shape}")
    print(f"revenue_inr shape: {revenue_inr.shape}")
    print("revenue_inr matrix:\n", revenue_inr)

    # Scalar broadcasting
    revenue_gst = revenue_inr * 1.05

    # Array-to-array broadcasting across days
    day_factor = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.3, 1.4])
    weekend_revenue = revenue_inr * day_factor

    print(f"\nweekend_revenue shape: {weekend_revenue.shape}")
    print("weekend_revenue (with 1.3x Sat & 1.4x Sun factor):\n", np.round(weekend_revenue, 1))

    # Verification: row 1 equals units_sold[1] * 44
    is_row1_equal = np.array_equal(revenue_inr[1], units_sold[1] * 44)
    print(f"\nVerification: np.array_equal(revenue_inr[1], units_sold[1] * 44) -> {is_row1_equal}")

    # -------------------------------------------------------------------------
    # TASK 3: Feature Scaling (Min-Max Normalization) with keepdims=True
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 3: Feature Scaling (Min-Max Normalization)")
    print("=" * 80)

    row_mins = units_sold.min(axis=1, keepdims=True)
    row_maxs = units_sold.max(axis=1, keepdims=True)
    row_ranges = row_maxs - row_mins

    units_scaled = (units_sold - row_mins) / row_ranges

    print(f"units_scaled shape: {units_scaled.shape}")
    print("units_scaled (normalized [0.0, 1.0] per item):\n", np.round(units_scaled, 3))

    scaled_mins = units_scaled.min(axis=1)
    scaled_maxs = units_scaled.max(axis=1)

    all_mins_zero = np.allclose(scaled_mins, 0.0)
    all_maxs_one = np.allclose(scaled_maxs, 1.0)

    print(f"\nScaled row minimums: {scaled_mins}")
    print(f"Scaled row maximums: {scaled_maxs}")
    print(f"np.allclose(scaled_mins, 0.0) -> {all_mins_zero}")
    print(f"np.allclose(scaled_maxs, 1.0) -> {all_maxs_one}")
    print("=" * 80)


if __name__ == "__main__":
    main()
