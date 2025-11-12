
import pandas as pd

# Load the mapping file
mapping_df = pd.read_csv('clean_data_mappings/mapped_gdp_countries.csv')

# Create a reversed dictionary for mapping
# We are mapping from the unique country name back to the original name in the GDP file
country_mapping = mapping_df.set_index('Mapped_Unique_Country')['Original_Country_in_GDP'].to_dict()

# Load the airports data
airports_df = pd.read_csv('source_data/airports.csv')

# The airports file has columns: 'id', 'name', 'city', 'country', 'iata', 'icao', 'lat', 'lon', 'alt', 'tz', 'dst', 'tz_name', 'type', 'source'
# We will map the 'country' column.
# We use the .get method on the dictionary to provide a default value (the original country name) if the key is not found.
airports_df['Country'] = airports_df['Country'].apply(lambda x: country_mapping.get(x, x))


# Save the cleaned data
airports_df.to_csv('clean_data/airports.csv', index=False)

print("Airports data cleaned and saved to clean_data/airports.csv")
