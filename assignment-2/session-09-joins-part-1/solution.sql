-- =============================================================================
-- SESSION 9: JOINS - Part 1
-- Coursework / Assignment Submission
-- Database: zomato_joins (or foodie_db)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'restaurants' and 'dishes' Tables & Insert Sample Records
-- Constraints:
--   restaurants: id, name, city
--   dishes: id, restaurant_id, dish_name, price
--   Requirement: At least 3 restaurants and 2-3 dishes for each restaurant.
--   Enhanced test data: 
--     - Added restaurant 4 ('Cafe Coffee Day') with 0 dishes to verify LEFT JOIN.
--     - Added dish 110 ('Dragon Noodles') with invalid restaurant_id = 99 to verify RIGHT JOIN.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS dishes;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE dishes (
    id INT PRIMARY KEY,
    restaurant_id INT,
    dish_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

-- Insert Sample Restaurants
INSERT INTO restaurants (id, name, city) VALUES
(1, 'Biryani By Kilo', 'Hyderabad'),
(2, 'Haldiram', 'Nagpur'),
(3, 'Pizza Hut', 'Pune'),
(4, 'Cafe Coffee Day', 'Mumbai');  -- Empty restaurant for testing LEFT JOIN

-- Insert Sample Dishes
INSERT INTO dishes (id, restaurant_id, dish_name, price) VALUES
-- Dishes for Biryani By Kilo (restaurant_id = 1)
(101, 1, 'Hyderabadi Chicken Biryani', 350.00),
(102, 1, 'Mutton Dum Biryani', 480.00),
(103, 1, 'Mirchi Ka Salan', 120.00),

-- Dishes for Haldiram (restaurant_id = 2)
(104, 2, 'Raj Kachori', 140.00),
(105, 2, 'Chole Bhature', 180.00),
(106, 2, 'Gulab Jamun (2 pcs)', 90.00),

-- Dishes for Pizza Hut (restaurant_id = 3)
(107, 3, 'Margherita Pizza', 299.00),
(108, 3, 'Garlic Breadsticks', 149.00),
(109, 3, 'Farmhouse Veg Pizza', 399.00),

-- Orphaned dish with invalid restaurant_id = 99 for testing RIGHT JOIN
(110, 99, 'Dragon Noodles', 220.00);

-- Verify raw data in both tables:
SELECT * FROM restaurants;
SELECT * FROM dishes;

-- -----------------------------------------------------------------------------
-- TASK 2: INNER JOIN
-- Display each dish along with its restaurant name and city (Zomato UI style).
-- Shows only dishes that have a matching restaurant in the system.
-- -----------------------------------------------------------------------------
SELECT 
    d.id AS dish_id,
    d.dish_name,
    d.price,
    r.name AS restaurant_name,
    r.city
FROM dishes d
INNER JOIN restaurants r ON d.restaurant_id = r.id;

-- -----------------------------------------------------------------------------
-- TASK 3: LEFT JOIN
-- List all restaurants and their dishes, showing restaurants even if they
-- currently have no dishes on the menu (NULL for dish columns).
-- -----------------------------------------------------------------------------
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    d.id AS dish_id,
    d.dish_name,
    d.price
FROM restaurants r
LEFT JOIN dishes d ON r.id = d.restaurant_id;

-- -----------------------------------------------------------------------------
-- TASK 4: RIGHT JOIN
-- Display all dishes and their restaurant names, including any dishes that
-- might not be linked to a restaurant (simulating data integrity/orphaned dish error).
-- -----------------------------------------------------------------------------
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    d.id AS dish_id,
    d.dish_name,
    d.price,
    d.restaurant_id AS dish_restaurant_fk
FROM restaurants r
RIGHT JOIN dishes d ON r.id = d.restaurant_id;

-- Note: For database engines that do not natively support RIGHT JOIN,
-- an identical result set is achieved by flipping table order with LEFT JOIN:
-- SELECT r.id AS restaurant_id, r.name AS restaurant_name, r.city, 
--        d.id AS dish_id, d.dish_name, d.price, d.restaurant_id AS dish_restaurant_fk
-- FROM dishes d
-- LEFT JOIN restaurants r ON d.restaurant_id = r.id;

-- -----------------------------------------------------------------------------
-- TASK 5: SPOTIFY SCENARIO - Playlists and Songs
-- Scenario: Show a list of all playlists and the songs inside them, even if
-- some playlists are empty.
--
-- Explanation of JOIN Type:
-- We must use a LEFT JOIN (with 'playlists' on the LEFT and 'songs' on the RIGHT).
-- Why:
-- 1. INNER JOIN only retains rows where keys exist in both tables. Any newly
--    created or empty playlist with zero songs would be completely excluded.
-- 2. LEFT JOIN guarantees every single playlist from the left table is preserved
--    in the output. For empty playlists, the song columns will be populated
--    with NULL, enabling the UI to display '0 Songs' or 'Empty Playlist'.
-- -----------------------------------------------------------------------------

-- Demonstration Schema & Query for Task 5:
DROP TABLE IF EXISTS playlist_songs;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS playlists;

CREATE TABLE playlists (
    playlist_id INT PRIMARY KEY,
    playlist_name VARCHAR(100) NOT NULL,
    created_by VARCHAR(50) NOT NULL
);

CREATE TABLE songs (
    song_id INT PRIMARY KEY,
    playlist_id INT,
    title VARCHAR(100) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    duration_sec INT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);

INSERT INTO playlists (playlist_id, playlist_name, created_by) VALUES
(1, 'Gym Workout Beats', 'Atharv'),
(2, 'Acoustic Morning', 'Sneha'),
(3, 'Study Lo-Fi Focus', 'Rahul'),
(4, 'Road Trip 2026', 'Atharv');  -- Empty playlist with no songs yet

INSERT INTO songs (song_id, playlist_id, title, artist, duration_sec) VALUES
(201, 1, 'Eye of the Tiger', 'Survivor', 245),
(202, 1, 'Lose Yourself', 'Eminem', 326),
(203, 1, 'Till I Collapse', 'Eminem', 297),
(204, 2, 'Banana Pancakes', 'Jack Johnson', 192),
(205, 2, 'Here Comes the Sun', 'The Beatles', 185),
(206, 3, 'Sunset Lover', 'Petit Biscuit', 237);

-- Task 5 Target Query:
SELECT 
    p.playlist_id,
    p.playlist_name,
    p.created_by,
    s.song_id,
    s.title AS song_title,
    s.artist,
    s.duration_sec
FROM playlists p
LEFT JOIN songs s ON p.playlist_id = s.playlist_id;
