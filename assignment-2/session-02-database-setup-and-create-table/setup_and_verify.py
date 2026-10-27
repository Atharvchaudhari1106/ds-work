"""
Session 2: Database Setup + CREATE TABLE
Execution & Verification Script

Demonstrates and verifies:
- Task 1 & 2: Creation of 'foodie_app.db'
- Task 3: Creation and population of 'restaurants' table (Zomato-style)
- Task 4: Design and creation of 'users' table with constraints (Flipkart-style)
- Task 5: Intentional syntax error catching, error message display, and resolution
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "foodie_app.db")

def main():
    print("=" * 75)
    print("SESSION 2: Database Setup + CREATE TABLE - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1 & 2: Database Connection
    # ---------------------------------------------------------
    print("\n[TASK 1 & 2] Connected to database: 'foodie_app.db'")
    print("[OK] Database connection verified.")

    # ---------------------------------------------------------
    # Task 3: 'restaurants' Table (Zomato-Style)
    # ---------------------------------------------------------
    print("\n[TASK 3] Creating 'restaurants' table (Zomato backend)...")
    cursor.execute("""
        CREATE TABLE restaurants (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cuisine VARCHAR(50) NOT NULL,
            rating DECIMAL(2, 1) NOT NULL,
            location VARCHAR(100) NOT NULL
        );
    """)

    sample_restaurants = [
        (1, 'Punjab Grill', 'North Indian', 4.5, 'Connaught Place, New Delhi'),
        (2, 'Biryani Blues', 'Hyderabadi', 4.3, 'Indiranagar, Bengaluru'),
        (3, 'Bastian', 'Seafood / Continental', 4.7, 'Bandra West, Mumbai')
    ]
    cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?, ?, ?);", sample_restaurants)
    conn.commit()
    print("[OK] Table 'restaurants' created and populated.")

    print("\n--- Output: SELECT * FROM restaurants ---")
    df_rests = pd.read_sql_query("SELECT * FROM restaurants;", conn)
    print(df_rests.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: 'users' Table (Flipkart-Style)
    # ---------------------------------------------------------
    print("\n[TASK 4] Creating 'users' table (Flipkart backend with constraints)...")
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(15) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    sample_users = [
        (101, 'atharv_c', 'atharv@example.com', '+919876543210'),
        (102, 'priya_sharma', 'priya.s@example.com', '+919812345678'),
        (103, 'rahul_verma', 'rahul.v@example.com', '+919898765432')
    ]
    cursor.executemany("""
        INSERT INTO users (user_id, username, email, phone_number)
        VALUES (?, ?, ?, ?);
    """, sample_users)
    conn.commit()
    print("[OK] Table 'users' created with UNIQUE constraints and populated.")

    print("\n--- Output: SELECT * FROM users ---")
    df_users = pd.read_sql_query("SELECT * FROM users;", conn)
    print(df_users.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: Intentional Error & Resolution
    # ---------------------------------------------------------
    print("\n" + "=" * 75)
    print("[TASK 5] Demonstrating Intentional Syntax Error & Resolution")
    print("=" * 75)

    invalid_sql = """
    CREATE TABLE invalid_demo_table (
        id INT PRIMARY KEY,
        username VARCHAR(50),
        email VARCHAR(100)
        phone VARCHAR(15)
    );
    """
    print("Attempting to execute invalid SQL statement (missing comma after email):")
    print(invalid_sql)

    try:
        cursor.execute(invalid_sql)
        print("Unexpected: Statement succeeded.")
    except sqlite3.OperationalError as e:
        print(f"[CAUGHT EXPECTED ERROR]: {type(e).__name__}: {e}")
        print("Diagnostic: The SQL parser encountered 'phone' where a comma ',' was expected.")

    print("\nExecuting Corrected Statement:")
    fixed_sql = """
    CREATE TABLE fixed_demo_table (
        id INT PRIMARY KEY,
        username VARCHAR(50),
        email VARCHAR(100),
        phone VARCHAR(15)
    );
    """
    print(fixed_sql.strip())
    cursor.execute(fixed_sql)
    conn.commit()
    print("[OK] Corrected table created successfully!")

    conn.close()
    print("\n[OK] All Session 2 tasks verified successfully!")

if __name__ == "__main__":
    main()
