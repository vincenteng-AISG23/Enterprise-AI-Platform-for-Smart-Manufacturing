import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv("sample_demand_data.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day

# Encode categorical columns
df_model = pd.get_dummies(df, columns=["product_id", "store_id"], drop_first=True)

# Features and target
X = df_model.drop(columns=["date", "demand"])
y = df_model["demand"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Feature importance
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

print("\nTop Feature Importances:")
print(feature_importance.head(10))

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

# Plot actual vs predicted
plt.figure(figsize=(8, 5))
plt.plot(range(len(y_test)), y_test.values, label="Actual Demand", marker="o")
plt.plot(range(len(predictions)), predictions, label="Predicted Demand", marker="x")
plt.title("Actual vs Predicted Demand")
plt.xlabel("Test Record")
plt.ylabel("Demand")
plt.legend()
plt.tight_layout()
plt.savefig("assets/actual_vs_predicted_demand.png")
plt.show()
