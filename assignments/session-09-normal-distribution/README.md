# Session 9: Normal Distribution

This folder contains the complete solutions for **Session 9 - Normal Distribution** using an interactive Jupyter Notebook.

---

## 📓 Primary Assignment Notebook

👉 [**`session_09_normal_distribution.ipynb`**](session_09_normal_distribution.ipynb)

### Tasks Covered:
1. **Task 1: Generating & Plotting Normal Distribution:** 100 random values generated using `numpy.random.normal(loc=50, scale=10)`, overlaid with the continuous Gaussian bell curve $f(x)$.
2. **Task 2: Fitness Tracker Daily Steps Symmetry:** Demonstrating that in a symmetric distribution, $\text{Mean} (5965) \approx \text{Median} (6000) \approx \text{Mode} (6000)$ using `numpy.mean()`, `numpy.median()`, and `scipy.stats.mode()`.
3. **Task 3: Online Game Scores & 68–95–99.7 Empirical Rule:** 200 player scores simulated with $N(70, 15^2)$, verifying that $72.5\%$ fall within the $\pm 1\sigma$ interval $[55, 85]$, matching the theoretical target ($\approx 68.3\%$) with highlighted visualization.
4. **Task 4: Real-World Normal Distribution Scenario:** 4-line explanation of why **Spotify Track Durations** fit a Gaussian normal curve through industry commercial norms, the Central Limit Theorem, and symmetric tapering tails.
