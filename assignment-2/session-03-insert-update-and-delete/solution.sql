-- =============================================================================
-- SESSION 3: INSERT, UPDATE & DELETE
-- Coursework / Assignment Submission
-- Database: playlist_app (or music_streaming_app)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: Create 'Playlist' Table & Insert 1 Favorite Song
-- Columns:
--   - id: INT, primary key
--   - song_name: VARCHAR(255)
--   - artist: VARCHAR(255)
--   - duration: INT (in seconds)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Playlist;

CREATE TABLE Playlist (
    id INT PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    duration INT NOT NULL
);

-- Insert 1 single row for favorite song (with deliberate typo 'Arjit Singh' for Task 3)
INSERT INTO Playlist (id, song_name, artist, duration) VALUES
(1, 'Tum Hi Ho', 'Arjit Singh', 262);

SELECT * FROM Playlist;

-- -----------------------------------------------------------------------------
-- TASK 2: Insert 3 New Rows for Recently Listened Songs
-- -----------------------------------------------------------------------------
INSERT INTO Playlist (id, song_name, artist, duration) VALUES
(2, 'Brown Munde', 'AP Dhillon', 260),
(3, 'Summer High', 'AP Dhillon', 175),
(4, 'Short Interlude', 'The Weeknd', 90);

SELECT * FROM Playlist;

-- -----------------------------------------------------------------------------
-- TASK 3: Fix Typo Using UPDATE with WHERE Clause
-- Change 'Arjit Singh' to 'Arijit Singh'
-- -----------------------------------------------------------------------------
UPDATE Playlist
SET artist = 'Arijit Singh'
WHERE artist = 'Arjit Singh';

-- Verify the update:
SELECT * FROM Playlist WHERE id = 1;

-- -----------------------------------------------------------------------------
-- TASK 4: Delete Song with Duration Less Than 120 Seconds
-- Target: 'Short Interlude' (duration = 90)
-- -----------------------------------------------------------------------------
DELETE FROM Playlist
WHERE duration < 120;

-- Verify deletion:
SELECT * FROM Playlist;

-- -----------------------------------------------------------------------------
-- TASK 5: Update Song Name to add '(Remix)' for 'AP Dhillon' where duration > 180
-- Only 'Brown Munde' (260s) is updated; 'Summer High' (175s) remains unchanged.
-- -----------------------------------------------------------------------------
-- Standard SQL / SQLite / PostgreSQL:
UPDATE Playlist
SET song_name = song_name || ' (Remix)'
WHERE artist = 'AP Dhillon' AND duration > 180;

-- MySQL Equivalent:
-- UPDATE Playlist
-- SET song_name = CONCAT(song_name, ' (Remix)')
-- WHERE artist = 'AP Dhillon' AND duration > 180;

-- Final verification query:
SELECT * FROM Playlist;
