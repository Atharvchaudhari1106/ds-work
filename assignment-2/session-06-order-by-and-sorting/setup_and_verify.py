"""
Session 6: ORDER BY + Sorting
Execution & Verification Script

Demonstrates and verifies:
- Task 1: Products sorted by price ASC (lowest to highest - Flipkart style)
- Task 2: Top 5 most expensive products using ORDER BY DESC and LIMIT
- Task 3: Movies multi-column sorting (release_year DESC, rating DESC)
- Task 4: First 10 restaurants sorted alphabetically (A-Z - Zomato style)
- Task 5: Top 3 trending songs sorted by play_count DESC with added_at DESC tie-breaker
"""

import sqlite3
import os
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "sorting_app.db")

def main():
    print("=" * 75)
    print("SESSION 6: ORDER BY + Sorting - Automated Verification")
    print("=" * 75)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Task 1 & 2: Products Table
    # ---------------------------------------------------------
    print("\n[TASK 1 & 2] Creating 'products' table and inserting catalog...")
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
    """)

    products_data = [
        (1, 'Boat Rockerz 450 Headphone', 'Electronics', 1499.00),
        (2, 'Apple iPhone 15', 'Mobiles', 71999.00),
        (3, 'Cotton Casual Shirt', 'Fashion', 799.00),
        (4, 'Samsung Galaxy S24', 'Mobiles', 79999.00),
        (5, 'Sony WH-1000XM5 Headset', 'Electronics', 28990.00),
        (6, 'Fastrack Analog Watch', 'Fashion', 1250.00),
        (7, 'MacBook Air M2', 'Laptops', 94990.00),
        (8, 'Logitech Wireless Mouse', 'Accessories', 599.00)
    ]
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?);", products_data)
    conn.commit()
    print("[OK] Products table created and 8 records inserted.")

    print("\n--- [TASK 1] Output: Products Sorted by Price (Lowest to Highest) ---")
    df_t1 = pd.read_sql_query("SELECT * FROM products ORDER BY price ASC;", conn)
    print(df_t1.to_string(index=False))

    print("\n--- [TASK 2] Output: Top 5 Most Expensive Products (Price DESC LIMIT 5) ---")
    df_t2 = pd.read_sql_query("SELECT * FROM products ORDER BY price DESC LIMIT 5;", conn)
    print(df_t2.to_string(index=False))

    # ---------------------------------------------------------
    # Task 3: Movies Multi-Column Sorting
    # ---------------------------------------------------------
    print("\n[TASK 3] Creating 'movies' table and querying sorted by release_year DESC, rating DESC...")
    cursor.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            release_year INTEGER NOT NULL,
            rating DECIMAL(3, 1) NOT NULL
        );
    """)

    movies_data = [
        (1, 'Oppenheimer', 2023, 8.9),
        (2, 'Barbie', 2023, 7.3),
        (3, 'Dune: Part Two', 2024, 8.6),
        (4, 'Furiosa', 2024, 7.6),
        (5, 'Interstellar', 2014, 8.7),
        (6, 'Inception', 2010, 8.8),
        (7, 'Spider-Man: Across the Spider-Verse', 2023, 8.7)
    ]
    cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?);", movies_data)
    conn.commit()

    query_t3 = """
        SELECT title, release_year, rating
        FROM movies
        ORDER BY release_year DESC, rating DESC;
    """
    df_t3 = pd.read_sql_query(query_t3, conn)
    print(df_t3.to_string(index=False))

    # ---------------------------------------------------------
    # Task 4: First 10 Restaurants Alphabetically
    # ---------------------------------------------------------
    print("\n[TASK 4] Creating 'restaurants' table and querying first 10 alphabetically...")
    cursor.execute("""
        CREATE TABLE restaurants (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cuisine VARCHAR(100) NOT NULL,
            rating DECIMAL(2, 1) NOT NULL,
            city VARCHAR(100) NOT NULL
        );
    """)

    restaurants_data = [
        (1, 'Swagat Restaurant', 'South Indian', 4.3, 'Ahmedabad'),
        (2, 'Barbeque Nation', 'Buffet / BBQ', 4.4, 'Ahmedabad'),
        (3, 'Cafe De Bistro', 'Continental', 3.9, 'Surat'),
        (4, "Domino's Pizza", 'Italian / Fast Food', 4.1, 'Ahmedabad'),
        (5, "Haldiram's", 'North Indian / Sweets', 4.2, 'Vadodara'),
        (6, 'Little Italy', 'Italian', 4.6, 'Ahmedabad'),
        (7, 'Mainland China', 'Chinese', 4.0, 'Ahmedabad'),
        (8, 'Punjab Grill', 'North Indian', 4.5, 'Surat'),
        (9, 'Sankalp', 'South Indian', 4.2, 'Surat'),
        (10, 'The Chocolate Room', 'Desserts', 4.3, 'Ahmedabad'),
        (11, 'Zaffran', 'Mughlai', 4.1, 'Vadodara'),
        (12, 'Agashiye', 'Gujarati Heritage', 4.8, 'Ahmedabad')
    ]
    cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?, ?, ?);", restaurants_data)
    conn.commit()

    query_t4 = "SELECT * FROM restaurants ORDER BY name ASC LIMIT 10;"
    df_t4 = pd.read_sql_query(query_t4, conn)
    print(df_t4.to_string(index=False))

    # ---------------------------------------------------------
    # Task 5: Top 3 Trending Songs with Tie-Breaker
    # ---------------------------------------------------------
    print("\n[TASK 5] Creating 'songs' table and querying top 3 trending with added_at tie-breaker...")
    cursor.execute("""
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            play_count INTEGER NOT NULL,
            added_at TIMESTAMP NOT NULL
        );
    """)

    songs_data = [
        (1, 'Starboy', 'The Weeknd', 1500000, '2026-10-15 10:00:00'),
        (2, 'Brown Munde', 'AP Dhillon', 2100000, '2026-10-18 12:00:00'),
        (3, 'Blinding Lights', 'The Weeknd', 2100000, '2026-10-22 14:30:00'),
        (4, 'Levitating', 'Dua Lipa', 1800000, '2026-10-20 09:15:00'),
        (5, 'Tum Hi Ho', 'Arijit Singh', 1950000, '2026-10-19 16:45:00')
    ]
    cursor.executemany("INSERT INTO songs VALUES (?, ?, ?, ?, ?);", songs_data)
    conn.commit()

    query_t5 = """
        SELECT * 
        FROM songs
        ORDER BY play_count DESC, added_at DESC
        LIMIT 3;
    """
    df_t5 = pd.read_sql_query(query_t5, conn)
    print(df_t5.to_string(index=False))

    conn.close()
    print("\n[OK] All Session 6 tasks verified successfully!")

if __name__ == "__main__":
    main()
