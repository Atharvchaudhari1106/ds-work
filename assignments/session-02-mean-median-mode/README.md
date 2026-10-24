# Session 2: Mean, Median & Mode

This folder contains solutions, scripts, datasets, and a Jupyter Notebook for **Session 2 - Mean, Median & Mode**.

---

## 📋 Table of Tasks & Files

| Task # | Problem Description | Solution Script | Key Concept Demonstrated |
| :--- | :--- | :--- | :--- |
| **Task 1** | Calculate mean of daily Spotify song play counts | [`playlist_stats.py`](playlist_stats.py) | $\text{Mean} = \frac{\sum x}{n}$ (Arithmetic Average) |
| **Task 2** | Calculate median delivery time for Zomato orders | [`zomato_median.py`](zomato_median.py) | Positional middle value; odd vs even lists |
| **Task 3** | Function `most_common_rating(ratings)` for Flipkart ratings | [`flipkart_mode.py`](flipkart_mode.py) | Frequency counting ($\max$ count) using `Counter` |
| **Task 4** | Compare YouTube channels views & analyze outlier impact | [`youtube_outliers.py`](youtube_outliers.py) | Mean sensitivity vs. Median robustness |
| **Task 5** | Load real dataset (IPL player runs) with Pandas & compute metrics | [`dataset_analysis.py`](dataset_analysis.py) | Real-world EDA using `pandas` (`mean`, `median`, `mode`) |
| **All-in-One** | Automated verification runner for all tasks | [`run_all_tasks.py`](run_all_tasks.py) | Runs all 5 tasks sequentially |
| **Notebook** | Interactive Jupyter Notebook with rich outputs | [`session_02_mean_median_mode.ipynb`](session_02_mean_median_mode.ipynb) | Theory, Latex formulas & Code cells |

---

## 🚀 How to Run the Solutions

Make sure your virtual environment is active:

```bash
# From the repository root (ds-work):
# Activate virtual environment (Windows PowerShell):
.venv\Scripts\Activate.ps1

# Run individual tasks:
python assignments/session-02-mean-median-mode/playlist_stats.py
python assignments/session-02-mean-median-mode/zomato_median.py
python assignments/session-02-mean-median-mode/flipkart_mode.py
python assignments/session-02-mean-median-mode/youtube_outliers.py
python assignments/session-02-mean-median-mode/dataset_analysis.py

# Or run the entire suite at once:
python assignments/session-02-mean-median-mode/run_all_tasks.py
```

---

## 📊 Summary of Outputs

### Task 1: Spotify Playlist Daily Plays
- **Input:** `[120, 135, 150, 200, 120, 90, 200]`
- **Calculation:** $\frac{1015}{7} = 145.00$
- **Result:** **145.00 plays/day**

### Task 2: Zomato Order Delivery Times
- **Input:** `[30, 25, 40, 35, 30, 45, 30]`
- **Sorted:** `[25, 30, 30, 30, 35, 40, 45]` ($n=7$, odd)
- **Middle Element:** Index $3$
- **Result:** **30.0 minutes**

### Task 3: Flipkart Product Ratings
- **Input:** `[5, 4, 4, 3, 5, 4, 2, 4]`
- **Frequency:** Rating `4` appears 4 times (highest)
- **Result:** Mode is **4**

### Task 4: YouTube Channels View Comparison (Outlier Impact)
- **Channel A (Steady):** Mean = $488.57$, Median = $490.0$, Difference = $1.43$
- **Channel B (Moderate):** Mean = $442.86$, Median = $400.0$, Difference = $42.86$
- **Channel C (Viral Spike):** Mean = $922.50$, Median = $107.5$, Difference = **$815.00$ (758% divergence)**
- **Conclusion:** **Channel C** is drastically skewed by the single $5000$-view video. The **Mean** is easily distorted by outliers, whereas the **Median** remains stable and representative of typical performance.

### Task 5: Real-World Dataset Analysis (IPL Player Runs)
- **Dataset:** `data/ipl_player_runs.csv` (Kaggle IPL records)
- **Mean Runs:** $395.70$
- **Median Runs:** $421.50$
- **Distribution:** Left-skewed (Skewness = $-0.61$), reflecting that many top players consistently scored between $400$ and $550$ runs.
