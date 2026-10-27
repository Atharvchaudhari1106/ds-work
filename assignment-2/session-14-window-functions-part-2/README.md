# Session 14: Window Functions - Part 2

## Overview & Objectives
This session covers value window functions and rolling window frames:
1. **Value Window Functions**:
   - **`LAG()`**: Accessing prior row data within a partition (e.g., previous order value, month-over-month growth).
   - **`LEAD()`**: Looking forward to subsequent rows within a partition (e.g., next purchase amount, customer churn signals).
2. **Window Framing Specifications (`ROWS BETWEEN`)**:
   - **Running Totals**: Accumulating sums dynamically across time using `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.
   - **Moving Averages**: Computing rolling n-period moving averages using sliding frames like `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.

---

## Task Solutions & Code Explanations

### Task 1: Create 'Orders' Table & Insert Sample Data
**Requirement:** Create a table called `Orders` with columns: `order_id`, `user_id`, `order_date`, and `total_amount`. Insert at least 7 sample rows representing different users and dates, similar to how food orders appear in Zomato or Swiggy.

```sql
DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL
);

INSERT INTO Orders (order_id, user_id, order_date, total_amount) VALUES
-- User 101 Orders (Atharv)
(1, 101, '2026-03-01', 350.00),
(2, 101, '2026-03-05', 450.00),
(3, 101, '2026-03-12', 600.00),
(4, 101, '2026-03-20', 800.00),

-- User 102 Orders (Sneha)
(5, 102, '2026-03-02', 200.00),
(6, 102, '2026-03-08', 300.00),
(7, 102, '2026-03-15', 250.00),
(8, 102, '2026-03-22', 400.00),

-- User 103 Orders (Rahul)
(9, 103, '2026-03-10', 500.00),
(10, 103, '2026-03-18', 750.00);
```

#### Base Data View:
| order_id | user_id | order_date | total_amount |
|---|---|---|---|
| 1 | 101 | 2026-03-01 | 350.00 |
| 2 | 101 | 2026-03-05 | 450.00 |
| 3 | 101 | 2026-03-12 | 600.00 |
| 4 | 101 | 2026-03-20 | 800.00 |
| 5 | 102 | 2026-03-02 | 200.00 |
| 6 | 102 | 2026-03-08 | 300.00 |
| 7 | 102 | 2026-03-15 | 250.00 |
| 8 | 102 | 2026-03-22 | 400.00 |
| 9 | 103 | 2026-03-10 | 500.00 |
| 10 | 103 | 2026-03-18 | 750.00 |

---

### Task 2: Previous Order Amount Using LAG()
**Requirement:** Write a SQL query using the `LAG()` function to show each user's `order_id`, `order_date`, and the `total_amount` of their previous order (if any), ordered by user and date. (*Hint: Use PARTITION BY user_id and ORDER BY order_date.*)

```sql
SELECT 
    user_id,
    order_id,
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (
        PARTITION BY user_id 
        ORDER BY order_date ASC
    ) AS previous_order_amount,
    ROUND(
        total_amount - LAG(total_amount, 1) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC
        ), 2
    ) AS spend_difference
FROM Orders
ORDER BY user_id ASC, order_date ASC;
```

#### Output:
| user_id | order_id | order_date | total_amount | previous_order_amount | spend_difference |
|---|---|---|---|---|---|
| 101 | 1 | 2026-03-01 | 350.00 | *NULL* | *NULL* |
| 101 | 2 | 2026-03-05 | 450.00 | 350.00 | +100.00 |
| 101 | 3 | 2026-03-12 | 600.00 | 450.00 | +150.00 |
| 101 | 4 | 2026-03-20 | 800.00 | 600.00 | +200.00 |
| 102 | 5 | 2026-03-02 | 200.00 | *NULL* | *NULL* |
| 102 | 6 | 2026-03-08 | 300.00 | 200.00 | +100.00 |
| 102 | 7 | 2026-03-15 | 250.00 | 300.00 | -50.00 |
| 102 | 8 | 2026-03-22 | 400.00 | 250.00 | +150.00 |
| 103 | 9 | 2026-03-10 | 500.00 | *NULL* | *NULL* |
| 103 | 10 | 2026-03-18 | 750.00 | 500.00 | +250.00 |

> **Key Takeaway:** The first order of each user partition evaluates to `NULL` for `previous_order_amount`. The difference tracks order-over-order basket growth.

---

### Task 3: Next Order Amount Using LEAD()
**Requirement:** Using the same Orders table, write a SQL query with the `LEAD()` function to display each `order_id`, `order_date`, and the next order's `total_amount` for the same user.

```sql
SELECT 
    user_id,
    order_id,
    order_date,
    total_amount,
    LEAD(total_amount, 1) OVER (
        PARTITION BY user_id 
        ORDER BY order_date ASC
    ) AS next_order_amount
FROM Orders
ORDER BY user_id ASC, order_date ASC;
```

