Github Repository: 

Disclaimer: For an ideal viewing experience, open the root/README.html in your browser.

# Global Air Network Socio-Economic Analysis

## Project Overview

This project aims to analyze the structure of the **Global Air Transportation Network** by integrating it with **country-level economic indicators**. The goal is to move beyond simple network connectivity to explore complex analytical questions regarding how national wealth, stability, and air travel infrastructure correlate.
---

## Setup and Data Ingestion

This project utilizes `compose.yml` to set up the necessary database environment. Data is then ingested into the database using the `ingestion.sql` script, which populates the tables with cleaned and processed data.

---

## Data Sources

This project combines data from two main sources: one for aviation and one for country-level economics. After cleaning, the final datasets are stored in the `clean_data` folder, ready to be loaded into the database.

| Source | Description | Files & Row Counts | URL |
| :--- | :--- | :--- | :--- |
| **Global Air Transportation Network** (Kaggle) | Core aviation data, valid for 2022. | `routes.csv` (67,661), `airports.csv` (7,697), `airlines.csv` (6,162), `airplanes.csv` (246) | `https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo/data` |
| **World Bank DataBank** | Economic and social data, valid for 2023. | `country_gdp.csv` (265 rows), covering GDP, political stability, and population size. | `https://databank.worldbank.org/source/world-development-indicators` |

---

## Database Schema

The database will consist of six primary tables. The linkages are defined by aviation codes (IATA/ICAO) and geographical names.

### Core Aviation Tables (4)

| Table Name | Description | Key Columns                                                                                                                                                                                                                                                                                                          |
| :--- | :--- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `airlines` | Carrier details and operational status. | `Airline_ID` (PK), `Name`, `Alias`, `IATA`, `ICAO`, `Callsign`, `Active`                                                                                                                                                                                                                                             |
| `airplanes` | Aircraft model and identification codes. | `IATA` (PK), `Name`, `ICAO`                                                                                                                                                                                                                                                                                          |
| `airports` | Geographic and infrastructure data for every airport. | `Airport_ID` (PK), `Name`, `City`, `Country`, `IATA`, `ICAO`, `Latitude`, `Longitude`, `Altitude`, `Timezone`, `DST`, `Tz_database_time_zone`, `Type`, `Source` (FK to `countries.Country_Name`)                                                                                                                     |
| `routes` | Defined flight segments between two airports. | `Routes_ID` (PK), `Airline` (Name), `Airline_ID` (FK to `airlines.Airline_ID`), `Source_airport` (IATA/ICAO), `Source_airport_ID` (FK to `airports.Airport_ID`), `Destination_airport` (IATA/ICAO), `Destination_airport_ID` (FK to `airports.Airport_ID`), `Codeshare`, `Stops`, `Equipment` (FK to airplanes.IATA) |

### Enrichment Tables (1)

This table introduces the socio-economic context for analysis.

| Table Name | Source | Key Columns | Linkage to `airports`                                         |
| :--- | :--- | :--- |:--------------------------------------------------------------|
| `countries` | World Bank | **`Country_Name`** (PK), `Time`, `Time_Code`, `Country_Code`, `GDP_current_US`, `GDP_per_capita_current_US`, `Political_Stability`, `Population` | `airports.Country` $\leftrightarrow$ `countries.Country_Name` |

---

## Data Cleaning

To get the data ready for analysis, we performed the following cleaning steps:

### 1. Standardizing Values
- **Fixing Null Values**: The source files used different ways to show null values (like `\N` or `<null>`). We standardized these to be consistent.
- **Standardizing Booleans**: We changed fields like `Codeshare` to use a simple `1` (for true) or `0` (for false) instead of text like 'Y'.
- **Cleaning Up Text**: We removed extra spaces and empty strings from text fields.

### 2. Ensuring Data Integrity
- **Handling Primary Keys**: We made sure every row in a table had a primary key. If a row was missing its key, we removed it.
- **Removing Duplicates**: We deleted any rows that were exact duplicates of each other.
- **Removing Conflicting Rows**: In some cases, the same primary key was used for different rows. We removed these conflicting entries, as they likely represented outdated data.
- **Removing Incomplete Rows**: We got rid of rows that were mostly empty because they weren't useful for analysis.

