from pymongo import MongoClient
import pandas as pd

def load_complaints(limit=None):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["grievtech_db"]
    collection = db["complaints"]

    cursor = collection.find({}, {"_id": 0})

    if limit:
        cursor = cursor.limit(limit)

    data = list(cursor)
    df = pd.DataFrame(data)

    print(f"Loaded {len(df)} records from MongoDB")

    return df
