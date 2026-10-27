# Session 17: SQL Project – HR Analysis (Restaurant & Reviews Analytics)

**Course:** Working with Databases & SQL Basics  
**Directory:** `assignment-2/session-17-sql-project-hr-analysis/`  
**Database File:** `restaurant_analytics.db`  
**Execution Environment:** Python 3.12, SQLite 3.49, Pandas 3.1  
**Status:** ✅ Completed, Verified & Executed

---

## 📌 Project Overview
This project consolidates relational database design, foreign key relationships, categorical aggregations, relational joins, and partitioned window ranking into an end-to-end analytics workflow.

*(Note: Although titled "HR Analysis" in the coursework curriculum portal, the operational tasks cover a comprehensive **Restaurant & Customer Reviews Analytics** data model simulating platforms like Zomato, Swiggy, and Yelp).*

### Core Objectives:
1. **Restaurant Entity Creation (Task 1):** Define and populate `Restaurant` with popular dining brands across diverse culinary cuisines.
2. **Cuisine Market Share (Task 2):** Aggregate and rank culinary categories by total restaurant count (`GROUP BY cuisine`, `ORDER BY restaurant_count DESC`).
3. **Relational Review Modeling (Task 3):** Implement the `Review` table with foreign key linkage (`restaurant_id`) to track customer sentiment.
4. **Multi-Table Sentiment Aggregation (Task 4):** Compute true customer ratings via `INNER JOIN`, multi-column `GROUP BY`, and `ROUND(AVG(rating), 2)`.
5. **Intra-Cuisine Leaderboards (Task 5):** Rank restaurants within each cuisine category using window functions (`DENSE_RANK() OVER (PARTITION BY cuisine ORDER BY average_rating DESC)`).

---

## 📂 Deliverables & File Structure

```text
assignment-2/session-17-sql-project-hr-analysis/
├── session_17_sql_project_hr_analysis.ipynb # Executed interactive notebook (Tasks 1-5)
├── solution.sql                            # Production SQL script (DDL, DML, and analytics queries)
├── setup_and_verify.py                     # Automated end-to-end verification test runner
├── restaurant_analytics.db                 # Pre-built SQLite database (Restaurant & Review)
└── README.md                               # Complete task walkthrough & analytics documentation
```

---

## 📋 Task Walkthrough & Verified Solutions

### Task 1: Creating `Restaurant` Table & Inserting Sample Records
> **Task 1:** Create a SQL table called `Restaurant` with columns: `id`, `name`, `cuisine`, `location`, and `average_rating`. Insert at least 5 sample rows representing popular restaurants from Zomato.

#### DDL & Ingestion (`solution.sql`):
```sql
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Restaurant;

CREATE TABLE Restaurant (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cuisine TEXT NOT NULL,
    location TEXT NOT NULL,
    average_rating DECIMAL(3, 2) NOT NULL CHECK (average_rating >= 0.0 AND average_rating <= 5.0)
);

INSERT INTO Restaurant (id, name, cuisine, location, average_rating) VALUES
(1, 'Punjab Grill', 'North Indian', 'Connaught Place', 4.50),
(2, 'Dhaba Estd 1986', 'North Indian', 'Cyber Hub', 4.30),
(3, 'Gulati', 'North Indian', 'Pandara Road', 4.70),
(4, 'Little Italy', 'Italian', 'Indiranagar', 4.40),
(5, 'Toscano', 'Italian', 'UB City', 4.60),
(6, 'Behrouz Biryani', 'Mughlai', 'Koramangala', 4.20),
(7, 'Biryani By Kilo', 'Mughlai', 'HSR Layout', 4.50);
```

#### Populated `Restaurant` Table:
| id | name | cuisine | location | average_rating |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Punjab Grill | North Indian | Connaught Place | 4.50 |
| 2 | Dhaba Estd 1986 | North Indian | Cyber Hub | 4.30 |
| 3 | Gulati | North Indian | Pandara Road | 4.70 |
| 4 | Little Italy | Italian | Indiranagar | 4.40 |
| 5 | Toscano | Italian | UB City | 4.60 |
| 6 | Behrouz Biryani | Mughlai | Koramangala | 4.20 |
| 7 | Biryani By Kilo | Mughlai | HSR Layout | 4.50 |

---

### Task 2: Cuisine Distribution Report
> **Task 2:** Write a SQL query to generate a report showing the number of restaurants for each cuisine type from your `Restaurant` table, ordered by the count in descending order.  
> *Hint: Use `GROUP BY` and `ORDER BY`.*

#### SQL Implementation:
```sql
SELECT 
    cuisine,
    COUNT(id) AS restaurant_count
FROM Restaurant
GROUP BY cuisine
ORDER BY restaurant_count DESC, cuisine ASC;
```

#### Query Output:
| cuisine | restaurant_count | Market Share |
| :--- | :---: | :---: |
| **North Indian** | **3** | 42.86% |
| **Italian** | **2** | 28.57% |
| **Mughlai** | **2** | 28.57% |

