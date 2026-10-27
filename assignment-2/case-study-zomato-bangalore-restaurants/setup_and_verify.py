"""
Automated Verification Runner for Case Study: Zomato Bangalore Restaurants
Validates Tasks 1 through 5 against zomato_bangalore.db.
"""

import os
import sqlite3
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "zomato_bangalore.csv")
    db_path = os.path.join(base_dir, "zomato_bangalore.db")

    print("=" * 75)
    print("CASE STUDY: Zomato Bangalore Restaurants - Kaggle (Automated Verification)")
    print(f"SQLite Version: {sqlite3.sqlite_version}")
    print(f"Pandas Version: {pd.__version__}")
    print("=" * 75)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ingestion setup
    cursor.execute("DROP TABLE IF EXISTS zomato_bangalore;")
    cursor.execute("""
        CREATE TABLE zomato_bangalore (
            restaurant_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            online_order TEXT NOT NULL,
            book_table TEXT NOT NULL,
            rating REAL NOT NULL,
            votes INTEGER NOT NULL,
            location TEXT NOT NULL,
            cuisines TEXT NOT NULL,
            approx_cost_for_two DECIMAL(10, 2) NOT NULL
        );
    """)

    df_csv = pd.read_csv(csv_path)
    df_csv.to_sql("zomato_bangalore", conn, if_exists="append", index=False)
    conn.commit()

    total_records = pd.read_sql_query("SELECT COUNT(*) AS total FROM zomato_bangalore;", conn)["total"].iloc[0]
    print(f"[OK] Ingested {total_records} restaurants into table 'zomato_bangalore'.")

    # -------------------------------------------------------------------------
    # TASK 1: Top 5 Highest-Rated North Indian Restaurants in Koramangala
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Top 5 Highest-Rated North Indian in Koramangala ---")
    query_task1 = """
    SELECT 
        name,
        location,
        cuisines,
        rating,
        votes
    FROM zomato_bangalore
    WHERE location LIKE '%Koramangala%'
      AND cuisines LIKE '%North Indian%'
    ORDER BY rating DESC, votes DESC
    LIMIT 5;
    """
    df_task1 = pd.read_sql_query(query_task1, conn)
    print(df_task1.to_string(index=False))

    assert len(df_task1) == 5, f"Expected 5 restaurants, got {len(df_task1)}"
    assert df_task1.iloc[0]["name"] == "Punjab Grill"
    assert df_task1.iloc[0]["rating"] == 4.8
    assert all("North Indian" in c for c in df_task1["cuisines"])
    assert all("Koramangala" in loc for loc in df_task1["location"])
    print("[OK] Task 1 passed: Identified top 5 North Indian restaurants in Koramangala.")

    # -------------------------------------------------------------------------
    # TASK 2: Average Cost for Two per Cuisine & Top 3 Most Expensive
    # -------------------------------------------------------------------------
    print("\n--- TASK 2: Top 3 Most Expensive Cuisines to Eat in Bangalore ---")
    query_task2 = """
    SELECT 
        cuisines AS cuisine_type,
        ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two,
        COUNT(*) AS restaurant_count
    FROM zomato_bangalore
    GROUP BY cuisines
    ORDER BY avg_cost_for_two DESC
    LIMIT 3;
    """
    df_task2 = pd.read_sql_query(query_task2, conn)
    print(df_task2.to_string(index=False))

    assert len(df_task2) == 3, f"Expected 3 cuisines, got {len(df_task2)}"
    assert df_task2.iloc[0]["cuisine_type"] == "Mediterranean"
    assert df_task2.iloc[0]["avg_cost_for_two"] >= 2000.0
    print("[OK] Task 2 passed: Top 3 most expensive cuisines computed correctly.")

    # -------------------------------------------------------------------------
    # TASK 3: Online Delivery with Rating Below 3.0
    # -------------------------------------------------------------------------
    print("\n--- TASK 3: Online Delivery Restaurants with Rating Below 3.0 ---")
    query_task3 = """
    SELECT 
        restaurant_id,
        name,
        location,
        cuisines,
        approx_cost_for_two,
        rating,
        votes,
        online_order
    FROM zomato_bangalore
    WHERE online_order = 'Yes'
      AND rating < 3.0
    ORDER BY rating ASC;
    """
    df_task3 = pd.read_sql_query(query_task3, conn)
    print(df_task3.to_string(index=False))

    assert len(df_task3) > 0, "Expected low-rated delivery restaurants to audit."
    assert all(df_task3["online_order"] == "Yes"), "All must offer online order."
    assert all(df_task3["rating"] < 3.0), "All ratings must be below 3.0."
    print(f"[OK] Task 3 passed: Identified {len(df_task3)} low-rated online delivery restaurants for turnaround strategy.")

    # -------------------------------------------------------------------------
    # TASK 4: Three-Tier Market Segmentation (Budget, Mid-Range, Premium)
    # -------------------------------------------------------------------------
    print("\n--- TASK 4: Restaurant Count by Market Segment ---")
    query_task4 = """
    SELECT 
        CASE 
            WHEN approx_cost_for_two < 400 THEN 'Budget (Below 400)'
            WHEN approx_cost_for_two BETWEEN 400 AND 800 THEN 'Mid-Range (400 - 800)'
            ELSE 'Premium (Above 800)'
        END AS market_segment,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(approx_cost_for_two), 2) AS avg_segment_cost,
        ROUND(AVG(rating), 2) AS avg_rating
    FROM zomato_bangalore
    GROUP BY market_segment
    ORDER BY 
        CASE market_segment
            WHEN 'Budget (Below 400)' THEN 1
            WHEN 'Mid-Range (400 - 800)' THEN 2
            WHEN 'Premium (Above 800)' THEN 3
        END;
    """
    df_task4 = pd.read_sql_query(query_task4, conn)
    print(df_task4.to_string(index=False))

    assert len(df_task4) == 3, f"Expected 3 market segments, got {len(df_task4)}"
    assert sum(df_task4["restaurant_count"]) == total_records
    print("[OK] Task 4 passed: Correctly segmented restaurants across Budget, Mid-Range, and Premium.")

    # -------------------------------------------------------------------------
    # TASK 5: Top 10 Most Popular Chains by Outlet Count
    # -------------------------------------------------------------------------
    print("\n--- TASK 5: Top 10 Most Popular Chains by Number of Outlets ---")
    query_task5 = """
    SELECT 
        name AS chain_name,
        COUNT(*) AS outlet_count,
        ROUND(AVG(rating), 2) AS avg_chain_rating,
        ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two
    FROM zomato_bangalore
    GROUP BY name
    ORDER BY outlet_count DESC, avg_chain_rating DESC
    LIMIT 10;
    """
    df_task5 = pd.read_sql_query(query_task5, conn)
    print(df_task5.to_string(index=False))

    assert len(df_task5) == 10, f"Expected 10 chains, got {len(df_task5)}"
    assert df_task5.iloc[0]["chain_name"] == "Cafe Coffee Day"
    assert df_task5.iloc[0]["outlet_count"] == 8
    print("[OK] Task 5 passed: Top 10 chains ranked by outlet volume successfully.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Case Study tasks verified successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
