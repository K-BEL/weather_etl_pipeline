#!/bin/bash
# Exit immediately if any command exits with a non-zero status
set -e

echo "============================================="
echo "Starting Weather ETL Pipeline Setup & Runner"
echo "============================================="

# 1. Database Setup
echo "Step 1: Initializing PostgreSQL database schema..."
if command -v psql &> /dev/null; then
    psql -d postgres -f schema.sql
    echo "Database schema initialized successfully."
else
    echo "Error: 'psql' client command not found. Please ensure PostgreSQL is installed and in your PATH."
    exit 1
fi

# 2. Environment Activation
echo "Step 2: Activating virtual environment..."
if [ -f "venv/to/venv/bin/activate" ]; then
    source venv/to/venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Warning: Virtual environment activation script not found. Running with environment's default Python."
fi

# 3. Running Pipeline
echo "Step 3: Executing ETL script..."
python3 etl.py

echo "============================================="
echo "Execution completed successfully!"
echo "============================================="
