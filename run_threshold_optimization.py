from training.threshold_optimizer import optimize_threshold

DATA_PATH = "src/data/complaints.csv"

print("Running Threshold Optimization...")

optimize_threshold(DATA_PATH)