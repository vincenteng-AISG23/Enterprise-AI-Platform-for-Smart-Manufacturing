import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.title("Predictive Maintenance Dashboard")

# Load model
model = joblib.load("model.pkl")

# Load data
df = pd.read_csv("sample_predictive_maintenance_data.csv")

st.subheader("Sample Data")
st.dataframe(df.head())

# Prediction
if st.button("Run Prediction"):
    df["failure_probability"] = model.predict_proba(df.drop("failure", axis=1))[:, 1]

    st.subheader("Prediction Results")
    st.dataframe(df)

    # 📊 Chart 1 — Failure Probability Distribution
    st.subheader("Failure Probability Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(df["failure_probability"], bins=20)
    st.pyplot(fig1)

    # 📊 Chart 2 — Risk Classification
    st.subheader("Risk Levels")

    def classify_risk(x):
        if x > 0.7:
            return "High"
        elif x > 0.4:
            return "Medium"
        else:
            return "Low"

    df["risk_level"] = df["failure_probability"].apply(classify_risk)

    risk_counts = df["risk_level"].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.bar(risk_counts.index, risk_counts.values)
    st.pyplot(fig2)
    