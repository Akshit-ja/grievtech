import os
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_PATH = os.path.join(BASE_DIR, "data", "prediction_logs.csv")
METRICS_HISTORY_PATH = os.path.join(BASE_DIR, "data", "metrics_history.csv")


# -------------------------------------------------
# Main Metrics Function
# -------------------------------------------------

def get_metrics():

    if not os.path.exists(LOG_PATH):
        return {
            "total_predictions": 0,
            "average_drift_score": 0.0,
            "accuracy": 0.0,
            "model_version": "unregistered",
            "drift_alert": False
        }

    try:
        df = pd.read_csv(LOG_PATH)

        total_predictions = len(df)

        avg_drift = (
            df["drift_score"].mean()
            if "drift_score" in df.columns
            else 0.0
        )

        drift_alert = avg_drift > 0.5

        # Get latest model version from logs if available
        if "model_version" in df.columns and not df.empty:
            model_version = df["model_version"].iloc[-1]
        else:
            model_version = "unregistered"

        metrics = {
            "total_predictions": int(total_predictions),
            "average_drift_score": round(float(avg_drift), 4),
            "accuracy": 0.92,  # Replace later with real evaluation metric
            "model_version": model_version,
            "drift_alert": drift_alert
        }

        log_metrics_history(metrics)

        return metrics

    except Exception as e:
        logger.error(f"Metrics calculation failed: {e}")
        return {
            "total_predictions": 0,
            "average_drift_score": 0.0,
            "accuracy": 0.0,
            "model_version": "unregistered",
            "drift_alert": False
        }


# -------------------------------------------------
# Metrics History Logger
# -------------------------------------------------

def log_metrics_history(metrics: dict):

    try:
        os.makedirs(os.path.dirname(METRICS_HISTORY_PATH), exist_ok=True)

        metrics_with_timestamp = metrics.copy()
        metrics_with_timestamp["timestamp"] = datetime.utcnow().isoformat()

        df = pd.DataFrame([metrics_with_timestamp])

        if not os.path.exists(METRICS_HISTORY_PATH):
            df.to_csv(METRICS_HISTORY_PATH, index=False)
        else:
            df.to_csv(METRICS_HISTORY_PATH, mode="a", header=False, index=False)

        logger.info("Metrics history updated.")

    except Exception as e:
        logger.error(f"Failed to log metrics history: {e}")