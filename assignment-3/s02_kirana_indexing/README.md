# Session 2: NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)

**Course Track:** Assignment Track 3: Data Science Foundations  
**Module:** Intermediate NumPy - Indexing, Slicing & Broadcasting  
**Case Study:** Apna Kirana Store Multi-Dimensional Inventory & Revenue Optimization Engine  
**Author:** Atharv Chaudhari (`ds-work`)

---

## 📋 Session Overview

This session advances numerical array manipulation techniques in **NumPy**, focusing on **high-dimensional indexing**, **vectorized slicing**, **boolean filtering**, and **broadcasting mechanics**. Using the real-world operational dataset of **Apna Kirana Store**, we eliminate slow Python iteration and perform multi-dimensional array queries, surge pricing calculations, and machine learning feature scaling in pure compiled C routines.

### 🎯 Key Learning Objectives
1. **Multi-Dimensional Indexing & Slicing:** Extracting rows, columns, sub-blocks, and alternate stepping patterns across 2D matrices and 3D tensors (`month_units`).
2. **View vs. Copy Semantics:** Understanding why slices are memory views and when `.copy()` is required to safeguard against buffer corruption.
3. **Boolean Indexing & Masking:** Filtering elements based on numerical thresholds (`units_sold > 40`) and performing in-place conditional updates without loops.
4. **Fancy Indexing:** Querying arbitrary non-contiguous rows (`[0, 3, 5]`) with coordinate lists.
5. **Broadcasting Mechanics:**
   - **Array-to-Array Broadcasting:** Expanding a `(6, 1)` price vector across a `(6, 7)` sales matrix.
   - **Scalar-to-Array Broadcasting:** Applying uniform surcharges (`1.05` GST).
   - **Trailing Dimension Alignment:** Applying a `(7,)` weekend surge factor across columns.
6. **Feature Scaling (Min-Max Normalization):** Using `min(axis=1, keepdims=True)` and `max(axis=1, keepdims=True)` to normalize inventory demand into $[0, 1]$ per item.

---

## 🗂️ Files in this Directory

| File | Purpose | Execution State |
| :--- | :--- | :--- |
| [`kirana_indexing.ipynb`](./kirana_indexing.ipynb) | **Primary interactive notebook** containing all 4 tasks solved, Markdown theoretical notes, and executed cell outputs. | ✅ Pre-rendered & Executed |
| [`kirana_indexing.py`](./kirana_indexing.py) | **Zero-dependency standalone Python verification script** for headless terminal execution. | ✅ Verified & Tested |
| [`README.md`](./README.md) | **Session documentation**, mathematical foundations, and output reference. | 📖 Documentation |

---

## 🛒 Business Context & Item Catalog

| Row Index | Item SKU | Item Description | Unit Price (INR) |
| :---: | :---: | :--- | :---: |
| **0** | `101` | Rice | ₹52 |
| **1** | `102` | Atta | ₹44 |
| **2** | `103` | Sugar | ₹45 |
| **3** | `104` | Tea | ₹380 |
| **4** | `105` | Oil | ₹140 |
| **5** | `106` | Dal | ₹120 |

---

## 📝 Detailed Task Walkthrough & Technical Findings

### Task 4: Multi-Dimensional Slicing & Views
- **Data Generation:**
  - `units_sold`: Generated with `np.random.seed(42)` and `np.random.randint(5, 60, size=(6, 7))` (Week 1 sales for 6 items over 7 days).
  - `month_units`: Generated with `np.random.randint(5, 60, size=(4, 6, 7))` (4 weeks $\times$ 6 items $\times$ 7 days).
- **Subarray Extractions:**
  1. `tea_week = units_sold[3, :].copy()`: Row index 3 representing full week tea sales `[28, 48, 34, 42, 6, 25, 37]`.
  2. `day3_sales = units_sold[:, 2].copy()`: Column index 2 representing Day 3 (Wednesday, 0-indexed) sales across all items `[33, 27, 28, 34, 48, 19]`. *(Day index 3 Thursday is `[19, 15, 7, 42, 29, 51]`)*.
  3. `staple_block = units_sold[0:3, 3:7].copy()`: Shape `(3, 4)` containing rows 0–2 (rice, atta, sugar) across the last four days (Thursday to Sunday).
  4. `alt_days = units_sold[:, ::2].copy()`: Shape `(6, 4)` taking step size 2 (columns 0, 2, 4, 6: Mon, Wed, Fri, Sun).
  5. `dal_last = units_sold[-1, :].copy()`: Dal sales extracted using negative row index `-1`.
  6. `w3_tea_d6 = month_units[2, 3, 5]`: Scalar element `5` for Week 3 (index 2), Tea (index 3), Day 6 (index 5) in 3D space *(or direct coordinates `month_units[3, 3, 6]` = `48`)*.
