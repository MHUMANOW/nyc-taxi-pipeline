import duckdb
import logging
import os

# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execution.log"),
        logging.StreamHandler()
    ]
)

# 2. Configs
TAXI_TYPES = {
    "Yellow Taxi": "yellow",
    "Green Taxi": "green",
    "High Volume FHV": "fhvhv",
    "Traditional FHV": "fhv",
}
MONTHS = [f"{m:02d}" for m in range(1, 7)]
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
CURATED_DIR = "data/curated"

def get_pickup_column(prefix):
    if prefix == "yellow": return "tpep_pickup_datetime"
    if prefix == "green": return "lpep_pickup_datetime"
    return "pickup_datetime"

def process_and_clean_data():
    logging.info("--- Start Data Pipeline ---")
    for label, prefix in TAXI_TYPES.items():
        for month in MONTHS:
            file_url = f"{BASE_URL}/{prefix}_tripdata_2024-{month}.parquet"
            output_file = f"{CURATED_DIR}/{prefix}_2024_{month}_clean.parquet"
            
            if os.path.exists(output_file):
                logging.info(f"File {output_file} exists, skipping download.")
                continue
                
            pickup_col = get_pickup_column(prefix)
            logging.info(f"Extracting and cleaning: {label} for month {month}")
            
            try:
                query = f"""
                    SELECT * 
                    FROM read_parquet('{file_url}')
                    WHERE {pickup_col} >= '2024-01-01' 
                      AND {pickup_col} < '2024-07-01'
                """
                duckdb.execute(f"COPY ({query}) TO '{output_file}' (FORMAT PARQUET)")
                logging.info(f"✅ Curated data saved: {output_file}")
            except Exception as e:
                logging.warning(f"❌ Skipped {label} month {month}: {e}")

def analyze_most_used():
    logging.info("--- Start Analysis ---")
    results = {}
    for label, prefix in TAXI_TYPES.items():
        file_pattern = f"{CURATED_DIR}/{prefix}_2024_*_clean.parquet"
        try:
            query = f"SELECT count(*) FROM read_parquet('{file_pattern}')"
            total_trips = duckdb.execute(query).fetchone()[0]
            results[label] = total_trips
            logging.info(f"Total trips for {label}: {total_trips:,}")
        except Exception:
            logging.warning(f"No curated data for {label}")
            
    if results:
        most_used = max(results, key=results.get)
        logging.info("=" * 45)
        logging.info(f"🎉 Answer: Most used taxi type is '{most_used}'")
        logging.info(f"Total Trips: {results[most_used]:,}")
        logging.info("=" * 45)

if __name__ == "__main__":
    process_and_clean_data()
    analyze_most_used()
    logging.info("--- Pipeline Completed ---")
