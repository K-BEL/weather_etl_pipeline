import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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
            "Rabat",
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
