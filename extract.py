import logging
import requests
import config

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
