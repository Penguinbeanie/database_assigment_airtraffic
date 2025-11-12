import csv

def validate_routes_data(routes_file_path, airlines_file_path, airports_file_path, airplanes_file_path, output_file_path):
    """
    Validates routes data against airlines, airports, and airplanes data.
    Deletes rows from routes.csv if:
    - 'Airline ID' does not exist in airlines.csv
    - 'Source airport ID' does not exist in airports.csv
    - 'Destination airport ID' does not exist in airports.csv
    - 'Equipment' code does not exist in airplanes.csv (IATA code)

    Args:
        routes_file_path (str): Path to the routes CSV file.
        airlines_file_path (str): Path to the airlines CSV file.
        airports_file_path (str): Path to the airports CSV file.
        airplanes_file_path (str): Path to the airplanes CSV file.
        output_file_path (str): Path to the output cleaned routes CSV file.
    """

    # 1. Load valid IDs from reference files into sets for efficient lookup
    valid_airline_ids = set()
    try:
        with open(airlines_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0].strip(): # Ensure ID is not empty or just whitespace
                    valid_airline_ids.add(row[0].strip()) # Airline ID is at index 0
        print(f"Loaded {len(valid_airline_ids)} valid airline IDs. Sample: {list(valid_airline_ids)[:5]}")
    except FileNotFoundError:
        print(f"Error: Airlines file not found at {airlines_file_path}")
        return
    except Exception as e:
        print(f"Error reading airlines file: {e}")
        return

    valid_airport_ids = set()
    try:
        with open(airports_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0].strip(): # Ensure ID is not empty or just whitespace
                    valid_airport_ids.add(row[0].strip()) # Airport ID is at index 0
        print(f"Loaded {len(valid_airport_ids)} valid airport IDs. Sample: {list(valid_airport_ids)[:5]}")
    except FileNotFoundError:
        print(f"Error: Airports file not found at {airports_file_path}")
        return
    except Exception as e:
        print(f"Error reading airports file: {e}")
        return

    valid_equipment_codes = set()
    try:
        with open(airplanes_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header
            for row in reader:
                if len(row) > 1 and row[1].strip(): # IATA code is at index 1, ensure it exists and is not empty
                    valid_equipment_codes.add(row[1].strip())
        print(f"Loaded {len(valid_equipment_codes)} valid equipment codes. Sample: {list(valid_equipment_codes)[:5]}")
    except FileNotFoundError:
        print(f"Error: Airplanes file not found at {airplanes_file_path}")
        return
    except Exception as e:
        print(f"Error reading airplanes file: {e}")
        return

    # 2. Process Routes: Read, validate, and store valid rows
    cleaned_rows = []
    try:
        with open(routes_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read header
            cleaned_rows.append(header)  # Keep the header

            # Assuming column indices for routes.csv:
            # Airline ID: 2
            # Source airport ID: 4
            # Destination airport ID: 6
            # Equipment: 9
            
            airline_id_idx = 2
            source_airport_id_idx = 4
            destination_airport_id_idx = 6
            equipment_idx = 9

            for row in reader:
                # Ensure row has enough columns to avoid IndexError
                if len(row) <= equipment_idx:
                    continue # Skip malformed rows

                # Check Airline ID
                if row[airline_id_idx] not in valid_airline_ids:
                    continue

                # Check Source Airport ID
                if row[source_airport_id_idx] not in valid_airport_ids:
                    continue

                # Check Destination Airport ID
                if row[destination_airport_id_idx] not in valid_airport_ids:
                    continue

                # Check Equipment (can be multiple codes separated by space)
                equipment_codes_in_row = row[equipment_idx].split(' ')
                all_equipment_valid = True
                for code in equipment_codes_in_row:
                    if code and code not in valid_equipment_codes:
                        all_equipment_valid = False
                        break
                
                if not all_equipment_valid:
                    continue

                cleaned_rows.append(row)

    except FileNotFoundError:
        print(f"Error: Routes file not found at {routes_file_path}")
        return
    except Exception as e:
        print(f"Error reading routes file: {e}")
        return

    # 3. Write Output: Write the validated data to a new file
    try:
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_rows)
        print(f"Validated data written to {output_file_path}. {len(cleaned_rows) - 1} rows remaining.")
    except Exception as e:
        print(f"Error writing validated data to file: {e}")

if __name__ == "__main__":
    routes_csv = 'clean_data/routes.csv'
    airlines_csv = 'clean_data/airlines.csv'
    airports_csv = 'clean_data/airports.csv'
    airplanes_csv = 'clean_data/airplanes.csv'
    output_csv = 'clean_data/routes_fully_validated.csv'
    
    validate_routes_data(routes_csv, airlines_csv, airports_csv, airplanes_csv, output_csv)
