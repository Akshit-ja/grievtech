import os
import joblib
import shap
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# -----------------------------
# Load Model Once (Startup)
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

model = joblib.load(MODEL_PATH)
explainer = shap.TreeExplainer(model)

MODEL_VERSION = "1.0.0"


# -----------------------------
# Request Schema
# -----------------------------

class PredictRequest(BaseModel):
    borough_encoded: int
    agency_encoded: int
    Year: int
    Month: int
    Day: int
    Hour: int
    Is_Weekend: int
    Part_of_Day: int


# -----------------------------
# Prediction Route
# -----------------------------

@router.post("/predict")
def predict(request: PredictRequest):

    # Convert request to DataFrame
    input_df = pd.DataFrame([request.dict()])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # SHAP explanation
    shap_values = explainer.shap_values(input_df)

    feature_impact = dict(
        zip(
            input_df.columns,
            shap_values[0].tolist()
        )
    )

    # Dummy drift score example
    drift_score = 0.02

    return {
        "prediction": int(prediction),
        "drift_score": float(drift_score),
        "model_version": MODEL_VERSION,
        "explanation": feature_impact
    }