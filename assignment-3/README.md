# Assignment Track 3: Data Science Foundations & Numerical Computing with NumPy & Pandas

This directory contains coursework submissions, laboratory notebooks, and applied assignments for **Assignment 3: Numerical Computing & Pandas Data Processing**.

All sessions follow an **`.ipynb`-first** interactive format with pre-rendered results, paired with standalone `.py` scripts and zero-dependency terminal execution runners.

---

## 🗂️ Sessions Index

| Session | Topic | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Session 1** | [NumPy Foundations (Part 1: Arrays & Creation)](./s01_kirana_numpy/README.md) | [`kirana_numpy.ipynb`](./s01_kirana_numpy/kirana_numpy.ipynb) <br> [`kirana_numpy.py`](./s01_kirana_numpy/kirana_numpy.py) | ✅ Completed (Executed) |
| **Session 2** | [NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)](./s02_kirana_indexing/README.md) | [`kirana_indexing.ipynb`](./s02_kirana_indexing/kirana_indexing.ipynb) <br> [`kirana_indexing.py`](./s02_kirana_indexing/kirana_indexing.py) | ✅ Completed (Executed) |
| **Session 3** | [NumPy Advanced (Part 3: Matrix Ops & Manipulation)](./s03_kirana_matrix/README.md) | [`kirana_matrix.ipynb`](./s03_kirana_matrix/kirana_matrix.ipynb) <br> [`kirana_matrix.py`](./s03_kirana_matrix/kirana_matrix.py) | ✅ Completed (Executed) |
| **Session 4** | [Data Collection using Pandas (Part 1)](./s04_society_collect/README.md) | [`society_collect.ipynb`](./s04_society_collect/society_collect.ipynb) <br> [`society_collect.py`](./s04_society_collect/society_collect.py) | ✅ Completed (Executed) |
| **Session 5** | [Data Collection using Pandas (Part 2)](./s05_fest_collect/README.md) | [`fest_collect.ipynb`](./s05_fest_collect/fest_collect.ipynb) <br> [`fest_collect.py`](./s05_fest_collect/fest_collect.py) | ✅ Completed (Executed) |

---

## 🛠️ Module Structure

```text
assignment-3/
├── README.md                          # This directory index and track documentation
├── kirana_numpy.ipynb                 # Quick-access copy of Session 1 notebook
├── kirana_numpy.py                    # Quick-access copy of Session 1 Python runner
├── kirana_indexing.ipynb              # Quick-access copy of Session 2 notebook
├── kirana_indexing.py                 # Quick-access copy of Session 2 Python runner
├── kirana_matrix.ipynb                # Quick-access copy of Session 3 notebook
├── kirana_matrix.py                   # Quick-access copy of Session 3 Python runner
├── society_collect.ipynb              # Quick-access copy of Session 4 notebook
├── society_collect.py                 # Quick-access copy of Session 4 Python runner
├── fest_collect.ipynb                 # Quick-access copy of Session 5 notebook
├── fest_collect.py                    # Quick-access copy of Session 5 Python runner
│
├── s01_kirana_numpy/                  # Session 1: NumPy Foundations (Part 1: Arrays & Creation)
│   ├── README.md                      # Comprehensive session documentation & task analysis
│   ├── kirana_numpy.ipynb             # Executed interactive Jupyter Notebook (All 4 tasks solved)
│   └── kirana_numpy.py                # Standalone zero-dependency verification script
│
├── s02_kirana_indexing/               # Session 2: NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)
│   ├── README.md                      # Comprehensive session documentation & broadcasting guide
│   ├── kirana_indexing.ipynb          # Executed interactive Jupyter Notebook (All 4 tasks solved)
│   └── kirana_indexing.py             # Standalone zero-dependency verification script
│
├── s03_kirana_matrix/                 # Session 3: NumPy Advanced (Part 3: Matrix Ops & Manipulation)
│   ├── README.md                      # Comprehensive session documentation & linear algebra guide
│   ├── kirana_matrix.ipynb            # Executed interactive Jupyter Notebook (All 4 tasks solved)
│   └── kirana_matrix.py               # Standalone zero-dependency verification script
│
├── s04_society_collect/               # Session 4: Data Collection using Pandas (Part 1)
│   ├── README.md                      # Comprehensive session documentation & data ingestion guide
│   ├── society_collect.ipynb          # Executed interactive Jupyter Notebook (All 4 tasks solved)
│   ├── society_collect.py             # Standalone zero-dependency verification script
│   ├── readings_comma.csv             # Standard CSV export (1,200 rows)
│   ├── readings_semicolon.csv         # Semicolon-delimited CSV export
│   ├── readings_tab.tsv               # Tab-separated values export
│   ├── readings.xlsx                  # Excel workbook export (openpyxl)
│   ├── readings.json                  # JSON records export
│   ├── meter_big.csv                  # 60,000-row smart meter dataset for chunking
│   ├── readings_messy.csv             # Injected data defects dataset
│   └── society_issue_report.csv       # Columnar diagnostic issue report
│
└── s05_fest_collect/                  # Session 5: Data Collection using Pandas (Part 2)
    ├── README.md                      # Comprehensive session documentation & multi-source guide
    ├── fest_collect.ipynb             # Executed interactive Jupyter Notebook (All 4 tasks solved)
    ├── fest_collect.py                # Standalone zero-dependency verification script
    ├── fest.db                        # SQLite database with registrations table
    ├── sponsors_api.json              # Nested API-style JSON payload (15 sponsors)
    ├── fest_events.csv                # Event master catalog with venue and budget
    ├── fest_master.csv                # Master merged dataset (400 rows x 9 columns)
    └── fest_data/                     # Directory with partitioned batch CSV files
        ├── day1.csv                   # 130 registration records
        ├── day2.csv                   # 140 registration records
        └── day3.csv                   # 130 registration records
```

---

## 💡 Key Conceptual Highlights

- **Contiguous Memory Buffers:** NumPy arrays allocate flat, unbroken blocks in memory (`C_CONTIGUOUS`), enabling direct hardware cache prefetching.
- **Vectorized SIMD Execution:** NumPy operations bypass Python's bytecode evaluation loop and execute pre-compiled C loops with SIMD vectorization.
- **Slicing & Memory Views:** Slices share underlying memory buffers; modifications affect the parent array unless `.copy()` is explicitly invoked.
- **Broadcasting Principles:** Automatic dimension expansion across scalar and array operands when dimensions are equal or one is 1.
- **Linear Algebra (`np.linalg`):** Inverting non-singular matrices, computing determinants, and calculating steady-state Markov eigenvectors.
- **Multi-Format Pandas Parsers:** Exporting and importing across CSV, Semicolon CSV, TSV, Excel, and JSON with automated schema detection.
- **Out-of-Core Processing (`chunksize`):** Reading large datasets in stream iterators to calculate metrics in constant $O(1)$ memory.
- **Early Issue Detection:** Quantifying missing rates, data type corruption, and high cardinality before feeding machine learning pipelines.
- **Relational SQL Ingestion:** Querying relational databases (`SQLite`, `PostgreSQL`, `MySQL`) directly via `pd.read_sql_query()`.
- **Semi-Structured Normalization:** Unpacking nested API responses into relational 2D structures using `pd.json_normalize()`.
- **Pathlib & Dynamic Globbing:** Object-oriented path resolution, automated directory creation, and batch pattern discovery (`Path.glob`).
- **Validated Joins (`validate='m:1'`):** Enforcing strict relational cardinality during merges to prevent Cartesian row duplications.
