# Publishing Projects & Building Your Data Science Portfolio

[![Repository](https://img.shields.io/badge/GitHub-my--movie--ratings-181717?style=for-the-badge&logo=github)](https://github.com/Atharvchaudhari1106/my-movie-ratings)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Portfolio-success?style=for-the-badge&logo=github)](https://atharvchaudhari1106.github.io/my-movie-ratings/)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-105.86%20MB%20Tracked-blue?style=for-the-badge&logo=git-lfs)](https://git-lfs.com/)
[![nbdime](https://img.shields.io/badge/nbdime-Diff%20Verified-orange?style=for-the-badge&logo=jupyter)](https://nbdime.readthedocs.io/)

This assignment module documents the end-to-end completion of the **"Publishing Projects & Building Your DS Portfolio"** coursework. It covers professional version control with Git CLI, large-file data management using **Git Large File Storage (Git LFS)**, AST-aware notebook diffing with **`nbdime`**, clean production data science architecture, and public portfolio deployment on **GitHub Pages**.

---

## 📌 Tasks Overview & Verification Matrix

| Task | Requirement | Deliverable | Status & Proof |
| :---: | :--- | :--- | :---: |
| **1** | Create GitHub repo named `my-movie-ratings` and push local notebook (`movie_ratings.ipynb`) using `git init`, `add`, `commit`, `remote add`, `push`. | GitHub Repository [`Atharvchaudhari1106/my-movie-ratings`](https://github.com/Atharvchaudhari1106/my-movie-ratings) | ✅ Verified on GitHub |
| **2** | Add large CSV (>100MB) via Git LFS (`git lfs track`) and explain in `README.md` why raw data files should NOT be uploaded directly to GitHub (privacy, storage, bandwidth). | `data/large_spotify_data.csv` (105.86 MB) tracked in `.gitattributes` | ✅ Verified via Git LFS upload |
| **3** | Install `nbdime` and diff two versions of a notebook (before/after adding IPL player runs plot). Paste diff in `README.md`. | `nbdiff` terminal execution comparing `v1_ipl_runs.ipynb` & `v2_ipl_runs.ipynb` | ✅ Output embedded & verified |
| **4** | Showcase DS work: `analysis.ipynb`, `processed_data.csv`, `plot.png`, `helper_functions.py` (*Constraint: No raw/unprocessed data*). | Clean Bayesian weighted rating pipeline and modular code library | ✅ Fully verified |
| **5** | Build simple GitHub Pages portfolio site with at least 2 project cards ('Instagram Follower Analysis', 'Zomato Restaurant Ratings') & downloadable resume. | Responsive website live on GitHub Pages with 3 project cards & `resume.pdf` | ✅ Live on GitHub Pages |

---

## 🛠️ Task 1: Repository Initialization & Git CLI Workflow

### Local Git Commands Executed
```bash
# 1. Initialize repository with main as default branch
git init -b main

# 2. Stage local Jupyter Notebook
git add movie_ratings.ipynb

# 3. Create initial commit
git commit -m "feat(task1): initialize repository with movie_ratings.ipynb"

# 4. Link remote GitHub repository
git remote add origin https://github.com/Atharvchaudhari1106/my-movie-ratings.git

# 5. Push upstream to main branch
git push -u origin main
```

**Verification:**
- GitHub Repository: [https://github.com/Atharvchaudhari1106/my-movie-ratings](https://github.com/Atharvchaudhari1106/my-movie-ratings)
- Commit SHA: `8984d01`

---

## 📦 Task 2: Git LFS Tracking & Raw Data Engineering Governance

### 1. Implementation
- Git LFS initialized: `git lfs install`
- Large CSV created: `data/large_spotify_data.csv` (**105.86 MB**, simulated Spotify playlist telemetry)
- File tracking rule registered: `git lfs track "data/large_spotify_data.csv"`
- Rule written to `.gitattributes`:
  ```text
  data/large_spotify_data.csv filter=lfs diff=lfs merge=lfs -text
  ```
- Push output confirms LFS upload:
  ```text
  Uploading LFS objects: 100% (1/1), 111 MB | 526 KB/s, done.
  To https://github.com/Atharvchaudhari1106/my-movie-ratings.git
     8984d01..a134a27  main -> main
  ```

### 2. Why Raw Data Files Must NEVER Be Uploaded Directly to GitHub Repos

1. **Storage Bloat & Immutable Git DAG History**:
   - Git operates as a Content-Addressable Storage (CAS) system. When a file is committed, Git stores a compressed snapshot in `.git/objects`.
   - Modifying a 100MB dataset across 5 iterations bloats the internal `.git/` folder to over 500MB.
   - Deleting the file (`git rm raw_data.csv`) only removes it from the *current commit tree*; the 500MB of binary data remains permanently encoded in the commit history. Every developer who ever clones the repository is forced to download gigabytes of dead data.
2. **GitHub Bandwidth Caps & Hard Size Constraints**:
   - GitHub enforces a strict 100MB hard limit per file (`remote: error: GH001: Large files detected`) and flags repositories exceeding 1GB.
   - Bloated repositories drastically increase CI/CD runner build times (GitHub Actions, Docker layer transfers) and saturate network bandwidth.
   - While Git LFS decouples storage by replacing the large payload with a 130-byte pointer file (`oid sha256:...`), free GitHub accounts have a 1GB/month LFS bandwidth quota.
3. **Data Privacy, Governance & Regulatory Compliance (GDPR / HIPAA)**:
   - Raw datasets frequently contain Personally Identifiable Information (PII), unmasked IP addresses, transaction hashes, or proprietary user event streams. Committing raw files exposes data to unauthorized public access and indexing.
   - Under GDPR and CCPA, users possess the "Right to be Forgotten." Removing a single user's record from a raw CSV stored in Git history requires rewriting commit hashes across the entire repository (`git-filter-repo`), breaking all downstream branches and collaborator forks.
4. **Architectural Best Practice**:
   - Decouple code versioning from data storage. Raw data belongs in managed object storage (AWS S3, Google Cloud Storage, or Snowflake/BigQuery) with lifecycle and access control policies.
   - Track reproducible data transformation pipelines using tools like **DVC (Data Version Control)** or **Git LFS**, keeping GitHub repositories lean, secure, and fast.

---

## 🔍 Task 3: Jupyter Notebook Diffing with `nbdime`

### Why `nbdime`?
Standard `git diff` produces illegible, hundreds-of-lines-long JSON syntax diffs when comparing `.ipynb` files due to execution counts, base64 images, and metadata shifts. `nbdime` (Notebook Diff and Merge) understands the underlying notebook structure (cells, source code, outputs, and renderers).

### Demonstration Notebooks
- `v1_ipl_runs.ipynb`: Top 5 all-time IPL run scorers in a Pandas DataFrame.
- `v2_ipl_runs.ipynb`: Added a markdown description and a Matplotlib bar chart visualization.

### Execution Command
```bash
nbdiff v1_ipl_runs.ipynb v2_ipl_runs.ipynb
```

### Exact Terminal Output Pasted from `nbdiff`
```diff
nbdiff v1_ipl_runs.ipynb v2_ipl_runs.ipynb
--- v1_ipl_runs.ipynb  2026-10-24 14:22:16.026919
+++ v2_ipl_runs.ipynb  2026-10-24 14:22:16.026919
## inserted before /cells/2:
+  markdown cell:
+    source:
+      ## Visualization: Top IPL Run Scorers
+      Bar plot showing total IPL career runs.
+  code cell:
+    execution_count: 2
+    source:
+      import matplotlib.pyplot as plt
+      
+      fig, ax = plt.subplots(figsize=(8, 4))
+      ax.bar(df['Player'], df['Runs'], color='#F59E0B')
+      ax.set_ylabel('Total Runs')
+      ax.set_title('Top 5 All-Time IPL Run Scorers')
+      plt.xticks(rotation=20)
+      plt.show()
+    outputs:
+      output 0:
+        output_type: display_data
+        data:
+          text/plain: <Figure size 800x400 with 1 Axes>
```

---

## 🔬 Task 4: Data Science Work Showcase (No Raw Data)

### Constraint Checklist
- [x] **No raw or unprocessed datasets included in repository.**
- [x] Processed dataset (`processed_data.csv`) is clean, normalized, and feature-engineered.
- [x] Python helper script (`helper_functions.py`) is modular and reusable.
- [x] Plot artifact (`plot.png`) is high-resolution (150 DPI) with dual series comparison.
- [x] Analysis notebook (`analysis.ipynb`) includes narrative, mathematical formulation, and visual validation.

### Core Mathematical Formula (IMDb Weighted Bayesian Score)
$$\text{WR} = \left(\frac{v}{v + m}\right) R + \left(\frac{m}{v + m}\right) C$$

Where:
- $R$ = Observed movie rating
- $v$ = Total vote count for the movie
- $m$ = Minimum threshold votes required ($m = 15,000$)
- $C$ = Mean rating across the entire dataset ($C = 8.59$)

---

## 🌐 Task 5: GitHub Pages Portfolio Site & Downloadable Resume

### Live Deployment
- **Live Site**: [https://atharvchaudhari1106.github.io/my-movie-ratings/](https://atharvchaudhari1106.github.io/my-movie-ratings/)
- **Downloadable Resume**: [`resume.pdf`](file:///C:/Users/Atharv/.gemini/antigravity-ide/scratch/my-movie-ratings/resume.pdf) / [Direct Link](https://atharvchaudhari1106.github.io/my-movie-ratings/resume.pdf)

### Project Cards Showcased
1. **Instagram Follower & Reach Analysis**: End-to-end data pipeline analyzing Reels dwell time, engagement conversion funnels, and demographic reach distributions.
2. **Zomato Restaurant Ratings & Delivery Optimization**: Machine learning engine estimating 85th-percentile kitchen prep times ($T_{\text{prep}}$) and courier dispatch routing.
3. **Movie Ratings Intelligence & Bayesian Recommender**: Bayesian shrinkage estimator correcting small-sample rating bias.

---

## 📂 Submission Notebooks

- [`publishing_projects_ds_portfolio.ipynb`](publishing_projects_ds_portfolio.ipynb): Complete executed verification notebook with all outputs, commands, and visual artifacts.
