# Data Science Foundations (`Intro to ds`)

This directory contains the complete coursework submissions, interactive Jupyter Notebooks, datasets, and conceptual solutions for the **Intro to Data Science** foundation track.

---

## 📂 Modules & Notebooks Index

| Session | Topic | Key Notebook | Key Deliverables & Focus | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Session 1** | [What is Data Science?](#session-1-what-is-data-science) | [`session_01_what_is_data_science.ipynb`](session_01_what_is_data_science.ipynb) | Daily App Optimization, 3 Pillars of Data Science (no healthcare), Spotify Recommender Scenario, Transportation Innovation (Uber DeepETA & H3). | ✅ Completed (Executed) |
| **Session 2** | [Data Science Lifecycle](#session-2-data-science-lifecycle) | [`session_02_data_science_lifecycle.ipynb`](session_02_data_science_lifecycle.ipynb) | Problem Definition (Zomato), Web API Data Ingestion (`requests`), Spotify Genre Aggregations (`pandas`), BookMyShow Movie Visualizations (`matplotlib`), Advanced Feature Engineering. | ✅ Completed (Executed) |
| **Git Fundamentals** | [Git Installation + Fundamentals](git-installation-fundamentals/README.md) | [`git_installation_fundamentals.ipynb`](git-installation-fundamentals/git_installation_fundamentals.ipynb) | Git CLI Verification, Global Identity, Local Repo Init (`InstaCloneRepo`), Public Cloning (`public-apis`), Semantic Commits (`playlist.txt`). | ✅ Completed (Executed) |
| **Git & GitHub** | [Git & GitHub Collaboration](git-github/README.md) | [`git_github_assignment.ipynb`](git-github/git_github_assignment.ipynb) | Git CLI Verification, Local Repo Init, GitHub Remote Link (`foodie-favorites`), Team Collaboration Simulation & Issue Creation. | ✅ Completed (Executed) |

---

## 📁 Folder Structure
```text
Intro to ds/
├── README.md                                 # Complete track overview & task solutions
├── session_01_what_is_data_science.ipynb     # Session 1 executed notebook (Tasks 1-4)
├── session_02_data_science_lifecycle.ipynb   # Session 2 executed notebook (Tasks 1-5)
├── git-installation-fundamentals/            # Git Installation + Fundamentals module
│   ├── git_installation_fundamentals.ipynb  # Execution & verification notebook
│   └── README.md                             # Step-by-step audit & solutions
├── git-github/                               # Git & GitHub module
│   ├── git_github_assignment.ipynb           # Terminal execution & verification notebook
│   └── README.md                             # Step-by-step audit & solutions
└── data/
    ├── spotify_mini.csv                      # Simulated 12-track Spotify dataset
    └── bookmyshow_movies.csv                 # 12-movie BookMyShow dataset across genres
```

---

## 📌 Session 1 Summary: What is Data Science?

### Primary Topics Covered:
1. **Daily App Telemetry & UX Improvement:** In-depth analysis of Instagram (reels recommendation embeddings), Zomato (quantile ETA & JIT dispatch), and Paytm (sub-50ms fraud anomaly detection).
2. **The Three Pillars of Data Science:** Comparative analysis across Statistics, Programming, and Domain Knowledge with concrete industrial use cases outside healthcare (Amazon, Netflix, Citadel, Uber, Spotify).
3. **Spotify Music Recommendation Scenario:** Context-aware acoustic vector matching and cosine similarity algorithm for morning focus playlists.
4. **Transportation Industry Innovation:** Uber's open-source H3 hierarchical hexagonal spatial indexing and Deep Graph Neural Networks (DeepETA), cutting travel time prediction error by 75.9%.

---

## 📌 Session 2 Summary: Data Science Lifecycle

### Primary Topics Covered:
1. **Problem Definition (Zomato):** Formulating a production-grade machine learning project to tackle peak dinner hour cart abandonment (34%) with defined primary business goals and behavioral/contextual/operational data requirements.
2. **API Data Ingestion via `requests`:** Live ingestion of the latest 5 posts from `https://jsonplaceholder.typicode.com/posts` using `requests.get()` and `response.json()`.
3. **Mini Spotify Dataset & Genre Aggregation:** Loading `data/spotify_mini.csv` into a Pandas DataFrame and computing song frequency distribution across genres (`df['genre'].value_counts()`).
4. **BookMyShow Movie Listings Bar Chart:** Visualizing movie distributions across genres with custom Matplotlib styling and value annotations.
5. **Advanced Feature Engineering on Food Orders:** Creating 3 non-trivial features from `[order_time, restaurant, cuisine, delivery_time, rating]`:
   - `is_peak_meal_rush`: Temporal rush classification capturing kitchen congestion and delivery transit non-linearities.
   - `restaurant_rating_drift`: Exponential moving average differential isolating sudden merchant quality drops.
   - `cuisine_speed_efficiency_ratio`: Normalized transit time relative to median cuisine prep duration, rewarding operational efficiency.

---

## 🛠️ Environment & Execution

Activate the local virtual environment to explore or re-run the notebooks:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Launch Jupyter
jupyter notebook "Intro to ds/session_02_data_science_lifecycle.ipynb"
```
