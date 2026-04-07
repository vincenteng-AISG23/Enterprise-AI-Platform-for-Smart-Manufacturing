from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def generate_dataset(n_rows: int = 3000) -> pd.DataFrame:
    machine_ids = [f"MCH-{i:03d}" for i in range(1, 31)]
    shifts = ["day", "night"]

    rows = []
    for _ in range(n_rows):
        machine_id = np.random.choice(machine_ids)
        shift = np.random.choice(shifts, p=[0.6, 0.4])

        machine_age_years = np.random.uniform(0.5, 12.0)
        maintenance_overdue_days = max(0, np.random.normal(18, 15))
        load_pct = np.clip(np.random.normal(72, 15), 20, 110)
        rpm = np.clip(np.random.normal(1450, 280), 700, 3200)
        temperature_c = np.clip(np.random.normal(68, 10), 35, 120)
        vibration_mm_s = np.clip(np.random.normal(4.2, 1.8), 0.2, 16.0)
        pressure_bar = np.clip(np.random.normal(7.0, 1.3), 2.0, 12.5)
        sound_db = np.clip(np.random.normal(78, 8), 45, 120)
        humidity_pct = np.clip(np.random.normal(58, 16), 15, 95)

        risk_score = (
            0.030 * temperature_c
            + 0.220 * vibration_mm_s
            + 0.018 * load_pct
            + 0.012 * sound_db
            + 0.028 * maintenance_overdue_days
            + 0.090 * machine_age_years
            + 0.004 * abs(pressure_bar - 7.0) * 10
            + (0.8 if shift == "night" else 0.0)
            + np.random.normal(0, 1.0)
        )

        failure_within_7_days = 1 if risk_score > 9.6 else 0

        rows.append(
            {
                "machine_id": machine_id,
                "shift": shift,
                "machine_age_years": round(machine_age_years, 2),
                "maintenance_overdue_days": round(maintenance_overdue_days, 1),
                "load_pct": round(load_pct, 1),
                "rpm": round(rpm, 0),
                "temperature_c": round(temperature_c, 1),
                "vibration_mm_s": round(vibration_mm_s, 2),
                "pressure_bar": round(pressure_bar, 2),
                "sound_db": round(sound_db, 1),
                "humidity_pct": round(humidity_pct, 1),
                "failure_within_7_days": failure_within_7_days,
            }
        )

    return pd.DataFrame(rows)

def main() -> None:
    output_path = Path(__file__).resolve().parents[1] / "data" / "sample_sensor_data.csv"
    df = generate_dataset()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated dataset: {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()
