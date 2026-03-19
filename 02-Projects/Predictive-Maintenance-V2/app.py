import os
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="AI Predictive Maintenance Dashboard", layout="wide")

# -----------------------------
# Load data
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "sample_predictive_maintenance_data.csv")
data = pd.read_csv(csv_path)

# -----------------------------
# Feature engineering
# -----------------------------
data["temperature_diff"] = data["process_temperature"] - data["air_temperature"]

# -----------------------------
# Train model
# -----------------------------
feature_cols = [
    "air_temperature",
    "process_temperature",
    "temperature_diff",
    "rotational_speed",
    "torque",
    "tool_wear",
]

X = data[feature_cols]
y = data["machine_failure"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict all machines
data["failure_probability"] = model.predict_proba(X)[:, 1]

# -----------------------------
# Business logic
# -----------------------------
def classify_risk(prob: float) -> str:
    if prob > 0.7:
        return "HIGH"
    elif prob > 0.4:
        return "MEDIUM"
    return "LOW"


def recommend_action(prob: float) -> str:
    if prob > 0.7:
        return "🚨 Stop machine immediately and perform maintenance"
    elif prob > 0.4:
        return "⚠️ Increase inspection frequency and monitor closely"
    return "✅ Continue normal operation"


def estimated_cost(prob: float) -> int:
    if prob > 0.7:
        return 30000
    elif prob > 0.4:
        return 10000
    return 2000


data["risk_level"] = data["failure_probability"].apply(classify_risk)
data["recommended_action"] = data["failure_probability"].apply(recommend_action)
data["estimated_downtime_cost"] = data["failure_probability"].apply(estimated_cost)

# -----------------------------
# KPI calculations
# -----------------------------
high_risk_count = int((data["risk_level"] == "HIGH").sum())
medium_risk_count = int((data["risk_level"] == "MEDIUM").sum())
low_risk_count = int((data["risk_level"] == "LOW").sum())
total_estimated_cost = int(data["estimated_downtime_cost"].sum())

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Machine Selection")
selected_part = st.sidebar.selectbox("Select Machine", data["part_id"].tolist())

selected_row = data[data["part_id"] == selected_part].iloc[0]

st.sidebar.subheader("Simulation")

sim_air_temp = st.sidebar.slider(
    "Air Temperature",
    float(data["air_temperature"].min()),
    float(data["air_temperature"].max()),
    float(selected_row["air_temperature"]),
)

sim_process_temp = st.sidebar.slider(
    "Process Temperature",
    float(data["process_temperature"].min()),
    float(data["process_temperature"].max()),
    float(selected_row["process_temperature"]),
)

sim_rot_speed = st.sidebar.slider(
    "Rotational Speed",
    int(data["rotational_speed"].min()),
    int(data["rotational_speed"].max()),
    int(selected_row["rotational_speed"]),
)

sim_torque = st.sidebar.slider(
    "Torque",
    float(data["torque"].min()),
    float(data["torque"].max()),
    float(selected_row["torque"]),
)

sim_tool_wear = st.sidebar.slider(
    "Tool Wear",
    int(data["tool_wear"].min()),
    int(data["tool_wear"].max()),
    int(selected_row["tool_wear"]),
)

sim_temp_diff = sim_process_temp - sim_air_temp

simulation_input = pd.DataFrame([{
    "air_temperature": sim_air_temp,
    "process_temperature": sim_process_temp,
    "temperature_diff": sim_temp_diff,
    "rotational_speed": sim_rot_speed,
    "torque": sim_torque,
    "tool_wear": sim_tool_wear,
}])

sim_failure_prob = float(model.predict_proba(simulation_input)[0][1])
sim_risk_level = classify_risk(sim_failure_prob)
sim_action = recommend_action(sim_failure_prob)
sim_cost = estimated_cost(sim_failure_prob)
sim_health_score = 100 - (sim_failure_prob * 100)

# -----------------------------
# Header
# -----------------------------
st.title("AI Predictive Maintenance Dashboard")
st.caption("Smart Manufacturing machine failure prediction and maintenance decision support")

# Upgrade 1: Executive alert banner
if high_risk_count > 0:
    st.error(f"🚨 ALERT: {high_risk_count} machines require immediate attention!")
else:
    st.success("✅ All machines operating within safe limits")

# -----------------------------
# KPI section
# -----------------------------
st.subheader("Factory Maintenance KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("High Risk Machines", high_risk_count)
c2.metric("Medium Risk Machines", medium_risk_count)
c3.metric("Low Risk Machines", low_risk_count)
c4.metric("Total Risk Exposure (SGD)", f"${total_estimated_cost:,.0f}")

# Upgrade 3: Risk distribution chart
st.subheader("Risk Distribution Overview")
risk_counts = (
    data["risk_level"]
    .value_counts()
    .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
)
st.bar_chart(risk_counts)

# -----------------------------
# Selected machine / simulation summary
# -----------------------------
st.subheader("Selected Machine Risk Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Machine", selected_part)
m2.metric("Failure Probability", f"{sim_failure_prob * 100:.1f}%")
m3.metric("Machine Health Score", f"{sim_health_score:.1f}%")
m4.metric("Estimated Downtime Cost", f"${sim_cost:,.0f}")

if sim_risk_level == "HIGH":
    st.error("🔴 High Risk – Immediate intervention required")
elif sim_risk_level == "MEDIUM":
    st.warning("🟠 Medium Risk – Monitor closely and inspect")
else:
    st.success("🟢 Low Risk – Continue normal operation")

st.subheader("Recommended Action")
if sim_risk_level == "HIGH":
    st.error("🚨 Stop machine immediately and perform maintenance.")
elif sim_risk_level == "MEDIUM":
    st.warning("⚠️ Increase inspection frequency and monitor closely.")
else:
    st.success("✅ Continue normal operation under standard monitoring.")

# Upgrade 4: Why this machine is risky
st.subheader("Why This Machine is At Risk")

feature_importance = pd.Series(
    model.feature_importances_,
    index=feature_cols
).sort_values(ascending=False)

top_driver = feature_importance.index[0]
st.info(f"Top model driver overall: **{top_driver}**")

risk_messages = []

if sim_torque > data["torque"].median():
    risk_messages.append("High torque detected — possible overload condition.")
if sim_tool_wear > data["tool_wear"].median():
    risk_messages.append("Tool wear is above normal — maintenance may be needed soon.")
if sim_temp_diff > data["temperature_diff"].median():
    risk_messages.append("Temperature difference is elevated — potential thermal stress.")
if sim_rot_speed < data["rotational_speed"].median():
    risk_messages.append("Lower rotational speed with stress variables may indicate unstable operating condition.")

if risk_messages:
    for msg in risk_messages:
        st.warning(msg)
else:
    st.success("No major abnormal operating stress signals detected for this simulation.")

# -----------------------------
# Machine operating parameters
# -----------------------------
st.subheader("Machine Operating Parameters")
machine_display = pd.DataFrame([{
    "part_id": selected_part,
    "air_temperature": sim_air_temp,
    "process_temperature": sim_process_temp,
    "temperature_diff": sim_temp_diff,
    "rotational_speed": sim_rot_speed,
    "torque": sim_torque,
    "tool_wear": sim_tool_wear,
    "risk_level": sim_risk_level,
}])
st.dataframe(machine_display, width="stretch")

# -----------------------------
# Failure driver importance
# -----------------------------
st.subheader("Failure Driver Importance")
st.bar_chart(feature_importance)

# -----------------------------
# Upgrade 2: Fleet overview sorted high risk first
# -----------------------------
st.subheader("Fleet Maintenance Overview")

fleet_view = data[[
    "part_id",
    "type",
    "failure_probability",
    "risk_level",
    "recommended_action",
    "estimated_downtime_cost"
]].copy()

fleet_view["failure_probability"] = (fleet_view["failure_probability"] * 100).round(1)
fleet_view["estimated_downtime_cost"] = fleet_view["estimated_downtime_cost"].astype(int)

risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
fleet_view["risk_priority"] = fleet_view["risk_level"].map(risk_order)
fleet_view = fleet_view.sort_values(by=["risk_priority", "failure_probability"], ascending=[True, False])
fleet_view = fleet_view.drop(columns=["risk_priority"])

fleet_view["failure_probability"] = fleet_view["failure_probability"].astype(str) + "%"
fleet_view["estimated_downtime_cost"] = fleet_view["estimated_downtime_cost"].apply(lambda x: f"${x:,.0f}")

st.dataframe(fleet_view, width="stretch")

# -----------------------------
# Business impact
# -----------------------------
st.subheader("Business Impact")
st.markdown("""
- Reduce unplanned equipment downtime  
- Prioritize maintenance resources more effectively  
- Lower production disruption risk  
- Improve plant reliability and maintenance planning  
""")

# -----------------------------
# Smart factory insight
# -----------------------------
st.subheader("Smart Factory Insight")
st.markdown("""
This dashboard demonstrates how AI can support predictive maintenance by:

- detecting machine failure risks earlier  
- identifying high-risk assets across the factory fleet  
- recommending maintenance actions based on risk level  
- translating technical signals into operational and financial decisions  
""")