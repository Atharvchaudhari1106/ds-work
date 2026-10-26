"""
Task 4: SQL + Python Restaurant Performance Report
Assessment: M4-A1 | Program: Data Science
Domain: Relational Database Modeling, SQL Aggregation, Ranking & CSV Export
"""

import sqlite3
import os
import pandas as pd
from tabulate import tabulate

DB_FILE = "food_delivery.db"
CSV_EXPORT_FILE = "restaurant_performance_report.csv"

def init_and_populate_database(db_path: str = DB_FILE):
    """Creates SQLite database schema and inserts seed data for restaurants and orders."""
    # Remove existing db file if present to guarantee clean repeatable runs
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create tables as specified in assessment requirements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        restaurant_id INTEGER NOT NULL,
        order_value REAL NOT NULL,
        delivery_time_mins REAL NOT NULL,
        rating REAL NOT NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
    );
    """)

    # 2. Insert at least 8 restaurants (inserting 9 restaurants across multiple cities)
    restaurants_data = [
        (1, "Spice Symphony",   "Indian",       "Mumbai"),
        (2, "Pizza Roma",       "Italian",      "Bengaluru"),
        (3, "Burger Garage",    "Burgers",      "Delhi"),
        (4, "Dragon Wok",       "Chinese",      "Mumbai"),
        (5, "Taco Fiesta",      "Mexican",      "Pune"),
        (6, "Curry House",      "Indian",       "Delhi"),
        (7, "Sushi Bay",        "Japanese",     "Bengaluru"),
        (8, "Pasta Bella",      "Italian",      "Pune"),
        (9, "The Green Bowl",   "Healthy/Salad","Mumbai")  # Zero orders edge-case testing
    ]
    cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?, ?);", restaurants_data)

    # 3. Insert at least 25 orders (inserting 28 realistic orders)
    orders_data = [
        # (order_id, restaurant_id, order_value, delivery_time_mins, rating)
        (1001, 1, 650.0, 32.0, 4.8),
        (1002, 1, 820.0, 35.0, 4.6),
        (1003, 1, 540.0, 28.0, 4.7),
        (1004, 1, 950.0, 40.0, 4.9),
        (1005, 2, 720.0, 29.0, 4.3),
        (1006, 2, 610.0, 31.0, 4.1),
        (1007, 2, 850.0, 34.0, 4.5),
        (1008, 3, 320.0, 24.0, 3.9),
        (1009, 3, 410.0, 22.0, 3.8),
        (1010, 3, 290.0, 26.0, 4.0),
        (1011, 4, 780.0, 38.0, 4.2),
        (1012, 4, 690.0, 36.0, 4.4),
        (1013, 4, 840.0, 41.0, 4.3),
        (1014, 4, 590.0, 33.0, 4.1),
        (1015, 5, 480.0, 25.0, 4.2),
        (1016, 5, 520.0, 27.0, 4.0),
        (1017, 5, 610.0, 30.0, 4.3),
        (1018, 6, 890.0, 42.0, 4.5),
        (1019, 6, 1050.0, 45.0, 4.6),
        (1020, 6, 740.0, 39.0, 4.4),
        (1021, 7, 1250.0, 50.0, 4.8),
        (1022, 7, 1400.0, 52.0, 4.9),
        (1023, 7, 980.0, 46.0, 4.7),
        (1024, 7, 1150.0, 48.0, 4.8),
        (1025, 8, 510.0, 28.0, 4.1),
        (1026, 8, 630.0, 32.0, 4.3),
        (1027, 8, 580.0, 30.0, 4.2),
        (1028, 2, 790.0, 33.0, 4.4)
    ]
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?);", orders_data)

    conn.commit()
    conn.close()
    print(f"[DATABASE INITIALIZED] Created '{db_path}' with {len(restaurants_data)} restaurants and {len(orders_data)} orders.")

def generate_restaurant_performance_report(db_path: str = DB_FILE, export_path: str = CSV_EXPORT_FILE):
    print("=" * 75)
    print("       TASK 4: SQL + PYTHON RESTAURANT PERFORMANCE REPORT")
    print("=" * 75)

    conn = sqlite3.connect(db_path)

    # SQL query using GROUP BY with COUNT(), SUM(), ROUND(AVG(), 2)
    # Using LEFT JOIN to ensure all restaurants (including zero orders) are captured
    query = """
    SELECT 
        r.restaurant_id,
        r.name AS restaurant_name,
        r.category,
        r.city,
        COUNT(o.order_id) AS total_orders,
        ROUND(COALESCE(SUM(o.order_value), 0.0), 2) AS total_revenue,
        ROUND(COALESCE(AVG(o.rating), 0.0), 2) AS avg_rating
    FROM restaurants r
    LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
    GROUP BY r.restaurant_id, r.name, r.category, r.city;
    """

    # Load result into Pandas DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Add rank column as explicitly specified:
    # df['revenue_rank'] = df['total_revenue'].rank(ascending=False, method='min').astype(int)
    df['revenue_rank'] = df['total_revenue'].rank(ascending=False, method='min').astype(int)

    # Sort by rank ascending
    df = df.sort_values(by='revenue_rank', ascending=True).reset_index(drop=True)

    print("\n--- [Full Ranked Restaurant Performance Table] ---")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

    # Print Top 5 restaurants by total revenue in a formatted table
    top5_df = df.head(5).copy()
    print("\n" + "=" * 75)
    print("              TOP 5 RESTAURANTS BY TOTAL REVENUE")
    print("=" * 75)
    print(tabulate(top5_df[['revenue_rank', 'restaurant_name', 'category', 'city', 'total_orders', 'total_revenue', 'avg_rating']], 
                   headers=['Rank', 'Restaurant', 'Category', 'City', 'Orders', 'Total Revenue (INR)', 'Avg Rating'], 
                   tablefmt="psql", 
                   showindex=False))

    # Export complete report to CSV using df.to_csv() with index=False
    df.to_csv(export_path, index=False)
    print(f"\n[EXPORT CONFIRMED] Complete performance report exported successfully to:")
    print(f"                  '{os.path.abspath(export_path)}'")
    print(f"                  Total Rows Exported: {len(df)}")
    print("=" * 75)

if __name__ == "__main__":
    init_and_populate_database(DB_FILE)
    generate_restaurant_performance_report(DB_FILE, CSV_EXPORT_FILE)
