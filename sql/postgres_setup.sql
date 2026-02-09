-- Create PostgreSQL analytics database
-- -------------------------------------------------

-- Create the analytics database to store clean data and KPIs
-- In practice, this database is created once during setup
CREATE DATABASE flight_analytics;

-- Connect to the analytics database
\c flight_analytics;


-- Table: Cleaned & validated flight data
-- -------------------------------------------------

-- This table stores validated and transformed flight data
-- It is the main analytics table used for KPI computation
CREATE TABLE IF NOT EXISTS flight_prices_clean (

    -- Airline operating the flight
    airline TEXT,

    -- Source airport code
    source TEXT,

    -- Destination airport code
    destination TEXT,

    -- Flight departure timestamp
    departure_datetime TIMESTAMP,

    -- Flight arrival timestamp
    arrival_datetime TIMESTAMP,

    -- Flight duration in hours
    duration_hrs NUMERIC,

    -- Number of stopovers
    stopovers INT,

    -- Travel class (Economy, Business, etc.)
    class TEXT,

    -- Booking channel
    booking_source TEXT,

    -- Base fare in Bangladeshi Taka
    base_fare_bdt NUMERIC,

    -- Tax and surcharge amount
    tax_surcharge_bdt NUMERIC,

    -- Total fare (Base Fare + Tax & Surcharge)
    total_fare_bdt NUMERIC,

    -- Season classification
    seasonality TEXT,

    -- Days between booking date and departure
    days_before_departure INT
);


-- KPI 1: Average Fare by Airline
-- -------------------------------------------------

-- This table stores the average total fare for each airline
CREATE TABLE IF NOT EXISTS kpi_avg_fare_by_airline (

    -- Airline name
    airline TEXT,

    -- Average total fare in BDT
    avg_total_fare_bdt NUMERIC
);


-- KPI 2: Booking Count by Airline
-- -------------------------------------------------

-- This table stores the total number of bookings per airline
CREATE TABLE IF NOT EXISTS kpi_booking_count_by_airline (

    -- Airline name
    airline TEXT,

    -- Total number of bookings
    booking_count INT
);


-- KPI 3: Most Popular Routes
-- -------------------------------------------------

-- This table stores the most frequently booked routes
CREATE TABLE IF NOT EXISTS kpi_popular_routes (

    -- Route represented as "Source → Destination"
    route TEXT,

    -- Number of bookings for the route
    booking_count INT
);


-- KPI 4: Seasonal Fare Comparison
-- -------------------------------------------------

-- This table stores average fares by season
-- Used to analyze seasonal price variation
CREATE TABLE IF NOT EXISTS kpi_seasonal_fares (

    -- Season name (Regular, Eid, Hajj, Winter Holidays)
    seasonality TEXT,

    -- Average total fare for the season
    avg_total_fare_bdt NUMERIC
);
