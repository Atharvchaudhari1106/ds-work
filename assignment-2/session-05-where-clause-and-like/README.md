# Session 5: WHERE Clause + LIKE Operator

This folder contains the complete solutions for **Session 5 - WHERE Clause + LIKE** from the Data Science & Database coursework track (`assignment-2`).

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_05_where_clause_and_like.ipynb`**](session_05_where_clause_and_like.ipynb) | Complete self-contained notebook with pre-executed code cells, DataFrame outputs, and predicate logic explanations |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL**, **PostgreSQL**, and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, runs queries, and prints formatted results |
| **Sample SQLite Database** | [`restaurants.db`](restaurants.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Create `Restaurants` Table & Insert Zomato Sample Data
> **Problem Statement:** Create a table called `Restaurants` with columns: `id`, `name`, `cuisine`, `rating`, and `city`. Insert at least 5 sample records representing real or fictional restaurants you might find on Zomato.

#### SQL Schema Definition & Data Insertion:
```sql
CREATE TABLE Restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    city VARCHAR(100) NOT NULL
);

INSERT INTO Restaurants (id, name, cuisine, rating, city) VALUES
(1, 'Swagat Restaurant', 'South Indian', 4.3, 'Ahmedabad'),
(2, 'Swadisht Dining', 'North Indian', 4.1, 'Surat'),
(3, 'Little Italy', 'Italian', 4.6, 'Ahmedabad'),
(4, 'Mainland China', 'Chinese', 3.8, 'Vadodara'),
(5, 'Sankalp', 'South Indian', 4.2, 'Surat'),
(6, 'Cafe De Bistro', 'Continental', 3.2, 'Ahmedabad');
```

#### Full Table Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |
| **2** | Swadisht Dining | North Indian | 4.1 | Surat |
| **3** | Little Italy | Italian | 4.6 | Ahmedabad |
| **4** | Mainland China | Chinese | 3.8 | Vadodara |
| **5** | Sankalp | South Indian | 4.2 | Surat |
| **6** | Cafe De Bistro | Continental | 3.2 | Ahmedabad |

---

### Task 2: Multi-Condition Filtering (`rating > 4.0` in Ahmedabad or Surat)
> **Problem Statement:** Write a SQL query to find all restaurants in the `Restaurants` table that have a rating greater than 4.0 and are located in either `'Ahmedabad'` or `'Surat'`.

#### SQL Query:
```sql
SELECT * 
FROM Restaurants
WHERE rating > 4.0 
  AND (city = 'Ahmedabad' OR city = 'Surat');
```

#### Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |
| **2** | Swadisht Dining | North Indian | 4.1 | Surat |
| **3** | Little Italy | Italian | 4.6 | Ahmedabad |
| **5** | Sankalp | South Indian | 4.2 | Surat |

---

### Task 3: Pattern Matching with `LIKE 'Swa%'`
> **Problem Statement:** Using the `LIKE` operator, write a query to select all restaurants whose names start with `'Swa'` (for example, `'Swagat'`, `'Swadisht'`) from the `Restaurants` table.  
> *Hint: Use `LIKE 'Swa%'`.*

#### SQL Query:
```sql
SELECT * 
FROM Restaurants
WHERE name LIKE 'Swa%';
```

#### Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |
| **2** | Swadisht Dining | North Indian | 4.1 | Surat |

---

### Task 4: Range Filtering with `BETWEEN ... AND`
> **Problem Statement:** Write a SQL query using the `BETWEEN` keyword to find all restaurants in the `Restaurants` table with a rating between 3.5 and 4.5 (inclusive).

#### SQL Query:
```sql
SELECT * 
FROM Restaurants
WHERE rating BETWEEN 3.5 AND 4.5;
```

#### Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |
| **2** | Swadisht Dining | North Indian | 4.1 | Surat |
| **4** | Mainland China | Chinese | 3.8 | Vadodara |
| **5** | Sankalp | South Indian | 4.2 | Surat |

---

### Task 5: Membership Testing with `IN` Operator
> **Problem Statement:** Write a query to find all restaurants whose cuisine is either `'Chinese'`, `'Italian'`, or `'South Indian'` using the `IN` operator.

#### SQL Query:
```sql
SELECT * 
FROM Restaurants
WHERE cuisine IN ('Chinese', 'Italian', 'South Indian');
```

#### Output:
| id | name | cuisine | rating | city |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Swagat Restaurant | South Indian | 4.3 | Ahmedabad |
| **3** | Little Italy | Italian | 4.6 | Ahmedabad |
| **4** | Mainland China | Chinese | 3.8 | Vadodara |
| **5** | Sankalp | South Indian | 4.2 | Surat |

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Runner:**
   ```powershell
   python assignment-2/session-05-where-clause-and-like/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_05_where_clause_and_like.ipynb`](session_05_where_clause_and_like.ipynb) directly in VS Code / GitHub.
