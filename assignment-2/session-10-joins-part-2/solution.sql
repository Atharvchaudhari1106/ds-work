-- =============================================================================
-- SESSION 10: JOINS - Part 2
-- Coursework / Assignment Submission
-- Database: joins_part2_db
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: FULL JOIN on Influencers & Collaborations
-- Problem: Create two tables: Influencers (id, name) and Collaborations 
-- (id, influencer1_id, influencer2_id, collab_date). Write a SQL FULL JOIN query 
-- to list all influencers and show their collaboration partner names if any, 
-- including influencers with no collaborations.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Collaborations;
DROP TABLE IF EXISTS Influencers;

CREATE TABLE Influencers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Collaborations (
    id INT PRIMARY KEY,
    influencer1_id INT,
    influencer2_id INT,
    collab_date DATE NOT NULL
);

-- Insert Sample Influencers
INSERT INTO Influencers (id, name) VALUES
(1, 'Virat Kohli'),
(2, 'Anushka Sharma'),
(3, 'CarryMinati'),
(4, 'Bhuvan Bam'),
(5, 'Technical Guruji'),  -- Solo creator (No collaborations)
(6, 'Prajakta Koli');      -- Solo creator (No collaborations)

-- Insert Sample Collaborations
INSERT INTO Collaborations (id, influencer1_id, influencer2_id, collab_date) VALUES
(101, 1, 2, '2026-01-15'),  -- Virat & Anushka
(102, 3, 4, '2026-02-10'),  -- CarryMinati & Bhuvan Bam
(103, 1, 3, '2026-03-01'),  -- Virat & CarryMinati
(104, 99, 100, '2026-04-05'); -- Unlinked external collab (to demonstrate both sides of FULL JOIN)

-- FULL JOIN Query (Standard SQL & SQLite 3.39+)
-- Lists all influencers and shows their collaboration partners, including solo creators
SELECT 
    i1.id AS influencer_id,
    i1.name AS influencer_name,
    c.id AS collab_id,
    c.collab_date,
    c.influencer2_id AS partner_id,
    i2.name AS partner_name
FROM Influencers i1
FULL JOIN Collaborations c ON i1.id = c.influencer1_id
LEFT JOIN Influencers i2 ON c.influencer2_id = i2.id;

-- Equivalent syntax for engines without native FULL JOIN (e.g. MySQL via UNION):
-- SELECT i1.id AS influencer_id, i1.name AS influencer_name, c.collab_date, i2.name AS partner_name
-- FROM Influencers i1
-- LEFT JOIN Collaborations c ON i1.id = c.influencer1_id
-- LEFT JOIN Influencers i2 ON c.influencer2_id = i2.id
-- UNION
-- SELECT i1.id AS influencer_id, i1.name AS influencer_name, c.collab_date, i2.name AS partner_name
-- FROM Collaborations c
-- LEFT JOIN Influencers i1 ON c.influencer1_id = i1.id
-- LEFT JOIN Influencers i2 ON c.influencer2_id = i2.id;


-- -----------------------------------------------------------------------------
-- TASK 2: SELF JOIN on Playlists (Spotify Nested Playlists)
-- Problem: Using a SELF JOIN, write a query on a table called Playlists 
-- (id, user_id, playlist_name, parent_playlist_id) to display each playlist 
-- alongside its parent playlist name, similar to how Spotify shows nested playlists.
-- Hint: Join Playlists with itself on parent_playlist_id = id.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Playlists;

CREATE TABLE Playlists (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(100) NOT NULL,
    parent_playlist_id INT
);

INSERT INTO Playlists (id, user_id, playlist_name, parent_playlist_id) VALUES
(1, 101, 'Top Hits 2026', NULL),              -- Root playlist (no parent)
(2, 101, 'Workout Motivation', NULL),          -- Root folder / parent playlist
(3, 101, 'High Intensity Cardio', 2),          -- Nested child of 'Workout Motivation'
(4, 101, 'Heavy Weightlifting', 2),            -- Nested child of 'Workout Motivation'
(5, 102, 'Chill & Acoustic', NULL),            -- Root folder / parent playlist
(6, 102, 'Sunday Morning Coffee', 5),          -- Nested child of 'Chill & Acoustic'
(7, 102, 'Rainy Day Acoustic', 5);             -- Nested child of 'Chill & Acoustic'

