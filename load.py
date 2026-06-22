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
    if df.empty:
        logger.warning("No data available to load into the database.")
        return

    try:
        engine = create_engine(config.DATABASE_URI)
        
        df.to_sql(
            name='taxi_stage', 
            con=engine, 
            if_exists='append', 
            index=False
        )
        
        logger.info(f"Successfully loaded {len(df)} records into taxi_stage.")

    except Exception as e:
        logger.error(f"Taxi Load Error: {e}")
