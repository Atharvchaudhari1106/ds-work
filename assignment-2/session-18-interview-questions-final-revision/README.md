# Session 18: Interview Questions + Final Revision

**Course:** Working with Databases & SQL Basics  
**Directory:** `assignment-2/session-18-interview-questions-final-revision/`  
**Database File:** `interview_revision.db`  
**Execution Environment:** Python 3.12, SQLite 3.49, Pandas 3.1  
**Status:** ✅ Completed, Verified & Executed

---

## 📌 Session Overview
This final capstone revision consolidates the most frequent and impactful SQL technical interview topics asked across top technology firms (such as Flipkart, Amazon, Google, Swiggy, and Zomato):

1. **Aggregation & Post-Filter (`HAVING`):** Filtering groups after aggregation where `WHERE` is prohibited.
2. **Relational Join Semantics (`LEFT JOIN`):** Computing total user order value while gracefully handling users with zero orders using `COALESCE`.
3. **Subqueries (Uncorrelated Scalar):** Dynamically filtering records against a calculated statistical benchmark (e.g. above-average ratings).
4. **Window Functions (`SUM() OVER`):** Generating cumulative running totals partitioned per user chronologically.
5. **Database Indexing & Query Optimization:** Formulating composite B-Tree index strategies and SARGable query patterns to maximize throughput on high-scale catalog tables.

---

## 📂 Deliverables & File Structure

```text
assignment-2/session-18-interview-questions-final-revision/
├── session_18_interview_questions_final_revision.ipynb # Executed interactive notebook (Tasks 1-5)
├── solution.sql                                       # Production SQL script (DDL, DML, and queries)
├── setup_and_verify.py                                # Automated end-to-end verification test runner
├── interview_revision.db                              # Populated SQLite database
└── README.md                                          # Complete task walkthrough & interview guide
```

---

## 📋 Task Walkthrough & Verified Solutions

### Task 1: Songs Uploaded per Artist (`GROUP BY` & `HAVING`)
> **Task 1:** Write an SQL query to display the total number of songs uploaded by each artist from a table `songs` (columns: `song_id`, `artist_name`, `title`) and show only those artists who have uploaded more than 3 songs.

#### SQL Implementation:
```sql
SELECT 
    artist_name,
    COUNT(song_id) AS total_songs
FROM songs
GROUP BY artist_name
HAVING COUNT(song_id) > 3
ORDER BY total_songs DESC, artist_name ASC;
```

#### Query Output:
| artist_name | total_songs | Songs Included in Database |
| :--- | :---: | :--- |
| **Arijit Singh** | **5** | *Tum Hi Ho, Kesariya, Channa Mereya, Raabta, Kalank* |
| **Taylor Swift** | **4** | *Cruel Summer, Anti-Hero, Blank Space, Lover* |

*(Note: Ed Sheeran (3), The Weeknd (2), and Diljit Dosanjh (1) are correctly excluded by `HAVING COUNT(song_id) > 3`).*

---

### Task 2: Relational JOIN for Total Order Amount per User
> **Task 2:** Given two tables, `orders` (`order_id`, `user_id`, `amount`) and `users` (`user_id`, `username`), write a SQL JOIN query to display each `username` along with their total order amount.

#### SQL Implementation (`LEFT JOIN` Best Practice):
```sql
SELECT 
    u.username,
    COALESCE(SUM(o.amount), 0.00) AS total_order_amount
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username
ORDER BY total_order_amount DESC;
```

#### Query Output:
| username | total_order_amount | Orders Evaluated |
| :--- | :---: | :--- |
| **sneha_reddy** | **₹2,650.00** | Orders: ₹950 + ₹1,100 + ₹600 |
| **priya_patel** | **₹2,000.00** | Orders: ₹1,200 + ₹800 |
| **rahul_sharma** | **₹1,200.00** | Orders: ₹450 + ₹750 |
| **amit_verma** | **₹350.00** | Orders: ₹350 |
| **vikram_m** | **₹0.00** | No orders placed (`COALESCE` handles `NULL`) |

---