-- SELF JOIN Query (Using LEFT JOIN so Root playlists are also displayed)
SELECT 
    child.id AS playlist_id,
    child.user_id,
    child.playlist_name,
    child.parent_playlist_id,
    COALESCE(parent.playlist_name, 'None (Root Playlist)') AS parent_playlist_name
FROM Playlists child
LEFT JOIN Playlists parent ON child.parent_playlist_id = parent.id;

-- Alternative SELF JOIN using INNER JOIN (Displays ONLY nested child playlists that have a parent):
SELECT 
    child.id AS child_playlist_id,
    child.playlist_name AS nested_playlist_name,
    parent.id AS parent_playlist_id,
    parent.playlist_name AS folder_playlist_name
FROM Playlists child
INNER JOIN Playlists parent ON child.parent_playlist_id = parent.id;


-- -----------------------------------------------------------------------------
-- TASK 3: Multiple JOINs across 3 Tables (Users, Orders, Payments)
-- Problem: Given three tables: Users (id, username), Orders (id, user_id, order_date), 
-- and Payments (id, order_id, amount), write a SQL query using multiple JOINs 
-- to display each username, their order date, and payment amount, 
-- showing all users even if they have no orders or payments.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Payments (
    id INT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

-- Insert Users
INSERT INTO Users (id, username) VALUES
(1, 'atharv_c'),
(2, 'sneha_p'),
(3, 'rahul_v'),
(4, 'priya_m');  -- User with NO orders or payments

-- Insert Orders
INSERT INTO Orders (id, user_id, order_date) VALUES
(101, 1, '2026-03-01'),  -- atharv_c
(102, 2, '2026-03-05'),  -- sneha_p (Order 1)
(103, 2, '2026-03-10'),  -- sneha_p (Order 2)
(104, 3, '2026-03-12');  -- rahul_v (Placed order, but pending payment)

-- Insert Payments
INSERT INTO Payments (id, order_id, amount) VALUES
(1001, 101, 750.00),   -- Payment for order 101
(1002, 102, 1200.00),  -- Payment for order 102
(1003, 103, 350.00);   -- Payment for order 103
-- Note: Order 104 has NO payment record (simulates unpaid / cash-on-delivery pending)

-- Multiple LEFT JOINs Query (Chained from Users -> Orders -> Payments)
SELECT 
    u.id AS user_id,
    u.username,
    o.id AS order_id,
    o.order_date,
    p.id AS payment_id,
    p.amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
LEFT JOIN Payments p ON o.id = p.order_id;


-- -----------------------------------------------------------------------------
-- TASK 4: Eliminating Duplicates in One-to-Many Relationships (Restaurants & Reviews)
-- Problem: You notice that your JOIN query between Zomato's Restaurants and 
-- Reviews tables is returning duplicate rows for some restaurants. Modify your 
-- query to eliminate duplicates and explain in one line why the duplicates were happening.
-- Hint: Use DISTINCT or GROUP BY and consider the relationship between restaurants and reviews.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE Reviews (
    id INT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    review_text VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id)
);

INSERT INTO Restaurants (id, name, city) VALUES
(1, 'Truffles', 'Bangalore'),
(2, 'Peter Cat', 'Kolkata'),
(3, 'Haldiram', 'Nagpur'),
(4, 'Barbeque Nation', 'Mumbai');