- **View vs. Copy Semantic:**
  - Slices in NumPy share the memory buffer of the base array. Modifying an uncopied slice `view[0] = 999` directly corrupts `units_sold`.
  - Invoking `.copy()` creates an independent memory allocation, ensuring complete isolation.

---

### Task 1: Boolean Indexing, Fancy Indexing & Negative Masking
- **High Sales Filtering:**
  - `high_mask = units_sold > 40`
  - Total `True` entries: **16 out of 42** sales points exceeded 40 units.
  - Matching sales: `[43, 56, 47, 43, 57, 44, 57, 48, 42, 48, 53, 46, 51, 55, 48, 59]`.
- **Fancy Indexing:**
  - `top_items = units_sold[[0, 3, 5]]` extracts rows for rice (`0`), tea (`3`), and dal (`5`), creating a new array of shape `(3, 7)`.
- **Negative Stock Depletion Rectification:**
  - `stock_change = units_sold - 30`
  - `neg_mask = stock_change_clean < 0`
  - Total negative entries rectified: **20 values**.
  - `stock_change_clean[neg_mask] = 0` sets all negative deficits to 0 in a single vectorized operation **without any Python loops**.

---

### Task 2: Broadcasting Rules & Multi-Tier Revenue Engine
1. **Price Vector Construction:**
   - `price_col = np.array([[52], [44], [45], [380], [140], [120]])` creates a 2D column vector of shape `(6, 1)`.
2. **Array-to-Array Revenue Broadcasting:**
   - Operands: `units_sold` `(6, 7)` and `price_col` `(6, 1)`.
   - Dimension 1 of `price_col` has length 1; NumPy automatically stretches it 7 times along axis 1 to produce `revenue_inr` of shape `(6, 7)`.
3. **Scalar GST Surcharge:**
   - `revenue_gst = revenue_inr * 1.05` stretches the scalar `1.05` across all 42 entries.
4. **Weekend Surge Factor:**
   - `day_factor = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.3, 1.4])` of shape `(7,)`.
   - Aligns with trailing dimension: `(6, 7)` vs `(1, 7)` -> stretches down the 6 rows to calculate `weekend_revenue`.
5. **Exact Mathematical Verification:**
   - `np.array_equal(revenue_inr[1], units_sold[1] * 44)` returns `True`, verifying that row 1 (atta @ 44 INR) matches exact multiplication.
   - *Broadcasting rule:* Two dimensions are compatible when **they are equal**, or **one of them is 1**. When broadcasting fails, printing `.shape` of both operands immediately isolates the mismatch.

---

### Task 3: Feature Scaling (Min-Max Normalization) with `keepdims=True`
- **Normalization Formula:**
  $$\text{units\_scaled}_{i, j} = \frac{\text{units\_sold}_{i, j} - \min_j(\text{units\_sold}_i)}{\max_j(\text{units\_sold}_i) - \min_j(\text{units\_sold}_i)}$$
- **Preserving Dimensions with `keepdims=True`:**
  - `row_mins = units_sold.min(axis=1, keepdims=True)` produces shape `(6, 1)` instead of `(6,)`.
  - `row_maxs = units_sold.max(axis=1, keepdims=True)` produces shape `(6, 1)` instead of `(6,)`.
  - Because axis 1 is retained as length 1, column-wise broadcasting across `units_sold` `(6, 7)` executes cleanly without manual `.reshape(-1, 1)`.
- **Validation:**
  - `np.allclose(units_scaled.min(axis=1), 0.0)` $\rightarrow$ `True`.
  - `np.allclose(units_scaled.max(axis=1), 1.0)` $\rightarrow$ `True`.
  - Every item row is successfully mapped onto $[0.0, 1.0]$ with zero loops and zero third-party libraries.

---

## 🚀 How to Run

### Method 1: Interactive Jupyter Notebook
```bash
jupyter notebook kirana_indexing.ipynb
```
Select **Kernel -> Restart & Run All** to verify all cells and interactive visualizations.

### Method 2: Headless Python Verification Script
```bash
python kirana_indexing.py
```
Executes the full pipeline and displays clean tabular output in your terminal.
