import pandas as pd
import numpy as np
import json
import os
from sklearn.metrics import precision_recall_curve
from xgboost import XGBClassifier


def optimize_threshold(data_path):

    df = pd.read_csv(data_path)

    target = "delayed"

    if target not in df.columns:
        raise ValueError("Column 'delayed' not found in dataset")

    if "year" not in df.columns:
        raise ValueError("Column 'year' not found in dataset")

    train = df[df["year"] <= 2023]
    test = df[df["year"] == 2024]

    X_train = train.drop(columns=[target])
    y_train = train[target]

    X_test = test.drop(columns=[target])
    y_test = test[target]

    if "year" in X_train.columns:
        X_train = X_train.drop(columns=["year"])

    if "year" in X_test.columns:
        X_test = X_test.drop(columns=["year"])

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=2,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]

    precisions, recalls, thresholds = precision_recall_curve(y_test, probs)

    best_threshold = 0.5
    best_recall = 0

    for p, r, t in zip(precisions, recalls, list(thresholds) + [1]):
        if p >= 0.60 and r > best_recall:
            best_recall = r
            best_threshold = t

    os.makedirs("reports", exist_ok=True)

    with open("reports/optimized_threshold.json", "w") as f:
        json.dump({
            "best_threshold": float(best_threshold),
            "recall": float(best_recall)
        }, f, indent=4)

    pd.DataFrame({
        "precision": precisions,
        "recall": recalls
    }).to_csv("reports/pr_curve_data.csv", index=False)

    print("Optimal Threshold:", best_threshold)
    print("Recall at Threshold:", best_recall)

    return best_threshold