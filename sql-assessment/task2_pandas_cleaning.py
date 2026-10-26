"""
Task 2: Food Delivery Orders Data Cleaning Pipeline
Assessment: M4-A1 | Program: Data Science
Domain: Food Delivery Orders Realistic Cleaning & Outlier Treatment
"""

import numpy as np
import pandas as pd
from tabulate import tabulate

def create_raw_orders_dataset() -> pd.DataFrame:
    """
    Creates a simulated dataset of food delivery orders with realistic data quality issues:
    - At least 20 rows (24 total rows created)
    - Columns: order_id, customer_name, restaurant_name, category, delivery_time_mins, order_value, rating
    - Missing values introduced across numeric and categorical columns (>= 4 missing values)
    - 3 duplicate rows manually introduced
    - Realistic high-value outliers in order_value
    """
    raw_data = [
        # (order_id, customer_name, restaurant_name, category, delivery_time, order_val, rating)
        (101, "Aarav Sharma",   "Spice Symphony",   "Indian",   32.0,   450.0,  4.6),
        (102, "Diya Patel",     "Pizza Roma",       "Italian",  28.0,   620.0,  4.2),
        (103, "Rohan Verma",    "Burger Garage",    "Burgers",  45.0,   310.0,  3.8),
        (104, "Ananya Iyer",    "Dragon Wok",       "Chinese",  np.nan, 580.0,  4.5), # Null delivery_time
        (105, "Kabir Mehta",    "Taco Fiesta",      "Mexican",  24.0,   490.0,  4.1),
        (106, "Pooja Reddy",    "Spice Symphony",   "Indian",   36.0,   750.0,  4.7),
        (107, "Vikram Malhotra","Sushi Bay",        "Japanese", 52.0,   np.nan, 4.8), # Null order_value
        (108, "Neha Kapoor",    "Pizza Roma",       "Italian",  30.0,   540.0,  4.0),
        (109, "Aditya Nair",    "Dragon Wok",       np.nan,     42.0,   680.0,  3.9), # Null category
        (110, "Sneha Joshi",    "Burger Garage",    "Burgers",  22.0,   290.0,  np.nan), # Null rating
        (111, "Ishaan Sen",     "Taco Fiesta",      "Mexican",  np.nan, 3950.0, 4.3), # Null delivery & Outlier value
        (112, "Tanvi Kulkarni", "Spice Symphony",   "Indian",   38.0,   820.0,  4.9),
        (113, "Arjun Gupta",    "Curry House",      "Indian",   40.0,   4600.0, 4.4), # Extreme Outlier order_value
        (114, "Meera Bansal",   "Pasta Bella",      "Italian",  29.0,   510.0,  4.1),
        (115, "Varun Rao",      "Dragon Wok",       "Chinese",  35.0,   720.0,  4.0),
        (116, "Siddharth Jain", "Burger Garage",    "Burgers",  26.0,   340.0,  3.7),
        (117, "Kavya Menon",    "Sushi Bay",        "Japanese", 48.0,   1250.0, 4.6),
        (118, "Rahul Desai",    "Taco Fiesta",      "Mexican",  31.0,   480.0,  4.2),
        (119, "Zara Khan",      "Pizza Roma",       "Italian",  27.0,   640.0,  4.5),
        (120, "Karan Singhal",  "Curry House",      "Indian",   34.0,   530.0,  4.3),
        (121, "Priya Sundaram", "Pasta Bella",      "Italian",  33.0,   590.0,  4.4),
        # 3 Duplicate Rows: Exact duplicates of order_id 101, 105, and 108
        (101, "Aarav Sharma",   "Spice Symphony",   "Indian",   32.0,   450.0,  4.6),
        (105, "Kabir Mehta",    "Taco Fiesta",      "Mexican",  24.0,   490.0,  4.1),
        (108, "Neha Kapoor",    "Pizza Roma",       "Italian",  30.0,   540.0,  4.0),
    ]

    columns = [
        "order_id", "customer_name", "restaurant_name",
        "category", "delivery_time_mins", "order_value", "rating"
    ]
    df = pd.DataFrame(raw_data, columns=columns)
    return df

