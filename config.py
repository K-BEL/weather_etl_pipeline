# Configuration parameters for Weather ETL Pipeline

# Open-Meteo API configuration
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 35.6895
LONGITUDE = 139.6917
FORECAST_DAYS = 1

# Database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres"
}

# Logging configuration
LOG_FILE = "pipeline.log"
