
-- PostgreSQL Analytics Queries
-- Project: Airflow Flight Price Analysis
-- Purpose: Validate KPIs & support reporting/demo
-- =====================================================

-- Use analytics database
\c flight_analytics;

-- 1. Record Count Validation
-- =====================================================
SELECT
    COUNT(*) AS total_clean_records
FROM flight_prices_clean;

-- 2. KPI: Average Fare by Airline
-- =====================================================
SELECT
    airline,
    avg_total_fare_bdt
FROM kpi_avg_fare_by_airline
ORDER BY avg_total_fare_bdt DESC
LIMIT 10;

-- 3. KPI: Booking Count by Airline
-- =====================================================
SELECT
    airline,
    booking_count
FROM kpi_booking_count_by_airline
ORDER BY booking_count DESC
LIMIT 10;

-- 4. KPI: Most Popular Routes
-- =====================================================
SELECT
    route,
    booking_count
FROM kpi_popular_routes
ORDER BY booking_count DESC
LIMIT 10;

-- 5. KPI: Peak vs Non-Peak Fare Comparison
-- =====================================================
SELECT
    season_type,
    avg_total_fare_bdt
FROM kpi_peak_vs_non_peak_fares;

-- 6. Seasonal Distribution Check
-- =====================================================
SELECT
    seasonality,
    COUNT(*) AS record_count
FROM flight_prices_clean
GROUP BY seasonality
ORDER BY record_count DESC;
