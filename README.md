# Data Science Work Repository (`ds-work`)

Welcome to your central Data Science repository! This workspace is configured for your Data Science coursework, practical sessions, assignments, and machine learning projects.

---

## 📁 Repository Structure

```text
ds-work/
├── .gitignore                                 # Ignores .venv, cache, and OS files
├── requirements.txt                           # Python project dependencies (pandas, numpy, scipy, matplotlib)
├── README.md                                  # Repository overview and setup guide
│
├── Intro to ds/                               # Intro to Data Science Foundation Track
│   ├── session_01_what_is_data_science.ipynb  # Session 1: What is Data Science? (All 4 tasks executed)
│   ├── session_02_data_science_lifecycle.ipynb# Session 2: Data Science Lifecycle (All 5 tasks executed)
│   ├── README.md                              # Complete course track documentation
│   └── data/                                  # Datasets (spotify_mini.csv, bookmyshow_movies.csv)
│
├── assignments/                               # Dedicated assignments directory
│   ├── README.md                              # Assignments index and submission guide
│   │
│   ├── git-branching-collaboration/           # Git Branching & Collaboration Module
│   │   ├── git_branching_collaboration.ipynb  # Execution & verification notebook
│   │   └── README.md                          # Full solutions documentation & merge logs
│   │
│   ├── publishing-projects-ds-portfolio/      # Publishing Projects & Building Your DS Portfolio
│   │   ├── publishing_projects_ds_portfolio.ipynb # Comprehensive execution & verification notebook
│   │   └── README.md                          # Full solutions documentation & GitHub links
│   │
│   ├── professional-project-structure/        # Professional Project Structure for DA/DS
│   │   ├── professional_project_structure.ipynb # Execution & verification notebook
│   │   └── README.md                          # Full solutions documentation & audit
│   │
│   ├── git-installation-fundamentals/         # Git Installation + Fundamentals Module
│   │   ├── git_installation_fundamentals.ipynb# Execution & verification notebook
│   │   └── README.md                          # Full solutions documentation & CLI logs
│   │
│   ├── git-github/                            # Git & GitHub Module
│   │   ├── git_github_assignment.ipynb        # Terminal execution & verification notebook
│   │   └── README.md                          # Full solutions documentation & GitHub links
│   │
│   ├── session-02-data-science-lifecycle/     # Session 2: Data Science Lifecycle
│   │   ├── session_02_data_science_lifecycle.ipynb # Primary interactive notebook (All 5 tasks solved & executed)
│   │   ├── README.md                          # Full solutions documentation
│   │   └── data/                              # Supporting datasets
│   │
│   ├── session-01-intro-to-statistics/        # Session 1: Introduction to Statistics in Data Science
│   │   ├── session_01_intro_to_statistics.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 1 task descriptions & answers
│   │
│   ├── session-02-mean-median-mode/           # Session 2: Mean, Median & Mode
│   │   ├── session_02_mean_median_mode.ipynb  # Primary interactive notebook (All 5 tasks solved & executed)
│   │   ├── playlist_stats.py                  # Task 1 Python script (explicitly requested)
│   │   ├── README.md                          # Session 2 task descriptions & answers
│   │   └── data/
│   │       └── ipl_player_runs.csv            # Real-world dataset for Task 5
│   │
│   ├── session-03-variance-and-standard-deviation/ # Session 3: Variance & Standard Deviation
│   │   ├── session_03_variance_and_standard_deviation.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 3 task descriptions & answers
│   │
│   ├── session-04-skewness-basic/             # Session 4: Skewness (Basic)
│   │   ├── session_04_skewness_basic.ipynb    # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 4 task descriptions & answers
│   │
│   ├── session-05-sampling/                   # Session 5: Sampling
│   │   ├── session_05_sampling.ipynb          # Primary interactive notebook (All 5 tasks solved & executed)
│   │   └── README.md                          # Session 5 task descriptions & answers
│   │
│   ├── session-06-hypothesis-testing-basic/   # Session 6: Hypothesis Testing (Basic)
│   │   ├── session_06_hypothesis_testing_basic.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 6 task descriptions & answers
│   │
│   ├── session-07-correlation/                # Session 7: Correlation
│   │   ├── session_07_correlation.ipynb       # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 7 task descriptions & answers
│   │
│   ├── session-08-probability-basics/         # Session 8: Probability Basics
│   │   ├── session_08_probability_basics.ipynb # Primary interactive notebook (All 5 tasks solved & executed)
│   │   └── README.md                          # Session 8 task descriptions & answers
│   │
│   ├── session-09-normal-distribution/        # Session 9: Normal Distribution
│   │   ├── session_09_normal_distribution.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 9 task descriptions & answers
│   │
│   ├── session-10-bayes-theorem-basic/        # Session 10: Bayes' Theorem (Basic)
│   │   ├── session_10_bayes_theorem_basic.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 10 task descriptions & answers
│   │
│   ├── session-11-vectors-and-matrices-basic/ # Session 11: Vectors & Matrices (Basic)
│   │   ├── session_11_vectors_and_matrices_basic.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 11 task descriptions & answers
│   └── session-12-matrix-multiplication-linear-regression/ # Session 12: Matrix Multiplication & Linear Regression
│       ├── session_12_matrix_multiplication_linear_regression.ipynb # Primary interactive notebook (All 5 tasks solved & executed)
│       └── README.md                          # Session 12 task descriptions & answers
│
├── assignment-2/                              # Dedicated SQL & Database Coursework Track
│   ├── README.md                              # Track 2 overview and session index
│   ├── session-01-database-intro-and-sql-basics/ # Session 1: Database Introduction & SQL Basics
│   │   ├── session_01_database_intro_sql_basics.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (MySQL & PostgreSQL compatible)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & AI answers
│   │
│   ├── session-02-database-setup-and-create-table/ # Session 2: Database Setup + CREATE TABLE
│   │   ├── session_02_database_setup_and_create_table.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (restaurants & users schemas)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & error guide
│   │
│   ├── session-03-insert-update-and-delete/   # Session 3: INSERT, UPDATE & DELETE
│   │   ├── session_03_insert_update_and_delete.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (DML operations & string concats)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & safety guide
│   │
│   ├── session-04-select-statement-basics/    # Session 4: SELECT Statement Basics
│   │   ├── session_04_select_statement_basics.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (LIMIT, DISTINCT, Aliases)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & debugging guide
│   │
│   ├── session-05-where-clause-and-like/      # Session 5: WHERE Clause + LIKE Operator
│   │   ├── session_05_where_clause_and_like.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (LIKE, BETWEEN, IN)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & operator guide
│   │
│   ├── session-06-order-by-and-sorting/       # Session 6: ORDER BY + Sorting
│   │   ├── session_06_order_by_and_sorting.ipynb # Executed interactive notebook
│   │   ├── solution.sql                       # Complete SQL script (ASC, DESC, Multi-Column)
│   │   ├── setup_and_verify.py                # Automated test & verification script
│   │   └── README.md                          # Comprehensive session walkthrough & sorting guide
│   │
│   └── session-08-group-by-and-having/        # Session 8: GROUP BY + HAVING
│       ├── session_08_group_by_and_having.ipynb # Executed interactive notebook
│       ├── solution.sql                       # Complete SQL script (GROUP BY, HAVING, Aggregations)
│       ├── setup_and_verify.py                # Automated test & verification script
│       └── README.md                          # Comprehensive session walkthrough & aggregation guide
│
├── notebooks/                                 # General exploratory data analysis (EDA)
├── data/                                      # Shared raw and processed datasets
│
├── sql-assessment/                            # TOPS Technologies Data Science Assessment M4-A1 (Modules 3-4)
├── food-delivery-pipeline/                    # Food Delivery Demand Pipeline Assessment M2-A1
├── my-movie-ratings/                          # Movie Ratings Analysis & Data Science Portfolio Project
├── foodie-favorites/                          # Foodie Favorites & Music Recommendation Project
├── python-module-6/                           # Advanced Python Programming, REST APIs & Case Studies
├── music-app/                                 # Fullstack Music Player & Interactive Web Application
└── Zomato-Cleaning-and-Visualization/         # Zomato Restaurant Dataset Cleaning & Spatial EDA
```

