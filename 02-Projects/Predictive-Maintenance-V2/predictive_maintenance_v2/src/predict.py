from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "model.joblib"

def sample_input() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "machine_id": "MCH-007",
                "shift": "night",
                "machine_age_years": 8.4,
                "maintenance_overdue_days": 29.0,
                "load_pct": 88.0,
                "rpm": 1720.0,
                "temperature_c": 84.0,
                "vibration_mm_s": 7.2,
                "pressure_bar": 8.9,
                "sound_db": 91.0,
                "humidity_pct": 67.0,
            }
        ]
    )

def main() -> None:
    model = joblib.load(MODEL_PATH)
    X_new = sample_input()

    risk_probability = model.predict_proba(X_new)[:, 1][0]
    prediction = model.predict(X_new)[0]

    print("Sample input:")
    print(X_new.to_string(index=False))
    print()
    print(f"Predicted failure risk within 7 days: {risk_probability:.2%}")
    print(f"Predicted class (1=High risk, 0=Lower risk): {prediction}")

if __name__ == "__main__":
    main()
