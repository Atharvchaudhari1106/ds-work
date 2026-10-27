# Session 9: JOINS - Part 1

## Overview & Objectives
This session covers foundational relational algebra and multi-table operations in SQL using **`INNER JOIN`**, **`LEFT JOIN`**, and **`RIGHT JOIN`**. Real-world applications like **Zomato** and **Spotify** are modeled to demonstrate how parent-child relationships, missing data, and referential integrity anomalies behave across different join algorithms.

---

## Task Solutions & Code Explanations

### Task 1: Create Tables (`restaurants` & `dishes`) and Insert Sample Data
**Requirement:** Create `restaurants` (`id`, `name`, `city`) and `dishes` (`id`, `restaurant_id`, `dish_name`, `price`). Insert at least 3 restaurants and 2–3 dishes for each restaurant.

```sql
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

-- Insert 4 restaurants (Restaurant 4 has no dishes to test LEFT JOIN)
INSERT INTO restaurants (id, name, city) VALUES
(1, 'Biryani By Kilo', 'Hyderabad'),
(2, 'Haldiram', 'Nagpur'),
(3, 'Pizza Hut', 'Pune'),
(4, 'Cafe Coffee Day', 'Mumbai');

-- Insert dishes (Dish 110 has restaurant_id = 99 to test RIGHT JOIN)
INSERT INTO dishes (id, restaurant_id, dish_name, price) VALUES
-- Biryani By Kilo (restaurant_id = 1)
(101, 1, 'Hyderabadi Chicken Biryani', 350.00),
(102, 1, 'Mutton Dum Biryani', 480.00),
(103, 1, 'Mirchi Ka Salan', 120.00),
-- Haldiram (restaurant_id = 2)
(104, 2, 'Raj Kachori', 140.00),
(105, 2, 'Chole Bhature', 180.00),
(106, 2, 'Gulab Jamun (2 pcs)', 90.00),
-- Pizza Hut (restaurant_id = 3)
(107, 3, 'Margherita Pizza', 299.00),
(108, 3, 'Garlic Breadsticks', 149.00),
(109, 3, 'Farmhouse Veg Pizza', 399.00),
-- Orphaned / unlinked dish
(110, 99, 'Dragon Noodles', 220.00);
```

#### Base Data View:
| id | Restaurant Name | City |
|---|---|---|
| 1 | Biryani By Kilo | Hyderabad |
| 2 | Haldiram | Nagpur |
| 3 | Pizza Hut | Pune |
| 4 | Cafe Coffee Day | Mumbai |

---

### Task 2: INNER JOIN (Dishes with Restaurant Info)
**Requirement:** Write an SQL `INNER JOIN` query to display each dish along with its restaurant name and city, similar to how Zomato shows dish details with restaurant info.

```sql
SELECT 
    d.id AS dish_id,
    d.dish_name,
    d.price,
    r.name AS restaurant_name,
    r.city
FROM dishes d
INNER JOIN restaurants r ON d.restaurant_id = r.id;
```

#### Output:
| dish_id | dish_name | price | restaurant_name | city |
|---|---|---|---|---|
| 101 | Hyderabadi Chicken Biryani | 350.00 | Biryani By Kilo | Hyderabad |
| 102 | Mutton Dum Biryani | 480.00 | Biryani By Kilo | Hyderabad |
| 103 | Mirchi Ka Salan | 120.00 | Biryani By Kilo | Hyderabad |
| 104 | Raj Kachori | 140.00 | Haldiram | Nagpur |
| 105 | Chole Bhature | 180.00 | Haldiram | Nagpur |
| 106 | Gulab Jamun (2 pcs) | 90.00 | Haldiram | Nagpur |
| 107 | Margherita Pizza | 299.00 | Pizza Hut | Pune |
| 108 | Garlic Breadsticks | 149.00 | Pizza Hut | Pune |
| 109 | Farmhouse Veg Pizza | 399.00 | Pizza Hut | Pune |

> **Key Takeaway:** Only rows with keys present in **both** tables are returned (9 rows). Neither the empty restaurant (`Cafe Coffee Day`) nor the orphaned dish (`Dragon Noodles`) is shown.

---

### Task 3: LEFT JOIN (All Restaurants, Even Without Dishes)
**Requirement:** Write an SQL `LEFT JOIN` query to list all restaurants and their dishes, showing restaurants even if they currently have no dishes on the menu (`NULL` for dish columns).

```sql
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    d.id AS dish_id,
    d.dish_name,
    d.price
FROM restaurants r
LEFT JOIN dishes d ON r.id = d.restaurant_id;
```

#### Output:
| restaurant_id | restaurant_name | city | dish_id | dish_name | price |
|---|---|---|---|---|---|
| 1 | Biryani By Kilo | Hyderabad | 101 | Hyderabadi Chicken Biryani | 350.00 |
| 1 | Biryani By Kilo | Hyderabad | 102 | Mutton Dum Biryani | 480.00 |
| 1 | Biryani By Kilo | Hyderabad | 103 | Mirchi Ka Salan | 120.00 |
| 2 | Haldiram | Nagpur | 104 | Raj Kachori | 140.00 |
| 2 | Haldiram | Nagpur | 105 | Chole Bhature | 180.00 |
| 2 | Haldiram | Nagpur | 106 | Gulab Jamun (2 pcs) | 90.00 |
| 3 | Pizza Hut | Pune | 107 | Margherita Pizza | 299.00 |
| 3 | Pizza Hut | Pune | 108 | Garlic Breadsticks | 149.00 |
| 3 | Pizza Hut | Pune | 109 | Farmhouse Veg Pizza | 399.00 |
| **4** | **Cafe Coffee Day** | **Mumbai** | *NULL* | *NULL* | *NULL* |

