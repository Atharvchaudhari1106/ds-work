# Session 6: ORDER BY + Sorting

This folder contains the complete solutions for **Session 6 - ORDER BY + Sorting** from the Data Science & Database coursework track (`assignment-2`).

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_06_order_by_and_sorting.ipynb`**](session_06_order_by_and_sorting.ipynb) | Complete self-contained notebook with pre-executed code cells, DataFrame outputs, and sorting logic guides |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL**, **PostgreSQL**, and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, runs sorting queries, and prints formatted results |
| **Sample SQLite Database** | [`sorting_app.db`](sorting_app.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Sort Products by Price Ascending (Lowest to Highest - Flipkart Style)
> **Problem Statement:** Write an SQL query to display all products from a `'products'` table and sort them by price in ascending order, similar to how Flipkart lists items from lowest to highest price.

#### SQL Schema Definition & Data Insertion:
```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO products (id, product_name, category, price) VALUES
(1, 'Boat Rockerz 450 Headphone', 'Electronics', 1499.00),
(2, 'Apple iPhone 15', 'Mobiles', 71999.00),
(3, 'Cotton Casual Shirt', 'Fashion', 799.00),
(4, 'Samsung Galaxy S24', 'Mobiles', 79999.00),
(5, 'Sony WH-1000XM5 Headset', 'Electronics', 28990.00),
(6, 'Fastrack Analog Watch', 'Fashion', 1250.00),
(7, 'MacBook Air M2', 'Laptops', 94990.00),
(8, 'Logitech Wireless Mouse', 'Accessories', 599.00);
```

#### SQL Query:
```sql
SELECT * 
FROM products
ORDER BY price ASC;
```

#### Output:
| id | product_name | category | price |
| :---: | :--- | :--- | :---: |
| **8** | Logitech Wireless Mouse | Accessories | 599.00 |
| **3** | Cotton Casual Shirt | Fashion | 799.00 |
| **6** | Fastrack Analog Watch | Fashion | 1,250.00 |
| **1** | Boat Rockerz 450 Headphone | Electronics | 1,499.00 |
| **5** | Sony WH-1000XM5 Headset | Electronics | 28,990.00 |
| **2** | Apple iPhone 15 | Mobiles | 71,999.00 |
| **4** | Samsung Galaxy S24 | Mobiles | 79,999.00 |
| **7** | MacBook Air M2 | Laptops | 94,990.00 |

---

### Task 2: Top 5 Most Expensive Products (`ORDER BY DESC LIMIT 5`)
> **Problem Statement:** Modify your previous query to show the top 5 most expensive products using `ORDER BY` with `DESC` and `LIMIT`.

#### SQL Query:
```sql
SELECT * 
FROM products
ORDER BY price DESC
LIMIT 5;
```

#### Output:
| id | product_name | category | price |
| :---: | :--- | :--- | :---: |
| **7** | MacBook Air M2 | Laptops | 94,990.00 |
| **4** | Samsung Galaxy S24 | Mobiles | 79,999.00 |
| **2** | Apple iPhone 15 | Mobiles | 71,999.00 |
| **5** | Sony WH-1000XM5 Headset | Electronics | 28,990.00 |
| **1** | Boat Rockerz 450 Headphone | Electronics | 1,499.00 |

---

### Task 3: Multi-Column Hierarchical Sort (`release_year DESC, rating DESC`)
> **Problem Statement:** Given a `'movies'` table with columns `'title'`, `'release_year'`, and `'rating'`, write an SQL query to list all movies sorted first by `release_year` in descending order (latest first), then by `rating` in descending order (highest rated first).

#### SQL Query:
```sql
SELECT title, release_year, rating
FROM movies
ORDER BY release_year DESC, rating DESC;
```

#### Output:
| title | release_year | rating |
| :--- | :---: | :---: |
| **Dune: Part Two** | 2024 | 8.6 |
| **Furiosa** | 2024 | 7.6 |
| **Oppenheimer** | 2023 | 8.9 |
| **Spider-Man: Across the Spider-Verse** | 2023 | 8.7 |
| **Barbie** | 2023 | 7.3 |
| **Interstellar** | 2014 | 8.7 |
| **Inception** | 2010 | 8.8 |

---

### Task 4: Alphabetical Restaurant Listing (`A-Z` with `LIMIT 10`)
> **Problem Statement:** Write an SQL query to display the first 10 restaurants from a `'restaurants'` table, sorted alphabetically by name, just like Zomato's A-Z listing.  
> *Hint: Use `ORDER BY` with `LIMIT`.*

#### SQL Query:
```sql
SELECT * 
FROM restaurants
ORDER BY name ASC
LIMIT 10;
```

#### Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **12** | Agashiye | Gujarati Heritage | 4.8 | Ahmedabad |
| **2** | Barbeque Nation | Buffet / BBQ | 4.4 | Ahmedabad |
| **3** | Cafe De Bistro | Continental | 3.9 | Surat |
| **4** | Domino's Pizza | Italian / Fast Food | 4.1 | Ahmedabad |
| **5** | Haldiram's | North Indian / Sweets | 4.2 | Vadodara |
| **6** | Little Italy | Italian | 4.6 | Ahmedabad |
| **7** | Mainland China | Chinese | 4.0 | Ahmedabad |
| **8** | Punjab Grill | North Indian | 4.5 | Surat |
| **9** | Sankalp | South Indian | 4.2 | Surat |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |

---

### Task 5: Top 3 Trending Songs with Tie-Breaker (`play_count DESC, added_at DESC`)
> **Problem Statement:** Suppose you want to display the top 3 trending songs from a `'songs'` table based on `play_count`, but if two songs have the same `play_count`, the more recently added song should come first. Write the SQL query to achieve this.  
> *Hint: Use `ORDER BY` with multiple columns.*

#### SQL Query:
```sql
SELECT * 
FROM songs
ORDER BY play_count DESC, added_at DESC
LIMIT 3;
```

#### Output:
| id | title | artist | play_count | added_at |
| :---: | :--- | :--- | :---: | :--- |
| **3** | **Blinding Lights** | The Weeknd | 2,100,000 | 2026-10-22 14:30:00 *(Added More Recently)* |
| **2** | **Brown Munde** | AP Dhillon | 2,100,000 | 2026-10-18 12:00:00 |
| **5** | **Tum Hi Ho** | Arijit Singh | 1,950,000 | 2026-10-19 16:45:00 |

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Runner:**
   ```powershell
   python assignment-2/session-06-order-by-and-sorting/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_06_order_by_and_sorting.ipynb`](session_06_order_by_and_sorting.ipynb) directly in VS Code / GitHub.
