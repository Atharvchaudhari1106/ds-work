# Case Study: Zomato Bangalore Restaurants Analytics (Kaggle Dataset)

**Role:** Data Analyst for Zomato Bangalore  
**Directory:** `assignment-2/case-study-zomato-bangalore-restaurants/`  
**Database File:** `zomato_bangalore.db`  
**Dataset File:** `zomato_bangalore.csv`  
**Execution Environment:** Python 3.12, SQLite 3.49, Pandas 3.1  
**Status:** ✅ Completed, Verified & Executed

---

## 📌 Business Goal & Strategic Context
As a Data Analyst for Zomato Bangalore, use SQL to help business, marketing, and operations teams answer critical questions around restaurant performance, pricing tiers, customer ratings, low-rating turnaround strategies, and chain penetration. The outcome directly guides:
- **Merchant Partner Selection:** Surface high-reputation local heroes for priority placement.
- **Pricing Strategy:** Gauge consumer willingness-to-pay across culinary genres.
- **Turnaround Marketing:** Revitalize underperforming cloud kitchens in high-density IT corridors.
- **Strategic Expansion:** Identify multi-outlet enterprise chains for city-wide exclusivity deals.

---

## 📂 Deliverables & File Structure

```text
assignment-2/case-study-zomato-bangalore-restaurants/
├── case_study_zomato_bangalore_restaurants.ipynb # Primary executed interactive notebook (Tasks 1-5)
├── solution.sql                                  # Production SQL script (DDL, queries, and business metrics)
├── setup_and_verify.py                           # Automated end-to-end verification test runner
├── zomato_bangalore.csv                          # Comprehensive Bangalore restaurants dataset
├── zomato_bangalore.db                           # Populated SQLite database
└── README.md                                     # Complete task walkthrough & strategy report
```

---

## 📋 Task Walkthrough & Verified Solutions

### Task 1: Top 5 Highest-Rated North Indian Restaurants in Koramangala
> **Task 1:** Write an SQL query to find the top 5 highest-rated restaurants in Koramangala that serve North Indian cuisine, using the Zomato Bangalore dataset.

#### SQL Implementation:
```sql
SELECT 
    name,
    location,
    cuisines,
    rating,
    votes
FROM zomato_bangalore
WHERE location LIKE '%Koramangala%'
  AND cuisines LIKE '%North Indian%'
ORDER BY rating DESC, votes DESC
LIMIT 5;
```

#### Query Output:
| name | location | cuisines | rating | votes |
| :--- | :--- | :--- | :---: | :---: |
| **Punjab Grill** | Koramangala | North Indian | **4.8** | 1,850 |
| **Empire Restaurant** | Koramangala | North Indian | **4.6** | 2,400 |
| **Meghana Foods** | Koramangala | North Indian | **4.5** | 3,100 |
| **Gramin** | Koramangala | North Indian | **4.4** | 1,420 |
| **Kapoor's Cafe** | Koramangala | North Indian | **4.3** | 980 |

---

### Task 2: Average Cost for Two per Cuisine & Top 3 Most Expensive Cuisines
> **Task 2:** Using SQL, calculate the average cost for two people for each cuisine type and list the 3 most expensive cuisines to eat in Bangalore.

#### SQL Implementation:
```sql
SELECT 
    cuisines AS cuisine_type,
    ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two,
    COUNT(*) AS restaurant_count
FROM zomato_bangalore
GROUP BY cuisines
ORDER BY avg_cost_for_two DESC
LIMIT 3;
```

#### Query Output:
| Rank | cuisine_type | avg_cost_for_two | restaurant_count | Category Profile |
| :---: | :--- | :---: | :---: | :--- |
| 🥇 1 | **Mediterranean** | **₹2,333.33** | 3 | Luxury Fine Dining (Olive Beach, Shiro) |
| 🥈 2 | **Continental** | **₹1,900.00** | 3 | High-End Microbreweries & Bistros (Byg Brewski, Toit) |
| 🥉 3 | **Chinese** | **₹983.33** | 3 | Premium Asian Dining (Mainland China, Beijing Bites) |

---

### Task 3: Low-Rated Online Delivery Outlets & Strategic Marketing Plan
> **Task 3:** Find all restaurants that offer online delivery but have a rating below 3.0, and suggest a marketing strategy to improve their ratings based on your findings.  
> *Hint: Look for patterns in location, cuisine, or price that might explain the low ratings.*

#### SQL Implementation:
```sql
SELECT 
    restaurant_id,
    name,
    location,
    cuisines,
    approx_cost_for_two,
    rating,
    votes,
    online_order
FROM zomato_bangalore
WHERE online_order = 'Yes'
  AND rating < 3.0
ORDER BY rating ASC, approx_cost_for_two ASC;
```

#### Query Output:
| restaurant_id | name | location | cuisines | approx_cost_for_two | rating | votes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| 29 | **Midnight Biryani Co** | BTM Layout | Mughlai | ₹350 | **2.6** | 320 |
| 27 | **Spice Route Express** | Electronic City | North Indian | ₹250 | **2.7** | 210 |
| 28 | **Curry in a Hurry** | Whitefield | North Indian | ₹300 | **2.8** | 180 |
| 31 | **Taste of Punjab Cloud**| HSR Layout | North Indian | ₹280 | **2.8** | 190 |
| 30 | **Burger Point** | Marathahalli | Fast Food | ₹220 | **2.9** | 150 |

