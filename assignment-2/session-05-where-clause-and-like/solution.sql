-- =============================================================================
-- SESSION 5: WHERE Clause + LIKE
-- Coursework / Assignment Submission
-- Database: restaurants_app (or foodie_app)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'Restaurants' Table & Insert at least 5 Zomato Records
-- Columns: id, name, cuisine, rating, city
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    city VARCHAR(100) NOT NULL
);

INSERT INTO Restaurants (id, name, cuisine, rating, city) VALUES
(1, 'Swagat Restaurant', 'South Indian', 4.3, 'Ahmedabad'),
(2, 'Swadisht Dining', 'North Indian', 4.1, 'Surat'),
(3, 'Little Italy', 'Italian', 4.6, 'Ahmedabad'),
(4, 'Mainland China', 'Chinese', 3.8, 'Vadodara'),
(5, 'Sankalp', 'South Indian', 4.2, 'Surat'),
(6, 'Cafe De Bistro', 'Continental', 3.2, 'Ahmedabad');

-- Verify full table content:
SELECT * FROM Restaurants;

-- -----------------------------------------------------------------------------
-- TASK 2: Find Restaurants with rating > 4.0 in 'Ahmedabad' or 'Surat'
-- -----------------------------------------------------------------------------
SELECT * 
FROM Restaurants
WHERE rating > 4.0 
  AND (city = 'Ahmedabad' OR city = 'Surat');

-- Alternative syntax using IN operator:
-- SELECT * FROM Restaurants WHERE rating > 4.0 AND city IN ('Ahmedabad', 'Surat');

-- -----------------------------------------------------------------------------
-- TASK 3: Using LIKE Operator, select restaurants starting with 'Swa'
-- -----------------------------------------------------------------------------
SELECT * 
FROM Restaurants
WHERE name LIKE 'Swa%';

-- -----------------------------------------------------------------------------
-- TASK 4: Using BETWEEN Keyword, find ratings between 3.5 and 4.5 (inclusive)
-- -----------------------------------------------------------------------------
SELECT * 
FROM Restaurants
WHERE rating BETWEEN 3.5 AND 4.5;

-- -----------------------------------------------------------------------------
-- TASK 5: Find Restaurants whose cuisine is 'Chinese', 'Italian', or 'South Indian'
-- Using the IN operator
-- -----------------------------------------------------------------------------
SELECT * 
FROM Restaurants
WHERE cuisine IN ('Chinese', 'Italian', 'South Indian');
