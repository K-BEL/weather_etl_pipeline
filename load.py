import logging
import psycopg2
import config

logger = logging.getLogger(__name__)

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
