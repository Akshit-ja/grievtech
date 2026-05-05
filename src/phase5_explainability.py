import shap
import matplotlib.pyplot as plt
import numpy as np
import os
import json


def run_phase5(model, X_sample):

    print("Phase 5: Explainability Started...")

    # Keep sample small for stability
    X_sample = X_sample.iloc[:50]

    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # -----------------------------
    # SHAP Explainer
    # -----------------------------

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    shap_values = np.array(shap_values)

    """
    Possible shapes:
    OLD SHAP multiclass: (n_classes, n_samples, n_features)
    NEW SHAP multiclass: (n_samples, n_features, n_classes)
    Binary: (n_samples, n_features)
    """

    if shap_values.ndim == 3:

        if shap_values.shape[0] < 20:
            shap_values = shap_values[0]

        else:
            shap_values = shap_values[:, :, 0]

    # shap_values now guaranteed (samples, features)

    # -----------------------------
    # GLOBAL SHAP SUMMARY PLOT
    # -----------------------------

    plt.figure()

    shap.summary_plot(shap_values, X_sample, show=False)

    plt.tight_layout()

    plt.savefig("models/shap_summary.png")

    plt.close()

    print("SHAP summary plot saved to models/shap_summary.png")

    # -----------------------------
    # GLOBAL FEATURE IMPORTANCE
    # -----------------------------

    feature_names = X_sample.columns

    mean_importance = np.abs(shap_values).mean(axis=0)

    global_importance = sorted(
        zip(feature_names, mean_importance),
        key=lambda x: x[1],
        reverse=True
    )[:20]

    global_json = [
        {
            "feature": str(f),
            "importance": float(v)
        }
        for f, v in global_importance
    ]

    with open("reports/global_shap_importance.json", "w") as f:
        json.dump(global_json, f, indent=4)

    print("Global SHAP importance saved to reports/global_shap_importance.json")

    # -----------------------------
    # PER-PREDICTION EXPLANATIONS
    # -----------------------------

    explanations = []

    probabilities = None

    try:
        probabilities = model.predict_proba(X_sample)
    except:
        probabilities = None

    predictions = model.predict(X_sample)

    for i in range(len(X_sample)):

        feature_impacts = []

        for j, val in enumerate(shap_values[i]):

            feature_impacts.append(
                (feature_names[j], val)
            )

        feature_impacts = sorted(
            feature_impacts,
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_features = feature_impacts[:3]

        explanation = {

            "prediction": str(predictions[i]),

            "probability": float(
                np.max(probabilities[i])
            ) if probabilities is not None else None,

            "top_features": [
                {
                    "feature": str(f),
                    "impact": float(v)
                }
                for f, v in top_features
            ]
        }

        explanations.append(explanation)

    with open("reports/prediction_explanations.json", "w") as f:
        json.dump(explanations, f, indent=4)

    print("Prediction explanations saved to reports/prediction_explanations.json")

    print("Phase 5 Explainability Completed Successfully")