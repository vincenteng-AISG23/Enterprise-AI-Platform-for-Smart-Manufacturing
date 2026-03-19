import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(BASE_DIR, "sample_predictive_maintenance_data.csv")

df = pd.read_csv(csv_path)

# Load dataset
df = pd.read_csv("sample_predictive_maintenance_data.csv")

df["temperature_diff"] = df["process_temperature"] - df["air_temperature"]
X = df[[
    "air_temperature",
    "process_temperature",
    "temperature_diff",
    "rotational_speed",
    "torque",
    "tool_wear"
]]

# Features and target
X = df.drop(columns=["machine_failure"], errors="ignore")
X = X.select_dtypes(include=["number"])
y = df["machine_failure"]

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
plt.title("Feature Importance for Predictive Maintenance")
plt.ylabel("Importance Score")
plt.tight_layout()
plt.savefig("assets/feature_importance_predictive_maintenance.png")
plt.show()

# Predict probability
prediction_proba = model.predict_proba(X_test)

# Take one example (first row)
sample_proba = prediction_proba[0][1]  # probability of failure

for i, proba in enumerate(prediction_proba):
    failure_prob = proba[1]

    if failure_prob > 0.7:
        risk = "HIGH"
        action = "STOP MACHINE"
    elif failure_prob > 0.4:
        risk = "MEDIUM"
        action = "INSPECT"
    else:
        risk = "LOW"
        action = "CONTINUE"

    print(f"\nMachine {i}")
    print(f"Failure Probability: {failure_prob:.2f}")
    print(f"Risk: {risk}")
    print(f"Action: {action}")

print(f"\nSample Failure Probability: {sample_proba:.2f}")

# Business logic layer
if sample_proba > 0.7:
    risk_level = "HIGH"
    action = "🚨 Stop machine immediately and perform maintenance"
elif sample_proba > 0.4:
    risk_level = "MEDIUM"
    action = "⚠️ Increase inspection frequency and monitor closely"
else:
    risk_level = "LOW"
    action = "✅ Continue normal operation"

print(f"\nRisk Level: {risk_level}")
print(f"Recommended Action: {action}")

# Cost impact simulation
if risk_level == "HIGH":
    estimated_loss = 30000
elif risk_level == "MEDIUM":
    estimated_loss = 10000
else:
    estimated_loss = 2000

print(f"Estimated Downtime Cost: ${estimated_loss}")

high_risk_count = sum(1 for p in prediction_proba if p[1] > 0.7)

print(f"\n🚨 Machines needing immediate attention: {high_risk_count}")