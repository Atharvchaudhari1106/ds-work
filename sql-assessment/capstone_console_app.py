"""
Section C — Mini Capstone Project
Console Application: Food Delivery Analytics Console Application
Assessment: M4-A1 | Program: Data Science
Integrates:
  - Module 3: Data Cleaning, Imputation & Outlier Handling
  - Module 4: SQLite Database Modeling, Aggregation & Relational Joins
  - Module 3: Exploratory Visualisation (Side-by-side Subplots with Seaborn)
  - Multi-sheet Excel Export via pandas.ExcelWriter
"""

import os
import sys
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

DB_FILE = "food_delivery.db"
EXCEL_REPORT_FILE = "food_delivery_report.xlsx"
CHART_EXPORT_FILE = "capstone_charts.png"

class FoodDeliveryAnalyticsApp:
    def __init__(self, db_path: str = DB_FILE, excel_path: str = EXCEL_REPORT_FILE):
        self.db_path = db_path
        self.excel_path = excel_path
        self.raw_df = None
        self.cleaned_df = None
        self.sql_category_summary = None
        self.sql_restaurant_summary = None

    # =========================================================================
    # OPTION 1: LOAD & CLEAN DATA
    # =========================================================================
    def load_and_clean_data(self) -> pd.DataFrame:
        print("\n" + "=" * 78)
        print("                 [OPTION 1] LOAD & CLEAN FOOD DELIVERY DATA")
        print("=" * 78)

        # 1. Simulate realistic dataset with known quality defects
        raw_records = [
            (101, "Aarav Sharma",   "Spice Symphony",   "Indian",   "Mumbai",    32.0,   450.0,  4.6),
            (102, "Diya Patel",     "Pizza Roma",       "Italian",  "Bengaluru", 28.0,   620.0,  4.2),
            (103, "Rohan Verma",    "Burger Garage",    "Burgers",  "Delhi",     45.0,   310.0,  3.8),
            (104, "Ananya Iyer",    "Dragon Wok",       "Chinese",  "Mumbai",    np.nan, 580.0,  4.5), # Null delivery
            (105, "Kabir Mehta",    "Taco Fiesta",      "Mexican",  "Pune",      24.0,   490.0,  4.1),
            (106, "Pooja Reddy",    "Spice Symphony",   "Indian",   "Mumbai",    36.0,   750.0,  4.7),
            (107, "Vikram Malhotra","Sushi Bay",        "Japanese", "Bengaluru", 52.0,   np.nan, 4.8), # Null order_val
            (108, "Neha Kapoor",    "Pizza Roma",       "Italian",  "Bengaluru", 30.0,   540.0,  4.0),
            (109, "Aditya Nair",    "Dragon Wok",       np.nan,     "Mumbai",    42.0,   680.0,  3.9), # Null category
            (110, "Sneha Joshi",    "Burger Garage",    "Burgers",  "Delhi",     22.0,   290.0,  np.nan), # Null rating
            (111, "Ishaan Sen",     "Taco Fiesta",      "Mexican",  "Pune",      np.nan, 3950.0, 4.3), # Outlier & Null
            (112, "Tanvi Kulkarni", "Spice Symphony",   "Indian",   "Mumbai",    38.0,   820.0,  4.9),
            (113, "Arjun Gupta",    "Curry House",      "Indian",   "Delhi",     40.0,   4600.0, 4.4), # Outlier
            (114, "Meera Bansal",   "Pasta Bella",      "Italian",  "Pune",      29.0,   510.0,  4.1),
            (115, "Varun Rao",      "Dragon Wok",       "Chinese",  "Mumbai",    35.0,   720.0,  4.0),
            (116, "Siddharth Jain", "Burger Garage",    "Burgers",  "Delhi",     26.0,   340.0,  3.7),
            (117, "Kavya Menon",    "Sushi Bay",        "Japanese", "Bengaluru", 48.0,   1250.0, 4.6),
            (118, "Rahul Desai",    "Taco Fiesta",      "Mexican",  "Pune",      31.0,   480.0,  4.2),
            (119, "Zara Khan",      "Pizza Roma",       "Italian",  "Bengaluru", 27.0,   640.0,  4.5),
            (120, "Karan Singhal",  "Curry House",      "Indian",   "Delhi",     34.0,   530.0,  4.3),
            (121, "Priya Sundaram", "Pasta Bella",      "Italian",  "Pune",      33.0,   590.0,  4.4),
            # 3 Duplicate rows
            (101, "Aarav Sharma",   "Spice Symphony",   "Indian",   "Mumbai",    32.0,   450.0,  4.6),
            (105, "Kabir Mehta",    "Taco Fiesta",      "Mexican",  "Pune",      24.0,   490.0,  4.1),
            (108, "Neha Kapoor",    "Pizza Roma",       "Italian",  "Bengaluru", 30.0,   540.0,  4.0),
        ]
        columns = ["order_id", "customer_name", "restaurant_name", "category", "city", 
                   "delivery_time_mins", "order_value", "rating"]
        self.raw_df = pd.DataFrame(raw_records, columns=columns)

        # Baseline Data Quality Summary
        raw_rows = len(self.raw_df)
        raw_nulls = int(self.raw_df.isnull().sum().sum())
        raw_dups = int(self.raw_df.duplicated().sum())

        # 2. Imputation Strategies
        deliv_median = self.raw_df['delivery_time_mins'].median()
        val_median = self.raw_df['order_value'].median()
        rating_mean = round(self.raw_df['rating'].mean(), 1)
        cat_mode = self.raw_df['category'].mode()[0]

        df_clean = self.raw_df.copy()
        df_clean['delivery_time_mins'] = df_clean['delivery_time_mins'].fillna(deliv_median)
        df_clean['order_value'] = df_clean['order_value'].fillna(val_median)
        df_clean['rating'] = df_clean['rating'].fillna(rating_mean)
        df_clean['category'] = df_clean['category'].fillna(cat_mode)

        # 3. Deduplication
        df_clean = df_clean.drop_duplicates().reset_index(drop=True)

        # 4. Outlier Detection & Capping (IQR)
        q1 = df_clean['order_value'].quantile(0.25)
        q3 = df_clean['order_value'].quantile(0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        
        outliers_detected = int(((df_clean['order_value'] < lower_fence) | (df_clean['order_value'] > upper_fence)).sum())
        df_clean['order_value'] = df_clean['order_value'].clip(lower=lower_fence, upper=upper_fence)

        clean_rows = len(df_clean)
        clean_nulls = int(df_clean.isnull().sum().sum())
        clean_dups = int(df_clean.duplicated().sum())

        self.cleaned_df = df_clean

        # Data Quality Summary Report
        summary_table = [
            ["Total Order Records", raw_rows, clean_rows, f"-{raw_rows - clean_rows} (Deduplicated)"],
            ["Missing / Null Cells", raw_nulls, clean_nulls, f"Resolved via Median/Mean/Mode"],
            ["Duplicate Records", raw_dups, clean_dups, f"-{raw_dups} Dropped"],
            ["Order Value Outliers", f"{outliers_detected} Detected", 0, f"Capped at Upper Fence (INR {upper_fence:.2f})"],
            ["Order Value Max", f"INR {self.raw_df['order_value'].max():.2f}", f"INR {df_clean['order_value'].max():.2f}", "Protected against extreme skew"]
        ]

        print("\n=== DATA QUALITY AUDIT & RECTIFICATION SUMMARY ===")
        print(tabulate(summary_table, headers=["Data Quality Metric", "Before Cleaning", "After Cleaning", "Applied Transformation"], tablefmt="psql"))
        print(f"\n[SUCCESS] Loaded and cleaned {clean_rows} validated orders ready for analytics.")
        return self.cleaned_df

    # =========================================================================
    # OPTION 2: RUN SQL ANALYSIS
    # =========================================================================
    def run_sql_analysis(self):
        print("\n" + "=" * 78)
        print("                 [OPTION 2] RUN SQL RELATIONAL DATABASE ANALYSIS")
        print("=" * 78)

        # Ensure database exists
        if not os.path.exists(self.db_path):
            print(f"[INFO] Initializing SQLite database at '{self.db_path}'...")
            from task4_sql_python_report import init_and_populate_database
            init_and_populate_database(self.db_path)

        conn = sqlite3.connect(self.db_path)

        # Query 1: GROUP BY with aggregate functions (COUNT, SUM, AVG) by cuisine category
        query_category = """
        SELECT 
            r.category AS cuisine_category,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.order_value), 2) AS total_revenue_inr,
            ROUND(AVG(o.order_value), 2) AS avg_order_value_inr,
            ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_mins,
            ROUND(AVG(o.rating), 2) AS avg_customer_rating
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.category
        ORDER BY total_revenue_inr DESC;
        """
        self.sql_category_summary = pd.read_sql_query(query_category, conn)

        # Query 2: Detailed JOIN between restaurants and orders with city segmentation
        query_restaurant = """
        SELECT 
            r.restaurant_id,
            r.name AS restaurant_name,
            r.category,
            r.city,
            COUNT(o.order_id) AS total_orders,
            ROUND(COALESCE(SUM(o.order_value), 0.0), 2) AS total_revenue_inr,
            ROUND(COALESCE(AVG(o.rating), 0.0), 2) AS avg_rating
        FROM restaurants r
        LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.name, r.category, r.city
        ORDER BY total_revenue_inr DESC;
        """
        self.sql_restaurant_summary = pd.read_sql_query(query_restaurant, conn)
        conn.close()

        print("\n>>> QUERY 1: Category-Level Performance (GROUP BY with Aggregates)")
        print(tabulate(self.sql_category_summary, headers="keys", tablefmt="psql", showindex=False))

        print("\n>>> QUERY 2: Restaurant Performance & City Breakdown (Relational LEFT JOIN)")
        print(tabulate(self.sql_restaurant_summary, headers="keys", tablefmt="psql", showindex=False))

    # =========================================================================
    # OPTION 3: VIEW CHARTS (SIDE-BY-SIDE SUBPLOTS)
    # =========================================================================
    def view_charts(self, save_path: str = CHART_EXPORT_FILE):
        print("\n" + "=" * 78)
        print("                 [OPTION 3] GENERATE & DISPLAY VISUAL CHARTS")
        print("=" * 78)

        if self.cleaned_df is None:
            print("[INFO] Cleaned dataset not in memory. Automatically running Step 1 first...")
            self.load_and_clean_data()

        df = self.cleaned_df

        sns.set_theme(style="whitegrid", font="sans-serif")
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle("Food Delivery Analytics — Operational Insights", fontsize=16, fontweight='bold', y=1.02)

        # Chart 1: Seaborn countplot showing orders by category
        cat_order = df['category'].value_counts().index
        palette1 = sns.color_palette("viridis", n_colors=len(cat_order))
        sns.countplot(
            data=df, 
            x='category', 
            order=cat_order, 
            ax=axes[0], 
            palette=palette1,
            hue='category',
            legend=False
        )
        axes[0].set_title("Order Volume by Cuisine Category", fontsize=13, fontweight='bold', pad=10)
        axes[0].set_xlabel("Cuisine Category", fontsize=11, fontweight='semibold')
        axes[0].set_ylabel("Total Order Count", fontsize=11, fontweight='semibold')
        axes[0].grid(axis='y', linestyle='--', alpha=0.5)

        # Direct labels on countplot
        for p in axes[0].patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                axes[0].annotate(f"{int(val)}", (p.get_x() + p.get_width() / 2., val),
                                ha='center', va='bottom', fontsize=10, fontweight='bold',
                                xytext=(0, 3), textcoords='offset points')

        # Chart 2: Seaborn barplot showing average delivery time by city
        city_order = df.groupby('city')['delivery_time_mins'].mean().sort_values(ascending=False).index
        palette2 = sns.color_palette("rocket", n_colors=len(city_order))
        sns.barplot(
            data=df, 
            x='city', 
            y='delivery_time_mins', 
            order=city_order,
            estimator=np.mean, 
            errorbar=None, 
            ax=axes[1], 
            palette=palette2,
            hue='city',
            legend=False
        )
        axes[1].set_title("Average Delivery Transit Time by City", fontsize=13, fontweight='bold', pad=10)
        axes[1].set_xlabel("Operational City", fontsize=11, fontweight='semibold')
        axes[1].set_ylabel("Average Delivery Time (Minutes)", fontsize=11, fontweight='semibold')
        axes[1].grid(axis='y', linestyle='--', alpha=0.5)

        # Direct labels on barplot
        for p in axes[1].patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                axes[1].annotate(f"{val:.1f} m", (p.get_x() + p.get_width() / 2., val),
                                ha='center', va='bottom', fontsize=10, fontweight='bold',
                                xytext=(0, 3), textcoords='offset points')

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"\n[CHARTS CREATED] Side-by-side analytical subplots saved successfully to:")
        print(f"                 '{os.path.abspath(save_path)}'")

    # =========================================================================
    # OPTION 4: EXPORT REPORT TO MULTI-SHEET EXCEL
    # =========================================================================
    def export_report(self):
        print("\n" + "=" * 78)
        print("                 [OPTION 4] EXPORT REPORT TO MULTI-SHEET EXCEL")
        print("=" * 78)

        # Ensure required dataframes are populated
        if self.cleaned_df is None:
            self.load_and_clean_data()
        if self.sql_category_summary is None or self.sql_restaurant_summary is None:
            self.run_sql_analysis()

        # Export using pandas.ExcelWriter as specified
        with pd.ExcelWriter(self.excel_path, engine="openpyxl") as writer:
            self.cleaned_df.to_excel(writer, sheet_name="Cleaned_Orders", index=False)
            self.sql_category_summary.to_excel(writer, sheet_name="Category_Summary", index=False)
            self.sql_restaurant_summary.to_excel(writer, sheet_name="Restaurant_Performance", index=False)

        abs_path = os.path.abspath(self.excel_path)
        print(f"\n[EXPORT COMPLETE] Comprehensive multi-sheet Excel report generated successfully!")
        print(f"  Target File : {abs_path}")
        print(f"  Sheets Saved: [1] 'Cleaned_Orders' ({len(self.cleaned_df)} rows)")
        print(f"                [2] 'Category_Summary' ({len(self.sql_category_summary)} rows)")
        print(f"                [3] 'Restaurant_Performance' ({len(self.sql_restaurant_summary)} rows)")

    # =========================================================================
    # MENU LOOP CONTROLLER
    # =========================================================================
    def run_menu(self):
        while True:
            print("\n" + "#" * 60)
            print("        FOOD DELIVERY ANALYTICS CONSOLE APPLICATION")
            print("#" * 60)
            print("  [1] Load & Clean Data (Pandas Pipeline)")
            print("  [2] Run SQL Analysis (SQLite Aggregations & Joins)")
            print("  [3] View Charts (Seaborn Side-by-Side Visualisation)")
            print("  [4] Export Report (Multi-Sheet Excel Workbook)")
            print("  [0] Exit")
            print("#" * 60)

            choice = input("Enter your option (0-4): ").strip()

            if choice == "1":
                self.load_and_clean_data()
            elif choice == "2":
                self.run_sql_analysis()
            elif choice == "3":
                self.view_charts()
            elif choice == "4":
                self.export_report()
            elif choice == "0":
                print("\n[EXIT] Exiting Food Delivery Analytics Console Application. Goodbye!\n")
                break
            else:
                print(f"[INVALID INPUT] Choice '{choice}' is not recognized. Please choose 1, 2, 3, 4, or 0.")

if __name__ == "__main__":
    app = FoodDeliveryAnalyticsApp()
    # Check if run non-interactively or with arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("[DEMO MODE] Executing all 4 application workflows autonomously...")
        app.load_and_clean_data()
        app.run_sql_analysis()
        app.view_charts()
        app.export_report()
        print("\n[DEMO COMPLETE] All features executed without error.")
    else:
        app.run_menu()
