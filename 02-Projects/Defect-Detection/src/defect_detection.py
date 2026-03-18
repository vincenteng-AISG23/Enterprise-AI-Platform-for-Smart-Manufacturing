import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
df = pd.read_csv("sample_defect_data.csv")

# Features and target
X = df.drop(columns=["part_id", "defect"])
y = df["defect"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, predictions)
cm = confusion_matrix(y_test, predictions)

print(f"Accuracy: {accuracy:.2f}")
print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Feature importance
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

print("\nTop Feature Importances:")
print(feature_importance)

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# Plot feature importance
plt.figure(figsize=(8, 5))
feature_importance.plot(kind="bar")
plt.title("Feature Importance for Defect Detection")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.savefig("assets/feature_importance_defect_detection.png")
plt.show()