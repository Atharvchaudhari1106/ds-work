-- =============================================================================
-- SESSION 12: CTE (WITH Clause)
-- Coursework / Assignment Submission
-- Database: cte_demo_db
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Basic CTE with WITH Clause (Flipkart/Myntra Top-Rated Products)
-- Problem: Create a CTE using the WITH clause to select all products with a 
-- rating above 4.5 from a 'Products' table, similar to how Flipkart or Myntra 
-- might highlight top-rated items.
-- -----------------------------------------------------------------------------
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
SELECT 
    product_id,
    product_name,
    category,
    price,
    rating
FROM TopRatedProducts
ORDER BY rating DESC, price ASC;


-- -----------------------------------------------------------------------------
-- TASK 2: Subquery vs CTE Comparison (Ahmedabad Restaurants with Delivery < 50)
-- Problem: Rewrite a query that finds all restaurants in 'Ahmedabad' with delivery 
-- charges under 50 from a 'Restaurants' table, first using a subquery and then 
-- using a CTE. Compare both queries for readability.
-- Hint: Focus on making the CTE version cleaner and easier to understand.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine VARCHAR(50) NOT NULL,
    delivery_charge DECIMAL(5, 2) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL
);

INSERT INTO Restaurants (id, name, city, cuisine, delivery_charge, rating) VALUES
(1, 'Manek Chowk Delights', 'Ahmedabad', 'Street Food', 30.00, 4.6),
(2, 'Agashiye - House of MG', 'Ahmedabad', 'Gujarati Thali', 40.00, 4.8),
(3, 'Swati Snacks', 'Ahmedabad', 'Chaat & Snacks', 45.00, 4.5),
(4, 'Gordhan Thal', 'Ahmedabad', 'Gujarati Thali', 60.00, 4.7),  -- Excluded: delivery >= 50
(5, 'Havmor Restaurant', 'Ahmedabad', 'North Indian', 55.00, 4.3), -- Excluded: delivery >= 50
(6, 'Truffles', 'Bangalore', 'Continental', 35.00, 4.7),          -- Excluded: city != Ahmedabad
(7, 'Britannia & Co', 'Mumbai', 'Parsi', 40.00, 4.4);              -- Excluded: city != Ahmedabad

-- Version A: Using a Derived Table Subquery (Inside-out reading order)
SELECT 
    restaurant_name,
    city,
    cuisine,
    delivery_charge,
    rating
FROM (
    SELECT 
        name AS restaurant_name,
        city,
        cuisine,
        delivery_charge,
        rating
    FROM Restaurants
    WHERE city = 'Ahmedabad'
) AS AhmedabadRestaurants
WHERE delivery_charge < 50.00
ORDER BY delivery_charge ASC;

-- Version B: Using a Clean CTE (Linear, top-to-bottom reading order)
WITH AhmedabadRestaurants AS (
    SELECT 
        name AS restaurant_name,
        city,
        cuisine,
        delivery_charge,
        rating
    FROM Restaurants
    WHERE city = 'Ahmedabad'
)
SELECT 
    restaurant_name,
    city,
    cuisine,
    delivery_charge,
    rating
FROM AhmedabadRestaurants
WHERE delivery_charge < 50.00
ORDER BY delivery_charge ASC;

-- Readability Comparison:
-- 1. Reading Flow: The CTE version reads sequentially from top to bottom (Define source -> Apply filter).
--    The subquery version forces the developer to read "inside-out", parsing the inner FROM clause before understanding the outer projection.
-- 2. Debugging: The CTE can be independently tested simply by changing the final SELECT to "SELECT * FROM AhmedabadRestaurants".
-- 3. Modularity: CTEs can be easily chained or referenced multiple times without code duplication.


-- -----------------------------------------------------------------------------
-- TASK 3: Multiple CTEs in a Single Query (Instagram Top Users & Top Posts)
-- Problem: Using two CTEs in a single query, find the top 3 most-followed users 
-- and the top 3 most-liked posts from a 'Users' and 'Posts' table (think Instagram-style data). 
-- Output both lists in the same result set.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    followers_count INT NOT NULL,
    account_status VARCHAR(20) DEFAULT 'Active'
);

CREATE TABLE Posts (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    caption VARCHAR(255) NOT NULL,
    likes_count INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users (id, username, followers_count, account_status) VALUES
(1, 'virat.kohli', 270000000, 'Active'),
(2, 'priyanka.chopra', 91000000, 'Active'),
(3, 'alia.bhatt', 85000000, 'Active'),
(4, 'tech_reviewer', 500000, 'Active'),
(5, 'daily_foodie', 250000, 'Active');

INSERT INTO Posts (id, user_id, caption, likes_count) VALUES
(101, 1, 'Historic victory at MCG! Proud of the boys.', 5800000),
(102, 1, 'Match day ready. Always grateful.', 4200000),
(103, 2, 'Unforgettable night at the Met Gala 2026.', 3900000),
(104, 3, 'Behind the scenes from our new film set.', 3100000),
(105, 4, 'Unboxing the future: New foldable phone review.', 180000),
(106, 5, 'Best street food crawl in Ahmedabad!', 95000);

-- Query 3: Two CTEs merged via UNION ALL into a Unified Executive Summary Result Set
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


-- -----------------------------------------------------------------------------
-- TASK 4: Recursive CTE for Next 7 Days (BookMyShow Movie Booking Dates)
-- Problem: Write a recursive CTE that generates a list of dates for the next 
-- 7 days starting from today, similar to how BookMyShow shows available dates for movie bookings.
-- Hint: Use a base case for today and recursion to add one day at a time.
-- -----------------------------------------------------------------------------
WITH RECURSIVE BookingDates AS (
    -- Base Case: Day 1 (Today)
    SELECT 
        1 AS day_number,
        DATE('now') AS booking_date
    UNION ALL
    -- Recursive Step: Add +1 day until 7 days are generated
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


-- -----------------------------------------------------------------------------
-- TASK 5: Refactoring a Messy Query Using CTEs for Clarity & Maintainability
-- Problem: Given a messy SQL query that finds all users with more than 1000 
-- followers from a 'Users' table, refactor it to use a CTE for better clarity and maintainability.
-- -----------------------------------------------------------------------------

-- 1. The Messy Original Query:
-- Characterized by nested subqueries, duplicate conditions, redundant aliases, and poor formatting:
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

-- 2. Clean, Refactored Query Using a Descriptive CTE:
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

-- Why the Refactored CTE is Superior:
-- 1. Eliminates 3 redundant subquery wrappers and duplicate table scans.
-- 2. Provides self-documenting naming ('ActiveInfluencerUsers') that reflects business intent.
-- 3. Consolidates filter conditions ('account_status' and 'followers_count') in one single location.
-- 4. Greatly assists the query optimizer by simplifying the abstract syntax tree (AST).
