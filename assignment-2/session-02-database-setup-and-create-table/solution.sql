-- =============================================================================
-- SESSION 2: Database Setup + CREATE TABLE
-- Coursework / Assignment Submission
-- Database: foodie_app
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1 & 2: Database Creation
-- -----------------------------------------------------------------------------
-- MySQL:
CREATE DATABASE IF NOT EXISTS foodie_app;
USE foodie_app;

-- SQLite:
-- Created automatically when connecting via: sqlite3 foodie_app.db

-- -----------------------------------------------------------------------------
-- TASK 3: Create 'restaurants' Table (Zomato-Style Backend)
-- Columns:
--   - id: integer, primary key
--   - name: varchar, max 100
--   - cuisine: varchar, max 50
--   - rating: decimal (e.g., 4.5)
--   - location: varchar, max 100
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- Insert sample records to verify schema:
INSERT INTO restaurants (id, name, cuisine, rating, location) VALUES
(1, 'Punjab Grill', 'North Indian', 4.5, 'Connaught Place, New Delhi'),
(2, 'Biryani Blues', 'Hyderabadi', 4.3, 'Indiranagar, Bengaluru'),
(3, 'Bastian', 'Seafood / Continental', 4.7, 'Bandra West, Mumbai');

SELECT * FROM restaurants;

-- -----------------------------------------------------------------------------
-- TASK 4: Create 'users' Table (Flipkart-Style App)
-- Columns:
--   - user_id: integer, primary key
--   - username: varchar, max 50
--   - email: varchar, max 100, unique
--   - phone_number: varchar(15), unique (VARCHAR preserves leading zeros & country codes)
--   - created_at: timestamp / datetime default current timestamp
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample user records:
INSERT INTO users (user_id, username, email, phone_number) VALUES
(101, 'atharv_c', 'atharv@example.com', '+919876543210'),
(102, 'priya_sharma', 'priya.s@example.com', '+919812345678'),
(103, 'rahul_verma', 'rahul.v@example.com', '+919898765432');

SELECT * FROM users;

-- -----------------------------------------------------------------------------
-- TASK 5: Intentional Error & Resolution
-- -----------------------------------------------------------------------------
-- DELIBERATE MISTAKE: Missing comma after 'email VARCHAR(100)'
-- 
-- CREATE TABLE test_table_error (
--     id INT PRIMARY KEY,
--     username VARCHAR(50),
--     email VARCHAR(100)       <-- Missing comma here!
--     phone VARCHAR(15)
-- );
--
-- ERROR RECEIVED:
-- MySQL: ERROR 1064 (42000): You have an error in your SQL syntax near 'phone VARCHAR(15))'
-- SQLite: OperationalError: near "phone": syntax error
--
-- FIX:
-- Add the comma after the email column definition.
DROP TABLE IF EXISTS test_table_fixed;

CREATE TABLE test_table_fixed (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15)
);
