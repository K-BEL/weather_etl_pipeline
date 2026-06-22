import logging, json, psycopg2, pandas as pd
from config import TAXI_FILE_LIST
from extract import extract_weather, extract_taxi_parquet
from transform import transform_weather, transform_taxi_data
from load import load_weather

# Set up logging to write to both pipeline.log and the console stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting Weather ETL Pipeline execution.")
    
    # 1. Extract
    # raw = extract_weather()

    df = pd.concat([extract_taxi_parquet(file) for file in TAXI_FILE_LIST], ignore_index=True)
    # print(json.dumps(raw, indent=4, default=str))
    
    # 2. Transform
    #clean_data = transform_weather(raw)
    #print(json.dumps(clean_data, indent=4, default=str))

    taxi_clean = transform_taxi_data(df)
    print(taxi_clean)
    
    # 3. Load
    #load_weather(clean_data)