-- Multiple reviews per restaurant (One-to-Many / 1:N relationship)
INSERT INTO Reviews (id, restaurant_id, user_name, rating, review_text) VALUES
(1, 1, 'Amit', 4.5, 'Amazing burgers!'),
(2, 1, 'Rohit', 4.8, 'Best peri peri fries.'),
(3, 1, 'Pooja', 4.2, 'Great ambience.'),
(4, 2, 'Sagnik', 4.9, 'Chelo Kebab is legendary.'),
(5, 2, 'Debolina', 4.7, 'Classic Kolkata nostalgia.'),
(6, 3, 'Tanmay', 4.0, 'Nice chole bhature.');
-- Note: Restaurant 4 has no reviews yet

-- Demonstrating the Duplicate Issue:
-- Joining Restaurants with Reviews directly duplicates restaurant metadata for each review:
-- SELECT r.id, r.name, r.city FROM Restaurants r JOIN Reviews rev ON r.id = rev.restaurant_id;

-- Solution 1: Using DISTINCT (Returns unique restaurants that have reviews)
SELECT DISTINCT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city
FROM Restaurants r
INNER JOIN Reviews rev ON r.id = rev.restaurant_id;

-- Solution 2: Using GROUP BY (Industry Best Practice - aggregates reviews into analytics metrics)
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    COUNT(rev.id) AS total_reviews,
    ROUND(AVG(rev.rating), 2) AS avg_rating
FROM Restaurants r
LEFT JOIN Reviews rev ON r.id = rev.restaurant_id
GROUP BY r.id, r.name, r.city;

-- One-Line Explanation of Why Duplicates Occur:
-- "Duplicates occur because the relationship between Restaurants and Reviews is One-to-Many (1:N), causing the parent restaurant row to duplicate for every matching review row."


-- -----------------------------------------------------------------------------
-- TASK 5: Comparing Two JOIN Conditions on Products & Categories (Flipkart Model)
-- Problem: Write two different JOIN queries on a Products and Categories table 
-- (like Flipkart) to list all products with their category names, but use different 
-- join conditions in each. Briefly explain which join condition is more efficient and why.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;

CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_code VARCHAR(20) UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,               -- Integer Surrogate Foreign Key
    category_code VARCHAR(20),     -- String Natural Foreign Key
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

INSERT INTO Categories (category_id, category_code, category_name) VALUES
(1, 'ELEC', 'Electronics'),
(2, 'FASH', 'Fashion & Apparel'),
(3, 'HOME', 'Home & Kitchen');

INSERT INTO Products (product_id, product_name, price, category_id, category_code) VALUES
(101, 'MacBook Air M3', 114900.00, 1, 'ELEC'),
(102, 'Sony WH-1000XM5', 28990.00, 1, 'ELEC'),
(103, 'Levi''s 511 Slim Jeans', 2999.00, 2, 'FASH'),
(104, 'Cotton Casual Shirt', 1499.00, 2, 'FASH'),
(105, 'Philips Air Fryer', 8499.00, 3, 'HOME');

-- Query 1: Join condition using Integer Primary Key / Foreign Key (Surrogate Key)
SELECT 
    p.product_id,
    p.product_name,
    p.price,
    c.category_name
FROM Products p
INNER JOIN Categories c ON p.category_id = c.category_id;

-- Query 2: Join condition using String / Natural Business Key (category_code)
SELECT 
    p.product_id,
    p.product_name,
    p.price,
    c.category_name
FROM Products p
INNER JOIN Categories c ON p.category_code = c.category_code;

-- Alternative Query 2 Variation: Using USING() clause (Syntactic sugar for matching column names)
-- SELECT p.product_id, p.product_name, p.price, c.category_name
-- FROM Products p
-- INNER JOIN Categories c USING (category_id);

-- Efficiency Explanation:
-- Query 1 (Integer Surrogate Key Join: p.category_id = c.category_id) is significantly more efficient than Query 2 because:
-- 1. Integer comparisons are fixed 4/8 byte primitive CPU register operations, whereas string comparisons require variable-length byte-by-byte collation scans.
-- 2. Numeric B-Tree indexes have a much higher branching factor, storing vastly more keys per memory page and minimizing disk I/O reads.
-- 3. Database optimizers can compute hash join partitions much faster with uniform bitwise operations on integers with virtually zero hash collisions.
