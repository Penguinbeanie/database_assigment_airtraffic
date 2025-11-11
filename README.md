# Global Air Network Socio-Economic Analysis

## Project Overview
This project aims to analyze the structure of the **Global Air Transportation Network** by integrating it with **city-level demographic data** and **country-level economic indicators**. The goal is to move beyond simple network connectivity to explore complex analytical questions regarding how national wealth, city population, and air travel infrastructure correlate, focusing on metrics like network centrality, economic disparity, and infrastructure allocation efficiency.

---

## Data Sources

The project uses a foundation of core aviation data enriched by two external, authoritative sources.

| Source Name | Data Type | Key Linking Fields | URL |
| :--- | :--- | :--- | :--- |
| **Global Air Transportation Network** (Kaggle) | Core Aviation Data | N/A (Internal) | `https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo/data` |
| **SimpleMaps World Cities** | City Population Data | `city`, `country` | `https://simplemaps.com/data/world-cities` |
| **World Bank DataBank** | Country Economic Data | `country` | `https://databank.worldbank.org/reports.aspx?source=2...` |

---

## Database Schema

The database will consist of six primary tables, with linkages defined by the IATA/ICAO codes and common text fields (`City`, `Country`).

### Core Aviation Tables (4)

| Table Name | Description | Key Columns |
| :--- | :--- | :--- |
| `airlines` | Carrier details and operational status. | `Name` (PK), `IATA`, `ICAO`, `Country`, `Active` |
| `airplanes` | Aircraft model and identification codes. | `Name`, `IATA code` (PK), `ICAO code` |
| `airports` | Geographic and infrastructure data for every airport. | `IATA` (PK), `Name`, `City`, `Country`, `Latitude`, `Longitude`, `Type` |
| `routes` | Defined flight segments between two airports. | `Airline` (FK to `airlines.Name`), `Source airport` (FK to `airports.IATA`), `Destination airport` (FK to `airports.IATA`), `Stops`, `Equipment` |

### Enrichment Tables (2)

These tables introduce the socio-economic context for analysis.

| Table Name | Source | Key Columns | Linkage to `airports` |
| :--- | :--- | :--- | :--- |
| `cities_population` | SimpleMaps | **`city`** (PK), **`country`** (PK), `population`, `lat`, `lng` | `airports.City` and `airports.Country` |
| `countries_economic` | World Bank | **`country`** (PK), `GDP_2023`, `GDP_Per_Capita_2023`, `GDP_PPP_2023` | `airports.Country` |

---

### Primary Linkages

1.  **Route Connectivity:** `routes.Source airport` $\leftrightarrow$ `airports.IATA`
2.  **City Demographics:** `airports.City` and `airports.Country` $\leftrightarrow$ `cities_population.city` and `cities_population.country`
3.  **National Economics:** `airports.Country` $\leftrightarrow$ `countries_economic.country`
