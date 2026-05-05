from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io
from backend.services.model_service import predict

router = APIRouter()

@router.post("/batch")
async def batch_predict(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    results = []

    for _, row in df.iterrows():
        result = predict(row["text"])
        results.append(result)

    return {
        "total_rows": len(results),
        "results": results
    }