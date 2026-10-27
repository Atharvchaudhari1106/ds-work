#!/usr/bin/env python3
"""
Session 10: JOINS - Part 2
Automated Execution & Verification Script
Database: joins_part2.db
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "joins_part2.db")

def main():
    print("=" * 75)
    print("SESSION 10: JOINS - Part 2 (Verification Script)")
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
    # TASK 1: FULL JOIN (Influencers & Collaborations)
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Influencers & Collaborations (FULL JOIN) ---")
    cursor.execute("DROP TABLE IF EXISTS Collaborations;")
    cursor.execute("DROP TABLE IF EXISTS Influencers;")

    cursor.execute("""
    CREATE TABLE Influencers (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Collaborations (
        id INT PRIMARY KEY,
        influencer1_id INT,
        influencer2_id INT,
        collab_date DATE NOT NULL
    );
    """)

    influencers_data = [
        (1, 'Virat Kohli'),
        (2, 'Anushka Sharma'),
        (3, 'CarryMinati'),
        (4, 'Bhuvan Bam'),
        (5, 'Technical Guruji'),  # Solo creator (No collaborations)
        (6, 'Prajakta Koli')       # Solo creator (No collaborations)
    ]
    cursor.executemany("INSERT INTO Influencers VALUES (?, ?);", influencers_data)

    collaborations_data = [
        (101, 1, 2, '2026-01-15'),  # Virat & Anushka
        (102, 3, 4, '2026-02-10'),  # CarryMinati & Bhuvan Bam
        (103, 1, 3, '2026-03-01'),  # Virat & CarryMinati
        (104, 99, 100, '2026-04-05') # Unlinked collaboration
    ]
    cursor.executemany("INSERT INTO Collaborations VALUES (?, ?, ?, ?);", collaborations_data)
    conn.commit()

    print("[OK] Influencers and Collaborations tables populated.")
    
    # Query: FULL JOIN
    task1_query = """
    SELECT 
        i1.id AS influencer_id,
        i1.name AS influencer_name,
        c.id AS collab_id,
        c.collab_date,
        i2.name AS partner_name
    FROM Influencers i1
    FULL JOIN Collaborations c ON i1.id = c.influencer1_id
    LEFT JOIN Influencers i2 ON c.influencer2_id = i2.id;
    """
    df_t1 = pd.read_sql_query(task1_query, conn)
    print("\nFULL JOIN Query Output:")
    print(df_t1.to_string(index=False))
    print(f"[OK] Total rows returned in FULL JOIN: {len(df_t1)}")

    # -------------------------------------------------------------------------
    # TASK 2: SELF JOIN (Spotify Nested Playlists)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 2: Playlists Table (SELF JOIN for Nested Playlists) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Playlists;")

    cursor.execute("""
    CREATE TABLE Playlists (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        playlist_name VARCHAR(100) NOT NULL,
        parent_playlist_id INT
    );
    """)

    playlists_data = [
        (1, 101, 'Top Hits 2026', None),             # Root
        (2, 101, 'Workout Motivation', None),         # Root Folder
        (3, 101, 'High Intensity Cardio', 2),         # Nested Child of 2
        (4, 101, 'Heavy Weightlifting', 2),           # Nested Child of 2
        (5, 102, 'Chill & Acoustic', None),           # Root Folder
        (6, 102, 'Sunday Morning Coffee', 5),         # Nested Child of 5
        (7, 102, 'Rainy Day Acoustic', 5)             # Nested Child of 5
    ]
    cursor.executemany("INSERT INTO Playlists VALUES (?, ?, ?, ?);", playlists_data)
    conn.commit()

    task2_query = """
    SELECT 
        child.id AS playlist_id,
        child.playlist_name,
        child.parent_playlist_id,
        COALESCE(parent.playlist_name, 'None (Root Playlist)') AS parent_playlist_name
    FROM Playlists child
    LEFT JOIN Playlists parent ON child.parent_playlist_id = parent.id;
    """
    df_t2 = pd.read_sql_query(task2_query, conn)
    print("\nSELF JOIN Query Output (All Playlists):")
    print(df_t2.to_string(index=False))

    task2_nested_only = """
    SELECT 
        child.id AS child_id,
        child.playlist_name AS nested_playlist,
        parent.playlist_name AS parent_folder
    FROM Playlists child
    INNER JOIN Playlists parent ON child.parent_playlist_id = parent.id;
    """
    df_t2_nested = pd.read_sql_query(task2_nested_only, conn)
    print("\nNested Playlists Only (INNER SELF JOIN):")
    print(df_t2_nested.to_string(index=False))

    # -------------------------------------------------------------------------
    # TASK 3: Multiple JOINs (Users -> Orders -> Payments)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 3: Multiple JOINs across 3 Tables (Users, Orders, Payments) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Payments;")
    cursor.execute("DROP TABLE IF EXISTS Orders;")
    cursor.execute("DROP TABLE IF EXISTS Users;")

    cursor.execute("""
    CREATE TABLE Users (
        id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Orders (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        order_date DATE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Payments (
        id INT PRIMARY KEY,
        order_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL
    );
    """)

    users_data = [(1, 'atharv_c'), (2, 'sneha_p'), (3, 'rahul_v'), (4, 'priya_m')]
    orders_data = [(101, 1, '2026-03-01'), (102, 2, '2026-03-05'), (103, 2, '2026-03-10'), (104, 3, '2026-03-12')]
    payments_data = [(1001, 101, 750.00), (1002, 102, 1200.00), (1003, 103, 350.00)]

    cursor.executemany("INSERT INTO Users VALUES (?, ?);", users_data)
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?);", orders_data)
    cursor.executemany("INSERT INTO Payments VALUES (?, ?, ?);", payments_data)
    conn.commit()

    task3_query = """
    SELECT 
        u.id AS user_id,
        u.username,
        o.id AS order_id,
        o.order_date,
        p.id AS payment_id,
        p.amount
    FROM Users u
    LEFT JOIN Orders o ON u.id = o.user_id
    LEFT JOIN Payments p ON o.id = p.order_id;
    """
    df_t3 = pd.read_sql_query(task3_query, conn)
    print("\nMultiple LEFT JOIN Output (Showing all users even with 0 orders/payments):")
    print(df_t3.to_string(index=False))
    print(f"[OK] Notice 'priya_m' has NULL order and payment, and 'rahul_v' has order but NULL payment.")

    # -------------------------------------------------------------------------
    # TASK 4: Eliminating Duplicates (Restaurants & Reviews)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 4: Eliminating Duplicates (Restaurants & Reviews) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Reviews;")
    cursor.execute("DROP TABLE IF EXISTS Restaurants;")

    cursor.execute("""
    CREATE TABLE Restaurants (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Reviews (
        id INT PRIMARY KEY,
        restaurant_id INT NOT NULL,
        user_name VARCHAR(50) NOT NULL,
        rating DECIMAL(2, 1) NOT NULL,
        review_text VARCHAR(255)
    );
    """)

    restaurants_data = [
        (1, 'Truffles', 'Bangalore'),
        (2, 'Peter Cat', 'Kolkata'),
        (3, 'Haldiram', 'Nagpur'),
        (4, 'Barbeque Nation', 'Mumbai')
    ]
    reviews_data = [
        (1, 1, 'Amit', 4.5, 'Amazing burgers!'),
        (2, 1, 'Rohit', 4.8, 'Best peri peri fries.'),
        (3, 1, 'Pooja', 4.2, 'Great ambience.'),
        (4, 2, 'Sagnik', 4.9, 'Chelo Kebab is legendary.'),
        (5, 2, 'Debolina', 4.7, 'Classic Kolkata nostalgia.'),
        (6, 3, 'Tanmay', 4.0, 'Nice chole bhature.')
    ]
    cursor.executemany("INSERT INTO Restaurants VALUES (?, ?, ?);", restaurants_data)
    cursor.executemany("INSERT INTO Reviews VALUES (?, ?, ?, ?, ?);", reviews_data)
    conn.commit()

    # Query with Duplicates
    df_dup = pd.read_sql_query("""
    SELECT r.id AS restaurant_id, r.name AS restaurant_name, r.city 
    FROM Restaurants r 
    INNER JOIN Reviews rev ON r.id = rev.restaurant_id;
    """, conn)
    print("\nBefore (Duplicate rows for Truffles and Peter Cat):")
    print(df_dup.to_string(index=False))

    # Solution 1: DISTINCT
    df_distinct = pd.read_sql_query("""
    SELECT DISTINCT r.id AS restaurant_id, r.name AS restaurant_name, r.city 
    FROM Restaurants r 
    INNER JOIN Reviews rev ON r.id = rev.restaurant_id;
    """, conn)
    print("\nAfter Solution 1 (DISTINCT - Unique Restaurants):")
    print(df_distinct.to_string(index=False))

    # Solution 2: GROUP BY
    df_groupby = pd.read_sql_query("""
    SELECT 
        r.id AS restaurant_id,
        r.name AS restaurant_name,
        r.city,
        COUNT(rev.id) AS total_reviews,
        ROUND(AVG(rev.rating), 2) AS avg_rating
    FROM Restaurants r
    LEFT JOIN Reviews rev ON r.id = rev.restaurant_id
    GROUP BY r.id, r.name, r.city;
    """, conn)
    print("\nAfter Solution 2 (GROUP BY - Analytics Summary):")
    print(df_groupby.to_string(index=False))

    # -------------------------------------------------------------------------
    # TASK 5: Products & Categories (Flipkart Model - Join Conditions)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 5: Comparing Two Join Conditions (Products & Categories) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Products;")
    cursor.execute("DROP TABLE IF EXISTS Categories;")

    cursor.execute("""
    CREATE TABLE Categories (
        category_id INT PRIMARY KEY,
        category_code VARCHAR(20) UNIQUE NOT NULL,
        category_name VARCHAR(100) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        category_id INT,
        category_code VARCHAR(20)
    );
    """)

    categories_data = [
        (1, 'ELEC', 'Electronics'),
        (2, 'FASH', 'Fashion & Apparel'),
        (3, 'HOME', 'Home & Kitchen')
    ]
    products_data = [
        (101, 'MacBook Air M3', 114900.00, 1, 'ELEC'),
        (102, 'Sony WH-1000XM5', 28990.00, 1, 'ELEC'),
        (103, "Levi's 511 Slim Jeans", 2999.00, 2, 'FASH'),
        (104, 'Cotton Casual Shirt', 1499.00, 2, 'FASH'),
        (105, 'Philips Air Fryer', 8499.00, 3, 'HOME')
    ]
    cursor.executemany("INSERT INTO Categories VALUES (?, ?, ?);", categories_data)
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?);", products_data)
    conn.commit()

    # Query 1: Integer Key Join
    query_cond1 = """
    SELECT 
        p.product_id,
        p.product_name,
        p.price,
        c.category_name
    FROM Products p
    INNER JOIN Categories c ON p.category_id = c.category_id;
    """
    df_cond1 = pd.read_sql_query(query_cond1, conn)
    print("\nCondition 1 (Integer Surrogate Key: p.category_id = c.category_id):")
    print(df_cond1.to_string(index=False))

    # Query 2: String Key Join
    query_cond2 = """
    SELECT 
        p.product_id,
        p.product_name,
        p.price,
        c.category_name
    FROM Products p
    INNER JOIN Categories c ON p.category_code = c.category_code;
    """
    df_cond2 = pd.read_sql_query(query_cond2, conn)
    print("\nCondition 2 (String Natural Key: p.category_code = c.category_code):")
    print(df_cond2.to_string(index=False))

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 10 tasks verified successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
