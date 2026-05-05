import pandas as pd


def run_phase2(df):

    print("Starting feature engineering...")

    # Ensure datetime format
    df["Created Date"] = pd.to_datetime(df["Created Date"], errors="coerce")

    # Drop rows where datetime failed
    df = df.dropna(subset=["Created Date"]).copy()

    # Basic time features
    df["Year"] = df["Created Date"].dt.year
    df["Month"] = df["Created Date"].dt.month
    df["Day"] = df["Created Date"].dt.day
    df["Hour"] = df["Created Date"].dt.hour

    # Weekend feature
    df["Is_Weekend"] = df["Created Date"].dt.dayofweek.apply(
        lambda x: 1 if x >= 5 else 0
    )

    # Part of day feature
    def get_part_of_day(hour):
        if 5 <= hour < 12:
            return 0  # Morning
        elif 12 <= hour < 17:
            return 1  # Afternoon
        elif 17 <= hour < 21:
            return 2  # Evening
        else:
            return 3  # Night

    df["Part_of_Day"] = df["Hour"].apply(get_part_of_day)

    print("After feature engineering:", df.shape)

    return df
