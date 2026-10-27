# Session 10: JOINS - Part 2

## Overview & Objectives
This session explores advanced multi-table relational patterns and performance optimization in SQL:
1. **`FULL OUTER JOIN`**: Symmetrical outer joins preserving unlinked rows from both parent and child relations simultaneously.
2. **`SELF JOIN`**: Querying hierarchical tree structures (such as nested Spotify folders/playlists) within a single table.
3. **Multi-Table Chained `LEFT JOIN`s**: Connecting 3 or more tables (`Users -> Orders -> Payments`) while preserving primary records at every step.
4. **Duplicate Elimination in One-to-Many Relationships**: Diagnosing why joining parent-child entities multiplies parent records and solving it using `DISTINCT` and `GROUP BY`.
5. **Join Key Performance & Indexing**: Comparing numeric surrogate key joins (`INT`) against alphanumeric business string joins (`VARCHAR`) in database engines (e.g. Flipkart catalog).

---

## Task Solutions & Code Explanations

### Task 1: FULL JOIN on Influencers & Collaborations
**Requirement:** Create two tables: `Influencers` (`id`, `name`) and `Collaborations` (`id`, `influencer1_id`, `influencer2_id`, `collab_date`). Write a SQL `FULL JOIN` query to list all influencers and show their collaboration partner names if any, including influencers with no collaborations.

```sql
DROP TABLE IF EXISTS Collaborations;
DROP TABLE IF EXISTS Influencers;

CREATE TABLE Influencers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Collaborations (
    id INT PRIMARY KEY,
    influencer1_id INT,
    influencer2_id INT,
    collab_date DATE NOT NULL
);

-- Insert Sample Influencers
INSERT INTO Influencers (id, name) VALUES
(1, 'Virat Kohli'),
(2, 'Anushka Sharma'),
(3, 'CarryMinati'),
(4, 'Bhuvan Bam'),
(5, 'Technical Guruji'),  -- Solo creator (No collabs)
(6, 'Prajakta Koli');      -- Solo creator (No collabs)

-- Insert Sample Collaborations
INSERT INTO Collaborations (id, influencer1_id, influencer2_id, collab_date) VALUES
(101, 1, 2, '2026-01-15'),  -- Virat & Anushka
(102, 3, 4, '2026-02-10'),  -- CarryMinati & Bhuvan Bam
(103, 1, 3, '2026-03-01'),  -- Virat & CarryMinati
(104, 99, 100, '2026-04-05'); -- Unlinked external collab

-- FULL JOIN Query
SELECT 
    i1.id AS influencer_id,
    i1.name AS influencer_name,
    c.id AS collab_id,
    c.collab_date,
    i2.name AS partner_name
FROM Influencers i1
FULL JOIN Collaborations c ON i1.id = c.influencer1_id
LEFT JOIN Influencers i2 ON c.influencer2_id = i2.id;
```

#### Output:
| influencer_id | influencer_name | collab_id | collab_date | partner_name |
|---|---|---|---|---|
| 1 | Virat Kohli | 101 | 2026-01-15 | Anushka Sharma |
| 1 | Virat Kohli | 103 | 2026-03-01 | CarryMinati |
| 2 | Anushka Sharma | *NULL* | *NULL* | *NULL* |
| 3 | CarryMinati | 102 | 2026-02-10 | Bhuvan Bam |
| 4 | Bhuvan Bam | *NULL* | *NULL* | *NULL* |
| **5** | **Technical Guruji** | *NULL* | *NULL* | *NULL* |
| **6** | **Prajakta Koli** | *NULL* | *NULL* | *NULL* |
| *NULL* | *NULL* | **104** | **2026-04-05** | *NULL* |

> **Key Takeaway:** `FULL JOIN` retains solo creators (*Technical Guruji*, *Prajakta Koli*) on the left side as well as unlinked collaboration records (ID 104) on the right side.

---

### Task 2: SELF JOIN on Playlists (Spotify Nested Playlists)
**Requirement:** Using a `SELF JOIN`, write a query on a table called `Playlists` (`id`, `user_id`, `playlist_name`, `parent_playlist_id`) to display each playlist alongside its parent playlist name, similar to how Spotify shows nested playlists. (*Hint: Join Playlists with itself on parent_playlist_id = id.*)

```sql
DROP TABLE IF EXISTS Playlists;

CREATE TABLE Playlists (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(100) NOT NULL,
    parent_playlist_id INT
);

INSERT INTO Playlists (id, user_id, playlist_name, parent_playlist_id) VALUES
(1, 101, 'Top Hits 2026', NULL),              -- Root playlist (no parent)
(2, 101, 'Workout Motivation', NULL),          -- Root folder / parent playlist
(3, 101, 'High Intensity Cardio', 2),          -- Nested child of 2
(4, 101, 'Heavy Weightlifting', 2),            -- Nested child of 2
(5, 102, 'Chill & Acoustic', NULL),            -- Root folder / parent playlist
(6, 102, 'Sunday Morning Coffee', 5),          -- Nested child of 5
(7, 102, 'Rainy Day Acoustic', 5);             -- Nested child of 5

-- SELF JOIN Query (Preserving root playlists with LEFT JOIN)
SELECT 
    child.id AS playlist_id,
    child.playlist_name,
    child.parent_playlist_id,
    COALESCE(parent.playlist_name, 'None (Root Playlist)') AS parent_playlist_name
FROM Playlists child
LEFT JOIN Playlists parent ON child.parent_playlist_id = parent.id;
```

