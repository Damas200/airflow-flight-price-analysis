# Import the DAG class to define an Airflow workflow
from airflow import DAG

# Import the task decorator (TaskFlow API)
from airflow.decorators import task

# Import MySQL hook to connect Airflow with MySQL
from airflow.hooks.mysql_hook import MySqlHook

# Utility function to define DAG start date
from airflow.utils.dates import days_ago

# Pandas is used for reading and processing CSV data
import pandas as pd


# Define the Airflow DAG
with DAG(
    dag_id="flight_csv_to_mysql",          # Name of the DAG (appears in Airflow UI)
    start_date=days_ago(1),                # DAG can run from yesterday
    schedule_interval=None,                # DAG runs only when triggered manually
    catchup=False,                         # Do not run past (backfill) executions
    tags=["phase2", "staging"]             # Tags to organize DAGs in Airflow UI
):

    # Define a task to load CSV data into MySQL
    @task
    def load_csv_to_mysql():
        """
        This task:
        1. Reads the flight price CSV file
        2. Renames columns to database-friendly names
        3. Converts date columns to datetime format
        4. Loads the data into MySQL staging table
        """

        # Read CSV file from Airflow data directory
        df = pd.read_csv(
            "/opt/airflow/data/Flight_Price_Dataset_of_Bangladesh.csv"
        )

        # Rename CSV columns to match database naming conventions
        # (lowercase, no spaces, consistent naming)
        df = df.rename(columns={
            "Airline": "airline",
            "Source": "source",
            "Source Name": "source_name",
            "Destination": "destination",
            "Destination Name": "destination_name",
            "Departure Date & Time": "departure_datetime",
            "Arrival Date & Time": "arrival_datetime",
            "Duration (hrs)": "duration_hrs",
            "Stopovers": "stopovers",
            "Aircraft Type": "aircraft_type",
            "Class": "class",
            "Booking Source": "booking_source",
            "Base Fare (BDT)": "base_fare_bdt",
            "Tax & Surcharge (BDT)": "tax_surcharge_bdt",
            "Total Fare (BDT)": "total_fare_bdt",
            "Seasonality": "seasonality",
            "Days Before Departure": "days_before_departure"
        })

        # Convert date columns from string to datetime format
        # This ensures correct storage and future time-based analysis
        df["departure_datetime"] = pd.to_datetime(df["departure_datetime"])
        df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"])

        # Create MySQL connection using Airflow connection (mysql_staging)
        mysql_hook = MySqlHook(mysql_conn_id="mysql_staging")

        # Get SQLAlchemy engine for writing data using pandas
        engine = mysql_hook.get_sqlalchemy_engine()

        # Load data into MySQL staging table
        # if_exists="replace" ensures idempotency (safe re-runs)
        df.to_sql(
            name="flight_prices_raw",   # Table name in MySQL
            con=engine,                 # Database connection
            if_exists="replace",        # Replace table if it already exists
            index=False                 # Do not store pandas index
        )

    # Execute the task inside the DAG
    load_csv_to_mysql()

