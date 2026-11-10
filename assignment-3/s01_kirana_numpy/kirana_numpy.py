"""
================================================================================
SESSION 1: NumPy Foundations (Part 1: Arrays & Creation)
Assignment Track 3: Data Science Foundations
Fictional Scenario: Apna Kirana Store Inventory & Sales System
Author: Atharv Chaudhari (ds-work)
================================================================================
"""

import sys
import timeit
import numpy as np


def main():
    print("=" * 80)
    print("SESSION 1: NumPy Foundations (Part 1: Arrays & Creation)")
    print("Apna Kirana Store Inventory & Sales System")
    print(f"NumPy Version: {np.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # TASK 1: Core Kirana Store Arrays & Attributes
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 1: Core Kirana Store Arrays & Attributes")
    print("=" * 80)

    # Set random seed for reproducibility
    np.random.seed(42)

    # units_sold: 6 items x 7 days with values in [5, 60)
    units_sold = np.random.randint(5, 60, size=(6, 7))

    # price_inr: 6 item prices in INR
    price_inr = np.array([52, 44, 45, 380, 140, 120])

    print("\nunits_sold matrix (6 items x 7 days):")
    print(units_sold)

    print("\nprice_inr vector (6 items):")
    print(price_inr)

    print("\n--- units_sold Attributes ---")
    print(f"  Shape   : {units_sold.shape} (Rows: 6 items, Cols: 7 days)")
    print(f"  Ndim    : {units_sold.ndim} (2D Matrix)")
    print(f"  Size    : {units_sold.size} elements")
    print(f"  Dtype   : {units_sold.dtype}")
    print(f"  Itemsize: {units_sold.itemsize} bytes")

    print("\n--- price_inr Attributes ---")
    print(f"  Shape   : {price_inr.shape} (1D Vector)")
    print(f"  Ndim    : {price_inr.ndim}")
    print(f"  Size    : {price_inr.size} elements")
    print(f"  Dtype   : {price_inr.dtype}")
    print(f"  Itemsize: {price_inr.itemsize} bytes")

    # -------------------------------------------------------------------------
    # TASK 2: Store Tracker Arrays
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 2: Store Tracker Arrays")
    print("=" * 80)

    stock_levels = np.full((6, 7), 100)
    returns = np.zeros((6, 7))
    in_stock = np.ones(6, dtype=bool)

    # Hint demonstration
    default_ones = np.ones(6)
    print("Hint Demonstration:")
    print(f"  np.ones(6) default dtype   : {default_ones.dtype} -> values: {default_ones}")
    print(f"  np.ones(6, dtype=bool)     : {in_stock.dtype}     -> values: {in_stock}\n")

    item_ids = np.arange(101, 107)
    day_marks = np.linspace(0, 6, 7)
    item_pairs = np.eye(6)

    trackers = [
        ("stock_levels", stock_levels),
        ("returns", returns),
        ("in_stock", in_stock),
        ("item_ids", item_ids),
        ("day_marks", day_marks),
        ("item_pairs", item_pairs),
    ]

    print(f"{'Array Name':<14} | {'Dtype':<10} | {'Nbytes':<10}")
    print("-" * 40)
    for name, arr in trackers:
        print(f"{name:<14} | {str(arr.dtype):<10} | {arr.nbytes} bytes")

    # -------------------------------------------------------------------------
    # TASK 3: Python List vs. NumPy Array (Memory & Performance)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 3: Python List vs. NumPy Array Benchmark")
    print("=" * 80)

    bills_list = list(range(1000000))
    bills_arr = np.array(bills_list)
    bills_back = bills_arr.tolist()

    print(f"List length         : {len(bills_list):,}")
    print(f"Array length        : {len(bills_arr):,}")
    print(f"Reconverted length  : {len(bills_back):,}")
    print(f"Roundtrip match     : {bills_list == bills_back}\n")

    list_ptr_size = sys.getsizeof(bills_list)
    arr_nbytes = bills_arr.nbytes

    print(f"sys.getsizeof (list pointers only): {list_ptr_size:,} bytes")
    print(f"bills_arr nbytes                  : {arr_nbytes:,} bytes")

    # Total Python list memory context (pointers + PyObject int headers)
    total_list_est = list_ptr_size + (len(bills_list) * 28)
    print(f"Total list estimated memory       : ~{total_list_est:,} bytes (~{total_list_est / (1024*1024):.2f} MB)")
    print(f"NumPy array total memory          : {arr_nbytes:,} bytes ({arr_nbytes / (1024*1024):.2f} MB)")
    print(f"NumPy memory savings              : ~{total_list_est / arr_nbytes:.2f}x less memory\n")

    # Timing comparison
    t_list = timeit.timeit(lambda: sum(bills_list), number=10) / 10
    t_arr = timeit.timeit(lambda: bills_arr.sum(), number=100) / 100

    print(f"Timing sum(bills_list) : {t_list * 1000:.3f} ms per execution")
    print(f"Timing bills_arr.sum() : {t_arr * 1000:.3f} ms per execution")
    print(f"NumPy speedup factor   : ~{t_list / t_arr:.1f}x faster execution!\n")

    print(f"C_CONTIGUOUS : {bills_arr.flags['C_CONTIGUOUS']}")
    print(f"Strides      : {bills_arr.strides}")

    # -------------------------------------------------------------------------
    # TASK 4: Array Report Function
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 4: Comprehensive Array Report Function")
    print("=" * 80)

    def array_report(name, arr):
        print(
            f"{name:<13} | shape: {str(arr.shape):<11} | ndim: {arr.ndim} | "
            f"size: {arr.size:<7} | dtype: {str(arr.dtype):<8} | "
            f"itemsize: {arr.itemsize}B | nbytes: {arr.nbytes:<8}B"
        )

    all_nine_arrays = [
        ("units_sold", units_sold),
        ("price_inr", price_inr),
        ("stock_levels", stock_levels),
        ("returns", returns),
        ("in_stock", in_stock),
        ("item_ids", item_ids),
        ("day_marks", day_marks),
        ("item_pairs", item_pairs),
        ("bills_arr", bills_arr),
    ]

    print("=" * 86)
    print(f"{'Name':<13} | {'Shape':<18} | {'Ndim'} | {'Size':<12} | {'Dtype':<15} | {'Itemsize'} | {'Nbytes'}")
    print("=" * 86)
    for name, arr in all_nine_arrays:
        array_report(name, arr)
    print("=" * 86)


if __name__ == "__main__":
    main()

