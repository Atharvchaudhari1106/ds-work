# Session 1: NumPy Foundations (Part 1: Arrays & Creation)

**Course Track:** Assignment Track 3: Data Science Foundations  
**Module:** NumPy Foundations & Numerical Computing  
**Case Study:** Apna Kirana Store Inventory & Sales Analytics Engine  
**Author:** Atharv Chaudhari (`ds-work`)

---

## 📋 Session Overview

In this session, we establish the foundational mechanics of numerical computing in Python using **NumPy** (`numpy`). We explore how contiguous C-order arrays provide exponential speedups and dramatic memory savings compared to standard Python lists through the lens of a fictional neighborhood grocery store (**Apna Kirana Store**).

### 🎯 Key Learning Objectives
1. **NumPy Array Fundamentals:** Why NumPy is the core linear algebra engine for Data Science and Machine Learning.
2. **Core Creation Constructors:**
   - `np.array()`: Sequence to ndarray conversion.
   - `np.random.randint()`: Discrete uniform random sampling with reproducible seeds.
   - `np.full()`: Constant-filled matrix initialization.
   - `np.zeros()`: Zero-initialized floating-point buffer.
   - `np.ones()`: Unit value initialization (with explicit `dtype=bool` behavior).
   - `np.arange()`: Half-open interval integer stepping.
   - `np.linspace()`: Closed interval linear coordinate interpolation.
   - `np.eye()`: Identity matrix generation.
3. **Array Structural Attributes:** `shape`, `ndim`, `size`, `dtype`, `itemsize`, `nbytes`, and `strides`.
4. **Memory & Performance Profiling:** Python list pointer architecture vs. contiguous memory layout (`C_CONTIGUOUS`), SIMD CPU instructions, and `%timeit` benchmarking.
5. **Reusable Diagnostic Tooling:** Creating a unified `array_report(name, arr)` profiler function.

---

## 🗂️ Files in this Directory

| File | Purpose | Execution State |
| :--- | :--- | :--- |
| [`kirana_numpy.ipynb`](./kirana_numpy.ipynb) | **Primary interactive notebook** containing all tasks, detailed Markdown theory, and executed outputs. | ✅ Pre-rendered & Executed |
| [`kirana_numpy.py`](./kirana_numpy.py) | **Zero-dependency standalone Python verification script** for headless terminal execution. | ✅ Verified & Tested |
| [`README.md`](./README.md) | **Session documentation**, mathematical foundations, and output reference. | 📖 Documentation |

---

## 🛒 Business Context: Apna Kirana Store

Apna Kirana Store manages daily sales and inventory across **6 staple grocery items** over a **7-day sales cycle** (Monday through Sunday):

| Index | Item SKU | Item Description | Price (INR) |
| :---: | :---: | :--- | :---: |
| **0** | `101` | Atta (10kg bag) | ₹52 |
| **1** | `102` | Basmati Rice (1kg) | ₹44 |
| **2** | `103` | Sugar (1kg) | ₹45 |
| **3** | `104` | Mustard Oil (1L) | ₹380 |
| **4** | `105` | Toor Dal (1kg) | ₹140 |
| **5** | `106` | Premium Tea Leaves (500g) | ₹120 |

---

## 📝 Task-by-Task Implementation & Results

### Task 1: Environment Setup & Core Arrays
- **Imports:** NumPy imported as `np`, confirming `np.__version__` (e.g. `2.5.4` / `1.26+`).
- **`units_sold` Matrix:** Generated with `np.random.seed(42)` and `np.random.randint(5, 60, size=(6, 7))`.
  - Values range from 5 to 59 units sold per item per day.
- **`price_inr` Vector:** Initialized with `np.array([52, 44, 45, 380, 140, 120])`.
- **Attributes:**
  - `units_sold`: Shape `(6, 7)`, Ndim `2`, Size `42`, Dtype `int32`, Itemsize `4` bytes.
  - `price_inr`: Shape `(6,)`, Ndim `1`, Size `6`, Dtype `int64`, Itemsize `8` bytes.

