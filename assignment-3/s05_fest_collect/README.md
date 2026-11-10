# Session 5: Data Collection using Pandas (Part 2)

**Course Track:** Assignment Track 3: Data Science Foundations  
**Module:** Advanced Data Ingestion, Relational SQL, Web Sources & Multi-Table Joins  
**Case Study:** Annual College Cultural & Tech Festival (*Vivanta Fest 2025*) Operations Engine  
**Author:** Atharv Chaudhari (`ds-work`)

---

## 📋 Session Overview

This session completes the Data Collection module in **Pandas**, expanding from flat file ingestion into **relational databases (SQLite)**, **nested REST APIs**, **direct HTTP/web URLs**, and **multi-source pipeline integration**. Modeling the operations of a university-wide cultural and technology festival (**Vivanta Fest 2025**), we build an end-to-end data pipeline that extracts registrations from SQL tables, unpacks JSON sponsor tiers, streams event schedules from GitHub, and uses `pathlib` to dynamically discover and join batch files with strict cardinality validation.

### 🎯 Key Learning Objectives
1. **Relational Database Ingestion:** Executing SQL queries via `pd.read_sql_query()` and `pd.read_sql()` over a persistent SQLite connection (`sqlite3.connect`).
2. **Semi-Structured Data Flattening:** Unpacking nested API-style payloads using `pd.json_normalize()` to flatten nested keys (`contact.city`, `contact.tier`).
3. **Web-Based URL Extraction:** Reading remote CSV files directly from GitHub's raw CDN (`raw.githubusercontent.com`).
4. **Modern Filesystem Automation with `pathlib`:** Object-oriented path manipulation (`Path`), dynamic pattern matching (`.glob('day*.csv')`), and directory scaffolding.
5. **Multi-Table Relational Merges:** Recombining partitioned batches with `pd.concat` and executing validated left joins (`how='left'`, `validate='m:1'`).

---

## 🗂️ Files in this Directory

| File | Type | Description |
| :--- | :--- | :--- |
| [`fest_collect.ipynb`](./fest_collect.ipynb) | **Jupyter Notebook** | Complete interactive pipeline with pre-rendered results and Markdown documentation. |
| [`fest_collect.py`](./fest_collect.py) | **Python Script** | Zero-dependency standalone runner for automated terminal execution. |
| [`README.md`](./README.md) | **Documentation** | Detailed session notes, technical analysis, and pipeline architecture. |
| [`fest.db`](./fest.db) | **Database (SQLite)** | Embedded SQLite relational database containing the 400-row `registrations` table. |
| [`sponsors_api.json`](./sponsors_api.json) | **Data (JSON API)** | Nested JSON payload modeling 15 corporate sponsors with contact metadata. |
| [`fest_events.csv`](./fest_events.csv) | **Data (Events CSV)** | Event catalog (venues, scheduled days, and budgets) hosted on GitHub. |
| [`fest_master.csv`](./fest_master.csv) | **Data (Master CSV)** | Integrated master dataset (400 rows $\times$ 9 attributes) ready for analytics. |
| [`fest_data/day1.csv`](./fest_data/day1.csv) | **Batch (CSV)** | Daily registration partition: 130 rows. |
| [`fest_data/day2.csv`](./fest_data/day2.csv) | **Batch (CSV)** | Daily registration partition: 140 rows. |
| [`fest_data/day3.csv`](./fest_data/day3.csv) | **Batch (CSV)** | Daily registration partition: 130 rows. |

---

## 🎪 Business Context: Vivanta Fest 2025

Vivanta Fest is an inter-collegiate festival hosting **5 competitive events** over a **3-day schedule**. The operations committee coordinates registrations from 6 universities, corporate sponsorship pipelines, and venue logistics:

- **Events:** `Dance`, `Coding`, `Quiz`, `Gaming`, `Music`
- **Total Registrations:** 400 students (`S001` to `S400`)
- **Participating Institutions:** St. Xavier Institute, National Tech College, Metro Arts Academy, Apex Engineering College, City Commerce College, Global Science University
- **Ticket Tiers:** ₹0 to ₹500 (in ₹50 increments)

---

## 📝 Detailed Task Walkthrough & Technical Findings

