# Global Air Network Socio-Economic Analysis

## Project Overview
This project aims to analyze the structure of the **Global Air Transportation Network** by integrating it with **country-level economic indicators**. The goal is to move beyond simple network connectivity to explore complex analytical questions regarding how national wealth, city population, and air travel infrastructure correlate, focusing on metrics like network centrality, economic disparity, and infrastructure allocation efficiency.

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
| `airlines` | Carrier details and operational status. | `Name` (PK), `IATA`, `ICAO`, `Country`, `Active` |
| `airplanes` | Aircraft model and identification codes. | `Name`, `IATA code` (PK), `ICAO code` |
| `airports` | Geographic and infrastructure data for every airport. | `IATA` (PK), `Name`, `City`, `Country`, `Latitude`, `Longitude`, `Type` |
| `routes` | Defined flight segments between two airports. | **`Route_ID` (PK)**, `Airline` (FK to `airlines.Name`), `Source airport` (FK to `airports.IATA`), `Destination airport` (FK to `airports.IATA`), `Stops`, `Equipment` |

### Enrichment Tables (1)

This table introduces the socio-economic context for analysis.

| Table Name | Source | Key Columns | Linkage to `airports` |
| :--- | :--- | :--- | :--- |
| `countries` | World Bank | **`Country_Name`** (PK), `Time`, `Time_Code`, `Country_Code`, `GDP_current_US`, `GDP_per_capita_current_US`, `Political_Stability`, `Population` | **Ideal:** `airports.Country` $\leftrightarrow$ `countries.Country_Name` |

---
