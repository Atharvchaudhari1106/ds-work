# Session 16: SQL Project – Sales Analysis

**Course:** Working with Databases & SQL Basics  
**Directory:** `assignment-2/session-16-sql-project-sales-analysis/`  
**Database File:** `sales_analysis.db`  
**Dataset File:** `food_orders.csv`  
**Execution Environment:** Python 3.12, SQLite 3.49, Pandas 3.1  
**Status:** ✅ Completed, Verified & Executed

---

## 📌 Project Overview
This project consolidates SQL database design, CSV dataset ingestion, aggregate metrics analysis, customer profiling, and dashboard reporting into an end-to-end sales analytics pipeline.

### Core Objectives:
1. **CSV Ingestion (Task 1):** Ingest raw transaction logs (`food_orders.csv`) into a structured SQL relational table (`FoodOrders`).
2. **Music Catalog Schema (Task 2):** Create and populate `TopSongs` with 5 popular Spotify streaming records.
3. **VIP Customer Identification (Task 3):** Determine the top 3 highest-spending customers using grouped aggregate order amounts.
4. **Restaurant Performance Reporting (Task 4):** Quantify order volume and Gross Merchandise Value (GMV) per restaurant brand.
5. **Dashboard KPIs (Task 5):** Format key business KPIs (`Average Order Amount` and `Total Unique Customers`) into a standardized two-column key-value format (`kpi_name`, `kpi_value`) using `UNION ALL`.

---

## 📂 Deliverables & File Structure

```text
assignment-2/session-16-sql-project-sales-analysis/
├── session_16_sql_project_sales_analysis.ipynb # Executed interactive notebook (Tasks 1-5)
├── solution.sql                               # Production SQL script (DDL, DML, and analytics queries)
├── setup_and_verify.py                        # Automated end-to-end verification test runner
├── food_orders.csv                            # Source food delivery orders dataset
├── sales_analysis.db                          # Pre-built SQLite database (FoodOrders & TopSongs)
└── README.md                                  # Complete task walkthrough & analytics documentation
```

---

## 📋 Task Walkthrough & Verified Solutions

### Task 1: Ingesting `food_orders.csv` into `FoodOrders`
> **Task 1:** Import a CSV file of food delivery orders (with columns like `order_id`, `restaurant_name`, `customer_name`, `order_amount`, `order_date`) into a new SQL table named `FoodOrders` using your database tool of choice.

#### DDL Definition (`solution.sql`):
```sql
DROP TABLE IF EXISTS FoodOrders;

CREATE TABLE FoodOrders (
    order_id INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    order_amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL
);
```

#### Python Ingestion Pipeline (`setup_and_verify.py`):
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("sales_analysis.db")
df_csv = pd.read_csv("food_orders.csv")
df_csv.to_sql("FoodOrders", conn, if_exists="append", index=False)
```

#### First 5 Ingested Records:
| order_id | restaurant_name | customer_name | order_amount | order_date |
| :---: | :--- | :--- | :---: | :---: |
| 1 | Burger King | Rahul Sharma | 350.00 | 2026-03-01 |
| 2 | Subway | Amit Verma | 300.00 | 2026-03-02 |
| 3 | Burger King | Priya Patel | 450.00 | 2026-03-03 |
| 4 | Pizza Hut | Rahul Sharma | 650.00 | 2026-03-04 |
| 5 | Starbucks | Amit Verma | 420.00 | 2026-03-05 |

---

### Task 2: Creating `TopSongs` & Inserting Spotify Records
> **Task 2:** Write SQL statements to create a table called `TopSongs` with columns: `song_id`, `song_title`, `artist`, `streams`, and `release_date`, then insert at least 5 records representing popular tracks from Spotify.

#### SQL Implementation:
```sql
DROP TABLE IF EXISTS TopSongs;

CREATE TABLE TopSongs (
    song_id INTEGER PRIMARY KEY,
    song_title TEXT NOT NULL,
    artist TEXT NOT NULL,
    streams BIGINT NOT NULL,
    release_date DATE NOT NULL
);

