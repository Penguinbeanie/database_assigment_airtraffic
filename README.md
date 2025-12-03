# Global Air Network Socio-Economic Analysis

## Project Overview

This project aims to analyze the structure of the **Global Air Transportation Network** by integrating it with **country-level economic indicators**. The goal is to move beyond simple network connectivity to explore complex analytical questions regarding how national wealth, stability, and air travel infrastructure correlate.
---

## Setup and Data Ingestion

This project utilizes `compose.yml` to set up the necessary database environment. Data is then ingested into the database using the `ingestion.sql` script, which populates the tables with cleaned and processed data.

---

## Data Sources

The project uses a foundation of core aviation data enriched by external, authoritative sources, with all processed data residing in the `clean_data` directory for ingestion.

| Source Name | Data Type | Key Linking Fields | URL |
| :--- | :--- | :--- | :--- |
| **Global Air Transportation Network** (Kaggle) | Core Aviation Data | N/A (Internal) | `https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo/data` |
| **World Bank DataBank** | Country Economic Data | `country` | `https://databank.worldbank.org/source/world-development-indicators` |

---

## Database Schema

The database will consist of six primary tables. The linkages are defined by aviation codes (IATA/ICAO) and geographical names.

### Core Aviation Tables (4)

| Table Name | Description | Key Columns |
| :--- | :--- | :--- |
| `airlines` | Carrier details and operational status. | `Airline_ID` (PK), `Name`, `Alias`, `IATA`, `ICAO`, `Callsign`, `Active` |
| `airplanes` | Aircraft model and identification codes. | `IATA` (PK), `Name`, `ICAO` |
| `airports` | Geographic and infrastructure data for every airport. | `Airport_ID` (PK), `Name`, `City`, `Country`, `IATA`, `ICAO`, `Latitude`, `Longitude`, `Altitude`, `Timezone`, `DST`, `Tz_database_time_zone`, `Type`, `Source` (FK to `countries.Country_Name`) |
| `routes` | Defined flight segments between two airports. | `Routes_ID` (PK), `Airline` (Name), `Airline_ID` (FK to `airlines.Airline_ID`), `Source_airport` (IATA/ICAO), `Source_airport_ID` (FK to `airports.Airport_ID`), `Destination_airport` (IATA/ICAO), `Destination_airport_ID` (FK to `airports.Airport_ID`), `Codeshare`, `Stops`, `Equipment` |

### Enrichment Tables (1)

This table introduces the socio-economic context for analysis.

| Table Name | Source | Key Columns | Linkage to `airports` |
| :--- | :--- | :--- | :--- |
| `countries` | World Bank | **`Country_Name`** (PK), `Time`, `Time_Code`, `Country_Code`, `GDP_current_US`, `GDP_per_capita_current_US`, `Political_Stability`, `Population` | **Ideal:** `airports.Country` $\leftrightarrow$ `countries.Country_Name` |

---

## Data Cleaning

Our data cleaning process makes sure all the information is accurate and works well together. This involves:

*   **Making Country Names Consistent:** We find all unique country names from airport data. Then, we match country names from the economic (GDP) data to these standard names, creating a lookup table. As a first step, a fuzzy algorithm was used, matching everything above a 90% similarity. What remained was then matched by hand. This is necessary to ensure name consistency across datasets.
*   **Connecting Economic Data:** We link the economic data (GDP) with the airline and airport information. This means we only keep economic data for countries that appear in our aviation data. If a country is in our aviation data but not in the original economic data, we add it with empty economic values.
*   **Cleaning and Checking Flight Routes:**
    *   **Fixing Missing IDs:** If some airport IDs are missing in the flight route data, we try to find them using airport names. If we can't find an ID, we remove that flight route. We also remove routes with airline IDs that aren't valid.
    *   **Standardizing "Codeshare":** The "Codeshare" column (which shows if a flight is shared between airlines) is changed to a simple "0" (no) or "1" (yes).
    *   **Ensuring All Connections Are Correct:** We thoroughly check that every flight route correctly links to existing airline IDs, airport IDs (for departure and arrival), and airplane types. If not, it is removed.