### 3. Combining and Validating Datasets
- **Matching Country Names**: The country names in the aviation and economic datasets didn't always match (e.g., "Bahamas" vs "Bahamas, The").

  For example, some country name mismatches we found:

  | World Bank Name   | Kaggle Name       |
  | :---------------- | :---------------- |
  | "Bahamas, The"    | "Bahamas"         |
  | "North Macedonia" | "Macedonia"       |
  | "Myanmar"         | "Burma"           |
  - We used a fuzzy-matching script (`rapidfuzz`) to automatically match names that were over 90% similar.
  - We manually fixed the rest of the names that didn't get matched.
  - Finally, we only kept economic data for countries that were present in our airport data.
- **Validating Routes**: We checked that every flight route correctly linked to an existing airline and airport. If a route had an invalid ID, we removed it.

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


## Question 1 (Basic RA: Select + Projection)

### Which airlines are inactive? Provide ID and name.


```python
query_question01 = """
SELECT 
    "Airline_ID",
    "Name"
FROM airlines
WHERE "Active" = 'N';
"""
q1_df = pd.read_sql(query_question01, engine)
q1_df
```

**Query Result:**

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Airline_ID</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>135 Airways</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>2 Sqn No 1 Elementary Flying Training School</td>
    </tr>
    <tr>
      <th>2</th>
      <td>5</td>
      <td>213 Flight Unit</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6</td>
      <td>223 Flight Unit State Airline</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7</td>
      <td>224th Flight Unit</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4901</th>
      <td>20963</td>
      <td>Atlantic Air Cargo</td>
    </tr>
    <tr>
      <th>4902</th>
      <td>21056</td>
      <td>Dummy</td>
    </tr>
    <tr>
      <th>4903</th>
      <td>21181</td>
      <td>Air Andaman (2Y)</td>
    </tr>
    <tr>
      <th>4904</th>
      <td>21240</td>
      <td>TDA Toa Domestic Airlines</td>
    </tr>
    <tr>
      <th>4905</th>
      <td>21251</td>
      <td>Lynx Aviation (L3/SSX)</td>
    </tr>
  </tbody>
</table>
<p>4906 rows × 2 columns</p>
</div>

## Relational Algebra Question 01

![Relational Algebra Diagram](Q1RA.jpeg)

## Question 2 (Basic RA: Union)

### Show all airprts located in either Germany or Austria. Include name, city, and country.


```python
query_question02 = """
SELECT 
    "Name",
    "City",
    "Country"
FROM airports
WHERE "Country" = 'Germany'
UNION
SELECT 
    "Name",
    "City",
    "Country"
FROM airports
WHERE "Country" = 'Austria'
"""

q2_df = pd.read_sql(query_question02, engine)
q2_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>City</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Hamburg Airport</td>
      <td>Hamburg</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Geilenkirchen Air Base</td>
      <td>Geilenkirchen</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Vilshofen Airport</td>
      <td>Vilshofen</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>3</th>
      <td>St. Johann In Tirol Airport</td>
      <td>St. Johann in Tirol</td>
      <td>Austria</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Wipperfürth-Neye Airport</td>
      <td>Wipperfuerth</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>264</th>
      <td>Hohn Air Base</td>
      <td>Hohn</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>265</th>
      <td>Rügen Airport</td>
      <td>Ruegen</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>266</th>
      <td>Torgau-Beilrode Airport</td>
      <td>Gransee</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>267</th>
      <td>Aalen-Heidenheim/Elchingen Airport</td>
      <td>Aalen-heidenheim</td>
      <td>Germany</td>
    </tr>
    <tr>
      <th>268</th>
      <td>Rothenburg/Görlitz Airport</td>
      <td>Rothenburg/ol</td>
      <td>Germany</td>
    </tr>
  </tbody>
</table>
<p>269 rows × 3 columns</p>
</div>

## Relational Algebra Question 02

![Relational Algebra Diagram](Q2Ra.jpeg)

## Question 3 (Extended RA: Join)

### Show all routes with one stop with the name of the airline, the departure and arrival airports (IATA codes).

```python
query_question03 = """
SELECT 
    a."Name",
    r."Source_airport",
    r."Destination_airport"
FROM routes r
JOIN airlines a ON r."Airline_ID" = a."Airline_ID"
WHERE r."Stops" = 1
"""

