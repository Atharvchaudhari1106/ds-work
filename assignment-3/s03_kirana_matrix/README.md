# Session 3: NumPy Advanced (Part 3: Matrix Ops & Manipulation)

**Course Track:** Assignment Track 3: Data Science Foundations  
**Module:** Advanced NumPy - Matrix Operations & Array Manipulation  
**Case Study:** Apna Kirana Store Multi-Product Matrix Analytics & Markov Market Share Engine  
**Author:** Atharv Chaudhari (`ds-work`)

---

## 📋 Session Overview

This session explores advanced **matrix algebra**, **multivariate statistical summaries**, **stochastic Markov processes**, and **memory buffer layout** in **NumPy**. Building upon the Apna Kirana Store dataset, we demonstrate how high-performance matrix operations replace complex programmatic loops with single-instruction linear algebra calls executed directly in BLAS/LAPACK.

### 🎯 Key Learning Objectives
1. **Matrix Multiplication Operators:** The critical distinction between element-wise multiplication (`*`), vector dot products (`.dot()`), and linear algebraic matrix products (`@` / `np.matmul()`).
2. **Item Co-Sales & Covariance Modeling:** Generating item-to-item correlation matrices via `units_sold @ units_sold.T`.
3. **Pure NumPy Statistical Reductions:** Computing row-wise and column-wise aggregates (`sum`, `mean`, `median`, `std`, `var`) with zero reliance on pandas.
4. **Markov Transition Models & Stationary Equilibria:**
   - Determinant calculation (`np.linalg.det`).
   - Matrix inversion (`np.linalg.inv`) and identity validation.
   - Eigendecomposition (`np.linalg.eig`) to derive long-term brand-switching equilibrium market shares.
5. **Array Concatenation, Stacking & Splitting:** Multi-week joining along existing (`axis=1`) and new (`axis=0`) axes, followed by lossless decomposition with `np.split()`.
6. **Physical Memory Mechanics:** Analyzing memory sharing with `np.shares_memory()` to contrast memory views (`ravel()`) against deep copies (`flatten()`).

---

## 🗂️ Files in this Directory

| File | Purpose | Execution State |
| :--- | :--- | :--- |
| [`kirana_matrix.ipynb`](./kirana_matrix.ipynb) | **Primary interactive notebook** containing all 4 tasks solved, Markdown theoretical notes, and executed cell outputs. | ✅ Pre-rendered & Executed |
| [`kirana_matrix.py`](./kirana_matrix.py) | **Zero-dependency standalone Python verification script** for headless terminal execution. | ✅ Verified & Tested |
| [`README.md`](./README.md) | **Session documentation**, mathematical foundations, and output reference. | 📖 Documentation |

---

## 📝 Task-by-Task Implementation & Mathematical Analysis

### Task 3: Daily Revenue Engine & Co-Sales Matrix
- **Data Initialization:** `units_sold` (shape `(6, 7)`) and `price_inr` (shape `(6,)`) regenerated with `np.random.seed(42)`.
- **Three Equivalent Daily Revenue Methods:**
  1. **Dot Product:** `price_inr.dot(units_sold)` $\rightarrow$ contracts 1D vector and 2D matrix along shared axis of length 6.
  2. **Formal Matrix Product:** `np.matmul(price_inr, units_sold)` $\rightarrow$ performs BLAS matrix multiplication.
  3. **Reshaped Element-Wise Sum:** `(units_sold * price_inr.reshape(6, 1)).sum(axis=0)` $\rightarrow$ broadcasts price down columns and reduces vertically.
- **Results Across Week (Mon–Sun in INR):**
  `[₹22,648, ₹30,184, ₹26,084, ₹28,103, ₹20,574, ₹24,021, ₹31,658]`
- **Verification:** `np.allclose` confirms all three methods evaluate to bit-identical numerical results.
- **Item Co-Sales Matrix:**
  $$\text{item\_cosales} = \text{units\_sold} \times \text{units\_sold}^T \quad (\text{Shape: } 6 \times 6)$$
  - Diagonal entries $\text{item\_cosales}_{i, i}$ indicate the Euclidean norm squared (total sales power) of item $i$.
  - Off-diagonal entries measure basket co-occurrence and shared sales velocity between product pairs.

