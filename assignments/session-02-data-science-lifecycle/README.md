# Session 2: Data Science Lifecycle

This directory contains the complete coursework submission and solutions for **Session 2 - Data Science Lifecycle**.

---

## 📓 Primary Interactive Notebook
👉 [**`session_02_data_science_lifecycle.ipynb`**](session_02_data_science_lifecycle.ipynb)

All 5 tasks are fully pre-executed with API calls, interactive Pandas DataFrames, and Matplotlib visualizations.

---

## 📂 Session Structure
```text
├── session_02_data_science_lifecycle.ipynb   # Main interactive notebook (All 5 tasks executed)
├── README.md                                 # Complete documentation & conceptual solutions
└── data/
    ├── spotify_mini.csv                      # Simulated 12-row Spotify dataset for Task 3
    └── bookmyshow_movies.csv                 # 12-movie BookMyShow dataset for Task 4
```

---

## 📋 Comprehensive Assignment Solutions

### Task 1: Problem Definition for a Daily App (Zomato)
- **Selected App:** **Zomato** (Food Delivery & Quick Commerce)
- **Problem Definition:** During peak dinner hours (7:30 PM – 9:30 PM), users encounter cognitive decision paralysis from infinite menu scrolling, causing a **34% cart abandonment rate** when unexpected delivery delays appear at final checkout.
- **Business Goal:**
  - Reduce dinner-hour cart abandonment by **15%**.
  - Increase checkout conversion rate from 18% to **24%**.
  - Cut user median time-to-order from 7.2 minutes to **under 3.5 minutes** with context-aware smart meal recommendations.
- **Data Required:**
  1. *User Behavioral History:* Past order frequencies, dish re-order cycles, typical spend per order, dietary restrictions.
  2. *Real-Time Contextual Signals:* Timestamp, device GPS geofence, live rainfall/weather index, local traffic velocity.
  3. *Restaurant & Operational Metrics:* Live kitchen prep backlog, active courier availability density within a 3.5km radius, 85th percentile preparation time.

---

### Task 2: Fetching REST API Data with `requests`
- **Target URL:** `https://jsonplaceholder.typicode.com/posts`
- **Methodology:** Used `requests.get()` with timeout and `response.json()` to parse the payload and extract the latest 5 posts:
```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url, timeout=10)
posts = response.json()[:5]

for i, post in enumerate(posts, 1):
    print(f"Post {i}: {post['title']}")
```
- **Live Output Fetched:**
  1. *Post 1:* `sunt aut facere repellat provident occaecati excepturi optio reprehenderit`
  2. *Post 2:* `qui est esse`
  3. *Post 3:* `ea molestias quasi exercitationem repellat qui ipsa sit aut`
  4. *Post 4:* `eum et est occaecati`
  5. *Post 5:* `nesciunt quas odio`

---

### Task 3: Mini Spotify Dataset & Genre Aggregation (`pandas`)
- **Simulated CSV:** Located at [`data/spotify_mini.csv`](data/spotify_mini.csv) with columns: `song_name`, `artist`, `streams`, `genre` (12 rows).
- **Genre Song Counts:**
  - **Rock:** 3 songs (*Believer*, *Smells Like Teen Spirit*, *Bohemian Rhapsody*)
  - **Hip-Hop:** 3 songs (*God's Plan*, *HUMBLE.*, *Sunflower*)
  - **R&B / Pop:** 2 songs (*Starboy*, *Blinding Lights*)
  - **Pop:** 2 songs (*Shape of You*, *Levitating*)
  - **Classical:** 2 songs (*Clair de Lune*, *Experience*)

---

### Task 4: Movie Listings Bar Chart (`matplotlib`)
- **Dataset:** 12 trending Indian theatrical releases on BookMyShow across Bollywood, Tollywood, and Mollywood.
- **Visualization:** A styled categorical bar chart depicting movie frequencies per broad genre with exact count annotations above each bar.

---

### Task 5: Feature Engineering for Online Food Orders
Given existing columns: `[order_time, restaurant, cuisine, delivery_time, rating]`:

1. **`is_peak_meal_rush` / `meal_period` (Categorical/Binary Temporal Feature):**
   - *Formula:* Classified as `Lunch Rush` (12:30–14:30), `Dinner Rush` (19:30–22:00), `Late Night` (23:00–04:00), or `Off-Peak`.
   - *Model Benefit:* Delivery transit time does not scale linearly with time of day. Kitchen backlog and courier scarcity spike during rush windows. This allows regression models to capture traffic wave nonlinearities and drastically improve ETA accuracy.

2. **`restaurant_rating_drift` (Numerical Differential Signal):**
   - *Formula:* $\Delta_{\text{Rating}} = \text{rating}_{\text{order}} - \overline{\text{rating}}_{\text{restaurant, 30-day EWM}}$
   - *Model Benefit:* Customer ratings are subjective; a 4.0 star review is a steep penalty for a 4.9-star luxury outlet, but high praise for a 3.2-star quick stall. Rating drift normalizes restaurant baseline prestige, creating an immediate leading indicator of merchant quality degradation in churn prediction models.

3. **`cuisine_speed_efficiency_ratio` (Normalized Efficiency Metric):**
   - *Formula:* $\text{Ratio} = \frac{\text{delivery\_time}}{\text{Median}(\text{delivery\_time}_{\text{cuisine}})}$
   - *Model Benefit:* Different cuisines have completely different cooking physics (e.g., slow-dum Biryani takes 30 min prep, while ice creams or burgers take 6 min). Normalizing by cuisine category allows recommendation and search ranking algorithms to identify and promote restaurants that operate faster than their culinary peers.
