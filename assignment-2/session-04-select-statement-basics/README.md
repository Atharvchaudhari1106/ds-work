# Session 4: SELECT Statement Basics

This folder contains the complete solutions for **Session 4 - SELECT Statement Basics** from the Data Science & Database coursework track.

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_04_select_statement_basics.ipynb`**](session_04_select_statement_basics.ipynb) | Complete self-contained notebook with pre-executed code cells, formatted DataFrame outputs, and concept explanations |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL**, **PostgreSQL**, and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up both tables, runs queries, and prints formatted results |
| **Sample SQLite Database** | [`music_and_food.db`](music_and_food.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Create `MusicPlaylist` & Retrieve All Songs
> **Problem Statement:** Create a table named `MusicPlaylist` with columns: `id`, `song_name`, `artist`, `genre`, and `duration`. Insert at least 5 records representing songs from your favorite Spotify playlist, then write a `SELECT` statement to retrieve all columns for all songs.

#### SQL Table Creation & Insertion:
```sql
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
```

#### SQL Retrieval Query:
```sql
SELECT * FROM MusicPlaylist;
```

#### Verified Output:
| id | song_name | artist | genre | duration |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Blinding Lights | The Weeknd | Synthwave / Pop | 3:20 |
| **2** | Starboy | The Weeknd | R&B / Pop | 3:50 |
| **3** | Shape of You | Ed Sheeran | Pop | 3:53 |
| **4** | Levitating | Dua Lipa | Disco-Pop | 3:23 |
| **5** | Tum Hi Ho | Arijit Singh | Bollywood Romantic | 4:22 |

---

### Task 2: Column Projection with `LIMIT 3`
> **Problem Statement:** Write a SQL query to display only the `song_name` and `artist` columns from the `MusicPlaylist` table, showing just the first 3 records using the `LIMIT` keyword.

#### SQL Query:
```sql
SELECT song_name, artist
FROM MusicPlaylist
LIMIT 3;
```

#### Verified Output:
| song_name | artist |
| :--- | :--- |
| **Blinding Lights** | The Weeknd |
| **Starboy** | The Weeknd |
| **Shape of You** | Ed Sheeran |

---

### Task 3: `FoodOrders` Table & Unique Restaurants (`DISTINCT`)
> **Problem Statement:** Suppose you have a table named `FoodOrders` with columns: `id`, `restaurant`, `food_item`, and `order_date`. Write a SQL query to list all unique restaurant names where you have placed orders, using the `DISTINCT` keyword.

#### SQL Table Creation & Data Ingestion:
```sql
CREATE TABLE FoodOrders (
    id INT PRIMARY KEY,
    restaurant VARCHAR(255) NOT NULL,
    food_item VARCHAR(255) NOT NULL,
    order_date DATE NOT NULL
);

INSERT INTO FoodOrders (id, restaurant, food_item, order_date) VALUES
(1, 'Biryani Blues', 'Hyderabadi Dum Biryani', '2026-10-20'),
(2, "Domino's Pizza", 'Farmhouse Pizza', '2026-10-21'),
(3, 'Biryani Blues', 'Chicken Tikka', '2026-10-22'),
(4, 'Punjab Grill', 'Dal Makhani', '2026-10-23'),
(5, "Domino's Pizza", 'Garlic Bread', '2026-10-24'),
(6, "Haldiram's", 'Chole Bhature', '2026-10-25');
```

#### SQL Query:
```sql
SELECT DISTINCT restaurant
FROM FoodOrders;
```

#### Verified Output:
| restaurant |
| :--- |
| **Biryani Blues** |
| **Domino's Pizza** |
| **Punjab Grill** |
| **Haldiram's** |

---

### Task 4: Column Aliasing (`AS 'Dish'` and `AS 'Date Ordered'`)
> **Problem Statement:** Write a SQL query on the `FoodOrders` table to select `food_item` as `'Dish'` and `order_date` as `'Date Ordered'`, displaying only these two columns with the column aliases in the output.

#### SQL Query:
```sql
SELECT 
    food_item AS "Dish",
    order_date AS "Date Ordered"
FROM FoodOrders;
```

#### Verified Output:
| Dish | Date Ordered |
| :--- | :--- |
| **Hyderabadi Dum Biryani** | 2026-10-20 |
| **Farmhouse Pizza** | 2026-10-21 |
| **Chicken Tikka** | 2026-10-22 |
| **Dal Makhani** | 2026-10-23 |
| **Garlic Bread** | 2026-10-24 |
| **Chole Bhature** | 2026-10-25 |

---

### Task 5: Debugging & Fixing SQL Query Mistake
> **Problem Statement:** You tried running this query: `SELECT DISTINCT food_item, restaurant FROM FoodOrders LIMIT 2`, but it returns an error or doesn't work as expected. Identify and fix the mistake in the query.  
> *Hint: Check the correct placement and usage of the LIMIT keyword in SQL syntax.*

#### 🔍 Identification of the Mistake:

1. **Missing `ORDER BY` (Non-Deterministic Behavior):**
   - In SQL, tables are fundamentally unordered mathematical sets.
   - When you invoke `LIMIT 2` without an `ORDER BY` clause, the SQL engine returns an **arbitrary** slice of rows based on storage or index caching. Consecutive executions or executions across different servers may yield inconsistent results.
   - Proper clause order is: `SELECT -> FROM -> [WHERE] -> [ORDER BY] -> LIMIT`.

2. **RDBMS Incompatibility (Microsoft SQL Server / Oracle):**
   - **Microsoft SQL Server (T-SQL):** The `LIMIT` keyword does **not** exist in T-SQL. Running this query throws:
     ```text
     Msg 156, Level 15: Incorrect syntax near the keyword 'LIMIT'.
     ```
     In T-SQL, you must use the `TOP` keyword:
     ```sql
     SELECT DISTINCT TOP 2 food_item, restaurant FROM FoodOrders;
     ```
   - **Oracle SQL:** Prior to Oracle 12c, `LIMIT` is unsupported; Oracle uses `WHERE ROWNUM <= 2` or `FETCH FIRST 2 ROWS ONLY`.

#### ✅ The Fixed Query:

**Standard SQL (MySQL, PostgreSQL, SQLite):**
```sql
SELECT DISTINCT food_item, restaurant
FROM FoodOrders
ORDER BY food_item ASC
LIMIT 2;
```

**Output of Fixed Query:**
| food_item | restaurant |
| :--- | :--- |
| **Chicken Tikka** | Biryani Blues |
| **Chole Bhature** | Haldiram's |

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Script:**
   ```powershell
   python assignments/session-04-select-statement-basics/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_04_select_statement_basics.ipynb`](session_04_select_statement_basics.ipynb) directly in VS Code / GitHub.
