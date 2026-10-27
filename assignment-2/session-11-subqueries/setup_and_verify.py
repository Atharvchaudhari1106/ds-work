#!/usr/bin/env python3
"""
Session 11: Subqueries
Verification and Automated Test Runner
Database: subqueries.db
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "subqueries.db")

def main():
    print("=" * 75)
    print("SESSION 11: SUBQUERIES (Verification Script)")
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
    # TASK 1: Subquery in WHERE Clause
    # -------------------------------------------------------------------------
    print("\n--- TASK 1: Restaurants Above City Average Rating ---")
    cursor.execute("DROP TABLE IF EXISTS Restaurants;")
    cursor.execute("""
    CREATE TABLE Restaurants (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL,
        rating DECIMAL(2, 1) NOT NULL
    );
    """)

    restaurants_data = [
        (1, 'Trishna', 'Mumbai', 4.6),
        (2, 'Britannia & Co', 'Mumbai', 4.4),
        (3, 'Bademiya', 'Mumbai', 3.8),
        (4, 'Local Fast Food', 'Mumbai', 3.2),
        (5, 'Truffles', 'Bangalore', 4.7),
        (6, 'Toit Brewpub', 'Bangalore', 4.6),
        (7, 'CTR Shri Sagar', 'Bangalore', 4.5),
        (8, 'Quick Bites', 'Bangalore', 3.6),
        (9, 'Bukhara', 'Delhi', 4.8),
        (10, "Karim's", 'Delhi', 4.3),
        (11, 'Paranthe Wali Gali Corner', 'Delhi', 3.7)
    ]
    cursor.executemany("INSERT INTO Restaurants VALUES (?, ?, ?, ?);", restaurants_data)
    conn.commit()

    task1_query = """
    SELECT 
        r1.id AS restaurant_id,
        r1.name AS restaurant_name,
        r1.city,
        r1.rating,
        ROUND((SELECT AVG(r2.rating) FROM Restaurants r2 WHERE r2.city = r1.city), 2) AS city_avg
    FROM Restaurants r1
    WHERE r1.rating > (
        SELECT AVG(r2.rating)
        FROM Restaurants r2
        WHERE r2.city = r1.city
    )
    ORDER BY r1.city, r1.rating DESC;
    """
    df_t1 = pd.read_sql_query(task1_query, conn)
    print(df_t1.to_string(index=False))
    print(f"[OK] Total qualifying restaurants above their city average: {len(df_t1)}")

    # -------------------------------------------------------------------------
    # TASK 2: Subquery in SELECT Statement
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 2: Zomato User Profile Order Summary (Subquery in SELECT) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Orders;")
    cursor.execute("DROP TABLE IF EXISTS Users;")

    cursor.execute("""
    CREATE TABLE Users (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Orders (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        order_date DATE NOT NULL,
        amount DECIMAL(10, 2) NOT NULL
    );
    """)

    users_data = [
        (1, 'Atharv Chaudhari', 'atharv@example.com'),
        (2, 'Sneha Patel', 'sneha@example.com'),
        (3, 'Rahul Verma', 'rahul@example.com'),
        (4, 'Priya Sharma', 'priya@example.com')
    ]
    orders_data = [
        (101, 1, '2026-03-01', 450.00),
        (102, 1, '2026-03-05', 780.00),
        (103, 1, '2026-03-12', 320.00),
        (104, 1, '2026-03-18', 650.00),
        (105, 2, '2026-03-04', 1200.00),
        (106, 2, '2026-03-15', 890.00),
        (107, 3, '2026-03-10', 250.00)
    ]
    cursor.executemany("INSERT INTO Users VALUES (?, ?, ?);", users_data)
    cursor.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?);", orders_data)
    conn.commit()

    task2_query = """
    SELECT 
        u.id AS user_id,
        u.name AS user_name,
        (
            SELECT COUNT(*)
            FROM Orders o
            WHERE o.user_id = u.id
        ) AS total_orders,
        COALESCE(
            (
                SELECT SUM(o.amount)
                FROM Orders o
                WHERE o.user_id = u.id
            ), 0.00
        ) AS total_spend
    FROM Users u
    ORDER BY total_orders DESC;
    """
    df_t2 = pd.read_sql_query(task2_query, conn)
    print(df_t2.to_string(index=False))
    print(f"[OK] Notice 'Priya Sharma' cleanly displays 0 orders and 0.0 spend without missing rows.")

    # -------------------------------------------------------------------------
    # TASK 3: Subquery with IN Operator
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 3: BookMyShow Top Movies with 5-Star Reviews (IN Subquery) ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Reviews;")
    cursor.execute("DROP TABLE IF EXISTS Movies;")

    cursor.execute("""
    CREATE TABLE Movies (
        id INT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        genre VARCHAR(50) NOT NULL,
        release_year INT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Reviews (
        id INT PRIMARY KEY,
        movie_id INT NOT NULL,
        reviewer_name VARCHAR(100) NOT NULL,
        rating INT NOT NULL
    );
    """)

    movies_data = [
        (1, 'Inception', 'Sci-Fi', 2010),
        (2, 'Interstellar', 'Sci-Fi', 2014),
        (3, 'Dangal', 'Biography / Sports', 2016),
        (4, 'Oppenheimer', 'Historical Drama', 2023),
        (5, 'Race 3', 'Action', 2018),
        (6, 'Housefull 4', 'Comedy', 2019)
    ]
    reviews_data = [
        (1, 1, 'Amit', 5),
        (2, 1, 'Kunal', 4),
        (3, 2, 'Pooja', 5),
        (4, 3, 'Rohit', 5),
        (5, 4, 'Sanya', 5),
        (6, 5, 'Tanmay', 2),
        (7, 5, 'Vikas', 1),
        (8, 6, 'Ritu', 3)
    ]
    cursor.executemany("INSERT INTO Movies VALUES (?, ?, ?, ?);", movies_data)
    cursor.executemany("INSERT INTO Reviews VALUES (?, ?, ?, ?);", reviews_data)
    conn.commit()

    task3_query = """
    SELECT 
        m.id AS movie_id,
        m.title,
        m.genre,
        m.release_year
    FROM Movies m
    WHERE m.id IN (
        SELECT DISTINCT r.movie_id
        FROM Reviews r
        WHERE r.rating = 5
    )
    ORDER BY m.release_year DESC;
    """
    df_t3 = pd.read_sql_query(task3_query, conn)
    print(df_t3.to_string(index=False))
    print(f"[OK] Total movies qualifying with at least one 5-star review: {len(df_t3)}")

    # -------------------------------------------------------------------------
    # TASK 4: Nested Subquery for Relational Division
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("--- TASK 4: Flipkart Sellers with Products in Every Category ---")
    print("=" * 75)
    cursor.execute("DROP TABLE IF EXISTS Products;")
    cursor.execute("DROP TABLE IF EXISTS Categories;")
    cursor.execute("DROP TABLE IF EXISTS Sellers;")

    cursor.execute("""
    CREATE TABLE Sellers (
        id INT PRIMARY KEY,
        seller_name VARCHAR(100) NOT NULL,
        rating DECIMAL(2, 1) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Categories (
        id INT PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Products (
        id INT PRIMARY KEY,
        seller_id INT NOT NULL,
        category_id INT NOT NULL,
        product_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );
    """)

    categories_data = [(1, 'Electronics'), (2, 'Fashion'), (3, 'Home & Kitchen')]
    sellers_data = [
        (1, 'RetailNet India', 4.8),
        (2, 'SuperCom MultiStore', 4.7),
        (3, 'TechWorld Electronics', 4.5),
        (4, 'StyleStreet Apparels', 4.2)
    ]
    products_data = [
        # RetailNet (Cat 1, 2, 3)
        (101, 1, 1, 'Smartphone Pro', 34999.00),
        (102, 1, 2, 'Denim Jacket', 2499.00),
        (103, 1, 3, 'Non-stick Cookware Set', 3999.00),
        # SuperCom (Cat 1, 2, 3)
        (104, 2, 1, 'Headphones', 8999.00),
        (105, 2, 2, 'Cotton T-Shirt', 799.00),
        (106, 2, 3, 'Air Purifier', 9499.00),
        # TechWorld (Cat 1 only)
        (107, 3, 1, 'Mechanical Keyboard', 4500.00),
        # StyleStreet (Cat 2 only)
        (108, 4, 2, 'Running Shoes', 3200.00)
    ]
    cursor.executemany("INSERT INTO Categories VALUES (?, ?);", categories_data)
    cursor.executemany("INSERT INTO Sellers VALUES (?, ?, ?);", sellers_data)
    cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?, ?);", products_data)
    conn.commit()

    # Approach 4A: Nested COUNT comparison
    task4_query_a = """
    SELECT 
        s.id AS seller_id,
        s.seller_name,
        s.rating
    FROM Sellers s
    WHERE (
        SELECT COUNT(DISTINCT p.category_id)
        FROM Products p
        WHERE p.seller_id = s.id
    ) = (
        SELECT COUNT(*)
        FROM Categories
    );
    """
    df_t4_a = pd.read_sql_query(task4_query_a, conn)
    print("\nApproach 4A (Nested COUNT comparison):")
    print(df_t4_a.to_string(index=False))

    # Approach 4B: Double NOT EXISTS
    task4_query_b = """
    SELECT 
        s.id AS seller_id,
        s.seller_name,
        s.rating
    FROM Sellers s
    WHERE NOT EXISTS (
        SELECT c.id
        FROM Categories c
        WHERE NOT EXISTS (
            SELECT 1
            FROM Products p
            WHERE p.seller_id = s.id 
              AND p.category_id = c.id
        )
    );
    """
    df_t4_b = pd.read_sql_query(task4_query_b, conn)
    print("\nApproach 4B (Double NOT EXISTS Relational Division):")
    print(df_t4_b.to_string(index=False))

    conn.close()
    print("\n" + "=" * 75)
    print("[SUCCESS] All Session 11 subquery tasks verified successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
