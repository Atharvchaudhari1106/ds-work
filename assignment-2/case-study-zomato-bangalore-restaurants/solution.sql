-- ============================================================================
-- CASE STUDY: Zomato Bangalore Restaurants - Kaggle Analytics
-- Database: zomato_bangalore.db
-- Dialect: SQLite / Standard ANSI SQL
-- Description: Business and strategic expansion analytics for Zomato Bangalore,
--              answering executive questions regarding rating optimization,
--              pricing strategy, customer preferences, and chain penetration.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- DDL: Create 'zomato_bangalore' Table
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS zomato_bangalore;

CREATE TABLE zomato_bangalore (
    restaurant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    online_order TEXT NOT NULL CHECK (online_order IN ('Yes', 'No')),
    book_table TEXT NOT NULL CHECK (book_table IN ('Yes', 'No')),
    rating REAL NOT NULL,
    votes INTEGER NOT NULL,
    location TEXT NOT NULL,
    cuisines TEXT NOT NULL,
    approx_cost_for_two DECIMAL(10, 2) NOT NULL
);

-- Note: Data imported from zomato_bangalore.csv into table zomato_bangalore

-- ----------------------------------------------------------------------------
-- TASK 1: Top 5 Highest-Rated North Indian Restaurants in Koramangala
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- TASK 2: Average Cost for Two per Cuisine & Top 3 Most Expensive Cuisines
-- ----------------------------------------------------------------------------
SELECT 
    cuisines AS cuisine_type,
    ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two,
    COUNT(*) AS restaurant_count
FROM zomato_bangalore
GROUP BY cuisines
ORDER BY avg_cost_for_two DESC
LIMIT 3;

-- ----------------------------------------------------------------------------
-- TASK 3: Online Delivery Restaurants with Rating Below 3.0 (Low-Rating Audit)
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- TASK 4: Three-Tier Market Segmentation (Budget, Mid-Range, Premium)
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- TASK 5: Top 10 Most Popular Restaurant Chains by Outlet Count
-- ----------------------------------------------------------------------------
SELECT 
    name AS chain_name,
    COUNT(*) AS outlet_count,
    ROUND(AVG(rating), 2) AS avg_chain_rating,
    ROUND(AVG(approx_cost_for_two), 2) AS avg_cost_for_two
FROM zomato_bangalore
GROUP BY name
ORDER BY outlet_count DESC, avg_chain_rating DESC
LIMIT 10;
