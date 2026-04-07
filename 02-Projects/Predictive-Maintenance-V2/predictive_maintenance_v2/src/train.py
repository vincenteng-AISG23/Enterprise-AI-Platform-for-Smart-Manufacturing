from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "sample_sensor_data.csv"
MODEL_PATH = BASE_DIR / "models" / "model.joblib"
METRICS_PATH = BASE_DIR / "outputs" / "metrics.json"
IMPORTANCE_CSV_PATH = BASE_DIR / "outputs" / "feature_importance.csv"
IMPORTANCE_PNG_PATH = BASE_DIR / "outputs" / "feature_importance.png"

TARGET = "failure_within_7_days"

def main() -> None:
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    categorical_features = ["machine_id", "shift"]
    numeric_features = [c for c in X.columns if c not in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=10,
        min_samples_split=8,
        min_samples_leaf=4,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    importances = pipeline.named_steps["model"].feature_importances_
    fi = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    fi.to_csv(IMPORTANCE_CSV_PATH, index=False)

    top_fi = fi.head(12).sort_values("importance")
    plt.figure(figsize=(10, 6))
    plt.barh(top_fi["feature"], top_fi["importance"])
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Top 12 Feature Importances")
    plt.tight_layout()
    plt.savefig(IMPORTANCE_PNG_PATH, dpi=150)
    plt.close()

    print("Training complete.")
    print(json.dumps(metrics, indent=2))
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")
    print(f"Saved feature importance to: {IMPORTANCE_CSV_PATH}")

if __name__ == "__main__":
    main()
