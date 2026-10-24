"""
Task 4: YouTube Channels View Comparison & Outlier Impact Analysis
File: youtube_outliers.py

Problem Statement:
Given three lists representing YouTube video views for three different channels, 
compare the mean, median, and mode for each channel, and decide which channel's 
data is most affected by outliers.

Hint: Try using one list with a very high value (e.g., [100, 120, 110, 105, 5000]) 
to see the effect on mean vs median.
"""

from collections import Counter
import statistics
from typing import List, Dict, Any

def get_channel_stats(views: List[int]) -> Dict[str, Any]:
    """
    Computes mean, median, mode, and outlier sensitivity metrics.
    """
    mean_val = statistics.mean(views)
    median_val = statistics.median(views)
    
    # Mode handling (return the most frequent, or indicate multimodal/no repetition)
    freq = Counter(views)
    max_count = max(freq.values())
    modes = [val for val, count in freq.items() if count == max_count]
    mode_display = modes[0] if max_count > 1 else "No unique mode"
    
    # Outlier impact measure: relative divergence between mean and median
    diff = abs(mean_val - median_val)
    divergence_percent = (diff / median_val) * 100 if median_val != 0 else 0

    return {
        "views": views,
        "mean": mean_val,
        "median": median_val,
        "mode": mode_display,
        "mean_median_diff": diff,
        "divergence_pct": divergence_percent
    }


def main():
    # 3 Channels with distinct distribution characteristics:
    channels = {
        "Channel A (Tech Tutorials - Steady)": [450, 480, 500, 480, 520, 490, 500],
        "Channel B (Daily Vlogs - Moderate spread)": [300, 600, 450, 300, 750, 400, 300],
        "Channel C (Viral Shorts - Severe Outlier)": [100, 120, 110, 105, 100, 5000] # Incorporating assignment hint
    }

    print("=" * 75)
    print("TASK 4: YOUTUBE VIDEO VIEWS - MEAN, MEDIAN, MODE & OUTLIER COMPARISON")
    print("=" * 75)
    
    results = {}
    print(f"{'Channel':<35} | {'Mean':>10} | {'Median':>8} | {'Mode':>10} | {'|Mean-Median|':>12}")
    print("-" * 85)

    for ch_name, views_data in channels.items():
        stats = get_channel_stats(views_data)
        results[ch_name] = stats
        mode_str = str(stats['mode'])
        print(f"{ch_name:<35} | {stats['mean']:>10.2f} | {stats['median']:>8.1f} | {mode_str:>10} | {stats['mean_median_diff']:>12.2f}")

    # Determine which channel is most affected by outliers
    most_affected = max(results.items(), key=lambda item: item[1]['mean_median_diff'])
    ch_winner = most_affected[0]
    data_winner = most_affected[1]

    print("=" * 85)
    print("\n" + "*" * 30 + " CONCLUSION & ANALYSIS " + "*" * 30)
    print(f"\n1. Channel Most Affected by Outliers: {ch_winner}")
    print(f"   - Views List : {data_winner['views']}")
    print(f"   - Mean Views : {data_winner['mean']:.2f}")
    print(f"   - Median     : {data_winner['median']:.1f}")
    print(f"   - Discrepancy (|Mean - Median|) : {data_winner['mean_median_diff']:.2f} views ({data_winner['divergence_pct']:.1f}% divergence)")

    print("\n2. Why does this happen? (Statistical Explanation):")
    print("   - The Mean is sensitive to extreme values (outliers) because every single")
    print("     number is summed up into the numerator.")
    print("   - The extreme viral video with 5,000 views artificially inflates Channel C's")
    print("     mean to over 900+ views, giving a misleading impression that all videos perform this well.")
    print("   - The Median is resistant (robust) to outliers because it only depends on the")
    print("     positional rank order of the sorted data.")
    print("   - Therefore, when data is skewed by outliers, the MEDIAN is the most reliable")
    print("     measure of central tendency.")
    print("=" * 85)


if __name__ == "__main__":
    main()
