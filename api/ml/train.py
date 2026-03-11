import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_score, recall_score
import joblib
import os
import mlflow
import mlflow.sklearn
import time
import requests

mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

mlflow.set_tracking_uri(mlflow_tracking_uri)
mlflow.set_registry_uri(mlflow_tracking_uri)

for i in range(10):
    try:
        mlflow.get_experiment_by_name("Default")
        print("✅ MLflow is ready")
        break
    except Exception:
        print("⏳ Waiting for MLflow...")
        time.sleep(3)
else:
    raise RuntimeError("MLflow server not responding")
mlflow.set_experiment("credit-risk-training")

# -------------------------
# Load processed data
# -------------------------
data_path = "api/ml/data/processed/borrowers_processed.csv"

df = pd.read_csv(data_path)


# -------------------------
# Encode categorical columns
# -------------------------
label_encoders = {}
for col in ["employment_type", "employer_category"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# -------------------------
# Features & target
# -------------------------
X = df.drop(columns=["borrower_id", "loan_default"])
print("Training features:", list(X.columns))
y = df["loan_default"]

# -------------------------
# Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# MLflow tracking starts HERE
# -------------------------
with mlflow.start_run(run_name="credit-risk-training"):

    # Log parameters
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 6)

    # Train model (same as before)
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)
    joblib.dump(list(X.columns), "api/ml/feature_columns.joblib")

    mlflow.log_artifact("api/ml/feature_columns.joblib")

    # Evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)

    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    if len(set(y_test)) > 1:
        roc_auc = roc_auc_score(y_test, y_proba)
        print("ROC AUC:", roc_auc)
        mlflow.log_metric("roc_auc", roc_auc)

    # Log metrics
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    # Log & register model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="credit_risk_model"
    )

    # (Optional for now, keep it)
    joblib.dump(model, "api/ml/credit_risk_model.joblib")

print("Model training completed and logged to MLflow.")

# trigger retraining
