# Session 2: Mean, Median & Mode

This folder contains the complete solutions for **Session 2 - Mean, Median & Mode** using an interactive Jupyter Notebook, with Python scripts used only where explicitly mandated by the tasks.

---

## 📓 Primary Assignment Notebook

The core submission is in:
👉 [**`session_02_mean_median_mode.ipynb`**](session_02_mean_median_mode.ipynb)

This notebook contains:
- Mathematical definitions, LaTeX formulas, and concept explanations.
- All 5 tasks solved step-by-step with pre-executed code outputs and dataframes.
- Interactive distribution and outlier comparison charts rendered via `matplotlib`.

---

## 📋 Tasks & File Structure

| Task # | Problem Description | Implementation | Notes |
| :--- | :--- | :--- | :--- |
| **Task 1** | Calculate mean daily Spotify song play counts | [`playlist_stats.py`](playlist_stats.py) + Notebook Cell | Task explicitly requires a script named `playlist_stats.py` |
| **Task 2** | Calculate median delivery time for Zomato orders | Notebook Cell 4 & 5 | In-notebook solution ($\text{Median} = 30.0\text{ mins}$) |
| **Task 3** | Function `most_common_rating(ratings)` for Flipkart ratings | Notebook Cell 6 & 7 | In-notebook function ($\text{Mode} = 4$) |
| **Task 4** | Compare YouTube channels views & analyze outlier impact | Notebook Cell 8, 9 & 10 | Includes bar comparison chart & mathematical explanation |
| **Task 5** | Load real dataset (IPL player runs) with Pandas & compute metrics | Notebook Cell 11 & 12 | Real dataset [`data/ipl_player_runs.csv`](data/ipl_player_runs.csv) + histogram |

---

## 🚀 How to Run the Notebook

1. Ensure the virtual environment is activated:
   ```powershell
   cd C:\Users\Atharv\.gemini\antigravity-ide\scratch\ds-work
   .\.venv\Scripts\Activate.ps1
   ```

2. Open the workspace in your IDE (VS Code / Antigravity):
   - Open [`session_02_mean_median_mode.ipynb`](session_02_mean_median_mode.ipynb)
   - Select the Python kernel from `.venv` (`Python 3.12.10 (.venv)`)
   - Click **Run All** to execute all cells.

3. To run `playlist_stats.py` directly from the terminal (Task 1):
   ```powershell
   python assignments/session-02-mean-median-mode/playlist_stats.py
   ```
