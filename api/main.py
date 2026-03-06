from fastapi import FastAPI
from contextlib import asynccontextmanager
import pandas as pd
import time
import asyncio
import os
import joblib
import docker
import json
import logging
import requests
import boto3
from openai import OpenAI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from pymongo import MongoClient
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime, timedelta, timezone
from pymongo.errors import ServerSelectionTimeoutError
from fastapi import Request
from pydantic import BaseModel


client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SAFE_FIXES = {
    "restart service",
    "clear cache",
}
COOLDOWN_MINUTES = 0

BASELINE_FALLBACKS = {
    "HighPredictionLatency": {"mean": 0.02, "std": 0.005},
    "High5xxErrorRate": {"mean": 0.01, "std": 0.005},
    "TrafficSpike": {"mean": 800, "std": 200},
    "ServiceDown": {"mean": 1, "std": 0},
    "ContainerRestartLoop": {"mean": 0, "std": 1},
}
MAX_OPENAI_CALLS_PER_METRIC = 3
MONGO_URI = os.getenv("MONGO_URI")
print(f"[DEBUG] MONGO_URI = {repr(MONGO_URI)}")  # repr() reveals hidden characters

client = None
for i in range(5):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tls=True)
        client.server_info()
        print("✅ MongoDB connected")
        break
    except Exception as e:
        print(f"Mongo connection failed attempt {i+1}: {e}")
        time.sleep(3)

if client is None:
    raise Exception("MongoDB connection failed")

db = client["credit_risk"]
borrowers_col = db["borrowers"]
unknown_events_col = db["unknown_events"]

MODEL_NAME = os.getenv("MODEL_NAME", "credit_risk_model")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")
MODEL_PATH = "/app/ml/credit_risk_model.joblib"
model = None
feature_columns = None

class BorrowerIdRequest(BaseModel):
    borrower_id: str

PREDICTION_COUNT = Counter(
    "credit_model_predictions_total",
    "Total number of prediction requests"
)
PREDICTION_LATENCY = Histogram(
    "credit_model_prediction_latency_seconds",
    "Prediction latency in seconds"
)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, feature_columns
    print("🔥 LIFESPAN STARTED")
    # MongoDB
    try:
      client.admin.command("ping")
      print("✅ MongoDB connected")
    except Exception:
      print("⚠️ MongoDB not available — continuing without blocking")

    # Load model (NO MLflow here)
    try:
        print("🚀 Loading model from file:", MODEL_PATH)
        model = joblib.load(MODEL_PATH)
        feature_columns = joblib.load("/app/ml/feature_columns.joblib")

        print("✅ MODEL LOADED:", type(model))
        print("MODEL FEATURES:", model.feature_names_in_)
    except Exception:
        import traceback
        print("❌ MODEL LOAD FAILED")
        traceback.print_exc()
        model = None

    yield
# ✅ Create app ONLY ONCE
app = FastAPI(lifespan=lifespan)

def serialize_mongo(doc):
    if isinstance(doc, list):
        return [serialize_mongo(item) for item in doc]
    if isinstance(doc, dict):
        return {
            key: serialize_mongo(value)
            for key, value in doc.items()
        }
    if isinstance(doc, ObjectId):
        return str(doc)
    if isinstance(doc, datetime):
        return doc.isoformat()
    return doc

def openai_rca(metric, value, mean, std):
    deviation = (
        "state-change"
        if std == 0
        else round(value / mean, 2) if mean else "unknown"
    )

    prompt = f"""
You are an SRE AIOps assistant.

RULES:
- Return ONLY ONE root cause
- Return ONLY ONE immediate fix
- Fix must be SAFE and operational (restart, scale, cache clear)
- Do NOT provide multiple options
- Do NOT explain alternatives
- Be concise

Context:
Metric: {metric}
Current value: {value}
Normal mean: {mean}
Std deviation: {std}

Respond ONLY in valid JSON with these keys:
- root_cause
- fix
"""
    logging.info(f"Requesting OpenAI RCA for {metric} with current value {value}")
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0,
        response_format={"type": "json_object"}
    )

    try:
        raw_content = response.choices[0].message.content
        logging.warning(f"OpenAI raw response: {raw_content}")
        content = response.choices[0].message.content.strip()
        # Remove accidental markdown fences
        if content.startswith("```"):
           content = content.strip("```").replace("json", "").strip()

        ai_result = json.loads(content)
    except Exception:
        ai_result = {
            "root_cause": "Unable to parse OpenAI response",
            "fix": "manual investigation"
        }

    return {
        "root_cause": ai_result.get("root_cause"),
        "fix": ai_result.get("fix"),
        "analysis": f"Deviation: {deviation}"
    }

