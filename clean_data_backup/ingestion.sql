-- Drop tables if they exist to make the script idempotent
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS airplanes;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS countries;

-- Create countries table
CREATE TABLE countries (
    "Time" INT,
    "Time_Code" VARCHAR(255),
    "Country_Name" VARCHAR(255) PRIMARY KEY,
    "Country_Code" VARCHAR(10) UNIQUE,
    "GDP_current_US" FLOAT CHECK ("GDP_current_US" >= 0),
    "GDP_per_capita_current_US" FLOAT CHECK ("GDP_per_capita_current_US" >= 0),
    "Political_Stability" FLOAT,
    "Population" FLOAT CHECK ("Population" >= 0)
);

-- Create airlines table
CREATE TABLE airlines (
    "Airline_ID" INT PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "Alias" VARCHAR(255),
    "IATA" VARCHAR(10) UNIQUE, -- Can be NULL but must be unique if present
    "ICAO" VARCHAR(10) UNIQUE, -- Can be NULL but must be unique if present
    "Callsign" VARCHAR(255),
    "Active" VARCHAR(10)
);

-- Create airplanes table
CREATE TABLE airplanes (
    "Name" VARCHAR(255) NOT NULL,
    "IATA" VARCHAR(10) PRIMARY KEY, -- Aircraft type codes
    "ICAO" VARCHAR(10)
);

-- Create airports table
CREATE TABLE airports (
    "Airport_ID" INT PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "City" VARCHAR(255),
    "Country" VARCHAR(255),
    "IATA" VARCHAR(10) UNIQUE,
    "ICAO" VARCHAR(10) UNIQUE,
    "Latitude" FLOAT CHECK ("Latitude" >= -90 AND "Latitude" <= 90),
    "Longitude" FLOAT CHECK ("Longitude" >= -180 AND "Longitude" <= 180),
    "Altitude" INT,
    "Timezone" VARCHAR(255),
    "DST" VARCHAR(2),
    "Tz_database_time_zone" VARCHAR(255),
    "Type" VARCHAR(255),
    "Source" VARCHAR(255),
    FOREIGN KEY ("Country") REFERENCES countries("Country_Name")
);

-- Create routes table
CREATE TABLE routes (
    "Routes_ID" INT PRIMARY KEY,
    "Airline" VARCHAR(10),
    "Airline_ID" INT NOT NULL,
    "Source_airport" VARCHAR(10),
    "Source_airport_ID" INT NOT NULL,
    "Destination_airport" VARCHAR(10),
    "Destination_airport_ID" INT NOT NULL,
    "Codeshare" VARCHAR(1) CHECK ("Codeshare" IS NULL OR "Codeshare" = 'Y'),
    "Stops" INT NOT NULL CHECK ("Stops" >= 0),
    "Equipment" VARCHAR(255),
    FOREIGN KEY ("Airline_ID") REFERENCES airlines("Airline_ID"),
    FOREIGN KEY ("Source_airport_ID") REFERENCES airports("Airport_ID"),
    FOREIGN KEY ("Destination_airport_ID") REFERENCES airports("Airport_ID")
    -- Trailing comma removed here
);

-- Load data from CSV files
-- ASSUMPTION: All CSV files are now in the mapped directory: /docker-entrypoint-initdb.d/

-- Create a temporary table to load the raw data for countries
CREATE TEMP TABLE tmp_countries (
    "Time" TEXT,
    "Time_Code" TEXT,
    "Country_Name" TEXT,
    "Country_Code" TEXT,
    "GDP_current_US" TEXT,
    "GDP_per_capita_current_US" TEXT,
    "Political_Stability" TEXT,
    "Population" TEXT
);

-- Load data from the CSV file into the temporary table
COPY tmp_countries FROM '/docker-entrypoint-initdb.d/aligned_gdp.csv' DELIMITER ',' CSV HEADER;

-- Insert data from the temporary table into the final countries table
INSERT INTO countries (
    "Time",
    "Time_Code",
    "Country_Name",
    "Country_Code",
    "GDP_current_US",
    "GDP_per_capita_current_US",
    "Political_Stability",
    "Population"
)
SELECT
    NULLIF("Time", '')::INT,
    "Time_Code",
    "Country_Name",
    "Country_Code",
    NULLIF(NULLIF("GDP_current_US", '..'), '')::FLOAT,
    NULLIF(NULLIF("GDP_per_capita_current_US", '..'), '')::FLOAT,
    NULLIF(NULLIF("Political_Stability", '..'), '')::FLOAT,
    NULLIF("Population", '')::FLOAT
FROM tmp_countries
WHERE "Country_Name" IS NOT NULL AND "Country_Name" != '';

-- Drop the temporary table
DROP TABLE tmp_countries;

COPY airlines FROM '/docker-entrypoint-initdb.d/airlines.csv' DELIMITER ',' CSV HEADER NULL '';
COPY airplanes FROM '/docker-entrypoint-initdb.d/airplanes.csv' DELIMITER ',' CSV HEADER NULL '';
COPY airports FROM '/docker-entrypoint-initdb.d/airports.csv' DELIMITER ',' CSV HEADER NULL '';
COPY routes FROM '/docker-entrypoint-initdb.d/routes.csv' DELIMITER ',' CSV HEADER NULL '';
