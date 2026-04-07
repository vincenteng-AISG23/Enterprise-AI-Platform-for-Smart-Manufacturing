from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE_DIR / "outputs" / "metrics.json"

def main() -> None:
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    print("Model evaluation summary")
    for key, value in metrics.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
