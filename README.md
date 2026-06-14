# Weather ETL Pipeline

A simple Python-based Extract, Transform, Load (ETL) pipeline that pulls Tokyo hourly weather forecast data from the Open-Meteo API, parses it, and loads it into a local PostgreSQL database staging table.

## Features
- **Extract**: Fetches coordinates and weather metrics (temperature, relative humidity, wind speed) from the Open-Meteo API.
- **Transform**: Structures raw JSON results into format-compliant records and normalizes timestamps.
- **Load**: Inserts records into a PostgreSQL staging table, ignoring duplicates using database primary keys.
- **Robustness**: 
  - Centralized configuration file (`config.py`).
  - Standard logging framework outputting to both console and `pipeline.log`.
  - Offline mode with mock data fallback if the external API is unreachable or times out.

---

## Prerequisites
- **Python 3.x**
- **PostgreSQL** database running locally

---

## Project Structure
- `etl.py` — The core pipeline runner containing the ETL logic.
- `config.py` — Central configuration parameters (API settings, database configs, logging).
- `requirements.txt` — Project external Python package list.
- `db_set.txt` — SQL DDL statement for database table setup.
- `pipeline.log` — Log outputs written by the pipeline execution.

---

## Installation & Setup

1. **Clone or navigate to the pipeline directory**:
   ```bash
   cd weather_etl_pipeline
   ```

2. **Set up virtual environment (if not already set up)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   Log into your local PostgreSQL instance and create the staging table using the SQL schema provided in `db_set.txt`:
   ```bash
   psql -d postgres -f db_set.txt
   ```
   *Note: If you run this manually, ensure you connect to the correct database name as configured in `config.py`.*

---

## Configuration

Modify the parameters in `config.py` to match your environment:
```python
# config.py
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 35.6895
LONGITUDE = 139.6917
FORECAST_DAYS = 1

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres"
}

LOG_FILE = "pipeline.log"
```

---

## Running the Pipeline

Execute the pipeline using Python:
```bash
python etl.py
```

### Log File
Pipeline progress and errors are captured in `pipeline.log` in the format:
```text
YYYY-MM-DD HH:MM:SS,MS [LEVEL] Message
```
