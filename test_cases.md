
# Test Cases

This document describes the manual test cases used to validate the correctness, reliability, completeness, and robustness of the Airflow Flight Price Analysis pipeline.

All tests were executed using the real dataset and actual outputs generated from the production pipeline.

---

## Test Case 1: CSV Data Ingestion into MySQL

**Description:**
Verify that the raw CSV file is fully ingested into the MySQL staging table.

**Steps:**

1. Trigger the Airflow DAG `flight_csv_to_mysql`.
2. Connect to MySQL staging database.
3. Execute:

```sql
SELECT COUNT(*) FROM flight_prices_raw;
```

**Expected Outcome:**

* All CSV records are loaded into MySQL.

**Actual Outcome:**

* **57,000 records loaded successfully**



---

## Test Case 2: Schema & Column Validation

**Description:**
Ensure that required columns exist and match expected data types.

**Steps:**

1. Inspect `flight_prices_raw` table schema.
2. Verify presence of required columns:

* airline
* source
* destination
* base_fare_bdt
* tax_surcharge_bdt
* total_fare_bdt

**Expected Outcome:**

* All required columns exist.
* Fare columns are numeric.
* Datetime columns are properly typed.

**Actual Outcome:**

* All required columns present and correctly typed.


---

## Test Case 3: Duplicate Removal Validation

**Description:**
Verify that duplicate flights are removed before loading to analytics layer.

Duplicates are defined based on:

* source
* destination
* departure_datetime

**Steps:**

```sql
SELECT COUNT(*) FROM flight_prices_raw;
SELECT COUNT(*) FROM flight_prices_clean;
```

**Expected Outcome:**

* Clean dataset may be smaller if duplicates exist.

**Actual Outcome:**

* Raw records: **57,000**
* Clean records: **56,982**
* **18 duplicate/invalid records removed**


---

## Test Case 4: Negative Fare Validation

**Description:**
Ensure no negative fare values exist in clean dataset.

**Steps:**

```sql
SELECT COUNT(*) 
FROM flight_prices_clean 
WHERE base_fare_bdt < 0 
   OR tax_surcharge_bdt < 0 
   OR total_fare_bdt < 0;
```

**Expected Outcome:**

* Result count = 0

**Actual Outcome:**

* No negative fare values found.


---

## Test Case 5: Clean Data Load into PostgreSQL

**Description:**
Verify that validated and transformed data is loaded into PostgreSQL.

**Steps:**

```sql
SELECT COUNT(*) FROM flight_prices_clean;
```

**Expected Outcome:**

* Clean dataset fully loaded.

**Actual Outcome:**

* **56,982 records loaded into PostgreSQL**

---

## Test Case 6: KPI – Average Fare by Airline

**Description:**
Verify correct computation of average fare per airline.

**Steps:**

```sql
SELECT *
FROM kpi_avg_fare_by_airline
ORDER BY avg_total_fare_bdt DESC
LIMIT 5;
```

**Actual Outcome:**

| Airline            | Avg Fare (BDT) |
| ------------------ | -------------- |
| Turkish Airlines   | 74,714.94      |
| AirAsia            | 73,830.16      |
| Cathay Pacific     | 72,594.04      |
| Malaysian Airlines | 72,197.89      |
| Thai Airways       | 72,062.79      |

**Validation Result:** Airlines correctly ranked by descending average fare.


---

## Test Case 7: KPI – Booking Count by Airline

**Description:**
Verify booking volume per airline.

**Steps:**

```sql
SELECT *
FROM kpi_booking_count_by_airline
ORDER BY booking_count DESC
LIMIT 5;
```

**Actual Outcome:**

| Airline                   | Booking Count |
| ------------------------- | ------------- |
| US-Bangla Airlines        | 4,493         |
| Lufthansa                 | 2,368         |
| Vistara                   | 2,367         |
| FlyDubai                  | 2,345         |
| Biman Bangladesh Airlines | 2,343         |

**Validation Result:** Airlines correctly ranked by booking frequency.


---

## Test Case 8: KPI – Most Popular Routes

**Description:**
Identify most frequently booked routes.

**Steps:**

```sql
SELECT *
FROM kpi_popular_routes
ORDER BY booking_count DESC
LIMIT 5;
```

**Actual Outcome:**

| Route     | Booking Count |
| --------- | ------------- |
| RJH → SIN | 417           |
| DAC → DXB | 412           |
| BZL → YYZ | 410           |
| CGP → BKK | 408           |
| CXB → DEL | 408           |

**Validation Result:** Routes correctly ranked by booking count.


---

## Test Case 9: KPI – Peak vs Non-Peak Fare Comparison

**Description:**
Validate seasonal price variation logic.

Peak seasons defined as:

* Eid
* Winter Holidays

**Steps:**

```sql
SELECT *
FROM kpi_peak_vs_non_peak_fares;
```

**Actual Outcome:**

| Season Type | Avg Fare (BDT) |
| ----------- | -------------- |
| Non-Peak    | 67,943.65      |
| Peak        | 79,878.06      |

**Validation Result:**
Peak season fares are significantly higher (~17.6% higher).

---

## Test Case 10: Seasonality Distribution Check

**Description:**
Verify distribution of seasonality categories.

**Steps:**

```sql
SELECT seasonality, COUNT(*)
FROM flight_prices_clean
GROUP BY seasonality;
```

**Actual Outcome:**

| Seasonality     | Count  |
| --------------- | ------ |
| Regular         | 44,512 |
| Winter Holidays | 10,926 |
| Hajj            | 941    |
| Eid             | 603    |


---

## Test Case 11: DAG Execution Verification

**Description:**
Ensure Airflow DAGs execute successfully.

**Steps:**

1. Open Airflow UI.
2. Trigger DAGs manually.
3. Verify task status.

**Actual Outcome:**

* `flight_csv_to_mysql`: Success
* `flight_mysql_to_postgres`: Success
* Parallel KPI tasks executed successfully
* No failed tasks


---

# Final Validation Summary

All test cases passed successfully.

The pipeline confirms:

* Complete ingestion of 57,000 records
* 18 duplicate/invalid records removed
* 56,982 validated records stored
* Correct KPI computation
* Parallel execution functioning
* Data integrity preserved
* Stable Airflow orchestration

The pipeline is reproducible, reliable, and production-ready.

---

