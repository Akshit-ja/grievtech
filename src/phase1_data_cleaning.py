import pandas as pd
import os

def run_phase1(limit=80000):
    
    # Path to dataset
    data_path = os.path.join("src", "data", "complaints.csv")

    print("Loading dataset from:", data_path)

    df = pd.read_csv(data_path)

    # Limit rows for faster pipeline
    df = df.head(limit)

    print("Original shape:", df.shape)

    # Keep important columns
    columns_to_keep = [
        "Created Date",
        "Complaint Type",
        "Borough",
        "Agency"
    ]

    # Ensure columns exist before selecting
    df = df[[col for col in columns_to_keep if col in df.columns]]

    # Drop missing important values
    df = df.dropna(subset=["Complaint Type", "Borough"])

    print("After cleaning:", df.shape)

    return df