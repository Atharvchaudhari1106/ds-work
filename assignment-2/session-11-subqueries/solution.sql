-- =============================================================================
-- SESSION 11: SUBQUERIES
-- Coursework / Assignment Submission
-- Database: subqueries_db
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Subquery in WHERE Clause (Restaurants above City Average)
-- Problem: Create a SQL query using a subquery in the WHERE clause to find 
-- all restaurants from a 'Restaurants' table whose average rating is higher 
-- than the average rating of all restaurants in the city.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL
);

INSERT INTO Restaurants (id, name, city, rating) VALUES
-- Mumbai Restaurants (Avg = 4.00)
(1, 'Trishna', 'Mumbai', 4.6),
(2, 'Britannia & Co', 'Mumbai', 4.4),
(3, 'Bademiya', 'Mumbai', 3.8),
(4, 'Local Fast Food', 'Mumbai', 3.2),

-- Bangalore Restaurants (Avg = 4.35)
(5, 'Truffles', 'Bangalore', 4.7),
(6, 'Toit Brewpub', 'Bangalore', 4.6),
(7, 'CTR Shri Sagar', 'Bangalore', 4.5),
(8, 'Quick Bites', 'Bangalore', 3.6),

-- Delhi Restaurants (Avg = 4.27)
(9, 'Bukhara', 'Delhi', 4.8),
(10, 'Karim''s', 'Delhi', 4.3),
(11, 'Paranthe Wali Gali Corner', 'Delhi', 3.7);

-- Query 1A: Correlated Subquery (Evaluates against the restaurant's own respective city)
-- Finds restaurants with rating higher than the average rating of restaurants in THAT city
SELECT 
    r1.id AS restaurant_id,
    r1.name AS restaurant_name,
    r1.city,
    r1.rating,
    ROUND((SELECT AVG(r2.rating) FROM Restaurants r2 WHERE r2.city = r1.city), 2) AS city_avg_rating
FROM Restaurants r1
WHERE r1.rating > (
    SELECT AVG(r2.rating)
    FROM Restaurants r2
    WHERE r2.city = r1.city
)
ORDER BY r1.city, r1.rating DESC;

-- Query 1B: Non-Correlated Subquery for a specific target city (e.g., 'Mumbai')
SELECT 
    id,
    name,
    city,
    rating
FROM Restaurants
WHERE city = 'Mumbai'
  AND rating > (
      SELECT AVG(rating) 
      FROM Restaurants 
      WHERE city = 'Mumbai'
  );


-- -----------------------------------------------------------------------------
-- TASK 2: Subquery in SELECT Statement (Zomato User Profile Order Summary)
-- Problem: Write a SQL query that uses a subquery in the SELECT statement to 
-- display each user's name from a 'Users' table along with the total number of 
-- orders they have placed from an 'Orders' table, like a summary you might see 
-- in a Zomato user profile.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users (id, name, email) VALUES
(1, 'Atharv Chaudhari', 'atharv@example.com'),
(2, 'Sneha Patel', 'sneha@example.com'),
(3, 'Rahul Verma', 'rahul@example.com'),
(4, 'Priya Sharma', 'priya@example.com');  -- User with 0 orders

INSERT INTO Orders (id, user_id, order_date, amount) VALUES
(101, 1, '2026-03-01', 450.00),
(102, 1, '2026-03-05', 780.00),
(103, 1, '2026-03-12', 320.00),
(104, 1, '2026-03-18', 650.00),
(105, 2, '2026-03-04', 1200.00),
(106, 2, '2026-03-15', 890.00),
(107, 3, '2026-03-10', 250.00);

-- Query 2: Scalar Subquery in SELECT Projection
SELECT 
    u.id AS user_id,
    u.name AS user_name,
    u.email,
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


-- -----------------------------------------------------------------------------
-- TASK 3: Subquery with IN Operator (BookMyShow 5-Star Rated Movies)
-- Problem: Given a 'Movies' table and a 'Reviews' table, write a SQL query using 
-- IN with a subquery to list all movies that have at least one review with a 
-- rating of 5 stars, as seen in BookMyShow's top-rated section.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies (
    id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    release_year INT NOT NULL
);

