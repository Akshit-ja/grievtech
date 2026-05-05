import os
import json
import joblib
import pandas as pd
import sys

MODELS_DIR = "models"
REGISTRY_PATH = os.path.join(MODELS_DIR, "model_registry.json")

FEATURE_COLUMNS = [
    "borough_encoded",
    "agency_encoded",
    "Year",
    "Month",
    "Day",
    "Hour",
    "Is_Weekend",
    "Part_of_Day"
]

def load_latest_model():
    if not os.path.exists(REGISTRY_PATH):
        print("❌ Model registry not found. Train model first.")
        sys.exit(1)

    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    model_path = os.path.join(MODELS_DIR, registry["latest_model"])

    if not os.path.exists(model_path):
        print(f"❌ Model file missing: {model_path}")
        sys.exit(1)

    model = joblib.load(model_path)
    return model, registry["model_version"]

def preprocess(sample):
    df = pd.DataFrame([sample])
    return df[FEATURE_COLUMNS]

def main():

    sample_input = {
        "borough_encoded": 1,
        "agency_encoded": 2,
        "Year": 2024,
        "Month": 2,
        "Day": 15,
        "Hour": 10,
        "Is_Weekend": 0,
        "Part_of_Day": 2
    }

    model, model_version = load_latest_model()
    print(f"✅ Loaded model version: {model_version}")

    df = preprocess(sample_input)

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    print("\n🔹 Prediction Result")
    print(f"Prediction: {pred}")
    print(f"Probability: {prob:.4f}")
    print(f"Model Version: {model_version}")

if __name__ == "__main__":
    main()