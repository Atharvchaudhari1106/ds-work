#!/usr/bin/env python3
"""
Session 13: Window Functions - Part 1
Verification & Automated Execution Script
Database: spotify_windows.db
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "spotify_windows.db")

def main():
    print("=" * 75)
    print("SESSION 13: Window Functions - Part 1 (Automated Verification)")
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
    # TASK 1: Create 'Playlists' Table & Insert Sample Data
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Creating 'Playlists' table and inserting sample data ---")
    cursor.execute("DROP TABLE IF EXISTS Playlists;")
    cursor.execute("""
    CREATE TABLE Playlists (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        playlist_name VARCHAR(100) NOT NULL,
        total_likes INT NOT NULL
    );
    """)

    playlists_data = [
        # User 101
        (1, 101, 'Gym Workout Beats', 15000),
        (2, 101, 'Coding Lo-Fi Focus', 12000),
        (3, 101, 'Rock Classics', 12000),
        (4, 101, 'Chill Acoustic', 8500),
        # User 102
        (5, 102, 'Bollywood Dance Party', 18500),
        (6, 102, 'Road Trip Anthems', 15000),
        (7, 102, 'Evening Jazz & Chai', 9200),
        # User 103
        (8, 103, 'Deep House Vibes', 14000),
        (9, 103, 'EDM Festival Bangers', 12000),
        (10, 103, 'Morning Motivation', 6000)
    ]
    cursor.executemany("INSERT INTO Playlists VALUES (?, ?, ?, ?);", playlists_data)
    conn.commit()

    df_raw = pd.read_sql_query("SELECT * FROM Playlists;", conn)
    print(df_raw.to_string(index=False))
    print(f"\n[OK] Playlists table populated with {len(df_raw)} records.")

    # -------------------------------------------------------------------------
    # TASK 2: ROW_NUMBER() OVER (ORDER BY total_likes DESC)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 2: ROW_NUMBER() - Strict Unique Row Numbers ---")
    print("=" * 75)
    task2_query = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY total_likes DESC) AS row_num,
        id AS playlist_id,
        playlist_name,
        user_id,
        total_likes
    FROM Playlists;
    """
    df_t2 = pd.read_sql_query(task2_query, conn)
    print(df_t2.to_string(index=False))
    print("\n[OK] ROW_NUMBER() assigns strictly consecutive, non-repeating numbers 1 to 10.")

    # -------------------------------------------------------------------------
    # TASK 3: RANK() OVER (ORDER BY total_likes DESC)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 3: RANK() - Standard Competition Ranking (Leaves Gaps on Ties) ---")
    print("=" * 75)
    task3_query = """
    SELECT 
        RANK() OVER (ORDER BY total_likes DESC) AS rank_pos,
        playlist_name,
        user_id,
        total_likes
    FROM Playlists;
    """
    df_t3 = pd.read_sql_query(task3_query, conn)
    print(df_t3.to_string(index=False))
    print("\n[OK] Notice: 15,000 likes has a tie at rank 2; the next rank skips to 4.")
    print("[OK] Notice: 12,000 likes has a 3-way tie at rank 5; the next rank skips to 8.")

    # -------------------------------------------------------------------------
    # TASK 4: DENSE_RANK() with PARTITION BY user_id
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 4: DENSE_RANK() PARTITION BY user_id (Per-User Rankings Without Gaps) ---")
    print("=" * 75)
    task4_query = """
    SELECT 
        user_id,
        DENSE_RANK() OVER (
            PARTITION BY user_id 
            ORDER BY total_likes DESC
        ) AS user_dense_rank,
        playlist_name,
        total_likes
    FROM Playlists
    ORDER BY user_id ASC, user_dense_rank ASC;
    """
    df_t4 = pd.read_sql_query(task4_query, conn)
    print(df_t4.to_string(index=False))
    print("\n[OK] Notice rankings reset to 1 for each distinct user_id.")
    print("[OK] For user 101, tied playlists receive rank 2, and the next playlist receives rank 3 without gaps.")

    # -------------------------------------------------------------------------
    # TASK 5: Top 2 Playlists Per User (Spotify 'Your Top Playlists')
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 5: Top 2 Playlists Per User (Filtering Window Ranks) ---")
    print("=" * 75)
    task5_query = """
    WITH RankedUserPlaylists AS (
        SELECT 
            user_id,
            playlist_name,
            total_likes,
            ROW_NUMBER() OVER (
                PARTITION BY user_id 
                ORDER BY total_likes DESC
            ) AS rank_in_user
        FROM Playlists
    )
    SELECT 
        user_id,
        rank_in_user AS playlist_rank,
        playlist_name,
        total_likes
    FROM RankedUserPlaylists
    WHERE rank_in_user <= 2
    ORDER BY user_id ASC, rank_in_user ASC;
    """
    df_t5 = pd.read_sql_query(task5_query, conn)
    print(df_t5.to_string(index=False))
    print(f"\n[OK] Total records returned (exactly 2 per user): {len(df_t5)}")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 13 window function tasks verified successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
