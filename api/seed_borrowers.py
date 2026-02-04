import pandas as pd
from pymongo import MongoClient
import time

MONGO_URI = "mongodb://mongodb:27017/"

# Wait for MongoDB
for i in range(10):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("MongoDB connected")
        break
    except Exception:
        print("Mongo not ready, retrying...")
        time.sleep(2)
else:
    raise Exception("MongoDB not reachable")

db = client["credit_risk"]
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
