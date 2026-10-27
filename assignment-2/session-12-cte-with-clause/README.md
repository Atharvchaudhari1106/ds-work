# Session 12: CTE (WITH Clause)

## Overview & Objectives
This session covers **Common Table Expressions (CTEs)** and the **`WITH`** clause in SQL:
1. **Single CTEs**: Modularizing filtering logic into named tabular expressions (e.g. Flipkart/Myntra top-rated products).
2. **Subquery vs CTE Comparison**: Contrasting inside-out subqueries with top-to-bottom CTEs for query readability and maintainability.
3. **Multiple CTEs**: Combining multiple independent business entities (e.g. Instagram top-followed users and top-liked posts) in a single query via `UNION ALL`.
4. **Recursive CTEs (`WITH RECURSIVE`)**: Generating dynamic sequences, calendars, and hierarchical tree traversals (e.g. BookMyShow next 7 days booking dates).
5. **Query Refactoring**: Converting messy, convoluted nested subqueries into clean, maintainable, and modular production SQL.

---

## Task Solutions & Code Explanations

### Task 1: Basic CTE with WITH Clause (Flipkart/Myntra Top-Rated Products)
**Requirement:** Create a CTE using the `WITH` clause to select all products with a rating above 4.5 from a `Products` table, similar to how Flipkart or Myntra might highlight top-rated items.

```sql
DROP TABLE IF EXISTS Products;

CREATE TABLE Products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL
);

INSERT INTO Products (id, name, category, price, rating) VALUES
(1, 'Sony WH-1000XM5 Wireless Headphones', 'Electronics', 28990.00, 4.8),
(2, 'Apple iPhone 15 Pro', 'Electronics', 129900.00, 4.7),
(3, 'Nike Air Jordan 1 Retro', 'Footwear', 11995.00, 4.9),
(4, 'Levi''s 511 Slim Fit Jeans', 'Fashion', 2999.00, 4.2),
(5, 'Puma Mens Running Shoes', 'Footwear', 3499.00, 4.1),
(6, 'Samsung Galaxy S24 Ultra', 'Electronics', 129999.00, 4.6),
(7, 'Fossil Gen 6 Smartwatch', 'Accessories', 14995.00, 4.0),
(8, 'Ray-Ban Wayfarer Classic', 'Accessories', 8590.00, 4.6);

-- CTE Query:
WITH TopRatedProducts AS (
    SELECT 
        id AS product_id,
        name AS product_name,
        category,
        price,
        rating
    FROM Products
    WHERE rating > 4.5
)
SELECT * FROM TopRatedProducts
ORDER BY rating DESC, price ASC;
```

#### Output:
| product_id | product_name | category | price | rating |
|---|---|---|---|---|
| 3 | Nike Air Jordan 1 Retro | Footwear | 11995.00 | 4.9 |
| 1 | Sony WH-1000XM5 Wireless Headphones | Electronics | 28990.00 | 4.8 |
| 2 | Apple iPhone 15 Pro | Electronics | 129900.00 | 4.7 |
| 8 | Ray-Ban Wayfarer Classic | Accessories | 8590.00 | 4.6 |
| 6 | Samsung Galaxy S24 Ultra | Electronics | 129999.00 | 4.6 |

---

### Task 2: Subquery vs CTE Comparison (Ahmedabad Restaurants with Delivery < 50)
**Requirement:** Rewrite a query that finds all restaurants in 'Ahmedabad' with delivery charges under 50 from a `Restaurants` table, first using a subquery and then using a CTE. Compare both queries for readability.

#### Version A: Derived Table Subquery
```sql
SELECT restaurant_name, city, cuisine, delivery_charge, rating
FROM (
    SELECT name AS restaurant_name, city, cuisine, delivery_charge, rating
    FROM Restaurants
    WHERE city = 'Ahmedabad'
) AS AhmedabadRestaurants
WHERE delivery_charge < 50.00
ORDER BY delivery_charge ASC;
```

#### Version B: Clean Common Table Expression (CTE)
```sql
WITH AhmedabadRestaurants AS (
    SELECT name AS restaurant_name, city, cuisine, delivery_charge, rating
    FROM Restaurants
    WHERE city = 'Ahmedabad'
)
SELECT restaurant_name, city, cuisine, delivery_charge, rating
FROM AhmedabadRestaurants
WHERE delivery_charge < 50.00
ORDER BY delivery_charge ASC;
```

#### Output:
| restaurant_name | city | cuisine | delivery_charge | rating |
|---|---|---|---|---|
| Manek Chowk Delights | Ahmedabad | Street Food | 30.00 | 4.6 |
| Agashiye - House of MG | Ahmedabad | Gujarati Thali | 40.00 | 4.8 |
| Swati Snacks | Ahmedabad | Chaat & Snacks | 45.00 | 4.5 |

#### Readability Comparison:
1. **Cognitive Flow:** The CTE version reads in natural narrative order: *"First, create the Ahmedabad dataset; second, filter for affordable delivery."* In contrast, the subquery requires reading from the inside out.
2. **Maintenance:** CTEs can be referenced multiple times without code repetition or subquery duplication.
3. **Isolation & Testing:** Developers can debug individual CTE stages by swapping `SELECT * FROM <CTEName>`.

