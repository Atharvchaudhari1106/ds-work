# Git & GitHub Assignment Submission

This folder contains the complete coursework submission and terminal audit log for the **GIT-GITHUB** module.

---

## 📓 Interactive Notebook & Audit Log
👉 [**`git_github_assignment.ipynb`**](git_github_assignment.ipynb)

---

## 🔗 Live GitHub Artifacts
- **Remote Repository:** [https://github.com/Atharvchaudhari1106/foodie-favorites](https://github.com/Atharvchaudhari1106/foodie-favorites)
- **Created GitHub Issue (#1):** [https://github.com/Atharvchaudhari1106/foodie-favorites/issues/1](https://github.com/Atharvchaudhari1106/foodie-favorites/issues/1)

---

## 📋 Task-by-Task Solutions & Terminal Outputs

### Task 1: Verify Git Installation
- **Command:** `git --version`
- **Output:** `git version 2.55.0.windows.5`

### Task 2: Initialize Local Git Repository (`music-recommendation`)
- **Commands Executed:**
  ```bash
  mkdir music-recommendation && cd music-recommendation
  git init -b main
  # Created README.md
  git add README.md
  git commit -m "Initial commit for music-recommendation project"
  ```
- **Commit Hash:** `2d1c2bd`

### Task 3: Remote Repository (`foodie-favorites`) & Upstream Push
- **Commands Executed:**
  ```bash
  gh repo create foodie-favorites --public --description "Foodie Favorites & Music Recommendation Project"
  git remote add origin https://github.com/Atharvchaudhari1106/foodie-favorites.git
  git push -u origin main
  ```
- **Live Remote:** Connected to `https://github.com/Atharvchaudhari1106/foodie-favorites.git`

### Task 4: Team Collaboration Simulation
1. **Added `Top 3 Music Apps` to `README.md`:**
   - Spotify
   - YouTube Music
   - Wynk Music
2. **Committed and Pushed:**
   ```bash
   git add README.md
   git commit -m "docs: add Top 3 Music Apps section"
   git push origin main
   ```
   *(Commit: `ceb7230`)*
3. **Created GitHub Issue:**
   - Title: `Add playlist sharing`
   - URL: [https://github.com/Atharvchaudhari1106/foodie-favorites/issues/1](https://github.com/Atharvchaudhari1106/foodie-favorites/issues/1)

### Task 5: Avoiding Notebook Versioning Chaos (3–4 Line Note)
> *"Using Git provides a centralized, cryptographic commit history where each change is recorded as a clean snapshot under a single, canonical filename (`analysis.ipynb`), completely eliminating filename clutter like `analysis_v1.ipynb` or `analysis_final2.ipynb`.*  
> *Through isolated Git feature branches, data scientists can independently test speculative machine learning models or data cleaning transformations without risking corruption of the primary working codebase.*  
> *GitHub acts as an immutable cloud audit trail with visual cell-by-cell diffs, enabling teams to trace exact historical model performance, review pull requests collaboratively, and seamlessly roll back breaking bugs using a single command (`git revert` / `git checkout`)."*
