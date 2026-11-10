"""
================================================================================
SESSION 3: NumPy Advanced (Part 3: Matrix Ops & Manipulation)
Assignment Track 3: Data Science Foundations
Fictional Scenario: Apna Kirana Store Multi-Product Matrix Analytics & Markov Engine
Author: Atharv Chaudhari (ds-work)
================================================================================
"""

import numpy as np


def main():
    print("=" * 80)
    print("SESSION 3: NumPy Advanced (Part 3: Matrix Ops & Manipulation)")
    print("Apna Kirana Store Multi-Product Matrix Analytics & Markov Market Share Engine")
    print(f"NumPy Version: {np.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # TASK 3: Revenue Calculation (3 Ways) & Item Co-Sales Matrix
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 3: Daily Revenue Engine (3 Vectorized Methods) & Item Co-Sales")
    print("=" * 80)

    np.random.seed(42)

    # 6 items x 7 days
    units_sold = np.random.randint(5, 60, size=(6, 7))
    price_inr = np.array([52, 44, 45, 380, 140, 120])

    print("units_sold (6 items x 7 days):")
    print(units_sold)
    print("\nprice_inr vector (INR):", price_inr)

    # Method 1: price_inr.dot(units_sold)
    rev_way1 = price_inr.dot(units_sold)

    # Method 2: np.matmul(price_inr, units_sold)
    rev_way2 = np.matmul(price_inr, units_sold)

    # Method 3: (units_sold * price_inr.reshape(6, 1)).sum(axis=0)
    rev_way3 = (units_sold * price_inr.reshape(6, 1)).sum(axis=0)

    print("\nDaily Revenues (Mon - Sun):")
    print(f"  Method 1 (price_inr.dot(units_sold))              : {rev_way1}")
    print(f"  Method 2 (np.matmul(price_inr, units_sold))       : {rev_way2}")
    print(f"  Method 3 ((units_sold * price.reshape).sum(axis=0)): {rev_way3}")

    is_all_equal = np.allclose(rev_way1, rev_way2) and np.allclose(rev_way2, rev_way3)
    print(f"\nVerification: All three revenue computations match identically -> {is_all_equal}")

    # Item Co-Sales Matrix: units_sold @ units_sold.T
    item_cosales = units_sold @ units_sold.T
    print(f"\nItem Co-Sales Matrix Shape: {item_cosales.shape}")
    print("item_cosales (units_sold @ units_sold.T):\n", item_cosales)

    # -------------------------------------------------------------------------
    # TASK 4: Weekly Statistical Summary & Busiest Day
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 4: Weekly Statistical Summary Table & Busiest Day Analysis")
    print("=" * 80)

    items = ['Rice', 'Atta', 'Sugar', 'Tea', 'Oil', 'Dal']
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    item_totals = units_sold.sum(axis=1)
    item_means = units_sold.mean(axis=1)
    item_medians = np.median(units_sold, axis=1)
    item_stds = units_sold.std(axis=1, ddof=0)
    item_vars = units_sold.var(axis=1, ddof=0)

    print("=" * 82)
    print(f"{'Item':<8} | {'SKU':<5} | {'Total':<6} | {'Mean':<8} | {'Median':<8} | {'Std Dev':<9} | {'Variance':<10}")
    print("=" * 82)
    for i in range(len(items)):
        print(f"{items[i]:<8} | {101+i:<5} | {item_totals[i]:<6} | {item_means[i]:<8.2f} | {item_medians[i]:<8.1f} | {item_stds[i]:<9.2f} | {item_vars[i]:<10.2f}")
    print("=" * 82)

    daily_totals = units_sold.sum(axis=0)
    busiest_day_idx = np.argmax(daily_totals)
    busiest_day_num = busiest_day_idx + 1
    busiest_day_name = days[busiest_day_idx]
    max_units = daily_totals[busiest_day_idx]

    print(f"\nBusiest Day: Day {busiest_day_num} ({busiest_day_name}) with {max_units} units sold!")

    # -------------------------------------------------------------------------
    # TASK 1: Markov Brand-Switching & Steady-State Market Share
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 1: Markov Brand-Switching & Steady-State Market Share")
    print("=" * 80)

    switch_p = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.5, 0.2],
        [0.2, 0.3, 0.5]
    ])

    print("switch_p (Brand Switching Matrix):\n", switch_p)

    det_val = np.linalg.det(switch_p)
    inv_p = np.linalg.inv(switch_p)
    inv_check = np.allclose(inv_p @ switch_p, np.eye(3))

    print(f"\nDeterminant np.linalg.det(switch_p) : {det_val:.4f}")
    print(f"np.allclose(inv(switch_p) @ switch_p, np.eye(3)) -> {inv_check}")

    # Eigendecomposition on switch_p.T
    eigenvals, eigenvecs = np.linalg.eig(switch_p.T)
    idx_1 = np.argmin(np.abs(eigenvals - 1.0))
    raw_eigenvector = eigenvecs[:, idx_1].real
    steady_share = raw_eigenvector / raw_eigenvector.sum()

    print(f"\nEigenvalues of switch_p.T: {eigenvals}")
    print(f"Normalized Steady-State Market Share (steady_share): {steady_share}")
    print(f"Sum of steady_share: {steady_share.sum():.6f}")
    print(f"steady_share @ switch_p == steady_share -> {np.allclose(steady_share @ switch_p, steady_share)}")

    # -------------------------------------------------------------------------
    # TASK 2: Concatenate, Stack, Split & Memory Profiling (ravel vs. flatten)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 2: Array Joining, Stacking, Splitting & Memory Profiling")
    print("=" * 80)

    week2 = np.random.randint(5, 60, size=(6, 7))
    two_weeks = np.concatenate([units_sold, week2], axis=1)
    stacked = np.stack([units_sold, week2], axis=0)

    print(f"two_weeks shape (np.concatenate axis=1): {two_weeks.shape} (6 x 14)")
    print(f"stacked shape (np.stack axis=0)        : {stacked.shape} (2 x 6 x 7)")

    # Split and verify
    halves = np.split(two_weeks, 2, axis=1)
    assert np.array_equal(halves[0], units_sold), "First half does not match units_sold!"
    assert np.array_equal(halves[1], week2), "Second half does not match week2!"
    print("Assertion passed: np.split halves identically equal original weeks!")

    # Memory profiling
    two_weeks_test = two_weeks.copy()
    rav = two_weeks_test.ravel()
    flat = two_weeks_test.flatten()

    shares_rav = np.shares_memory(two_weeks_test, rav)
    shares_flat = np.shares_memory(two_weeks_test, flat)

    print(f"\nnp.shares_memory(two_weeks_test, rav)  : {shares_rav} (ravel is a VIEW)")
    print(f"np.shares_memory(two_weeks_test, flat) : {shares_flat} (flatten is a COPY)")

    # Mutation test
    rav[0] = 999
    flat[1] = 888
    print(f"After mutating rav[0]=999  -> two_weeks_test[0, 0] = {two_weeks_test[0, 0]} (Changed!)")
    print(f"After mutating flat[1]=888 -> two_weeks_test[0, 1] = {two_weeks_test[0, 1]} (Protected!)")
    print("=" * 80)


if __name__ == "__main__":
    main()
