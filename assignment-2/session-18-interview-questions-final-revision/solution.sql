-- ============================================================================
-- SESSION 18: Interview Questions + Final Revision
-- Database: interview_revision.db
-- Dialect: SQLite / Standard ANSI SQL
-- Description: Core SQL Interview Practice covering Aggregations & HAVING,
--              Relational JOINs, Subqueries, Window Functions, and Index Optimization.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Artists with More Than 3 Uploaded Songs (HAVING Clause)
-- Schema: songs (song_id, artist_name, title)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    song_id INTEGER PRIMARY KEY,
    artist_name TEXT NOT NULL,
    title TEXT NOT NULL
);

INSERT INTO songs (song_id, artist_name, title) VALUES
(1,  'Arijit Singh',   'Tum Hi Ho'),
(2,  'Arijit Singh',   'Kesariya'),
(3,  'Arijit Singh',   'Channa Mereya'),
(4,  'Arijit Singh',   'Raabta'),
(5,  'Arijit Singh',   'Kalank'),
(6,  'Taylor Swift',   'Cruel Summer'),
(7,  'Taylor Swift',   'Anti-Hero'),
(8,  'Taylor Swift',   'Blank Space'),
(9,  'Taylor Swift',   'Lover'),
(10, 'Ed Sheeran',     'Shape of You'),
(11, 'Ed Sheeran',     'Perfect'),
(12, 'Ed Sheeran',     'Bad Habits'),
(13, 'The Weeknd',     'Blinding Lights'),
(14, 'The Weeknd',     'Starboy'),
(15, 'Diljit Dosanjh', 'Lover');

-- Task 1 Query: Total songs per artist where count > 3
SELECT 
    artist_name,
    COUNT(song_id) AS total_songs
FROM songs
GROUP BY artist_name
HAVING COUNT(song_id) > 3
ORDER BY total_songs DESC, artist_name ASC;

-- ----------------------------------------------------------------------------
-- TASK 2: Relational JOIN for Total Order Amount per User
-- Schema: users (user_id, username), orders (order_id, user_id, amount)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username) VALUES
(1, 'rahul_sharma'),
(2, 'priya_patel'),
(3, 'amit_verma'),
(4, 'sneha_reddy'),
(5, 'vikram_m');

INSERT INTO orders (order_id, user_id, amount) VALUES
(101, 1, 450.00),
(102, 1, 750.00),
(103, 2, 1200.00),
(104, 2, 800.00),
(105, 3, 350.00),
(106, 4, 950.00),
(107, 4, 1100.00),
(108, 4, 600.00);

-- Task 2 Query: Display each username along with their total order amount
-- Using LEFT JOIN to ensure all users (even those with 0 orders) are included:
SELECT 
    u.username,
    COALESCE(SUM(o.amount), 0.00) AS total_order_amount
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username
ORDER BY total_order_amount DESC;

-- Standard INNER JOIN variant (only users with orders):
SELECT 
    u.username,
    SUM(o.amount) AS total_order_amount
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username
ORDER BY total_order_amount DESC;

-- ----------------------------------------------------------------------------
-- TASK 3: Scalar Subquery for Above-Average Rated Restaurants
-- Schema: restaurants (id, name, rating)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rating DECIMAL(3, 2) NOT NULL
);

INSERT INTO restaurants (id, name, rating) VALUES
(1, 'Gulati', 4.80),
(2, 'Punjab Grill', 4.50),
(3, 'Toscano', 4.60),
(4, 'Haldirams', 3.80),
(5, 'Subway', 3.70),
(6, 'Chai Point', 3.60);

-- Task 3 Query: Restaurants whose rating is higher than the average rating
SELECT 
    name,
    rating
FROM restaurants
WHERE rating > (
    SELECT AVG(rating) 
    FROM restaurants
)
ORDER BY rating DESC;

-- Diagnostic: Overall average rating
SELECT ROUND(AVG(rating), 2) AS overall_avg_rating FROM restaurants;

-- ----------------------------------------------------------------------------
-- TASK 4: Window Function Cumulative Running Total per User
-- Schema: transactions (id, user_id, amount, transaction_date)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL
);

INSERT INTO transactions (id, user_id, amount, transaction_date) VALUES
(1, 101, 500.00,  '2026-03-01'),
(2, 101, 300.00,  '2026-03-05'),
(3, 101, 700.00,  '2026-03-10'),
(4, 102, 1000.00, '2026-03-02'),
(5, 102, 450.00,  '2026-03-08'),
(6, 102, 550.00,  '2026-03-15');

-- Task 4 Query: Display user_id, amount, and running total ordered by transaction_date
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

-- ----------------------------------------------------------------------------
-- TASK 5: Flipkart Query Performance Optimization (Index & Query Structure)
-- Target Query:
-- SELECT product_id, title, price, category 
-- FROM products 
-- WHERE category = 'Electronics' AND price BETWEEN 1000 AND 5000;
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL
);

-- Optimization 1: Composite B-Tree Index on (category, price)
-- Rule: Equality column ('category') first, followed by Range column ('price')
CREATE INDEX idx_products_category_price ON products (category, price);

-- Optimization 2: Covering Index / SARGable predicates / Partitioning
-- Ensures query planner performs an Index Seek instead of a Full Table Scan (TABLE SCAN).
EXPLAIN QUERY PLAN
SELECT product_id, title, price, category 
FROM products 
WHERE category = 'Electronics' AND price BETWEEN 1000 AND 5000;
