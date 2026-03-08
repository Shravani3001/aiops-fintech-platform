import mlflow
import mlflow.sklearn
import joblib

# MLflow tracking server
mlflow.set_tracking_uri("http://localhost:5000")

# Load your model
model = joblib.load("ml/credit_risk_model.joblib")

# Start MLflow run
with mlflow.start_run() as run:
    # Only use 'name', do NOT use 'artifact_path'
    mlflow.sklearn.log_model(model, name="credit_risk_model")
    run_id = run.info.run_id

# Register model
model_uri = f"runs:/{run_id}/credit_risk_model"
mlflow.register_model(model_uri, "credit_risk_model")

print("MODEL REGISTERED")
