# Git Installation + Fundamentals Assignment Submission

This folder contains the complete coursework submission and terminal audit log for the **Git Installation + Fundamentals** module.

---

## 📓 Interactive Notebook & Audit Log
👉 [**`git_installation_fundamentals.ipynb`**](git_installation_fundamentals.ipynb)

---

## 📋 Task-by-Task Solutions & Terminal Outputs

### Task 1: Verify Git Installation
- **Terminal Command:**
  ```bash
  git --version
  ```
- **Console Output:**
  ```text
  git version 2.55.0.windows.5
  ```

---

### Task 2: Configure Global Git Username and Email
- **Commands Executed:**
  ```bash
  git config --global user.name "Atharv Chaudhari"
  git config --global user.email "atharvchaudhari1106@users.noreply.github.com"
  ```
- **Verification:**
  - `git config --global user.name` -> `Atharv Chaudhari`
  - `git config --global user.email` -> `atharvchaudhari1106@users.noreply.github.com`

---

### Task 3: Initialize `InstaCloneRepo` & Observe `.git` Folder
- **Commands Executed:**
  ```bash
  mkdir InstaCloneRepo && cd InstaCloneRepo
  git init
  ```
- **Output:**
  ```text
  Initialized empty Git repository in C:/Users/Atharv/.gemini/antigravity-ide/scratch/InstaCloneRepo/.git/
  ```
- **Observation of the `.git` Directory:**
  The `.git` folder is a hidden administrative directory that holds Git's entire database and internal plumbing:
  - `HEAD`: Points to the branch currently checked out (`ref: refs/heads/master`).
  - `config`: Stores repository-specific configuration options.
  - `description`: Used by GitWeb.
  - `hooks/`: Contains client-side git hooks (pre-commit, post-commit sample scripts).
  - `info/`: Contains repository-level exclusion rules (`info/exclude`).
  - `objects/`: Content-addressable object store storing compressed Git blobs, trees, commits, and tags.
  - `refs/`: Stores commit hash references for local branch tips (`refs/heads/`) and tags.

---

### Task 4: Clone Public Repository (`public-apis`) & Inspect `git status`
- **Command:**
  ```bash
  git clone https://github.com/public-apis/public-apis.git
  cd public-apis
  git status
  ```
- **Console Output:**
  ```text
  On branch master
  Your branch is up to date with 'origin/master'.

  nothing to commit, working tree clean
  ```
- **Description of What We See:**
  1. `On branch master`: We are working on the default primary branch (`master`).
  2. `Your branch is up to date with 'origin/master'`: The local branch pointer matches the remote GitHub repository pointer with zero ahead/behind difference.
  3. `nothing to commit, working tree clean`: There are no unstaged modifications, staged changes, or untracked files. The working directory perfectly matches the latest commit state.

---

### Task 5: Create, Stage & Commit `playlist.txt` in `InstaCloneRepo`
- **File Created:** `InstaCloneRepo/playlist.txt` with contents:
  ```text
  1. Starboy - The Weeknd
  2. Blinding Lights - The Weeknd
  3. Levitating - Dua Lipa
  ```
- **Commands Executed:**
  ```bash
  git add playlist.txt
  git commit -m "feat(audio): add initial playlist with 3 trending tracks"
  ```
- **Commit Confirmation:**
  ```text
  [master (root-commit) db5af95] feat(audio): add initial playlist with 3 trending tracks
   1 file changed, 3 insertions(+)
   create mode 100644 playlist.txt
  ```
- **Commit Message Rationale:**
  Follows industry-standard Conventional Commits syntax (`feat(scope): imperative summary`), providing clear context as if operating on a production music app codebase.
