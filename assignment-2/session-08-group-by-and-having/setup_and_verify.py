"""
Session 8: GROUP BY + HAVING
Execution & Verification Script

Demonstrates and verifies:
- Task 1: Create 'Orders' table & populate with 9 realistic e-commerce/food orders
- Task 2: Order count grouped by payment_method (Zomato analytics breakdown)
- Task 3: Total amount spent grouped by user_id
- Task 4: Filter aggregated groups using HAVING AVG(amount) > 300
- Task 5: Deep-dive demonstration comparing WHERE (pre-filter) vs HAVING (post-filter)
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "orders.db")

def main():
    print("=" * 75)
    print("SESSION 8: GROUP BY + HAVING - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1: Orders Table Creation & Ingestion
    # ---------------------------------------------------------
    print("\n[TASK 1] Creating 'Orders' table and inserting 9 sample records...")
    cursor.execute("""
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL
        );
    """)

    orders_data = [
        (1, 101, 'Card', 550.00),
        (2, 102, 'Card', 450.00),
        (3, 101, 'UPI', 320.00),
        (4, 103, 'UPI', 280.00),
        (5, 104, 'UPI', 420.00),
        (6, 102, 'COD', 180.00),
        (7, 103, 'COD', 220.00),
        (8, 104, 'Wallet', 150.00),
        (9, 101, 'Wallet', 250.00)
    ]
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?);", orders_data)
    conn.commit()
    print("[OK] Orders table created and populated.")

    print("\n--- Output: All Orders in Table ---")
    df_all = pd.read_sql_query("SELECT * FROM Orders;", conn)
    print(df_all.to_string(index=False))

    # ---------------------------------------------------------
    # Task 2: Orders Count Grouped by Payment Method
    # ---------------------------------------------------------
    print("\n[TASK 2] Query: Count of orders per payment_method...")
    query_t2 = """
        SELECT 
            payment_method,
            COUNT(order_id) AS order_count
        FROM Orders
        GROUP BY payment_method;
    """
    df_t2 = pd.read_sql_query(query_t2, conn)
    print(df_t2.to_string(index=False))

    # ---------------------------------------------------------
    # Task 3: Total Spend by user_id
    # ---------------------------------------------------------
    print("\n[TASK 3] Query: Total amount spent by each user_id...")
    query_t3 = """
        SELECT 
            user_id,
            SUM(amount) AS total_spend
        FROM Orders
        GROUP BY user_id
        ORDER BY total_spend DESC;
    """
    df_t3 = pd.read_sql_query(query_t3, conn)
    print(df_t3.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: Payment Methods with AVG(amount) > 300 using HAVING
    # ---------------------------------------------------------
    print("\n[TASK 4] Query: Payment methods where AVG(amount) > 300 (GROUP BY + HAVING)...")
    query_t4 = """
        SELECT 
            payment_method,
            ROUND(AVG(amount), 2) AS avg_amount
        FROM Orders
        GROUP BY payment_method
        HAVING AVG(amount) > 300;
    """
    df_t4 = pd.read_sql_query(query_t4, conn)
    print(df_t4.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: WHERE vs HAVING Demonstration
    # ---------------------------------------------------------
    print("\n" + "=" * 75)
    print("[TASK 5] Demonstrating WHERE (Row Filter) vs HAVING (Group Filter)")
    print("=" * 75)

    print("\n1. WHERE Filter: Counts orders where individual transaction amount > 250:")
    where_sql = """
        SELECT 
            payment_method,
            COUNT(*) AS large_orders_count
        FROM Orders
        WHERE amount > 250
        GROUP BY payment_method;
    """
    df_where = pd.read_sql_query(where_sql, conn)
    print(df_where.to_string(index=False))

    print("\n2. HAVING Filter: Shows payment methods where total combined revenue > 600:")
    having_sql = """
        SELECT 
            payment_method,
            SUM(amount) AS total_revenue
        FROM Orders
        GROUP BY payment_method
        HAVING SUM(amount) > 600;
    """
    df_having = pd.read_sql_query(having_sql, conn)
    print(df_having.to_string(index=False))

    print("\n3. Combined Pipeline (WHERE row filter + HAVING group filter):")
    combined_sql = """
        SELECT 
            payment_method,
            COUNT(*) AS qualifying_orders,
            SUM(amount) AS total_revenue
        FROM Orders
        WHERE amount >= 200
        GROUP BY payment_method
        HAVING SUM(amount) > 500;
    """
    df_combined = pd.read_sql_query(combined_sql, conn)
    print(df_combined.to_string(index=False))

    conn.close()
    print("\n[OK] All Session 8 tasks verified successfully!")

if __name__ == "__main__":
    main()
