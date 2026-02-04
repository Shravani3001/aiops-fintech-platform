import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, classification_report

# -------------------------
# Paths
# -------------------------
MODEL_PATH = "api/ml/credit_risk_model.joblib"
DATA_PATH = "api/ml/data/processed/borrowers_processed.csv"

# -------------------------
# Load model & data
# -------------------------
print("Loading model...")
model = joblib.load(MODEL_PATH)

print("Loading processed data...")
df = pd.read_csv(DATA_PATH)

# -------------------------
# Prepare features & target
# -------------------------
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

# -------------------------
# Run predictions
# -------------------------
y_pred = model.predict(X)

# -------------------------
# Evaluation metrics
# -------------------------
print("\nConfusion Matrix:")
cm = confusion_matrix(y_true, y_pred)
print(cm)

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

print(f"\nPrecision (default=1): {precision:.3f}")
print(f"Recall (default=1)   : {recall:.3f}")

print("\nDetailed classification report:")
print(classification_report(y_true, y_pred))

# -------------------------
# Optional: Risk band check
# -------------------------
if hasattr(model, "predict_proba"):
    print("\nSample risk band predictions:")
    probs = model.predict_proba(X)[:, 1]

    def risk_band(p):
        if p < 0.3:
            return "LOW"
        elif p < 0.6:
            return "MEDIUM"
        else:
            return "HIGH"

    sample = pd.DataFrame({
        "borrower_id": df["borrower_id"].head(10),
        "default_probability": probs[:10],
        "risk_band": [risk_band(p) for p in probs[:10]]
    })

    print(sample)