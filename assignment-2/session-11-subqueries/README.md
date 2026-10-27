# Session 11: Subqueries

## Overview & Objectives
This session covers subqueries (nested SQL queries) across the most common real-world application paradigms:
1. **Subqueries in `WHERE` Clauses**: Dynamic filtering using correlated subqueries (e.g. restaurants rated above their local city average).
2. **Scalar Subqueries in `SELECT` Statements**: Aggregating child records directly inside column projections (e.g. Zomato user profile order count and spend summaries).
3. **Subqueries with `IN` / `NOT IN`**: Membership testing against dynamic result sets (e.g. BookMyShow movies with at least one 5-star review).
4. **Nested Subqueries for Relational Division**: Solving universal quantification ($R \div S$) problems using nested category counts and classical `NOT EXISTS` constructs (e.g. Flipkart sellers selling in every catalog category).

---

## Task Solutions & Code Explanations

### Task 1: Subquery in WHERE Clause (Restaurants Above City Average)
**Requirement:** Create a SQL query using a subquery in the `WHERE` clause to find all restaurants from a `Restaurants` table whose average rating is higher than the average rating of all restaurants in the city.

```sql
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL
);

INSERT INTO Restaurants (id, name, city, rating) VALUES
-- Mumbai Restaurants (City Avg = 4.00)
(1, 'Trishna', 'Mumbai', 4.6),
(2, 'Britannia & Co', 'Mumbai', 4.4),
(3, 'Bademiya', 'Mumbai', 3.8),
(4, 'Local Fast Food', 'Mumbai', 3.2),

-- Bangalore Restaurants (City Avg = 4.35)
(5, 'Truffles', 'Bangalore', 4.7),
(6, 'Toit Brewpub', 'Bangalore', 4.6),
(7, 'CTR Shri Sagar', 'Bangalore', 4.5),
(8, 'Quick Bites', 'Bangalore', 3.6),

-- Delhi Restaurants (City Avg = 4.27)
(9, 'Bukhara', 'Delhi', 4.8),
(10, 'Karim''s', 'Delhi', 4.3),
(11, 'Paranthe Wali Gali Corner', 'Delhi', 3.7);

-- Correlated Subquery: Evaluates each restaurant against its own city's average
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
```

#### Output:
| restaurant_id | restaurant_name | city | rating | city_avg |
|---|---|---|---|---|
| 5 | Truffles | Bangalore | 4.7 | 4.35 |
| 6 | Toit Brewpub | Bangalore | 4.6 | 4.35 |
| 7 | CTR Shri Sagar | Bangalore | 4.5 | 4.35 |
| 9 | Bukhara | Delhi | 4.8 | 4.27 |
| 10 | Karim's | Delhi | 4.3 | 4.27 |
| 1 | Trishna | Mumbai | 4.6 | 4.00 |
| 2 | Britannia & Co | Mumbai | 4.4 | 4.00 |

> **Key Takeaway:** The subquery in `WHERE` is **correlated** because it binds `r2.city = r1.city`. It calculates a dynamic threshold for each city on the fly.

---

### Task 2: Subquery in SELECT Statement (Zomato User Profile Order Summary)
**Requirement:** Write a SQL query that uses a subquery in the `SELECT` statement to display each user's name from a `Users` table along with the total number of orders they have placed from an `Orders` table, like a summary you might see in a Zomato user profile.

```sql
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
```

#### Output:
| user_id | user_name | total_orders | total_spend |
|---|---|---|---|
| 1 | Atharv Chaudhari | 4 | 2200.00 |
| 2 | Sneha Patel | 2 | 2090.00 |
| 3 | Rahul Verma | 1 | 250.00 |
| **4** | **Priya Sharma** | **0** | **0.00** |

> **Key Takeaway:** Scalar subqueries inside `SELECT` return exactly one value per row. For users without orders (`Priya Sharma`), `COUNT(*)` returns `0` cleanly without losing the parent user record.

---

### Task 3: Subquery with IN Operator (BookMyShow 5-Star Rated Movies)
**Requirement:** Given a `Movies` table and a `Reviews` table, write a SQL query using `IN` with a subquery to list all movies that have at least one review with a rating of 5 stars, as seen in BookMyShow's top-rated section.

```sql
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
```

#### Output:
| movie_id | title | genre | release_year |
|---|---|---|---|
| 4 | Oppenheimer | Historical Drama | 2023 |
| 3 | Dangal | Biography / Sports | 2016 |
| 2 | Interstellar | Sci-Fi | 2014 |
| 1 | Inception | Sci-Fi | 2010 |

> **Key Takeaway:** The inner query outputs a list of movie IDs having 5-star ratings. Movies like *Race 3* (max rating 2) and *Housefull 4* (max rating 3) are filtered out.

---

### Task 4: Nested Subquery for Relational Division (Flipkart Sellers in Every Category)
**Requirement:** Write a nested SQL query to find the names of all sellers from a `Sellers` table on a Flipkart-style platform who have sold products in every category listed in a `Categories` table. (*Hint: Use nested subqueries to compare seller's categories with the complete list of categories.*)

#### Solution 4A: Nested Subquery comparing Distinct Category Counts
```sql
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
```

#### Solution 4B: Classical Double NOT EXISTS (Relational Division)
```sql
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
```

#### Output:
| seller_id | seller_name | rating |
|---|---|---|
| 1 | RetailNet India | 4.8 |
| 2 | SuperCom MultiStore | 4.7 |

> **Key Takeaway:** `RetailNet India` and `SuperCom MultiStore` sell across all 3 catalog categories (*Electronics*, *Fashion*, *Home & Kitchen*). Single-category niche sellers (*TechWorld Electronics* and *StyleStreet Apparels*) are excluded.

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-11-subqueries/solution.sql): Executable SQL queries for Tasks 1 to 4.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-11-subqueries/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_11_subqueries.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-11-subqueries/session_11_subqueries.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`subqueries.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-11-subqueries/subqueries.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-11-subqueries/README.md): Comprehensive documentation.
