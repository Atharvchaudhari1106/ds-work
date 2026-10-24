# Git Branching & Collaboration Assignment Submission

This folder contains the complete coursework submission and terminal audit log for the **Git Branching & Collaboration** module.

---

## 📓 Interactive Notebook & Audit Log
👉 [**`git_branching_collaboration.ipynb`**](git_branching_collaboration.ipynb)

---

## 🔗 Live GitHub Artifacts
- **Forked Repository:** [https://github.com/Atharvchaudhari1106/Zomato-Cleaning-and-Visualization](https://github.com/Atharvchaudhari1106/Zomato-Cleaning-and-Visualization)
- **Live Upstream Pull Request (#1):** [https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1](https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1)
- **Classmate Review Request Comment:** [https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1#issuecomment-6382092688](https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1#issuecomment-6382092688)

---

## 📋 Task-by-Task Solutions & Terminal Outputs

### Task 1: Create `feature-playlist` Branch & Add `playlist.md`
- **Commands Executed:**
  ```bash
  git checkout -b feature-playlist
  # Created playlist.md describing Top 3 Spotify playlists
  git add playlist.md
  git commit -m "feat(playlist): add curated top 3 Spotify playlists"
  ```
- **Commit Hash:** `fd64fe7`

---

### Task 2: Non-Fast-Forward Merge & Conflict Resolution Walkthrough
1. **Merge `--no-ff`:**
   ```bash
   git checkout main
   git merge --no-ff feature-playlist -m "Merge branch 'feature-playlist' into main (non-fast-forward)"
   ```
2. **Intentional Conflict Creation:**
   - Modified line 4 of `playlist.md` on `main` to daily viral chart updates (`1bc24f0`).
   - Modified line 4 of `playlist.md` on `feature-playlist` to weekly algorithmic filters (`4cc01cd`).
   - Merging triggered:
     ```text
     CONFLICT (content): Merge conflict in playlist.md
     Automatic merge failed; fix conflicts and then commit the result.
     ```
3. **Conflict Resolution:**
   Synthesized both enhancements into a unified line:
   ```markdown
   1. **Today's Top Hits:** Synthesized hybrid feed featuring dynamic daily viral chart updates and weekly algorithmic recommendation filters.
   ```
   Committed resolution (`559f0d5`) and pushed to remote origin.

---

### Task 3: Fork Public Data Science Repo & Create `feature-zomato-analysis`
- **Forked Repository:** `danyadanish/Zomato-Cleaning-and-Visualization`
- **Branch Created:** `feature-zomato-analysis`
- **Added `zomato_analysis.txt`:**
  > *"I would analyze Zomato order data by applying quantile regression to predict 85th-percentile kitchen preparation times and geospatial clustering to optimize courier dispatch zones during peak dinner rush."*
- **Commit:** `a4732b9`

---

### Task 4: Push to Fork & Open Pull Request (PR)
- **Branch Pushed:** `git push -u origin feature-zomato-analysis`
- **Opened Pull Request:** [https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1](https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1)
- **Added Review Request Comment:** [https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1#issuecomment-6382092688](https://github.com/danyadanish/Zomato-Cleaning-and-Visualization/pull/1#issuecomment-6382092688)

---

### Task 5: AI-Generated Constructive PR Review Comment
```markdown
"Hey @teammate, great work on adding the new plot_customer_retention_cohorts() visualization function! The heatmap color gradient makes retention drop-offs immediately recognizable, and modularizing the matplotlib axis formatting keeps the codebase very clean.

A few constructive suggestions before we merge:
1. Dynamic Scaling: Consider parameterizing figsize or adding tight_layout(pad=1.5) so tick labels don't get truncated when rendered in standard Jupyter notebook views on varying screen resolutions.
2. Null Handling: If an early cohort month has zero active users, seaborn.heatmap might render NaN squares—passing mask=cohort_matrix.isnull() or an explicit zero fill will make the plotting function much more resilient against sparse datasets.
3. Docstring & Type Annotations: Adding a concise docstring with an example call and type annotations (e.g., cohort_data: pd.DataFrame, metric: str = 'retention' -> plt.Axes) will make it much easier for the rest of the team to integrate this function into our production reporting dashboards.

Overall, this is a super valuable addition to our analytics pipeline. Once these minor points are addressed, happy to give this my full approval! 🚀"
```