> **Key Takeaway:** `LEFT JOIN` preserves all rows of the left table (`restaurants`). `Cafe Coffee Day` has 0 dishes, so its dish fields default to `NULL`.

---

### Task 4: RIGHT JOIN (All Dishes, Including Unlinked/Orphaned Dishes)
**Requirement:** Write an SQL `RIGHT JOIN` query to display all dishes and their restaurant names, including any dishes that might not be linked to a restaurant (simulating a data integrity error).

```sql
SELECT 
    r.id AS restaurant_id,
    r.name AS restaurant_name,
    r.city,
    d.id AS dish_id,
    d.dish_name,
    d.price,
    d.restaurant_id AS dish_fk
FROM restaurants r
RIGHT JOIN dishes d ON r.id = d.restaurant_id;
```

#### Output:
| restaurant_id | restaurant_name | city | dish_id | dish_name | price | dish_fk |
|---|---|---|---|---|---|---|
| 1 | Biryani By Kilo | Hyderabad | 101 | Hyderabadi Chicken Biryani | 350.00 | 1 |
| 1 | Biryani By Kilo | Hyderabad | 102 | Mutton Dum Biryani | 480.00 | 1 |
| 1 | Biryani By Kilo | Hyderabad | 103 | Mirchi Ka Salan | 120.00 | 1 |
| 2 | Haldiram | Nagpur | 104 | Raj Kachori | 140.00 | 2 |
| 2 | Haldiram | Nagpur | 105 | Chole Bhature | 180.00 | 2 |
| 2 | Haldiram | Nagpur | 106 | Gulab Jamun (2 pcs) | 90.00 | 2 |
| 3 | Pizza Hut | Pune | 107 | Margherita Pizza | 299.00 | 3 |
| 3 | Pizza Hut | Pune | 108 | Garlic Breadsticks | 149.00 | 3 |
| 3 | Pizza Hut | Pune | 109 | Farmhouse Veg Pizza | 399.00 | 3 |
| *NULL* | *NULL* | *NULL* | **110** | **Dragon Noodles** | **220.00** | **99** |

> **Key Takeaway:** `RIGHT JOIN` ensures all records from the right table (`dishes`) are present. Dish `110` references non-existent `restaurant_id = 99`, so the restaurant columns are padded with `NULL`.

---

### Task 5: Spotify Scenario - Playlists and Songs
**Scenario:** You want to show a list of all playlists and the songs inside them, like Spotify. Explain which JOIN type (`INNER`, `LEFT`, or `RIGHT`) you would use to show all playlists, even if some are empty, and write the SQL query for it.

#### Architectural Explanation
1. **Why `INNER JOIN` is unsuitable:** An `INNER JOIN` only returns rows where keys exist in both tables. When a Spotify user creates a new playlist (e.g., *"Road Trip 2026"*), it begins with 0 songs. An `INNER JOIN` would completely omit this playlist from the user's library view!
2. **Why `LEFT JOIN` is the correct choice:** Putting `playlists` on the **LEFT** (`FROM playlists p LEFT JOIN songs s ON p.playlist_id = s.playlist_id`) guarantees that every playlist appears in the result set. If a playlist contains songs, they are listed; if it is empty, the song columns are `NULL`, allowing the frontend to display *"0 songs / Empty playlist"*.

```sql
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
```

#### Output:
| playlist_id | playlist_name | created_by | song_id | song_title | artist | duration_sec |
|---|---|---|---|---|---|---|
| 1 | Gym Workout Beats | Atharv | 201 | Eye of the Tiger | Survivor | 245 |
| 1 | Gym Workout Beats | Atharv | 202 | Lose Yourself | Eminem | 326 |
| 1 | Gym Workout Beats | Atharv | 203 | Till I Collapse | Eminem | 297 |
| 2 | Acoustic Morning | Sneha | 204 | Banana Pancakes | Jack Johnson | 192 |
| 2 | Acoustic Morning | Sneha | 205 | Here Comes the Sun | The Beatles | 185 |
| 3 | Study Lo-Fi Focus | Rahul | 206 | Sunset Lover | Petit Biscuit | 237 |
| **4** | **Road Trip 2026** | **Atharv** | *NULL* | *NULL* | *NULL* | *NULL* |

---

## Directory Contents
- [`solution.sql`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-09-joins-part-1/solution.sql): Executable SQL queries for Tasks 1 to 5.
- [`setup_and_verify.py`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-09-joins-part-1/setup_and_verify.py): Automated Python script executing and verifying all queries against SQLite.
- [`session_09_joins_part_1.ipynb`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-09-joins-part-1/session_09_joins_part_1.ipynb): Pre-executed Jupyter Notebook with full DataFrame outputs.
- [`zomato_joins.db`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-09-joins-part-1/zomato_joins.db): Embedded SQLite database file.
- [`README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ds-work/assignment-2/session-09-joins-part-1/README.md): Comprehensive documentation.
