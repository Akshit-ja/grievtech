import os
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI(title="GrievTech API", version="1.0")

# -----------------------------
# Load Model + Label Encoder
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# -----------------------------
# Request Schema
# -----------------------------
class ComplaintRequest(BaseModel):
    complaint_text: str


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "GrievTech API is running successfully 🚀"}


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.post("/predict")
def predict_complaint(request: ComplaintRequest):

    # Convert text → vector
    text_vector = vectorizer.transform([request.complaint_text])

    # Predict class
    prediction = model.predict(text_vector)[0]

    # Predict probabilities
    probabilities = model.predict_proba(text_vector)[0]
    confidence = float(np.max(probabilities))

    # Decode label
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    return {
        "predicted_category": predicted_label,
        "confidence_score": round(confidence, 4)
    }


# -----------------------------
# Run Server Directly
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
