-- ============================================================================
-- SESSION 17: SQL Project - HR Analysis (Restaurant & Reviews Analytics)
-- Database: restaurant_analytics.db
-- Dialect: SQLite / Standard ANSI SQL
-- Description: End-to-end database design, relational joins, cuisine aggregations,
--              and partition ranking using window functions.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Create 'Restaurant' Table & Insert Sample Rows
-- Schema: id, name, cuisine, location, average_rating
-- ----------------------------------------------------------------------------
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

-- Diagnostic check for Restaurant table
SELECT * FROM Restaurant ORDER BY id ASC;

-- ----------------------------------------------------------------------------
-- TASK 2: Number of Restaurants per Cuisine Type
-- Ordered by restaurant count descending
-- ----------------------------------------------------------------------------
SELECT 
    cuisine,
    COUNT(id) AS restaurant_count
FROM Restaurant
GROUP BY cuisine
ORDER BY restaurant_count DESC, cuisine ASC;

-- ----------------------------------------------------------------------------
-- TASK 3: Create 'Review' Table & Insert 14 Sample Reviews
-- Schema: id, restaurant_id, user_name, rating, review_date
-- ----------------------------------------------------------------------------
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

-- Diagnostic check for Review table
SELECT * FROM Review ORDER BY id ASC;

-- ----------------------------------------------------------------------------
-- TASK 4: Average Review Rating per Restaurant using JOIN & GROUP BY
-- Ordered by highest average rating first
-- ----------------------------------------------------------------------------
SELECT 
    r.name,
    r.cuisine,
    ROUND(AVG(rev.rating), 2) AS avg_review_rating
FROM Restaurant r
INNER JOIN Review rev ON r.id = rev.restaurant_id
GROUP BY r.id, r.name, r.cuisine
ORDER BY avg_review_rating DESC, r.name ASC;

-- ----------------------------------------------------------------------------
-- TASK 5: Rank Restaurants by Average Review Rating within Each Cuisine
-- Uses DENSE_RANK() window function partitioned by cuisine
-- ----------------------------------------------------------------------------
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
