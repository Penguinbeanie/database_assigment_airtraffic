import pandas as pd

# Load the mapping file
mapping_df = pd.read_csv('clean_data_mappings/mapped_gdp_countries.csv')

# Create a reversed dictionary for mapping
# We are mapping from the unique country name back to the original name in the GDP file
country_mapping = mapping_df.set_index('Mapped_Unique_Country')['Original_Country_in_GDP'].to_dict()

# Load the airlines data
airlines_df = pd.read_csv('source_data/airlines.csv')

# The airlines file has columns: 'id', 'name', 'alias', 'iata', 'icao', 'callsign', 'country', 'active'
# We will map the 'country' column.
# We use the .get method on the dictionary to provide a default value (the original country name) if the key is not found.
airlines_df['Country'] = airlines_df['Country'].apply(lambda x: country_mapping.get(x, x))


# Save the cleaned data
airlines_df.to_csv('clean_data/airlines.csv', index=False)

print("Airlines data cleaned and saved to clean_data/airlines.csv")