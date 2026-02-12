
# Airflow Project: Flight Price Analysis (Bangladesh)

## 1. Introduction & Objective

The objective of this project is to design and implement an end-to-end data engineering pipeline using **Apache Airflow** to process and analyze flight price data for Bangladesh. The pipeline ingests raw CSV data, performs data validation and transformation, computes key performance indicators (KPIs), and stores the final analytical results in a **PostgreSQL** database for further analysis.

This project follows production-style data engineering practices:

* Separation of staging and analytics layers
* Idempotent workflows (safe re-runs)
* Automated orchestration using Airflow
* Data quality validation rules
* Parallel KPI computation

The dataset used is the *Flight Price Dataset of Bangladesh* (Kaggle), originally containing **57,000 records**.

---

## 2. Technology Stack

* **Apache Airflow 2.8.1** – workflow orchestration
* **MySQL 8.0** – staging database
* **PostgreSQL 15** – analytics database
* **Python (pandas, SQLAlchemy)** – data processing
* **Docker & Docker Compose** – containerized deployment

---

## 3. Pipeline Architecture & Data Flow

```
CSV File
   ↓
Airflow DAG 1 (Ingestion)
   ↓
MySQL (Staging Layer - Raw Data)
   ↓
Airflow DAG 2 (Validation + Transformation + KPIs)
   ↓
PostgreSQL (Analytics Layer)
```

### Design Rationale

* **MySQL** is used as a staging layer to store raw data exactly as received.
* **PostgreSQL** is used for analytics because of its strong aggregation capabilities.
* **Apache Airflow** orchestrates the workflow, manages dependencies, and handles failures.
* KPI computations were separated into parallel tasks to improve modularity and scalability.

---

## 4. Airflow DAGs Description

---

## 4.1 DAG 1: `flight_csv_to_mysql`

### Purpose

Ingest the raw CSV file into MySQL staging table (`flight_prices_raw`).

### Tasks Performed

* Read CSV using pandas.
* Normalize column names.
* Convert datetime fields.
* Load data into MySQL.

### Result

* **57,000 records** successfully loaded into MySQL staging layer.

---

## 4.2 DAG 2: `flight_mysql_to_postgres`

### Purpose

Validate data, remove duplicates, transform records, compute KPIs, and load clean results into PostgreSQL.

---

### Data Validation Rules Implemented

1. Required columns must exist:

   * airline
   * source
   * destination
   * base_fare_bdt
   * tax_surcharge_bdt

2. Removed rows with:

   * Missing critical values
   * Negative fare values

3. Removed duplicate records based on:

   * `source`
   * `destination`
   * `departure_datetime`

4. Recalculated:

```
Total Fare = Base Fare + Tax & Surcharge
```

5. Classified season type:

   * Peak: Eid, Winter Holidays
   * Non-Peak: Regular, Hajj

---

### Final Cleaned Dataset Result

```sql
SELECT COUNT(*) FROM flight_prices_clean;
```

**Final Clean Records:**

```
56,982
```

🔎 **Explanation:**

* Original records: 57,000
* Removed: 18 invalid or duplicate records
* Final analytics-ready dataset: **56,982 records**

---

## 5. KPI Definitions & Results (Real Pipeline Output)

All KPI values below come directly from the final PostgreSQL database.

---

## 5.1 Average Fare by Airline (Top 5)

| Airline            | Avg Total Fare (BDT) |
| ------------------ | -------------------- |
| Turkish Airlines   | 74,714.94            |
| AirAsia            | 73,830.16            |
| Cathay Pacific     | 72,594.04            |
| Malaysian Airlines | 72,197.89            |
| Thai Airways       | 72,062.79            |

**Insight:**
International airlines show consistently higher average fares.

---

## 5.2 Booking Count by Airline (Top 5)

| Airline                   | Booking Count |
| ------------------------- | ------------- |
| US-Bangla Airlines        | 4,493         |
| Lufthansa                 | 2,368         |
| Vistara                   | 2,367         |
| FlyDubai                  | 2,345         |
| Biman Bangladesh Airlines | 2,343         |

**Insight:**
Regional carriers dominate booking volume.

---

## 5.3 Most Popular Routes

| Route     | Booking Count |
| --------- | ------------- |
| RJH → SIN | 417           |
| DAC → DXB | 412           |
| BZL → YYZ | 410           |
| CGP → BKK | 408           |
| CXB → DEL | 408           |

**Insight:**
Routes to major international hubs show highest demand.

---

## 5.4 Seasonal Fare Variation

### Season Distribution

```sql
SELECT seasonality, COUNT(*) FROM flight_prices_clean GROUP BY seasonality;
```

| Seasonality     | Count  |
| --------------- | ------ |
| Regular         | 44,512 |
| Winter Holidays | 10,926 |
| Hajj            | 941    |
| Eid             | 603    |

---

### Peak vs Non-Peak Comparison

```sql
SELECT * FROM kpi_peak_vs_non_peak_fares;
```

| Season Type | Avg Fare (BDT) |
| ----------- | -------------- |
| Non-Peak    | 67,943.65      |
| Peak        | 79,878.06      |

**Insight:**

* Peak fares are ~11,934 BDT higher than Non-Peak.
* This confirms strong seasonal price inflation during Eid and Winter Holidays.

---

## 6. Additional Improvements (Supervisor Feedback Implemented)

### 1. Duplicate Removal

Duplicates removed using:

```
source + destination + departure_datetime
```

### 2. Parallel KPI Tasks

KPIs were separated into independent tasks:

* avg_fare_by_airline
* booking_count_by_airline
* popular_routes
* seasonal_fares
* peak_vs_non_peak

This allows parallel execution in Airflow.

### 3. DAG Notifications

Email alert system configured for failed tasks.

--
## 6. Challenges Encountered & Solutions

### Challenge 1: Docker Port Conflicts
**Issue:** MySQL and PostgreSQL ports conflicted with existing services.  
**Solution:** Custom port mappings were applied, and containers were isolated using Docker Compose networks.

---

### Challenge 2: Airflow Scheduler Not Running
**Issue:** DAGs were visible but not executing.  
**Solution:** Scheduler process was manually verified and restarted; container startup commands were corrected.

---

### Challenge 3: Database Initialization Errors
**Issue:** Database creation scripts failed on re-runs.  
**Solution:** SQL scripts were made idempotent using `IF NOT EXISTS`.

---

## 7. Conclusion

This project successfully demonstrates a complete, production-style data engineering pipeline using Apache Airflow. The pipeline ingests raw data, enforces data quality, performs transformations, computes meaningful KPIs, and stores results in a dedicated analytics database.

