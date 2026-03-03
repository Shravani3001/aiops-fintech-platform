import pandas as pd
from pymongo import MongoClient
import time
import os

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not set in environment variables")

# Wait for MongoDB
for i in range(10):
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")
        print("MongoDB connected")
        break
    except Exception:
        print(f"Mongo not ready, retrying... ({e})")
        time.sleep(2)
else:
    raise Exception("MongoDB not reachable")

db = client.get_database()
borrowers = db["borrowers"]

# Load processed borrowers
df = pd.read_csv("/app/api/ml/data/processed/borrowers_processed.csv")

records = df.to_dict(orient="records")

inserted = 0
for record in records:
    if "borrower_id" not in record:
        continue

    if not borrowers.find_one({"borrower_id": record["borrower_id"]}):
        borrowers.insert_one(record)
        inserted += 1

print(f"Seeding completed. Inserted {inserted} borrowers.")
