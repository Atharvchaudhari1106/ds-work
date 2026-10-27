-- =============================================================================
-- SESSION 1: Database Introduction & SQL Basics
-- Coursework / Assignment Submission
-- Database: music_streaming_app
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create Database
-- -----------------------------------------------------------------------------
-- For MySQL:
CREATE DATABASE IF NOT EXISTS music_streaming_app;
USE music_streaming_app;

-- For PostgreSQL:
-- CREATE DATABASE music_streaming_app;
-- \c music_streaming_app;

-- -----------------------------------------------------------------------------
-- TASK 2: Create Table 'playlists'
-- Columns:
--   - playlist_id: Integer, Primary Key
--   - name: Varchar (playlist title)
--   - created_by: Varchar (user who created the playlist)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS playlists;

CREATE TABLE playlists (
    playlist_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_by VARCHAR(100) NOT NULL
);

-- -----------------------------------------------------------------------------
-- TASK 3: Insert Sample Rows
-- Insert 3 sample playlists created by different users
-- -----------------------------------------------------------------------------
INSERT INTO playlists (playlist_id, name, created_by) VALUES
(1, 'Bollywood Hits', 'Amit'),
(2, 'Chill Vibes', 'Pooja'),
(3, 'Workout Mix', 'Rahul');

-- Verify full table content:
SELECT * FROM playlists;

-- -----------------------------------------------------------------------------
-- TASK 4: Query Playlists Created by 'Amit'
-- Using WHERE clause to filter by 'created_by' column
-- -----------------------------------------------------------------------------
SELECT playlist_id, name, created_by
FROM playlists
WHERE created_by = 'Amit';

-- -----------------------------------------------------------------------------
-- TASK 5: Conceptual Explanation (Table vs Row vs Column)
-- Context: Food Delivery App (Zomato)
--
-- 1. TABLE ('Orders'):
--    The complete collection of all order data in Zomato.
--    Like the master ledger storing every meal delivery request.
--
-- 2. COLUMN ('restaurant_name', 'total_amount', etc.):
--    A specific vertical attribute/category describing a property of the order.
--
-- 3. ROW ('Order #101'):
--    A single horizontal record representing one complete individual transaction:
--    (101, 'Rohan Sharma', 'Biryani Blues', 450.00, 'Delivered')
-- =============================================================================
