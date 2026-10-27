-- ============================================================================
-- SESSION 16: SQL Project - Sales Analysis
-- Database: sales_analysis.db
-- Dialect: SQLite / Standard ANSI SQL
-- Description: End-to-end sales analysis project covering table creation,
--              CSV ingestion, customer segmentation, performance reporting,
--              and dashboard KPI metric generation.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Create 'FoodOrders' Table & Ingest CSV Data
-- Schema: order_id, restaurant_name, customer_name, order_amount, order_date
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS FoodOrders;

CREATE TABLE FoodOrders (
    order_id INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    order_amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL
);

-- Note: Data ingestion from food_orders.csv is executed via Python/SQLite
-- or SQLite CLI: .mode csv / .import food_orders.csv FoodOrders

-- ----------------------------------------------------------------------------
-- TASK 2: Create 'TopSongs' Table & Insert 5 Popular Spotify Tracks
-- Schema: song_id, song_title, artist, streams, release_date
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS TopSongs;

CREATE TABLE TopSongs (
    song_id INTEGER PRIMARY KEY,
    song_title TEXT NOT NULL,
    artist TEXT NOT NULL,
    streams BIGINT NOT NULL,
    release_date DATE NOT NULL
);

INSERT INTO TopSongs (song_id, song_title, artist, streams, release_date) VALUES
(1, 'Blinding Lights', 'The Weeknd', 4200000000, '2019-11-29'),
(2, 'Shape of You', 'Ed Sheeran', 3800000000, '2017-01-06'),
(3, 'Someone You Loved', 'Lewis Capaldi', 3300000000, '2018-11-08'),
(4, 'Sunflower', 'Post Malone & Swae Lee', 3200000000, '2018-10-19'),
(5, 'As It Was', 'Harry Styles', 3100000000, '2022-04-01');

-- Diagnostic query on TopSongs
SELECT * FROM TopSongs ORDER BY streams DESC;

-- ----------------------------------------------------------------------------
-- TASK 3: Top 3 Customers by Total Spend
-- ----------------------------------------------------------------------------
SELECT 
    customer_name,
    ROUND(SUM(order_amount), 2) AS total_spent
FROM FoodOrders
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 3;

-- ----------------------------------------------------------------------------
-- TASK 4: Product / Restaurant Performance Report
-- Lists each restaurant_name, number of orders, and total order_amount
-- Ordered by total order_amount descending
-- ----------------------------------------------------------------------------
SELECT 
    restaurant_name,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_amount), 2) AS total_order_amount
FROM FoodOrders
GROUP BY restaurant_name
ORDER BY total_order_amount DESC;

-- ----------------------------------------------------------------------------
-- TASK 5: Executive Dashboard KPIs (Two columns: kpi_name, kpi_value)
-- (1) Average order_amount
-- (2) Total number of unique customers
-- ----------------------------------------------------------------------------
SELECT 
    'Average Order Amount' AS kpi_name,
    CAST(ROUND(AVG(order_amount), 2) AS TEXT) AS kpi_value
FROM FoodOrders

UNION ALL

SELECT 
    'Total Unique Customers' AS kpi_name,
    CAST(COUNT(DISTINCT customer_name) AS TEXT) AS kpi_value
FROM FoodOrders;

-- Alternative Horizontal Dashboard Format:
SELECT 
    ROUND(AVG(order_amount), 2) AS avg_order_amount,
    COUNT(DISTINCT customer_name) AS total_unique_customers
FROM FoodOrders;
