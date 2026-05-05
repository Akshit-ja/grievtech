from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

router = APIRouter()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["grievtech_db"]
feedback_collection = db["feedback"]


class FeedbackRequest(BaseModel):
    complaint_text: str
    predicted_label: int
    user_feedback: int  # 1 = correct, 0 = incorrect


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):

    feedback_entry = {
        "complaint_text": request.complaint_text,
        "predicted_label": request.predicted_label,
        "user_feedback": request.user_feedback,
        "timestamp": datetime.datetime.utcnow()
    }

    feedback_collection.insert_one(feedback_entry)

    return {"message": "Feedback recorded successfully"}