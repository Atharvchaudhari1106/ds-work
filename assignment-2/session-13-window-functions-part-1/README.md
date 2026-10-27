# Session 13: Window Functions - Part 1

## Overview & Objectives
This session introduces SQL **Window Functions** and ranking algorithms:
1. **Window Concept**: Performing non-aggregating analytical calculations where individual rows preserve their row-level identities.
2. **`ROW_NUMBER()`**: Generating strictly unique, consecutive sequence numbers (1, 2, 3...) regardless of tied values.
3. **`RANK()`**: Standard competition ranking where ties share the same rank and subsequent ranks are skipped (e.g. 1, 2, 2, 4).
4. **`DENSE_RANK()`**: Dense ranking where ties share the same rank without creating gaps (e.g. 1, 2, 2, 3).
5. **`PARTITION BY`**: Partitioning the calculation window by an attribute (e.g. `user_id`) to compute localized rankings within each partition.
6. **Top-N Per Group Pattern**: Filtering window function rankings using Common Table Expressions (CTEs) to extract top entities per group (e.g. Spotify's "Your Top Playlists").

---

## Task Solutions & Code Explanations

### Task 1: Create 'Playlists' Table & Insert Sample Data
**Requirement:** Create a table named `Playlists` with columns: `id`, `user_id`, `playlist_name`, and `total_likes`. Insert at least 8 sample rows with different users and playlists, making sure some playlists have the same `user_id`.

```sql
DROP TABLE IF EXISTS Playlists;

CREATE TABLE Playlists (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(100) NOT NULL,
    total_likes INT NOT NULL
);

INSERT INTO Playlists (id, user_id, playlist_name, total_likes) VALUES
-- User 101 (Atharv)
(1, 101, 'Gym Workout Beats', 15000),
(2, 101, 'Coding Lo-Fi Focus', 12000),
(3, 101, 'Rock Classics', 12000),         -- Tied with Coding Lo-Fi Focus
(4, 101, 'Chill Acoustic', 8500),
-- User 102 (Sneha)
(5, 102, 'Bollywood Dance Party', 18500),
(6, 102, 'Road Trip Anthems', 15000),      -- Tied with Gym Workout Beats
(7, 102, 'Evening Jazz & Chai', 9200),
-- User 103 (Rahul)
(8, 103, 'Deep House Vibes', 14000),
(9, 103, 'EDM Festival Bangers', 12000),   -- Tied with other 12000 playlists
(10, 103, 'Morning Motivation', 6000);
```

#### Base Data View:
| id | user_id | playlist_name | total_likes |
|---|---|---|---|
| 1 | 101 | Gym Workout Beats | 15000 |
| 2 | 101 | Coding Lo-Fi Focus | 12000 |
| 3 | 101 | Rock Classics | 12000 |
| 4 | 101 | Chill Acoustic | 8500 |
| 5 | 102 | Bollywood Dance Party | 18500 |
| 6 | 102 | Road Trip Anthems | 15000 |
| 7 | 102 | Evening Jazz & Chai | 9200 |
| 8 | 103 | Deep House Vibes | 14000 |
| 9 | 103 | EDM Festival Bangers | 12000 |
| 10 | 103 | Morning Motivation | 6000 |

---

### Task 2: ROW_NUMBER() with OVER() Clause
**Requirement:** Write a SQL query using `ROW_NUMBER()` and the `OVER()` clause to assign a unique row number to each playlist, ordered by `total_likes` in descending order.

```sql
SELECT 
    ROW_NUMBER() OVER (ORDER BY total_likes DESC) AS row_num,
    id AS playlist_id,
    playlist_name,
    user_id,
    total_likes
FROM Playlists;
```

#### Output:
| row_num | playlist_id | playlist_name | user_id | total_likes |
|---|---|---|---|---|
| 1 | 5 | Bollywood Dance Party | 102 | 18500 |
| 2 | 1 | Gym Workout Beats | 101 | 15000 |
| 3 | 6 | Road Trip Anthems | 102 | 15000 |
| 4 | 8 | Deep House Vibes | 103 | 14000 |
| 5 | 2 | Coding Lo-Fi Focus | 101 | 12000 |
| 6 | 3 | Rock Classics | 101 | 12000 |
| 7 | 9 | EDM Festival Bangers | 103 | 12000 |
| 8 | 7 | Evening Jazz & Chai | 102 | 9200 |
| 9 | 4 | Chill Acoustic | 101 | 8500 |
| 10 | 10 | Morning Motivation | 103 | 6000 |

> **Key Takeaway:** `ROW_NUMBER()` generates strictly sequential integers 1 through 10. Even though items tied at 15,000 and 12,000 likes, no duplicate row numbers exist.

---

### Task 3: RANK() with OVER() Clause
**Requirement:** Use the `RANK()` function with the `OVER()` clause to rank all playlists by `total_likes`, and display the `playlist_name`, `user_id`, `total_likes`, and their rank.

```sql
SELECT 
    RANK() OVER (ORDER BY total_likes DESC) AS rank_pos,
    playlist_name,
    user_id,
    total_likes
FROM Playlists;
```

#### Output:
| rank_pos | playlist_name | user_id | total_likes |
|---|---|---|---|
| 1 | Bollywood Dance Party | 102 | 18500 |
| **2** | **Gym Workout Beats** | **101** | **15000** |
| **2** | **Road Trip Anthems** | **102** | **15000** |
| 4 | Deep House Vibes | 103 | 14000 |
| **5** | **Coding Lo-Fi Focus** | **101** | **12000** |
| **5** | **Rock Classics** | **101** | **12000** |
| **5** | **EDM Festival Bangers** | **103** | **12000** |
| 8 | Evening Jazz & Chai | 102 | 9200 |
| 9 | Chill Acoustic | 101 | 8500 |
| 10 | Morning Motivation | 103 | 6000 |

> **Key Takeaway:** Both 15,000-like playlists share Rank **2**, so Rank 3 is skipped and the next rank is **4**. Similarly, the three 12,000-like playlists share Rank **5**, so Ranks 6 and 7 are skipped and the next rank is **8**.

---

### Task 4: DENSE_RANK() with PARTITION BY user_id
**Requirement:** Write a SQL query using `DENSE_RANK()` and `PARTITION BY user_id` to rank each user's playlists by `total_likes`, showing `playlist_name`, `user_id`, `total_likes`, and dense rank.

```sql
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
```

#### Output:
| user_id | user_dense_rank | playlist_name | total_likes |
|---|---|---|---|
| 101 | 1 | Gym Workout Beats | 15000 |
| **101** | **2** | **Coding Lo-Fi Focus** | **12000** |
| **101** | **2** | **Rock Classics** | **12000** |
| 101 | 3 | Chill Acoustic | 8500 |
| 102 | 1 | Bollywood Dance Party | 18500 |
| 102 | 2 | Road Trip Anthems | 15000 |
| 102 | 3 | Evening Jazz & Chai | 9200 |
| 103 | 1 | Deep House Vibes | 14000 |
| 103 | 2 | EDM Festival Bangers | 12000 |
| 103 | 3 | Morning Motivation | 6000 |

> **Key Takeaway:** Rankings reset to 1 for every distinct `user_id`. When User 101 has tied playlists at 12,000 likes, both receive Rank **2**, and the next rank is **3** without any gap.

---

### Task 5: Top 2 Playlists Per User (Spotify 'Your Top Playlists')
**Requirement:** Imagine you want to show the top 2 playlists per user based on `total_likes`, like Spotify's 'Your Top Playlists' feature. Write a query using a window function to select only the top 2 playlists for each user.

```sql
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
```

#### Output:
| user_id | playlist_rank | playlist_name | total_likes |
|---|---|---|---|
| 101 | 1 | Gym Workout Beats | 15000 |
| 101 | 2 | Coding Lo-Fi Focus | 12000 |
| 102 | 1 | Bollywood Dance Party | 18500 |
| 102 | 2 | Road Trip Anthems | 15000 |
| 103 | 1 | Deep House Vibes | 14000 |
| 103 | 2 | EDM Festival Bangers | 12000 |

> **Key Takeaway:** Wrapping the window function inside a CTE allows filtering on the calculated rank (`WHERE rank_in_user <= 2`), extracting exactly the top 2 playlists for each user.

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-13-window-functions-part-1/solution.sql): Executable SQL queries for Tasks 1 to 5.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-13-window-functions-part-1/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_13_window_functions_part_1.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-13-window-functions-part-1/session_13_window_functions_part_1.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`spotify_windows.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-13-window-functions-part-1/spotify_windows.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-13-window-functions-part-1/README.md): Comprehensive documentation.
