
#  Airflow Flight Price Analysis

##  Project Overview
This project implements an **end-to-end data engineering pipeline** using **Apache Airflow** to process and analyze flight price data for Bangladesh.

The pipeline ingests raw CSV data, stages it in MySQL, validates and transforms it, computes analytical KPIs, and stores the final results in a PostgreSQL analytics database.  
All results shown in this repository are **real outputs generated from the executed pipeline**.

---

##  Objective
- Ingest raw flight price data from a CSV file
- Stage raw data in MySQL
- Validate and transform data using Airflow
- Compute business KPIs
- Store cleaned data and KPIs in PostgreSQL
- Enable monitoring and reproducibility using Airflow

---

##  Technologies Used
- **Apache Airflow** – workflow orchestration
- **MySQL** – staging database
- **PostgreSQL** – analytics database
- **Python (Pandas)** – data processing
- **Docker & Docker Compose** – containerization
- **SQL** – schema definition and analytics queries

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
MySQL (Staging)
↓
Airflow DAG (Validation & Transformation)
↓
PostgreSQL (Analytics & KPIs)

````

---

## ⚙️ Airflow DAGs

### 1️ `flight_csv_to_mysql`
**Purpose:**  
Loads raw flight price data from CSV into MySQL staging.

**Result:**  
- **57,000 records successfully ingested** into `flight_prices_raw`

---

### 2 `flight_mysql_to_postgres`
**Purpose:**  
Validates, transforms, and analyzes flight price data.

**Key operations:**
- Remove null and invalid values
- Recalculate total fare
- Classify Peak vs Non-Peak seasons
- Compute KPIs
- Load cleaned data into PostgreSQL

**Result:**  
- **57,000 cleaned records** stored in `flight_prices_clean`

---

##  KPI Results (REAL PIPELINE OUTPUTS)

###  KPI 1: Average Fare by Airline (Top 5)
| Airline | Avg Total Fare (BDT) |
|-------|----------------------|
| Turkish Airlines | 74,738.63 |
| AirAsia | 73,830.16 |
| Cathay Pacific | 72,594.04 |
| Malaysian Airlines | 72,247.17 |
| Thai Airways | 72,062.79 |

---

###  KPI 2: Booking Count by Airline (Top 5)
| Airline | Booking Count |
|-------|---------------|
| US-Bangla Airlines | 4,496 |
| Lufthansa | 2,368 |
| Vistara | 2,368 |
| FlyDubai | 2,346 |
| Biman Bangladesh Airlines | 2,344 |

---

###  KPI 3: Most Popular Routes
| Route | Booking Count |
|------|---------------|
| RJH → SIN | 417 |
| DAC → DXB | 413 |
| BZL → YYZ | 410 |
| CGP → BKK | 408 |
| CXB → DEL | 408 |

---

###  KPI 4: Peak vs Non-Peak Fare Comparison
| Season Type | Avg Total Fare (BDT) |
|------------|----------------------|
| Peak | 79,859.41 |
| Non-Peak | 67,935.11 |

**Peak seasons include:** Eid and Winter Holidays.

---

###  Seasonality Distribution (Data Insight)
| Seasonality | Records |
|------------|---------|
| Regular | 44,525 |
| Winter Holidays | 10,930 |
| Hajj | 942 |
| Eid | 603 |

---

##  Testing
Testing was performed manually and documented in `test_cases.md`, covering:
- CSV ingestion correctness
- Row count consistency (MySQL vs PostgreSQL)
- Validation of null and negative values
- KPI correctness verification
- End-to-end pipeline execution

---

##  How to Run the Project

### 1️⃣ Start services
```bash
docker compose up -d
````

### 2️⃣ Open Airflow UI

```
http://localhost:8080
```

Login:

* Username: `admin`
* Password: `admin`

### 3️⃣ Trigger DAGs (in order)

1. `flight_csv_to_mysql`
2. `flight_mysql_to_postgres`

---

## Documentation

* `project_report.md` – detailed technical report with real results
* `system_architecture.md` – pipeline architecture and data flow
* `test_cases.md` – validation and testing plan
* `postgres_analytics.sql` – SQL queries used to verify KPIs

---

##  Key Learning Outcomes

* Designing end-to-end Airflow pipelines
* Data staging and analytics separation
* Validation and transformation using Python
* KPI computation for business analysis
* Containerized data engineering workflows

---

##  Author

**Damas Niyonkuru**
Module Lab 1 – Airflow Project: Flight Price Analysis

