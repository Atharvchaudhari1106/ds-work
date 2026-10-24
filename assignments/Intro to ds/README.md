# Session 1: What is Data Science? (Intro to DS)

This folder contains the complete coursework submission and solutions for **Session 1: What is Data Science? (Intro to DS)**.

---

## 📓 Primary Assignment Notebook
👉 [**`session_01_what_is_data_science.ipynb`**](session_01_what_is_data_science.ipynb)

All code cells are fully pre-executed with interactive Pandas DataFrames, summary statistics, and embedded visualizations.

---

## 📋 Comprehensive Assignment Solutions

### Task 1: 3 Daily Apps & Data-Driven Experience Improvement
*List 3 apps you use daily (such as Instagram, Zomato, Paytm) and describe one way each app uses data to improve your experience.*

| App | Domain | Data Captured & Tracked | Analytical / ML Engine | User Experience Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Instagram** | Social Media & Video | Dwell time per Reel (ms), scroll velocity, sound saves, DM shares, like/comment graph. | Graph Neural Networks (GNNs), Two-Tower vector embeddings, multi-task ranking. | **Personalized Explore & Reels Feed:** Synthesizes billions of items in real-time, matching visual and audio embeddings to user micro-tastes to eliminate search friction. |
| **Zomato** | Food Delivery & Quick Commerce | Historical kitchen prep time, live courier GPS telemetry, hyperlocal weather conditions, road traffic congestion. | Quantile Gradient Boosted Regression & Spatial-Temporal Dispatch Optimization. | **Hyper-Accurate Dynamic ETA & JIT Kitchen Dispatch:** Computes 85th percentile prep times so couriers arrive exactly when meals are bagged, ensuring piping-hot food and predictable delivery times. |
| **Paytm** | Digital Payments & Fintech (UPI) | Transaction velocity, IP geofencing, device biometrics, merchant category code (MCC), account age. | Real-Time Anomaly Detection & High-Throughput Risk Scoring (<50ms). | **Zero-Friction Fast-Pay & Instant Fraud Safeguard:** Frequent local QR payments get instant one-tap approvals, while suspicious transfers trigger immediate step-up biometric verification. |

---

### Task 2: The Three Pillars of Data Science
*Create a table with three columns: Statistics, Programming, and Domain Knowledge. For each column, write 2 specific skills or concepts that are important for a Data Scientist and give a real-world example (not from healthcare) of how each is used.*

| Pillar Concept | Statistics | Programming | Domain Knowledge |
| :--- | :--- | :--- | :--- |
| **Skill / Concept 1** | **A/B Hypothesis Testing & Significance** ($p$-values, Two-sample $t$-test, Type I/II error control). | **Vectorized Data Wrangling & Transformations** (Python, Pandas, NumPy, SQL window functions). | **Unit Economics & SaaS Growth Funnels** (LTV, CAC, Churn Velocity, Cohort Retention). |
| **Real-World Example 1** | *E-Commerce (Amazon):* Testing whether a redesigned one-click checkout button yields a statistically significant conversion lift ($p < 0.05$) rather than random variance before global rollout. | *Quantitative Finance & Algorithmic Trading:* Ingesting and transforming millions of raw tick-by-tick order-book rows per second to calculate rolling Volume-Weighted Average Price (VWAP) in sub-milliseconds. | *Subscription Streaming (Spotify):* Recognizing that high user signups are unprofitable if 60-day cohort churn is 40%; formulating pre-churn survival models before free trials end. |
| **Skill / Concept 2** | **Probability Distributions & Poisson Processes** (Inhomogeneous Poisson modeling, Pareto distributions). | **Production Scripting, API Microservices & CI/CD** (FastAPI, Docker, Git, REST/gRPC endpoints). | **Marketplace Liquidity & Spatial Elasticity** (Supply-Demand Bottlenecks, Surge Multipliers). |
| **Real-World Example 2** | *Cloud Infrastructure (Netflix / AWS):* Modeling concurrent stream arrival spikes as a Poisson process to automatically provision server clusters ahead of major show premieres. | *Ride-Hailing (Uber):* Wrapping trained dynamic pricing and route matching models into containerized microservices returning surge rates to mobile apps in <80ms. | *Logistics & Food Delivery (Swiggy / Ola):* Recognizing that monsoon storms cause severe driver supply deficits; formulating localized incentive multipliers to attract couriers to high-demand clusters. |

---

### Task 3: Spotify Song Recommendation Scenario
*Imagine you work for a music streaming app like Spotify. Write a short scenario (3-4 sentences) describing how data-driven decision making could help the app recommend new songs to users.*

> **Scenario:**  
> *"At Spotify, when our telemetry detects that a listener consistently skips upbeat EDM and pop tracks after ten seconds during weekday morning commutes while completing 95% of lo-fi and acoustic instrumental songs, our recommendation engine flags these behavioral signals as strong implicit preferences for a calming morning acoustic session. By synthesizing high-dimensional audio embeddings—specifically filtering for low tempo, high acousticness, and relaxed valence—with co-listening matrix factorization from similar commuter cohorts, the platform maps the listener's exact contextual state. Rather than defaulting to static global top-40 charts, our data-driven decision pipeline curates an individualized 'Morning Focus' playlist featuring unfamiliar independent lo-fi producers whose acoustic vectors match the user's high-retention tracks. This algorithmic feedback loop systematically eliminates decision fatigue for the listener, drives organic discovery for emerging artists, and maximizes long-term user retention."*

---

### Task 4: Innovative Industry Application — Transportation & Mobility
*Pick one industry from this list: e-commerce, sports, or transportation. Research and describe one innovative way data science is being used in that industry today.*

- **Selected Industry:** Transportation & Mobility Networks (e.g., Uber, Waymo)
- **Innovative Technology:** Deep Graph Neural Networks (**DeepETA**) combined with **Uber H3 Hierarchical Hexagonal Spatial Indexing**
- **Detailed Mechanics:**
  1. **H3 Hexagonal Spatial Indexing:**  
     Traditional square grids distort distance measurements because diagonal neighbors are $\approx 1.414\times$ farther than orthogonal neighbors. Uber's open-source H3 library tessellates the planet into discrete hexagons, ensuring that every neighboring cell is equidistant. This enables smooth spatial convolution for hyperlocal demand forecasting without directional distortion.
  2. **DeepETA (Graph Neural Networks with Attention):**  
     Road networks are modeled as dynamic directed graphs where road segments are edges and intersections are nodes. DeepETA applies spatial-temporal graph attention to model how traffic bottlenecks ripple across city networks, dropping arrival time estimation errors from 6.0 minutes (traditional static Dijkstra routing) down to **1.45 minutes** (a **75.9% error reduction**).
  3. **Predictive Fleet Repositioning:**  
     By correlating live airport arrivals, transit timetables, and venue events, reinforcement learning models reposition idle vehicles into anticipated demand hot-zones 20–30 minutes in advance, slashing rider wait times and deadhead fuel waste.

---

## 🛠️ Verification & Execution

To re-run or inspect the notebook using the project's virtual environment:

```powershell
# Activate the project venv
.\.venv\Scripts\Activate.ps1

# Run Jupyter or inspect notebook
jupyter notebook "Intro to ds/session_01_what_is_data_science.ipynb"
```
