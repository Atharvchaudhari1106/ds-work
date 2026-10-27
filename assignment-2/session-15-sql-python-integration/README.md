# Session 15: SQL + Python Integration

**Course:** Working with Databases & SQL Basics  
**Directory:** `assignment-2/session-15-sql-python-integration/`  
**Database File:** `foodie.db`  
**Output CSV:** `top_rated_restaurants.csv`  
**Execution Environment:** Python 3.12, SQLite 3.49, Pandas 3.1  
**Status:** ✅ Completed, Verified & Executed

---

## 📌 Executive Summary
In end-to-end data science pipelines, SQL and Python form the core dual-engine architecture:
- **SQL / Relational DBMS**: Excels at querying, aggregation, filtering, join optimization, and relational persistence.
- **Python / Pandas**: Excels at vectorized transformations, statistical modeling, machine learning, and automated programmatic scheduling.

This session demonstrates full integration between Python's standard library `sqlite3` and the `pandas` data analysis library, establishing reproducible database creation, record insertion, querying, DataFrame loading, feature engineering via `.apply()`, and daily automation export to CSV.

---

## 📂 Deliverables & File Structure

```text
assignment-2/session-15-sql-python-integration/
├── session_15_sql_python_integration.ipynb  # Primary executed interactive notebook (Tasks 1-5)
├── solution.sql                            # Production SQL script (DDL, DML, and diagnostic queries)
├── daily_summary.py                        # Automated standalone pipeline script for Task 5
├── setup_and_verify.py                     # Automated end-to-end test runner
├── foodie.db                               # Populated SQLite database file
├── top_rated_restaurants.csv               # Automated CSV export of top-rated restaurants
└── README.md                               # Complete documentation & task walkthrough
```

---

## 🛠️ Tasks & Comprehensive Solutions

### Task 1: Installing `sqlite3` & Creating `foodie.db`
> **Task 1:** Install the `sqlite3` module in Python and write a script to create a new database called `foodie.db` with a table `Restaurants (id, name, cuisine, rating)`.

#### 💡 Note on `sqlite3` Installation:
The `sqlite3` module is part of Python's **Standard Library** (compliant with PEP 249 Python Database API Specification v2.0). It is bundled into all standard Python distributions. **No external `pip install sqlite3` is needed.** Attempting `pip install sqlite3` will either fail or install an unneeded dummy package.

#### Python Implementation:
```python
import sqlite3

# Connect to database (creates file if not present)
conn = sqlite3.connect("foodie.db")
cursor = conn.cursor()

# Idempotent table creation
cursor.execute("DROP TABLE IF EXISTS Restaurants;")
cursor.execute("""
CREATE TABLE Restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cuisine TEXT NOT NULL,
    rating REAL NOT NULL
);
""")
conn.commit()
print("[OK] Database 'foodie.db' and table 'Restaurants' successfully initialized.")
```

---

### Task 2: Inserting Sample Restaurants & Fetching Rating > 4.0
> **Task 2:** Using `sqlite3` in Python, insert three sample restaurants into the `Restaurants` table in `foodie.db` and write a query to fetch all restaurants with a rating above 4.0, then print their names.

#### Python Implementation:
```python
# Sample restaurants dataset
sample_restaurants = [
    (1, "Little Italy", "Italian", 4.8),
    (2, "Punjab Grill", "North Indian", 4.6),
    (3, "Chai Point", "Cafe", 3.9)
]

# Parameterized batch insert
cursor.executemany(
    "INSERT INTO Restaurants (id, name, cuisine, rating) VALUES (?, ?, ?, ?);",
    sample_restaurants
)
conn.commit()

# Query restaurants with rating > 4.0
cursor.execute("SELECT name FROM Restaurants WHERE rating > 4.0;")
high_rated = cursor.fetchall()

print("Restaurants with rating above 4.0:")
for (name,) in high_rated:
    print(f"  - {name}")
```

#### Terminal Output:
```text
Restaurants with rating above 4.0:
  - Little Italy
  - Punjab Grill
```
*(Notice: 'Chai Point' with rating 3.9 is correctly excluded).*

---

### Task 3: Loading Data into Pandas DataFrame & Displaying `head(2)`
> **Task 3:** Write Python code to load all rows from the `Restaurants` table in `foodie.db` into a Pandas DataFrame and display the top 2 rows using `DataFrame.head()`.

#### Python Implementation:
```python
import pandas as pd

# Direct database query to Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM Restaurants;", conn)

# Display top 2 rows
print(df.head(2))
```

#### Tabular Output (`df.head(2)`):
| id | name | cuisine | rating |
| :---: | :--- | :--- | :---: |
| **1** | Little Italy | Italian | 4.8 |
| **2** | Punjab Grill | North Indian | 4.6 |

---

### Task 4: Adding `delivery_charge` & Computing Conditional `final_rating`
> **Task 4:** Add a new column `delivery_charge` to your DataFrame, setting it to 50 for all restaurants, and then calculate a new column `final_rating` as `rating + (0.1 if cuisine is 'Italian')`.  
> *Hint: Use `DataFrame.apply()` or a lambda function for the conditional logic.*

#### Mathematical Logic:
$$\text{final\_rating} = \text{rating} + \begin{cases} 0.1 & \text{if cuisine} = \text{'Italian'} \\ 0.0 & \text{otherwise} \end{cases}$$

#### Python Implementation:
```python
# 1. Add scalar column delivery_charge
df["delivery_charge"] = 50

# 2. Conditional calculation using DataFrame.apply() with lambda
df["final_rating"] = df.apply(
    lambda row: round(row["rating"] + (0.1 if row["cuisine"] == "Italian" else 0.0), 2),
    axis=1
)

print(df)
```

#### Transformed DataFrame:
| id | name | cuisine | rating | delivery_charge | final_rating | Bonus Applied? |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Little Italy | Italian | 4.8 | 50 | **4.9** | ✅ Yes (+0.1 Italian Bonus) |
| **2** | Punjab Grill | North Indian | 4.6 | 50 | **4.6** | ❌ No (+0.0) |
| **3** | Chai Point | Cafe | 3.9 | 50 | **3.9** | ❌ No (+0.0) |

---

### Task 5: Daily Summary Automation (Rating > 4.5 $\rightarrow$ CSV)
> **Task 5:** Automate a daily summary: Write a Python script that connects to `foodie.db`, fetches all restaurants with rating above 4.5, loads them into a DataFrame, and saves the result as a CSV file named `top_rated_restaurants.csv`.

#### Python Implementation (`daily_summary.py`):
```python
import sqlite3
import pandas as pd

def generate_daily_summary(db_path="foodie.db", output_csv="top_rated_restaurants.csv"):
    with sqlite3.connect(db_path) as conn:
        query = """
        SELECT id, name, cuisine, rating
        FROM Restaurants
        WHERE rating > 4.5
        ORDER BY rating DESC;
        """
        df_top = pd.read_sql_query(query, conn)
    
    df_top.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Exported {len(df_top)} records to {output_csv}")
    return df_top

if __name__ == "__main__":
    generate_daily_summary()
```

#### Exported CSV File (`top_rated_restaurants.csv`):
```csv
id,name,cuisine,rating
1,Little Italy,Italian,4.8
2,Punjab Grill,North Indian,4.6
```

---

## 🚀 How to Run & Verify

Run the automated verification suite from the repository root:

```powershell
python assignment-2/session-15-sql-python-integration/setup_and_verify.py
```

Run the standalone daily automation script:
```powershell
python assignment-2/session-15-sql-python-integration/daily_summary.py
```