q3_df = pd.read_sql(query_question03, engine)
q3_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Source_airport</th>
      <th>Destination_airport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Canadian North</td>
      <td>YRT</td>
      <td>YEK</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Air Canada</td>
      <td>ABJ</td>
      <td>BRU</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Air Canada</td>
      <td>YVR</td>
      <td>YBL</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cubana de Aviación</td>
      <td>FCO</td>
      <td>HAV</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AirTran Airways</td>
      <td>HOU</td>
      <td>SAT</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AirTran Airways</td>
      <td>MCO</td>
      <td>ORF</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Scandinavian Airlines System</td>
      <td>ARN</td>
      <td>GEV</td>
    </tr>
  </tbody>
</table>
</div>

## Relational Algebra Question 03

![Relational Algebra Diagram](Q3RA.jpeg)

![Relational Algebra Diagram](Q3RA2.jpeg)

## Question 4 (Extended RA: Aggregate Functions)

### How many routes does each airline have?


```python
query_question04 = """
SELECT 
    a."Name",
    COUNT(*) AS Route_Count
FROM routes r
JOIN airlines a ON r."Airline_ID" = a."Airline_ID"
GROUP BY a."Name"
HAVING COUNT(*) > 80;
"""
q4_df = pd.read_sql(query_question04, engine)
q4_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>route_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Air Bourbon</td>
      <td>210</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TransAsia Airways</td>
      <td>92</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Air India Limited</td>
      <td>364</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Meridiana</td>
      <td>140</td>
    </tr>
    <tr>
      <th>4</th>
      <td>EVA Air</td>
      <td>114</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>136</th>
      <td>LOT Polish Airlines</td>
      <td>114</td>
    </tr>
    <tr>
      <th>137</th>
      <td>Sriwijaya Air</td>
      <td>106</td>
    </tr>
    <tr>
      <th>138</th>
      <td>LAN Airlines</td>
      <td>285</td>
    </tr>
    <tr>
      <th>139</th>
      <td>Iberia Airlines</td>
      <td>797</td>
    </tr>
    <tr>
      <th>140</th>
      <td>Philippine Airlines</td>
      <td>144</td>
    </tr>
  </tbody>
</table>
<p>141 rows × 2 columns</p>
</div>

![Relational Algebra Diagram](Q4RA.jpeg)

## Question 5 (Extended RA: Aggregate Functions)

### Which countries have the highest percentage of domestic routes?

```python
query_question05 = """
WITH route_with_countries AS (
    SELECT
        r."Routes_ID",
        src_c."Country_Name"  AS src_country,
        dest_c."Country_Name" AS dest_country
    FROM routes r
    JOIN airports src_a 
        ON r."Source_airport" = src_a."IATA"
    JOIN countries src_c 
        ON src_a."Country" = src_c."Country_Name"
    JOIN airports dest_a 
        ON r."Destination_airport" = dest_a."IATA"
    JOIN countries dest_c 
        ON dest_a."Country" = dest_c."Country_Name"
),
route_stats AS (
    SELECT
        src_country AS country,
        COUNT(*) AS total_routes,
        COUNT(*) FILTER (WHERE src_country = dest_country) AS domestic_routes
    FROM route_with_countries
    GROUP BY src_country
)
SELECT
    country,
    total_routes,
    domestic_routes,
    domestic_routes::FLOAT / total_routes AS domestic_share
FROM route_stats
WHERE total_routes >= 100
ORDER BY domestic_share DESC
LIMIT 15;
"""

q5_df = pd.read_sql(query_question05, engine)
q5_df

