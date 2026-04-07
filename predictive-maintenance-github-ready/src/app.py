from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

from utils import create_health_rule_based_features


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "predictive_maintenance_model.pkl"

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


st.title("Predictive Maintenance Dashboard")
st.write("Estimate machine failure risk based on operational parameters.")

if not MODEL_PATH.exists():
    st.warning("Model file not found. Please run `python src/train.py` first.")
    st.stop()

model = load_model()

with st.sidebar:
    st.header("Input Machine Parameters")
    machine_id = st.number_input("Machine ID", min_value=1, value=101)
    temperature = st.number_input("Temperature", value=75.0)
    vibration = st.number_input("Vibration", value=0.45)
    pressure = st.number_input("Pressure", value=28.0)
    runtime_hours = st.number_input("Runtime Hours", value=1200)
    maintenance_count = st.number_input("Maintenance Count", value=2)
    error_count = st.number_input("Error Count", value=5)

input_df = pd.DataFrame([
    {
        "machine_id": machine_id,
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "runtime_hours": runtime_hours,
        "maintenance_count": maintenance_count,
        "error_count": error_count,
    }
])

feature_df = create_health_rule_based_features(input_df)

if st.button("Predict Risk"):
    prediction = model.predict(feature_df)[0]
    probability = model.predict_proba(feature_df)[0][1]

    st.subheader("Prediction Result")
    st.write(f"Failure Prediction: {'High Risk' if prediction == 1 else 'Low Risk'}")
    st.write(f"Failure Probability: {probability:.2%}")

    if probability >= 0.7:
        st.error("Immediate inspection recommended.")
    elif probability >= 0.4:
        st.warning("Plan maintenance soon.")
    else:
        st.success("Machine currently appears stable.")

st.subheader("Current Input Data")
st.dataframe(input_df)