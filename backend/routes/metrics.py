from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

LOG_PATH = "backend/data/prediction_logs.csv"

@router.get("/metrics")
def get_metrics():
    if not os.path.exists(LOG_PATH):
        return {"total_predictions": 0}

    df = pd.read_csv(LOG_PATH)

    return {
        "total_predictions": len(df),
        "average_drift": df["drift_score"].mean(),
        "model_versions": df["model_version"].unique().tolist()
    }