-- =============================================================================
-- SESSION 4: SELECT Statement Basics
-- Coursework / Assignment Submission
-- Database: music_and_food (or music_streaming_app)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create Table 'MusicPlaylist' & Insert 5 Spotify Records
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS MusicPlaylist;

CREATE TABLE MusicPlaylist (
    id INT PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    duration VARCHAR(20) NOT NULL
);

INSERT INTO MusicPlaylist (id, song_name, artist, genre, duration) VALUES
(1, 'Blinding Lights', 'The Weeknd', 'Synthwave / Pop', '3:20'),
(2, 'Starboy', 'The Weeknd', 'R&B / Pop', '3:50'),
(3, 'Shape of You', 'Ed Sheeran', 'Pop', '3:53'),
(4, 'Levitating', 'Dua Lipa', 'Disco-Pop', '3:23'),
(5, 'Tum Hi Ho', 'Arijit Singh', 'Bollywood Romantic', '4:22');

-- Retrieve all columns for all songs:
SELECT * FROM MusicPlaylist;

-- -----------------------------------------------------------------------------
-- TASK 2: Display song_name and artist with LIMIT 3
-- -----------------------------------------------------------------------------
SELECT song_name, artist
FROM MusicPlaylist
LIMIT 3;

-- -----------------------------------------------------------------------------
-- TASK 3: FoodOrders Table & DISTINCT Restaurants
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS FoodOrders;

CREATE TABLE FoodOrders (
    id INT PRIMARY KEY,
    restaurant VARCHAR(255) NOT NULL,
    food_item VARCHAR(255) NOT NULL,
    order_date DATE NOT NULL
);

INSERT INTO FoodOrders (id, restaurant, food_item, order_date) VALUES
(1, 'Biryani Blues', 'Hyderabadi Dum Biryani', '2026-10-20'),
(2, 'Domino''s Pizza', 'Farmhouse Pizza', '2026-10-21'),
(3, 'Biryani Blues', 'Chicken Tikka', '2026-10-22'),
(4, 'Punjab Grill', 'Dal Makhani', '2026-10-23'),
(5, 'Domino''s Pizza', 'Garlic Bread', '2026-10-24'),
(6, 'Haldiram''s', 'Chole Bhature', '2026-10-25');

-- List all unique restaurant names using DISTINCT:
SELECT DISTINCT restaurant
FROM FoodOrders;

-- -----------------------------------------------------------------------------
-- TASK 4: Column Aliases ('Dish' and 'Date Ordered')
-- -----------------------------------------------------------------------------
SELECT 
    food_item AS "Dish",
    order_date AS "Date Ordered"
FROM FoodOrders;

-- -----------------------------------------------------------------------------
-- TASK 5: Identify and Fix Query Mistake
-- Original problematic query:
--   SELECT DISTINCT food_item, restaurant FROM FoodOrders LIMIT 2
--
-- ANALYSIS & FIXES:
-- 1. Standard SQL (MySQL, PostgreSQL, SQLite):
--    Without an ORDER BY clause, LIMIT produces non-deterministic results.
--    In correct SQL clause ordering: SELECT -> FROM -> ORDER BY -> LIMIT.
-- -----------------------------------------------------------------------------
SELECT DISTINCT food_item, restaurant
FROM FoodOrders
ORDER BY food_item ASC
LIMIT 2;

-- 2. Microsoft SQL Server (T-SQL) Compatibility:
--    If running on SQL Server, LIMIT is invalid syntax and throws an error.
--    T-SQL requires TOP:
--    SELECT DISTINCT TOP 2 food_item, restaurant FROM FoodOrders;
--
-- 3. Oracle SQL Compatibility:
--    Oracle 12c+ requires:
--    SELECT DISTINCT food_item, restaurant FROM FoodOrders FETCH FIRST 2 ROWS ONLY;