*   **Removing Extra Information:** We remove duplicate ID codes (IATA/ICAO) in the airplane data to make sure each code is unique. Also, an unnecessary "index" column is taken out of the airline data.
*   **Ensuring that each table has a unique and non-null primary key:** For each table, a suitable primary key was selected. If a row had no value, we removed it.

---

# Documentation of Question Design, Adjustments, and Results

##  Database Connection Setup

All analytical SQL queries were executed from a Jupyter Notebook, using a PostgreSQL database running inside Docker. After starting the environment via:

```
docker compose up -d
```

the PostgreSQL server becomes available at:

* **Host:** `localhost`
* **Port:** `5432`
* **User:** `postgres`
* **Password:** `postgres`
* **Database:** `postgres`

We connect to this database using SQLAlchemy:

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
```

All queries are executed using:

```python
pd.read_sql(query, engine)
```

This allows seamless integration between SQL analysis and visualization tools such as Pandas and Matplotlib.

---

# **Analytical Methodology & Question Design**

To explore the structure of the Global Air Transportation Network and its relation to socio-economic indicators, we developed **10 analytical questions**.
These questions required precise SQL queries, and several were refined to match the actual structure and limitations of the available dataset.

Below is a detailed description of each question and how it was adapted.

---

# **Question Adjustment Summary (1–10)**

### **1. Top 10 cities by number of airports**

Straightforward aggregation using the `airports` table.
We filtered out empty city fields and grouped by city + country.

---

### **2. Most commonly used airplane on routes requiring ≥ 1 stop**

Filtered by `Stops >= 1` and counted occurrences of each aircraft type.
Although multi-stop routes are rare in the dataset, SQL implementation is valid.

---

### **3. Percentage of codeshare routes**

The `Codeshare` column was cleaned to boolean (0/1).
The share of codeshare flights among all routes was computed.

---

### **4. Original city-population question → replaced with airport-connectivity question**

**Original intention:**

> Examine correlation between a city’s population and airline diversity at its largest airport.

**Issue:**
Population is available **only at country level**, not city level.

**Revised question:**

> For each country, identify the airport with the highest total traffic (incoming + outgoing routes) and count how many unique airlines serve it.

This preserves the connectivity analysis while fitting available data.

---

### **5. Airports with the highest incoming/outgoing route imbalance**

We define **disparity** as:
$|\text{outgoing routes} - \text{incoming routes}|$
A clear and SQL-friendly metric.

---



### **6. Countries with highest ratio of outgoing routes to GDP per capita**

Calculated total outgoing routes per country, joined with GDP data, and computed:

$\frac{\text{outgoing routes}}{\text{GDP per capita}}$

---

### **7. Original multi-stop city question → replaced with international reachability**

**Original:**

> For each city with more than 1M population, measure average stops to reach major cities.

**Issues:**

* No city population data
* Stops column rarely > 0
* Would require recursive pathfinding (not allowed)

**Revised question:**

> For each country, how many unique destination countries can be reached directly?

This produced meaningful results (e.g., France ≈ 112 reachable countries).

---

### **8. Top 10 countries by inbound airline diversity**

For each country, we counted distinct airlines flying into its airports.
Shows how attractive a country is as a destination market.

---

### **9. Aircraft types used on the largest number of distinct routes**

The `Equipment` column contains space-separated aircraft codes.
Using `regexp_split_to_table`, we normalized these and counted distinct routes per aircraft type.
Revealed dominance of Airbus A320/319/321 and Boeing 737 variants.

---

### **10. Countries with the highest percentage of domestic routes**

Defined **domestic route share** as:

$\frac{\text{domestic routes}}{\text{all routes departing from that country}}$

Filtered to include only countries with ≥ 100 outgoing routes.
Highlights differences between large domestic markets (USA, China, Brazil…) and hub-focused countries (Singapore, Qatar…).

---
