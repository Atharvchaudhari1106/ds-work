"""
Task 1: Spotify Playlist Daily Play Count - Mean Calculation
File: playlist_stats.py

Problem Statement:
Create a Python script called playlist_stats.py that takes a list of daily Spotify 
song play counts (e.g., [120, 135, 150, 200, 120, 90, 200]) and calculates 
the mean (average) number of plays.
"""

import statistics
from typing import List, Union

def calculate_mean(play_counts: List[Union[int, float]]) -> float:
    """
    Calculates the arithmetic mean (average) of a list of daily song play counts.

    Formula:
        Mean = sum(play_counts) / len(play_counts)

    Args:
        play_counts (List[int | float]): List of play counts.

    Returns:
        float: The calculated mean value.

    Raises:
        ValueError: If play_counts list is empty.
    """
    if not play_counts:
        raise ValueError("Play counts list cannot be empty.")
    
    total_plays = sum(play_counts)
    total_days = len(play_counts)
    return total_plays / total_days


def display_playlist_statistics(play_counts: List[int]) -> None:
    """
    Displays a detailed breakdown of the Spotify playlist stats.
    """
    print("=" * 60)
    print("TASK 1: SPOTIFY PLAYLIST DAILY PLAYS - MEAN CALCULATION")
    print("=" * 60)
    print(f"Daily Spotify Play Counts : {play_counts}")
    print(f"Total Recorded Days       : {len(play_counts)}")
    print(f"Total Song Plays          : {sum(play_counts)}")
    
    # 1. Manual Arithmetic Calculation
    mean_manual = calculate_mean(play_counts)
    print(f"\n--- Calculation ---")
    print(f"Formula: Sum of plays / Number of days")
    print(f"         {sum(play_counts)} / {len(play_counts)}")
    print(f"Result (Mean Daily Plays) : {mean_manual:.2f}")

    # 2. Verification using Python's standard library
    mean_stats_lib = statistics.mean(play_counts)
    print(f"Verification (statistics.mean) : {mean_stats_lib:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    # Example dataset provided in the assignment
    sample_play_counts = [120, 135, 150, 200, 120, 90, 200]
    display_playlist_statistics(sample_play_counts)
