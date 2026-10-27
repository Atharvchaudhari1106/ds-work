# Assignment Track 2: Working with Databases & SQL Basics

This directory contains coursework submissions, exercises, and assignments for **Assignment 2: Database Management & SQL**.

All sessions follow an **`.ipynb`-first** interactive format with pre-rendered results, paired with standalone `.sql` scripts and zero-dependency Python verification runners.

---

## 📂 Sessions Index

| Session | Topic | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Session 1** | [Database Intro & SQL Basics](session-01-database-intro-and-sql-basics/README.md) | [`session_01_database_intro_sql_basics.ipynb`](session-01-database-intro-and-sql-basics/session_01_database_intro_sql_basics.ipynb) <br> [`solution.sql`](session-01-database-intro-and-sql-basics/solution.sql) | ✅ Completed (Executed) |
| **Session 2** | [Database Setup + CREATE TABLE](session-02-database-setup-and-create-table/README.md) | [`session_02_database_setup_and_create_table.ipynb`](session-02-database-setup-and-create-table/session_02_database_setup_and_create_table.ipynb) <br> [`solution.sql`](session-02-database-setup-and-create-table/solution.sql) | ✅ Completed (Executed) |
| **Session 3** | [INSERT, UPDATE & DELETE](session-03-insert-update-and-delete/README.md) | [`session_03_insert_update_and_delete.ipynb`](session-03-insert-update-and-delete/session_03_insert_update_and_delete.ipynb) <br> [`solution.sql`](session-03-insert-update-and-delete/solution.sql) | ✅ Completed (Executed) |
| **Session 4** | [SELECT Statement Basics](session-04-select-statement-basics/README.md) | [`session_04_select_statement_basics.ipynb`](session-04-select-statement-basics/session_04_select_statement_basics.ipynb) <br> [`solution.sql`](session-04-select-statement-basics/solution.sql) | ✅ Completed (Executed) |
| **Session 5** | [WHERE Clause + LIKE](session-05-where-clause-and-like/README.md) | [`session_05_where_clause_and_like.ipynb`](session-05-where-clause-and-like/session_05_where_clause_and_like.ipynb) <br> [`solution.sql`](session-05-where-clause-and-like/solution.sql) | ✅ Completed (Executed) |
| **Session 6** | [ORDER BY + Sorting](session-06-order-by-and-sorting/README.md) | [`session_06_order_by_and_sorting.ipynb`](session-06-order-by-and-sorting/session_06_order_by_and_sorting.ipynb) <br> [`solution.sql`](session-06-order-by-and-sorting/solution.sql) | ✅ Completed (Executed) |
| **Session 8** | [GROUP BY + HAVING](session-08-group-by-and-having/README.md) | [`session_08_group_by_and_having.ipynb`](session-08-group-by-and-having/session_08_group_by_and_having.ipynb) <br> [`solution.sql`](session-08-group-by-and-having/solution.sql) | ✅ Completed (Executed) |

---

## 🛠️ Module Structure

```text
assignment-2/
├── README.md                                  # This directory index
│
├── session-01-database-intro-and-sql-basics/  # Session 1: Database Introduction & SQL Basics
│   ├── session_01_database_intro_sql_basics.ipynb # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (MySQL & PostgreSQL compatible)
│   ├── setup_and_verify.py                    # Automated test runner (SQLite engine)
│   ├── music_streaming_app.db                 # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & Zomato AI explanation
│
├── session-02-database-setup-and-create-table/# Session 2: Database Setup + CREATE TABLE
│   ├── session_02_database_setup_and_create_table.ipynb # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (restaurants & users tables)
│   ├── setup_and_verify.py                    # Automated test runner & error diagnostic demo
│   ├── foodie_app.db                          # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & schema guide
│
├── session-03-insert-update-and-delete/       # Session 3: INSERT, UPDATE & DELETE
│   ├── session_03_insert_update_and_delete.ipynb # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (DML operations & string concats)
│   ├── setup_and_verify.py                    # Automated test runner
│   ├── playlist_app.db                        # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & safety practices
│
├── session-04-select-statement-basics/        # Session 4: SELECT Statement Basics
│   ├── session_04_select_statement_basics.ipynb # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (LIMIT, DISTINCT, Aliases)
│   ├── setup_and_verify.py                    # Automated test runner
│   ├── music_and_food.db                      # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & query debugging guide
│
├── session-05-where-clause-and-like/          # Session 5: WHERE Clause + LIKE Operator
│   ├── session_05_where_clause_and_like.ipynb # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (LIKE, BETWEEN, IN)
│   ├── setup_and_verify.py                    # Automated test runner
│   ├── restaurants.db                         # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & operator guide
│
├── session-06-order-by-and-sorting/           # Session 6: ORDER BY + Sorting
│   ├── session_06_order_by_and_sorting.ipynb  # Interactive executed notebook (Tasks 1-5)
│   ├── solution.sql                           # Production SQL script (ASC, DESC, Multi-Column)
│   ├── setup_and_verify.py                    # Automated test runner
│   ├── sorting_app.db                         # Pre-built SQLite database
│   └── README.md                              # Complete task walkthrough & sorting guide
│
└── session-08-group-by-and-having/            # Session 8: GROUP BY + HAVING
    ├── session_08_group_by_and_having.ipynb   # Interactive executed notebook (Tasks 1-5)
    ├── solution.sql                           # Production SQL script (GROUP BY, HAVING, WHERE vs HAVING)
    ├── setup_and_verify.py                    # Automated test runner
    ├── orders.db                              # Pre-built SQLite database
    └── README.md                              # Complete task walkthrough & aggregation guide
```

---

## 🚀 How to Run & Verify

Each session includes an automated Python verification script that runs locally without requiring a running database server:

```powershell
# Verify Session 1
python assignment-2/session-01-database-intro-and-sql-basics/setup_and_verify.py

# Verify Session 2
python assignment-2/session-02-database-setup-and-create-table/setup_and_verify.py

# Verify Session 3
python assignment-2/session-03-insert-update-and-delete/setup_and_verify.py

# Verify Session 4
python assignment-2/session-04-select-statement-basics/setup_and_verify.py

# Verify Session 5
python assignment-2/session-05-where-clause-and-like/setup_and_verify.py

# Verify Session 6
python assignment-2/session-06-order-by-and-sorting/setup_and_verify.py

# Verify Session 8
python assignment-2/session-08-group-by-and-having/setup_and_verify.py
```
