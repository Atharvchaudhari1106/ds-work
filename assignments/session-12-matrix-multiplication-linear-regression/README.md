# Session 12: Matrix Multiplication & Linear Regression Math Intuition

This directory contains the complete solutions for **Session 12 - Matrix Multiplication & Linear Regression Math Intuition** implemented as an interactive, fully pre-executed Jupyter Notebook.

---

## 📓 Primary Assignment Notebook

👉 [**`session_12_matrix_multiplication_linear_regression.ipynb`**](session_12_matrix_multiplication_linear_regression.ipynb)

### Tasks Covered:

1. **Task 1: Instagram 2x2 Matrix Multiplication:**
   - Multiplied matrix $A \in \mathbb{R}^{2 \times 2}$ (Engagement likes & comments for 2 posts over 2 days) by matrix $B \in \mathbb{R}^{2 \times 2}$ (Reach & ad revenue value weights):
     $$A = \begin{bmatrix} 120 & 45 \\ 200 & 80 \end{bmatrix}, \quad B = \begin{bmatrix} 2 & 3 \\ 1 & 4 \end{bmatrix}$$
     $$C = A \cdot B = \begin{bmatrix} 285 & 540 \\ 480 & 920 \end{bmatrix}$$
   - Verified step-by-step dot products using both native Python loops and NumPy `@` operator.
   - Includes side-by-side heatmaps illustrating Matrix A, Matrix B, and Product Matrix C.

2. **Task 2: Linear Regression Prediction Function:**
   - Authored the universal prediction function `linear_regression_predict(x, m, c)` implementing the univariate regression formula:
     $$y = mx + c$$
   - Supports both single scalar values and batch NumPy arrays/lists.
   - Verified against diverse benchmark test cases (standard scalars, zero feature tests, depreciation negative slopes, and vectorized arrays).

3. **Task 3: Zomato Order Delivery Time Prediction:**
   - Implemented the empirical delivery model $y = 4x + 10$:
     - Slope $m = 4$ minutes/km (transit time rate).
     - Intercept $c = 10$ minutes (fixed kitchen preparation and order dispatch baseline).
   - Calculated predicted delivery times for distances $x \in \{2\text{ km}, 5\text{ km}, 8\text{ km}\}$:
     - At $2\text{ km}$: $4(2) + 10 = \mathbf{18\text{ minutes}}$
     - At $5\text{ km}$: $4(5) + 10 = \mathbf{30\text{ minutes}}$
     - At $8\text{ km}$: $4(8) + 10 = \mathbf{42\text{ minutes}}$
   - Includes a Matplotlib regression line plot highlighting the 10-minute prep intercept and projection drop lines for the 3 predicted coordinates.

4. **Task 4: Flipkart Product Price Prediction — Slope & Intercept Intuition:**
   - Evaluated the model $\text{Price} = m \cdot (\text{Rating}) + c$:
     - **Slope ($m$):** Represents the rate of price appreciation per 1-star increase in user rating ($\frac{\Delta \text{Price}}{\Delta \text{Rating}}$). Captures consumer willingness to pay a premium for verified quality and brand equity.
     - **Intercept ($c$):** Represents the theoretical baseline entry-level price floor of a product with zero ratings, covering fundamental manufacturing, packaging, inventory, and platform listing costs.
   - Includes an illustrative visual model ($\text{Price} = 600 \cdot \text{Rating} + 400$) with slope triangle and price annotations.

5. **Task 5: Matrix Multiplication in Spotify Recommender Systems:**
   - Prompt submitted: *"How does matrix multiplication help in training a machine learning model like Spotify's song recommendation system?"*
   - Summary in our own words:
     1. Spotify uses **Matrix Factorization** to decompose massive user-song listening matrices into dense latent vectors ($U$ for user musical tastes, $V$ for track acoustic features).
     2. Multiplying $U \times V^T$ reconstructs the entire predicted user-track affinity matrix, computing billions of preference scores simultaneously via tensor dot products.
     3. During training, GPU-accelerated matrix multiplication allows rapid loss minimization and weight updates using algorithms like Alternating Least Squares (ALS).
     4. During inference, instant vector dot products deliver sub-second song ranking for playlists like "Discover Weekly".
   - Includes a simulation demo with a predicted affinity heatmap across users and music tracks.

---

## 📊 Summary of Results

| Task / Topic | Mathematical Expression | Key Computational Output | Practical Takeaway |
| :--- | :--- | :---: | :--- |
| **Task 1: Matrix Multiplication** | $C = A \cdot B$ | $\begin{bmatrix} 285 & 540 \\ 480 & 920 \end{bmatrix}$ | Matrix multiplication models multi-metric linear transformations. |
| **Task 2: Predict Function** | $y = mx + c$ | Reusable Function | Forms the inference engine of univariate regression. |
| **Task 3: Zomato Delivery** | $y = 4x + 10$ | **18m, 30m, 42m** | Fixed baseline prep ($c=10$) + variable transit time ($m=4$). |
| **Task 4: Flipkart Intuition** | $\text{Price} = m(\text{Rating}) + c$ | Slope: Sensitivity / Intercept: Floor | Connects linear algebra parameters to real-world economic value. |
| **Task 5: Spotify Recommender** | $R \approx U \cdot V^T$ | Collaborative Filtering Affinity | Matrix multiplication enables personalized recommendations at scale. |
