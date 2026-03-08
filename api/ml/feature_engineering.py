import pandas as pd

# Load raw data
raw_path = "api/ml/data/raw/borrowers_raw.csv"
processed_path = "api/ml/data/processed/borrowers_processed.csv"

df = pd.read_csv(raw_path)

# -------------------------
# Feature Engineering
# -------------------------

# EMI to Income Ratio
df["emi_income_ratio"] = (df["emi_amount"] / df["monthly_income"]).round(2)

# Default Rate
df["default_rate"] = df.apply(
    lambda x: round(
        x["past_defaults_count"] / x["total_loans_taken"], 2
    ) if x["total_loans_taken"] > 0 else 0,
    axis=1
)

# Income Stability Score (rule-based)
def calculate_income_stability(row):
    score = 0.3

    if row["employment_type"] == "salaried":
        score += 0.2
    if row["employer_category"] == "govt":
        score += 0.2
    if row["employment_years"] >= 5:
        score += 0.2

    return round(min(score, 1.0), 1)

df["income_stability_score"] = df.apply(calculate_income_stability, axis=1)

# -------------------------
# Save processed data
# -------------------------
df.to_csv(processed_path, index=False)

print("Feature engineering completed. Processed file saved.")