def apply_fix(fix: str):
    if fix == "restart service":
        try:
            cluster = os.getenv("ECS_CLUSTER_NAME")
            service = os.getenv("ECS_SERVICE_NAME")
            region  = os.getenv("AWS_DEFAULT_REGION" or "ap-south-1")

            print("DEBUG ECS_CLUSTER_NAME =", cluster)
            print("DEBUG ECS_SERVICE_NAME =", service)
            print("DEBUG AWS_DEFAULT_REGION =", region)
            

            ecs = boto3.client("ecs", region_name=os.getenv("AWS_DEFAULT_REGION"))

            ecs.update_service(
                cluster=cluster,
                service=service,
                forceNewDeployment=True
            )

            print("✅ ECS service redeployment triggered")
            return True

        except Exception as e:
            print("❌ ECS self-heal failed:", e)
            return False

    return False

def in_cooldown(signature: str) -> bool:
    recent = db.incidents.find_one(
        {"signature": signature, "healed": True},
        sort=[("created_at", -1)]
    )

    if not recent:
        return False

    last_time = recent["created_at"]

    # 🔧 FIX: make last_time timezone-aware if needed
    if last_time.tzinfo is None:
        last_time = last_time.replace(tzinfo=timezone.utc)

    return datetime.now(timezone.utc) - last_time < timedelta(minutes=COOLDOWN_MINUTES)

def get_baseline(metric: str):
    past = db.incidents.find_one(
        {"metric": metric},
        sort=[("created_at", -1)]
    )
    if past:
        return past["baseline_mean"], past["baseline_std"]

    fallback = BASELINE_FALLBACKS.get(metric)
    if fallback:
        return fallback["mean"], fallback["std"]

    return 0, 0

def openai_call_allowed(signature: str) -> bool:
    incident = db.incidents.find_one({"signature": signature})
    if incident and incident.get("status") == "known":
        return False
    
    count = db.incidents.count_documents({
        "signature": signature,
        "source": {"$regex": "^openai"}
    })
    return count < MAX_OPENAI_CALLS_PER_METRIC

