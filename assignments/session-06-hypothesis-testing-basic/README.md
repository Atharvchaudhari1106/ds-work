# Session 6: Hypothesis Testing (Basic)

This folder contains the complete solutions for **Session 6 - Hypothesis Testing (Basic)** using an interactive Jupyter Notebook.

---

## 📓 Primary Assignment Notebook

👉 [**`session_06_hypothesis_testing_basic.ipynb`**](session_06_hypothesis_testing_basic.ipynb)

### Tasks Covered:
1. **Task 1: Formulating Hypotheses:** Directional null ($H_0: \mu_{\text{Insta}} \le \mu_{\text{YT}}$) and alternative ($H_1: \mu_{\text{Insta}} > \mu_{\text{YT}}$) hypotheses comparing daily time spent on Instagram vs. YouTube.
2. **Task 2: Two-Sample t-Test on Zomato AOV:** Comparing new home page (₹350, $s=50, n=30$) vs. old home page (₹320, $s=50, n=30$) using `scipy.stats.ttest_ind_from_stats`. Computes $t = 2.3238$, $p = 0.0237 < 0.05 \implies$ **Reject $H_0$** with t-distribution rejection curve.
3. **Task 3: A/B Testing Blueprint:** Complete specification for Paytm's redesigned 1-Click UPI Payment button, defining Control, Variant, Conversion KPI, Guardrails, and Hypotheses.
4. **Task 4: Flipkart Wishlist Button A/B Test Significance:** Intuitive and statistical evaluation of 520 vs. 480 clicks out of 1000 users ($p = 0.0736 > 0.05$), explaining why it is NOT statistically significant and likely due to chance.
