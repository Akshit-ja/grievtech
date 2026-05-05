import pandas as pd
import json
import os
from datetime import datetime
from training.threshold_optimizer import optimize_threshold

DRIFT_THRESHOLD = 0.20  # 20% change triggers retraining


def detect_drift(data_path):

    df = pd.read_csv(data_path)

    if "year" not in df.columns:
        raise ValueError("Column 'year' not found in dataset.")

    if "delayed" not in df.columns:
        raise ValueError("Target column 'delayed' not found in dataset.")

    baseline = df[df["year"] <= 2023]
    live = df[df["year"] == 2024]

    if baseline.empty or live.empty:
        raise ValueError("Baseline or live dataset is empty. Check year split.")

    numeric_cols = baseline.select_dtypes(include="number").columns

    drift_results = {}
    retrain_required = False

    for col in numeric_cols:

        if col in ["year", "delayed"]:
            continue

        base_mean = baseline[col].mean()
        live_mean = live[col].mean()

        if base_mean == 0:
            continue

        percent_change = abs(live_mean - base_mean) / abs(base_mean)

        drift_results[col] = {
            "baseline_mean": float(base_mean),
            "live_mean": float(live_mean),
            "percent_change": float(percent_change)
        }

        if percent_change > DRIFT_THRESHOLD:
            retrain_required = True

    os.makedirs("reports", exist_ok=True)

    # Save drift report
    with open("reports/drift_report.json", "w") as f:
        json.dump(drift_results, f, indent=4)

    history_file = "reports/retraining_history.json"

    # 🔥 AUTOMATED RETRAINING TRIGGER
    if retrain_required:

        print("⚠ Drift detected. Triggering automatic retraining...")

        # optimize_threshold MUST return new model version
        new_version = optimize_threshold(data_path)

        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                history = json.load(f)
        else:
            history = []

        history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "Drift Threshold Exceeded",
            "new_model_version": new_version
        })

        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)

        retrain_status = "Retraining Triggered"

    else:
        retrain_status = "No Retraining Needed"

    with open("reports/retraining_status.json", "w") as f:
        json.dump({"status": retrain_status}, f, indent=4)

    print("Drift analysis complete.")

    return drift_results