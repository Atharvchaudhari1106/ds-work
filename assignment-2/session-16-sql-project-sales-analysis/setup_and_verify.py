"""
Automated Verification Runner for Session 16: SQL Project - Sales Analysis
Verifies Tasks 1 to 5, creates sales_analysis.db, and validates all results.
"""

import os
import sqlite3
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "food_orders.csv")
    db_path = os.path.join(base_dir, "sales_analysis.db")

    print("=" * 75)
    print("SESSION 16: SQL Project - Sales Analysis (Automated Verification)")
    print(f"SQLite Version: {sqlite3.sqlite_version}")
    print(f"Pandas Version: {pd.__version__}")
    print("=" * 75)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # -------------------------------------------------------------------------
    # TASK 1: Import CSV into SQL table 'FoodOrders'
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Ingesting 'food_orders.csv' into 'FoodOrders' table ---")
    cursor.execute("DROP TABLE IF EXISTS FoodOrders;")
    cursor.execute("""
        CREATE TABLE FoodOrders (
            order_id INTEGER PRIMARY KEY,
            restaurant_name TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            order_amount DECIMAL(10, 2) NOT NULL,
            order_date DATE NOT NULL
        );
    """)

    df_csv = pd.read_csv(csv_path)
    df_csv.to_sql("FoodOrders", conn, if_exists="append", index=False)
    conn.commit()

    df_check = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM FoodOrders;", conn)
    total_imported = df_check["total_rows"].iloc[0]
    print(f"[OK] Successfully imported {total_imported} orders into 'FoodOrders' table.")
    assert total_imported == 19, f"Expected 19 records, got {total_imported}"

    # Preview first 5 rows
    df_preview = pd.read_sql_query("SELECT * FROM FoodOrders LIMIT 5;", conn)
    print("\nFirst 5 imported records:")
    print(df_preview.to_string(index=False))

    # -------------------------------------------------------------------------
    # TASK 2: Create 'TopSongs' table & insert at least 5 Spotify records
    # -------------------------------------------------------------------------
    print("\n--- TASK 2: Creating 'TopSongs' table & inserting Spotify records ---")
    cursor.execute("DROP TABLE IF EXISTS TopSongs;")
    cursor.execute("""
        CREATE TABLE TopSongs (
            song_id INTEGER PRIMARY KEY,
            song_title TEXT NOT NULL,
            artist TEXT NOT NULL,
            streams BIGINT NOT NULL,
            release_date DATE NOT NULL
        );
    """)

    spotify_tracks = [
        (1, "Blinding Lights", "The Weeknd", 4200000000, "2019-11-29"),
        (2, "Shape of You", "Ed Sheeran", 3800000000, "2017-01-06"),
        (3, "Someone You Loved", "Lewis Capaldi", 3300000000, "2018-11-08"),
        (4, "Sunflower", "Post Malone & Swae Lee", 3200000000, "2018-10-19"),
        (5, "As It Was", "Harry Styles", 3100000000, "2022-04-01")
    ]

    cursor.executemany(
        "INSERT INTO TopSongs (song_id, song_title, artist, streams, release_date) VALUES (?, ?, ?, ?, ?);",
        spotify_tracks
    )
    conn.commit()

    df_songs = pd.read_sql_query("SELECT * FROM TopSongs ORDER BY streams DESC;", conn)
    print(f"[OK] Inserted {len(df_songs)} Spotify tracks into 'TopSongs'.")
    print(df_songs.to_string(index=False))
    assert len(df_songs) >= 5, "TopSongs must have at least 5 records."

    # -------------------------------------------------------------------------
    # TASK 3: Top 3 Customers by Total order_amount
    # -------------------------------------------------------------------------
    print("\n--- TASK 3: Finding Top 3 Customers by Total Spend ---")
    query_task3 = """
    SELECT 
        customer_name,
        ROUND(SUM(order_amount), 2) AS total_spent
    FROM FoodOrders
    GROUP BY customer_name
    ORDER BY total_spent DESC
    LIMIT 3;
    """
    df_top_customers = pd.read_sql_query(query_task3, conn)
    print(df_top_customers.to_string(index=False))

    assert len(df_top_customers) == 3, f"Expected 3 rows, got {len(df_top_customers)}"
    assert df_top_customers.iloc[0]["customer_name"] == "Sneha Reddy"
    assert df_top_customers.iloc[0]["total_spent"] == 2600.00
    assert df_top_customers.iloc[1]["customer_name"] == "Priya Patel"
    assert df_top_customers.iloc[1]["total_spent"] == 2150.00
    assert df_top_customers.iloc[2]["customer_name"] == "Rohan Gupta"
    assert df_top_customers.iloc[2]["total_spent"] == 1950.00
    print("[OK] Task 3 passed: Correct top 3 customers identified with exact spend amounts.")

    # -------------------------------------------------------------------------
    # TASK 4: Product / Restaurant Performance Report
    # -------------------------------------------------------------------------
    print("\n--- TASK 4: Restaurant Performance Report (Orders & Spend) ---")
    query_task4 = """
    SELECT 
        restaurant_name,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(order_amount), 2) AS total_order_amount
    FROM FoodOrders
    GROUP BY restaurant_name
    ORDER BY total_order_amount DESC;
    """
    df_performance = pd.read_sql_query(query_task4, conn)
    print(df_performance.to_string(index=False))

    assert df_performance.iloc[0]["restaurant_name"] == "Behrouz Biryani"
    assert df_performance.iloc[0]["total_orders"] == 4
    assert df_performance.iloc[0]["total_order_amount"] == 3700.00
    assert df_performance["total_order_amount"].is_monotonic_decreasing
    print("[OK] Task 4 passed: Performance report correctly grouped and ordered descending.")

    # -------------------------------------------------------------------------
    # TASK 5: Executive Dashboard KPIs (kpi_name, kpi_value)
    # -------------------------------------------------------------------------
    print("\n--- TASK 5: Executive Dashboard KPIs ---")
    query_task5 = """
    SELECT 
        'Average Order Amount' AS kpi_name,
        CAST(ROUND(AVG(order_amount), 2) AS TEXT) AS kpi_value
    FROM FoodOrders

    UNION ALL

    SELECT 
        'Total Unique Customers' AS kpi_name,
        CAST(COUNT(DISTINCT customer_name) AS TEXT) AS kpi_value
    FROM FoodOrders;
    """
    df_kpis = pd.read_sql_query(query_task5, conn)
    print(df_kpis.to_string(index=False))

    assert len(df_kpis) == 2, f"Expected 2 KPI rows, got {len(df_kpis)}"
    assert list(df_kpis.columns) == ["kpi_name", "kpi_value"]
    assert df_kpis.iloc[0]["kpi_name"] == "Average Order Amount"
    assert float(df_kpis.iloc[0]["kpi_value"]) == 590.53
    assert df_kpis.iloc[1]["kpi_name"] == "Total Unique Customers"
    assert int(df_kpis.iloc[1]["kpi_value"]) == 7
    print("[OK] Task 5 passed: Executive KPI dashboard formatted into two columns successfully.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 16 tasks verified successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
