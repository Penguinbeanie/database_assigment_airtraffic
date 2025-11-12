import pandas as pd

def delete_index_column(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'index' in df.columns:
            df = df.drop(columns=['index'])
            df.to_csv(file_path, index=False)
            print(f"Successfully deleted 'index' column from {file_path}")
        else:
            print(f"'index' column not found in {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = "clean_data/airlines.csv"
    delete_index_column(file_path)
