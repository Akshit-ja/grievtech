from fastapi import APIRouter
from backend.schemas import PredictionRequest
from backend.model_loader import load_model, log_prediction, compute_drift
from backend.metrics_store import increment_predictions, update_accuracy, metrics
import logging
import numpy as np

router = APIRouter()
logger = logging.getLogger(__name__)

model, feature_names = load_model()

DRIFT_THRESHOLD = 0.2


@router.post("/predict")
def predict(data: PredictionRequest):
    try:
        features_dict = {
            "borough_encoded": data.borough_encoded,
            "agency_encoded": data.agency_encoded,
            "Year": data.Year,
            "Month": data.Month,
            "Day": data.Day,
            "Hour": data.Hour,
            "Is_Weekend": data.Is_Weekend,
            "Part_of_Day": data.Part_of_Day
        }

        features = np.array([list(features_dict.values())])

        prediction = int(model.predict(features)[0])
        probs = model.predict_proba(features)[0]
        confidence = round(max(probs) * 100, 2)

        increment_predictions()

        log_prediction({**features_dict, "prediction": prediction})

        drift_score = compute_drift(features_dict)
        metrics["drift_score"] = drift_score

        metrics["drift_alert"] = drift_score > DRIFT_THRESHOLD

        update_accuracy(prediction, data.true_label)

        logger.info("Prediction successful.")

        return {
            "prediction": prediction,
            "confidence": confidence,
            "risk": ["Low", "Medium", "High"][prediction],
            "drift_score": drift_score,
            "drift_alert": metrics["drift_alert"],
            "accuracy": metrics["accuracy"],
            "model_version": metrics["model_version"]
        }

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return {"error": str(e)}