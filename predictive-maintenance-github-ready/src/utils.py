import pandas as pd


def create_health_rule_based_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create simple engineered features for predictive maintenance.

    This starter function can be expanded with rolling windows,
    time-series features, and machine-specific domain logic.
    """
    df = df.copy()

    if "temperature" in df.columns and "vibration" in df.columns:
        df["temp_vibration_ratio"] = df["temperature"] / (df["vibration"] + 0.001)

    required = {"temperature", "vibration", "pressure", "error_count"}
    if required.issubset(df.columns):
        df["stress_index"] = (
            df["temperature"] * 0.3
            + df["vibration"] * 100 * 0.4
            + df["pressure"] * 0.2
            + df["error_count"] * 0.1
        )

    return df