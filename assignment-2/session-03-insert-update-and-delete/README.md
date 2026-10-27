# Session 3: INSERT, UPDATE & DELETE

This folder contains the complete solutions for **Session 3 - INSERT, UPDATE & DELETE** from the Data Science & Database coursework track (`assignment-2`).

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_03_insert_update_and_delete.ipynb`**](session_03_insert_update_and_delete.ipynb) | Complete self-contained notebook with pre-executed code cells, before/after DataFrame outputs, and DML safety principles |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL**, **PostgreSQL**, and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, performs DML operations, and prints table state changes |
| **Sample SQLite Database** | [`playlist_app.db`](playlist_app.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Create `Playlist` Table & Insert Single Favorite Song
> **Problem Statement:** Create a table called `Playlist` with columns: `id` (INT, primary key), `song_name` (VARCHAR), `artist` (VARCHAR), and `duration` (INT, seconds). Insert a single row for your current favorite song.

#### SQL Statement:
```sql
CREATE TABLE Playlist (
    id INT PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    duration INT NOT NULL
);

INSERT INTO Playlist (id, song_name, artist, duration)
VALUES (1, 'Tum Hi Ho', 'Arjit Singh', 262);
```
*(Note: We deliberately include the typo `'Arjit Singh'` to be corrected in Task 3).*

#### Output After Task 1:
| id | song_name | artist | duration |
| :---: | :--- | :--- | :---: |
| **1** | Tum Hi Ho | Arjit Singh | 262 |

---

### Task 2: Insert 3 Recently Listened Spotify Songs
> **Problem Statement:** Insert 3 new rows into the `Playlist` table for songs you recently listened to on Spotify, including their `song_name`, `artist`, and `duration`.

#### SQL Statement:
```sql
INSERT INTO Playlist (id, song_name, artist, duration) VALUES
(2, 'Brown Munde', 'AP Dhillon', 260),
(3, 'Summer High', 'AP Dhillon', 175),
(4, 'Short Interlude', 'The Weeknd', 90);
```

#### Output After Task 2:
| id | song_name | artist | duration |
| :---: | :--- | :--- | :---: |
| **1** | Tum Hi Ho | Arjit Singh | 262 |
| **2** | Brown Munde | AP Dhillon | 260 |
| **3** | Summer High | AP Dhillon | 175 |
| **4** | Short Interlude | The Weeknd | 90 |

---

### Task 3: Fix Typo Using `UPDATE ... WHERE`
> **Problem Statement:** Update the artist name for one of your `Playlist` entries to fix a typo (for example, change `'Arjit Singh'` to `'Arijit Singh'`) using the `UPDATE` statement with a `WHERE` clause.

#### SQL Statement:
```sql
UPDATE Playlist
SET artist = 'Arijit Singh'
WHERE artist = 'Arjit Singh';
```

#### Output After Task 3 (Typo Fixed):
| id | song_name | artist | duration |
| :---: | :--- | :--- | :---: |
| **1** | Tum Hi Ho | **Arijit Singh** | 262 |
| **2** | Brown Munde | AP Dhillon | 260 |
| **3** | Summer High | AP Dhillon | 175 |
| **4** | Short Interlude | The Weeknd | 90 |

---

### Task 4: Delete Short Songs (`duration < 120`)
> **Problem Statement:** Delete a song from the `Playlist` table where the duration is less than 120 seconds using the `DELETE` statement and a `WHERE` clause.  
> *Hint: Make sure your `WHERE` clause is specific so you don't accidentally delete all rows.*

#### SQL Statement:
```sql
DELETE FROM Playlist
WHERE duration < 120;
```

#### Output After Task 4 (`'Short Interlude'` Removed):
| id | song_name | artist | duration |
| :---: | :--- | :--- | :---: |
| **1** | Tum Hi Ho | Arijit Singh | 262 |
| **2** | Brown Munde | AP Dhillon | 260 |
| **3** | Summer High | AP Dhillon | 175 |

---

### Task 5: Compound `UPDATE` (AP Dhillon Songs > 180s)
> **Problem Statement:** Write an SQL statement that would update the `song_name` for all songs by `'AP Dhillon'` in your `Playlist` to add `'(Remix)'` at the end of the name, but only if the duration is more than 180 seconds.  
> *Constraint: Combine UPDATE with WHERE to target only the correct rows.*

#### SQL Statement:
```sql
-- Standard ANSI SQL / SQLite / PostgreSQL:
UPDATE Playlist
SET song_name = song_name || ' (Remix)'
WHERE artist = 'AP Dhillon' AND duration > 180;

-- MySQL Equivalent:
-- UPDATE Playlist
-- SET song_name = CONCAT(song_name, ' (Remix)')
-- WHERE artist = 'AP Dhillon' AND duration > 180;
```

#### Condition Evaluation:
- `'Brown Munde'`: `artist = 'AP Dhillon'` AND `260 > 180` $\rightarrow$ **Condition TRUE $\rightarrow$ Appends `(Remix)`**
- `'Summer High'`: `artist = 'AP Dhillon'` AND `175 > 180` $\rightarrow$ **Condition FALSE $\rightarrow$ Unchanged**
- `'Tum Hi Ho'`: `artist = 'Arijit Singh'` $\rightarrow$ **Condition FALSE $\rightarrow$ Unchanged**

#### Final Output After Task 5:
| id | song_name | artist | duration |
| :---: | :--- | :--- | :---: |
| **1** | Tum Hi Ho | Arijit Singh | 262 |
| **2** | **Brown Munde (Remix)** | AP Dhillon | 260 |
| **3** | Summer High | AP Dhillon | 175 |

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Runner:**
   ```powershell
   python assignment-2/session-03-insert-update-and-delete/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_03_insert_update_and_delete.ipynb`](session_03_insert_update_and_delete.ipynb) directly in VS Code / GitHub.
