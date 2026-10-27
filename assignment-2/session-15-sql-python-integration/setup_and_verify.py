"""
Automated Verification Runner for Session 15: SQL + Python Integration
Tests Tasks 1 through 5 and generates foodie.db and top_rated_restaurants.csv.
"""

import os
import sqlite3
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "foodie.db")
    csv_path = os.path.join(base_dir, "top_rated_restaurants.csv")

    print("=" * 75)
    print("SESSION 15: SQL + Python Integration (Automated Verification)")
    print(f"SQLite Version: {sqlite3.sqlite_version}")
    print(f"Pandas Version: {pd.__version__}")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # TASK 1: Create foodie.db and Restaurants table
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Creating database 'foodie.db' & table 'Restaurants' ---")
    print("Note: The 'sqlite3' module is built directly into Python's standard library.")
    print("      No separate 'pip install sqlite3' is required.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Restaurants;")
    cursor.execute("""
        CREATE TABLE Restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            rating REAL NOT NULL
        );
    """)
    conn.commit()
    print("[OK] Created table 'Restaurants' with columns (id, name, cuisine, rating).")

    # -------------------------------------------------------------------------
    # TASK 2: Insert 3 sample restaurants & fetch rating > 4.0
    # -------------------------------------------------------------------------
    print("\n--- TASK 2: Inserting 3 sample restaurants & querying rating > 4.0 ---")
    restaurants_data = [
        (1, "Little Italy", "Italian", 4.8),
        (2, "Punjab Grill", "North Indian", 4.6),
        (3, "Chai Point", "Cafe", 3.9)
    ]
    cursor.executemany(
        "INSERT INTO Restaurants (id, name, cuisine, rating) VALUES (?, ?, ?, ?);",
        restaurants_data
    )
    conn.commit()
    print(f"[OK] Inserted {len(restaurants_data)} sample restaurants into Restaurants table.")

    cursor.execute("SELECT name FROM Restaurants WHERE rating > 4.0;")
    rows = cursor.fetchall()
    print("Restaurants with rating above 4.0:")
    for (name,) in rows:
        print(f"  - {name}")

    assert len(rows) == 2, f"Expected 2 restaurants with rating > 4.0, found {len(rows)}"
    assert ("Little Italy",) in rows
    assert ("Punjab Grill",) in rows
    print("[OK] Task 2 passed: Successfully fetched and printed restaurants with rating > 4.0.")

    # -------------------------------------------------------------------------
    # TASK 3: Load all rows into Pandas DataFrame & display top 2 rows
    # -------------------------------------------------------------------------
    print("\n--- TASK 3: Loading all rows into Pandas DataFrame & displaying head(2) ---")
    df = pd.read_sql_query("SELECT * FROM Restaurants;", conn)
    print("All rows in DataFrame:")
    print(df.to_string(index=False))

    print("\nTop 2 rows using DataFrame.head(2):")
    head_2 = df.head(2)
    print(head_2.to_string(index=False))

    assert len(head_2) == 2, f"Expected 2 rows in head(2), got {len(head_2)}"
    print("[OK] Task 3 passed: DataFrame loaded and top 2 rows displayed successfully.")

    # -------------------------------------------------------------------------
    # TASK 4: Add 'delivery_charge' and calculate 'final_rating'
    # -------------------------------------------------------------------------
    print("\n--- TASK 4: Adding 'delivery_charge' and conditional 'final_rating' ---")
    # Add new column delivery_charge = 50
    df["delivery_charge"] = 50

    # Calculate final_rating: rating + (0.1 if cuisine is 'Italian' else 0.0)
    df["final_rating"] = df.apply(
        lambda row: round(row["rating"] + (0.1 if row["cuisine"] == "Italian" else 0.0), 2),
        axis=1
    )

    print("Updated DataFrame with 'delivery_charge' and 'final_rating':")
    print(df.to_string(index=False))

    # Assertions
    assert all(df["delivery_charge"] == 50), "All delivery charges must equal 50."
    little_italy_final = df.loc[df["name"] == "Little Italy", "final_rating"].values[0]
    punjab_grill_final = df.loc[df["name"] == "Punjab Grill", "final_rating"].values[0]
    chai_point_final = df.loc[df["name"] == "Chai Point", "final_rating"].values[0]

    assert little_italy_final == 4.9, f"Expected Little Italy final rating 4.9, got {little_italy_final}"
    assert punjab_grill_final == 4.6, f"Expected Punjab Grill final rating 4.6, got {punjab_grill_final}"
    assert chai_point_final == 3.9, f"Expected Chai Point final rating 3.9, got {chai_point_final}"
    print("[OK] Task 4 passed: Correctly added delivery_charge and computed Italian bonus.")

    # -------------------------------------------------------------------------
    # TASK 5: Automate daily summary (rating > 4.5) to CSV
    # -------------------------------------------------------------------------
    print("\n--- TASK 5: Daily Summary Automation (rating > 4.5 -> CSV) ---")
    query_top = "SELECT * FROM Restaurants WHERE rating > 4.5 ORDER BY rating DESC;"
    df_top = pd.read_sql_query(query_top, conn)
    df_top.to_csv(csv_path, index=False)
    print(f"Top-rated restaurants (rating > 4.5) written to {csv_path}:")
    print(df_top.to_string(index=False))

    assert os.path.exists(csv_path), "top_rated_restaurants.csv was not created!"
    df_read_back = pd.read_csv(csv_path)
    assert len(df_read_back) == 2, f"Expected 2 rows in top_rated_restaurants.csv, got {len(df_read_back)}"
    assert all(df_read_back["rating"] > 4.5), "All ratings in CSV must be > 4.5"
    print("[OK] Task 5 passed: top_rated_restaurants.csv saved and verified.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 15 tasks verified successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
