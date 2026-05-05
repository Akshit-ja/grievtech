import numpy as np

# Baseline average complaint length (example reference)
BASELINE_MEAN_LENGTH = 120
BASELINE_STD_LENGTH = 30


def calculate_drift(text: str) -> float:
    """
    Simple drift calculation based on text length deviation.
    Replace with advanced embedding drift in production.
    """

    text_length = len(text)

    z_score = abs(text_length - BASELINE_MEAN_LENGTH) / BASELINE_STD_LENGTH

    # Normalize to 0-1 scale
    drift_score = min(z_score / 3, 1.0)

    return round(float(drift_score), 4)