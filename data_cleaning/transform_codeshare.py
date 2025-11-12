import csv

def transform_codeshare_column(input_routes_file_path, output_routes_file_path):
    """
    Transforms the 'Codeshare' column in the routes data:
    - '' or empty strings are translated to '0'.
    - 'Y' is translated to '1'.
    - Other values remain unchanged.

    Args:
        input_routes_file_path (str): Path to the input routes CSV file.
        output_routes_file_path (str): Path to the output transformed routes CSV file.
    """

    transformed_rows = []
    try:
        with open(input_routes_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read header
            transformed_rows.append(header)  # Keep the header

            # Assuming 'Codeshare' is at index 7
            codeshare_idx = 7
            
            for row in reader:
                if len(row) > codeshare_idx:
                    codeshare_value = row[codeshare_idx].strip()
                    if codeshare_value == '':
                        row[codeshare_idx] = '0'
                    elif codeshare_value == 'Y':
                        row[codeshare_idx] = '1'
                transformed_rows.append(row)

    except FileNotFoundError:
        print(f"Error: Input routes file not found at {input_routes_file_path}")
        return
    except Exception as e:
        print(f"Error reading routes file: {e}")
        return

    try:
        with open(output_routes_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(transformed_rows)
        print(f"Transformed data written to {output_routes_file_path}. {len(transformed_rows) - 1} rows remaining.")
    except Exception as e:
        print(f"Error writing transformed data to file: {e}")

if __name__ == "__main__":
    input_csv = 'clean_data/routes.csv'
    output_csv = 'clean_data/routes_transformed_codeshare.csv'
    transform_codeshare_column(input_csv, output_csv)
