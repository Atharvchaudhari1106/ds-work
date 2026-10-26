-- =====================================================================
-- ASSESSMENT: DATA SCIENCE M4-A1
-- SQL SCRIPTS: DDL, SEED DATA & ANALYTICAL QUERIES (SQLite)
-- Application Domain: Food Delivery Platform Analytics
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. DDL: Create Tables (restaurants, orders)
-- ---------------------------------------------------------------------

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    order_value REAL NOT NULL,
    delivery_time_mins REAL NOT NULL,
    rating REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- ---------------------------------------------------------------------
-- 2. DML: Insert Seed Records (9 Restaurants, 28 Orders)
-- ---------------------------------------------------------------------

INSERT INTO restaurants (restaurant_id, name, category, city) VALUES
(1, 'Spice Symphony', 'Indian', 'Mumbai'),
(2, 'Pizza Roma', 'Italian', 'Bengaluru'),
(3, 'Burger Garage', 'Burgers', 'Delhi'),
(4, 'Dragon Wok', 'Chinese', 'Mumbai'),
(5, 'Taco Fiesta', 'Mexican', 'Pune'),
(6, 'Curry House', 'Indian', 'Delhi'),
(7, 'Sushi Bay', 'Japanese', 'Bengaluru'),
(8, 'Pasta Bella', 'Italian', 'Pune'),
(9, 'The Green Bowl', 'Healthy/Salad', 'Mumbai');

INSERT INTO orders (order_id, restaurant_id, order_value, delivery_time_mins, rating) VALUES
(1001, 1, 650.0, 32.0, 4.8),
(1002, 1, 820.0, 35.0, 4.6),
(1003, 1, 540.0, 28.0, 4.7),
(1004, 1, 950.0, 40.0, 4.9),
(1005, 2, 720.0, 29.0, 4.3),
(1006, 2, 610.0, 31.0, 4.1),
(1007, 2, 850.0, 34.0, 4.5),
(1008, 3, 320.0, 24.0, 3.9),
(1009, 3, 410.0, 22.0, 3.8),
(1010, 3, 290.0, 26.0, 4.0),
(1011, 4, 780.0, 38.0, 4.2),
(1012, 4, 690.0, 36.0, 4.4),
(1013, 4, 840.0, 41.0, 4.3),
(1014, 4, 590.0, 33.0, 4.1),
(1015, 5, 480.0, 25.0, 4.2),
(1016, 5, 520.0, 27.0, 4.0),
(1017, 5, 610.0, 30.0, 4.3),
(1018, 6, 890.0, 42.0, 4.5),
(1019, 6, 1050.0, 45.0, 4.6),
(1020, 6, 740.0, 39.0, 4.4),
(1021, 7, 1250.0, 50.0, 4.8),
(1022, 7, 1400.0, 52.0, 4.9),
(1023, 7, 980.0, 46.0, 4.7),
(1024, 7, 1150.0, 48.0, 4.8),
(1025, 8, 510.0, 28.0, 4.1),
(1026, 8, 630.0, 32.0, 4.3),
(1027, 8, 580.0, 30.0, 4.2),
(1028, 2, 790.0, 33.0, 4.4);

-- ---------------------------------------------------------------------
-- 3. Section B - Task 4 Query: Ranked Restaurant Performance Report
-- ---------------------------------------------------------------------
-- Uses LEFT JOIN to include restaurants with zero orders (e.g., 'The Green Bowl')
SELECT 
    r.restaurant_id,
    r.name AS restaurant_name,
    r.category,
    r.city,
    COUNT(o.order_id) AS total_orders,
    ROUND(COALESCE(SUM(o.order_value), 0.0), 2) AS total_revenue,
    ROUND(COALESCE(AVG(o.rating), 0.0), 2) AS avg_rating
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.name, r.category, r.city
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------
-- 4. Section C - Mini Capstone Query 1: Category-Level Aggregation
-- ---------------------------------------------------------------------
SELECT 
    r.category,
    COUNT(o.order_id) AS total_orders,
    ROUND(COALESCE(SUM(o.order_value), 0.0), 2) AS total_revenue,
    ROUND(COALESCE(AVG(o.order_value), 0.0), 2) AS avg_order_value,
    ROUND(COALESCE(AVG(o.delivery_time_mins), 0.0), 2) AS avg_delivery_time,
    ROUND(COALESCE(AVG(o.rating), 0.0), 2) AS avg_rating
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.category
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------
-- 5. Section C - Mini Capstone Query 2: City & Restaurant Detailed JOIN
-- ---------------------------------------------------------------------
SELECT 
    r.city,
    r.name AS restaurant_name,
    r.category,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.order_value), 2) AS restaurant_revenue,
    ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.city, r.name, r.category
ORDER BY r.city ASC, restaurant_revenue DESC;

-- ---------------------------------------------------------------------
-- 6. Section D - Top 3 Restaurants with Min 5 Orders Filter (AI task)
-- ---------------------------------------------------------------------
SELECT 
    r.name AS restaurant_name,
    r.category,
    COUNT(o.order_id) AS order_count,
    ROUND(AVG(o.rating), 2) AS avg_rating,
    ROUND(SUM(o.order_value), 2) AS total_revenue
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.name, r.category
HAVING COUNT(o.order_id) >= 5
ORDER BY avg_rating DESC
LIMIT 3;