---

## 🚀 Projects & Module Portfolios

| Folder | Topic / Focus | Core Technologies |
| :--- | :--- | :--- |
| [`assignments/`](./assignments/) | Assignment Track 1: Statistics & Git Coursework | Jupyter, SciPy, NumPy, Matplotlib, Git |
| [`assignment-2/`](./assignment-2/) | Assignment Track 2: Working with Databases & SQL | SQL (MySQL, PostgreSQL, SQLite), Pandas |
| [`sql-assessment/`](./sql-assessment/) | TOPS Technologies Data Science M4-A1 Assessment | SQLite, Pandas, NumPy, Matplotlib, Seaborn |
| [`food-delivery-pipeline/`](./food-delivery-pipeline/) | Food Delivery Demand & Pipeline M2-A1 Assessment | Python, Git Flow, OOP, Functional Tools |
| [`my-movie-ratings/`](./my-movie-ratings/) | Movie Ratings Analysis & Portfolio Page | Jupyter Notebook, Pandas, Data Viz, Git LFS |
| [`foodie-favorites/`](./foodie-favorites/) | Foodie Favorites & Curated Playlists | Markdown, Data Aggregation |
| [`python-module-6/`](./python-module-6/) | Core & Advanced Python, REST APIs, Crypto Tracker | Python 3, `requests`, `requests.Session()` |
| [`music-app/`](./music-app/) | Interactive Music Application & Server | Node.js, Vite, JavaScript, HTML5/CSS3 |
| [`Zomato-Cleaning-and-Visualization/`](./Zomato-Cleaning-and-Visualization/) | Zomato Dataset Cleaning & Spatial Mapping | Pandas, Seaborn, Folium / Geopandas |


---

## 🛠️ Environment Setup

A dedicated Python virtual environment `.venv` is configured with `pandas`, `numpy`, `scipy`, and `matplotlib`.

### Activate the environment:
**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (cmd):**
```cmd
.venv\Scripts\activate.bat
```

To install any future libraries:
```powershell
.venv\Scripts\pip install <package_name>
.venv\Scripts\pip freeze > requirements.txt
```

---

## 📤 Pushing Changes to GitHub

```powershell
git add .
git commit -m "feat: complete Sessions 1 through 9 executed notebooks"
git push origin main
```
