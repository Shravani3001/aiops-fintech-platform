from pymongo import MongoClient
from datetime import datetime, timezone

mongo = MongoClient("mongodb://mongodb:27017/")
db = mongo["credit_risk"]
incidents = db["incidents"]

now = datetime.now(timezone.utc)

seed_data = [
    {
        "metric": "HighPredictionLatency",
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