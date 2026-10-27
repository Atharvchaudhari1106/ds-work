# Assignment Track 2: Working with Databases & SQL Basics

This directory contains coursework submissions, exercises, and assignments for **Assignment 2: Database Management & SQL**.

All sessions follow an **`.ipynb`-first** interactive format with pre-rendered results, paired with standalone `.sql` scripts and zero-dependency Python verification runners.

---

## 📂 Sessions Index

| Session | Topic | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Session 1** | [Database Intro & SQL Basics](session-01-database-intro-and-sql-basics/README.md) | [`session_01_database_intro_sql_basics.ipynb`](session-01-database-intro-and-sql-basics/session_01_database_intro_sql_basics.ipynb) <br> [`solution.sql`](session-01-database-intro-and-sql-basics/solution.sql) | ✅ Completed (Executed) |
| **Session 4** | [SELECT Statement Basics](session-04-select-statement-basics/README.md) | [`session_04_select_statement_basics.ipynb`](session-04-select-statement-basics/session_04_select_statement_basics.ipynb) <br> [`solution.sql`](session-04-select-statement-basics/solution.sql) | ✅ Completed (Executed) |

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
└── session-04-select-statement-basics/        # Session 4: SELECT Statement Basics
    ├── session_04_select_statement_basics.ipynb # Interactive executed notebook (Tasks 1-5)
    ├── solution.sql                           # Production SQL script (LIMIT, DISTINCT, Aliases)
    ├── setup_and_verify.py                    # Automated test runner
    ├── music_and_food.db                      # Pre-built SQLite database
    └── README.md                              # Complete task walkthrough & query debugging guide
```

---

## 🚀 How to Run & Verify

Each session includes an automated Python verification script that runs locally without requiring a running database server:

```powershell
# Verify Session 1
python assignment-2/session-01-database-intro-and-sql-basics/setup_and_verify.py

# Verify Session 4
python assignment-2/session-04-select-statement-basics/setup_and_verify.py
```
