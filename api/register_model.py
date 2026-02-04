import mlflow
import mlflow.sklearn
import joblib

mlflow.set_tracking_uri("http://localhost:5000")

model = joblib.load("/app/credit_risk_model.joblib")

with mlflow.start_run() as run:
    mlflow.sklearn.log_model(model, artifact_path="model")
    run_id = run.info.run_id

model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "credit_risk_model")

print("MODEL REGISTERED")
