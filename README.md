# Data Science Work Repository (`ds-work`)

Welcome to your central Data Science repository! This workspace is configured for your Data Science coursework, practical sessions, assignments, and machine learning projects.

---

## 📁 Repository Structure

```text
ds-work/
├── .gitignore                                 # Ignores .venv, cache, and OS files
├── requirements.txt                           # Python project dependencies (pandas, numpy, matplotlib)
├── README.md                                  # Repository overview and setup guide
│
├── assignments/                               # Dedicated assignments directory
│   ├── README.md                              # Assignments index and submission guide
│   │
│   ├── session-01-intro-to-statistics/        # Session 1: Introduction to Statistics in Data Science
│   │   ├── session_01_intro_to_statistics.ipynb # Primary interactive notebook (All 4 tasks solved & executed)
│   │   └── README.md                          # Session 1 task descriptions & answers
│   │
│   └── session-02-mean-median-mode/           # Session 2: Mean, Median & Mode
│       ├── session_02_mean_median_mode.ipynb  # Primary interactive notebook (All 5 tasks solved & executed)
│       ├── playlist_stats.py                  # Task 1 Python script (explicitly requested)
│       ├── README.md                          # Session 2 task descriptions & answers
│       └── data/
│           └── ipl_player_runs.csv            # Real-world dataset for Task 5
│
├── notebooks/                                 # General exploratory data analysis (EDA)
└── data/                                      # Shared raw and processed datasets
```

---

## 🛠️ Environment Setup

A dedicated Python virtual environment `.venv` is configured with `pandas`, `numpy`, and `matplotlib`.

### Activate the environment:
**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (cmd):**
```cmd
.venv\Scripts\activate.bat
```

To install any future libraries:
```powershell
.venv\Scripts\pip install <package_name>
.venv\Scripts\pip freeze > requirements.txt
```

---

## 📤 Pushing Changes to GitHub

```powershell
git add .
git commit -m "feat: complete Session 1 and Session 2 executed notebooks"
git push origin main
```
