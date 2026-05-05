import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
import os

def run_calibration(data_path):

    print("Running calibration analysis...")

    # Load only a subset of rows to prevent RAM crash
    df = pd.read_csv(
        data_path,
        nrows=5000,          # <-- important fix
        low_memory=False
    )

    print("Loaded data shape:", df.shape)

    # Create a dummy binary target if not present
    if "target" not in df.columns:
        np.random.seed(42)
        df["target"] = np.random.randint(0, 2, len(df))

    y_true = df["target"]
    y_prob = np.random.uniform(0, 1, len(df))  # simulated probabilities

    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)

    os.makedirs("reports", exist_ok=True)

    plt.figure(figsize=(6,6))
    plt.plot(prob_pred, prob_true, marker='o')
    plt.plot([0,1],[0,1],'--')
    plt.title("Calibration Curve")
    plt.xlabel("Predicted Probability")
    plt.ylabel("True Probability")

    output_path = "reports/calibration_curve.png"
    plt.savefig(output_path)

    print("Calibration plot saved to:", output_path)