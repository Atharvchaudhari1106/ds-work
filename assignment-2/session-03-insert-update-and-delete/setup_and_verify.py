"""
Session 3: INSERT, UPDATE & DELETE
Execution & Verification Script

Demonstrates and verifies:
- Task 1: Create 'Playlist' table & insert single favorite song
- Task 2: Insert 3 additional songs with multi-row INSERT
- Task 3: UPDATE with WHERE clause to fix artist typo ('Arjit Singh' -> 'Arijit Singh')
- Task 4: DELETE with WHERE clause to remove tracks with duration < 120s
- Task 5: Conditional compound UPDATE adding '(Remix)' for AP Dhillon songs > 180s
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "playlist_app.db")

def main():
    print("=" * 75)
    print("SESSION 3: INSERT, UPDATE & DELETE - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1: Create Playlist table & insert 1 favorite song
    # ---------------------------------------------------------
    print("\n[TASK 1] Creating 'Playlist' table and inserting 1 favorite song...")
    cursor.execute("""
        CREATE TABLE Playlist (
            id INTEGER PRIMARY KEY,
            song_name VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            duration INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        INSERT INTO Playlist (id, song_name, artist, duration)
        VALUES (1, 'Tum Hi Ho', 'Arjit Singh', 262);
    """)
    conn.commit()
    print("[OK] Table created and single song inserted.")

    print("\n--- Current Playlist (After Task 1) ---")
    df_t1 = pd.read_sql_query("SELECT * FROM Playlist;", conn)
    print(df_t1.to_string(index=False))

    # ---------------------------------------------------------
    # Task 2: Insert 3 new rows
    # ---------------------------------------------------------
    print("\n[TASK 2] Inserting 3 new recently played songs...")
    new_songs = [
        (2, 'Brown Munde', 'AP Dhillon', 260),
        (3, 'Summer High', 'AP Dhillon', 175),
        (4, 'Short Interlude', 'The Weeknd', 90)
    ]
    cursor.executemany("INSERT INTO Playlist VALUES (?, ?, ?, ?);", new_songs)
    conn.commit()
    print("[OK] Inserted 3 new songs successfully.")

    print("\n--- Current Playlist (After Task 2) ---")
    df_t2 = pd.read_sql_query("SELECT * FROM Playlist;", conn)
    print(df_t2.to_string(index=False))

    # ---------------------------------------------------------
    # Task 3: Fix typo using UPDATE
    # ---------------------------------------------------------
    print("\n[TASK 3] Fixing typo: Changing 'Arjit Singh' to 'Arijit Singh'...")
    cursor.execute("""
        UPDATE Playlist
        SET artist = 'Arijit Singh'
        WHERE artist = 'Arjit Singh';
    """)
    conn.commit()
    print(f"[OK] Rows updated: {cursor.rowcount}")

    print("\n--- Current Playlist (After Task 3: Typo Fixed) ---")
    df_t3 = pd.read_sql_query("SELECT * FROM Playlist;", conn)
    print(df_t3.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: DELETE song where duration < 120 seconds
    # ---------------------------------------------------------
    print("\n[TASK 4] Deleting song where duration < 120 seconds...")
    cursor.execute("""
        DELETE FROM Playlist
        WHERE duration < 120;
    """)
    conn.commit()
    print(f"[OK] Rows deleted: {cursor.rowcount}")

    print("\n--- Current Playlist (After Task 4: Short Tracks Removed) ---")
    df_t4 = pd.read_sql_query("SELECT * FROM Playlist;", conn)
    print(df_t4.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: Compound UPDATE for AP Dhillon songs > 180s
    # ---------------------------------------------------------
    print("\n[TASK 5] Updating AP Dhillon songs > 180s to add '(Remix)'...")
    cursor.execute("""
        UPDATE Playlist
        SET song_name = song_name || ' (Remix)'
        WHERE artist = 'AP Dhillon' AND duration > 180;
    """)
    conn.commit()
    print(f"[OK] Rows updated: {cursor.rowcount}")

    print("\n--- Final Playlist State (After Task 5) ---")
    df_t5 = pd.read_sql_query("SELECT * FROM Playlist;", conn)
    print(df_t5.to_string(index=False))

    conn.close()
    print("\n[OK] All Session 3 tasks verified successfully!")

if __name__ == "__main__":
    main()
