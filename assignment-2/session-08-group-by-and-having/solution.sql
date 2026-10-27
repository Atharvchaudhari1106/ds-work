-- =============================================================================
-- SESSION 8: GROUP BY + HAVING
-- Coursework / Assignment Submission
-- Database: orders_db (or foodie_app)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'Orders' Table & Insert at least 8 Sample Records
-- Columns: order_id, user_id, payment_method, amount
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);

INSERT INTO Orders (order_id, user_id, payment_method, amount) VALUES
(1, 101, 'Card', 550.00),
(2, 102, 'Card', 450.00),
(3, 101, 'UPI', 320.00),
(4, 103, 'UPI', 280.00),
(5, 104, 'UPI', 420.00),
(6, 102, 'COD', 180.00),
(7, 103, 'COD', 220.00),
(8, 104, 'Wallet', 150.00),
(9, 101, 'Wallet', 250.00);

-- Verify full table content:
SELECT * FROM Orders;

-- -----------------------------------------------------------------------------
-- TASK 2: Count Orders per payment_method (Zomato Analytics Breakdown)
-- -----------------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(order_id) AS order_count
FROM Orders
GROUP BY payment_method;

-- -----------------------------------------------------------------------------
-- TASK 3: Total Amount Spent by Each user_id
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    SUM(amount) AS total_spend
FROM Orders
GROUP BY user_id
ORDER BY total_spend DESC;

-- -----------------------------------------------------------------------------
-- TASK 4: Payment Methods with Average Order Amount > 300 (GROUP BY + HAVING)
-- -----------------------------------------------------------------------------
SELECT 
    payment_method,
    ROUND(AVG(amount), 2) AS avg_order_amount
FROM Orders
GROUP BY payment_method
HAVING AVG(amount) > 300;

-- -----------------------------------------------------------------------------
-- TASK 5: WHERE vs HAVING Explanation & Example Queries
-- -----------------------------------------------------------------------------
-- 1. WHERE Clause Example: Filters individual raw rows BEFORE grouping
-- (Only consider individual orders greater than 250)
SELECT 
    payment_method,
    COUNT(*) AS high_value_orders_count
FROM Orders
WHERE amount > 250
GROUP BY payment_method;

-- 2. HAVING Clause Example: Filters aggregated groups AFTER grouping
-- (Only show payment methods where the combined total revenue exceeds 600)
SELECT 
    payment_method,
    SUM(amount) AS total_revenue
FROM Orders
GROUP BY payment_method
HAVING SUM(amount) > 600;

-- 3. Combined WHERE + HAVING in a Single Pipeline:
SELECT 
    payment_method,
    COUNT(*) AS qualifying_orders,
    SUM(amount) AS total_revenue
FROM Orders
WHERE amount >= 200          -- Row-level filter (pre-aggregation)
GROUP BY payment_method
HAVING SUM(amount) > 500;    -- Group-level filter (post-aggregation)
