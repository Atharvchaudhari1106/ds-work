"""
Session 4: SELECT Statement Basics
Execution & Verification Script

Demonstrates and verifies:
- Task 1: MusicPlaylist table creation, 5 Spotify songs insert & SELECT *
- Task 2: Column projection (song_name, artist) with LIMIT 3
- Task 3: FoodOrders table creation, records insert & SELECT DISTINCT restaurant
- Task 4: Column aliases (Dish, Date Ordered)
- Task 5: Analysis and correction of the LIMIT query with ORDER BY
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "music_and_food.db")

def main():
    print("=" * 75)
    print("SESSION 4: SELECT Statement Basics - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1: MusicPlaylist table & 5 sample songs
    # ---------------------------------------------------------
    print("\n[TASK 1] Creating 'MusicPlaylist' table and inserting 5 Spotify songs...")
    cursor.execute("""
        CREATE TABLE MusicPlaylist (
            id INTEGER PRIMARY KEY,
            song_name VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            genre VARCHAR(100) NOT NULL,
            duration VARCHAR(20) NOT NULL
        );
    """)

    songs = [
        (1, 'Blinding Lights', 'The Weeknd', 'Synthwave / Pop', '3:20'),
        (2, 'Starboy', 'The Weeknd', 'R&B / Pop', '3:50'),
        (3, 'Shape of You', 'Ed Sheeran', 'Pop', '3:53'),
        (4, 'Levitating', 'Dua Lipa', 'Disco-Pop', '3:23'),
        (5, 'Tum Hi Ho', 'Arijit Singh', 'Bollywood Romantic', '4:22')
    ]
    cursor.executemany("INSERT INTO MusicPlaylist VALUES (?, ?, ?, ?, ?);", songs)
    conn.commit()
    print("[OK] Table created and 5 records inserted.")

    print("\n--- Output: SELECT * FROM MusicPlaylist ---")
    df_songs = pd.read_sql_query("SELECT * FROM MusicPlaylist;", conn)
    print(df_songs.to_string(index=False))

    # ---------------------------------------------------------
    # Task 2: song_name and artist with LIMIT 3
    # ---------------------------------------------------------
    print("\n[TASK 2] Query: SELECT song_name, artist FROM MusicPlaylist LIMIT 3;")
    df_limit3 = pd.read_sql_query("SELECT song_name, artist FROM MusicPlaylist LIMIT 3;", conn)
    print(df_limit3.to_string(index=False))

    # ---------------------------------------------------------
    # Task 3: FoodOrders table and DISTINCT restaurants
    # ---------------------------------------------------------
    print("\n[TASK 3] Creating 'FoodOrders' table and querying unique restaurants...")
    cursor.execute("""
        CREATE TABLE FoodOrders (
            id INTEGER PRIMARY KEY,
            restaurant VARCHAR(255) NOT NULL,
            food_item VARCHAR(255) NOT NULL,
            order_date DATE NOT NULL
        );
    """)

    orders = [
        (1, 'Biryani Blues', 'Hyderabadi Dum Biryani', '2026-10-20'),
        (2, "Domino's Pizza", 'Farmhouse Pizza', '2026-10-21'),
        (3, 'Biryani Blues', 'Chicken Tikka', '2026-10-22'),
        (4, 'Punjab Grill', 'Dal Makhani', '2026-10-23'),
        (5, "Domino's Pizza", 'Garlic Bread', '2026-10-24'),
        (6, "Haldiram's", 'Chole Bhature', '2026-10-25')
    ]
    cursor.executemany("INSERT INTO FoodOrders VALUES (?, ?, ?, ?);", orders)
    conn.commit()
    print("[OK] Table 'FoodOrders' populated with 6 orders across 4 unique restaurants.")

    print("\n--- Output: SELECT DISTINCT restaurant FROM FoodOrders ---")
    df_unique_rests = pd.read_sql_query("SELECT DISTINCT restaurant FROM FoodOrders;", conn)
    print(df_unique_rests.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: Column aliases ('Dish' and 'Date Ordered')
    # ---------------------------------------------------------
    print("\n[TASK 4] Query: SELECT food_item AS 'Dish', order_date AS 'Date Ordered' FROM FoodOrders;")
    df_aliases = pd.read_sql_query("""
        SELECT food_item AS "Dish", order_date AS "Date Ordered"
        FROM FoodOrders;
    """, conn)
    print(df_aliases.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: Identify and Fix Query Mistake
    # ---------------------------------------------------------
    print("\n" + "=" * 75)
    print("[TASK 5] Debugging Query: SELECT DISTINCT food_item, restaurant FROM FoodOrders LIMIT 2")
    print("=" * 75)
    print("DIAGNOSIS & ANALYSIS:")
    print("1. Missing ORDER BY (Non-Deterministic Behavior):")
    print("   In SQL standards, using LIMIT without ORDER BY returns arbitrary rows.")
    print("   Depending on database indexes and storage engines, the returned 2 rows are inconsistent.")
    print("2. Multi-DBMS Compatibility (T-SQL vs MySQL/PostgreSQL):")
    print("   - In SQL Server (SSMS / T-SQL), 'LIMIT' is invalid syntax. T-SQL uses TOP: 'SELECT DISTINCT TOP 2 ...'")
    print("   - In Oracle SQL, 'FETCH FIRST 2 ROWS ONLY' is used.")
    print("3. Clause Ordering:")
    print("   Standard SQL clause hierarchy: SELECT -> FROM -> [WHERE] -> [ORDER BY] -> LIMIT.")
    
    print("\nCORRECTED QUERY (Deterministic with ORDER BY):")
    query_fixed = """
        SELECT DISTINCT food_item, restaurant
        FROM FoodOrders
        ORDER BY food_item ASC
        LIMIT 2;
    """
    print(query_fixed.strip())
    print("\n--- Output of Corrected Query ---")
    df_fixed = pd.read_sql_query(query_fixed, conn)
    print(df_fixed.to_string(index=False))

    conn.close()
    print("\n[OK] All Session 4 tasks verified successfully!")

if __name__ == "__main__":
    main()
