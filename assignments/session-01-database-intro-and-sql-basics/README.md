# Session 1: Database Introduction & SQL Basics

This folder contains the complete solutions for **Session 1 - Database Introduction & SQL Basics** from the Data Science & Database coursework track.

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_01_database_intro_sql_basics.ipynb`**](session_01_database_intro_sql_basics.ipynb) | Complete self-contained notebook with pre-executed code cells, formatted DataFrame outputs, and full concept guides |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with both **MySQL** and **PostgreSQL** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, runs queries, and prints formatted results |
| **Sample SQLite Database** | [`music_streaming_app.db`](music_streaming_app.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Install MySQL/PostgreSQL & Create Database
> **Problem Statement:** Install MySQL or PostgreSQL on your system and create a new database named `'music_streaming_app'` using the command line or GUI tool of your choice.

#### Option A: MySQL
- **Command Line (CLI):**
  ```bash
  mysql -u root -p
  CREATE DATABASE music_streaming_app;
  USE music_streaming_app;
  ```
- **GUI (MySQL Workbench):**
  1. Open MySQL Workbench and connect to your local instance.
  2. In the query tab, run `CREATE DATABASE music_streaming_app;`.
  3. Refresh the **Schemas** sidebar to view the new database.

#### Option B: PostgreSQL
- **Command Line (CLI):**
  ```bash
  psql -U postgres
  CREATE DATABASE music_streaming_app;
  \c music_streaming_app;
  ```
- **GUI (pgAdmin 4):**
  1. Expand **Servers** > **Databases**.
  2. Right-click **Databases** > **Create** > **Database...**.
  3. Enter Name: `music_streaming_app` and click **Save**.

---

### Task 2: Create Table `playlists`
> **Problem Statement:** Inside the `'music_streaming_app'` database, create a table called `'playlists'` with columns: `playlist_id` (integer, primary key), `name` (varchar), and `created_by` (varchar).

#### SQL Definition:
```sql
CREATE TABLE playlists (
    playlist_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_by VARCHAR(100) NOT NULL
);
```

#### Column Details:
| Column Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `playlist_id` | `INT` / `INTEGER` | `PRIMARY KEY` | Unique identifier for each playlist |
| `name` | `VARCHAR(255)` | `NOT NULL` | The title/name of the playlist |
| `created_by` | `VARCHAR(100)` | `NOT NULL` | The username or name of the playlist curator |

---

### Task 3: Insert Sample Rows
> **Problem Statement:** Insert three sample rows into the `'playlists'` table representing playlists like `'Bollywood Hits'`, `'Chill Vibes'`, and `'Workout Mix'`, each created by a different user.

#### SQL Statement:
```sql
INSERT INTO playlists (playlist_id, name, created_by) VALUES
(1, 'Bollywood Hits', 'Amit'),
(2, 'Chill Vibes', 'Pooja'),
(3, 'Workout Mix', 'Rahul');
```

#### Verified Table State:
| playlist_id | name | created_by |
| :---: | :--- | :--- |
| **1** | Bollywood Hits | Amit |
| **2** | Chill Vibes | Pooja |
| **3** | Workout Mix | Rahul |

---

### Task 4: Filter Query (`WHERE created_by = 'Amit'`)
> **Problem Statement:** Write an SQL `SELECT` query to display all playlists created by the user `'Amit'` from the `'playlists'` table.  
> *Hint: Use the `WHERE` clause to filter by the `'created_by'` column.*

#### SQL Query:
```sql
SELECT playlist_id, name, created_by
FROM playlists
WHERE created_by = 'Amit';
```

#### Query Result:
| playlist_id | name | created_by |
| :---: | :--- | :--- |
| **1** | Bollywood Hits | Amit |

---

### Task 5: AI Explanation — Table vs. Row vs. Column (Zomato Example)
> **Problem Statement:** Open ChatGPT or Copilot and ask it to explain the difference between a table, a row, and a column in SQL using an example from a food delivery app like Zomato. Paste the explanation you receive into your assignment.

#### 🤖 AI-Generated Explanation:

In relational databases (SQL), data is organized in a 2-dimensional grid of rows and columns. To clearly visualize the difference between a **Table**, a **Row**, and a **Column**, let's take the real-world example of **Zomato**, India's popular food delivery app.

Imagine how Zomato tracks every meal delivery across millions of customers:

```text
+-----------------------------------------------------------------------------------------+
|                                    TABLE: Orders                                        |
+----------+------------------+---------------------+-------------------+-----------------+
| order_id | customer_name    | restaurant_name     | total_amount (Rs) | order_status    |
+----------+------------------+---------------------+-------------------+-----------------+
| 101      | Rohan Sharma     | Biryani Blues       | 450.00            | Delivered       |
| 102      | Priya Patel      | Domino's Pizza      | 620.00            | Out for Delivery|
| 103      | Amit Verma       | Punjab Grill        | 890.00            | Preparing       |
+----------+------------------+---------------------+-------------------+-----------------+
```

#### 1. Table (`Orders`)
* **Definition:** A structured collection of related data stored together in rows and columns that represents a distinct entity or concept.
* **Zomato Analogy:** The **entire "Orders" master ledger**. Just as Zomato maintains separate tables for `Users`, `Restaurants`, `Menu_Items`, and `Riders`, the `Orders` table holds every meal order ever placed on the platform.

#### 2. Column (Attribute / Field)
* **Definition:** A vertical element that defines a specific property, category, or characteristic that every entry will have. It dictates the data type (e.g., Integer, Text, Currency, Timestamp).
* **Zomato Analogy:** An **individual attribute or specification** of an order:
  * `order_id` (Unique integer ID)
  * `customer_name` (Text)
  * `restaurant_name` (Text - where the food is coming from)
  * `total_amount` (Decimal - price paid)
  * `order_status` (Categorical - `'Preparing'`, `'Out for Delivery'`, `'Delivered'`)

#### 3. Row (Record / Tuple)
* **Definition:** A single horizontal entry that contains all the column values for one specific, individual instance of the entity.
* **Zomato Analogy:** **One customer's specific meal order**.
  * Looking at Row 1: `(101, 'Rohan Sharma', 'Biryani Blues', 450.00, 'Delivered')`
  * This row gives you the complete picture of Rohan's single transaction—linking his identity, restaurant choice, amount charged, and current status into one coherent data point.

#### Summary Comparison:
| Concept | Database Term | Zomato Analogy | Real Example |
| :--- | :--- | :--- | :--- |
| **Table** | Relation / Entity | The entire order logbook | `Orders` table |
| **Column** | Attribute / Field | A specific feature of any order | `restaurant_name` (`VARCHAR`), `total_amount` (`DECIMAL`) |
| **Row** | Tuple / Record | One customer's specific order | `(101, 'Rohan Sharma', 'Biryani Blues', 450.00, 'Delivered')` |

---

## 🚀 How to Run & Verify

1. **Run the Automated Python Verification Script:**
   ```powershell
   python assignments/session-01-database-intro-and-sql-basics/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch your Jupyter Notebook interface or open [`session_01_database_intro_sql_basics.ipynb`](session_01_database_intro_sql_basics.ipynb) directly in VS Code / GitHub.
