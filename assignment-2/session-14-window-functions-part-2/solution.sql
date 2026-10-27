-- =============================================================================
-- SESSION 14: Window Functions - Part 2
-- Coursework / Assignment Submission
-- Database: orders_window_db
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'Orders' Table & Insert Sample Records
-- Columns: order_id, user_id, order_date, total_amount
-- Represents realistic food delivery orders on Zomato / Swiggy across users.
-- -----------------------------------------------------------------------------
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

-- Verify raw table data:
SELECT * FROM Orders;


-- -----------------------------------------------------------------------------
-- TASK 2: Previous Order Amount Using LAG()
-- Problem: Write a SQL query using the LAG() function to show each user's 
-- order_id, order_date, and the total_amount of their previous order (if any), 
-- ordered by user and date.
-- Hint: Use PARTITION BY user_id and ORDER BY order_date in your window function.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- TASK 3: Next Order Amount Using LEAD()
-- Problem: Using the same Orders table, write a SQL query with the LEAD() function 
-- to display each order_id, order_date, and the next order's total_amount for the same user.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- TASK 4: Cumulative Running Total per User
-- Problem: Write a SQL query to calculate the running total of total_amount 
-- for each user, showing order_id, order_date, total_amount, and a column 
-- running_total that accumulates the sum as you move through each user's orders.
-- Hint: Use SUM(total_amount) OVER (PARTITION BY user_id ORDER BY order_date 
-- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW).
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- TASK 5: 3-Order Moving Average Using Window Frame
-- Problem: Write a SQL query to calculate a 3-order moving average of total_amount 
-- for each user, showing order_id, order_date, total_amount, and moving_avg columns.
-- Constraint: Use SUM() OVER() with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW 
-- to compute the moving average.
-- -----------------------------------------------------------------------------

-- Implementation meeting exact constraint (SUM() OVER() divided by available window count):
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

-- Alternative direct AVG() formulation:
-- SELECT user_id, order_id, order_date, total_amount,
--        ROUND(AVG(total_amount) OVER (
--            PARTITION BY user_id ORDER BY order_date 
--            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
--        ), 2) AS moving_avg
-- FROM Orders
-- ORDER BY user_id, order_date;
