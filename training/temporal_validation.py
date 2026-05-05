import os
import json
import pandas as pd

from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    precision_recall_curve,
    auc
)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def run_temporal_validation(path):

    print("Loading dataset...")
    df = pd.read_csv(path, nrows=100000, low_memory=False)

    text_col = "Descriptor"
    date_col = "Created Date"
    label_col = "Complaint Type"

    df = df[[text_col, date_col, label_col]].dropna()

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    df["year"] = df[date_col].dt.year

    print("Available years:", sorted(df["year"].unique()))

    df = df.sort_values(date_col)

    split_index = int(len(df) * 0.8)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    print("Train size:", len(train_df))
    print("Test size:", len(test_df))

    # ---------------------
    # Vectorization
    # ---------------------

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X_train = vectorizer.fit_transform(train_df[text_col])
    X_test = vectorizer.transform(test_df[text_col])

    y_train = train_df[label_col]
    y_test = test_df[label_col]

    # ---------------------
    # Model Training
    # ---------------------

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("\nTemporal Validation Report\n")
    print(classification_report(y_test, preds))

    # ---------------------
    # Metrics
    # ---------------------

    accuracy = accuracy_score(y_test, preds)

    precision = precision_score(
        y_test,
        preds,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        preds,
        average="weighted",
        zero_division=0
    )

    # ---------------------
    # PR Curve
    # ---------------------

    probs = model.predict_proba(X_test)

    precision_curve, recall_curve, thresholds = precision_recall_curve(
        (y_test == y_test.iloc[0]).astype(int),
        probs[:, 0]
    )

    pr_auc = auc(recall_curve, precision_curve)

    pr_df = pd.DataFrame({
        "precision": precision_curve[:-1],
        "recall": recall_curve[:-1],
        "threshold": thresholds
    })

    os.makedirs("reports", exist_ok=True)

    pr_df.to_csv("reports/pr_curve_data.csv", index=False)

    # ---------------------
    # Benchmark Report
    # ---------------------

    benchmark_report = {

        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "pr_auc": float(pr_auc),

        "threshold_used": 0.5,

        "train_size": int(len(train_df)),
        "test_size": int(len(test_df)),

        "future_window": "Latest 20% of dataset (temporal validation)"
    }

    with open("reports/benchmark_report.json", "w") as f:
        json.dump(benchmark_report, f, indent=4)

    # ---------------------
    # Assertions
    # ---------------------

    assert recall >= 0.50, "Recall below acceptable level"
    assert precision >= 0.50, "Precision below acceptable level"

    print("\nBenchmark report saved to reports/benchmark_report.json")
    print("PR curve data saved to reports/pr_curve_data.csv")

    print("\nTemporal Validation Completed Successfully")


if __name__ == "__main__":
    run_temporal_validation("src/data/complaints.csv")