from training.calibration import run_calibration

DATA_PATH = "src/data/complaints.csv"

if __name__ == "__main__":
    run_calibration(DATA_PATH)