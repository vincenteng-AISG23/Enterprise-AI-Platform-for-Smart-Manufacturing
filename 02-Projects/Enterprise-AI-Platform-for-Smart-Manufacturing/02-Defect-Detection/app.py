import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="AI Defect Detection Dashboard", layout="wide")

st.title("AI Defect Detection Dashboard")
st.caption("Smart Manufacturing quality inspection demo")

# Load data
data = pd.read_csv("sample_defect_data.csv")

# Build training features safely
X = data.drop(columns=["defect"], errors="ignore")
X = X.select_dtypes(include=["number"])
y = data["defect"]

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Sidebar inputs
st.sidebar.header("Input Parameters")

color_variation = st.sidebar.slider("Color Variation", 0.0, 10.0, 3.0, 0.1)
edge_roughness = st.sidebar.slider("Edge Roughness", 0.0, 10.0, 3.0, 0.1)
scratch_score = st.sidebar.slider("Scratch Score", 0.0, 10.0, 2.0, 0.1)
shape_deviation = st.sidebar.slider("Shape Deviation", 0.0, 10.0, 1.0, 0.1)

# Create input in exact model feature structure
input_df = pd.DataFrame([{
    "edge_roughness": edge_roughness,
    "color_variation": color_variation,
    "scratch_score": scratch_score,
    "shape_deviation": shape_deviation
}])

# Force exact training column order
input_df = input_df.reindex(columns=X.columns)

# Predict
prediction = model.predict(input_df)[0]
prediction_proba = model.predict_proba(input_df)[0]

# KPI row
col1, col2, col3 = st.columns(3)

# Executive KPI Panel
st.subheader("Production KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Estimated Defect Rate", f"{prediction_proba[1]*100:.1f}%")
col2.metric("Quality Score", f"{100 - prediction_proba[1]*100:.1f}%")
col3.metric("Inspection Confidence", "High")

with col1:
    st.metric("Prediction", "Defect Detected" if prediction == 1 else "No Defect")

with col2:
    st.metric("Defect Probability", f"{prediction_proba[1] * 100:.1f}%")

with col3:
    st.metric("Non-Defect Probability", f"{prediction_proba[0] * 100:.1f}%")

if prediction_proba[1] > 0.7:
    st.error("🔴 High Risk of Defect")
elif prediction_proba[1] > 0.4:
    st.warning("🟠 Medium Risk of Defect")
else:
    st.success("🟢 Low Risk of Defect")

# Business interpretation
st.subheader("Business Interpretation")
if prediction == 1:
    st.error("High likelihood of defect. Recommend quality hold and inspection.")
else:
    st.success("Low likelihood of defect. Part can proceed to next stage.")


# Recommended action
st.subheader("Recommended Action")

if prediction_proba[1] > 0.7:
    st.error("🚨 Stop production. Perform immediate quality inspection.")
elif prediction_proba[1] > 0.4:
    st.warning("⚠️ Increase inspection frequency and monitor closely.")
else:
    st.success("✅ Proceed with production. Maintain standard QC checks.")

# Input summary
st.subheader("Input Data")
st.dataframe(input_df, use_container_width=True)

# Feature importance
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

st.subheader("Feature Importance")
st.bar_chart(feature_importance)

# Cost Impact
st.subheader("Estimated Cost Impact")

cost_per_defect = 50  # SGD (adjust later)
daily_volume = 1000   # production volume

estimated_loss = prediction_proba[1] * daily_volume * cost_per_defect

st.metric("Estimated Daily Loss (SGD)", f"${estimated_loss:,.0f}")

# Sample data preview
st.subheader("Sample Training Data")
st.dataframe(data.head(), use_container_width=True)

# Business impact section
st.subheader("Potential Business Impact")
st.markdown("""
- Reduce manual inspection effort  
- Improve product quality consistency  
- Reduce scrap and rework  
- Support smarter shopfloor quality control  
""")

# Smart Factory Insight
st.subheader("Smart Factory Insight")

st.markdown("""
This AI model enables:
- Real-time defect prediction on production lines  
- Reduced manual inspection workload  
- Early detection of quality issues  
- Continuous improvement through data-driven insights  
""")