---

### Task 3: Multiple CTEs in a Single Query (Instagram Top Users & Top Posts)
**Requirement:** Using two CTEs in a single query, find the top 3 most-followed users and the top 3 most-liked posts from a `Users` and `Posts` table (think Instagram-style data). Output both lists in the same result set.

```sql
WITH TopFollowedUsers AS (
    SELECT 
        'Most Followed User' AS metric_category,
        username AS entity_name,
        followers_count AS metric_value
    FROM Users
    ORDER BY followers_count DESC
    LIMIT 3
),
TopLikedPosts AS (
    SELECT 
        'Most Liked Post' AS metric_category,
        caption AS entity_name,
        likes_count AS metric_value
    FROM Posts
    ORDER BY likes_count DESC
    LIMIT 3
)
SELECT * FROM TopFollowedUsers
UNION ALL
SELECT * FROM TopLikedPosts;
```

#### Output:
| metric_category | entity_name | metric_value |
|---|---|---|
| Most Followed User | virat.kohli | 270,000,000 |
| Most Followed User | priyanka.chopra | 91,000,000 |
| Most Followed User | alia.bhatt | 85,000,000 |
| Most Liked Post | Historic victory at MCG! Proud of the boys. | 5,800,000 |
| Most Liked Post | Match day ready. Always grateful. | 4,200,000 |
| Most Liked Post | Unforgettable night at the Met Gala 2026. | 3,900,000 |

---

### Task 4: Recursive CTE for Next 7 Days (BookMyShow Movie Booking Dates)
**Requirement:** Write a recursive CTE that generates a list of dates for the next 7 days starting from today, similar to how BookMyShow shows available dates for movie bookings. (*Hint: Use a base case for today and recursion to add one day at a time.*)

```sql
WITH RECURSIVE BookingDates AS (
    -- Base Case: Day 1 (Today)
    SELECT 
        1 AS day_number,
        DATE('now') AS booking_date
    UNION ALL
    -- Recursive Member: Add +1 day iteratively
    SELECT 
        day_number + 1,
        DATE(booking_date, '+1 day')
    FROM BookingDates
    WHERE day_number < 7
)
SELECT 
    day_number,
    booking_date AS iso_date,
    strftime('%d-%m-%Y', booking_date) AS formatted_date,
    CASE strftime('%w', booking_date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS day_of_week
FROM BookingDates;
```

#### Output:
| day_number | iso_date | formatted_date | day_of_week |
|---|---|---|---|
| 1 | 2026-10-27 | 27-10-2026 | Tuesday |
| 2 | 2026-10-28 | 28-10-2026 | Wednesday |
| 3 | 2026-10-29 | 29-10-2026 | Thursday |
| 4 | 2026-10-30 | 30-10-2026 | Friday |
| 5 | 2026-10-31 | 31-10-2026 | Saturday |
| 6 | 2026-11-01 | 01-11-2026 | Sunday |
| 7 | 2026-11-02 | 02-11-2026 | Monday |

---

### Task 5: Refactoring a Messy Query Using CTEs for Clarity & Maintainability
**Requirement:** Given a messy SQL query that finds all users with more than 1000 followers from a `Users` table, refactor it to use a CTE for better clarity and maintainability.

#### Messy Original Query:
```sql
SELECT u.id, u.username, u.followers_count, u.account_status
FROM (
    SELECT * FROM (
        SELECT id, username, followers_count, account_status
        FROM Users
        WHERE account_status = 'Active'
    ) AS active_sub
    WHERE active_sub.followers_count > 1000
) AS u
WHERE u.id IN (
    SELECT user_id FROM (
        SELECT id AS user_id, followers_count FROM Users WHERE followers_count > 1000
    ) AS follower_sub
)
ORDER BY u.followers_count DESC;
```

#### Clean Refactored CTE Query:
```sql
WITH ActiveInfluencerUsers AS (
    SELECT 
        id AS user_id,
        username,
        followers_count,
        account_status
    FROM Users
    WHERE account_status = 'Active'
      AND followers_count > 1000
)
SELECT 
    user_id,
    username,
    followers_count,
    account_status
FROM ActiveInfluencerUsers
ORDER BY followers_count DESC;
```

#### Output:
| user_id | username | followers_count | account_status |
|---|---|---|---|
| 1 | virat.kohli | 270,000,000 | Active |
| 2 | priyanka.chopra | 91,000,000 | Active |
| 3 | alia.bhatt | 85,000,000 | Active |
| 4 | tech_reviewer | 500,000 | Active |
| 5 | daily_foodie | 250,000 | Active |

#### Key Benefits of the Refactoring:
- Eliminates 3 layers of redundant inline subqueries and repeated table lookups.
- Introduces self-documenting semantic naming (`ActiveInfluencerUsers`).
- Reduces maintenance risk by keeping filter conditions in a single place.

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-12-cte-with-clause/solution.sql): Executable SQL queries for Tasks 1 to 5.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-12-cte-with-clause/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_12_cte_with_clause.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-12-cte-with-clause/session_12_cte_with_clause.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`cte_demo.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-12-cte-with-clause/cte_demo.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-12-cte-with-clause/README.md): Comprehensive documentation.
