import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score
import joblib


def compute_feature_distribution(X):
    stats = {}

    for col in X.columns:
        stats[col] = {
            "mean": float(X[col].mean()),
            "std": float(X[col].std())
        }

    return stats


def compute_distribution_shift(baseline, live):

    shifts = []

    for feature in baseline:

        if feature in live:

            base_mean = baseline[feature]["mean"]
            live_mean = live[feature]["mean"]

            shift = abs(base_mean - live_mean)

            shifts.append(shift)

    if len(shifts) == 0:
        return 0.0

    return float(np.mean(shifts))


def run_drift_monitor():

    print("🚀 Starting Drift Monitoring...")

    os.makedirs("reports", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # -----------------------------
    # Load baseline benchmark
    # -----------------------------

    benchmark_path = "reports/benchmark_report.json"

    if os.path.exists(benchmark_path):

        with open(benchmark_path) as f:
            baseline_metrics = json.load(f)

        baseline_recall = baseline_metrics.get("recall", 0.7)

    else:
        print("Benchmark report missing — using default baseline")
        baseline_recall = 0.7

    print("Baseline Recall:", baseline_recall)

    # -----------------------------
    # Load trained model
    # -----------------------------

    model_path = "models/model_v1.pkl"

    if not os.path.exists(model_path):
        print("Model not found. Train model first.")
        return

    model = joblib.load(model_path)

    # -----------------------------
    # Load dataset
    # -----------------------------

    data_path = "src/data/complaints.csv"

    df = pd.read_csv(data_path, nrows=5000, low_memory=False)

    # Use only numeric features
    X = df.select_dtypes(include=["number"]).fillna(0)

    # Handle target safely
    if "Complaint Type" in df.columns:
        y = df["Complaint Type"].astype("category").cat.codes
    else:
        y = np.zeros(len(X))

    # -----------------------------
    # Align features with model
    # -----------------------------

    if hasattr(model, "feature_names_in_"):

        expected_features = model.feature_names_in_

        for col in expected_features:
            if col not in X.columns:
                X[col] = 0

        X = X[expected_features]

    # -----------------------------
    # Predict
    # -----------------------------

    preds = model.predict(X)

    # -----------------------------
    # Compute recall
    # -----------------------------

    try:
        live_recall = recall_score(y, preds, average="macro", zero_division=0)
    except:
        live_recall = 0.0

    print("Live Recall:", live_recall)

    # -----------------------------
    # Feature drift detection
    # -----------------------------

    baseline_file = "models/training_distribution.json"

    live_distribution = compute_feature_distribution(X)

    if os.path.exists(baseline_file):

        with open(baseline_file) as f:
            baseline_distribution = json.load(f)

    else:

        baseline_distribution = live_distribution

        with open(baseline_file, "w") as f:
            json.dump(baseline_distribution, f, indent=4)

        print("Baseline distribution saved")

    drift_score = compute_distribution_shift(
        baseline_distribution,
        live_distribution
    )

    # -----------------------------
    # Performance drift
    # -----------------------------

    recall_drop = max(0, baseline_recall - live_recall)

    # -----------------------------
    # Drift severity scoring
    # -----------------------------

    if recall_drop < 0.05:
        severity = "LOW"
    elif recall_drop < 0.15:
        severity = "MEDIUM"
    elif recall_drop < 0.30:
        severity = "HIGH"
    else:
        severity = "CRITICAL"

    print("Drift Severity:", severity)

    # -----------------------------
    # Drift alert trigger
    # -----------------------------

    drift_alert = bool(recall_drop > 0.10 or drift_score > 0.15)

    # -----------------------------
    # Performance visualization
    # -----------------------------

    plt.figure()

    labels = ["Baseline Recall", "Live Recall"]
    values = [baseline_recall, live_recall]

    plt.bar(labels, values)

    plt.ylabel("Recall")
    plt.title("Performance Drift Comparison")

    plt.savefig("reports/performance_drift.png")

    plt.close()

    # -----------------------------
    # Save drift report
    # -----------------------------

    report = {
        "baseline_recall": float(baseline_recall),
        "live_recall": float(live_recall),
        "recall_drop": float(recall_drop),
        "drift_score": float(drift_score),
        "drift_severity": severity,
        "drift_alert": drift_alert,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("reports/drift_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("✅ Drift report saved")
    print("📊 Performance plot saved")

    if drift_alert:
        print("⚠ DRIFT ALERT: Retraining recommended")
    else:
        print("System stable")


if __name__ == "__main__":
    run_drift_monitor()