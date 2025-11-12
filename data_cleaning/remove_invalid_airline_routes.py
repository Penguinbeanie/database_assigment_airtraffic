import csv

def remove_invalid_airline_routes(input_routes_file_path, output_routes_file_path):
    """
    Removes rows from the routes data where the 'Airline ID' column contains '\\N'.

    Args:
        input_routes_file_path (str): Path to the input routes CSV file.
        output_routes_file_path (str): Path to the output cleaned routes CSV file.
    """

    cleaned_rows = []
    try:
        with open(input_routes_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read header
            cleaned_rows.append(header)  # Keep the header

            # Assuming 'Airline ID' is at index 2
            airline_id_idx = 2
            
            for row in reader:
                if len(row) > airline_id_idx and row[airline_id_idx] == '\\N':
                    # Skip this row if 'Airline ID' is '\N'
                    continue
                cleaned_rows.append(row)

    except FileNotFoundError:
        print(f"Error: Input routes file not found at {input_routes_file_path}")
        return
    except Exception as e:
        print(f"Error reading routes file: {e}")
        return

    try:
        with open(output_routes_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_rows)
        print(f"Cleaned data written to {output_routes_file_path}. {len(cleaned_rows) - 1} rows remaining.")
    except Exception as e:
        print(f"Error writing cleaned data to file: {e}")

if __name__ == "__main__":
    input_csv = 'clean_data/routes.csv'
    output_csv = 'clean_data/routes_no_invalid_airlines.csv'
    remove_invalid_airline_routes(input_csv, output_csv)
