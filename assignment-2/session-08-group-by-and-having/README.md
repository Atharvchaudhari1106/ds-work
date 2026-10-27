# Session 8: GROUP BY + HAVING

This folder contains the complete solutions for **Session 8 - GROUP BY + HAVING** from the Data Science & Database coursework track (`assignment-2`).

---

## 📂 Primary Assignment Deliverables

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Interactive Jupyter Notebook** | [**`session_08_group_by_and_having.ipynb`**](session_08_group_by_and_having.ipynb) | Complete self-contained notebook with pre-executed code cells, DataFrame outputs, and execution lifecycle guides |
| **Pure SQL Query File** | [**`solution.sql`**](solution.sql) | Production-ready SQL script compatible with **MySQL**, **PostgreSQL**, and **SQLite** |
| **Zero-Install Python Runner** | [**`setup_and_verify.py`**](setup_and_verify.py) | Automated test script that sets up the database, performs aggregations, and prints formatted summary tables |
| **Sample SQLite Database** | [`orders.db`](orders.db) | Embedded database file generated from the executed pipeline |

---

## 📋 Task-by-Task Solutions

### Task 1: Create `Orders` Table & Insert Sample Orders
> **Problem Statement:** Create a table called `Orders` with columns: `order_id`, `user_id`, `payment_method`, and `amount`. Insert at least 8 sample records representing different users and payment methods (like `UPI`, `Card`, `Wallet`, `COD`).

#### SQL Schema Definition & Data Insertion:
```sql
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);

INSERT INTO Orders (order_id, user_id, payment_method, amount) VALUES
(1, 101, 'Card', 550.00),
(2, 102, 'Card', 450.00),
(3, 101, 'UPI', 320.00),
(4, 103, 'UPI', 280.00),
(5, 104, 'UPI', 420.00),
(6, 102, 'COD', 180.00),
(7, 103, 'COD', 220.00),
(8, 104, 'Wallet', 150.00),
(9, 101, 'Wallet', 250.00);
```

#### Full Table Content:
| order_id | user_id | payment_method | amount |
| :---: | :---: | :--- | :---: |
| **1** | 101 | Card | ₹550.00 |
| **2** | 102 | Card | ₹450.00 |
| **3** | 101 | UPI | ₹320.00 |
| **4** | 103 | UPI | ₹280.00 |
| **5** | 104 | UPI | ₹420.00 |
| **6** | 102 | COD | ₹180.00 |
| **7** | 103 | COD | ₹220.00 |
| **8** | 104 | Wallet | ₹150.00 |
| **9** | 101 | Wallet | ₹250.00 |

---

### Task 2: Count Orders by Payment Method (Zomato Analytics Breakdown)
> **Problem Statement:** Write an SQL query to count how many orders were placed using each `payment_method` in the `Orders` table, similar to how Zomato shows payment breakdown in analytics.

#### SQL Query:
```sql
SELECT 
    payment_method,
    COUNT(order_id) AS order_count
FROM Orders
GROUP BY payment_method;
```

#### Output:
| payment_method | order_count |
| :--- | :---: |
| **UPI** | 3 |
| **Card** | 2 |
| **COD** | 2 |
| **Wallet** | 2 |

---

### Task 3: Total Amount Spent by Each User
> **Problem Statement:** Write an SQL query to find the total amount spent by each `user_id` in the `Orders` table. Display `user_id` and their total spend.

#### SQL Query:
```sql
SELECT 
    user_id,
    SUM(amount) AS total_spend
FROM Orders
GROUP BY user_id
ORDER BY total_spend DESC;
```

#### Output:
| user_id | total_spend |
| :---: | :---: |
| **101** | ₹1,120.00 |
| **102** | ₹630.00 |
| **104** | ₹570.00 |
| **103** | ₹500.00 |

---

### Task 4: Payment Methods with `AVG(amount) > 300` using `HAVING`
> **Problem Statement:** Write an SQL query to show only those payment methods where the average order amount is greater than 300, using `GROUP BY` and `HAVING`.  
> *Hint: Use `AVG(amount)` in your `HAVING` clause.*

#### SQL Query:
```sql
SELECT 
    payment_method,
    ROUND(AVG(amount), 2) AS avg_order_amount
FROM Orders
GROUP BY payment_method
HAVING AVG(amount) > 300;
```

#### Output:
| payment_method | avg_order_amount |
| :--- | :---: |
| **Card** | ₹500.00 |
| **UPI** | ₹340.00 |

*(Note: COD [₹200.00] and Wallet [₹200.00] were correctly excluded by the `HAVING` predicate).*

---

### Task 5: Deep Dive — `WHERE` vs `HAVING` Comparison
> **Problem Statement:** Explain the difference between `WHERE` and `HAVING` by giving one example query for each, using the `Orders` table. Your examples should show a scenario where `WHERE` and `HAVING` filter different things.

#### 1. Core Differences:
| Feature | `WHERE` Clause | `HAVING` Clause |
| :--- | :--- | :--- |
| **What it filters** | Individual **raw rows** (pre-aggregation) | Summarized **groups** (post-aggregation) |
| **Execution Point** | Before `GROUP BY` | After `GROUP BY` |
| **Supports Aggregates?** | ❌ No (`WHERE AVG(amount) > 300` causes error) | ✅ Yes (`HAVING AVG(amount) > 300`) |

#### 2. `WHERE` Example (Row-Level Filter):
```sql
-- Counts high-value individual orders (> 250) per payment method:
SELECT 
    payment_method,
    COUNT(*) AS large_orders_count
FROM Orders
WHERE amount > 250
GROUP BY payment_method;
```
*Output:* Card: 2, UPI: 3 (filters out single transactions $\le$ 250).

#### 3. `HAVING` Example (Group-Level Filter):
```sql
-- Shows payment channels whose COMBINED revenue exceeds 600:
SELECT 
    payment_method,
    SUM(amount) AS total_revenue
FROM Orders
GROUP BY payment_method
HAVING SUM(amount) > 600;
```
*Output:* Card: ₹1,000, UPI: ₹1,020 (filters out COD [₹400] and Wallet [₹400]).

---

## 🚀 How to Run & Verify

1. **Run the Automated Test Runner:**
   ```powershell
   python assignment-2/session-08-group-by-and-having/setup_and_verify.py
   ```

2. **Open the Pre-Executed Interactive Notebook:**
   - Launch Jupyter or view [`session_08_group_by_and_having.ipynb`](session_08_group_by_and_having.ipynb) directly in VS Code / GitHub.
