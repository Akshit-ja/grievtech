import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")
LOG_PATH = os.path.join(BASE_DIR, "..", "data", "prediction_logs.csv")

MODEL_VERSION = "1.0.0"