# Professional Project Structure for DA/DS

This folder contains the complete coursework submission and architectural verification audit for the **Professional Project Structure for DA/DS** module.

---

## 📓 Interactive Notebook & Audit Log
👉 [**`professional_project_structure.ipynb`**](professional_project_structure.ipynb)

---

## 📋 Task-by-Task Solutions & Deliverables

### Task 1: Data Analytics Project Structure (`insta-analytics`)
- **Root Directory:** [`insta-analytics/`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/insta-analytics)
- **Directory Layout:**
  ```text
  insta-analytics/
  ├── .gitignore
  ├── README.md
  ├── data/
  │   ├── raw/
  │   │   └── sample_instagram_reach.csv      # Sample telemetry CSV
  │   └── processed/
  ├── notebooks/
  │   └── 01_exploratory_data_analysis.ipynb   # Sample Jupyter notebook
  ├── scripts/
  ├── dashboards/
  └── reports/
  ```

---

### Task 2: Machine Learning Project Structure (`ml-project`)
- **Root Directory:** [`ml-project/`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ml-project)
- **Verified Subfolder Layout with Dummy Files:**
  ```text
  ml-project/
  ├── README.md                          # Production model documentation
  ├── data/
  │   └── dummy_data.txt                 # Dummy text file
  ├── src/
  │   └── dummy_src.txt                  # Dummy text file
  ├── notebooks/
  │   └── dummy_notebook.txt             # Dummy text file
  ├── models/
  │   └── dummy_model.txt                # Dummy text file
  └── saved_artifacts/
      └── dummy_artifact.txt             # Dummy text file
  ```

---

### Task 3: Targeted `.gitignore` for `insta-analytics`
Location: [`insta-analytics/.gitignore`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/insta-analytics/.gitignore)
```gitignore
# 1. Ignore all files in data/raw
data/raw/*
!data/raw/.gitkeep

# 2. Ignore any .ipynb_checkpoints folders
**/.ipynb_checkpoints/
.ipynb_checkpoints/

# 3. Ignore model weights and pickled artifacts (.h5 and .pkl)
*.h5
*.pkl
**/*.h5
**/*.pkl

# Python standard exclusions
__pycache__/
*.py[cod]
.venv/
```

---

### Task 4: Professional `README.md` for `Spotify Song Popularity Predictor`
Location: [`ml-project/README.md`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/ml-project/README.md)
- **Project Summary:** Formulation of supervised regression pipeline predicting track popularity scores ($0–100$) from acoustic features.
- **Dataset Reference Placeholder:** Link to Kaggle Spotify 1.2M+ track catalog with schema specification.
- **Setup & Installation:** Step-by-step virtual environment creation and pip dependency installation list (`pandas`, `scikit-learn`, `xgboost`, `fastapi`).
- **Results & Visuals:** Comparative model performance table ($R^2$, RMSE, MAE) and ASCII SHAP feature importance plot.

---

### Task 5: Open-Source Project Audit (`facebook/prophet`)
- **Cloned Repository:** `https://github.com/facebook/prophet` (Meta's time series forecasting package).
- **Directory Audit:**
  1. *Follows:* Dedicated `notebooks/` directory isolating demonstration tutorials (`quick_start.ipynb`, `diagnostics.ipynb`) from source libraries.
  2. *Differs:* No `data/raw/` vs. `data/processed/` pipeline structure; sample time series are embedded inside unit test fixtures.
  3. *Differs:* Polyglot layout split into `python/` and `R/` root trees without dedicated `models/` or `saved_artifacts/` folders because it is an algorithm library rather than an operationalized model service.
- **Suggested Improvement:** Decouple tutorial datasets into a top-level `data/` directory with an automated download script (`scripts/download_sample_datasets.py`) to reduce setup barriers for new practitioners.
