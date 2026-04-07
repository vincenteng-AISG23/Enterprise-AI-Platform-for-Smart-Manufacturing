import os
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Enterprise Predictive Maintenance Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load data and model
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "sample_predictive_maintenance_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "src", "model.pkl")

df = pd.read_csv(CSV_PATH)
model = joblib.load(MODEL_PATH)

# --------------------------------------------------
# Add enterprise-style fields if not already present
# --------------------------------------------------
if "machine_id" not in df.columns:
    df["machine_id"] = [f"M{str(i + 1).zfill(3)}" for i in range(len(df))]

if "plant" not in df.columns:
    plants = ["Plant MY", "Plant SG", "Plant TH"]
    df["plant"] = [plants[i % len(plants)] for i in range(len(df))]

if "line" not in df.columns:
    df["line"] = [f"L{(i % 3) + 1}" for i in range(len(df))]

# Ensure temperature_diff exists for scoring the full dataset
df["temperature_diff"] = df["process_temperature"] - df["air_temperature"]

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.title("AI Predictive Maintenance Dashboard")
st.caption("Enterprise Smart Manufacturing machine failure prediction, prioritization, and business impact analysis")

st.sidebar.header("Enterprise Filters")

plant_options = ["All"] + sorted(df["plant"].unique().tolist())
selected_plant = st.sidebar.selectbox("Plant Filter", plant_options)

filtered_df = df.copy()
if selected_plant != "All":
    filtered_df = filtered_df[filtered_df["plant"] == selected_plant].copy()

machine_options = filtered_df["machine_id"].tolist()
selected_machine = st.sidebar.selectbox("Select Machine", machine_options)

selected_row = filtered_df[filtered_df["machine_id"] == selected_machine].iloc[0]

# --------------------------------------------------
# Sidebar simulation sliders
# --------------------------------------------------
st.sidebar.header("Simulation")

air_temperature = st.sidebar.slider(
    "Air Temperature",
    float(df["air_temperature"].min() - 5),
    float(df["air_temperature"].max() + 5),
    float(selected_row["air_temperature"])
)

process_temperature = st.sidebar.slider(
    "Process Temperature",
    float(df["process_temperature"].min() - 5),
    float(df["process_temperature"].max() + 5),
    float(selected_row["process_temperature"])
)

rotational_speed = st.sidebar.slider(
    "Rotational Speed",
    int(df["rotational_speed"].min() - 100),
    int(df["rotational_speed"].max() + 100),
    int(selected_row["rotational_speed"])
)

torque = st.sidebar.slider(
    "Torque",
    float(df["torque"].min() - 10),
    float(df["torque"].max() + 10),
    float(selected_row["torque"])
)

tool_wear = st.sidebar.slider(
    "Tool Wear",
    int(df["tool_wear"].min()),
    int(df["tool_wear"].max() + 20),
    int(selected_row["tool_wear"])
)

# --------------------------------------------------
# Real ML prediction for selected machine
# --------------------------------------------------
temperature_diff = process_temperature - air_temperature

features = pd.DataFrame([{
    "air_temperature": air_temperature,
    "process_temperature": process_temperature,
    "rotational_speed": rotational_speed,
    "torque": torque,
    "tool_wear": tool_wear,
    "temperature_diff": temperature_diff
}])

failure_probability = model.predict_proba(features)[0][1]
prediction = model.predict(features)[0]

if failure_probability > 0.7:
    risk_level = "HIGH"
    recommended_action = "Immediate inspection and maintenance action"
    estimated_loss = 50000
elif failure_probability > 0.4:
    risk_level = "MEDIUM"
    recommended_action = "Plan maintenance soon"
    estimated_loss = 10000
else:
    risk_level = "LOW"
    recommended_action = "Continue normal operation"
    estimated_loss = 2000

# --------------------------------------------------
# Batch scoring for KPI dashboard
# --------------------------------------------------
score_features = filtered_df[[
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
    "temperature_diff"
]].copy()

filtered_df["failure_probability"] = model.predict_proba(score_features)[:, 1]

def classify_risk(probability: float) -> str:
    if probability > 0.7:
        return "HIGH"
    if probability > 0.4:
        return "MEDIUM"
    return "LOW"

