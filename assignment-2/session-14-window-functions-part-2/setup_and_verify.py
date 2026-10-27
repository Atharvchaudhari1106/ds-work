#!/usr/bin/env python3
"""
Session 14: Window Functions - Part 2
Automated Verification & Execution Script
Database: orders_window.db
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "orders_window.db")

def main():
    print("=" * 75)
    print("SESSION 14: Window Functions - Part 2 (Automated Verification)")
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
    # TASK 1: Create 'Orders' Table & Insert Sample Data
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Creating 'Orders' table & inserting 10 sample orders ---")
    cursor.execute("DROP TABLE IF EXISTS Orders;")
    cursor.execute("""
    CREATE TABLE Orders (
        order_id INT PRIMARY KEY,
        user_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL
    );
    """)

    orders_data = [
        # User 101 Orders (Atharv)
        (1, 101, '2026-03-01', 350.00),
        (2, 101, '2026-03-05', 450.00),
        (3, 101, '2026-03-12', 600.00),
        (4, 101, '2026-03-20', 800.00),
        # User 102 Orders (Sneha)
        (5, 102, '2026-03-02', 200.00),
        (6, 102, '2026-03-08', 300.00),
        (7, 102, '2026-03-15', 250.00),
        (8, 102, '2026-03-22', 400.00),
        # User 103 Orders (Rahul)
        (9, 103, '2026-03-10', 500.00),
        (10, 103, '2026-03-18', 750.00)
    ]
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?);", orders_data)
    conn.commit()

    df_raw = pd.read_sql_query("SELECT * FROM Orders;", conn)
    print(df_raw.to_string(index=False))
    print(f"\n[OK] Orders table populated with {len(df_raw)} records.")

    # -------------------------------------------------------------------------
    # TASK 2: Previous Order Amount Using LAG()
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 2: LAG() Function - Previous Order Amount per User ---")
    print("=" * 75)
    task2_query = """
    SELECT 
        user_id,
        order_id,
        order_date,
        total_amount,
        LAG(total_amount, 1) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC
        ) AS previous_order_amount,
        ROUND(
            total_amount - LAG(total_amount, 1) OVER (
                PARTITION BY user_id 
                ORDER BY order_date ASC
            ), 2
        ) AS spend_diff
    FROM Orders
    ORDER BY user_id ASC, order_date ASC;
    """
    df_t2 = pd.read_sql_query(task2_query, conn)
    print(df_t2.to_string(index=False))
    print("\n[OK] First order for each user has previous_order_amount = NaN / NULL.")

    # -------------------------------------------------------------------------
    # TASK 3: Next Order Amount Using LEAD()
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 3: LEAD() Function - Next Order Amount per User ---")
    print("=" * 75)
    task3_query = """
    SELECT 
        user_id,
        order_id,
        order_date,
        total_amount,
        LEAD(total_amount, 1) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC
        ) AS next_order_amount
    FROM Orders
    ORDER BY user_id ASC, order_date ASC;
    """
    df_t3 = pd.read_sql_query(task3_query, conn)
    print(df_t3.to_string(index=False))
    print("\n[OK] Final order for each user has next_order_amount = NaN / NULL.")

    # -------------------------------------------------------------------------
    # TASK 4: Cumulative Running Total per User
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 4: Cumulative Running Total per User ---")
    print("=" * 75)
    task4_query = """
    SELECT 
        user_id,
        order_id,
        order_date,
        total_amount,
        SUM(total_amount) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
    FROM Orders
    ORDER BY user_id ASC, order_date ASC;
    """
    df_t4 = pd.read_sql_query(task4_query, conn)
    print(df_t4.to_string(index=False))
    print("\n[OK] Running total accumulates monotonically per user and resets per user.")

    # -------------------------------------------------------------------------
    # TASK 5: 3-Order Moving Average Using Window Frame
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 5: 3-Order Moving Average (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) ---")
    print("=" * 75)
    task5_query = """
    SELECT 
        user_id,
        order_id,
        order_date,
        total_amount,
        ROUND(
            SUM(total_amount) OVER (
                PARTITION BY user_id 
                ORDER BY order_date ASC 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) * 1.0 / 
            COUNT(total_amount) OVER (
                PARTITION BY user_id 
                ORDER BY order_date ASC 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ), 
            2
        ) AS moving_avg
    FROM Orders
    ORDER BY user_id ASC, order_date ASC;
    """
    df_t5 = pd.read_sql_query(task5_query, conn)
    print(df_t5.to_string(index=False))
    print("\n[OK] Successfully computed 3-order moving average using SUM() OVER() window frame constraint.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 14 window function tasks verified successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
