# Configuration parameters for Weather ETL Pipeline

# Open-Meteo API configuration
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 34.0209
LONGITUDE = -6.8416
FORECAST_DAYS = 1

# Database connection configuration
import os

# If DB_HOST is not provided, default to localhost
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "weather_stg")
db_user = os.getenv("DB_USER", "root")
db_pass = os.getenv("DB_PASS", "root")

# Construct the URI dynamically
DATABASE_URI = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}"

# Logging configuration
LOG_FILE = "pipeline.log"
