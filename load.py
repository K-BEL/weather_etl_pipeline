# pyrefly: ignore [missing-import]
import logging
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
import config
from models import Base, WeatherStage

logger = logging.getLogger(__name__)

def load_weather(records):
    """Inserts records into the local PostgreSQL database using SQLAlchemy."""
    if not records:
        logger.warning("No records available to load into the database.")
        return
        
    try:
        logger.info("Connecting to database using SQLAlchemy...")
        engine = create_engine(config.DATABASE_URI)
        
        # Auto-create the table if it doesn't exist
        Base.metadata.create_all(engine)
        
        # Map tuple records to dictionaries matching column names
        data_to_insert = [
            {
                "city": r[0],
                "latitude": r[1],
                "longitude": r[2],
                "reading_timestamp": r[3],
                "temperature_celsius": r[4],
                "is_hot": r[5],
                "relative_humidity": r[6],
                "wind_speed_kmh": r[7]
            }
            for r in records
        ]
        
        # Build PostgreSQL specific upsert statement
        stmt = insert(WeatherStage)
        stmt_on_conflict = stmt.on_conflict_do_nothing(
            index_elements=["city", "reading_timestamp"]
        )
        
        with engine.begin() as conn:
            result = conn.execute(stmt_on_conflict, data_to_insert)
            logger.info(f"Database Load complete. Rows affected: {result.rowcount}")
            
    except Exception as e:
        logger.error(f"Database Load Error: {e}")


def load_taxi(df):
    """Inserts records into the local PostgreSQL database using SQLAlchemy."""
    if df.empty:
        logger.warning("No records available to load into the database.")
        return
        
    try:
        logger.info("Connecting to database using SQLAlchemy...")
        engine = create_engine(config.DATABASE_URI)
        
        # Auto-create the table if it doesn't exist
        Base.metadata.create_all(engine)
        
        # Map tuple records to dictionaries matching column names
        data_to_insert = [
            {
                "'VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime',
       'passenger_count', 'trip_distance', 'RatecodeID', 'store_and_fwd_flag',
       'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount', 'extra',
       'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge',
       'total_amount', 'congestion_surcharge', 'Airport_fee',
       'cbd_congestion_fee'": r[0],
                
            }
            for r in records
        ]
        
        # Build PostgreSQL specific upsert statement
        stmt = insert(WeatherStage)
        stmt_on_conflict = stmt.on_conflict_do_nothing(
            index_elements=["city", "reading_timestamp"]
        )
        
        with engine.begin() as conn:
            result = conn.execute(stmt_on_conflict, data_to_insert)
            logger.info(f"Database Load complete. Rows affected: {result.rowcount}")
            
    except Exception as e:
        logger.error(f"Database Load Error: {e}")