---

### Task 3: Creating `Review` Table & Ingesting Reviews
> **Task 3:** Add a new table called `Review` with columns: `id`, `restaurant_id`, `user_name`, `rating`, and `review_date`. Insert at least 10 sample reviews, linking them to restaurants using `restaurant_id`.

#### SQL Implementation:
```sql
CREATE TABLE Review (
    id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    rating DECIMAL(3, 2) NOT NULL CHECK (rating >= 0.0 AND rating <= 5.0),
    review_date DATE NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE CASCADE
);

INSERT INTO Review (id, restaurant_id, user_name, rating, review_date) VALUES
(1,  3, 'Aarav Sharma',   5.00, '2026-03-01'),
(2,  3, 'Diya Kapoor',    4.80, '2026-03-05'),
(3,  5, 'Rohan Verma',    4.80, '2026-03-02'),
(4,  5, 'Meera Nair',     4.60, '2026-03-06'),
(5,  1, 'Kabir Mehta',    4.50, '2026-03-03'),
(6,  1, 'Ananya Sen',     4.70, '2026-03-07'),
(7,  7, 'Siddharth Rao',  4.60, '2026-03-04'),
(8,  7, 'Pooja Hegde',    4.40, '2026-03-08'),
(9,  4, 'Vikram Singhal', 4.40, '2026-03-02'),
(10, 4, 'Ishaan Goel',    4.20, '2026-03-09'),
(11, 2, 'Neha Gupta',     4.20, '2026-03-01'),
(12, 2, 'Kunal Roy',      4.40, '2026-03-10'),
(13, 6, 'Tanvi Joshi',    4.10, '2026-03-04'),
(14, 6, 'Aditya Malik',   4.30, '2026-03-11');
```

---

### Task 4: Average Review Rating per Restaurant (JOIN & GROUP BY)
> **Task 4:** Write a SQL query using a `JOIN` to display each restaurant's `name`, `cuisine`, and its average review rating (from the `Review` table), ordered by highest average rating first.  
> *Hint: Use `JOIN` and `GROUP BY` with aggregate functions.*

#### SQL Implementation:
```sql
SELECT 
    r.name,
    r.cuisine,
    ROUND(AVG(rev.rating), 2) AS avg_review_rating
FROM Restaurant r
INNER JOIN Review rev ON r.id = rev.restaurant_id
GROUP BY r.id, r.name, r.cuisine
ORDER BY avg_review_rating DESC, r.name ASC;
```

#### Query Output:
| name | cuisine | avg_review_rating | User Reviews Included |
| :--- | :--- | :---: | :--- |
| **Gulati** | North Indian | **4.90** | [5.0, 4.8] |
| **Toscano** | Italian | **4.70** | [4.8, 4.6] |
| **Punjab Grill** | North Indian | **4.60** | [4.5, 4.7] |
| **Biryani By Kilo** | Mughlai | **4.50** | [4.6, 4.4] |
| **Dhaba Estd 1986** | North Indian | **4.30** | [4.2, 4.4] |
| **Little Italy** | Italian | **4.30** | [4.4, 4.2] |
| **Behrouz Biryani** | Mughlai | **4.20** | [4.1, 4.3] |

---

### Task 5: Ranking Restaurants within Each Cuisine using Window Functions
> **Task 5:** Use a window function to rank restaurants by their average review rating within each cuisine type, showing the restaurant name, cuisine, average rating, and rank.  
> *Hint: Use the `RANK()` or `DENSE_RANK()` window function partitioned by cuisine.*

#### SQL Implementation:
```sql
WITH RestaurantAverages AS (
    SELECT 
        r.name,
        r.cuisine,
        ROUND(AVG(rev.rating), 2) AS average_rating
    FROM Restaurant r
    INNER JOIN Review rev ON r.id = rev.restaurant_id
    GROUP BY r.id, r.name, r.cuisine
)
SELECT 
    name,
    cuisine,
    average_rating,
    DENSE_RANK() OVER (
        PARTITION BY cuisine 
        ORDER BY average_rating DESC
    ) AS rank
FROM RestaurantAverages
ORDER BY cuisine ASC, rank ASC;
```

#### Query Output:
| Cuisine | Restaurant Name | Average Rating | Rank within Cuisine |
| :--- | :--- | :---: | :---: |
| **Italian** | **Toscano** | **4.70** | **1** |
| Italian | Little Italy | 4.30 | 2 |
| **Mughlai** | **Biryani By Kilo** | **4.50** | **1** |
| Mughlai | Behrouz Biryani | 4.20 | 2 |
| **North Indian** | **Gulati** | **4.90** | **1** |
| North Indian | Punjab Grill | 4.60 | 2 |
| North Indian | Dhaba Estd 1986 | 4.30 | 3 |

---

## ⚡ Automated Verification Command

Run the self-contained verification suite directly from your terminal:

```powershell
python assignment-2/session-17-sql-project-hr-analysis/setup_and_verify.py
```
