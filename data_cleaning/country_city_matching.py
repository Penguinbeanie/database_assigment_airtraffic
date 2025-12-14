import os

import pandas as pd
from rapidfuzz import fuzz, process


def extract_country_city_from_airports_csv():
    """
    Extracts unique 'Country' and 'City' columns from the airports.csv file.
    """
    script_dir = os.path.dirname(__file__)
    airports_csv_path = os.path.abspath(
        os.path.join(script_dir, "..", "source_data", "airports.csv")
    )
    clean_data_dir = os.path.abspath(
        os.path.join(script_dir, "..", "clean_data_mappings")
    )

    try:
        df = pd.read_csv(airports_csv_path)

        # Filter out NaN values before getting unique and sorting
        unique_countries = sorted(list(df["Country"].dropna().unique()))
        unique_cities = sorted(list(df["City"].dropna().unique()))

        print("Extracted Unique Countries:", unique_countries)
        print("Extracted Unique Cities:", unique_cities)

        # Ensure the clean_data_mappings directory exists
        os.makedirs(clean_data_dir, exist_ok=True)

        # Save unique countries to a CSV
        countries_df = pd.DataFrame({"Unique_Countries": unique_countries})
        countries_output_path = os.path.join(clean_data_dir, "unique_countries.csv")
        countries_df.to_csv(countries_output_path, index=False)
        print(f"Unique countries saved to: {countries_output_path}")

        # Save unique cities to a CSV
        cities_df = pd.DataFrame({"Unique_Cities": unique_cities})
        cities_output_path = os.path.join(clean_data_dir, "unique_cities.csv")
        cities_df.to_csv(cities_output_path, index=False)
        print(f"Unique cities saved to: {cities_output_path}")

    except FileNotFoundError:
        print(f"Error: The file {airports_csv_path} was not found.")
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


'''
def map_countries_fuzzywuzzy():
    """
    Maps countries from worldcities.csv to unique airport countries using rapidfuzz.
    Saves matched and unmapped countries to CSVs.
    """
    script_dir = os.path.dirname(__file__)
    worldcities_csv_path = os.path.abspath(
        os.path.join(script_dir, "..", "source_data", "worldcities.csv")
    )
    clean_data_dir = os.path.abspath(os.path.join(script_dir, "..", "clean_data_mappings"))
    unique_countries_csv_path = os.path.join(clean_data_dir, "unique_countries.csv")

    country_mapping = {}
    successfully_mapped_unique_countries_worldcities = (
        set()
    )  # To track unique_countries that were mapped TO
    CHUNK_SIZE = 10000  # Process 10,000 rows at a time

    print("\n--- Performing Fuzzy Country Mapping (Worldcities) ---")
    try:
        # Load the list of unique countries to match against (from unique_countries.csv)
        if not os.path.exists(unique_countries_csv_path):
            print(
                f"Error: {unique_countries_csv_path} not found. Please run extract_country_city_from_airports_csv first."
            )
            return
        unique_countries_df = pd.read_csv(unique_countries_csv_path)
        unique_countries_list = (
            unique_countries_df["Unique_Countries"].dropna().tolist()
        )

        if not unique_countries_list:
            print(
                "Warning: No unique countries found in unique_countries.csv to perform fuzzy matching."
            )
            return

        # Read worldcities.csv in chunks and perform fuzzy matching
        for chunk in pd.read_csv(worldcities_csv_path, chunksize=CHUNK_SIZE):
            for country_in_csv in chunk["country"].dropna().unique():
                if country_in_csv not in country_mapping:
                    best_match = process.extractOne(
                        country_in_csv, unique_countries_list
                    )
                    if best_match and best_match[1] >= 90:
                        country_mapping[country_in_csv] = best_match[0]
                        successfully_mapped_unique_countries_worldcities.add(
                            best_match[0]
                        )
                    else:
                        country_mapping[country_in_csv] = None

        # Save successful mappings to CSV
        if country_mapping:
            # Filter out None values for mapped countries before creating DataFrame for successful mappings
            successful_mappings = {
                k: v for k, v in country_mapping.items() if v is not None
            }
            if successful_mappings:
                mapping_df = pd.DataFrame(
                    list(successful_mappings.items()),
                    columns=[
                        "Original_Country_in_Worldcities",
                        "Mapped_Unique_Country",
                    ],
                )
                fuzzy_mapping_output_path = os.path.join(
                    clean_data_dir, "mapped_worldcities_countries.csv"
                )
                mapping_df.to_csv(fuzzy_mapping_output_path, index=False)
                print(
                    f"Fuzzy country mappings (score >= 90) saved to: {fuzzy_mapping_output_path}"
                )
                print("Fuzzy Country Mapping Results (Original -> Mapped):")
                for original, mapped in successful_mappings.items():
                    print(f"  '{original}' -> '{mapped}'")
            else:
                print("No fuzzy country mappings found with score >= 90.")
        else:
            print("No fuzzy country mappings found with score >= 90.")

        # Identify unique_countries that were not mapped TO
        unmapped_unique_countries_worldcities = [
            country
            for country in unique_countries_list
            if country not in successfully_mapped_unique_countries_worldcities
        ]
        if unmapped_unique_countries_worldcities:
            unmapped_df = pd.DataFrame(
                {
                    "Unmapped_Unique_Countries": sorted(
                        unmapped_unique_countries_worldcities
                    )
                }
            )
            unmapped_output_path = os.path.join(
                clean_data_dir, "unmapped_worldcities_countries.csv"
            )
            unmapped_df.to_csv(unmapped_output_path, index=False)
            print(
                f"Unique countries (from unique_countries.csv) not mapped by worldcities.csv saved to: {unmapped_output_path}"
            )
            print(
                "\nUnique Countries (from unique_countries.csv) not mapped by worldcities.csv:"
            )
            for country in unmapped_unique_countries_worldcities:
                print(f"  - {country}")
        else:
            print(
                "All unique countries (from unique_countries.csv) were mapped by worldcities.csv."
            )

    except FileNotFoundError:
        print(
            f"Error: The file {worldcities_csv_path} or {unique_countries_csv_path} was not found."
        )
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during fuzzy mapping: {e}")
'''


