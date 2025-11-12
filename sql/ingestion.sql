-- Drop tables if they exist to make the script idempotent
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS airplanes;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS countries;

-- Create countries table
CREATE TABLE countries (
    "Time" INT NOT NULL,
    "Time_Code" VARCHAR(255),
    "Country_Name" VARCHAR(255) PRIMARY KEY,
    "Country_Code" VARCHAR(10) NOT NULL UNIQUE,
    "GDP_current_US" FLOAT CHECK ("GDP_current_US" >= 0),
    "GDP_per_capita_current_US" FLOAT CHECK ("GDP_per_capita_current_US" >= 0),
    "Political_Stability" FLOAT,
    "Population" FLOAT NOT NULL CHECK ("Population" >= 0)
);

-- Create airlines table
CREATE TABLE airlines (
    "index" INT,
    "Airline_ID" INT PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "Alias" VARCHAR(255),
    "IATA" VARCHAR(10) UNIQUE, -- Can be NULL but must be unique if present
    "ICAO" VARCHAR(10) UNIQUE, -- Can be NULL but must be unique if present
    "Callsign" VARCHAR(255),
    "Country" VARCHAR(255) NOT NULL,
    "Active" BOOLEAN NOT NULL,
    FOREIGN KEY ("Country") REFERENCES countries("Country_Name")
);

-- Create airplanes table
CREATE TABLE airplanes (
    "index" INT,
    "Name" VARCHAR(255) NOT NULL,
    "IATA" VARCHAR(10) UNIQUE, -- Aircraft type codes
    "ICAO" VARCHAR(10) PRIMARY KEY
);

-- Create airports table
CREATE TABLE airports (
    "index" INT,
    "Airport_ID" INT PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "City" VARCHAR(255) NOT NULL,
    "Country" VARCHAR(255) NOT NULL,
    "IATA" VARCHAR(10) UNIQUE,
    "ICAO" VARCHAR(10) UNIQUE,
    "Latitude" FLOAT NOT NULL CHECK ("Latitude" >= -90 AND "Latitude" <= 90),
    "Longitude" FLOAT NOT NULL CHECK ("Longitude" >= -180 AND "Longitude" <= 180),
    "Altitude" INT NOT NULL,
    "Timezone" VARCHAR(255),
    "DST" VARCHAR(1),
    "Tz_database_time_zone" VARCHAR(255),
    "Type" VARCHAR(255) NOT NULL,
    "Source" VARCHAR(255) NOT NULL,
    FOREIGN KEY ("Country") REFERENCES countries("Country_Name")
);

-- Create routes table
CREATE TABLE routes (
    "routes_ID" INT PRIMARY KEY,
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
COPY countries FROM '/docker-entrypoint-initdb.d/aligned_gdp.csv' DELIMITER ',' CSV HEADER;
COPY airlines FROM '/docker-entrypoint-initdb.d/airlines.csv' DELIMITER ',' CSV HEADER;
COPY airplanes FROM '/docker-entrypoint-initdb.d/airplanes.csv' DELIMITER ',' CSV HEADER;
COPY airports FROM '/docker-entrypoint-initdb.d/airports.csv' DELIMITER ',' CSV HEADER;
COPY routes FROM '/docker-entrypoint-initdb.d/routes.csv' DELIMITER ',' CSV HEADER;
