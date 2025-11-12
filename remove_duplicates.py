import pandas as pd

file_path = "clean_data/airplanes.csv"

try:
    df = pd.read_csv(file_path)

    # Identify duplicates in 'IATA' and 'ICAO' columns
    # For IATA, consider non-empty strings as potential duplicates
    iata_duplicates = df[
        df["IATA"].duplicated(keep=False) & (df["IATA"].notna()) & (df["IATA"] != "")
    ]
    # For ICAO, consider non-empty strings as potential duplicates
    icao_duplicates = df[
        df["ICAO"].duplicated(keep=False) & (df["ICAO"].notna()) & (df["ICAO"] != "")
    ]

    # Replace duplicate IATA values with None (which will be written as empty string in CSV)
    for iata_val in iata_duplicates["IATA"].unique():
        if iata_val:  # Ensure it's not an empty string or NaN
            df.loc[df["IATA"] == iata_val, "IATA"] = None

    # Replace duplicate ICAO values with None (which will be written as empty string in CSV)
    for icao_val in icao_duplicates["ICAO"].unique():
        if icao_val:  # Ensure it's not an empty string or NaN
            df.loc[df["ICAO"] == icao_val, "ICAO"] = None

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"Successfully processed and updated {file_path}")

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