#### Output:
| playlist_id | playlist_name | parent_playlist_id | parent_playlist_name |
|---|---|---|---|
| 1 | Top Hits 2026 | *NULL* | None (Root Playlist) |
| 2 | Workout Motivation | *NULL* | None (Root Playlist) |
| 3 | High Intensity Cardio | 2 | Workout Motivation |
| 4 | Heavy Weightlifting | 2 | Workout Motivation |
| 5 | Chill & Acoustic | *NULL* | None (Root Playlist) |
| 6 | Sunday Morning Coffee | 5 | Chill & Acoustic |
| 7 | Rainy Day Acoustic | 5 | Chill & Acoustic |

> **Key Takeaway:** Aliasing the table twice as `child` and `parent` allows SQL to traverse the self-referential tree structure. Using `LEFT JOIN` ensures root playlists are not omitted.

---

### Task 3: Multiple JOINs across 3 Tables (Users, Orders, Payments)
**Requirement:** Given three tables: `Users` (`id`, `username`), `Orders` (`id`, `user_id`, `order_date`), and `Payments` (`id`, `order_id`, `amount`), write a SQL query using multiple JOINs to display each username, their order date, and payment amount, showing all users even if they have no orders or payments.

```sql
SELECT 
    u.id AS user_id,
    u.username,
    o.id AS order_id,
    o.order_date,
    p.id AS payment_id,
    p.amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
LEFT JOIN Payments p ON o.id = p.order_id;
```

#### Output:
| user_id | username | order_id | order_date | payment_id | amount |
|---|---|---|---|---|---|
| 1 | atharv_c | 101 | 2026-03-01 | 1001 | 750.00 |
| 2 | sneha_p | 102 | 2026-03-05 | 1002 | 1200.00 |
| 2 | sneha_p | 103 | 2026-03-10 | 1003 | 350.00 |
| **3** | **rahul_v** | 104 | 2026-03-12 | *NULL* | *NULL* |
| **4** | **priya_m** | *NULL* | *NULL* | *NULL* | *NULL* |

> **Key Takeaway:** Chained `LEFT JOIN`s preserve users who have zero orders (`priya_m`), as well as orders that are placed but awaiting payment confirmation (`rahul_v`).

---

### Task 4: Eliminating Duplicates in One-to-Many Relationships (Restaurants & Reviews)
**Requirement:** You notice that your JOIN query between Zomato's Restaurants and Reviews tables is returning duplicate rows for some restaurants. Modify your query to eliminate duplicates and explain in one line why the duplicates were happening. (*Hint: Use DISTINCT or GROUP BY and consider the relationship between restaurants and reviews.*)

#### One-Line Explanation:
> **"Duplicates occur because the relationship between Restaurants and Reviews is One-to-Many (1:N), causing the parent restaurant row to duplicate for every matching review row."**

#### Solution 1: Using `DISTINCT` (Filters to unique restaurant identities)
```sql
SELECT DISTINCT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city
FROM Restaurants r
INNER JOIN Reviews rev ON r.id = rev.restaurant_id;
```

#### Solution 2: Using `GROUP BY` (Aggregates child review metrics)
```sql
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    COUNT(rev.id) AS total_reviews,
    ROUND(AVG(rev.rating), 2) AS avg_rating
FROM Restaurants r
LEFT JOIN Reviews rev ON r.id = rev.restaurant_id
GROUP BY r.id, r.name, r.city;
```

#### Group By Aggregation Output:
| restaurant_id | restaurant_name | city | total_reviews | avg_rating |
|---|---|---|---|---|
| 1 | Truffles | Bangalore | 3 | 4.50 |
| 2 | Peter Cat | Kolkata | 2 | 4.80 |
| 3 | Haldiram | Nagpur | 1 | 4.00 |
| 4 | Barbeque Nation | Mumbai | 0 | *NULL* |

---

### Task 5: Comparing Two JOIN Conditions on Products & Categories (Flipkart Model)
**Requirement:** Write two different JOIN queries on a `Products` and `Categories` table (like Flipkart) to list all products with their category names, but use different join conditions in each. Briefly explain which join condition is more efficient and why.

#### Query 1: Join on Integer Surrogate Foreign Key
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.price,
    c.category_name
FROM Products p
INNER JOIN Categories c ON p.category_id = c.category_id;
```

#### Query 2: Join on String / Natural Business Key
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.price,
    c.category_name
FROM Products p
INNER JOIN Categories c ON p.category_code = c.category_code;
```

#### Efficiency Comparison:
**Condition 1 (`p.category_id = c.category_id`) is significantly more efficient** than Condition 2 for three core engineering reasons:
1. **CPU & ALU Register Execution:** Fixed-width 4-byte/8-byte integers (`INT / BIGINT`) compare in a single CPU instruction clock cycle. Variable-length character strings (`VARCHAR`) require character-by-character scanning and locale collation overhead.
2. **B-Tree Index Density & I/O Reduction:** Numeric indexes have a much higher branching factor. More integer keys fit into an 8KB memory page compared to long string keys, drastically lowering cache misses and disk reads.
3. **Hash Join Optimization:** Modern database optimizers build hash tables faster with uniform bitwise integer hashing, yielding near-zero collision rates compared to string hashing.

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-10-joins-part-2/solution.sql): Executable SQL queries for Tasks 1 to 5.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-10-joins-part-2/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_10_joins_part_2.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-10-joins-part-2/session_10_joins_part_2.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`joins_part2.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-10-joins-part-2/joins_part2.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-10-joins-part-2/README.md): Comprehensive documentation.
