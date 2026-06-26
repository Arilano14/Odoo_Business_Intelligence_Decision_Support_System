import os
import sys

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.etl.extract import extract_all
from app.etl.transform import transform_data
from app.etl.load import load_data

def main():
    print("Starting ETL Process...")
    raw_data = extract_all()
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)
    print("ETL Process Completed Successfully!")

if __name__ == "__main__":
    main()
