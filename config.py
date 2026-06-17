# Configuration parameters for Weather ETL Pipeline

# Open-Meteo API configuration
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 34.0209
LONGITUDE = -6.8416
FORECAST_DAYS = 1

# Database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres"
}
DATABASE_URI = "postgresql+psycopg2://@localhost/postgres"

# Logging configuration
LOG_FILE = "pipeline.log"
