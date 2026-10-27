-- ============================================================================
-- SESSION 15: SQL + Python Integration
-- Database: foodie.db
-- Dialect: SQLite / Standard ANSI SQL
-- Description: Table schema, sample data, and queries for Python sqlite3 integration
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Create 'Restaurants' Table in foodie.db
-- Schema: id (PK), name, cuisine, rating
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Restaurants;

CREATE TABLE Restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cuisine TEXT NOT NULL,
    rating REAL NOT NULL CHECK (rating >= 0.0 AND rating <= 5.0)
);

-- ----------------------------------------------------------------------------
-- TASK 2: Insert Sample Restaurants & Fetch Rating > 4.0
-- ----------------------------------------------------------------------------
INSERT INTO Restaurants (id, name, cuisine, rating) VALUES
(1, 'Little Italy', 'Italian', 4.8),
(2, 'Punjab Grill', 'North Indian', 4.6),
(3, 'Chai Point', 'Cafe', 3.9);

-- Query: Fetch all restaurants with rating > 4.0
SELECT name
FROM Restaurants
WHERE rating > 4.0
ORDER BY rating DESC;

-- Detailed check with all attributes
SELECT 
    id,
    name,
    cuisine,
    rating
FROM Restaurants
WHERE rating > 4.0
ORDER BY rating DESC;

-- ----------------------------------------------------------------------------
-- TASK 3: Fetch All Restaurants for Pandas DataFrame Loading
-- ----------------------------------------------------------------------------
SELECT 
    id,
    name,
    cuisine,
    rating
FROM Restaurants
ORDER BY id ASC;

-- ----------------------------------------------------------------------------
-- TASK 5: Query for Daily Automation Summary (Rating > 4.5)
-- ----------------------------------------------------------------------------
SELECT 
    id,
    name,
    cuisine,
    rating
FROM Restaurants
WHERE rating > 4.5
ORDER BY rating DESC;