filtered_df["risk_level"] = filtered_df["failure_probability"].apply(classify_risk)
filtered_df["estimated_risk_cost"] = filtered_df["risk_level"].map({
    "HIGH": 50000,
    "MEDIUM": 10000,
    "LOW": 2000
})

high_count = int((filtered_df["risk_level"] == "HIGH").sum())
medium_count = int((filtered_df["risk_level"] == "MEDIUM").sum())
low_count = int((filtered_df["risk_level"] == "LOW").sum())
total_risk_exposure = int(filtered_df["estimated_risk_cost"].sum())

# --------------------------------------------------
# Executive alerts and summary
# --------------------------------------------------
if high_count > 0:
    st.error(f"🚨 ALERT: {high_count} machines require immediate attention.")
else:
    st.success("✅ No machines are currently in the HIGH risk category.")

plant_risk = filtered_df.groupby("plant")["estimated_risk_cost"].sum()
top_plant = plant_risk.idxmax()
top_plant_cost = int(plant_risk.max())

st.info(
    f"Executive Summary: {high_count} high-risk machines are currently creating an estimated risk exposure "
    f"of SGD {total_risk_exposure:,.0f}. Highest exposure is concentrated in {top_plant} "
    f"at SGD {top_plant_cost:,.0f}."
)

# --------------------------------------------------
# KPI cards
# --------------------------------------------------
st.subheader("Factory Maintenance KPIs")
col1, col2, col3, col4 = st.columns(4)

col1.metric("High Risk Machines", high_count)
col2.metric("Medium Risk Machines", medium_count)
col3.metric("Low Risk Machines", low_count)
col4.metric("Total Risk Exposure (SGD)", f"${total_risk_exposure:,.0f}")

st.subheader("Risk Distribution")

risk_counts = filtered_df["risk_level"].value_counts().reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)

fig1, ax1 = plt.subplots()
risk_counts.plot(kind="bar", ax=ax1)
ax1.set_title("Machine Risk Distribution")
ax1.set_ylabel("Number of Machines")
ax1.set_xlabel("Risk Level")
st.pyplot(fig1)

# --------------------------------------------------
# Selected machine details
# --------------------------------------------------
st.subheader("Selected Machine Prediction")
c1, c2 = st.columns(2)

with c1:
    st.write(f"**Machine ID:** {selected_machine}")
    st.write(f"**Plant:** {selected_row['plant']}")
    st.write(f"**Line:** {selected_row['line']}")
    st.write(f"**Predicted Failure Probability:** {failure_probability:.2%}")
    st.write(f"**Risk Level:** {risk_level}")

with c2:
    st.write(f"**Recommended Action:** {recommended_action}")
    st.write(f"**Estimated Downtime Cost:** SGD {estimated_loss:,.0f}")
    st.write(f"**Prediction Class:** {int(prediction)}")

# --------------------------------------------------
# Risk distribution table
# --------------------------------------------------
st.subheader("Risk Distribution Overview")

display_df = filtered_df[[
    "machine_id",
    "plant",
    "line",
    "failure_probability",
    "risk_level",
    "estimated_risk_cost"
]].copy()

display_df["failure_probability"] = display_df["failure_probability"].map(lambda x: f"{x:.2%}")
display_df["estimated_risk_cost"] = display_df["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")

st.dataframe(display_df, use_container_width=True)

st.subheader("Plant Risk Exposure")

plant_risk = filtered_df.groupby("plant")["estimated_risk_cost"].sum()

fig2, ax2 = plt.subplots()
plant_risk.plot(kind="bar", ax=ax2)
ax2.set_title("Risk Exposure by Plant")
ax2.set_ylabel("Estimated Risk Cost (SGD)")
ax2.set_xlabel("Plant")
st.pyplot(fig2)

st.subheader("Top 5 High-Risk Machines")

top5 = filtered_df.sort_values(by="failure_probability", ascending=False).head(5).copy()
top5["failure_probability"] = top5["failure_probability"].map(lambda x: f"{x:.2%}")
top5["estimated_risk_cost"] = top5["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")

st.dataframe(
    top5[["machine_id", "plant", "line", "failure_probability", "risk_level", "estimated_risk_cost"]],
    use_container_width=True
)