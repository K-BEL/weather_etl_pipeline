#!/bin/bash
# Exit immediately if any command exits with a non-zero status
set -e

echo "============================================="
echo "Starting Weather ETL Pipeline Setup & Runner"
echo "============================================="

# 1. Environment Activation
echo "Step 1: Activating virtual environment..."
if [ -f "venv/to/venv/bin/activate" ]; then
    source venv/to/venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment activation script not found. Running with environment's default Python."
fi

# 2. Install dependencies
echo "Step 2: Installing dependencies..."
pip install -r requirements.txt --quiet

# 3. Running Pipeline
# Note: SQLAlchemy will automatically create the weather_stg table if it does not exist.
echo "Step 3: Executing ETL script..."
python3 etl.py

echo "============================================="
echo "Execution completed successfully!"
echo "============================================="