#### Output:
| user_id | order_id | order_date | total_amount | next_order_amount |
|---|---|---|---|---|
| 101 | 1 | 2026-03-01 | 350.00 | 450.00 |
| 101 | 2 | 2026-03-05 | 450.00 | 600.00 |
| 101 | 3 | 2026-03-12 | 600.00 | 800.00 |
| 101 | 4 | 2026-03-20 | 800.00 | *NULL* |
| 102 | 5 | 2026-03-02 | 200.00 | 300.00 |
| 102 | 6 | 2026-03-08 | 300.00 | 250.00 |
| 102 | 7 | 2026-03-15 | 250.00 | 400.00 |
| 102 | 8 | 2026-03-22 | 400.00 | *NULL* |
| 103 | 9 | 2026-03-10 | 500.00 | 750.00 |
| 103 | 10 | 2026-03-18 | 750.00 | *NULL* |

> **Key Takeaway:** The final transaction for each user returns `NULL` for `next_order_amount`, indicating no subsequent order exists.

---

### Task 4: Cumulative Running Total per User
**Requirement:** Write a SQL query to calculate the running total of `total_amount` for each user, showing `order_id`, `order_date`, `total_amount`, and a column `running_total` that accumulates the sum as you move through each user's orders. (*Hint: Use SUM(total_amount) OVER (PARTITION BY user_id ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW).*)

```sql
SELECT 
    user_id,
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY user_id 
        ORDER BY order_date ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM Orders
ORDER BY user_id ASC, order_date ASC;
```

#### Output:
| user_id | order_id | order_date | total_amount | running_total |
|---|---|---|---|---|
| 101 | 1 | 2026-03-01 | 350.00 | 350.00 |
| 101 | 2 | 2026-03-05 | 450.00 | 800.00 |
| 101 | 3 | 2026-03-12 | 600.00 | 1400.00 |
| 101 | 4 | 2026-03-20 | 800.00 | 2200.00 |
| 102 | 5 | 2026-03-02 | 200.00 | 200.00 |
| 102 | 6 | 2026-03-08 | 300.00 | 500.00 |
| 102 | 7 | 2026-03-15 | 250.00 | 750.00 |
| 102 | 8 | 2026-03-22 | 400.00 | 1150.00 |
| 103 | 9 | 2026-03-10 | 500.00 | 500.00 |
| 103 | 10 | 2026-03-18 | 750.00 | 1250.00 |

---

### Task 5: 3-Order Moving Average Using Window Frame
**Requirement:** Write a SQL query to calculate a 3-order moving average of `total_amount` for each user, showing `order_id`, `order_date`, `total_amount`, and `moving_avg` columns. (*Constraint: Use SUM() OVER() with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW to compute the moving average.*)

```sql
SELECT 
    user_id,
    order_id,
    order_date,
    total_amount,
    ROUND(
        SUM(total_amount) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) * 1.0 / 
        COUNT(total_amount) OVER (
            PARTITION BY user_id 
            ORDER BY order_date ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS moving_avg
FROM Orders
ORDER BY user_id ASC, order_date ASC;
```

#### Output:
| user_id | order_id | order_date | total_amount | moving_avg | Window Calculation |
|---|---|---|---|---|---|
| 101 | 1 | 2026-03-01 | 350.00 | 350.00 | (350) / 1 |
| 101 | 2 | 2026-03-05 | 450.00 | 400.00 | (350 + 450) / 2 |
| 101 | 3 | 2026-03-12 | 600.00 | 466.67 | (350 + 450 + 600) / 3 |
| 101 | 4 | 2026-03-20 | 800.00 | 616.67 | (450 + 600 + 800) / 3 |
| 102 | 5 | 2026-03-02 | 200.00 | 200.00 | (200) / 1 |
| 102 | 6 | 2026-03-08 | 300.00 | 250.00 | (200 + 300) / 2 |
| 102 | 7 | 2026-03-15 | 250.00 | 250.00 | (200 + 300 + 250) / 3 |
| 102 | 8 | 2026-03-22 | 400.00 | 316.67 | (300 + 250 + 400) / 3 |
| 103 | 9 | 2026-03-10 | 500.00 | 500.00 | (500) / 1 |
| 103 | 10 | 2026-03-18 | 750.00 | 625.00 | (500 + 750) / 2 |

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-14-window-functions-part-2/solution.sql): Executable SQL queries for Tasks 1 to 5.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-14-window-functions-part-2/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_14_window_functions_part_2.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-14-window-functions-part-2/session_14_window_functions_part_2.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`orders_window.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-14-window-functions-part-2/orders_window.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-14-window-functions-part-2/README.md): Comprehensive documentation.
