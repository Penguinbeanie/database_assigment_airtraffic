import csv

def clean_routes_data(routes_file_path, airports_file_path):
    """
    Cleans the routes data by replacing '\\N' airport IDs with actual IDs
    from the airports data, or deleting rows if no ID is found.

    Args:
        routes_file_path (str): Path to the routes CSV file.
        airports_file_path (str): Path to the airports CSV file.
    """

    # 1. Load Airports: Create a dictionary mapping airport names to their IDs
    airport_name_to_id = {}
    try:
        with open(airports_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Skip header
            # Assuming 'Airport ID' is at index 0 and 'Name' is at index 1
            for row in reader:
                if len(row) > 1:
                    airport_id = row[0]
                    airport_name = row[1]
                    airport_name_to_id[airport_name] = airport_id
    except FileNotFoundError:
        print(f"Error: Airports file not found at {airports_file_path}")
        return
    except Exception as e:
        print(f"Error reading airports file: {e}")
        return

    # 2. Process Routes: Read, clean, and store valid rows
    cleaned_rows = []
    try:
        with open(routes_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read header
            cleaned_rows.append(header)  # Keep the header

            # Assuming column indices:
            # Source airport: 3
            # Source airport ID: 4
            # Destination airport: 5
            # Destination airport ID: 6
            
            source_airport_name_idx = 3
            source_airport_id_idx = 4
            destination_airport_name_idx = 5
            destination_airport_id_idx = 6

            for row in reader:
                if len(row) < 7:  # Ensure row has enough columns
                    continue # Skip malformed rows

                keep_row = True
                
                # Check Source Airport ID
                if row[source_airport_id_idx] == '\\N':
                    source_airport_name = row[source_airport_name_idx]
                    if source_airport_name in airport_name_to_id:
                        row[source_airport_id_idx] = airport_name_to_id[source_airport_name]
                    else:
                        keep_row = False # Mark for deletion if ID not found
                        # print(f"Deleting row due to unknown Source Airport: {source_airport_name}")

                # Check Destination Airport ID (only if row is still to be kept)
                if keep_row and row[destination_airport_id_idx] == '\\N':
                    destination_airport_name = row[destination_airport_name_idx]
                    if destination_airport_name in airport_name_to_id:
                        row[destination_airport_id_idx] = airport_name_to_id[destination_airport_name]
                    else:
                        keep_row = False # Mark for deletion if ID not found
                        # print(f"Deleting row due to unknown Destination Airport: {destination_airport_name}")
                
                if keep_row:
                    cleaned_rows.append(row)

    except FileNotFoundError:
        print(f"Error: Routes file not found at {routes_file_path}")
        return
    except Exception as e:
        print(f"Error reading routes file: {e}")
        return

    # 3. Write Output: Write the cleaned data to a new routes file
    try:
        output_routes_file_path = routes_file_path.replace('.csv', '_cleaned.csv')
        with open(output_routes_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_rows)
        print(f"Cleaned data written to {output_routes_file_path}. {len(cleaned_rows) - 1} rows remaining.")
    except Exception as e:
        print(f"Error writing cleaned data to file: {e}")

if __name__ == "__main__":
    routes_csv = 'clean_data/routes.csv'
    airports_csv = 'clean_data/airports.csv'
    clean_routes_data(routes_csv, airports_csv)