```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>total_routes</th>
      <th>domestic_routes</th>
      <th>domestic_share</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>China</td>
      <td>7894</td>
      <td>6743</td>
      <td>0.854193</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Brazil</td>
      <td>1325</td>
      <td>1129</td>
      <td>0.852075</td>
    </tr>
    <tr>
      <th>2</th>
      <td>French Polynesia</td>
      <td>108</td>
      <td>91</td>
      <td>0.842593</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Indonesia</td>
      <td>817</td>
      <td>603</td>
      <td>0.738066</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Iran, Islamic Rep.</td>
      <td>356</td>
      <td>257</td>
      <td>0.721910</td>
    </tr>
    <tr>
      <th>5</th>
      <td>United States</td>
      <td>7508</td>
      <td>5382</td>
      <td>0.716835</td>
    </tr>
    <tr>
      <th>6</th>
      <td>India</td>
      <td>1145</td>
      <td>773</td>
      <td>0.675109</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Australia</td>
      <td>836</td>
      <td>557</td>
      <td>0.666268</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Argentina</td>
      <td>253</td>
      <td>166</td>
      <td>0.656126</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Colombia</td>
      <td>337</td>
      <td>219</td>
      <td>0.649852</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Chile</td>
      <td>155</td>
      <td>97</td>
      <td>0.625806</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Philippines</td>
      <td>393</td>
      <td>240</td>
      <td>0.610687</td>
    </tr>
    <tr>
      <th>12</th>
      <td>New Zealand</td>
      <td>188</td>
      <td>114</td>
      <td>0.606383</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Venezuela, RB</td>
      <td>145</td>
      <td>81</td>
      <td>0.558621</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Norway</td>
      <td>410</td>
      <td>222</td>
      <td>0.541463</td>
    </tr>
  </tbody>
</table>
</div>

![Relational Algebra Diagram](Q5Ra.jpeg)

## Question 6 (Extended RA: Aggregate Functions)

### Which aircraft types (Equipment codes) appear on the largest number of distinct routes

```python
query_question06 = """
WITH expanded_equipment AS (
    SELECT
        r."Routes_ID",
        trim(equip) AS equipment
    FROM routes r,
         regexp_split_to_table(r."Equipment", ' ') AS equip
    WHERE trim(equip) <> ''
)

SELECT
    equipment,
    COUNT(DISTINCT "Routes_ID") AS route_count
FROM expanded_equipment
GROUP BY equipment
ORDER BY route_count DESC
LIMIT 10;
"""
q6_df = pd.read_sql(query_question06, engine)
q6_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>equipment</th>
      <th>route_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>320</td>
      <td>14844</td>
    </tr>
    <tr>
      <th>1</th>
      <td>738</td>
      <td>9745</td>
    </tr>
    <tr>
      <th>2</th>
      <td>319</td>
      <td>7338</td>
    </tr>
    <tr>
      <th>3</th>
      <td>321</td>
      <td>3379</td>
    </tr>
    <tr>
      <th>4</th>
      <td>737</td>
      <td>2628</td>
    </tr>
    <tr>
      <th>5</th>
      <td>E90</td>
      <td>1816</td>
    </tr>
    <tr>
      <th>6</th>
      <td>AT7</td>
      <td>1529</td>
    </tr>
    <tr>
      <th>7</th>
      <td>333</td>
      <td>1517</td>
    </tr>
    <tr>
      <th>8</th>
      <td>73G</td>
      <td>1406</td>
    </tr>
    <tr>
      <th>9</th>
      <td>332</td>
      <td>1386</td>
    </tr>
  </tbody>
</table>
</div>

![Relational Algebra Diagram](Q6RA.jpeg)

## Question 7 (Extended RA: Aggregate Functions)

### What is the average number of unique destination countries reachable from each country


