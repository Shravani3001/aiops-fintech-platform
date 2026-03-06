from pymongo import MongoClient
from datetime import datetime, timezone
import os
import time

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI not set in environment variables")

# Wait for MongoDB connection
for i in range(10):
    try:
        mongo = MongoClient(MONGO_URI)
        mongo.admin.command("ping")
        print("MongoDB connected")
        break
    except Exception as e:
        print(f"Mongo not ready, retrying... ({e})")
        time.sleep(2)
else:
    raise Exception("MongoDB not reachable")

db = mongo.get_database()
incidents = db["incidents"]

now = datetime.now(timezone.utc)

seed_data = [
    {
        "metric": "HighPredictionLatency",
        "signature": "HighPredictionLatency:critical",
        "baseline_mean": 0.02,
        "baseline_std": 0.005,
        "severity": "critical",
        "root_cause": "API overloaded or slow model inference",
        "fix_applied": "restart api container",
        "healed": True,
        "source": "manual-seed",
        "created_at": now
    },
    {
        "metric": "High5xxErrorRate",
        "signature": "High5xxErrorRate:critical",
        "baseline_mean": 0.01,
        "baseline_std": 0.005,
        "severity": "critical",
        "root_cause": "Unhandled application error",
        "fix_applied": "restart api container",
        "healed": True,
        "source": "manual-seed",
        "created_at": now
    },
    {
        "metric": "ServiceDown",
        "signature": "ServiceDown:critical",
        "baseline_mean": 1,
        "baseline_std": 0,
        "severity": "critical",
        "root_cause": "Service process crashed",
        "fix_applied": "restart api container",
        "healed": True,
        "source": "manual-seed",
        "created_at": now
    },
    {
        "metric": "TrafficSpike",
        "signature": "TrafficSpike:critical",
        "baseline_mean": 800,
        "baseline_std": 200,
        "severity": "warning",
        "root_cause": "Sudden increase in incoming requests",
        "fix_applied": "monitor",
        "healed": False,
        "source": "manual-seed",
        "created_at": now
    },
    {
        "metric": "ContainerRestartLoop",
        "signature": "ContainerRestartLoop:critical",
        "baseline_mean": 0,
        "baseline_std": 1,
        "severity": "critical",
        "root_cause": "Crash loop due to misconfiguration",
        "fix_applied": "manual investigation",
        "healed": False,
        "source": "manual-seed",
        "created_at": now
    }
]

# Idempotent insert (prevents duplicates)
for incident in seed_data:
    exists = incidents.find_one({
        "metric": incident["metric"],
        "source": "manual-seed"
    })
    if not exists:
        incidents.insert_one(incident)
        print(f"✅ Seeded: {incident['metric']}")
    else:
        print(f"⚠️ Already exists: {incident['metric']}")

print("🎉 Incident seeding completed")