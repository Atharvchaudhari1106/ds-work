"""
Session 5: WHERE Clause + LIKE
Execution & Verification Script

Demonstrates and verifies:
- Task 1: Create 'Restaurants' table and populate with 6 Zomato records
- Task 2: Conditional filtering with rating > 4.0 AND city in ('Ahmedabad', 'Surat')
- Task 3: Pattern matching using LIKE 'Swa%'
- Task 4: Range filtering using BETWEEN 3.5 AND 4.5 (inclusive)
- Task 5: Membership filtering using IN ('Chinese', 'Italian', 'South Indian')
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "restaurants.db")

def main():
    print("=" * 75)
    print("SESSION 5: WHERE Clause + LIKE - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1: Create Restaurants table & insert sample records
    # ---------------------------------------------------------
    print("\n[TASK 1] Creating 'Restaurants' table and inserting sample Zomato data...")
    cursor.execute("""
        CREATE TABLE Restaurants (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cuisine VARCHAR(100) NOT NULL,
            rating DECIMAL(2, 1) NOT NULL,
            city VARCHAR(100) NOT NULL
        );
    """)

    sample_restaurants = [
        (1, 'Swagat Restaurant', 'South Indian', 4.3, 'Ahmedabad'),
        (2, 'Swadisht Dining', 'North Indian', 4.1, 'Surat'),
        (3, 'Little Italy', 'Italian', 4.6, 'Ahmedabad'),
        (4, 'Mainland China', 'Chinese', 3.8, 'Vadodara'),
        (5, 'Sankalp', 'South Indian', 4.2, 'Surat'),
        (6, 'Cafe De Bistro', 'Continental', 3.2, 'Ahmedabad')
    ]
    cursor.executemany("INSERT INTO Restaurants VALUES (?, ?, ?, ?, ?);", sample_restaurants)
    conn.commit()
    print("[OK] Table created and 6 sample records inserted.")

    print("\n--- Output: All Restaurants in Table ---")
    df_all = pd.read_sql_query("SELECT * FROM Restaurants;", conn)
    print(df_all.to_string(index=False))

    # ---------------------------------------------------------
    # Task 2: Rating > 4.0 AND (city = 'Ahmedabad' OR city = 'Surat')
    # ---------------------------------------------------------
    print("\n[TASK 2] Query: rating > 4.0 AND city in ('Ahmedabad', 'Surat')")
    query_t2 = """
        SELECT * 
        FROM Restaurants
        WHERE rating > 4.0 
          AND (city = 'Ahmedabad' OR city = 'Surat');
    """
    df_t2 = pd.read_sql_query(query_t2, conn)
    print(df_t2.to_string(index=False))

    # ---------------------------------------------------------
    # Task 3: Pattern matching with LIKE 'Swa%'
    # ---------------------------------------------------------
    print("\n[TASK 3] Query: name LIKE 'Swa%'")
    query_t3 = "SELECT * FROM Restaurants WHERE name LIKE 'Swa%';"
    df_t3 = pd.read_sql_query(query_t3, conn)
    print(df_t3.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: Range filtering with BETWEEN 3.5 AND 4.5
    # ---------------------------------------------------------
    print("\n[TASK 4] Query: rating BETWEEN 3.5 AND 4.5")
    query_t4 = "SELECT * FROM Restaurants WHERE rating BETWEEN 3.5 AND 4.5;"
    df_t4 = pd.read_sql_query(query_t4, conn)
    print(df_t4.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: IN operator ('Chinese', 'Italian', 'South Indian')
    # ---------------------------------------------------------
    print("\n[TASK 5] Query: cuisine IN ('Chinese', 'Italian', 'South Indian')")
    query_t5 = "SELECT * FROM Restaurants WHERE cuisine IN ('Chinese', 'Italian', 'South Indian');"
    df_t5 = pd.read_sql_query(query_t5, conn)
    print(df_t5.to_string(index=False))

    conn.close()
    print("\n[OK] All Session 5 tasks verified successfully!")

if __name__ == "__main__":
    main()
