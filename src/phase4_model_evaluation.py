from sklearn.metrics import accuracy_score, classification_report


def run_phase4(model, X_test, y_test, le_borough, le_agency, le_target):

    print("Phase 4: Model Evaluation Started...")

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    return y_pred
