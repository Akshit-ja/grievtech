import os
import json
import joblib
import pandas as pd
from datetime import datetime
import logging

from backend.services.drift_service import calculate_drift

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REGISTRY_PATH = os.path.join(MODELS_DIR, "model_registry.json")
LOG_PATH = os.path.join(BASE_DIR, "data", "prediction_logs.csv")

# -------------------------------------------------
# Load Latest Model (Safe + Version Controlled)
# -------------------------------------------------

model = None
MODEL_VERSION = "unregistered"

try:
    if os.path.exists(REGISTRY_PATH):

        with open(REGISTRY_PATH, "r") as f:
            registry = json.load(f)

        latest_model_filename = registry.get("latest_model")

        if latest_model_filename:

            model_path = os.path.join(MODELS_DIR, latest_model_filename)

            if os.path.exists(model_path):

                model = joblib.load(model_path)

                MODEL_VERSION = registry.get(
                    "model_version",
                    latest_model_filename.replace(".pkl", "")
                )

                logger.info(f"Loaded model version: {MODEL_VERSION}")

            else:
                logger.warning("Model file listed in registry not found.")

        else:
            logger.warning("No 'latest_model' defined in registry.")

    else:
        logger.warning("Model registry file not found.")

except Exception as e:
    logger.error(f"Model loading failed: {e}")
    model = None

# -------------------------------------------------
# Feature Columns
# -------------------------------------------------

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

# -------------------------------------------------
# Threshold Configuration
# -------------------------------------------------

CUSTOM_THRESHOLD = 0.40   # Recall Optimization
ALERT_THRESHOLD = 0.80    # High Priority Trigger

# -------------------------------------------------
# Prediction Function
# -------------------------------------------------

def predict(
    borough_encoded: int,
    agency_encoded: int,
    year: int,
    month: int,
    text: str | None = None
):

    if model is None:
        logger.warning("Prediction attempted but model is not loaded.")
        return {
            "prediction": 0,
            "probability": 0.0,
            "threshold_used": CUSTOM_THRESHOLD,
            "alert": None,
            "explanation": [],
            "drift_score": 0.0,
            "model_version": MODEL_VERSION
        }

    now = datetime.utcnow()

    data = {
        "borough_encoded": borough_encoded,
        "agency_encoded": agency_encoded,
        "Year": year,
        "Month": month,
        "Day": now.day,
        "Hour": now.hour,
        "Is_Weekend": 1 if now.weekday() >= 5 else 0,
        "Part_of_Day": (
            0 if now.hour < 6 else
            1 if now.hour < 12 else
            2 if now.hour < 18 else
            3
        )
    }

    df = pd.DataFrame([data])[FEATURE_COLUMNS]

    try:
        # Safer probability handling
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(df)[0][1])
        else:
            # Fallback if predict_proba is unavailable
            raw_prediction = int(model.predict(df)[0])
            probability = float(raw_prediction)

        prediction = int(probability >= CUSTOM_THRESHOLD)

    except Exception as e:
        logger.error(f"Model prediction failed: {e}")
        probability = 0.0
        prediction = 0

    # -------------------------------------------------
    # Alert Logic
    # -------------------------------------------------

    alert_message = None
    if probability >= ALERT_THRESHOLD:
        alert_message = "HIGH PRIORITY – Immediate Administrative Review Recommended"

    # -------------------------------------------------
    # Lightweight Explainability Layer
    # (SHAP can be plugged in later)
    # -------------------------------------------------

    explanation = [
        "Complaint Frequency Pattern",
        "Agency Historical Risk Behaviour",
        "Temporal Trend Indicators"
    ]

    # -------------------------------------------------
    # Drift Monitoring
    # -------------------------------------------------

    drift_score = calculate_drift(text) if text else 0.0

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    result_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "prediction": prediction,
        "probability": round(probability, 4),
        "threshold_used": CUSTOM_THRESHOLD,
        "alert": alert_message,
        "drift_score": drift_score,
        "model_version": MODEL_VERSION
    }

    log_batch([result_log])

    # -------------------------------------------------
    # Final Response
    # -------------------------------------------------

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "threshold_used": CUSTOM_THRESHOLD,
        "alert": alert_message,
        "explanation": explanation,
        "drift_score": drift_score,
        "model_version": MODEL_VERSION
    }

# -------------------------------------------------
# Logging Utility
# -------------------------------------------------

def log_batch(rows: list):

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    df = pd.DataFrame(rows)

    if not os.path.exists(LOG_PATH):
        df.to_csv(LOG_PATH, index=False)
    else:
        df.to_csv(LOG_PATH, mode="a", header=False, index=False)

    logger.info(f"Logged {len(rows)} predictions.")