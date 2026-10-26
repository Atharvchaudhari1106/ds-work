"""
Task 1: Daily Order Analysis with NumPy
Assessment: M4-A1 | Program: Data Science
Domain: Food Delivery Platform Daily Performance
"""

import numpy as np

def run_daily_order_analysis():
    print("=" * 70)
    print("       TASK 1: DAILY ORDER & REVENUE ANALYSIS WITH NUMPY")
    print("=" * 70)

    # 1. Reproducibility seed
    np.random.seed(42)

    # 2. Generate 30 days of synthetic order counts (100 to 800) and revenue (5000.0 to 50000.0)
    num_days = 30
    daily_orders = np.random.randint(100, 801, size=num_days)
    daily_revenue = np.random.uniform(5000.0, 50000.0, size=num_days).round(2)

    print(f"\n[Generated Data]")
    print(f"Daily Orders Array (30 days):\n{daily_orders}")
    print(f"\nDaily Revenue Array (30 days, INR):\n{daily_revenue}")

    # 3. Statistical Calculations
    total_orders = int(np.sum(daily_orders))
    total_revenue = float(np.sum(daily_revenue))
    mean_orders = float(np.mean(daily_orders))
    std_orders = float(np.std(daily_orders))
    
    # Day number with highest single-day revenue (0-indexed and 1-indexed)
    highest_rev_idx = int(np.argmax(daily_revenue))
    highest_rev_val = daily_revenue[highest_rev_idx]

    print("\n" + "-" * 70)
    print("                      SUMMARY STATISTICS")
    print("-" * 70)
    print(f"Total Orders Fulfilled       : {total_orders:,} orders")
    print(f"Total Revenue Generated      : INR {total_revenue:,.2f}")
    print(f"Mean Daily Orders            : {mean_orders:.2f} orders/day")
    print(f"Standard Deviation of Orders : {std_orders:.2f} orders")
    print(f"Peak Revenue Day Index       : Index {highest_rev_idx} (Day {highest_rev_idx + 1})")
    print(f"Peak Revenue Amount          : INR {highest_rev_val:,.2f} with {daily_orders[highest_rev_idx]} orders")

    # 4. Boolean Indexing for Surge / Peak Days (order count > mean + 1 std)
    peak_threshold = mean_orders + 1.0 * std_orders
    peak_mask = daily_orders > peak_threshold
    peak_days_indices = np.where(peak_mask)[0]
    peak_orders = daily_orders[peak_mask]
    peak_revenues = daily_revenue[peak_mask]
    peak_day_count = int(np.sum(peak_mask))
    peak_total_revenue = float(np.sum(peak_revenues))

    print("\n" + "-" * 70)
    print("               BOOLEAN INDEXING: PEAK / SURGE DAYS")
    print("-" * 70)
    print(f"Surge Order Threshold (Mean + 1 Std) : > {peak_threshold:.2f} orders")
    print(f"Number of Peak Days Identified       : {peak_day_count} days")
    print(f"Peak Days (Day Numbers 1-indexed)    : {[int(idx + 1) for idx in peak_days_indices]}")
    print(f"Peak Days Order Counts               : {peak_orders.tolist()}")
    print(f"Total Revenue on Peak Days           : INR {peak_total_revenue:,.2f}")
    print(f"Peak Days Revenue Share of Total     : {(peak_total_revenue / total_revenue) * 100:.2f}%")

    # 5. Matrix Reshaping into 5x6 (5 blocks of 6 days each)
    order_matrix_5x6 = daily_orders.reshape(5, 6)
    block_totals = np.sum(order_matrix_5x6, axis=1)

    print("\n" + "-" * 70)
    print("              RESHAPED 5x6 MATRIX & BLOCK TOTALS")
    print("-" * 70)
    print("5x6 Matrix (5 Weekly Blocks of 6 Days):\n", order_matrix_5x6)
    print("\nTotal Orders per Block (np.sum(axis=1)):")
    for block_num, b_total in enumerate(block_totals, start=1):
        print(f"  * Block {block_num} (Days {(block_num-1)*6 + 1:02d} to {block_num*6:02d}) : {b_total:,} orders")

    print("\nVerification: Sum of 5 blocks =", np.sum(block_totals), "== Total Orders =", total_orders)
    print("=" * 70)

if __name__ == "__main__":
    run_daily_order_analysis()