INSERT INTO TopSongs (song_id, song_title, artist, streams, release_date) VALUES
(1, 'Blinding Lights', 'The Weeknd', 4200000000, '2019-11-29'),
(2, 'Shape of You', 'Ed Sheeran', 3800000000, '2017-01-06'),
(3, 'Someone You Loved', 'Lewis Capaldi', 3300000000, '2018-11-08'),
(4, 'Sunflower', 'Post Malone & Swae Lee', 3200000000, '2018-10-19'),
(5, 'As It Was', 'Harry Styles', 3100000000, '2022-04-01');
```

#### Query Output (`ORDER BY streams DESC`):
| song_id | song_title | artist | streams | release_date |
| :---: | :--- | :--- | :---: | :---: |
| 1 | Blinding Lights | The Weeknd | 4,200,000,000 | 2019-11-29 |
| 2 | Shape of You | Ed Sheeran | 3,800,000,000 | 2017-01-06 |
| 3 | Someone You Loved | Lewis Capaldi | 3,300,000,000 | 2018-11-08 |
| 4 | Sunflower | Post Malone & Swae Lee | 3,200,000,000 | 2018-10-19 |
| 5 | As It Was | Harry Styles | 3,100,000,000 | 2022-04-01 |

---

### Task 3: VIP Customer Segmentation (Top 3 Customers by Spend)
> **Task 3:** Write an SQL query to find the top 3 customers who ordered the most from the `FoodOrders` table based on total `order_amount`, and display their names and total spent.

#### SQL Implementation:
```sql
SELECT 
    customer_name,
    ROUND(SUM(order_amount), 2) AS total_spent
FROM FoodOrders
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 3;
```

#### Query Output:
| Rank | customer_name | total_spent | Orders Summary |
| :---: | :--- | :---: | :--- |
| 🥇 1 | **Sneha Reddy** | **₹2,600.00** | Orders: ₹900 (Biryani By Kilo), ₹1,100 (Behrouz), ₹600 (Pizza Hut) |
| 🥈 2 | **Priya Patel** | **₹2,150.00** | Orders: ₹450 (Burger King), ₹750 (Biryani By Kilo), ₹950 (Behrouz) |
| 🥉 3 | **Rohan Gupta** | **₹1,950.00** | Orders: ₹500 (Burger King), ₹850 (Behrouz), ₹600 (Subway) |

---

### Task 4: Product / Restaurant Performance Report
> **Task 4:** Generate a product performance report by writing an SQL query that lists each `restaurant_name` from `FoodOrders`, the number of orders, and the total `order_amount`, ordered by total `order_amount` descending.  
> *Hint: Use `GROUP BY` and `ORDER BY` clauses.*

#### SQL Implementation:
```sql
SELECT 
    restaurant_name,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_amount), 2) AS total_order_amount
FROM FoodOrders
GROUP BY restaurant_name
ORDER BY total_order_amount DESC;
```

#### Query Output:
| restaurant_name | total_orders | total_order_amount | % of Platform GMV |
| :--- | :---: | :---: | :---: |
| **Behrouz Biryani** | 4 | **₹3,700.00** | 32.98% |
| **Pizza Hut** | 3 | **₹1,730.00** | 15.42% |
| **Biryani By Kilo** | 2 | **₹1,650.00** | 14.71% |
| **Subway** | 4 | **₹1,550.00** | 13.81% |
| **Burger King** | 3 | **₹1,300.00** | 11.59% |
| **Starbucks** | 2 | **₹770.00** | 6.86% |
| **Haldiram's** | 1 | **₹520.00** | 4.63% |

---

### Task 5: Executive Dashboard KPIs (`kpi_name`, `kpi_value`)
> **Task 5:** Create an SQL query that calculates two KPIs for the `FoodOrders` table: (1) average `order_amount` and (2) total number of unique customers, and format the output for dashboard display (two columns: `kpi_name`, `kpi_value`).

#### SQL Implementation (`UNION ALL` Normalized Key-Value Layout):
```sql
SELECT 
    'Average Order Amount' AS kpi_name,
    CAST(ROUND(AVG(order_amount), 2) AS TEXT) AS kpi_value
FROM FoodOrders

UNION ALL

SELECT 
    'Total Unique Customers' AS kpi_name,
    CAST(COUNT(DISTINCT customer_name) AS TEXT) AS kpi_value
FROM FoodOrders;
```

#### Query Output:
| kpi_name | kpi_value | Analytical Interpretation |
| :--- | :---: | :--- |
| **Average Order Amount** | **590.53** | Platform Average Basket Size / AOV (Gross ₹11,220 ÷ 19 orders) |
| **Total Unique Customers** | **7** | Unique transacting user base across period |

---

## ⚡ Automated Verification Command

Run the self-contained verification suite directly from your terminal:

```powershell
python assignment-2/session-16-sql-project-sales-analysis/setup_and_verify.py
```
