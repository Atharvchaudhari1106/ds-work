"""
Task 5: Real-World Dataset Analysis using Pandas
File: dataset_analysis.py

Problem Statement:
Pick any real dataset from Kaggle or UCI (e.g., IPL player runs, Swiggy restaurant 
ratings, or movie box office collections), load it using pandas, and display 
the mean, median, and mode for one numeric column of your choice.
"""

import os
import pandas as pd

def analyze_dataset_column(csv_path: str, column_name: str = "runs"):
    """
    Loads a dataset from CSV and computes the mean, median, and mode
    for a chosen numeric column.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at: {csv_path}")
    
    # 1. Load dataset with pandas
    df = pd.read_csv(csv_path)
    
    print("=" * 70)
    print("TASK 5: REAL DATASET ANALYSIS (IPL PLAYER RUNS - PANDAS)")
    print("=" * 70)
    print(f"Dataset Source : IPL Player Season Statistics (Kaggle dataset)")
    print(f"Dataset Shape  : {df.shape[0]} rows x {df.shape[1]} columns")
    print("\n--- First 5 Rows Preview ---")
    print(df.head())
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in dataset. Available: {list(df.columns)}")
    
    col = df[column_name]
    
    # 2. Compute Mean, Median, and Mode
    col_mean = col.mean()
    col_median = col.median()
    col_mode_series = col.mode()
    
    print(f"\n" + "-" * 70)
    print(f"CENTRAL TENDENCY METRICS FOR COLUMN: '{column_name.upper()}'")
    print("-" * 70)
    print(f"1. Mean (Average)   : {col_mean:.2f}")
    print(f"2. Median (50th %)  : {col_median:.2f}")
    if len(col_mode_series) > 0:
        mode_values = ", ".join(f"{val:.2f}" if isinstance(val, float) else str(val) for val in col_mode_series)
        print(f"3. Mode (Most Freq) : {mode_values}")
    else:
        print(f"3. Mode             : No repeating values")
        
    # Additional statistical insights
    col_min = col.min()
    col_max = col.max()
    col_std = col.std()
    skewness = col.skew()
    
    print(f"\n--- Additional Distribution Insights ---")
    print(f"Minimum Value : {col_min}")
    print(f"Maximum Value : {col_max}")
    print(f"Standard Dev  : {col_std:.2f}")
    print(f"Skewness      : {skewness:.2f}")
    
    if skewness > 0:
        skew_type = "Right-skewed (Positive Skew)"
        reason = "Mean > Median. High-scoring top-order batsmen pull the mean upward."
    elif skewness < 0:
        skew_type = "Left-skewed (Negative Skew)"
        reason = "Mean < Median."
    else:
        skew_type = "Symmetric distribution"
        reason = "Mean ≈ Median."
        
    print(f"Distribution  : {skew_type}")
    print(f"Interpretation: {reason}")
    print("=" * 70)


def main():
    # Path to bundled IPL runs dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "data", "ipl_player_runs.csv")
    
    # Analyze 'runs' column
    analyze_dataset_column(data_file, column_name="runs")
    
    # Also optionally display 'strike_rate' column
    print("\n--- Bonus: Quick Glance at 'strike_rate' Column ---")
    df = pd.read_csv(data_file)
    print(f"Strike Rate Mean   : {df['strike_rate'].mean():.2f}")
    print(f"Strike Rate Median : {df['strike_rate'].median():.2f}")
    print(f"Strike Rate Mode   : {df['strike_rate'].mode().iloc[0]:.2f}")


if __name__ == "__main__":
    main()
