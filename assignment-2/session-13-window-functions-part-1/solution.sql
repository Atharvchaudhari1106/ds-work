-- =============================================================================
-- SESSION 13: Window Functions - Part 1
-- Coursework / Assignment Submission
-- Database: spotify_windows_db
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'Playlists' Table & Insert at least 8 Sample Records
-- Columns: id, user_id, playlist_name, total_likes
-- Includes ties in likes to demonstrate window ranking semantics.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Playlists;

CREATE TABLE Playlists (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(100) NOT NULL,
    total_likes INT NOT NULL
);

INSERT INTO Playlists (id, user_id, playlist_name, total_likes) VALUES
-- User 101 Playlists
(1, 101, 'Gym Workout Beats', 15000),
(2, 101, 'Coding Lo-Fi Focus', 12000),
(3, 101, 'Rock Classics', 12000),         -- Tie with Lo-Fi Focus
(4, 101, 'Chill Acoustic', 8500),

-- User 102 Playlists
(5, 102, 'Bollywood Dance Party', 18500),
(6, 102, 'Road Trip Anthems', 15000),      -- Tie with Gym Workout Beats
(7, 102, 'Evening Jazz & Chai', 9200),

-- User 103 Playlists
(8, 103, 'Deep House Vibes', 14000),
(9, 103, 'EDM Festival Bangers', 12000),   -- Tie with other 12000 playlists
(10, 103, 'Morning Motivation', 6000);

-- Verify raw table data:
SELECT * FROM Playlists;


-- -----------------------------------------------------------------------------
-- TASK 2: ROW_NUMBER() with OVER() Clause
-- Problem: Write a SQL query using ROW_NUMBER() and the OVER() clause to assign 
-- a unique row number to each playlist, ordered by total_likes in descending order.
-- -----------------------------------------------------------------------------
SELECT 
    ROW_NUMBER() OVER (ORDER BY total_likes DESC) AS row_num,
    id AS playlist_id,
    playlist_name,
    user_id,
    total_likes
FROM Playlists;


-- -----------------------------------------------------------------------------
-- TASK 3: RANK() with OVER() Clause
-- Problem: Use the RANK() function with the OVER() clause to rank all playlists 
-- by total_likes, and display the playlist_name, user_id, total_likes, and their rank.
-- Note: RANK() leaves gaps after ties (e.g. 1, 2, 2, 4).
-- -----------------------------------------------------------------------------
SELECT 
    RANK() OVER (ORDER BY total_likes DESC) AS rank_pos,
    playlist_name,
    user_id,
    total_likes
FROM Playlists;


-- -----------------------------------------------------------------------------
-- TASK 4: DENSE_RANK() with PARTITION BY user_id
-- Problem: Write a SQL query using DENSE_RANK() and PARTITION BY user_id to rank 
-- each user's playlists by total_likes, showing playlist_name, user_id, total_likes, 
-- and dense rank.
-- Hint: This shows how popular each playlist is within each user's account, 
-- similar to Spotify ranking a user's top personal playlists without gaps.
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    DENSE_RANK() OVER (
        PARTITION BY user_id 
        ORDER BY total_likes DESC
    ) AS user_dense_rank,
    playlist_name,
    total_likes
FROM Playlists
ORDER BY user_id ASC, user_dense_rank ASC;


-- -----------------------------------------------------------------------------
-- TASK 5: Top 2 Playlists Per User (Spotify 'Your Top Playlists')
-- Problem: Imagine you want to show the top 2 playlists per user based on 
-- total_likes, like Spotify's 'Your Top Playlists' feature. Write a query using 
-- a window function to select only the top 2 playlists for each user.
-- -----------------------------------------------------------------------------
WITH RankedUserPlaylists AS (
    SELECT 
        user_id,
        playlist_name,
        total_likes,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY total_likes DESC
        ) AS rank_in_user
    FROM Playlists
)
SELECT 
    user_id,
    rank_in_user AS playlist_rank,
    playlist_name,
    total_likes
FROM RankedUserPlaylists
WHERE rank_in_user <= 2
ORDER BY user_id ASC, rank_in_user ASC;

-- Alternative Version Using DENSE_RANK() (Includes ties if two playlists share #2):
-- WITH DenseRankedPlaylists AS (
--     SELECT user_id, playlist_name, total_likes,
--            DENSE_RANK() OVER (PARTITION BY user_id ORDER BY total_likes DESC) AS user_rank
--     FROM Playlists
-- )
-- SELECT user_id, user_rank, playlist_name, total_likes
-- FROM DenseRankedPlaylists
-- WHERE user_rank <= 2
-- ORDER BY user_id, user_rank;