def notify_slack(metric, severity, value, message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logging.error("SLACK_WEBHOOK_URL not set")
        return

    payload = {
        "text": (
            "🚨 *AIOps Alert*\n"
            f"*Metric:* {metric}\n"
            f"*Severity:* {severity}\n"
            f"*Current value:* {value}\n"
            f"*Message:* {message}"
        )
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code != 200:
            logging.error(f"Slack notify failed: {response.text}")
        else:
            logging.info("✅ Slack notification sent")
    except Exception as e:
        logging.error(f"Slack notify exception: {e}")

@app.post("/predict/borrower-id")
def predict_by_borrower_id(request: BorrowerIdRequest):
    start_time = time.time()

    if model is None:
      raise HTTPException(
        status_code=503,
        detail="Model not loaded"
    )

    borrower_id = request.borrower_id
    if not borrower_id:
        raise HTTPException(status_code=400, detail="borrower_id is required")

    # Fetch borrower from MongoDB
    borrower = borrowers_col.find_one({"borrower_id": borrower_id})
    if not borrower:
       raise HTTPException(status_code=404, detail="Borrower not found")
    borrower["_id"] = str(borrower["_id"])

    # Build model input in the exact order used during training
    data = {col: borrower.get(col) for col in feature_columns}
    df = pd.DataFrame([data])

    # Encode categoricals (same as training)
    df["employment_type"] = df["employment_type"].map({
       "salaried": 0,
       "self-employed": 1
    }).fillna(0)

    df["employer_category"] = df["employer_category"].map({
       "private": 0,
       "govt": 1,
       "business": 2,
       "government": 1
    })
    df = df.fillna(0)
    df = df[feature_columns]
    probability = float(model.predict_proba(df)[0][1])

    latency = time.time() - start_time

    # Update metrics
    PREDICTION_COUNT.inc()
    PREDICTION_LATENCY.observe(latency)

    # Risk band
    if probability < 0.3:
        risk_band = "LOW"
    elif probability < 0.6:
        risk_band = "MEDIUM"
    else:
        risk_band = "HIGH"

    return {
        "borrower_id": borrower_id,
        "default_probability": round(float(probability), 2),
        "risk_band": risk_band,
        "borrower_details": serialize_mongo(borrower),
        "latency_seconds": round(latency, 4)
    }
@app.get("/health/model")
def model_health():
    return {"model_loaded": model is not None}

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code)
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(latency)

    return response

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/incident/analyze")
async def analyze_incident(request: Request):
    logging.warning("🔥 AIOPS ALERT RECEIVED 🔥")

    payload = await request.json()
    logging.warning(json.dumps(payload, indent=2))

    alerts = payload.get("alerts", [])
    if not alerts:
        logging.warning("No alerts found in the payload")
        return {"message": "no alerts received"}

    results = []

    for alert in alerts:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        metric = labels.get("alertname")
        alert_severity = labels.get("severity")  

        if metric == "ServiceDown":
           logging.warning("ServiceDown detected – monitoring only")
           results.append({
             "metric": metric,
             "action": "observed_only"
           })
           continue

        if not metric or not alert_severity:
            logging.warning(f"Skipping alert due to missing metric or severity: {alert}")
            continue

        logging.warning(
            f"Processing alert for metric={metric}, alert_severity={alert_severity}"
        )

        try:
            current_value = float(annotations.get("current_value", 0.0))
        except ValueError:
            current_value = 0.0
        
        baseline_mean, baseline_std = get_baseline(metric)

        # 🔹 COMPUTED SEVERITY (AIOps logic)
        if baseline_std == 0:
            computed_severity = (
                "critical" if current_value != baseline_mean else "warning"
            )
        else:
            computed_severity = (
                "critical"
                if current_value > baseline_mean + 3 * baseline_std
                else "warning"
            )
        signature = f"{metric}:{computed_severity}"

        logging.warning(
            f"Alertmanager severity={alert_severity}, AIOps computed_severity={computed_severity}"
        )
        logging.warning(
            f"Computed severity for {metric}: {computed_severity}"
        )
        
        if metric.startswith("Unknown"):

            rca = openai_rca(metric, current_value, baseline_mean, baseline_std)

            # --- Store discovery history ---
            unknown_events_col.update_one(
                {"metric": metric},
                {
                   "$setOnInsert": {
                      "metric": metric,
                      "first_seen": datetime.now(timezone.utc)
                   },
                   "$set": {
                      "last_seen": datetime.now(timezone.utc),
                      "labels": labels,
                      "annotations": annotations,
                      "openai_root_cause": rca.get("root_cause"),
                      "openai_suggested_fix": rca.get("fix")
                   },
                   "$inc": {"count": 1}
                },
                upsert=True
            )

            # --- ALSO STORE IN INCIDENTS (Learning Memory) ---
            db.incidents.update_one(
                {"signature": signature},
                {
                   "$setOnInsert": {
                       "metric": metric,
                       "signature": signature,
                       "baseline_mean": baseline_mean,
                       "baseline_std": baseline_std,
                       "root_cause": rca.get("root_cause"),
                       "fix_applied": rca.get("fix"),
                       "severity": computed_severity,
                       "source": "openai-unknown-learning",
                       "healed": False,
                       "status": "learning",
                       "retrigger_count": 0,
                       "created_at": datetime.now(timezone.utc)
                   },
                   "$inc": {"occurrence_count": 1},
                   "$set": {"last_seen": datetime.now(timezone.utc)}
                },
                upsert=True
            )

            notify_slack(
              metric,
              computed_severity,
              current_value,
              f"AI RCA: {rca.get('root_cause')} | Suggested fix: {rca.get('fix')} (manual approval required)"
            )

        # 🔹 COOLDOWN CHECK (PLACE IT HERE)
        if in_cooldown(signature):
          logging.warning(f"Incident {signature} is in cooldown. Skipping actions.")
          continue
        

        # 🔹 LOOK FOR PAST INCIDENT (USE COMPUTED SEVERITY)
        past = db.incidents.find_one(
            {"signature": signature}
        )
        if (
              past
              and past.get("occurrence_count", 0) >= 2
              and past.get("status") != "known"
        ):
            db.incidents.update_one(
                {"_id": past["_id"]},
                {"$set": {"status": "known", "promoted_at": datetime.now(timezone.utc)}}
            )

        if past:
            logging.warning(
               f"Found past incident for {metric}, checking auto-fix"
            )

            # 🔁 Always update retrigger info
            db.incidents.update_one(
               {"_id": past["_id"]},
               {
                    "$inc": {"retrigger_count": 1},
                    "$set": {"last_seen": datetime.now(timezone.utc)}
               }
            )

            fix = past["fix_applied"]

            # Special case override
            if metric == "HighPredictionLatency" and computed_severity == "critical":
               fix = "restart service"

            logging.warning(
                f"Auto-heal check → fix='{fix}', in_SAFE_FIXES={fix in SAFE_FIXES}, severity={computed_severity}"
            )

            # ✅ Auto-heal path
            if fix in SAFE_FIXES and computed_severity == "critical":
                healed = apply_fix(fix)

                db.incidents.update_one(
                   {"_id": past["_id"]},
                   {
                     "$set": {
                       "healed": healed,
                       "healing_initiated": True
                     }
                   }
                )

                results.append({
                  "metric": metric,
                  "severity": computed_severity,
                  "action": "auto-heal",
                  "healed": healed
                })
                continue

            # 🚨 Manual / notify-human path
            notify_slack(metric, computed_severity, current_value, fix)

            results.append({
              "metric": metric,
              "severity": computed_severity,
              "action": "notify-human"
            })
            continue
        if not openai_call_allowed(signature):
            notify_slack(
                 metric,
                 computed_severity,
                 current_value,
                 "OpenAI budget exceeded"
            )
            

            db.incidents.update_one(
                {"signature": signature},
                {
                   "$setOnInsert": {
                        "metric": metric,
                        "signature": signature,
                        "baseline_mean": baseline_mean,
                        "baseline_std": baseline_std,
                        "root_cause": "OpenAI budget exceeded",
                        "fix_applied": "manual investigation",
                        "severity": computed_severity,
                        "source": "budget-guard",
                        "healed": False,
                        "status": "learning",
                        "retrigger_count": 0,
                        "created_at": datetime.now(timezone.utc)
                    },
                    "$inc": {"occurrence_count": 1},
                    "$set": {"last_seen": datetime.now(timezone.utc)}
                },
                upsert=True
            )

            results.append({
                 "metric": metric,
                 "severity": computed_severity,
                 "action": "notify-human",
                 "source": "budget-guard"
            })
            continue

        # 🔹 OPENAI RCA
        rca = openai_rca(metric, current_value, baseline_mean, baseline_std)
        fix = rca["fix"]

        if fix in SAFE_FIXES:
            healed = apply_fix(fix)
            source = "openai-auto"
        else:
            healed = False
            notify_slack(metric, computed_severity, current_value, fix)
            source = "openai-escalated"

        db.incidents.update_one(
            {"signature": signature},
            {
                "$setOnInsert": {
                    "metric": metric,
                    "signature": signature,
                    "baseline_mean": baseline_mean,
                    "baseline_std": baseline_std,
                    "root_cause": rca["root_cause"],
                    "fix_applied": fix,
                    "severity": computed_severity,
                    "source": source,
                    "healed": healed,
                    "status": "learning",
                    "retrigger_count": 0,
                    "created_at": datetime.now(timezone.utc)
                },
                "$inc": {"occurrence_count": 1},
                "$set": {"last_seen": datetime.now(timezone.utc)}
            },
            upsert=True
        )
        results.append({
            "metric": metric,
            "severity": computed_severity,
            "action": source,
            "healed": healed,
            "root_cause": rca["root_cause"]
        })

    return {"status": "processed", "results": results}
