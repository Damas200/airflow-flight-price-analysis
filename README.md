#  Airflow Flight Price Analysis

##  Project Overview

This project implements a **production-style end-to-end data engineering pipeline** using **Apache Airflow** to process and analyze flight price data for Bangladesh.

The pipeline ingests raw CSV data, stages it in MySQL, validates and transforms it, removes duplicates, computes analytical KPIs in parallel, and stores final results in a PostgreSQL analytics database.

All results shown in this repository are **real outputs generated from the executed pipeline**.

---

##  Objective

* Ingest raw flight price data from a CSV file
* Stage raw data in MySQL
* Validate and clean the dataset
* Remove duplicate records
* Compute business KPIs (parallel execution)
* Store cleaned data and KPIs in PostgreSQL
* Enable monitoring, retry logic, and observability using Airflow

---

##  Technologies Used

* **Apache Airflow 2.8.1** – workflow orchestration
* **MySQL 8.0** – staging database
* **PostgreSQL 15** – analytics database
* **Python (Pandas, SQLAlchemy)** – data validation & transformation
* **Docker & Docker Compose** – containerized deployment
* **SQL** – schema and analytical queries

---

##  Project Structure

```
airflow-flight-price-analysis/
├── dags/
│   ├── flight_csv_to_mysql.py
│   └── flight_mysql_to_postgres.py
├── data/
│   └── Flight_Price_Dataset_of_Bangladesh.csv
├── sql/
│   ├── mysql_setup.sql
│   ├── postgres_setup.sql
│   └── postgres_analytics.sql
├── docker-compose.yaml
├── README.md
├── project_report.md
├── system_architecture.md
└── test_cases.md
```

---

##  Pipeline Architecture

```
CSV File
    ↓
Airflow DAG (Ingestion)
    ↓
MySQL (Staging Layer)
    ↓
Airflow DAG (Validation + Deduplication + Transformation)
    ↓
Parallel KPI Tasks
    ↓
PostgreSQL (Analytics Layer)
```

---

##  Airflow DAGs

### 1️. `flight_csv_to_mysql`

**Purpose:**
Load raw flight price data from CSV into MySQL staging table.

**Result:**

* **57,000 raw records ingested** into `flight_prices_raw`

---

### 2️. `flight_mysql_to_postgres`

**Purpose:**
Validate, clean, deduplicate, transform, and analyze flight data.

###  Data Processing Performed

* Removed null critical fields
* Removed negative fare values
* Removed duplicates based on:

  * `source`
  * `destination`
  * `departure_datetime`
* Recalculated total fare:

  ```
  Total Fare = Base Fare + Tax & Surcharge
  ```
* Classified season into:

  * Peak (Eid, Winter Holidays)
  * Non-Peak (Regular, Hajj)

###  Final Clean Dataset

* **56,982 validated and cleaned records**
* 18 duplicate/invalid records removed

---

#  KPI Results (REAL PIPELINE OUTPUTS)

##  KPI 1: Average Fare by Airline (Top 5)

| Airline            | Avg Total Fare (BDT) |
| ------------------ | -------------------- |
| Turkish Airlines   | 74,714.94            |
| AirAsia            | 73,830.16            |
| Cathay Pacific     | 72,594.04            |
| Malaysian Airlines | 72,197.89            |
| Thai Airways       | 72,062.79            |

---

##  KPI 2: Booking Count by Airline (Top 5)

| Airline                   | Booking Count |
| ------------------------- | ------------- |
| US-Bangla Airlines        | 4,493         |
| Lufthansa                 | 2,368         |
| Vistara                   | 2,367         |
| FlyDubai                  | 2,345         |
| Biman Bangladesh Airlines | 2,343         |

---

##  KPI 3: Most Popular Routes

| Route     | Booking Count |
| --------- | ------------- |
| RJH → SIN | 417           |
| DAC → DXB | 412           |
| BZL → YYZ | 410           |
| CGP → BKK | 408           |
| CXB → DEL | 408           |

---

##  KPI 4: Peak vs Non-Peak Fare Comparison

| Season Type | Avg Total Fare (BDT) |
| ----------- | -------------------- |
| Peak        | 79,878.06            |
| Non-Peak    | 67,943.65            |

 Peak fares are approximately **17.6% higher** than non-peak fares.

---

##  Seasonality Distribution (Clean Data)

| Seasonality     | Records |
| --------------- | ------- |
| Regular         | 44,512  |
| Winter Holidays | 10,926  |
| Hajj            | 941     |
| Eid             | 603     |

---

##  Testing

All validation tests passed successfully (see `test_cases.md`):

* CSV ingestion correctness
* Duplicate removal validation
* Row count consistency (MySQL vs PostgreSQL)
* Negative fare validation
* KPI accuracy verification
* End-to-end DAG execution success

---

## ▶️ How to Run the Project

### 1️. Start services

```bash
docker compose up -d
```

### 2️. Open Airflow UI

```
http://localhost:8080
```

Login:

* Username: `admin`
* Password: `admin`

### 3️. Trigger DAGs (in order)

1. `flight_csv_to_mysql`
2. `flight_mysql_to_postgres`

---

##  Documentation

* `project_report.md` – detailed technical report with real validated results
* `system_architecture.md` – architecture and design explanation
* `test_cases.md` – manual validation plan
* `postgres_analytics.sql` – verification queries

---

##  Author

**Damas Niyonkuru**
Module Lab 1 – Airflow Project: Flight Price Analysis

---
