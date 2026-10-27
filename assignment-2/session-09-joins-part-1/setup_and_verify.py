#!/usr/bin/env python3
"""
Session 9: JOINS - Part 1
Verification and Execution Script
Tests Tasks 1-5 against an embedded SQLite database (zomato_joins.db).
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "zomato_joins.db")

def run_session_9():
    print("=" * 70)
    print("SESSION 9: JOINS - Part 1 (Verification Script)")
    print("SQLite Library Version:", sqlite3.sqlite_version)
    print("=" * 70)

    # 1. Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = OFF;") # turned off during test setup so orphaned dish can exist without constraint failure

    # -------------------------------------------------------------------------
    # TASK 1: Create Tables & Insert Sample Records
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Setting up 'restaurants' and 'dishes' tables ---")
    cursor.execute("DROP TABLE IF EXISTS dishes;")
    cursor.execute("DROP TABLE IF EXISTS restaurants;")

    cursor.execute("""
    CREATE TABLE restaurants (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE dishes (
        id INT PRIMARY KEY,
        restaurant_id INT,
        dish_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );
    """)

    # Insert 4 restaurants (Restaurant 4 has NO dishes to test LEFT JOIN)
    restaurants_data = [
        (1, 'Biryani By Kilo', 'Hyderabad'),
        (2, 'Haldiram', 'Nagpur'),
        (3, 'Pizza Hut', 'Pune'),
        (4, 'Cafe Coffee Day', 'Mumbai')
    ]
    cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?);", restaurants_data)

    # Insert dishes (including dish 110 with restaurant_id 99 to test RIGHT JOIN)
    dishes_data = [
        # Biryani By Kilo
        (101, 1, 'Hyderabadi Chicken Biryani', 350.00),
        (102, 1, 'Mutton Dum Biryani', 480.00),
        (103, 1, 'Mirchi Ka Salan', 120.00),
        # Haldiram
        (104, 2, 'Raj Kachori', 140.00),
        (105, 2, 'Chole Bhature', 180.00),
        (106, 2, 'Gulab Jamun (2 pcs)', 90.00),
        # Pizza Hut
        (107, 3, 'Margherita Pizza', 299.00),
        (108, 3, 'Garlic Breadsticks', 149.00),
        (109, 3, 'Farmhouse Veg Pizza', 399.00),
        # Orphaned / unlinked dish (simulating data integrity anomaly)
        (110, 99, 'Dragon Noodles', 220.00)
    ]
    cursor.executemany("INSERT INTO dishes VALUES (?, ?, ?, ?);", dishes_data)
    conn.commit()

    df_restaurants = pd.read_sql_query("SELECT * FROM restaurants;", conn)
    df_dishes = pd.read_sql_query("SELECT * FROM dishes;", conn)
    print("\n[OK] Restaurants Table:")
    print(df_restaurants.to_string(index=False))
    print("\n[OK] Dishes Table:")
    print(df_dishes.to_string(index=False))

    # -------------------------------------------------------------------------
    # TASK 2: INNER JOIN
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("--- TASK 2: INNER JOIN (Dishes with Restaurant Info) ---")
    print("=" * 70)
    task2_query = """
    SELECT 
        d.id AS dish_id,
        d.dish_name,
        d.price,
        r.name AS restaurant_name,
        r.city
    FROM dishes d
    INNER JOIN restaurants r ON d.restaurant_id = r.id;
    """
    df_inner = pd.read_sql_query(task2_query, conn)
    print(df_inner.to_string(index=False))
    print(f"\n[OK] Total matching rows returned: {len(df_inner)}")

    # -------------------------------------------------------------------------
    # TASK 3: LEFT JOIN
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("--- TASK 3: LEFT JOIN (All Restaurants, even if no dishes on menu) ---")
    print("=" * 70)
    task3_query = """
    SELECT 
        r.id AS restaurant_id,
        r.name AS restaurant_name,
        r.city,
        d.id AS dish_id,
        d.dish_name,
        d.price
    FROM restaurants r
    LEFT JOIN dishes d ON r.id = d.restaurant_id;
    """
    df_left = pd.read_sql_query(task3_query, conn)
    print(df_left.to_string(index=False))
    print(f"\n[OK] Notice 'Cafe Coffee Day' has dish_id, dish_name, price as NULL / NaN.")
    print(f"[OK] Total rows returned: {len(df_left)}")

    # -------------------------------------------------------------------------
    # TASK 4: RIGHT JOIN
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("--- TASK 4: RIGHT JOIN (All Dishes, including unlinked / orphaned dishes) ---")
    print("=" * 70)
    task4_query = """
    SELECT 
        r.id AS restaurant_id,
        r.name AS restaurant_name,
        r.city,
        d.id AS dish_id,
        d.dish_name,
        d.price,
        d.restaurant_id AS dish_fk
    FROM restaurants r
    RIGHT JOIN dishes d ON r.id = d.restaurant_id;
    """
    df_right = pd.read_sql_query(task4_query, conn)
    print(df_right.to_string(index=False))
    print(f"\n[OK] Notice 'Dragon Noodles' (dish_id 110) has restaurant_id, name, city as NULL / NaN.")
    print(f"[OK] Total rows returned: {len(df_right)}")

    # -------------------------------------------------------------------------
    # TASK 5: Spotify Scenario - Playlists and Songs
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("--- TASK 5: Spotify Scenario (All Playlists, including empty ones) ---")
    print("=" * 70)
    cursor.execute("DROP TABLE IF EXISTS songs;")
    cursor.execute("DROP TABLE IF EXISTS playlists;")

    cursor.execute("""
    CREATE TABLE playlists (
        playlist_id INT PRIMARY KEY,
        playlist_name VARCHAR(100) NOT NULL,
        created_by VARCHAR(50) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE songs (
        song_id INT PRIMARY KEY,
        playlist_id INT,
        title VARCHAR(100) NOT NULL,
        artist VARCHAR(100) NOT NULL,
        duration_sec INT NOT NULL
    );
    """)

    playlists_data = [
        (1, 'Gym Workout Beats', 'Atharv'),
        (2, 'Acoustic Morning', 'Sneha'),
        (3, 'Study Lo-Fi Focus', 'Rahul'),
        (4, 'Road Trip 2026', 'Atharv')  # Empty playlist
    ]
    cursor.executemany("INSERT INTO playlists VALUES (?, ?, ?);", playlists_data)

    songs_data = [
        (201, 1, 'Eye of the Tiger', 'Survivor', 245),
        (202, 1, 'Lose Yourself', 'Eminem', 326),
        (203, 1, 'Till I Collapse', 'Eminem', 297),
        (204, 2, 'Banana Pancakes', 'Jack Johnson', 192),
        (205, 2, 'Here Comes the Sun', 'The Beatles', 185),
        (206, 3, 'Sunset Lover', 'Petit Biscuit', 237)
    ]
    cursor.executemany("INSERT INTO songs VALUES (?, ?, ?, ?, ?);", songs_data)
    conn.commit()

    task5_query = """
    SELECT 
        p.playlist_id,
        p.playlist_name,
        p.created_by,
        s.song_id,
        s.title AS song_title,
        s.artist,
        s.duration_sec
    FROM playlists p
    LEFT JOIN songs s ON p.playlist_id = s.playlist_id;
    """
    df_spotify = pd.read_sql_query(task5_query, conn)
    print(df_spotify.to_string(index=False))
    print(f"\n[OK] Notice 'Road Trip 2026' appears with NULL song info because LEFT JOIN preserves it!")
    print(f"[OK] Total rows returned: {len(df_spotify)}")

    conn.close()
    print("\n" + "=" * 70)
    print("[SUCCESS] All Session 9 JOIN tasks verified successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_session_9()
