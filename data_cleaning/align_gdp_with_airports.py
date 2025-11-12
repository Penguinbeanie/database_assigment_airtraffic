
import pandas as pd

# Load the cleaned airports data
airports_df = pd.read_csv('clean_data/airports.csv')
airport_countries = set(airports_df['Country'].unique())

# Load the original GDP data
gdp_df = pd.read_csv('source_data/country_gdp.csv')

# 1. Filter gdp_df to remove countries not in airports.csv
gdp_df_filtered = gdp_df[gdp_df['Country Name'].isin(airport_countries)].copy()

# 2. Find countries in airports.csv but not in country_gdp.csv
gdp_countries = set(gdp_df['Country Name'].unique())
missing_countries = airport_countries - gdp_countries

# Create a dataframe for the missing countries
if missing_countries:
    missing_df = pd.DataFrame(list(missing_countries), columns=['Country Name'])
    # Add other columns from gdp_df with NaN values
    for col in gdp_df.columns:
        if col != 'Country Name':
            missing_df[col] = pd.NA
    
    # Reorder columns to match gdp_df
    missing_df = missing_df[gdp_df.columns]

    # Concatenate the two dataframes
    final_gdp_df = pd.concat([gdp_df_filtered, missing_df], ignore_index=True)
else:
    final_gdp_df = gdp_df_filtered

# Save the new dataframe to a new csv file
final_gdp_df.to_csv('clean_data/aligned_gdp.csv', index=False)

print("Aligned GDP data saved to clean_data/aligned_gdp.csv")
