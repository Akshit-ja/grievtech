import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


def run_phase3(df):

    print("Phase 3: Model Training Started...")

    # --------------------------------
    # Remove rare complaint types
    # --------------------------------
    counts = df["Complaint Type"].value_counts()
    valid_complaints = counts[counts >= 50].index

    df = df[df["Complaint Type"].isin(valid_complaints)].copy()

    print("After removing rare complaint types:", df.shape)
        # --------------------------------
    # Group complaint types into broader categories
    # --------------------------------
    def group_complaint(x):
        x = x.lower()

        if "noise" in x:
            return "Noise"
        elif "parking" in x or "driveway" in x:
            return "Parking"
        elif "water" in x:
            return "Water"
        elif "heat" in x:
            return "Heating"
        elif "street" in x:
            return "Street"
        elif "building" in x:
            return "Building"
        else:
            return "Other"

    df["Complaint_Group"] = df["Complaint Type"].apply(group_complaint)


    # --------------------------------
    # Encode categorical features
    # --------------------------------
    le_borough = LabelEncoder()
    le_agency = LabelEncoder()
    le_target = LabelEncoder()

    df["borough_encoded"] = le_borough.fit_transform(df["Borough"])
    df["agency_encoded"] = le_agency.fit_transform(df["Agency"])
    df["target_encoded"] = le_target.fit_transform(df["Complaint_Group"])


    # --------------------------------
    # Feature Selection
    # --------------------------------
    X = df[[
        "borough_encoded",
        "agency_encoded",
        "Year",
        "Month",
        "Day",
        "Hour",
        "Is_Weekend",
        "Part_of_Day"
    ]]

    y = df["target_encoded"]

    # --------------------------------
    # Train-Test Split (NO STRATIFY)
    # --------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # --------------------------------
    # XGBoost Multi-class Model
    # --------------------------------
    num_classes = len(y.unique())

    model = XGBClassifier(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softmax",
        num_class=num_classes,
        random_state=42,
        n_jobs=-1,
        eval_metric="mlogloss",
        use_label_encoder=False
    )

    model.fit(X_train, y_train)

    print("Model training completed.")

    # --------------------------------
    # Save Model & Encoders
    # --------------------------------
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/xgboost_model.pkl")
    joblib.dump(le_borough, "models/le_borough.pkl")
    joblib.dump(le_agency, "models/le_agency.pkl")
    joblib.dump(le_target, "models/le_target.pkl")

    print("Model and encoders saved successfully.")

    return model, X_test, y_test, le_borough, le_agency, le_target
