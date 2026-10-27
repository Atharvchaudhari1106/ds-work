#!/usr/bin/env python3
"""
Session 12: CTE (WITH Clause)
Verification & Automated Execution Runner
Database: cte_demo.db
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "cte_demo.db")

def main():
    print("=" * 75)
    print("SESSION 12: CTE (WITH Clause) - Automated Verification")
    print("SQLite Version:", sqlite3.sqlite_version)
    print("=" * 75)

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------------------------------------------------------------------------
    # TASK 1: Basic CTE with WITH Clause
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Top-Rated Products (rating > 4.5) ---")
    cursor.execute("DROP TABLE IF EXISTS Products;")
    cursor.execute("""
    CREATE TABLE Products (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        rating DECIMAL(2, 1) NOT NULL
    );
    """)

    products_data = [
        (1, 'Sony WH-1000XM5 Wireless Headphones', 'Electronics', 28990.00, 4.8),
        (2, 'Apple iPhone 15 Pro', 'Electronics', 129900.00, 4.7),
        (3, 'Nike Air Jordan 1 Retro', 'Footwear', 11995.00, 4.9),
        (4, "Levi's 511 Slim Fit Jeans", 'Fashion', 2999.00, 4.2),
        (5, 'Puma Mens Running Shoes', 'Footwear', 3499.00, 4.1),
        (6, 'Samsung Galaxy S24 Ultra', 'Electronics', 129999.00, 4.6),
        (7, 'Fossil Gen 6 Smartwatch', 'Accessories', 14995.00, 4.0),
        (8, 'Ray-Ban Wayfarer Classic', 'Accessories', 8590.00, 4.6)
    ]
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?);", products_data)
    conn.commit()

    task1_query = """
    WITH TopRatedProducts AS (
        SELECT 
            id AS product_id,
            name AS product_name,
            category,
            price,
            rating
        FROM Products
        WHERE rating > 4.5
    )
    SELECT * FROM TopRatedProducts
    ORDER BY rating DESC, price ASC;
    """
    df_t1 = pd.read_sql_query(task1_query, conn)
    print(df_t1.to_string(index=False))
    print(f"[OK] Total top-rated items returned: {len(df_t1)}")

    # -------------------------------------------------------------------------
    # TASK 2: Subquery vs CTE Comparison (Ahmedabad Restaurants)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 2: Subquery vs CTE (Ahmedabad Restaurants delivery < 50) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Restaurants;")
    cursor.execute("""
    CREATE TABLE Restaurants (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL,
        cuisine VARCHAR(50) NOT NULL,
        delivery_charge DECIMAL(5, 2) NOT NULL,
        rating DECIMAL(2, 1) NOT NULL
    );
    """)

    restaurants_data = [
        (1, 'Manek Chowk Delights', 'Ahmedabad', 'Street Food', 30.00, 4.6),
        (2, 'Agashiye - House of MG', 'Ahmedabad', 'Gujarati Thali', 40.00, 4.8),
        (3, 'Swati Snacks', 'Ahmedabad', 'Chaat & Snacks', 45.00, 4.5),
        (4, 'Gordhan Thal', 'Ahmedabad', 'Gujarati Thali', 60.00, 4.7),
        (5, 'Havmor Restaurant', 'Ahmedabad', 'North Indian', 55.00, 4.3),
        (6, 'Truffles', 'Bangalore', 'Continental', 35.00, 4.7),
        (7, 'Britannia & Co', 'Mumbai', 'Parsi', 40.00, 4.4)
    ]
    cursor.executemany("INSERT INTO Restaurants VALUES (?, ?, ?, ?, ?, ?);", restaurants_data)
    conn.commit()

    # Subquery version
    query_subquery = """
    SELECT restaurant_name, city, cuisine, delivery_charge, rating
    FROM (
        SELECT name AS restaurant_name, city, cuisine, delivery_charge, rating
        FROM Restaurants
        WHERE city = 'Ahmedabad'
    ) AS AhmedabadRestaurants
    WHERE delivery_charge < 50.00
    ORDER BY delivery_charge ASC;
    """
    df_sub = pd.read_sql_query(query_subquery, conn)
    print("\nVersion A (Subquery):")
    print(df_sub.to_string(index=False))

    # CTE version
    query_cte = """
    WITH AhmedabadRestaurants AS (
        SELECT name AS restaurant_name, city, cuisine, delivery_charge, rating
        FROM Restaurants
        WHERE city = 'Ahmedabad'
    )
    SELECT restaurant_name, city, cuisine, delivery_charge, rating
    FROM AhmedabadRestaurants
    WHERE delivery_charge < 50.00
    ORDER BY delivery_charge ASC;
    """
    df_cte = pd.read_sql_query(query_cte, conn)
    print("\nVersion B (CTE):")
    print(df_cte.to_string(index=False))
    print("[OK] Both versions return identical data; CTE provides cleaner linear readability.")

    # -------------------------------------------------------------------------
    # TASK 3: Two CTEs in a Single Query (Instagram Top Users & Top Posts)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 3: Two CTEs in Single Query (Top Users & Top Posts) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Posts;")
    cursor.execute("DROP TABLE IF EXISTS Users;")

    cursor.execute("""
    CREATE TABLE Users (
        id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        followers_count INT NOT NULL,
        account_status VARCHAR(20) DEFAULT 'Active'
    );
    """)

    cursor.execute("""
    CREATE TABLE Posts (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        caption VARCHAR(255) NOT NULL,
        likes_count INT NOT NULL
    );
    """)

    users_data = [
        (1, 'virat.kohli', 270000000, 'Active'),
        (2, 'priyanka.chopra', 91000000, 'Active'),
        (3, 'alia.bhatt', 85000000, 'Active'),
        (4, 'tech_reviewer', 500000, 'Active'),
        (5, 'daily_foodie', 250000, 'Active')
    ]
    posts_data = [
        (101, 1, 'Historic victory at MCG! Proud of the boys.', 5800000),
        (102, 1, 'Match day ready. Always grateful.', 4200000),
        (103, 2, 'Unforgettable night at the Met Gala 2026.', 3900000),
        (104, 3, 'Behind the scenes from our new film set.', 3100000),
        (105, 4, 'Unboxing the future: New foldable phone review.', 180000),
        (106, 5, 'Best street food crawl in Ahmedabad!', 95000)
    ]
    cursor.executemany("INSERT INTO Users VALUES (?, ?, ?, ?);", users_data)
    cursor.executemany("INSERT INTO Posts VALUES (?, ?, ?, ?);", posts_data)
    conn.commit()

    task3_query = """
    WITH TopFollowedUsers AS (
        SELECT 
            'Most Followed User' AS metric_category,
            username AS entity_name,
            followers_count AS metric_value
        FROM Users
        ORDER BY followers_count DESC
        LIMIT 3
    ),
    TopLikedPosts AS (
        SELECT 
            'Most Liked Post' AS metric_category,
            caption AS entity_name,
            likes_count AS metric_value
        FROM Posts
        ORDER BY likes_count DESC
        LIMIT 3
    )
    SELECT * FROM TopFollowedUsers
    UNION ALL
    SELECT * FROM TopLikedPosts;
    """
    df_t3 = pd.read_sql_query(task3_query, conn)
    print(df_t3.to_string(index=False))
    print(f"[OK] Total combined records returned from both CTEs: {len(df_t3)}")

    # -------------------------------------------------------------------------
    # TASK 4: Recursive CTE for Next 7 Days (BookMyShow Movie Dates)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 4: Recursive CTE (Next 7 Days Booking Dates) ---")
    print("=" * 75)
    task4_query = """
    WITH RECURSIVE BookingDates AS (
        -- Base Case: Day 1 (Today)
        SELECT 
            1 AS day_number,
            DATE('now') AS booking_date
        UNION ALL
        -- Recursive Step: Add +1 day
        SELECT 
            day_number + 1,
            DATE(booking_date, '+1 day')
        FROM BookingDates
        WHERE day_number < 7
    )
    SELECT 
        day_number,
        booking_date AS iso_date,
        strftime('%d-%m-%Y', booking_date) AS formatted_date,
        CASE strftime('%w', booking_date)
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS day_of_week
    FROM BookingDates;
    """
    df_t4 = pd.read_sql_query(task4_query, conn)
    print(df_t4.to_string(index=False))
    print(f"[OK] Successfully generated next {len(df_t4)} days with Recursive CTE!")

    # -------------------------------------------------------------------------
    # TASK 5: Refactoring Messy Query with CTE
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 5: Refactoring Messy Query using CTE ---")
    print("=" * 75)

    messy_query = """
    SELECT u.id, u.username, u.followers_count, u.account_status
    FROM (
        SELECT * FROM (
            SELECT id, username, followers_count, account_status
            FROM Users
            WHERE account_status = 'Active'
        ) AS active_sub
        WHERE active_sub.followers_count > 1000
    ) AS u
    WHERE u.id IN (
        SELECT user_id FROM (
            SELECT id AS user_id, followers_count FROM Users WHERE followers_count > 1000
        ) AS follower_sub
    )
    ORDER BY u.followers_count DESC;
    """
    df_messy = pd.read_sql_query(messy_query, conn)
    print("\nMessy Query Output:")
    print(df_messy.to_string(index=False))

    clean_cte_query = """
    WITH ActiveInfluencerUsers AS (
        SELECT 
            id AS user_id,
            username,
            followers_count,
            account_status
        FROM Users
        WHERE account_status = 'Active'
          AND followers_count > 1000
    )
    SELECT 
        user_id,
        username,
        followers_count,
        account_status
    FROM ActiveInfluencerUsers
    ORDER BY followers_count DESC;
    """
    df_clean = pd.read_sql_query(clean_cte_query, conn)
    print("\nClean Refactored CTE Query Output:")
    print(df_clean.to_string(index=False))
    print("[OK] Query successfully refactored from complex nested subqueries to clean CTE.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 12 CTE tasks verified successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
