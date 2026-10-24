"""
Runner & Verification Suite for Session 2 Assignment Tasks
Runs all 5 tasks sequentially to verify outputs.
"""

import sys
import os

# Ensure current directory is on sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import playlist_stats
import zomato_median
import flipkart_mode
import youtube_outliers
import dataset_analysis

def run_suite():
    print("#" * 75)
    print("DATA SCIENCE ASSIGNMENT: SESSION 2 - MEAN, MEDIAN & MODE")
    print("#" * 75)
    print("\n")
    
    # Task 1
    playlist_stats.display_playlist_statistics([120, 135, 150, 200, 120, 90, 200])
    print("\n")
    
    # Task 2
    zomato_median.main()
    print("\n")
    
    # Task 3
    flipkart_mode.main()
    print("\n")
    
    # Task 4
    youtube_outliers.main()
    print("\n")
    
    # Task 5
    dataset_analysis.main()
    print("\n")
    
    print("#" * 75)
    print("ALL 5 ASSIGNMENT TASKS COMPLETED SUCCESSFULLY!")
    print("#" * 75)

if __name__ == "__main__":
    run_suite()
