
# System Architecture 

## 1. Overview

This document describes the system architecture of the **Airflow Flight Price Analysis** project. The architecture is designed to support a scalable, reliable, and production-style data pipeline that ingests raw flight price data, validates and transforms it, computes analytical KPIs, and stores results for analysis.

The system follows a layered approach separating ingestion, staging, transformation, and analytics.

---

## 2. High-Level Architecture

```

+--------------------------------------------------+
|              CSV Data Source                     |
|  Flight_Price_Dataset_of_Bangladesh.csv          |
+---------------------------+----------------------+
                            |
                            v
+--------------------------------------------------+
|              Apache Airflow (DAGs)               |
|                                                  |
|  DAG 1: flight_csv_to_mysql                      |
|  - Read CSV                                     |
|  - Normalize schema                             |
|  - Load into MySQL staging                      |
|                                                  |
|  DAG 2: flight_mysql_to_postgres                 |
|  - Data validation                              |
|  - Data transformation                          |
|  - KPI computation                              |
|  - Load to PostgreSQL                           |
+---------------------------+----------------------+
|
+-------------+------------------------------+
              |                              |
              v                              v
+---------------------------+      +-----------------------------+
|      MySQL (Staging)      |      |   PostgreSQL (Analytics)    |
|                           |      |                             |
|  Table: flight_prices_raw |      |  Table: flight_prices_clean |
|                           |      |  KPI Tables:                |
|                           |      |   - kpi_avg_fare_by_airline |
|                           |      |   - kpi_booking_count       |
|                           |      |   - kpi_popular_routes      |
|                           |      |   - kpi_peak_vs_non_peak    |
+---------------------------+      +-----------------------------+

```

---

## 3. Component Description

### 3.1 CSV Data Source
- Input dataset: **Flight_Price_Dataset_of_Bangladesh.csv**
- Contains **57,000 records**
- Includes airline, route, fare, seasonality, and booking information

---

### 3.2 Apache Airflow
Apache Airflow is used as the workflow orchestration engine.

**Responsibilities:**
- Task scheduling and dependency management
- Retry logic and failure handling
- Logging and observability
- Manual and automated DAG execution

Two DAGs are implemented:
- `flight_csv_to_mysql`
- `flight_mysql_to_postgres`

---

### 3.3 MySQL – Staging Layer
- Purpose: Store raw ingested data
- Table: `flight_prices_raw`
- Characteristics:
  - Minimal transformation
  - Schema closely matches CSV structure
  - Acts as a buffer between source and analytics

**Why MySQL?**
- Lightweight
- Fast inserts
- Ideal for staging raw data

---

### 3.4 PostgreSQL – Analytics Layer
- Purpose: Store validated, transformed, and enriched data
- Tables:
  - `flight_prices_clean`
  - KPI tables:
    - `kpi_avg_fare_by_airline`
    - `kpi_booking_count_by_airline`
    - `kpi_popular_routes`
    - `kpi_peak_vs_non_peak_fares`

**Why PostgreSQL?**
- Strong analytical capabilities
- Efficient aggregations
- Suitable for BI and reporting workloads

---

## 4. Data Flow Explanation

1. **Ingestion Phase**
   - Airflow reads the CSV file.
   - Data is normalized and loaded into MySQL.
   - Record count validation ensures completeness.

2. **Validation Phase**
   - Required columns are checked.
   - Invalid records (e.g., negative fares) are filtered.
   - Data types are enforced.

3. **Transformation Phase**
   - Total fare is recalculated if required.
   - Date and season fields are standardized.

4. **Analytics Phase**
   - KPIs are computed using SQL aggregations.
   - Results are stored in dedicated KPI tables.

---

## 5. Design Principles Applied

- **Separation of Concerns**  
  Staging and analytics are handled by different databases.

- **Idempotency**  
  DAGs can be safely re-run without duplicating data.

- **Scalability**  
  Architecture can handle larger datasets with minimal changes.

- **Observability**  
  Airflow provides task-level logs and execution tracking.

---

## 6. Deployment Architecture (Docker)

All components are deployed using Docker Compose:

- Airflow Webserver & Scheduler
- MySQL container (staging)
- PostgreSQL container (analytics)

This ensures:
- Consistent environment
- Easy setup
- Reproducibility

---

## 7. Conclusion

The system architecture successfully supports a complete data engineering workflow, from raw data ingestion to analytical insights. The modular and layered design ensures data quality, reliability, and ease of maintenance, making the solution suitable for both academic and real-world analytics applications.

---