### Task 2: Store Tracker Arrays & Specialized Constructors
The store operations are modeled using six specialized tracking arrays:
1. `stock_levels = np.full((6, 7), 100)`: Baseline stock initialized to 100 units for each item across all 7 days.
2. `returns = np.zeros((6, 7))`: Customer return counts initialized to `0.0` (`float64`).
3. `in_stock = np.ones(6, dtype=bool)`: Boolean availability status for the 6 SKUs.
   > **Note on Hint:** Calling `np.ones(6)` without specifying `dtype=bool` produces `float64` numbers (`1.0, 1.0, ...`). Passing `dtype=bool` correctly yields boolean values (`True, True, ...`) taking only 1 byte per element.
4. `item_ids = np.arange(101, 107)`: SKUs `[101, 102, 103, 104, 105, 106]`.
5. `day_marks = np.linspace(0, 6, 7)`: Equidistant day coordinates `[0., 1., 2., 3., 4., 5., 6.]`.
6. `item_pairs = np.eye(6)`: 6x6 identity matrix for item cross-correlations.

### Task 3: Python List vs. NumPy Array Benchmark
A dataset of 1,000,000 transaction amounts (`bills_list = list(range(1000000))`) was converted to `bills_arr = np.array(bills_list)` and back to list with `bills_arr.tolist()`.

#### Memory Analysis
- `sys.getsizeof(bills_list)`: **8,000,056 bytes** (`list pointers only`).
  > **Why "list pointers only"?** A Python list is an array of 8-byte memory pointers referencing separate `PyObject` integer instances. Each 64-bit Python integer allocates 28 bytes of object overhead. Thus, the true memory footprint of `bills_list` is approximately **~36 MB**.
- `bills_arr.nbytes`: **8,000,000 bytes** (~7.63 MB).
- **Efficiency:** The NumPy array represents an immediate **~4.5x memory reduction** over Python's pointer overhead.

#### Speed Comparison (`%timeit`)
- Python built-in `sum(bills_list)`: **~3.54 ms** per execution.
- NumPy vectorized `bills_arr.sum()`: **~165 µs** per execution.
- **Speedup:** NumPy executes **~21x faster** by executing compiled C routines that maximize CPU cache utilization and vectorize instructions.

#### Memory Layout
- `bills_arr.flags['C_CONTIGUOUS']`: `True` (elements occupy an unbroken linear block in physical RAM).
- `bills_arr.strides`: `(8,)` (each step advances 8 bytes to the next 64-bit integer).

---

## 📊 Task 4: Comprehensive Array Report

Executing `array_report(name, arr)` for all nine session arrays produces the following master audit table:

| Array Name | Shape | Ndim | Size | Dtype | Itemsize | Total Nbytes |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `units_sold` | `(6, 7)` | 2 | 42 | `int32` | 4 bytes | 168 B |
| `price_inr` | `(6,)` | 1 | 6 | `int64` | 8 bytes | 48 B |
| `stock_levels` | `(6, 7)` | 2 | 42 | `int64` | 8 bytes | 336 B |
| `returns` | `(6, 7)` | 2 | 42 | `float64` | 8 bytes | 336 B |
| `in_stock` | `(6,)` | 1 | 6 | `bool` | 1 byte | 6 B |
| `item_ids` | `(6,)` | 1 | 6 | `int64` | 8 bytes | 48 B |
| `day_marks` | `(7,)` | 1 | 7 | `float64` | 8 bytes | 56 B |
| `item_pairs` | `(6, 6)` | 2 | 36 | `float64` | 8 bytes | 288 B |
| `bills_arr` | `(1000000,)` | 1 | 1,000,000 | `int64` | 8 bytes | 8,000,000 B |

---

## 🚀 How to Run

### Method 1: Launch Interactive Jupyter Notebook
```bash
jupyter notebook kirana_numpy.ipynb
```
Select **Kernel -> Restart & Run All** to re-render all computations and `%timeit` benchmarks.

### Method 2: Headless Python Verification Script
```bash
python kirana_numpy.py
```
This runs the complete workflow and displays the full diagnostic report in your terminal with zero external dependencies beyond `numpy`.
