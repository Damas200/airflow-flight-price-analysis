-- -------------------------------------------------
-- Create MySQL database for staging flight data
-- -------------------------------------------------

-- Create the staging database if it does not already exist
-- This makes the script safe to run multiple times (idempotent)
CREATE DATABASE IF NOT EXISTS flight_staging;

-- Select the staging database for use
USE flight_staging;


-- -------------------------------------------------
-- Create raw flight prices staging table
-- -------------------------------------------------

-- This table stores raw data ingested from the CSV file
-- Minimal transformation is applied at this stage
CREATE TABLE IF NOT EXISTS flight_prices_raw (

    -- Airline operating the flight
    airline VARCHAR(100),

    -- Source airport code 
    source VARCHAR(50),

    -- Full name of the source airport
    source_name VARCHAR(100),

    -- Destination airport code 
    destination VARCHAR(50),

    -- Full name of the destination airport
    destination_name VARCHAR(100),

    -- Flight departure date and time
    departure_datetime DATETIME,

    -- Flight arrival date and time
    arrival_datetime DATETIME,

    -- Flight duration in hours
    duration_hrs DECIMAL(5,2),

    -- Number of stopovers (0 = direct flight)
    stopovers INT,

    -- Type of aircraft used
    aircraft_type VARCHAR(100),

    -- Travel class (Economy, Business, First Class)
    class VARCHAR(50),

    -- Booking channel (Online, Travel Agency, etc.)
    booking_source VARCHAR(100),

    -- Base fare amount in Bangladeshi Taka
    base_fare_bdt DECIMAL(10,2),

    -- Tax and surcharge amount in Bangladeshi Taka
    tax_surcharge_bdt DECIMAL(10,2),

    -- Total fare amount in Bangladeshi Taka
    total_fare_bdt DECIMAL(10,2),

    -- Season classification (Regular, Eid, Hajj, Winter Holidays)
    seasonality VARCHAR(50),

    -- Number of days between booking date and departure
    days_before_departure INT
);