```python
query_question7 = """
SELECT
    origin_c."Country_Name" AS origin_country,
    COUNT(DISTINCT dest_c."Country_Name") AS reachable_countries
FROM routes r
JOIN airports origin_a ON r."Source_airport" = origin_a."IATA"
JOIN countries origin_c ON origin_a."Country" = origin_c."Country_Name"
JOIN airports dest_a ON r."Destination_airport" = dest_a."IATA"
JOIN countries dest_c ON dest_a."Country" = dest_c."Country_Name"
GROUP BY origin_c."Country_Name"
ORDER BY reachable_countries DESC;
"""
q7_df = pd.read_sql(query_question7, engine)
q7_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>origin_country</th>
      <th>reachable_countries</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>112</td>
    </tr>
    <tr>
      <th>1</th>
      <td>United Kingdom</td>
      <td>98</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>96</td>
    </tr>
    <tr>
      <th>3</th>
      <td>United States</td>
      <td>90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Turkiye</td>
      <td>90</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>217</th>
      <td>Falkland Islands</td>
      <td>1</td>
    </tr>
    <tr>
      <th>218</th>
      <td>Tuvalu</td>
      <td>1</td>
    </tr>
    <tr>
      <th>219</th>
      <td>Saint Pierre and Miquelon</td>
      <td>1</td>
    </tr>
    <tr>
      <th>220</th>
      <td>Niue</td>
      <td>1</td>
    </tr>
    <tr>
      <th>221</th>
      <td>Samoa</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>222 rows × 2 columns</p>
</div>

![Relational Algebra Diagram](Q7RA.jpeg)

## Question 8 (Extended RA: Aggregate Functions)

### What are the top 5 countries where the ratio of total outgoing routes (from all airports in the country) to the country's GDP per Capita is the highest?


```python
query_question08 = """
WITH outgoing_per_country AS (
    SELECT 
        a."Country",
        COUNT(*) AS outgoing_routes
    FROM routes r
    JOIN airports a 
        ON r."Source_airport_ID" = a."Airport_ID"
    GROUP BY a."Country"
),
country_with_gdp AS (
    SELECT
        c."Country_Name",
        c."GDP_per_capita_current_US"
    FROM countries c
    WHERE c."GDP_per_capita_current_US" IS NOT NULL
      AND c."GDP_per_capita_current_US" > 0
)
SELECT 
    og."Country",
    og.outgoing_routes,
    cg."GDP_per_capita_current_US" AS gdp_per_capita,
    (og.outgoing_routes / cg."GDP_per_capita_current_US") AS ratio
FROM outgoing_per_country og
JOIN country_with_gdp cg
    ON og."Country" = cg."Country_Name"
ORDER BY ratio DESC
LIMIT 5;
"""

q8_df = pd.read_sql(query_question08, engine)
q8_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Country</th>
      <th>outgoing_routes</th>
      <th>gdp_per_capita</th>
      <th>ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>China</td>
      <td>8013</td>
      <td>12951.178240</td>
      <td>0.618708</td>
    </tr>
    <tr>
      <th>1</th>
      <td>India</td>
      <td>1145</td>
      <td>2530.120313</td>
      <td>0.452548</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pakistan</td>
      <td>249</td>
      <td>1365.169274</td>
      <td>0.182395</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Indonesia</td>
      <td>817</td>
      <td>4876.307745</td>
      <td>0.167545</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Madagascar</td>
      <td>65</td>
      <td>508.718428</td>
      <td>0.127772</td>
    </tr>
  </tbody>
</table>
</div>

![Relational Algebra Diagram](Q8RA.jpeg)

## Question 9 (Extended RA: Aggregate Functions)

### Which airports have the largest disparity between the number of outgoing and incoming routes?

```python
query_question9 = """
WITH outgoing AS (
    SELECT 
        r."Source_airport_ID" AS airport_id,
        COUNT(*) AS outgoing_count
    FROM routes r
    GROUP BY r."Source_airport_ID"
),
incoming AS (
    SELECT 
        r."Destination_airport_ID" AS airport_id,
        COUNT(*) AS incoming_count
    FROM routes r
    GROUP BY r."Destination_airport_ID"
),
combined AS (
    SELECT
        a."Airport_ID",
        a."Name",
        a."City",
        a."Country",
        COALESCE(o.outgoing_count, 0) AS outgoing_count,
        COALESCE(i.incoming_count, 0) AS incoming_count,
        ABS(COALESCE(o.outgoing_count, 0) - COALESCE(i.incoming_count, 0)) AS disparity
    FROM airports a
    LEFT JOIN outgoing o ON a."Airport_ID" = o.airport_id
    LEFT JOIN incoming i ON a."Airport_ID" = i.airport_id
)
SELECT *
FROM combined
ORDER BY disparity DESC
LIMIT 10;
"""
q9_df = pd.read_sql(query_question9, engine)
q9_df
```

