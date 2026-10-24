# Session 10: Bayes' Theorem (Basic)

This directory contains the complete solutions for **Session 10 - Bayes' Theorem (Basic)** implemented as an interactive, fully pre-executed Jupyter Notebook.

---

## 📓 Primary Assignment Notebook

👉 [**`session_10_bayes_theorem_basic.ipynb`**](session_10_bayes_theorem_basic.ipynb)

### Tasks Covered:

1. **Task 1: Bayes' Posterior Function:**
   - Implementation of `bayes_posterior(prior, likelihood, evidence)` using Bayes' Theorem:
     $$P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}$$
   - Includes input validation, division-by-zero protection, and validation against standard benchmark scenarios (rare disease medical testing, biased coin identification, machine defect alarm).

2. **Task 2: Swiggy Premium Restaurant Scenario:**
   - Explicit definitions and comments for Prior, Likelihood, and Marginal Evidence via the Law of Total Probability:
     - $P(\text{Premium}) = 10\%$, $P(\text{Regular}) = 90\%$
     - $P(\text{Discount} \mid \text{Premium}) = 80\%$, $P(\text{Discount} \mid \text{Regular}) = 20\%$
     - $P(\text{Discount}) = (0.80 \times 0.10) + (0.20 \times 0.90) = 0.08 + 0.18 = 0.26$ ($26\%$)
     - Posterior $P(\text{Premium} \mid \text{Discount}) = \frac{0.08}{0.26} \approx \mathbf{30.77\%}$
   - Includes dual visualization: Prior vs. Posterior probability update bar chart and discount contribution pie chart.

3. **Task 3: Spam Detection Filter Simulation:**
   - Simulated realistic dataset of 20 email subjects (8 Spam, 12 Ham/Non-Spam).
   - Scanned subjects for keyword `'free'` using regex word boundaries.
   - Calculated:
     - Prior $P(\text{Spam}) = 40.0\%$, Likelihood $P(\text{'free'} \mid \text{Spam}) = 75.0\%$, Likelihood $P(\text{'free'} \mid \text{Ham}) = 16.67\%$
     - Total Evidence $P(\text{'free'}) = 40.0\%$
     - Posterior $P(\text{Spam} \mid \text{'free'}) = \mathbf{75.00\%}$
   - Visualized with class contingency matrix and Bayesian belief shift chart.

4. **Task 4: Real-World App Example (Instagram Bot Detection):**
   - Full prompt submitted to ChatGPT/Copilot and resulting scenario documented.
   - Evaluated Instagram's Trust & Safety bot detection model based on the observable feature `"Bio contains suspicious external link"`:
     - Prior $P(\text{Bot}) = 5.0\%$, Likelihoods $70.0\%$ (bots) vs $2.0\%$ (genuine).
     - Posterior $P(\text{Bot} \mid \text{Suspicious Link}) = \mathbf{64.81\%}$.
     - Engineering insight: Explains why Instagram initiates CAPTCHA / SMS OTP challenges rather than immediate permanent bans due to the Base Rate Fallacy ($35.19\%$ false alarm rate on link-flagged accounts).

---

## 📊 Summary of Results

| Task / Scenario | Prior Probability | Marginal Evidence | Posterior Probability | Key Data Science Takeaway |
| :--- | :---: | :---: | :---: | :--- |
| **Task 1: Diagnostic Test** | $1.0\%$ | $5.94\%$ | **$16.09\%$** | Diagnostic tests require Bayesian adjustment for rare base rates. |
| **Task 2: Swiggy Discount** | $10.0\%$ | $26.0\%$ | **$30.77\%$** | Seeing a discount triples the probability of a restaurant being premium ($10\% \to 30.77\%$). |
| **Task 3: Email Spam Filter** | $40.0\%$ | $40.0\%$ | **$75.00\%$** | Seeing `'free'` boosts spam likelihood from $40.0\%$ to $75.0\%$. |
| **Task 4: Instagram Bot Account** | $5.0\%$ | $5.40\%$ | **$64.81\%$** | High-sensitivity flags still produce false positives when the underlying population is predominantly non-bot. |
