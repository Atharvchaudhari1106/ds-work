# Data Science Work Repository (`ds-work`)

Welcome to your central Data Science repository! This workspace is configured for your Data Science coursework, practical sessions, assignments, and machine learning projects.

---

## 📁 Repository Structure

```text
ds-work/
├── .gitignore                                 # Ignores .venv, cache, and OS files
├── requirements.txt                           # Python project dependencies
├── README.md                                  # Repository overview and setup guide
│
├── assignments/                               # Dedicated assignments directory / sub-repo
│   ├── README.md                              # Assignments index and submission guide
│   └── session-02-mean-median-mode/           # Session 2: Mean, Median & Mode
│       ├── playlist_stats.py                  # Task 1: Mean Spotify play counts
│       ├── zomato_median.py                   # Task 2: Median Zomato delivery times
│       ├── flipkart_mode.py                   # Task 3: Mode for Flipkart product ratings
│       ├── youtube_outliers.py                # Task 4: Outlier impact on YouTube views
│       ├── dataset_analysis.py                # Task 5: Real IPL dataset analysis (Pandas)
│       ├── run_all_tasks.py                   # Run & test all 5 tasks
│       ├── session_02_mean_median_mode.ipynb  # Interactive Jupyter Notebook
│       ├── README.md                          # Session 2 task descriptions & answers
│       └── data/
│           └── ipl_player_runs.csv            # Real-world dataset for Task 5
│
├── notebooks/                                 # General exploratory data analysis (EDA)
└── data/                                      # Shared raw and processed datasets
```

---

## 🛠️ Environment Setup

A dedicated Python virtual environment `.venv` is configured with `pandas` and `numpy`.

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

## 📤 How to Upload / Push to GitHub

You have GitHub CLI (`gh`) already installed and authenticated on your machine!

### Option 1: Publish the entire `ds-work` repository (Recommended)

1. Open your terminal in this repository folder (`ds-work`):
   ```powershell
   cd C:\Users\Atharv\.gemini\antigravity-ide\scratch\ds-work
   ```

2. Add all files and make the initial commit:
   ```powershell
   git add .
   git commit -m "feat: complete data science setup with Session 2 assignments"
   ```

3. Create the remote repository on GitHub using GitHub CLI:
   ```powershell
   gh repo create ds-work --public --source=. --remote=origin --push
   ```
   *(Or change `--public` to `--private` if you prefer a private repository).*

4. Done! Your code will be live at:
   `https://github.com/Atharvchaudhari1106/ds-work`

---

### Option 2: Upload the `assignments` folder as its own dedicated GitHub repository

If your instructor or submission portal requires a repository dedicated solely to assignments (e.g. `ds-assignments`):

1. Navigate to the `assignments` folder:
   ```powershell
   cd C:\Users\Atharv\.gemini\antigravity-ide\scratch\ds-work\assignments
   ```

2. Initialize Git in that folder:
   ```powershell
   git init
   git add .
   git commit -m "feat: add Session 2 Mean, Median & Mode assignment"
   ```

3. Push directly to GitHub:
   ```powershell
   gh repo create ds-assignments --public --source=. --remote=origin --push
   ```

4. Your assignment submission link will be:
   `https://github.com/Atharvchaudhari1106/ds-assignments`
