from src.database.mongo_loader import load_complaints

df = load_complaints(limit=5000)
print(df.head())
