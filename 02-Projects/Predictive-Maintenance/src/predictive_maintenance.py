import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "sample_machine_data.csv"
ASSET_DIR = ROOT / "assets"
ASSET_DIR.mkdir(exist_ok=True)


def main():
    df = pd.read_csv(DATA_PATH)

    X = pd.get_dummies(df.drop(columns=["failure_next_7d", "machine_id"]), drop_first=True)
    y = df["failure_next_7d"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        min_samples_leaf=6,
        class_weight="balanced_subsample",
        random_state=42,
    )
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)

    metrics = {
        "roc_auc": roc_auc_score(y_test, probs),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }

    print("\nPredictive Maintenance Model Results")
    print("-" * 40)
    for key, value in metrics.items():
        print(f"{key:>10}: {value:.3f}")

    with open(ROOT / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    feature_importance = (
        pd.Series(model.feature_importances_, index=X.columns)
        .sort_values(ascending=True)
        .tail(8)
    )
    plt.figure(figsize=(6, 4.4))
    feature_importance.plot(kind="barh")
    plt.xlabel("Random forest importance")
    plt.title("Top predictive signals")
    plt.tight_layout()
    plt.savefig(ASSET_DIR / "feature_importance.png", dpi=180)
    plt.close()

    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(4.4, 4))
    ax.imshow(cm)
    ax.set_xticks([0, 1], labels=["Pred 0", "Pred 1"])
    ax.set_yticks([0, 1], labels=["Actual 0", "Actual 1"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=14, fontweight="bold")
    ax.set_title("Confusion matrix")
    plt.tight_layout()
    plt.savefig(ASSET_DIR / "confusion_matrix.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    main()
