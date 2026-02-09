
# Airflow Project: Flight Price Analysis (Bangladesh)

## 1. Introduction & Objective

The objective of this project is to design and implement an end-to-end data engineering pipeline using **Apache Airflow** to process and analyze flight price data for Bangladesh. The pipeline ingests raw CSV data, performs data validation and transformation, computes key performance indicators (KPIs), and stores the final analytical results in a **PostgreSQL** database for further analysis.

The project follows real-world data engineering best practices, including separation of staging and analytics layers, idempotent workflows, and automated orchestration using Airflow.

The dataset used in this project is the *Flight Price Dataset of Bangladesh* obtained from Kaggle, containing **57,000 flight records**.

---

## 2. Technology Stack

- **Apache Airflow 2.8.1** – workflow orchestration
- **MySQL 8.0** – staging database
- **PostgreSQL 15** – analytics database
- **Python (pandas, SQLAlchemy)** – data processing
- **Docker & Docker Compose** – containerized deployment

---

## 3. Pipeline Architecture & Data Flow

The pipeline is designed as a multi-stage architecture to ensure data quality, scalability, and maintainability.

```

CSV File
↓
Airflow DAG (Ingestion)
↓
MySQL (Staging Layer)
↓
Airflow DAG (Validation & Transformation)
↓
PostgreSQL (Analytics Layer + KPIs)

```

### Design Rationale
- **MySQL** is used as a staging layer to store raw ingested data with minimal transformation.
- **PostgreSQL** is used for analytics due to its strong aggregation and analytical capabilities.
- **Apache Airflow** orchestrates all tasks, ensuring correct execution order, retries, and logging.

---

## 4. Airflow DAGs Description

### 4.1 DAG 1: `flight_csv_to_mysql`

**Purpose:**  
Ingest the raw CSV file into a MySQL staging table.

**Key Tasks:**
- Read the CSV file using pandas.
- Normalize column names to database-friendly formats.
- Create the staging table if it does not already exist.
- Load data using an idempotent truncate-and-insert strategy.

**Validation at Ingestion:**
- Ensured all CSV columns were loaded correctly.
- Verified record count after ingestion.

**Result:**  
- **57,000 records** successfully loaded into `flight_prices_raw` table in MySQL.

---

### 4.2 DAG 2: `flight_mysql_to_postgres`

**Purpose:**  
Validate, transform, enrich data, compute KPIs, and load results into PostgreSQL.

#### Data Validation Rules
- Required columns exist:
  - Airline
  - Source
  - Destination
  - Base Fare (BDT)
  - Tax & Surcharge (BDT)
  - Total Fare (BDT)
- No negative fare values.
- Non-empty categorical fields (Airline, Source, Destination).
- Numeric data types validated for fare-related columns.

#### Data Transformation
- Recalculated **Total Fare** where necessary:
  
```

Total Fare = Base Fare + Tax & Surcharge

```

- Standardized datetime fields.
- Season classification preserved from dataset.

#### Load Strategy
- Cleaned data loaded into `flight_prices_clean` table in PostgreSQL.
- KPI tables generated using SQL aggregations.

**Result:**  
- **57,000 validated records** loaded into PostgreSQL with no data loss.

---

## 5. KPI Definitions & Results (Real Pipeline Output)

### 5.1 Average Fare by Airline (Top 5)

| Airline | Average Total Fare (BDT) |
|------|--------------------------|
| Turkish Airlines | 74,738.63 |
| AirAsia | 73,830.16 |
| Cathay Pacific | 72,594.04 |
| Malaysian Airlines | 72,247.17 |
| Thai Airways | 72,062.79 |

**Insight:**  
International airlines tend to have higher average fares compared to regional carriers.

---

### 5.2 Booking Count by Airline (Top 5)

| Airline | Booking Count |
|------|---------------|
| US-Bangla Airlines | 4,496 |
| Lufthansa | 2,368 |
| Vistara | 2,368 |
| FlyDubai | 2,346 |
| Biman Bangladesh Airlines | 2,344 |

**Insight:**  
Local and regional airlines dominate booking volume, indicating higher demand for regional routes.

---

### 5.3 Most Popular Routes

| Route | Booking Count |
|------|---------------|
| RJH → SIN | 417 |
| DAC → DXB | 413 |
| BZL → YYZ | 410 |
| CGP → BKK | 408 |
| CXB → DEL | 408 |

**Insight:**  
Routes connecting Bangladesh to major international hubs show consistently high demand.

---

### 5.4 Seasonal Fare Variation (Peak vs Non-Peak)

**Peak seasons defined as:**  
- Eid  
- Hajj  
- Winter Holidays  

**Non-Peak:** Regular season

| Season Type | Average Fare (BDT) |
|------------|--------------------|
| Peak | 79,859.41 |
| Non-Peak | 67,935.11 |

**Insight:**  
Peak season fares are approximately **17.5% higher** than non-peak fares, confirming strong seasonal price effects.

---

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