### Task 3: Above-Average Rated Restaurants (Scalar Subquery)
> **Task 3:** Write a SQL subquery to find the names of all restaurants from a `restaurants` table (`id`, `name`, `rating`) whose rating is higher than the average rating of all restaurants.

#### SQL Implementation:
```sql
SELECT 
    name,
    rating
FROM restaurants
WHERE rating > (
    SELECT AVG(rating) 
    FROM restaurants
)
ORDER BY rating DESC;
```

#### Query Output:
| name | rating | Benchmark Comparison |
| :--- | :---: | :--- |
| **Gulati** | **4.80** | > Overall Average (**4.17**) |
| **Toscano** | **4.60** | > Overall Average (**4.17**) |
| **Punjab Grill** | **4.50** | > Overall Average (**4.17**) |

*(Note: Haldirams (3.80), Subway (3.70), and Chai Point (3.60) are correctly filtered out).*

---

### Task 4: User Running Total (Window Function)
> **Task 4:** Using a `transactions` table (`id`, `user_id`, `amount`, `transaction_date`), write a SQL query with a window function to display each user's transaction amount and their running total (cumulative sum) ordered by `transaction_date`.

#### SQL Implementation:
```sql
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
```

#### Query Output:
| user_id | transaction_id | transaction_date | amount | running_total | Rolling Sum Accumulation |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **101** | 1 | 2026-03-01 | 500.00 | **500.00** | 500.00 |
| **101** | 2 | 2026-03-05 | 300.00 | **800.00** | 500.00 + 300.00 |
| **101** | 3 | 2026-03-10 | 700.00 | **1500.00** | 800.00 + 700.00 |
| **102** | 4 | 2026-03-02 | 1000.00 | **1000.00** | 1000.00 (Resets for user 102) |
| **102** | 5 | 2026-03-08 | 450.00 | **1450.00** | 1000.00 + 450.00 |
| **102** | 6 | 2026-03-15 | 550.00 | **2000.00** | 1450.00 + 550.00 |

---

### Task 5: Flipkart Product Query Optimization
> **Task 5:** List two optimizations you would apply to speed up a query that filters Flipkart products by category and price, and briefly explain how each helps.  
> *Hint: Think about indexes and query structure.*

Target query:
```sql
SELECT product_id, title, price, category 
FROM products 
WHERE category = 'Electronics' AND price BETWEEN 1000 AND 5000;
```

#### 1. Composite B-Tree Index on `(category, price)`
- **SQL Statement:**
  ```sql
  CREATE INDEX idx_products_category_price ON products (category, price);
  ```
- **Why it helps:**
  - **Index Seek with Bounded Range Scan:** In composite B-tree indexes, the leading column must be the **equality filter** (`category = 'Electronics'`) followed by the **range filter** (`price BETWEEN 1000 AND 5000`).
  - The query optimizer navigates directly to the `'Electronics'` subtree in $\mathcal{O}(\log N)$ time and reads sequentially only the price leaf pages within the $[1000, 5000]$ interval.
  - This completely eliminates an expensive **Full Table Scan (`SCAN TABLE`)**, avoiding disk I/O on unrelated product categories.

#### 2. SARGable Query Structure & Covering Indexes
- **Why it helps:**
  - **SARGability (Search Argument Able):** Never apply scalar functions or data-type conversions on indexed columns in the `WHERE` clause (e.g. avoid `WHERE LOWER(category) = 'electronics'` or `WHERE CAST(price AS INT) ...`), because function calls invalidate B-Tree traversal and force a full table scan.
  - **Covering Index (Index-Only Scan):** If the index includes the projected columns (`product_id`, `title`), the query engine satisfies the entire query from the index cache in memory without performing random I/O lookups to retrieve rows from the underlying heap table.

#### Execution Plan Verification (`EXPLAIN QUERY PLAN`):
```text
SEARCH products USING INDEX idx_products_category_price (category=? AND price>? AND price<?)
```

---

## ⚡ Automated Verification Command

Run the self-contained verification suite directly from your terminal:

```powershell
python assignment-2/session-18-interview-questions-final-revision/setup_and_verify.py
```
