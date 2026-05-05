from pydantic import BaseModel
from typing import List, Optional

# -----------------------------------------
# Prediction Request
# -----------------------------------------

class PredictionRequest(BaseModel):
    borough_encoded: int
    agency_encoded: int
    year: int
    month: int
    text: Optional[str] = None


# -----------------------------------------
# Prediction Response
# -----------------------------------------

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    threshold_used: float
    alert: Optional[str]
    explanation: List[str]
    drift_score: float
    model_version: str


# -----------------------------------------
# Metrics Response  (THIS WAS MISSING)
# -----------------------------------------

class MetricsResponse(BaseModel):
    total_predictions: int
    high_priority_alerts: int
    average_probability: float
    model_version: str