---

### Task 4: Weekly Statistical Summary & Busiest Day Analysis
All summary metrics were computed using pure NumPy operations without pandas:

| Item | SKU | Weekly Total | Mean (units/day) | Median | Std Dev ($\sigma$) | Variance ($\sigma^2$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rice** | `101` | 235 | 33.57 | 33.0 | 14.75 | 217.67 |
| **Atta** | `102` | 208 | 29.71 | 27.0 | 14.19 | 201.35 |
| **Sugar** | `103` | 208 | 29.71 | 28.0 | 17.52 | 307.06 |
| **Tea** | `104` | 220 | 31.43 | 34.0 | 12.67 | 160.53 |
| **Oil** | `105` | 249 | 35.57 | 31.0 | 12.57 | 157.96 |
| **Dal** | `106` | 284 | 40.57 | 48.0 | 15.46 | 239.10 |

- **Busiest Day:** Determined via `np.argmax(units_sold.sum(axis=0)) + 1`:
  - **Day 7 (Sunday)** recorded the maximum weekly volume with **230 units sold**.

---

### Task 1: Brand-Switching Markov Chain & Steady-State Market Share
We model weekly consumer brand-switching among three competing tea brands:
$$P = \begin{bmatrix} 0.7 & 0.2 & 0.1 \\ 0.3 & 0.5 & 0.2 \\ 0.2 & 0.3 & 0.5 \end{bmatrix}$$

1. **Invertibility & Determinant:**
   - $\det(P) = 0.1100 \neq 0$ (confirming non-singularity and full rank).
   - $\text{inv}(P) @ P = I_3$ confirmed with `np.allclose`.
2. **Stationary Distribution ($\pi$):**
   - In a Markov chain, stationary market share satisfies $\pi P = \pi$, or equivalently $P^T \pi^T = 1.0 \cdot \pi^T$.
   - Eigenvalue decomposition on $P^T$ (`switch_p.T`) yields eigenvalues $[1.0000, 0.4618, 0.2382]$.
   - Extracting the eigenvector corresponding to $\lambda = 1.0$ and normalizing such that $\sum \pi_i = 1.0$:
     - **Brand A (Tata Tea):** **46.34%** market share
     - **Brand B (Red Label):** **31.71%** market share
     - **Brand C (Wagh Bakri):** **21.95%** market share
   - Verified condition: $\pi P = \pi$ evaluated to `True`.

---

### Task 2: Multi-Week Array Operations & Memory Profiling
1. **Horizontal Concatenation:**
   - `two_weeks = np.concatenate([units_sold, week2], axis=1)` combines 2 weeks into shape **`(6, 14)`**.
2. **Tensor Stacking:**
   - `stacked = np.stack([units_sold, week2], axis=0)` packs weeks into a 3D tensor of shape **`(2, 6, 7)`**.
3. **Lossless Decomposition:**
   - `np.split(two_weeks, 2, axis=1)` splits the array back into original weekly matrices; assertions confirmed 100% data fidelity.
4. **Memory Profiling (`ravel()` vs. `flatten()`):**
   - `np.shares_memory(two_weeks, two_weeks.ravel())` $\rightarrow$ **`True`** (Memory view).
   - `np.shares_memory(two_weeks, two_weeks.flatten())` $\rightarrow$ **`False`** (Deep memory copy).
   - **Mutation Test:** Changing `rav[0] = 999` directly modified `two_weeks[0, 0]`, whereas mutating `flat[1] = 888` left `two_weeks[0, 1]` completely untouched.

---

## 🚀 How to Run

### Method 1: Interactive Jupyter Notebook
```bash
jupyter notebook kirana_matrix.ipynb
```
Select **Kernel -> Restart & Run All** to verify all computations, linear algebra verifications, and visualizations.

### Method 2: Headless Python Verification Script
```bash
python kirana_matrix.py
```
Runs all four tasks and renders formatted diagnostic tables directly in your terminal.
