import logging
import config
from extract import extract_weather
from transform import transform_weather
from load import load_weather

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

if __name__ == "__main__":
    logger.info("Starting Weather ETL Pipeline execution.")
    
    # 1. Extract
    raw = extract_weather()
    
    # 2. Transform
    clean_data = transform_weather(raw)
    
    # 3. Load
    load_weather(clean_data)
    
    logger.info("Weather ETL Pipeline execution completed.")