**Query Result:**

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Airport_ID</th>
      <th>Name</th>
      <th>City</th>
      <th>Country</th>
      <th>outgoing_count</th>
      <th>incoming_count</th>
      <th>disparity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2006</td>
      <td>Auckland International Airport</td>
      <td>Auckland</td>
      <td>New Zealand</td>
      <td>79</td>
      <td>99</td>
      <td>20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2074</td>
      <td>Prince Mohammad Bin Abdulaziz Airport</td>
      <td>Madinah</td>
      <td>Saudi Arabia</td>
      <td>34</td>
      <td>50</td>
      <td>16</td>
    </tr>
    <tr>
      <th>2</th>
      <td>73</td>
      <td>Halifax / Stanfield International Airport</td>
      <td>Halifax</td>
      <td>Canada</td>
      <td>19</td>
      <td>30</td>
      <td>11</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4059</td>
      <td>Jomo Kenyatta International Airport</td>
      <td>Nairobi</td>
      <td>Kenya</td>
      <td>97</td>
      <td>107</td>
      <td>10</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3941</td>
      <td>Eleftherios Venizelos International Airport</td>
      <td>Athens</td>
      <td>Greece</td>
      <td>166</td>
      <td>176</td>
      <td>10</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1638</td>
      <td>Humberto Delgado Airport (Lisbon Portela Airport)</td>
      <td>Lisbon</td>
      <td>Portugal</td>
      <td>194</td>
      <td>202</td>
      <td>8</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3862</td>
      <td>Portland International Jetport Airport</td>
      <td>Portland</td>
      <td>United States</td>
      <td>1</td>
      <td>9</td>
      <td>8</td>
    </tr>
    <tr>
      <th>7</th>
      <td>346</td>
      <td>Munich Airport</td>
      <td>Munich</td>
      <td>Germany</td>
      <td>326</td>
      <td>318</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1382</td>
      <td>Charles de Gaulle International Airport</td>
      <td>Paris</td>
      <td>France</td>
      <td>476</td>
      <td>469</td>
      <td>7</td>
    </tr>
    <tr>
      <th>9</th>
      <td>3861</td>
      <td>Louis Armstrong New Orleans International Airport</td>
      <td>New Orleans</td>
      <td>United States</td>
      <td>70</td>
      <td>77</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>

![Relational Algebra Diagram](Q9RA.jpeg)

## Question 10 (Extended RA: Aggregate Functions)

### What are the top 10 cities globally, based on the total number of airports?

```python
query_question10 = """
SELECT 
    a."City",
    a."Country",
    COUNT(*) AS airport_count,
    STRING_AGG(a."Name", ', ' ORDER BY a."Name") AS airport_names
FROM airports a
WHERE a."City" IS NOT NULL
  AND a."City" <> ''
GROUP BY a."City", a."Country"
ORDER BY airport_count DESC
LIMIT 10;
"""

q10_df = pd.read_sql(query_question10, engine)
q10_df
```

**Query Result:**

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Country</th>
      <th>airport_count</th>
      <th>airport_names</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Columbus</td>
      <td>United States</td>
      <td>8</td>
      <td>Bolton Field, Columbus Metropolitan Airport, C...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>New York</td>
      <td>United States</td>
      <td>6</td>
      <td>Downtown-Manhattan/Wall St Heliport, Indianola...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Moscow</td>
      <td>Russian Federation</td>
      <td>6</td>
      <td>Bykovo Airport, Domodedovo International Airpo...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>London</td>
      <td>United Kingdom</td>
      <td>6</td>
      <td>London City Airport, London Gatwick Airport, L...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jacksonville</td>
      <td>United States</td>
      <td>6</td>
      <td>Cecil Airport, Jacksonville Executive at Craig...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Houston</td>
      <td>United States</td>
      <td>6</td>
      <td>Andrau Airpark, David Wayne Hooks Memorial Air...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Atlanta</td>
      <td>United States</td>
      <td>5</td>
      <td>Cobb County-Mc Collum Field, DeKalb Peachtree ...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Greenville</td>
      <td>United States</td>
      <td>5</td>
      <td>Donaldson Field Airport, Greenville Downtown A...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Izmir</td>
      <td>Turkiye</td>
      <td>5</td>
      <td>Adnan Menderes International Airport, Çiğli Ai...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Vancouver</td>
      <td>Canada</td>
      <td>5</td>
      <td>Coal Harbour Seaplane Base, Harbour (Public) H...</td>
    </tr>
  </tbody>
</table>
</div>

![Relational Algebra Diagram](Q10RA.jpeg)

