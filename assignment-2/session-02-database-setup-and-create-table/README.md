# Session 2: Database Setup + CREATE TABLE

This folder contains the complete solutions for **Session 2 - Database Setup + CREATE TABLE** from the Data Science & Database coursework track (`assignment-2`).

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_02_database_setup_and_create_table.ipynb`**](session_02_database_setup_and_create_table.ipynb) | Complete self-contained notebook with pre-executed code cells, formatted DataFrame outputs, and concept explanations |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL** and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, runs queries, and demonstrates error handling |
| **Sample SQLite Database** | [`foodie_app.db`](foodie_app.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1 & 2: Install RDBMS & Create Database (`foodie_app`)
> **Problem Statement 1:** Install MySQL Community Server or SQLite on your system and verify the installation by connecting to the database using the command line or a GUI tool like MySQL Workbench or DB Browser for SQLite.  
> **Problem Statement 2:** Create a new database named `'foodie_app'` to simulate a Zomato-style backend.

#### Setup & Verification:
- **MySQL Community Server:**
  ```sql
  CREATE DATABASE IF NOT EXISTS foodie_app;
  USE foodie_app;
  ```
  Verified via MySQL CLI (`mysql -u root -p`) or GUI (**MySQL Workbench**).

- **SQLite Engine:**
  Created automatically upon connection:
  ```bash
  sqlite3 foodie_app.db
  ```
  Verified via CLI or GUI (**DB Browser for SQLite**).

---

### Task 3: Create `restaurants` Table (Zomato-Style Backend)
> **Problem Statement:** Write a `CREATE TABLE` statement to define a `'restaurants'` table in the `'foodie_app'` database with the following columns: `id` (integer, primary key), `name` (varchar/character, max 100), `cuisine` (varchar/character, max 50), `rating` (decimal, e.g., 4.5), and `location` (varchar/character, max 100).

#### SQL Table Definition:
```sql
CREATE TABLE restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    location VARCHAR(100) NOT NULL
);
```

#### Sample Verification Rows:
```sql
INSERT INTO restaurants (id, name, cuisine, rating, location) VALUES
(1, 'Punjab Grill', 'North Indian', 4.5, 'Connaught Place, New Delhi'),
(2, 'Biryani Blues', 'Hyderabadi', 4.3, 'Indiranagar, Bengaluru'),
(3, 'Bastian', 'Seafood / Continental', 4.7, 'Bandra West, Mumbai');
```

#### Verified Table Output:
| id | name | cuisine | rating | location |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Punjab Grill | North Indian | 4.5 | Connaught Place, New Delhi |
| **2** | Biryani Blues | Hyderabadi | 4.3 | Indiranagar, Bengaluru |
| **3** | Bastian | Seafood / Continental | 4.7 | Bandra West, Mumbai |

---

### Task 4: Design & Create `users` Table (Flipkart-Style App)
> **Problem Statement:** Design and create a `'users'` table for a Flipkart-style app with columns: `user_id` (primary key), `username`, `email`, `phone_number`, and `created_at` (date/time). Pick appropriate data types for each column.  
> *Hint: Think about which columns should be unique and which data types best fit email and phone numbers.*

#### Architectural Data Type Decisions:
1. **`phone_number VARCHAR(15)` vs `INTEGER`:**
   - Phone numbers must be stored as text because:
     - Leading zeroes (e.g., `011...`) would be dropped by numeric types.
     - Country codes and formatting characters (e.g., `+91`) require string representation.
     - Phone numbers are identifiers, not quantitative values; they never undergo mathematical operations.
2. **`email VARCHAR(100) UNIQUE NOT NULL`:**
   - Guarantees each account has a unique login identifier across the platform.
3. **`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`:**
   - Automatically tracks the registration moment in standard UTC format.

#### SQL Table Definition:
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Verified Table Output:
| user_id | username | email | phone_number | created_at |
| :---: | :--- | :--- | :--- | :--- |
| **101** | atharv_c | atharv@example.com | +919876543210 | 2026-10-27 07:17:22 |
| **102** | priya_sharma | priya.s@example.com | +919812345678 | 2026-10-27 07:17:22 |
| **103** | rahul_verma | rahul.v@example.com | +919898765432 | 2026-10-27 07:17:22 |

---

### Task 5: Intentional Syntax Mistake & Error Diagnostics
> **Problem Statement:** Intentionally make a mistake in your `CREATE TABLE` statement (such as missing a comma or using an unsupported data type), run it, and then fix the error based on the message you receive.  
> *Hint: Take a screenshot of the error and the corrected SQL statement for your records.*

#### 1. Deliberate Mistake (Missing Comma):
```sql
CREATE TABLE invalid_demo_table (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)       -- <-- MISSING COMMA HERE!
    phone VARCHAR(15)
);
```

#### 2. Exact Error Message Received:
- **SQLite Engine:**
  ```text
  OperationalError: near "phone": syntax error
  ```
- **MySQL Engine:**
  ```text
  ERROR 1064 (42000): You have an error in your SQL syntax near 'phone VARCHAR(15))' at line 5
  ```

#### 3. Error Diagnosis:
The SQL parser parses the `email VARCHAR(100)` column definition and expects a delimiter comma `,` before encountering the next column name `phone`. Because the comma was omitted, the parser attempts to read `phone` as part of the `email` definition, resulting in an immediate syntax error.

#### 4. The Corrected SQL Statement:
```sql
CREATE TABLE fixed_demo_table (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),      -- <-- ADDED MISSING COMMA
    phone VARCHAR(15)
);
```
*(Status: Successfully executed without errors).*

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Runner:**
   ```powershell
   python assignment-2/session-02-database-setup-and-create-table/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_02_database_setup_and_create_table.ipynb`](session_02_database_setup_and_create_table.ipynb) directly in VS Code / GitHub.
