# Import DAG class to define an Airflow workflow
from airflow import DAG

# TaskFlow API decorator to define tasks as Python functions
from airflow.decorators import task

# Hook to connect Airflow with MySQL
from airflow.hooks.mysql_hook import MySqlHook

# Hook to connect Airflow with PostgreSQL
from airflow.hooks.postgres_hook import PostgresHook

# Utility function for defining DAG start date
from airflow.utils.dates import days_ago

# Pandas is used for data validation, transformation, and KPI computation
import pandas as pd


# Define the Airflow DAG
with DAG(
    dag_id="flight_mysql_to_postgres",      # DAG name shown in Airflow UI
    start_date=days_ago(1),                 # DAG can run starting from yesterday
    schedule_interval=None,                 # Run only when triggered manually
    catchup=False,                          # Do not backfill old DAG runs
    tags=["phase3", "analytics"]            # Tags for organization in UI
):

    
    # Extract data from MySQL
    
    @task
    def extract_from_mysql():
        """
        This task extracts raw flight data from the MySQL staging table
        and loads it into a pandas DataFrame.
        """

        # Create MySQL connection using Airflow connection id
        mysql_hook = MySqlHook(mysql_conn_id="mysql_staging")

        # Get SQLAlchemy engine to run SQL queries
        engine = mysql_hook.get_sqlalchemy_engine()

        # Read entire staging table into a pandas DataFrame
        df = pd.read_sql("SELECT * FROM flight_prices_raw", engine)

        # Return DataFrame to the next task
        return df


    
    # Validate and Transform the Data
    
    @task
    def validate_and_transform(df: pd.DataFrame):
        """
        This task performs data validation, cleaning, and transformation.
        """

        # Remove rows with missing critical values
        df = df.dropna(subset=[
            "airline", "source", "destination",
            "base_fare_bdt", "tax_surcharge_bdt"
        ])

        # Remove invalid fare values (negative numbers)
        df = df[
            (df["base_fare_bdt"] >= 0) &
            (df["tax_surcharge_bdt"] >= 0)
        ]

        # Recalculate total fare
        # Ensures consistency even if CSV total fare is incorrect
        df["total_fare_bdt"] = (
            df["base_fare_bdt"] + df["tax_surcharge_bdt"]
        )

        # Create route column (Source → Destination)
        df["route"] = df["source"] + " → " + df["destination"]

        # Define Peak vs Non-Peak seasons
        # Peak seasons are defined using domain knowledge
        peak_seasons = ["Eid", "Winter Holidays"]

        df["season_type"] = df["seasonality"].apply(
            lambda x: "Peak" if x in peak_seasons else "Non-Peak"
        )

        # Return cleaned and transformed DataFrame
        return df


    
    # Load Clean Data & Compute KPIs
    
    @task
    def load_clean_data(df: pd.DataFrame):
        """
        This task loads clean data into PostgreSQL and computes KPIs.
        """

        # Create PostgreSQL connection using Airflow connection id
        pg_hook = PostgresHook(postgres_conn_id="postgres_analytics")

        # Get SQLAlchemy engine
        engine = pg_hook.get_sqlalchemy_engine()

        
        # Load Clean Flight Data
        
        df[[
            "airline", "source", "destination",
            "departure_datetime", "arrival_datetime",
            "duration_hrs", "stopovers", "class",
            "booking_source", "base_fare_bdt",
            "tax_surcharge_bdt", "total_fare_bdt",
            "seasonality", "days_before_departure"
        ]].to_sql(
            "flight_prices_clean",    # Analytics table
            engine,
            if_exists="replace",      # Safe re-runs (idempotent)
            index=False
        )

        
        # KPI 1: Average Fare by Airline
        
        df.groupby("airline")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql(
                "kpi_avg_fare_by_airline",
                engine,
                if_exists="replace",
                index=False
            )

        
        # KPI 2: Booking Count by Airline
        
        df.groupby("airline").size().reset_index(name="booking_count") \
            .to_sql(
                "kpi_booking_count_by_airline",
                engine,
                if_exists="replace",
                index=False
            )

        
        # KPI 3: Most Popular Routes
        
        df.groupby("route").size().reset_index(name="booking_count") \
            .sort_values("booking_count", ascending=False) \
            .to_sql(
                "kpi_popular_routes",
                engine,
                if_exists="replace",
                index=False
            )

        
        # KPI 4a: Average Fare by Season
        
        df.groupby("seasonality")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql(
                "kpi_seasonal_fares",
                engine,
                if_exists="replace",
                index=False
            )

        
        # KPI 4b: Peak vs Non-Peak Fare Comparison
        
        df.groupby("season_type")["total_fare_bdt"].mean().reset_index() \
            .rename(columns={"total_fare_bdt": "avg_total_fare_bdt"}) \
            .to_sql(
                "kpi_peak_vs_non_peak_fares",
                engine,
                if_exists="replace",
                index=False
            )


    # Define task execution order (dependency chain)
    load_clean_data(
        validate_and_transform(
            extract_from_mysql()
        )
    )