def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 75)
    print("       TASK 2: FOOD DELIVERY ORDERS DATA CLEANING PIPELINE")
    print("=" * 75)

    print("\n--- [Step 1: Inspecting Raw Simulated Dataset] ---")
    print(f"Initial Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("\nInitial First 8 Rows:")
    print(tabulate(df.head(8), headers="keys", tablefmt="psql", showindex=False))

    # 1. Missing Values Treatment
    print("\n--- [Step 2: Missing Values Inspection & Imputation] ---")
    null_counts_before = df.isnull().sum()
    print("Null Counts BEFORE Imputation:")
    print(null_counts_before[null_counts_before > 0])
    total_missing_before = df.isnull().sum().sum()
    print(f"Total Missing Values Count: {total_missing_before}")

    # Compute imputation statistics
    delivery_median = df['delivery_time_mins'].median()
    order_val_median = df['order_value'].median()
    rating_mean = round(df['rating'].mean(), 1)
    category_mode = df['category'].mode()[0]

    print("\nImputation Metrics Computed:")
    print(f"  * delivery_time_mins Median : {delivery_median:.1f} mins")
    print(f"  * order_value Median        : INR {order_val_median:.2f}")
    print(f"  * rating Mean (rounded 1 dec): {rating_mean:.1f}")
    print(f"  * category Mode             : '{category_mode}'")

    # Apply imputation
    df['delivery_time_mins'] = df['delivery_time_mins'].fillna(delivery_median)
    df['order_value'] = df['order_value'].fillna(order_val_median)
    df['rating'] = df['rating'].fillna(rating_mean)
    df['category'] = df['category'].fillna(category_mode)

    null_counts_after = df.isnull().sum()
    print("\nNull Counts AFTER Imputation:")
    print(null_counts_after)
    print(f"Total Missing Values Remaining: {df.isnull().sum().sum()}")

    # 2. Duplicate Rows Removal
    print("\n--- [Step 3: Duplicate Rows Detection & Removal] ---")
    initial_shape = df.shape
    num_duplicates = df.duplicated().sum()
    print(f"Duplicate Rows Identified: {num_duplicates}")
    print("Identified Duplicate Rows:")
    print(tabulate(df[df.duplicated(keep=False)], headers="keys", tablefmt="psql", showindex=False))

    df = df.drop_duplicates().reset_index(drop=True)
    dedup_shape = df.shape
    print(f"\nDataFrame Shape BEFORE Deduplication : {initial_shape}")
    print(f"DataFrame Shape AFTER Deduplication  : {dedup_shape}")
    print(f"Rows Removed                         : {initial_shape[0] - dedup_shape[0]}")

    # 3. Outlier Detection in order_value using IQR Method
    print("\n--- [Step 4: Outlier Detection & Capping in order_value (IQR Method)] ---")
    q1 = df['order_value'].quantile(0.25)
    q3 = df['order_value'].quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    print(f"Summary Statistics for 'order_value':")
    print(f"  * 25th Percentile (Q1) : INR {q1:.2f}")
    print(f"  * 75th Percentile (Q3) : INR {q3:.2f}")
    print(f"  * Interquartile Range  : INR {iqr:.2f}")
    print(f"  * Lower Fence (Q1 - 1.5*IQR) : INR {lower_fence:.2f}")
    print(f"  * Upper Fence (Q3 + 1.5*IQR) : INR {upper_fence:.2f}")

    # Filter outlier rows (orders with order_value > upper_fence or < lower_fence)
    outlier_mask = (df['order_value'] < lower_fence) | (df['order_value'] > upper_fence)
    outlier_rows = df[outlier_mask]

    print(f"\nOutlier Rows Detected ({len(outlier_rows)} row(s)):")
    print(tabulate(outlier_rows[['order_id', 'customer_name', 'restaurant_name', 'category', 'order_value']], 
                   headers="keys", tablefmt="psql", showindex=False))

    # Cap outliers at upper fence using clip()
    df['order_value'] = df['order_value'].clip(lower=lower_fence, upper=upper_fence)
    print(f"\nOutlier Capping Applied: All order_value > {upper_fence:.2f} capped at upper fence.")

    print("\nPost-Capping Verification for Detected Outlier Rows:")
    capped_rows = df[df['order_id'].isin(outlier_rows['order_id'])]
    print(tabulate(capped_rows[['order_id', 'customer_name', 'restaurant_name', 'order_value']], 
                   headers="keys", tablefmt="psql", showindex=False))

    print("\n" + "=" * 75)
    print("                      CLEANED DATASET PREVIEW")
    print("=" * 75)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=True))
    return df

if __name__ == "__main__":
    df_raw = create_raw_orders_dataset()
    df_clean = run_cleaning_pipeline(df_raw)
