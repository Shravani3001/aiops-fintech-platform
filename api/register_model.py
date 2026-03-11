import mlflow
import mlflow.sklearn
import joblib
import json
from mlflow.tracking import MlflowClient

# -------------------------
# MLflow setup
# -------------------------
mlflow.set_tracking_uri("http://3.110.184.81:5000")
mlflow.set_experiment("credit-risk-training")

# -------------------------
# Load trained model
# -------------------------
model = joblib.load("api/ml/credit_risk_model.joblib")

# -------------------------
# Load evaluation metrics
# -------------------------
with open("evaluation_metrics.json") as f:
    metrics = json.load(f)

roc_auc = metrics["roc_auc"]

print("New model ROC AUC:", roc_auc)

# -------------------------
# Log model to MLflow
# -------------------------
with mlflow.start_run() as run:

    mlflow.log_metric("roc_auc", roc_auc)

    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="credit_risk_model"
    )

print("Model logged to MLflow")

# -------------------------
# Compare with production model
# -------------------------
client = MlflowClient()

latest_versions = client.get_latest_versions("credit_risk_model")
new_version = latest_versions[0].version

prod_versions = client.get_latest_versions(
    "credit_risk_model",
    stages=["Production"]
)

# -------------------------
# Promotion logic
# -------------------------
if prod_versions:

    prod_run = client.get_run(prod_versions[0].run_id)
    prod_auc = prod_run.data.metrics.get("roc_auc", 0)

    print("Current Production ROC AUC:", prod_auc)

    if roc_auc > prod_auc:

        print("New model better → promoting to Production")

        client.transition_model_version_stage(
            name="credit_risk_model",
            version=new_version,
            stage="Production"
        )

    else:

        print("New model worse → keeping current Production model")

else:

    print("No production model found → promoting first model")

    client.transition_model_version_stage(
        name="credit_risk_model",
        version=new_version,
        stage="Production"
    )

print("Model registration process complete")