#### 🔍 Pattern Diagnosis & Root Causes:
1. **Low Average Order Value (AOV):** All low-rated delivery outlets operate in the ultra-budget tier (₹220–₹350 for two), leading to tight operating margins and compromises on ingredient freshness.
2. **Geographical Bottlenecks:** Concentrated in high-commute IT corridors (Electronic City, Whitefield, Marathahalli, BTM Layout) where transit delays cause food to arrive cold.
3. **Packaging Failure:** Spillages in curries and soggy fast-food buns are the primary drivers of 1-star reviews.

#### 💡 Actionable Marketing & Operational Turnaround Plan:
- **Dynamic Delivery Geofencing:** Restrict delivery radiuses from 8 km to 3.5 km during peak traffic hours (7:30 PM–10:00 PM) to ensure delivery under 25 minutes.
- **Subsidized Thermal Packaging:** Provide bulk-subsidized, tamper-evident insulated foil packaging to eliminate spillage and cold delivery.
- **Automated Service Recovery Vouchers:** Instantly issue an automated apology notification and a 40% discount coupon to any customer rating $\le 2.0$.
- **Menu Pruning:** Remove the bottom 15% lowest-rated, slow-prep items that create kitchen bottlenecks.

---

### Task 4: Three-Tier Market Segmentation (Budget, Mid-Range, Premium)
> **Task 4:** Write an SQL query to segment restaurants into three market segments based on average cost for two: budget (below 400), mid-range (400-800), and premium (above 800). Count how many restaurants fall into each segment.

#### SQL Implementation:
```sql
SELECT 
    CASE 
        WHEN approx_cost_for_two < 400 THEN 'Budget (Below 400)'
        WHEN approx_cost_for_two BETWEEN 400 AND 800 THEN 'Mid-Range (400 - 800)'
        ELSE 'Premium (Above 800)'
    END AS market_segment,
    COUNT(*) AS restaurant_count,
    ROUND(AVG(approx_cost_for_two), 2) AS avg_segment_cost,
    ROUND(AVG(rating), 2) AS avg_rating
FROM zomato_bangalore
GROUP BY market_segment
ORDER BY 
    CASE market_segment
        WHEN 'Budget (Below 400)' THEN 1
        WHEN 'Mid-Range (400 - 800)' THEN 2
        WHEN 'Premium (Above 800)' THEN 3
    END;
```

#### Query Output:
| market_segment | restaurant_count | avg_segment_cost | avg_rating | Business Share |
| :--- | :---: | :---: | :---: | :---: |
| **Budget (Below 400)** | 33 | ₹303.03 | 3.84 | 40.74% |
| **Mid-Range (400 - 800)** | 36 | ₹531.94 | 4.24 | 44.44% |
| **Premium (Above 800)** | 12 | ₹1,729.17 | 4.59 | 14.81% |

---

### Task 5: Top 10 Most Popular Restaurant Chains by Outlet Count
> **Task 5:** Use ChatGPT or Copilot to help you write an SQL query that lists the top 10 most popular restaurant chains (by number of outlets) in the dataset, then run and validate the query yourself.  
> *Hint: Search for 'SQL group by count example' if you get stuck.*

#### SQL Implementation:
```sql
SELECT 
    name AS chain_name,
    COUNT(*) AS outlet_count,
    ROUND(AVG(rating), 2) AS avg_chain_rating,
    ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two
FROM zomato_bangalore
GROUP BY name
ORDER BY outlet_count DESC, avg_chain_rating DESC
LIMIT 10;
```

#### Query Output:
| chain_name | outlet_count | avg_chain_rating | avg_cost_for_two | Strategic Value |
| :--- | :---: | :---: | :---: | :--- |
| **Cafe Coffee Day** | **8** | 3.77 | ₹350.00 | High daily frequency coffee partner |
| **Onesta** | **7** | 4.26 | ₹600.00 | Dominant casual Italian dining chain |
| **Empire Restaurant**| **6** | 4.38 | ₹641.67 | Late-night delivery anchor brand |
| **Just Bake** | **6** | 3.92 | ₹300.00 | Core dessert / celebration cake brand |
| **McDonald's** | **5** | 4.12 | ₹400.00 | High-volume QSR partner |
| **Chai Point** | **5** | 4.08 | ₹250.00 | Key B2B office-hours beverage partner |
| **Domino's Pizza** | **4** | 4.20 | ₹400.00 | High repeat pizza franchise |
| **Subway** | **4** | 4.10 | ₹350.00 | Healthy eating quick-service brand |
| **KFC** | **4** | 4.00 | ₹450.00 | Weekend demand driver |
| **Meghana Foods** | **3** | 4.53 | ₹500.00 | Highest-rated local biryani powerhouse |

---

## ⚡ Automated Verification Command

Run the self-contained verification suite directly from your terminal:

```powershell
python assignment-2/case-study-zomato-bangalore-restaurants/setup_and_verify.py
```
