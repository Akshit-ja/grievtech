from backend.routes import feedback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import time
import uuid

from backend.core.logging_config import setup_logging
from backend.schemas import PredictionRequest, PredictionResponse, MetricsResponse
from backend.services.model_service import predict
from backend.services.metrics_service import get_metrics

logger = setup_logging()

app = FastAPI(
    title="GrievTech AI Backend",
    description="Enterprise Grievance Risk Monitoring System",
    version="2.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "GrievTech Backend Running Successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ---------------------------------
# 🔥 CORE PREDICTION LOGIC WRAPPER
# ---------------------------------

def format_prediction(result):
    risk_score = result.get("risk_score", 0)

    if risk_score >= 0.7:
        risk_level = "High"
        escalation = True
    elif risk_score >= 0.4:
        risk_level = "Medium"
        escalation = False
    else:
        risk_level = "Low"
        escalation = False

    return {
        "complaint_id": str(uuid.uuid4())[:8],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "escalation_required": escalation
    }


# ---------------------------------
# ✅ FAST PREDICT (NO DELAY UI)
# ---------------------------------

@app.post("/predict")
@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict_route(request: PredictionRequest):
    start_time = time.time()

    try:
        raw_result = predict(
            borough_encoded=request.borough_encoded,
            agency_encoded=request.agency_encoded,
            year=request.year,
            month=request.month,
            text=request.text
        )

        result = format_prediction(raw_result)

        duration = round(time.time() - start_time, 2)
        logger.info(f"Prediction completed in {duration}s")

        return result

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")


# ---------------------------------
# ✅ BATCH (OPTIMIZED)
# ---------------------------------

@app.post("/api/v1/batch")
async def batch_predict(file: UploadFile = File(...)):
    try:
        start_time = time.time()

        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        required_columns = ["borough_encoded", "agency_encoded", "year", "month"]

        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing {col}")

        results = []

        for _, row in df.iterrows():
            raw = predict(
                borough_encoded=int(row["borough_encoded"]),
                agency_encoded=int(row["agency_encoded"]),
                year=int(row["year"]),
                month=int(row["month"]),
                text=row.get("text", "")
            )

            results.append(format_prediction(raw))

        duration = round(time.time() - start_time, 2)

        return {
            "total_rows": len(results),
            "processing_time_seconds": duration,
            "results": results
        }

    except Exception as e:
        logger.error(f"Batch failed: {e}")
        raise HTTPException(status_code=500, detail="Batch prediction failed")


# ---------------------------------
# METRICS
# ---------------------------------

@app.get("/api/v1/metrics", response_model=MetricsResponse)
def metrics_route():
    try:
        return get_metrics()
    except Exception as e:
        logger.error(f"Metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")