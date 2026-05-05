from training.drift_monitor import detect_drift

DATA_PATH = "data/processed/processed_data.csv"

if __name__ == "__main__":
    print("Running Drift Monitoring...")
    detect_drift(DATA_PATH)