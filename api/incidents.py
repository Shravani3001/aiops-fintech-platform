from datetime import datetime, timezone

def store_incident(db, incident):
    now = datetime.now(timezone.utc)

    existing = db.incidents.find_one({"metric": incident["metric"]})

    if existing:
        db.incidents.update_one(
            {"_id": existing["_id"]},
            {
                "$set": {
                    "last_seen": now
                },
                "$inc": {
                    "retrigger_count": 1
                }
            }
        )
        return "updated"
    else:
        incident["created_at"] = now
        incident["retrigger_count"] = 1
        db.incidents.insert_one(incident)
        return "created"

def create_incident(
    metric,
    current_value,
    baseline_mean,
    baseline_std,
    severity,
    root_cause,
    fix_applied,
    healed,
    source="manual",
    notes=""
):
    return {
        "metric": metric,
        "current_value": current_value,
        "baseline_mean": baseline_mean,
        "baseline_std": baseline_std,
        "severity": severity,
        "detected_at": datetime.now(timezone.utc),

        "root_cause": root_cause,
        "fix_applied": fix_applied,
        "healed": healed,

        "source": source,
        "notes": notes
    }