### Task 1: SQLite Database Setup & SQL Query Ingestion
- Generated 400 registration records using `np.random.seed(42)`.
- Wrote to `fest.db` SQLite database using `df_registrations.to_sql('registrations', conn, index=False)`.
- **SQL Ingestion:**
  - `pd.read_sql_query("SELECT * FROM registrations WHERE paid = 'Yes'", conn)`
  - `pd.read_sql("SELECT * FROM registrations WHERE paid = 'Yes'", conn)`
- **Results:**
  - Both methods returned identical shapes: **`(287, 6)`** (287 paid attendees, 6 attributes).
- *Constraint Adhered:* Utilized a simple `SELECT ... WHERE` query.

---

### Task 2: Nested API-Style JSON & `pd.json_normalize`
- Constructed `sponsors_api.json` modeling 15 corporate sponsors across tiers (Platinum, Gold, Silver, Bronze, Supporter).
- Ingested with `json.load()` and flattened using `pd.json_normalize(payload['data'])`.
- **Columns Verified:**
  - `sponsor`, `amount_inr`, **`contact.city`**, **`contact.tier`**.
- **Tier Capital Distribution:**
  - Platinum: ₹270,000 (RedBull, TechGig)
  - Gold: ₹255,000 (Spotify, Domino's, Zepto)
  - Silver: ₹155,000 (Boat, Unstop, Nestle)
  - Bronze: ₹130,000 (Logitech, CodeChef, Decathlon, Keventers)
  - Supporter: ₹45,000 (Skillshare, Subway, Duolingo)

---

### Task 3: Event Catalog & Web-Based URL Ingestion
- Created `fest_events.csv` with 5 event rows:

| Event | Venue | Scheduled Day | Allocated Budget (INR) |
| :--- | :--- | :---: | :---: |
| **Dance** | Main Auditorium | Day 1 | ₹80,000 |
| **Coding** | Computer Lab 3 | Day 2 | ₹60,000 |
| **Quiz** | Seminar Hall B | Day 1 | ₹30,000 |
| **Gaming** | E-Sports Arena | Day 3 | ₹95,000 |
| **Music** | Open Air Amphitheatre | Day 2 | ₹110,000 |

- Loaded directly into memory using its GitHub Raw CDN address:
  `https://raw.githubusercontent.com/Atharvchaudhari1106/ds-work/main/assignment-3/s05_fest_collect/fest_events.csv`
- Output shape confirmed: `events.shape` = **`(5, 4)`**.

---

### Task 4: Pathlib Handling, Batch Globbing, Concat & Validated Merge
1. **Partitioning:**
   - Initialized `fest_data/` folder using `Path('fest_data').mkdir(exist_ok=True)`.
   - Partitioned the 400 registrations into:
     - `day1.csv`: 130 rows (`0:130`)
     - `day2.csv`: 140 rows (`130:270`)
     - `day3.csv`: 130 rows (`270:400`)
     - Total: $130 + 140 + 130 = 400$ rows.
2. **Dynamic Batch Discovery:**
   - Discovered files via `sorted(Path('fest_data').glob('day*.csv'))`.
   - Recombined using `pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)` $\rightarrow$ **`(400, 6)`**.
3. **Validated Left Join:**
   - Merged with `events` on `event` using `validate='m:1'`:
     ```python
     fest_master = pd.merge(recombined, events, on='event', how='left', validate='m:1')
     ```
   - Exported to `fest_master.csv` (shape: `400 rows x 9 columns`).
4. **Assertions:**
   - `assert len(fest_master) == 400` $\rightarrow$ **PASSED**.
   - `assert fest_master['venue'].isna().sum() == 0` $\rightarrow$ **PASSED** (all 400 participants successfully mapped to their assigned event venues).

---

## 🚀 How to Run

### Method 1: Interactive Jupyter Notebook
```bash
jupyter notebook fest_collect.ipynb
```
Select **Kernel -> Restart & Run All** to execute all database queries, web requests, and joins.

### Method 2: Headless Python Verification Script
```bash
python fest_collect.py
```
Recreates all SQLite tables, JSON responses, batch partitions, and master merged CSV files directly in your terminal.
