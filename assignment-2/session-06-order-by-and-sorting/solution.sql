-- =============================================================================
-- SESSION 6: ORDER BY + Sorting
-- Coursework / Assignment Submission
-- Database: sorting_app
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Products Sorted by Price (Lowest to Highest - Flipkart Style)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO products (id, product_name, category, price) VALUES
(1, 'Boat Rockerz 450 Headphone', 'Electronics', 1499.00),
(2, 'Apple iPhone 15', 'Mobiles', 71999.00),
(3, 'Cotton Casual Shirt', 'Fashion', 799.00),
(4, 'Samsung Galaxy S24', 'Mobiles', 79999.00),
(5, 'Sony WH-1000XM5 Headset', 'Electronics', 28990.00),
(6, 'Fastrack Analog Watch', 'Fashion', 1250.00),
(7, 'MacBook Air M2', 'Laptops', 94990.00),
(8, 'Logitech Wireless Mouse', 'Accessories', 599.00);

-- Query: Sort by price ascending (lowest to highest)
SELECT * 
FROM products
ORDER BY price ASC;

-- -----------------------------------------------------------------------------
-- TASK 2: Top 5 Most Expensive Products (ORDER BY DESC + LIMIT)
-- -----------------------------------------------------------------------------
SELECT * 
FROM products
ORDER BY price DESC
LIMIT 5;

-- -----------------------------------------------------------------------------
-- TASK 3: Movies Multi-Column Sort (release_year DESC, rating DESC)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    rating DECIMAL(3, 1) NOT NULL
);

INSERT INTO movies (id, title, release_year, rating) VALUES
(1, 'Oppenheimer', 2023, 8.9),
(2, 'Barbie', 2023, 7.3),
(3, 'Dune: Part Two', 2024, 8.6),
(4, 'Furiosa', 2024, 7.6),
(5, 'Interstellar', 2014, 8.7),
(6, 'Inception', 2010, 8.8),
(7, 'Spider-Man: Across the Spider-Verse', 2023, 8.7);

-- Query: Latest movies first; for same year, highest rating first
SELECT title, release_year, rating
FROM movies
ORDER BY release_year DESC, rating DESC;

-- -----------------------------------------------------------------------------
-- TASK 4: First 10 Restaurants Alphabetically (Zomato A-Z Listing)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    city VARCHAR(100) NOT NULL
);

INSERT INTO restaurants (id, name, cuisine, rating, city) VALUES
(1, 'Swagat Restaurant', 'South Indian', 4.3, 'Ahmedabad'),
(2, 'Barbeque Nation', 'Buffet / BBQ', 4.4, 'Ahmedabad'),
(3, 'Cafe De Bistro', 'Continental', 3.9, 'Surat'),
(4, 'Domino''s Pizza', 'Italian / Fast Food', 4.1, 'Ahmedabad'),
(5, 'Haldiram''s', 'North Indian / Sweets', 4.2, 'Vadodara'),
(6, 'Little Italy', 'Italian', 4.6, 'Ahmedabad'),
(7, 'Mainland China', 'Chinese', 4.0, 'Ahmedabad'),
(8, 'Punjab Grill', 'North Indian', 4.5, 'Surat'),
(9, 'Sankalp', 'South Indian', 4.2, 'Surat'),
(10, 'The Chocolate Room', 'Desserts', 4.3, 'Ahmedabad'),
(11, 'Zaffran', 'Mughlai', 4.1, 'Vadodara'),
(12, 'Agashiye', 'Gujarati Heritage', 4.8, 'Ahmedabad');

-- Query: First 10 restaurants sorted alphabetically (A-Z)
SELECT * 
FROM restaurants
ORDER BY name ASC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- TASK 5: Top 3 Trending Songs with Tie-Breaker (play_count DESC, added_at DESC)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    play_count INT NOT NULL,
    added_at TIMESTAMP NOT NULL
);

INSERT INTO songs (id, title, artist, play_count, added_at) VALUES
(1, 'Starboy', 'The Weeknd', 1500000, '2026-10-15 10:00:00'),
(2, 'Brown Munde', 'AP Dhillon', 2100000, '2026-10-18 12:00:00'),
(3, 'Blinding Lights', 'The Weeknd', 2100000, '2026-10-22 14:30:00'), -- Tied with Brown Munde, but added later
(4, 'Levitating', 'Dua Lipa', 1800000, '2026-10-20 09:15:00'),
(5, 'Tum Hi Ho', 'Arijit Singh', 1950000, '2026-10-19 16:45:00');

-- Query: Top 3 trending songs; tie-breaker: more recently added first
SELECT * 
FROM songs
ORDER BY play_count DESC, added_at DESC
LIMIT 3;
