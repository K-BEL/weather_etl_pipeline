-- Create a fresh table to hold hourly weather readings
CREATE TABLE IF NOT EXISTS weather_stg (
    city VARCHAR(50),
    latitude NUMERIC(6, 4),
    longitude NUMERIC(7, 4),
    reading_timestamp TIMESTAMP,
    temperature_celsius NUMERIC(4, 1),
    relative_humidity NUMERIC(3, 0),
    wind_speed_kmh NUMERIC(4, 1),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Composite primary key ensures we don't load duplicate data for the same city/time
    PRIMARY KEY (city, reading_timestamp)
);
