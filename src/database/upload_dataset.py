import pandas as pd
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["grievtech_db"]
collection = db["complaints"]

# Build safe file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "311-service-requests-from-2010-to-present.csv")

chunk_size = 100000  # 100k rows per batch

print("Starting upload...")

for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
    records = chunk.to_dict(orient="records")
    collection.insert_many(records)
    print(f"Inserted {len(records)} records")

print("Upload completed successfully!")

