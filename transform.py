import logging
from datetime import datetime
import pandas as pd
import numpy as np

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
            "hot" if temps[i] > 25 else "cold",
            humidities[i],
            winds[i]
        )
        transformed_records.append(record)
        
    logger.info(f"Transformed {len(transformed_records)} hourly records successfully.")
    return transformed_records


def transform_taxi_data(df):
    if df.empty:
        logger.warning("No raw data found to transform.")
        return []

    # 1. Cast Dates
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    # 2. Clean Metrics
    # Ensure distance is positive
    df = df[df['trip_distance'] > 0]
    
    # 3. Handle specific Flag columns
    # Convert 'Y'/'N' to 1/0 for SQL friendliness
    df['store_and_fwd_flag'] = df['store_and_fwd_flag'].map({'Y': 1, 'N': 0})
    
    # 4. Fill NaNs in monetary columns
    cols = ['fare_amount', 'tip_amount', 'total_amount', 'passenger_count', 'Airport_fee']
    df[cols] = df[cols].fillna(0)
    
    return df
