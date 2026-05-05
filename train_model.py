import pandas as pd
import os
import json
import joblib
from datetime import datetime
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, average_precision_score

# =====================================================
# CONFIG
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "complaints.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REGISTRY_PATH = os.path.join(MODELS_DIR, "model_registry.json")
METRICS_HISTORY_PATH = os.path.join(MODELS_DIR, "metrics_history.csv")

os.makedirs(MODELS_DIR, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

print(f"✅ Loading dataset from: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, nrows=50000)

print("📊 Dataset shape:", df.shape)

# =====================================================
# FEATURE ENGINEERING (AUTO IF NOT PRESENT)
# =====================================================

# Create timestamp if not present
if "timestamp" not in df.columns:
    if "Created Date" not in df.columns:
        raise ValueError("Dataset must contain either 'timestamp' or 'Created Date'")
    df["timestamp"] = pd.to_datetime(df["Created Date"], errors="coerce")

df = df.dropna(subset=["timestamp"])

# Time features
df["Year"] = df["timestamp"].dt.year
df["Month"] = df["timestamp"].dt.month
df["Day"] = df["timestamp"].dt.day
df["Hour"] = df["timestamp"].dt.hour
df["Is_Weekend"] = (df["timestamp"].dt.weekday >= 5).astype(int)

df["Part_of_Day"] = df["Hour"].apply(
    lambda x: 0 if x < 6 else 1 if x < 12 else 2 if x < 18 else 3
)

# Encode Borough
if "borough_encoded" not in df.columns:
    if "Borough" not in df.columns:
        raise ValueError("Dataset must contain 'Borough'")
    df["borough_encoded"] = df["Borough"].astype("category").cat.codes

# Encode Agency
if "agency_encoded" not in df.columns:
    if "Agency" not in df.columns:
        raise ValueError("Dataset must contain 'Agency'")
    df["agency_encoded"] = df["Agency"].astype("category").cat.codes

# Create target if not present
if "target" not in df.columns:
    if "Complaint Status" not in df.columns:
        raise ValueError("Dataset must contain 'target' or 'Complaint Status'")
    df["target"] = (df["Complaint Status"].str.lower() == "closed").astype(int)

# =====================================================
# MODEL FEATURES
# =====================================================

required_features = [
    "borough_encoded",
    "agency_encoded",
    "Year",
    "Month",
    "Day",
    "Hour",
    "Is_Weekend",
    "Part_of_Day"
]

missing = [col for col in required_features + ["target"] if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns after engineering: {missing}")

df = df.sort_values("timestamp")

X = df[required_features].copy()
X.columns = required_features  # Force correct column names
y = df["target"]

# =====================================================
# TEMPORAL SPLIT (80/20)
# =====================================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
y_train = y.iloc[:split_index]
X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]

print("🚀 Training model...")

# =====================================================
# TRAIN
# =====================================================

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    eval_metric="logloss",
    use_label_encoder=False
)

model.fit(X_train, y_train)

# =====================================================
# EVALUATE
# =====================================================

preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

precision = precision_score(y_test, preds)
recall = recall_score(y_test, preds)
pr_auc = average_precision_score(y_test, probs)

# =====================================================
# MODEL VERSIONING
# =====================================================

timestamp_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
model_version = f"xgboost_model_v{timestamp_str}"
model_filename = f"{model_version}.pkl"
model_path = os.path.join(MODELS_DIR, model_filename)

joblib.dump(model, model_path)

registry_data = {
    "latest_model": model_filename,
    "model_version": model_version,
    "trained_at": timestamp_str,
    "dataset_size": len(df)
}

with open(REGISTRY_PATH, "w") as f:
    json.dump(registry_data, f, indent=4)

# =====================================================
# METRICS HISTORY
# =====================================================

metrics_entry = {
    "timestamp": timestamp_str,
    "model_version": model_version,
    "precision": float(precision),
    "recall": float(recall),
    "pr_auc": float(pr_auc),
    "dataset_size": len(df)
}

metrics_df = pd.DataFrame([metrics_entry])

if os.path.exists(METRICS_HISTORY_PATH):
    metrics_df.to_csv(METRICS_HISTORY_PATH, mode="a", header=False, index=False)
else:
    metrics_df.to_csv(METRICS_HISTORY_PATH, index=False)

# =====================================================
# DONE
# =====================================================

print("\n✅ Model trained successfully:", model_filename)
print("📊 Precision:", round(precision, 4))
print("📊 Recall:", round(recall, 4))
print("📊 PR-AUC:", round(pr_auc, 4))