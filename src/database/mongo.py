from pymongo import MongoClient

def get_database():

    # Connect to local MongoDB server
    client = MongoClient("mongodb://localhost:27017/")

    # Create (or access) database
    db = client["grievtech_db"]

    return db
