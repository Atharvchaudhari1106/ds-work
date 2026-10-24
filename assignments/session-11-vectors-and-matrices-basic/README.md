# Session 11: Vectors & Matrices (Basic)

This directory contains the complete solutions for **Session 11 - Vectors & Matrices (Basic)** implemented as an interactive, fully pre-executed Jupyter Notebook.

---

## 📓 Primary Assignment Notebook

👉 [**`session_11_vectors_and_matrices_basic.ipynb`**](session_11_vectors_and_matrices_basic.ipynb)

### Tasks Covered:

1. **Task 1: 1D Vector Playlist Duration:**
   - Represented 5 song durations in seconds as a Python list and 1D vector $\mathbf{v} \in \mathbb{R}^5$: `[210, 180, 245, 200, 175]`.
   - Calculated total playlist duration using both Python `sum()` and NumPy `np.sum(v)`.
   - Results:
     - Total Duration: **1,010 seconds** ($16 \text{ minutes and } 50 \text{ seconds}$, or $16.83 \text{ minutes}$).
     - Summary statistics: Mean = $202.0\text{s}$, Min = $175\text{s}$, Max = $245\text{s}$.
   - Includes Matplotlib visualization showing each track's duration relative to the playlist average.

2. **Task 2: 3x3 Matrix Swiggy Food Ratings:**
   - Represented a $3 \times 3$ user-item rating matrix $R \in \mathbb{R}^{3 \times 3}$ for 3 friends across 3 Swiggy food items:
     $$R = \begin{bmatrix} 5 & 4 & 3 \\ 4 & 5 & 2 \\ 3 & 4 & 5 \end{bmatrix}$$
   - Extracted ratings for the **second food item** (Column Index 1: *"Butter Naan"*):
     - Friend 1 (Aman): **4 / 5 ★**
     - Friend 2 (Priya): **5 / 5 ★**
     - Friend 3 (Rohan): **4 / 5 ★**
     - Mean Rating for Item 2: **4.33 / 5.0 ★**
   - Visualized with a 2D Heatmap of ratings and a bar chart focusing on the second item.

3. **Task 3: Daily Dish Orders Across 3 Days (Matrix Column Sum):**
   - Modeled an order volume matrix $M \in \mathbb{R}^{3 \times 4}$ (3 Days $\times$ 4 Dishes):
     $$M = \begin{bmatrix} 24 & 35 & 18 & 42 \\ 30 & 48 & 25 & 55 \\ 28 & 42 & 22 & 49 \end{bmatrix}$$
   - Computed column-wise reduction along Axis 0 (`np.sum(M, axis=0)`):
     - Paneer Biryani: **82 orders**
     - Butter Chicken: **125 orders**
     - Veg Manchurian: **65 orders**
     - Masala Dosa: **146 orders**
   - Visualized using stacked bar charts showing daily breakdown per dish and ranking by total order volume.

4. **Task 4: Flipkart Products Matrix & Revenue Function:**
   - Represented 5 products in a $5 \times 2$ table matrix $P$ (Column 0: Price, Column 1: Quantity Sold).
   - Authored the dedicated function `calculate_product_revenue(matrix)` calculating row-wise element product $\mathbf{r} = \mathbf{p} \odot \mathbf{q}$:
     - Wireless Earbuds: ₹1,499 $\times$ 120 = **₹179,880**
     - Smart Fitness Band: ₹2,499 $\times$ 85 = **₹212,415**
     - Ergonomic Laptop Stand: ₹899 $\times$ 210 = **₹188,790**
     - Fast USB-C Charger: ₹699 $\times$ 340 = **₹237,660**
     - Noise-Cancelling Headphones: ₹4,999 $\times$ 45 = **₹224,955**
   - Calculated total store revenue via vector dot product $\mathbf{p}^T \mathbf{q} = \mathbf{₹1,043,700}$.
   - Visualized with horizontal revenue comparisons and a price vs. quantity bubble scatter plot.

---

## 📊 Summary of Results

| Task / Scenario | Linear Algebra Concept | Dimensions | Key Result / Aggregate |
| :--- | :--- | :---: | :--- |
| **Task 1: Playlist** | 1D Vector Summation | $\mathbf{v} \in \mathbb{R}^5$ | Total Duration = **1,010 seconds** ($16\text{m } 50\text{s}$) |
| **Task 2: Swiggy Ratings** | 2D Matrix Column Slicing | $R \in \mathbb{R}^{3 \times 3}$ | Second Item Ratings = **[4, 5, 4]** (Mean: 4.33 ★) |
| **Task 3: Dish Orders** | Matrix Axis 0 Reduction | $M \in \mathbb{R}^{3 \times 4}$ | Dish Totals = **[82, 125, 65, 146]** orders |
| **Task 4: Flipkart Revenue** | Hadamard Product & Dot Product | $P \in \mathbb{R}^{5 \times 2}$ | Total Revenue = **₹1,043,700** across 5 products |
