"""
Automated Verification Runner for Session 17: SQL Project - HR Analysis
(Restaurant & Reviews Analytics)
Verifies Tasks 1 to 5 and creates restaurant_analytics.db.
"""

import os
import sqlite3
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "restaurant_analytics.db")

    print("=" * 75)
    print("SESSION 17: SQL Project - HR Analysis (Automated Verification)")
    print(f"SQLite Version: {sqlite3.sqlite_version}")
    print(f"Pandas Version: {pd.__version__}")
    print("=" * 75)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # -------------------------------------------------------------------------
    # TASK 1: Create 'Restaurant' Table & Insert at least 5 sample rows
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Creating 'Restaurant' table & inserting sample rows ---")
    cursor.execute("DROP TABLE IF EXISTS Review;")
    cursor.execute("DROP TABLE IF EXISTS Restaurant;")
    cursor.execute("""
        CREATE TABLE Restaurant (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            location TEXT NOT NULL,
            average_rating DECIMAL(3, 2) NOT NULL
        );
    """)

    restaurants_data = [
        (1, "Punjab Grill", "North Indian", "Connaught Place", 4.50),
        (2, "Dhaba Estd 1986", "North Indian", "Cyber Hub", 4.30),
        (3, "Gulati", "North Indian", "Pandara Road", 4.70),
        (4, "Little Italy", "Italian", "Indiranagar", 4.40),
        (5, "Toscano", "Italian", "UB City", 4.60),
        (6, "Behrouz Biryani", "Mughlai", "Koramangala", 4.20),
        (7, "Biryani By Kilo", "Mughlai", "HSR Layout", 4.50)
    ]

    cursor.executemany(
        "INSERT INTO Restaurant (id, name, cuisine, location, average_rating) VALUES (?, ?, ?, ?, ?);",
        restaurants_data
    )
    conn.commit()

    df_restaurants = pd.read_sql_query("SELECT * FROM Restaurant;", conn)
    print(f"[OK] Populated 'Restaurant' table with {len(df_restaurants)} records.")
    print(df_restaurants.to_string(index=False))
    assert len(df_restaurants) >= 5, "Restaurant table must have at least 5 records."

    # -------------------------------------------------------------------------
    # TASK 2: Report showing number of restaurants per cuisine type
    # -------------------------------------------------------------------------
    print("\n--- TASK 2: Number of restaurants for each cuisine type ---")
    query_task2 = """
    SELECT 
        cuisine,
        COUNT(id) AS restaurant_count
    FROM Restaurant
    GROUP BY cuisine
    ORDER BY restaurant_count DESC, cuisine ASC;
    """
    df_cuisine_counts = pd.read_sql_query(query_task2, conn)
    print(df_cuisine_counts.to_string(index=False))

    assert df_cuisine_counts.iloc[0]["cuisine"] == "North Indian"
    assert df_cuisine_counts.iloc[0]["restaurant_count"] == 3
    assert df_cuisine_counts["restaurant_count"].is_monotonic_decreasing
    print("[OK] Task 2 passed: Grouped by cuisine and sorted descending.")

    # -------------------------------------------------------------------------
    # TASK 3: Add 'Review' table & insert at least 10 sample reviews
    # -------------------------------------------------------------------------
    print("\n--- TASK 3: Creating 'Review' table & inserting sample reviews ---")
    cursor.execute("""
        CREATE TABLE Review (
            id INTEGER PRIMARY KEY,
            restaurant_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            rating DECIMAL(3, 2) NOT NULL,
            review_date DATE NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
        );
    """)

    reviews_data = [
        (1,  3, "Aarav Sharma",   5.00, "2026-03-01"),
        (2,  3, "Diya Kapoor",    4.80, "2026-03-05"),
        (3,  5, "Rohan Verma",    4.80, "2026-03-02"),
        (4,  5, "Meera Nair",     4.60, "2026-03-06"),
        (5,  1, "Kabir Mehta",    4.50, "2026-03-03"),
        (6,  1, "Ananya Sen",     4.70, "2026-03-07"),
        (7,  7, "Siddharth Rao",  4.60, "2026-03-04"),
        (8,  7, "Pooja Hegde",    4.40, "2026-03-08"),
        (9,  4, "Vikram Singhal", 4.40, "2026-03-02"),
        (10, 4, "Ishaan Goel",    4.20, "2026-03-09"),
        (11, 2, "Neha Gupta",     4.20, "2026-03-01"),
        (12, 2, "Kunal Roy",      4.40, "2026-03-10"),
        (13, 6, "Tanvi Joshi",    4.10, "2026-03-04"),
        (14, 6, "Aditya Malik",   4.30, "2026-03-11")
    ]

    cursor.executemany(
        "INSERT INTO Review (id, restaurant_id, user_name, rating, review_date) VALUES (?, ?, ?, ?, ?);",
        reviews_data
    )
    conn.commit()

    df_reviews = pd.read_sql_query("SELECT * FROM Review;", conn)
    print(f"[OK] Populated 'Review' table with {len(df_reviews)} sample reviews.")
    assert len(df_reviews) >= 10, "Review table must contain at least 10 sample reviews."

    # -------------------------------------------------------------------------
    # TASK 4: JOIN query for restaurant's name, cuisine, and average review rating
    # -------------------------------------------------------------------------
    print("\n--- TASK 4: Average review rating per restaurant (JOIN & GROUP BY) ---")
    query_task4 = """
    SELECT 
        r.name,
        r.cuisine,
        ROUND(AVG(rev.rating), 2) AS avg_review_rating
    FROM Restaurant r
    INNER JOIN Review rev ON r.id = rev.restaurant_id
    GROUP BY r.id, r.name, r.cuisine
    ORDER BY avg_review_rating DESC, r.name ASC;
    """
    df_avg_ratings = pd.read_sql_query(query_task4, conn)
    print(df_avg_ratings.to_string(index=False))

    assert len(df_avg_ratings) == 7, f"Expected 7 restaurants, got {len(df_avg_ratings)}"
    assert df_avg_ratings.iloc[0]["name"] == "Gulati"
    assert df_avg_ratings.iloc[0]["avg_review_rating"] == 4.90
    assert df_avg_ratings["avg_review_rating"].is_monotonic_decreasing
    print("[OK] Task 4 passed: Correctly computed average review ratings ordered descending.")

    # -------------------------------------------------------------------------
    # TASK 5: Rank restaurants by average review rating within each cuisine
    # -------------------------------------------------------------------------
    print("\n--- TASK 5: Window function ranking within each cuisine type ---")
    query_task5 = """
    WITH RestaurantAverages AS (
        SELECT 
            r.name,
            r.cuisine,
            ROUND(AVG(rev.rating), 2) AS average_rating
        FROM Restaurant r
        INNER JOIN Review rev ON r.id = rev.restaurant_id
        GROUP BY r.id, r.name, r.cuisine
    )
    SELECT 
        name,
        cuisine,
        average_rating,
        DENSE_RANK() OVER (
            PARTITION BY cuisine 
            ORDER BY average_rating DESC
        ) AS rank
    FROM RestaurantAverages
    ORDER BY cuisine ASC, rank ASC;
    """
    df_ranked = pd.read_sql_query(query_task5, conn)
    print(df_ranked.to_string(index=False))

    # Assertions
    # Italian
    italian_top = df_ranked[(df_ranked["cuisine"] == "Italian") & (df_ranked["rank"] == 1)].iloc[0]
    assert italian_top["name"] == "Toscano" and italian_top["average_rating"] == 4.70

    # Mughlai
    mughlai_top = df_ranked[(df_ranked["cuisine"] == "Mughlai") & (df_ranked["rank"] == 1)].iloc[0]
    assert mughlai_top["name"] == "Biryani By Kilo" and mughlai_top["average_rating"] == 4.50

    # North Indian
    north_indian_top = df_ranked[(df_ranked["cuisine"] == "North Indian") & (df_ranked["rank"] == 1)].iloc[0]
    assert north_indian_top["name"] == "Gulati" and north_indian_top["average_rating"] == 4.90

    print("[OK] Task 5 passed: Window function partitioned by cuisine accurately ranked restaurants.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 17 tasks verified successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