def map_countries_to_gdp_fuzzywuzzy():
    """
    Maps countries from country_gdp.csv to unique airport countries using rapidfuzz.
    Saves matched and unmapped countries to CSVs.
    """
    script_dir = os.path.dirname(__file__)
    country_gdp_csv_path = os.path.abspath(
        os.path.join(script_dir, "..", "source_data", "country_gdp.csv")
    )
    clean_data_dir = os.path.abspath(
        os.path.join(script_dir, "..", "clean_data_mappings")
    )
    unique_countries_csv_path = os.path.join(clean_data_dir, "unique_countries.csv")

    country_mapping = {}
    successfully_mapped_unique_countries_gdp = (
        set()
    )  # To track unique_countries that were mapped TO
    CHUNK_SIZE = 10000  # Process 10,000 rows at a time

    print("\n--- Performing Fuzzy Country Mapping (Country GDP) ---")
    try:
        # Load the list of unique countries to match against (from unique_countries.csv)
        if not os.path.exists(unique_countries_csv_path):
            print(
                f"Error: {unique_countries_csv_path} not found. Please run extract_country_city_from_airports_csv first."
            )
            return
        unique_countries_df = pd.read_csv(unique_countries_csv_path)
        unique_countries_list = (
            unique_countries_df["Unique_Countries"].dropna().tolist()
        )

        if not unique_countries_list:
            print(
                "Warning: No unique countries found in unique_countries.csv to perform fuzzy matching."
            )
            return

        # Read country_gdp.csv in chunks and perform fuzzy matching
        for chunk in pd.read_csv(country_gdp_csv_path, chunksize=CHUNK_SIZE):
            for country_in_csv in chunk["Country Name"].dropna().unique():
                if country_in_csv not in country_mapping:
                    best_match = process.extractOne(
                        country_in_csv, unique_countries_list
                    )
                    if best_match and best_match[1] >= 90:
                        country_mapping[country_in_csv] = best_match[0]
                        successfully_mapped_unique_countries_gdp.add(best_match[0])
                    else:
                        country_mapping[country_in_csv] = None

        # Save successful mappings to CSV
        if country_mapping:
            # Filter out None values for mapped countries before creating DataFrame for successful mappings
            successful_mappings = {
                k: v for k, v in country_mapping.items() if v is not None
            }
            if successful_mappings:
                mapping_df = pd.DataFrame(
                    list(successful_mappings.items()),
                    columns=["Original_Country_in_GDP", "Mapped_Unique_Country"],
                )
                fuzzy_mapping_output_path = os.path.join(
                    clean_data_dir, "mapped_gdp_countries.csv"
                )
                mapping_df.to_csv(fuzzy_mapping_output_path, index=False)
                print(
                    f"Fuzzy country mappings (score >= 90) saved to: {fuzzy_mapping_output_path}"
                )
                print("Fuzzy Country Mapping Results (Original -> Mapped):")
                for original, mapped in successful_mappings.items():
                    print(f"  '{original}' -> '{mapped}'")
            else:
                print("No fuzzy country mappings found with score >= 90.")
        else:
            print("No fuzzy country mappings found with score >= 90.")

        # Identify unique_countries that were not mapped TO
        unmapped_unique_countries_gdp = [
            country
            for country in unique_countries_list
            if country not in successfully_mapped_unique_countries_gdp
        ]
        if unmapped_unique_countries_gdp:
            unmapped_df = pd.DataFrame(
                {"Unmapped_Unique_Countries": sorted(unmapped_unique_countries_gdp)}
            )
            unmapped_output_path = os.path.join(
                clean_data_dir, "unmapped_gdp_countries.csv"
            )
            unmapped_df.to_csv(unmapped_output_path, index=False)
            print(
                f"Unique countries (from unique_countries.csv) not mapped by country_gdp.csv saved to: {unmapped_output_path}"
            )
            print(
                "\nUnique Countries (from unique_countries.csv) not mapped by country_gdp.csv:"
            )
            for country in unmapped_unique_countries_gdp:
                print(f"  - {country}")
        else:
            print(
                "All unique countries (from unique_countries.csv) were mapped by country_gdp.csv."
            )

    except FileNotFoundError:
        print(
            f"Error: The file {country_gdp_csv_path} or {unique_countries_csv_path} was not found."
        )
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during fuzzy mapping: {e}")


if __name__ == "__main__":
    extract_country_city_from_airports_csv()
    # map_countries_fuzzywuzzy()
    map_countries_to_gdp_fuzzywuzzy()
