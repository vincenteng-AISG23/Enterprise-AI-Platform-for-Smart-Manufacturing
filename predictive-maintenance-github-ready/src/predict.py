from pathlib import Path
import joblib
import pandas as pd

from utils import create_health_rule_based_features


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "predictive_maintenance_model.pkl"


def load_model(model_path: Path = MODEL_PATH):
    return joblib.load(model_path)


def predict_machine_health(input_data: dict):
    model = load_model()
    df = pd.DataFrame([input_data])
    df = create_health_rule_based_features(df)

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "failure_probability": float(round(probability, 4))
    }


if __name__ == "__main__":
    sample_input = {
        "machine_id": 101,
        "temperature": 85,
        "vibration": 0.72,
        "pressure": 31,
        "runtime_hours": 1450,
        "maintenance_count": 3,
        "error_count": 8
    }

    result = predict_machine_health(sample_input)
    print(result)