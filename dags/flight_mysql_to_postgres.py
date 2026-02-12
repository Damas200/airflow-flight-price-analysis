
# Flight MySQL to PostgreSQL Analytics DAG
# Purpose:
#   - Extract data from MySQL staging
#   - Clean and validate the data
#   - Remove duplicates
#   - Compute KPIs in parallel
#   - Load results into PostgreSQL analytics database
# ============================================================


# Import Airflow core class
from airflow import DAG

# TaskFlow API allows defining tasks as Python functions
from airflow.decorators import task

# MySQL and PostgreSQL connection hooks
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.postgres_hook import PostgresHook

# Utility for setting start date
from airflow.utils.dates import days_ago

# Pandas for data processing
import pandas as pd


# Default arguments for the DAG
# Email notification is enabled if a task fails
default_args = {
    "owner": "airflow",
    "email": ["damas.niyonkuru@amalitech.com"],  # Replace with your real email
    "email_on_failure": True,
    "email_on_retry": False,
}


# Define the DAG
with DAG(
    dag_id="flight_mysql_to_postgres",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,  # Manual execution
    catchup=False,
    tags=["phase3", "analytics"]
):


    # 1️. EXTRACT DATA FROM MYSQL STAGING
    # ============================================================
    @task
    def extract_from_mysql():
        """
        This task reads raw flight data from MySQL staging database.
        """

        # Connect to MySQL using Airflow connection
        mysql_hook = MySqlHook(mysql_conn_id="mysql_staging")

        # Create SQLAlchemy engine
        engine = mysql_hook.get_sqlalchemy_engine()

        # Read full table into pandas DataFrame
        df = pd.read_sql("SELECT * FROM flight_prices_raw", engine)

        return df


    
    # 2️. VALIDATE AND TRANSFORM DATA
    # ============================================================
    @task
    def validate_and_transform(df: pd.DataFrame):
        """
        This task cleans the data and prepares it for analytics.
        """

        # Remove rows with missing important fields
        df = df.dropna(subset=[
            "airline", "source", "destination",
            "base_fare_bdt", "tax_surcharge_bdt"
        ])

        # Remove negative fare values
        df = df[
            (df["base_fare_bdt"] >= 0) &
            (df["tax_surcharge_bdt"] >= 0)
        ]

        # Remove duplicate flights
        # Duplicates defined by same source, destination, and departure time
        df = df.drop_duplicates(
            subset=["source", "destination", "departure_datetime"]
        )

        # Recalculate total fare
        # This ensures consistency
        df["total_fare_bdt"] = (
            df["base_fare_bdt"] + df["tax_surcharge_bdt"]
        )

        # Create route column for route-based analysis
        df["route"] = df["source"] + " → " + df["destination"]

        # Define peak seasons
        peak_seasons = ["Eid", "Winter Holidays"]

        # Create new column for Peak vs Non-Peak comparison
        df["season_type"] = df["seasonality"].apply(
            lambda x: "Peak" if x in peak_seasons else "Non-Peak"
        )

        return df


    
    # 3️. LOAD CLEAN DATA INTO POSTGRESQL
    # ============================================================
    @task
    def load_clean_data(df: pd.DataFrame):
        """
        This task loads cleaned data into PostgreSQL.
        """

        # Connect to PostgreSQL analytics database
        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        # Load clean dataset
        # 'replace' makes it safe to rerun (idempotent pipeline)
        df[[
            "airline", "source", "destination",
            "departure_datetime", "arrival_datetime",
            "duration_hrs", "stopovers", "class",
            "booking_source", "base_fare_bdt",
            "tax_surcharge_bdt", "total_fare_bdt",
            "seasonality", "days_before_departure"
        ]].to_sql(
            "flight_prices_clean",
            engine,
            if_exists="replace",
            index=False
        )

        return df


    
    # 4️. KPI TASKS (RUN IN PARALLEL)
    # ============================================================

    # KPI 1: Average Fare by Airline
    @task
    def kpi_avg_fare(df: pd.DataFrame):

        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        df.groupby("airline")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql("kpi_avg_fare_by_airline",
                    engine,
                    if_exists="replace",
                    index=False)


    # KPI 2: Booking Count by Airline
    @task
    def kpi_booking_count(df: pd.DataFrame):

        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        df.groupby("airline").size().reset_index(name="booking_count") \
            .to_sql("kpi_booking_count_by_airline",
                    engine,
                    if_exists="replace",
                    index=False)


    # KPI 3: Most Popular Routes
    @task
    def kpi_popular_routes(df: pd.DataFrame):

        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        df.groupby("route").size().reset_index(name="booking_count") \
            .sort_values("booking_count", ascending=False) \
            .to_sql("kpi_popular_routes",
                    engine,
                    if_exists="replace",
                    index=False)


    # KPI 4: Seasonal Average Fare
    @task
    def kpi_seasonal(df: pd.DataFrame):

        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        df.groupby("seasonality")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql("kpi_seasonal_fares",
                    engine,
                    if_exists="replace",
                    index=False)


    # KPI 5: Peak vs Non-Peak Comparison
    @task
    def kpi_peak_vs_non_peak(df: pd.DataFrame):

        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")
        engine = pg_hook.get_sqlalchemy_engine()

        df.groupby("season_type")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql("kpi_peak_vs_non_peak_fares",
                    engine,
                    if_exists="replace",
                    index=False)


    # ============================================================
    # DAG EXECUTION FLOW
    # ============================================================

    # Step 1: Extract
    extracted = extract_from_mysql()

    # Step 2: Clean and Transform
    cleaned = validate_and_transform(extracted)

    # Step 3: Load Clean Data
    loaded = load_clean_data(cleaned)

    # Step 4: Run KPI tasks in parallel
    kpi_avg_fare(loaded)
    kpi_booking_count(loaded)
    kpi_popular_routes(loaded)
    kpi_seasonal(loaded)
    kpi_peak_vs_non_peak(loaded)
