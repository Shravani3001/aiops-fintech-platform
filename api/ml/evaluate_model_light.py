import joblib
import pandas as pd
import json
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    classification_report,
    roc_auc_score
)

MODEL_PATH = "api/ml/credit_risk_model.joblib"
DATA_PATH = "api/ml/data/processed/borrowers_processed.csv"

print("Loading model...")
model = joblib.load(MODEL_PATH)

print("Loading processed data...")
df = pd.read_csv(DATA_PATH)

TARGET_COL = "loan_default"

X = df.drop(columns=[TARGET_COL, "borrower_id"])

X["employment_type"] = X["employment_type"].map({
    "salaried": 0,
    "self-employed": 1
})

X["employer_category"] = X["employer_category"].map({
    "private": 0,
    "government": 1,
    "business": 2
})

y_true = df[TARGET_COL]

y_pred = model.predict(X)

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

print(f"\nPrecision: {precision:.3f}")
print(f"Recall: {recall:.3f}")

print("\nDetailed classification report:")
print(classification_report(y_true, y_pred))

# NEW: ROC AUC
if hasattr(model, "predict_proba"):
    probs = model.predict_proba(X)[:, 1]
    roc_auc = roc_auc_score(y_true, probs)

    print(f"\nROC AUC: {roc_auc:.4f}")

    # SAVE metric for pipeline
    with open("evaluation_metrics.json", "w") as f:
        json.dump({"roc_auc": float(roc_auc)}, f)