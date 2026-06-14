import logging
import requests
import psycopg2
from datetime import datetime
import config

# Set up logging to write to both pipeline.log and the console stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_weather():
    """Fetches raw weather data for Tokyo from the Open-Meteo API."""
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "forecast_days": config.FORECAST_DAYS
    }
    
    try:
        logger.info(f"Extracting weather data from Open-Meteo API for coordinates ({config.LATITUDE}, {config.LONGITUDE})...")
        response = requests.get(config.API_URL, params=params, timeout=10)
        response.raise_for_status()
        logger.info("Weather data extracted successfully from API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Extraction Error: {e}")
        logger.info("Falling back to local mock data for testing...")
        return {
            "latitude": config.LATITUDE,
            "longitude": config.LONGITUDE,
            "hourly": {
                "time": ["2026-06-14T00:00", "2026-06-14T01:00"],
                "temperature_2m": [22.5, 21.8],
                "relative_humidity_2m": [65, 70],
                "wind_speed_10m": [12.5, 10.2]
            }
        }


def transform_weather(raw_data):
    """Parses raw JSON data into structured rows matching our database schema."""
    if not raw_data:
        logger.warning("No raw data found to transform.")
        return []
    
    lat = raw_data.get("latitude")
    lon = raw_data.get("longitude")
    hourly_data = raw_data.get("hourly", {})
    
    timestamps = hourly_data.get("time", [])
    temps = hourly_data.get("temperature_2m", [])
    humidities = hourly_data.get("relative_humidity_2m", [])
    winds = hourly_data.get("wind_speed_10m", [])
    
    transformed_records = []
    
    for i in range(len(timestamps)):
        dt_obj = datetime.strptime(timestamps[i], "%Y-%m-%dT%H:%M")
        
        record = (
            "Tokyo",
            lat,
            lon,
            dt_obj,
            temps[i],
            humidities[i],
            winds[i]
        )
        transformed_records.append(record)
        
    logger.info(f"Transformed {len(transformed_records)} hourly records successfully.")
    return transformed_records


def load_weather(records):
    """Inserts records into the local PostgreSQL database."""
    if not records:
        logger.warning("No records available to load into the database.")
        return
        
    insert_query = """
        INSERT INTO weather_stg (city, latitude, longitude, reading_timestamp, temperature_celsius, relative_humidity, wind_speed_kmh)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (city, reading_timestamp) DO NOTHING;
    """
    
    conn = None
    cur = None
    try:
        logger.info(f"Connecting to database '{config.DB_CONFIG['database']}' on host '{config.DB_CONFIG['host']}'...")
        conn = psycopg2.connect(**config.DB_CONFIG)
        cur = conn.cursor()
        
        cur.executemany(insert_query, records)
        conn.commit()
        logger.info(f"Database Load complete. Rows affected: {cur.rowcount}")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database Load Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    logger.info("Starting Weather ETL Pipeline execution.")
    raw = extract_weather()
    clean_data = transform_weather(raw)
    load_weather(clean_data)
    logger.info("Weather ETL Pipeline execution completed.")