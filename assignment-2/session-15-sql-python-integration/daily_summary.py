"""
Daily Summary Automation Script (Session 15, Task 5)

Connects to foodie.db, fetches all restaurants with rating > 4.5,
loads them into a Pandas DataFrame, and saves the result as top_rated_restaurants.csv.
"""

import os
import sqlite3
import pandas as pd


def generate_daily_summary(db_filename: str = "foodie.db", csv_filename: str = "top_rated_restaurants.csv"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, db_filename)
    csv_path = os.path.join(base_dir, csv_filename)

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)

    query = """
    SELECT id, name, cuisine, rating
    FROM Restaurants
    WHERE rating > 4.5
    ORDER BY rating DESC;
    """

    df_top = pd.read_sql_query(query, conn)
    conn.close()

    print(f"Retrieved {len(df_top)} restaurant(s) with rating > 4.5:")
    print(df_top.to_string(index=False))

    df_top.to_csv(csv_path, index=False)
    print(f"\n[SUCCESS] Daily summary saved to: {csv_path}")
    return df_top


if __name__ == "__main__":
    generate_daily_summary()
