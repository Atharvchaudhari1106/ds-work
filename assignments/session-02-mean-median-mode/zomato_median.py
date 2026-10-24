"""
Task 2: Zomato Order Delivery Times - Median Calculation
File: zomato_median.py

Problem Statement:
Given the following array of delivery times (in minutes) for Zomato orders:
[30, 25, 40, 35, 30, 45, 30], write code to find the median delivery time and print it.
"""

import statistics
from typing import List, Union

def calculate_median(data: List[Union[int, float]]) -> float:
    """
    Calculates the median value of a numerical list.
    
    Algorithm:
    1. Sort the list in ascending order.
    2. If length (n) is odd: median is the middle element at index n // 2.
    3. If length (n) is even: median is the average of the two middle elements.
    """
    if not data:
        raise ValueError("Data list cannot be empty.")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2 != 0:
        # Odd number of observations
        return float(sorted_data[mid])
    else:
        # Even number of observations
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0


def main():
    # Zomato order delivery times in minutes from prompt
    delivery_times = [30, 25, 40, 35, 30, 45, 30]

    print("=" * 60)
    print("TASK 2: ZOMATO ORDER DELIVERY TIMES - MEDIAN CALCULATION")
    print("=" * 60)
    print(f"Original Delivery Times (mins) : {delivery_times}")
    
    sorted_times = sorted(delivery_times)
    n = len(sorted_times)
    print(f"Sorted Delivery Times (mins)   : {sorted_times}")
    print(f"Number of Orders (n)           : {n} (Odd number of values)")
    print(f"Middle Element Index           : {n} // 2 = {n // 2} (Index {n // 2})")

    # Manual Calculation
    median_val = calculate_median(delivery_times)
    print(f"\n--- Median Result ---")
    print(f"Median Delivery Time (Manual)  : {median_val} minutes")

    # Library Verification
    stats_median = statistics.median(delivery_times)
    print(f"Verification (statistics.median): {stats_median} minutes")
    print("=" * 60)


if __name__ == "__main__":
    main()
