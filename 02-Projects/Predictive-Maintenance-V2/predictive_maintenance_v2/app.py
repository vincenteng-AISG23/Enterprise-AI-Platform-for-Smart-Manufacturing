from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "model.joblib"
METRICS_PATH = BASE_DIR / "outputs" / "metrics.json"
IMPORTANCE_PATH = BASE_DIR / "outputs" / "feature_importance.csv"

st.set_page_config(page_title="Predictive Maintenance V2", layout="wide")
st.title("Predictive Maintenance V2")
st.caption("A portfolio-ready smart manufacturing demo")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_metrics():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_importance():
    return pd.read_csv(IMPORTANCE_PATH)

model = load_model()
metrics = load_metrics()
feature_importance = load_importance()

col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", metrics["accuracy"])
col2.metric("Recall", metrics["recall"])
col3.metric("ROC AUC", metrics["roc_auc"])

st.subheader("Machine risk scoring")

with st.form("score_form"):
    machine_id = st.selectbox("Machine ID", [f"MCH-{i:03d}" for i in range(1, 31)], index=6)
    shift = st.selectbox("Shift", ["day", "night"], index=1)
    machine_age_years = st.slider("Machine age (years)", 0.5, 15.0, 8.4)
    maintenance_overdue_days = st.slider("Maintenance overdue (days)", 0.0, 60.0, 29.0)
    load_pct = st.slider("Load (%)", 20.0, 110.0, 88.0)
    rpm = st.slider("RPM", 700.0, 3200.0, 1720.0)
    temperature_c = st.slider("Temperature (°C)", 35.0, 120.0, 84.0)
    vibration_mm_s = st.slider("Vibration (mm/s)", 0.2, 16.0, 7.2)
    pressure_bar = st.slider("Pressure (bar)", 2.0, 12.5, 8.9)
    sound_db = st.slider("Sound (dB)", 45.0, 120.0, 91.0)
    humidity_pct = st.slider("Humidity (%)", 15.0, 95.0, 67.0)

    submitted = st.form_submit_button("Score machine")

if submitted:
    X_new = pd.DataFrame([{
        "machine_id": machine_id,
        "shift": shift,
        "machine_age_years": machine_age_years,
        "maintenance_overdue_days": maintenance_overdue_days,
        "load_pct": load_pct,
        "rpm": rpm,
        "temperature_c": temperature_c,
        "vibration_mm_s": vibration_mm_s,
        "pressure_bar": pressure_bar,
        "sound_db": sound_db,
        "humidity_pct": humidity_pct,
    }])

    risk_probability = model.predict_proba(X_new)[:, 1][0]
    prediction = model.predict(X_new)[0]

    st.write("### Prediction result")
    st.write(f"Failure risk within 7 days: **{risk_probability:.2%}**")
    st.write(f"Predicted class: **{'High risk' if prediction == 1 else 'Lower risk'}**")

st.subheader("Top feature importance")
st.dataframe(feature_importance.head(15), use_container_width=True)
