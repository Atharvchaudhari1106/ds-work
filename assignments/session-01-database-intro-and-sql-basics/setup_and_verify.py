"""
Session 1: Database Introduction & SQL Basics
Execution & Verification Script

This script creates the database 'music_streaming_app.db', executes the DDL/DML,
runs the queries for Tasks 1-4, and prints the Task 5 concept explanation.
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "music_streaming_app.db")

def main():
    print("=" * 70)
    print("SESSION 1: Database Introduction & SQL Basics - Verification")
    print("=" * 70)

    # Clean existing test database
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1 & 2: Database and Table Creation
    # ---------------------------------------------------------
    print("\n[TASK 1 & 2] Creating table 'playlists' in 'music_streaming_app'...")
    cursor.execute("""
        CREATE TABLE playlists (
            playlist_id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_by VARCHAR(100) NOT NULL
        );
    """)
    print("[OK] Table 'playlists' created successfully.")

    # ---------------------------------------------------------
    # Task 3: Insert Sample Rows
    # ---------------------------------------------------------
    print("\n[TASK 3] Inserting sample playlist rows...")
    sample_data = [
        (1, 'Bollywood Hits', 'Amit'),
        (2, 'Chill Vibes', 'Pooja'),
        (3, 'Workout Mix', 'Rahul')
    ]
    cursor.executemany("""
        INSERT INTO playlists (playlist_id, name, created_by)
        VALUES (?, ?, ?);
    """, sample_data)
    conn.commit()
    print(f"[OK] Inserted {len(sample_data)} rows successfully.")

    print("\n--- Current 'playlists' Table Content ---")
    df_all = pd.read_sql_query("SELECT * FROM playlists;", conn)
    print(df_all.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: Select Playlists Created by 'Amit'
    # ---------------------------------------------------------
    print("\n[TASK 4] Query: SELECT * FROM playlists WHERE created_by = 'Amit';")
    df_amit = pd.read_sql_query("SELECT * FROM playlists WHERE created_by = 'Amit';", conn)
    print(df_amit.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: Zomato Conceptual Explanation
    # ---------------------------------------------------------
    print("\n" + "=" * 70)
    print("[TASK 5] AI Response: Table vs. Row vs. Column (Zomato Example)")
    print("=" * 70)
    explanation = """
Context: Imagine how Zomato tracks food delivery in a database:

1. TABLE ('Orders'):
   - Definition: The structured container holding all related information.
   - Zomato Example: The entire 'Orders' table containing every order placed on the platform.

2. COLUMN (Field / Attribute):
   - Definition: A vertical category that specifies a particular detail for every record.
   - Zomato Example: 'restaurant_name', 'delivery_address', 'order_status', or 'total_amount'.

3. ROW (Record / Tuple):
   - Definition: A single horizontal entry that groups all attributes for one real-world item.
   - Zomato Example: Order #9843 placed by Amit for 'Butter Chicken' from 'Punjab Grill' costing Rs. 540.
"""
    print(explanation.strip())
    print("=" * 70)

    conn.close()
    print("\n[OK] All tasks verified successfully!")

if __name__ == "__main__":
    main()
