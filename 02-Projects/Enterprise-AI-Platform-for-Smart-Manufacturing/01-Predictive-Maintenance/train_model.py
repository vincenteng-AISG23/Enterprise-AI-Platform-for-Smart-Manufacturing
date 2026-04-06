import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
df = pd.read_csv("sample_predictive_maintenance_data.csv")

# Features & target
X = df[["temperature", "pressure", "vibration", "humidity"]]
y = df["failure"]

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained successfully")