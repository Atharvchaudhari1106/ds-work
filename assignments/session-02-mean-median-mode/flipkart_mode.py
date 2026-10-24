"""
Task 3: Flipkart Product Ratings - Mode Calculation
File: flipkart_mode.py

Problem Statement:
Write a function most_common_rating(ratings) that takes a list of Flipkart product 
ratings (e.g., [5, 4, 4, 3, 5, 4, 2, 4]) and returns the mode (most frequent rating).
"""

from collections import Counter
import statistics
from typing import List, Any

def most_common_rating(ratings: List[int]) -> int:
    """
    Takes a list of product ratings and returns the mode (most frequent rating).

    Args:
        ratings (List[int]): List of numerical product ratings.

    Returns:
        int: The most frequently occurring rating value.

    Raises:
        ValueError: If ratings list is empty.
    """
    if not ratings:
        raise ValueError("Ratings list cannot be empty.")
    
    # Count frequency of each rating
    frequency_map = Counter(ratings)
    
    # Counter.most_common(1) returns [(value, frequency)]
    most_common_item, highest_count = frequency_map.most_common(1)[0]
    return most_common_item


def main():
    # Flipkart product ratings from the assignment prompt
    flipkart_ratings = [5, 4, 4, 3, 5, 4, 2, 4]

    print("=" * 60)
    print("TASK 3: FLIPKART PRODUCT RATINGS - MODE CALCULATION")
    print("=" * 60)
    print(f"Product Ratings List : {flipkart_ratings}")
    
    # Frequency count breakdown
    freq = Counter(flipkart_ratings)
    print("\n--- Rating Frequency Table ---")
    for rating, count in sorted(freq.items()):
        bar = "*" * count
        print(f"Rating {rating} : {count} times  {bar}")
    
    # Calculate mode using the specified function
    mode_rating = most_common_rating(flipkart_ratings)
    print(f"\n--- Mode Result ---")
    print(f"Most Common Rating (Mode)       : {mode_rating} (appeared {freq[mode_rating]} times)")
    
    # Verification with statistics library
    stats_mode = statistics.mode(flipkart_ratings)
    print(f"Verification (statistics.mode)  : {stats_mode}")
    print("=" * 60)


if __name__ == "__main__":
    main()
