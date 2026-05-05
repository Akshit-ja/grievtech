import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier

from phase5_explainability import run_phase5

print("Starting Explainability Runner...")

model_path = "models/model_v1.pkl"

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv("src/data/complaints.csv", nrows=500)

# Keep only numeric features for the model
X = df.select_dtypes(include=["number"]).fillna(0)

# Create a dummy label if needed
if "Complaint Type" in df.columns:
    y = df["Complaint Type"]
else:
    y = [0] * len(X)

# --------------------------------------------------
# Load or train model
# --------------------------------------------------

if os.path.exists(model_path):

    print("Loading existing model...")

    model = joblib.load(model_path)

else:

    print("Model not found. Training quick model...")

    os.makedirs("models", exist_ok=True)

    model = RandomForestClassifier(n_estimators=50)

    model.fit(X, y)

    joblib.dump(model, model_path)

    print("Model trained and saved to models/model_v1.pkl")

# --------------------------------------------------
# Run SHAP explainability
# --------------------------------------------------

X_sample = X.iloc[:50]

run_phase5(model, X_sample)

print("Explainability pipeline completed successfully.")