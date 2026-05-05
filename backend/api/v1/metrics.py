from fastapi import APIRouter
from backend.metrics_store import get_metrics
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/metrics")
def metrics():
    logger.info("Metrics endpoint accessed.")
    return get_metrics()