CREATE TABLE Reviews (
    id INT PRIMARY KEY,
    movie_id INT NOT NULL,
    reviewer_name VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text VARCHAR(255),
    FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

INSERT INTO Movies (id, title, genre, release_year) VALUES
(1, 'Inception', 'Sci-Fi', 2010),
(2, 'Interstellar', 'Sci-Fi', 2014),
(3, 'Dangal', 'Biography / Sports', 2016),
(4, 'Oppenheimer', 'Historical Drama', 2023),
(5, 'Race 3', 'Action', 2018),
(6, 'Housefull 4', 'Comedy', 2019);

INSERT INTO Reviews (id, movie_id, reviewer_name, rating, review_text) VALUES
(1, 1, 'Amit', 5, 'Mind-bending cinematic masterpiece!'),
(2, 1, 'Kunal', 4, 'Great concept and visuals.'),
(3, 2, 'Pooja', 5, 'Emotional and visually staggering.'),
(4, 3, 'Rohit', 5, 'Incredible performances and direction.'),
(5, 4, 'Sanya', 5, 'Stunning storytelling and sound design.'),
(6, 5, 'Tanmay', 2, 'Poor plot and acting.'),
(7, 5, 'Vikas', 1, 'Waste of time.'),
(8, 6, 'Ritu', 3, 'Average comedy, nothing special.');

-- Query 3: Subquery with IN to find movies with at least one 5-star review
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


-- -----------------------------------------------------------------------------
-- TASK 4: Nested Subquery for Relational Division (Flipkart Sellers in Every Category)
-- Problem: Write a nested SQL query to find the names of all sellers from a 
-- 'Sellers' table on a Flipkart-style platform who have sold products in every 
-- category listed in a 'Categories' table.
-- Hint: Use nested subqueries to compare seller's categories with the complete list of categories.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Sellers;

CREATE TABLE Sellers (
    id INT PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL
);

CREATE TABLE Categories (
    id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    id INT PRIMARY KEY,
    seller_id INT NOT NULL,
    category_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (seller_id) REFERENCES Sellers(id),
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

INSERT INTO Categories (id, category_name) VALUES
(1, 'Electronics'),
(2, 'Fashion'),
(3, 'Home & Kitchen');

INSERT INTO Sellers (id, seller_name, rating) VALUES
(1, 'RetailNet India', 4.8),      -- Has products in All 3 categories!
(2, 'SuperCom MultiStore', 4.7),  -- Has products in All 3 categories!
(3, 'TechWorld Electronics', 4.5),-- Only in Electronics
(4, 'StyleStreet Apparels', 4.2); -- Only in Fashion

INSERT INTO Products (id, seller_id, category_id, product_name, price) VALUES
-- RetailNet India (Category 1, 2, 3)
(101, 1, 1, 'Smartphone Pro', 34999.00),
(102, 1, 2, 'Denim Jacket', 2499.00),
(103, 1, 3, 'Non-stick Cookware Set', 3999.00),

-- SuperCom MultiStore (Category 1, 2, 3)
(104, 2, 1, 'Noise Cancelling Headphones', 8999.00),
(105, 2, 2, 'Casual Cotton T-Shirt', 799.00),
(106, 2, 3, 'Air Purifier', 9499.00),

-- TechWorld Electronics (Category 1 only)
(107, 3, 1, 'Mechanical Keyboard', 4500.00),
(108, 3, 1, 'Wireless Gaming Mouse', 2200.00),

-- StyleStreet Apparels (Category 2 only)
(109, 4, 2, 'Running Shoes', 3200.00);

-- Solution 4A: Nested Subquery comparing Distinct Category Counts
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

-- Solution 4B: Classical Double NOT EXISTS (Relational Division)
-- "Find sellers for which there does NOT exist a category that the seller has NOT sold"
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
