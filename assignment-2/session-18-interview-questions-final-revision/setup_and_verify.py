"""
Automated Verification Runner for Session 18: Interview Questions + Final Revision
Verifies Tasks 1 to 5, creates interview_revision.db, and validates all results.
"""

import os
import sqlite3
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "interview_revision.db")

    print("=" * 75)
    print("SESSION 18: Interview Questions + Final Revision (Automated Verification)")
    print(f"SQLite Version: {sqlite3.sqlite_version}")
    print(f"Pandas Version: {pd.__version__}")
    print("=" * 75)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # -------------------------------------------------------------------------
    # TASK 1: Songs with more than 3 songs per artist
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Artists with > 3 songs (GROUP BY & HAVING) ---")
    cursor.execute("DROP TABLE IF EXISTS songs;")
    cursor.execute("""
        CREATE TABLE songs (
            song_id INTEGER PRIMARY KEY,
            artist_name TEXT NOT NULL,
            title TEXT NOT NULL
        );
    """)

    songs_data = [
        (1,  "Arijit Singh",   "Tum Hi Ho"),
        (2,  "Arijit Singh",   "Kesariya"),
        (3,  "Arijit Singh",   "Channa Mereya"),
        (4,  "Arijit Singh",   "Raabta"),
        (5,  "Arijit Singh",   "Kalank"),
        (6,  "Taylor Swift",   "Cruel Summer"),
        (7,  "Taylor Swift",   "Anti-Hero"),
        (8,  "Taylor Swift",   "Blank Space"),
        (9,  "Taylor Swift",   "Lover"),
        (10, "Ed Sheeran",     "Shape of You"),
        (11, "Ed Sheeran",     "Perfect"),
        (12, "Ed Sheeran",     "Bad Habits"),
        (13, "The Weeknd",     "Blinding Lights"),
        (14, "The Weeknd",     "Starboy"),
        (15, "Diljit Dosanjh", "Lover")
    ]
    cursor.executemany("INSERT INTO songs (song_id, artist_name, title) VALUES (?, ?, ?);", songs_data)
    conn.commit()

    query_task1 = """
    SELECT 
        artist_name,
        COUNT(song_id) AS total_songs
    FROM songs
    GROUP BY artist_name
    HAVING COUNT(song_id) > 3
    ORDER BY total_songs DESC, artist_name ASC;
    """
    df_task1 = pd.read_sql_query(query_task1, conn)
    print(df_task1.to_string(index=False))

    assert len(df_task1) == 2, f"Expected 2 artists with > 3 songs, got {len(df_task1)}"
    assert list(df_task1["artist_name"]) == ["Arijit Singh", "Taylor Swift"]
    assert list(df_task1["total_songs"]) == [5, 4]
    print("[OK] Task 1 passed: Artists with more than 3 songs correctly filtered using HAVING.")

    # -------------------------------------------------------------------------
    # TASK 2: JOIN query for total order amount per username
    # -------------------------------------------------------------------------
    print("\n--- TASK 2: Username along with total order amount (JOIN) ---")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    users_data = [(1, "rahul_sharma"), (2, "priya_patel"), (3, "amit_verma"), (4, "sneha_reddy"), (5, "vikram_m")]
    orders_data = [
        (101, 1, 450.00),
        (102, 1, 750.00),
        (103, 2, 1200.00),
        (104, 2, 800.00),
        (105, 3, 350.00),
        (106, 4, 950.00),
        (107, 4, 1100.00),
        (108, 4, 600.00)
    ]
    cursor.executemany("INSERT INTO users (user_id, username) VALUES (?, ?);", users_data)
    cursor.executemany("INSERT INTO orders (order_id, user_id, amount) VALUES (?, ?, ?);", orders_data)
    conn.commit()

    query_task2 = """
    SELECT 
        u.username,
        COALESCE(SUM(o.amount), 0.00) AS total_order_amount
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id, u.username
    ORDER BY total_order_amount DESC;
    """
    df_task2 = pd.read_sql_query(query_task2, conn)
    print(df_task2.to_string(index=False))

    assert len(df_task2) == 5, f"Expected 5 users, got {len(df_task2)}"
    assert df_task2.iloc[0]["username"] == "sneha_reddy" and df_task2.iloc[0]["total_order_amount"] == 2650.00
    assert df_task2.iloc[1]["username"] == "priya_patel" and df_task2.iloc[1]["total_order_amount"] == 2000.00
    assert df_task2.iloc[2]["username"] == "rahul_sharma" and df_task2.iloc[2]["total_order_amount"] == 1200.00
    assert df_task2.iloc[3]["username"] == "amit_verma" and df_task2.iloc[3]["total_order_amount"] == 350.00
    assert df_task2.iloc[4]["username"] == "vikram_m" and df_task2.iloc[4]["total_order_amount"] == 0.00
    print("[OK] Task 2 passed: Username and total order amount calculated accurately via JOIN.")

    # -------------------------------------------------------------------------
    # TASK 3: Subquery for restaurants with rating above average
    # -------------------------------------------------------------------------
    print("\n--- TASK 3: Restaurants with rating > overall average (Subquery) ---")
    cursor.execute("DROP TABLE IF EXISTS restaurants;")
    cursor.execute("""
        CREATE TABLE restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            rating DECIMAL(3, 2) NOT NULL
        );
    """)

    restaurants_data = [
        (1, "Gulati", 4.80),
        (2, "Punjab Grill", 4.50),
        (3, "Toscano", 4.60),
        (4, "Haldirams", 3.80),
        (5, "Subway", 3.70),
        (6, "Chai Point", 3.60)
    ]
    cursor.executemany("INSERT INTO restaurants (id, name, rating) VALUES (?, ?, ?);", restaurants_data)
    conn.commit()

    query_task3 = """
    SELECT 
        name,
        rating
    FROM restaurants
    WHERE rating > (
        SELECT AVG(rating) 
        FROM restaurants
    )
    ORDER BY rating DESC;
    """
    df_task3 = pd.read_sql_query(query_task3, conn)
    print(df_task3.to_string(index=False))

    avg_rating = pd.read_sql_query("SELECT AVG(rating) AS avg_r FROM restaurants;", conn)["avg_r"].iloc[0]
    print(f"Overall Average Rating: {round(avg_rating, 2)}")

    assert len(df_task3) == 3, f"Expected 3 restaurants above average, got {len(df_task3)}"
    assert all(df_task3["rating"] > avg_rating), "All returned restaurants must exceed average rating."
    print("[OK] Task 3 passed: Scalar subquery successfully filtered above-average restaurants.")

    # -------------------------------------------------------------------------
    # TASK 4: Window running total per user ordered by transaction_date
    # -------------------------------------------------------------------------
    print("\n--- TASK 4: Window Cumulative Running Total per User ---")
    cursor.execute("DROP TABLE IF EXISTS transactions;")
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            transaction_date DATE NOT NULL
        );
    """)

    transactions_data = [
        (1, 101, 500.00,  "2026-03-01"),
        (2, 101, 300.00,  "2026-03-05"),
        (3, 101, 700.00,  "2026-03-10"),
        (4, 102, 1000.00, "2026-03-02"),
        (5, 102, 450.00,  "2026-03-08"),
        (6, 102, 550.00,  "2026-03-15")
    ]
    cursor.executemany("INSERT INTO transactions (id, user_id, amount, transaction_date) VALUES (?, ?, ?, ?);", transactions_data)
    conn.commit()

    query_task4 = """
    SELECT 
        user_id,
        id AS transaction_id,
        transaction_date,
        amount,
        SUM(amount) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_date ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
    FROM transactions
    ORDER BY user_id ASC, transaction_date ASC;
    """
    df_task4 = pd.read_sql_query(query_task4, conn)
    print(df_task4.to_string(index=False))

    user_101_totals = list(df_task4[df_task4["user_id"] == 101]["running_total"])
    user_102_totals = list(df_task4[df_task4["user_id"] == 102]["running_total"])
    assert user_101_totals == [500.00, 800.00, 1500.00]
    assert user_102_totals == [1000.00, 1450.00, 2000.00]
    print("[OK] Task 4 passed: Window function computed cumulative running total resetting per user.")

    # -------------------------------------------------------------------------
    # TASK 5: Flipkart Query Performance Optimization & Execution Plan
    # -------------------------------------------------------------------------
    print("\n--- TASK 5: Query Optimization & EXPLAIN QUERY PLAN ---")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock INTEGER NOT NULL
        );
    """)

    sample_products = [
        (1, "Wireless Earbuds", "Electronics", 1499.00, 50),
        (2, "Smart Watch", "Electronics", 2999.00, 30),
        (3, "Bluetooth Speaker", "Electronics", 1899.00, 40),
        (4, "Gaming Laptop", "Electronics", 65000.00, 10),
        (5, "Running Shoes", "Footwear", 2499.00, 100),
        (6, "Cotton T-Shirt", "Apparel", 699.00, 200)
    ]
    cursor.executemany("INSERT INTO products (product_id, title, category, price, stock) VALUES (?, ?, ?, ?, ?);", sample_products)
    conn.commit()

    # Optimization 1: Create Composite Index on (category, price)
    cursor.execute("CREATE INDEX idx_products_category_price ON products (category, price);")
    conn.commit()

    # Check execution plan
    explain_df = pd.read_sql_query("""
        EXPLAIN QUERY PLAN
        SELECT product_id, title, price, category 
        FROM products 
        WHERE category = 'Electronics' AND price BETWEEN 1000 AND 5000;
    """, conn)
    print("Execution Plan Output:")
    print(explain_df.to_string(index=False))

    plan_details = " ".join(explain_df["detail"].tolist())
    assert "idx_products_category_price" in plan_details, "Query planner should use the composite index."
    print("[OK] Task 5 passed: Composite index successfully utilized in Query Execution Plan.")

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 18 tasks verified successfully!")
    print("=" * 75)


if __name__ == "__main__":
    main()
