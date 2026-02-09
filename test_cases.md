
# Test Cases 

This document describes the manual test cases used to validate the correctness, reliability, and completeness of the Airflow Flight Price Analysis pipeline.  
All tests were executed using the real dataset and actual pipeline outputs.

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
   ````

**Expected Outcome:**

* All CSV records are loaded into MySQL.

**Actual Outcome:**

* **57,000 records loaded successfully** 

**Status:** Pass

---

## Test Case 2: Schema & Column Validation

**Description:**
Ensure that required columns exist and match expected data types.

**Steps:**

1. Inspect the `flight_prices_raw` table schema.
2. Verify presence of required columns:

   * airline
   * source
   * destination
   * base_fare_bdt
   * tax_surcharge_bdt
   * total_fare_bdt

**Expected Outcome:**

* All required columns exist with correct data types.

**Actual Outcome:**

* All required columns present and correctly typed 

**Status:** Pass

---

## Test Case 3: Data Quality – Negative Fare Check

**Description:**
Ensure there are no invalid negative fare values.

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

* No negative fare values found 

**Status:** Pass

---

## Test Case 4: Clean Data Load into PostgreSQL

**Description:**
Verify that validated and transformed data is loaded into PostgreSQL analytics database.

**Steps:**

1. Trigger DAG `flight_mysql_to_postgres`.
2. Execute:

   ```sql
   SELECT COUNT(*) FROM flight_prices_clean;
   ```

**Expected Outcome:**

* Same number of records as staging (no data loss).

**Actual Outcome:**

* **57,000 records loaded** 

**Status:** Pass

---

## Test Case 5: KPI – Average Fare by Airline

**Description:**
Verify correct computation of average fare per airline.

**Steps:**

```sql
SELECT * 
FROM kpi_avg_fare_by_airline 
ORDER BY avg_total_fare_bdt DESC 
LIMIT 5;
```

**Expected Outcome:**

* Airlines ranked by descending average fare.

**Actual Outcome:**

| Airline            | Avg Fare (BDT) |
| ------------------ | -------------- |
| Turkish Airlines   | 74,738.63      |
| AirAsia            | 73,830.16      |
| Cathay Pacific     | 72,594.04      |
| Malaysian Airlines | 72,247.17      |
| Thai Airways       | 72,062.79      |

**Status:** Pass

---

## Test Case 6: KPI – Booking Count by Airline

**Description:**
Verify booking volume per airline.

**Steps:**

```sql
SELECT * 
FROM kpi_booking_count_by_airline 
ORDER BY booking_count DESC 
LIMIT 5;
```

**Expected Outcome:**

* Airlines ranked by booking frequency.

**Actual Outcome:**

| Airline                   | Booking Count |
| ------------------------- | ------------- |
| US-Bangla Airlines        | 4,496         |
| Lufthansa                 | 2,368         |
| Vistara                   | 2,368         |
| FlyDubai                  | 2,346         |
| Biman Bangladesh Airlines | 2,344         |

**Status:** Pass

---

## Test Case 7: KPI – Most Popular Routes

**Description:**
Identify most frequently booked source-destination routes.

**Steps:**

```sql
SELECT * 
FROM kpi_popular_routes 
ORDER BY booking_count DESC 
LIMIT 5;
```

**Expected Outcome:**

* Top routes by booking count.

**Actual Outcome:**

| Route     | Booking Count |
| --------- | ------------- |
| RJH → SIN | 417           |
| DAC → DXB | 413           |
| BZL → YYZ | 410           |
| CGP → BKK | 408           |
| CXB → DEL | 408           |

**Status:** Pass

---

## Test Case 8: KPI – Peak vs Non-Peak Fare Comparison

**Description:**
Validate seasonal fare variation logic.

**Steps:**

```sql
SELECT * 
FROM kpi_peak_vs_non_peak_fares;
```

**Expected Outcome:**

* Peak season fares higher than non-peak.

**Actual Outcome:**

| Season Type | Avg Fare (BDT) |
| ----------- | -------------- |
| Peak        | 79,859.41      |
| Non-Peak    | 67,935.11      |

**Status:** Pass

---

## Test Case 9: DAG Execution Verification

**Description:**
Ensure Airflow DAGs execute successfully.

**Steps:**

1. Open Airflow UI.
2. Verify DAG run status.

**Expected Outcome:**

* DAGs complete without failure.

**Actual Outcome:**

* `flight_csv_to_mysql`: Success 
* `flight_mysql_to_postgres`: Success 

**Status:** Pass

---

## Conclusion

All test cases passed successfully, confirming that:

* Data ingestion is complete and accurate.
* Validation and transformation rules are enforced.
* KPIs are computed correctly using real data.
* The Airflow pipeline is stable and reproducible.

---

