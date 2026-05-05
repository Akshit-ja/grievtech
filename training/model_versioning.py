import os
import json
import joblib
from datetime import datetime

MODEL_DIR = "models"
VERSION_LOG = os.path.join(MODEL_DIR, "version_log.json")


def save_new_version(model):

    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(VERSION_LOG):
        with open(VERSION_LOG, "r") as f:
            version_data = json.load(f)
    else:
        version_data = {"current_version": 0, "history": []}

    new_version = version_data["current_version"] + 1
    model_name = f"model_v{new_version}.pkl"
    model_path = os.path.join(MODEL_DIR, model_name)

    joblib.dump(model, model_path)

    entry = {
        "version": new_version,
        "model_file": model_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    version_data["current_version"] = new_version
    version_data["history"].append(entry)

    with open(VERSION_LOG, "w") as f:
        json.dump(version_data, f, indent=4)

    return new_version