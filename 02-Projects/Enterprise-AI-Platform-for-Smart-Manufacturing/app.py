import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise AI Platform for Smart Manufacturing",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
PM_DIR = BASE_DIR / "01-Predictive-Maintenance"
DD_DIR = BASE_DIR / "02-Defect-Detection"
DF_DIR = BASE_DIR / "03-Demand-Forecasting"

st.title("Enterprise AI Platform for Smart Manufacturing")
st.caption("Integrated AI use cases across maintenance, quality, and planning")

# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------
st.sidebar.title("Platform Navigation")
module = st.sidebar.radio(
    "Select Module",
    [
        "Executive Overview",
        "Predictive Maintenance",
        "Defect Detection",
        "Demand Forecasting"
    ]
)

# --------------------------------------------------
# Shared helper functions
# --------------------------------------------------
def safe_read_csv(path: Path):
    try:
        if path.exists():
            return pd.read_csv(path)
    except Exception:
        return None
    return None


def module_health_status():
    pm_model_ok = (PM_DIR / "model.pkl").exists()
    pm_data_ok = (PM_DIR / "sample_machine_data.csv").exists()

    dd_image_ok = len(list(DD_DIR.glob("*.png")) + list((DD_DIR / "assets").glob("*.png"))) > 0
    dd_csv_ok = len(list(DD_DIR.glob("*.csv"))) > 0

    df_csv_ok = (DF_DIR / "demand_forecast_sample.csv").exists()

    return {
        "pm": pm_model_ok and pm_data_ok,
        "dd": dd_image_ok or dd_csv_ok,
        "df": df_csv_ok
    }


def get_platform_kpis():
    high_risk_machines = 0
    total_risk_exposure = 0.0
    defect_records = 0
    forecast_accuracy_display = "N/A"

    # Predictive Maintenance KPI
    try:
        pm_model_path = PM_DIR / "model.pkl"
        pm_machine_path = PM_DIR / "sample_machine_data.csv"

        if pm_model_path.exists() and pm_machine_path.exists():
            pm_model = joblib.load(pm_model_path)
            pm_df = pd.read_csv(pm_machine_path)
            pm_df.columns = [c.strip().lower() for c in pm_df.columns]

            temp_col = "temperature_c" if "temperature_c" in pm_df.columns else None
            pressure_col = "pressure_psi" if "pressure_psi" in pm_df.columns else None
            vib_col = "vibration_mm_s" if "vibration_mm_s" in pm_df.columns else None

            if temp_col and pressure_col and vib_col:
                pm_input = pd.DataFrame({
                    "temperature": pm_df[temp_col],
                    "pressure": pm_df[pressure_col],
                    "vibration": pm_df[vib_col],
                    "humidity": 40.0
                })

                probs = pm_model.predict_proba(pm_input)[:, 1]
                high_risk_machines = int((probs > 0.7).sum())
                total_risk_exposure = float((probs * 10000).sum())
    except Exception:
        pass

    # Defect Detection KPI
    try:
        dd_csvs = list(DD_DIR.glob("*.csv"))
        if dd_csvs:
            dd_df = pd.read_csv(dd_csvs[0])
            defect_records = len(dd_df)
    except Exception:
        pass

    # Demand Forecasting KPI
    try:
        forecast_path = DF_DIR / "demand_forecast_sample.csv"
        if forecast_path.exists():
            forecast_df = pd.read_csv(forecast_path)
            forecast_df.columns = [c.strip().lower() for c in forecast_df.columns]

            if {"actual_demand", "forecast_demand"}.issubset(set(forecast_df.columns)):
                forecast_df["error"] = (
                    forecast_df["actual_demand"] - forecast_df["forecast_demand"]
                ).abs()
                acc = 1 - (forecast_df["error"].mean() / forecast_df["actual_demand"].mean())
                forecast_accuracy_display = f"{acc:.2%}"
    except Exception:
        pass

    return high_risk_machines, total_risk_exposure, defect_records, forecast_accuracy_display


def classify_risk(probability: float):
    if probability > 0.7:
        return "High", "Immediate maintenance required"
    if probability > 0.4:
        return "Medium", "Schedule inspection"
    return "Low", "Continue normal operation"


# --------------------------------------------------
# Executive Overview
# --------------------------------------------------
if module == "Executive Overview":
    st.subheader("Executive Overview")

    high_risk_machines, total_risk_exposure, defect_records, forecast_accuracy_display = get_platform_kpis()
    health = module_health_status()

    st.markdown(
        """
This platform demonstrates how AI can be applied across multiple manufacturing domains and consolidated into
a single executive decision layer for operations, quality, and planning.

It brings together three practical AI use cases:

- **Predictive Maintenance** for reliability improvement  
- **Defect Detection** for quality enhancement  
- **Demand Forecasting** for production planning  
"""
    )

    st.markdown("### Platform KPI Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("High-Risk Machines", high_risk_machines)
    k2.metric("Total Risk Exposure", f"SGD {total_risk_exposure:,.0f}")
    k3.metric("Defect Records", defect_records)
    k4.metric("Forecast Accuracy", forecast_accuracy_display)

    st.markdown("### Module Health")
    h1, h2, h3 = st.columns(3)
    h1.metric("Predictive Maintenance", "Active" if health["pm"] else "Missing Files")
    h2.metric("Defect Detection", "Active" if health["dd"] else "Missing Files")
    h3.metric("Demand Forecasting", "Active" if health["df"] else "Missing Files")

    st.markdown("### Platform Overview")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("AI Use Cases", "3")
    p2.metric("Business Domains", "Reliability / Quality / Planning")
    p3.metric("Platform Type", "Enterprise AI Portfolio")
    p4.metric("Decision Layer", "Executive Control Tower")

    st.markdown("### Executive Summary")
    st.info(
        f"""
This platform translates AI outputs into business decision support.

Current indicators suggest:
- **{high_risk_machines} high-risk machine(s)** identified from available maintenance data
- **SGD {total_risk_exposure:,.0f}** estimated downtime exposure across the monitored set
- **{defect_records} defect-related record(s)** available for quality review
- **Forecast accuracy of {forecast_accuracy_display}** based on available demand planning data
"""
    )

    st.markdown("### Strategic Scope")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
**Operational Focus**
- Improve asset reliability
- Reduce quality defects
- Strengthen planning accuracy
- Increase visibility across operations

**Transformation Focus**
- Move from reactive to predictive maintenance
- Move from manual inspection to AI-assisted quality control
- Move from historical planning to forecast-driven planning
"""
        )

    with c2:
        st.markdown(
            """
**Leadership Focus**
- Translate AI output into business actions
- Provide KPI-driven visibility to decision makers
- Strengthen cross-functional alignment between operations, quality, and planning
- Demonstrate how AI can support enterprise transformation
"""
        )

    st.markdown("### Business Value")
    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown(
            """
**Reliability**
- Reduce unplanned downtime
- Lower maintenance cost
- Improve equipment availability
"""
        )

    with b2:
        st.markdown(
            """
**Quality**
- Detect faults earlier
- Reduce scrap and rework
- Improve product consistency
"""
        )

    with b3:
        st.markdown(
            """
**Planning**
- Improve demand visibility
- Support production scheduling
- Reduce planning inefficiencies
"""
        )

    st.markdown("### AI Use Case Portfolio")
    u1, u2, u3 = st.columns(3)

    with u1:
        st.markdown(
            """
#### Predictive Maintenance
**Purpose:** predict machine failure risk before breakdown

**Key Outputs:**
- failure probability
- risk classification
- estimated downtime impact

**Business Outcome:**
improved maintenance prioritization and reduced disruption
"""
        )

    with u2:
        st.markdown(
            """
#### Defect Detection
**Purpose:** improve inspection effectiveness through AI-assisted quality analysis

**Key Outputs:**
- defect visualization
- defect result review
- quality support insights

**Business Outcome:**
better defect control and lower scrap
"""
        )

    with u3:
        st.markdown(
            """
#### Demand Forecasting
**Purpose:** improve planning through demand trend and forecast comparison

**Key Outputs:**
- actual vs forecast trend
- forecast accuracy
- planning insights

**Business Outcome:**
improved forecast confidence and planning quality
"""
        )

    st.markdown("### Suggested Enterprise Architecture")
    st.code(
        "ERP / MES / Sensors / Images / Demand History\n"
        "                ↓\n"
        "Data Preparation / Feature Engineering\n"
        "                ↓\n"
        "Machine Learning Models by Use Case\n"
        "                ↓\n"
        "Business Rules / KPI Logic / Executive Insights\n"
        "                ↓\n"
        "Enterprise AI Control Tower"
    )

    st.markdown("### Recommended Next Actions")
    action_items = []
    if high_risk_machines > 0:
        action_items.append(f"- Review and prioritize maintenance plan for **{high_risk_machines} high-risk machine(s)**")
    if defect_records > 0:
        action_items.append(f"- Review **{defect_records} defect-related record(s)** for recurring quality issues")
    if forecast_accuracy_display != "N/A":
        action_items.append(f"- Validate forecast assumptions against the latest planning accuracy of **{forecast_accuracy_display}**")
    if not action_items:
        action_items.append("- Load module data sources to activate platform-level decision support")

    st.markdown("\n".join(action_items))

    st.markdown("### CIO Perspective")
    st.warning(
        """
This is not just a model showcase.

It demonstrates how AI can be framed as an **enterprise capability** by linking predictive analytics to
operational priorities, executive KPIs, and business decision support.
"""
    )

# --------------------------------------------------
# Predictive Maintenance
# --------------------------------------------------
elif module == "Predictive Maintenance":
    st.subheader("Predictive Maintenance")

    model_path = PM_DIR / "model.pkl"
    if not model_path.exists():
        st.error("Model file not found. Please run train_model.py inside 01-Predictive-Maintenance first.")
        st.stop()

    model = joblib.load(model_path)

    machine_file = PM_DIR / "sample_machine_data.csv"
    if not machine_file.exists():
        st.error("sample_machine_data.csv not found inside 01-Predictive-Maintenance.")
        st.stop()

    machine_df = pd.read_csv(machine_file)
    machine_df.columns = [c.strip().lower() for c in machine_df.columns]

    machine_id_col = "machine_id"
    line_col = "production_line" if "production_line" in machine_df.columns else None
    shift_col = "shift" if "shift" in machine_df.columns else None
    hours_col = "operating_hours_per_day" if "operating_hours_per_day" in machine_df.columns else None
    temp_col = "temperature_c" if "temperature_c" in machine_df.columns else None
    vib_col = "vibration_mm_s" if "vibration_mm_s" in machine_df.columns else None
    pressure_col = "pressure_psi" if "pressure_psi" in machine_df.columns else None

    if machine_id_col not in machine_df.columns:
        st.error("sample_machine_data.csv must contain a 'machine_id' column.")
        st.stop()

    if not all([temp_col, vib_col, pressure_col]):
        st.error("sample_machine_data.csv must contain temperature_c, vibration_mm_s, and pressure_psi columns.")
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.subheader("PM Filters")

    filtered_df = machine_df.copy()

    if line_col:
        line_list = ["All"] + sorted(filtered_df[line_col].dropna().astype(str).unique().tolist())
        selected_line = st.sidebar.selectbox("Production Line", line_list)
        if selected_line != "All":
            filtered_df = filtered_df[filtered_df[line_col].astype(str) == selected_line]

    if shift_col:
        shift_list = ["All"] + sorted(filtered_df[shift_col].dropna().astype(str).unique().tolist())
        selected_shift = st.sidebar.selectbox("Shift", shift_list)
        if selected_shift != "All":
            filtered_df = filtered_df[filtered_df[shift_col].astype(str) == selected_shift]

    machine_list = filtered_df[machine_id_col].dropna().astype(str).tolist()
    if not machine_list:
        st.warning("No machines found for the selected filters.")
        st.stop()

    selected_machine = st.sidebar.selectbox("Select Machine", machine_list)
    selected_row = filtered_df[filtered_df[machine_id_col].astype(str) == selected_machine].iloc[0]

    default_temp = float(selected_row[temp_col]) if pd.notna(selected_row[temp_col]) else 80.0
    default_pressure = float(selected_row[pressure_col]) if pd.notna(selected_row[pressure_col]) else 30.0
    default_vibration = float(selected_row[vib_col]) if pd.notna(selected_row[vib_col]) else 0.5
    default_humidity = 40.0

    st.sidebar.markdown("### Simulation")
    temperature = st.sidebar.slider("Temperature (°C)", 50.0, 120.0, float(default_temp))
    pressure = st.sidebar.slider("Pressure (psi)", 20.0, 200.0, float(default_pressure))
    vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 20.0, float(default_vibration))
    humidity = st.sidebar.slider("Humidity (%)", 20.0, 80.0, float(default_humidity))

    input_data = pd.DataFrame(
        [[temperature, pressure, vibration, humidity]],
        columns=["temperature", "pressure", "vibration", "humidity"]
    )

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    risk_level, recommended_action = classify_risk(probability)
    estimated_loss = probability * 10000

    st.markdown(
        f"""
<div style="padding:10px; border-radius:8px; background-color:#eef6ff; margin-bottom:10px;">
<strong>Executive Summary:</strong> Machine <strong>{selected_machine}</strong> has a predicted failure probability of
<strong>{probability:.2%}</strong>, categorized as <strong>{risk_level}</strong> risk.
Estimated downtime exposure is <strong>SGD {estimated_loss:,.0f}</strong>.
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### Factory Maintenance KPIs")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Machine Status", "High Risk" if prediction == 1 else "Normal")
    k2.metric("Failure Probability", f"{probability:.2%}")
    k3.metric("Risk Level", risk_level)
    k4.metric("Estimated Downtime Cost", f"SGD {estimated_loss:,.0f}")

    st.markdown("### Selected Machine Details")
    c1, c2 = st.columns(2)

    with c1:
        st.write(f"**Machine ID:** {selected_machine}")
        if line_col:
            st.write(f"**Production Line:** {selected_row[line_col]}")
        if shift_col:
            st.write(f"**Shift:** {selected_row[shift_col]}")
        if hours_col:
            st.write(f"**Operating Hours / Day:** {selected_row[hours_col]}")

    with c2:
        st.write(f"**Recommended Action:** {recommended_action}")
        st.write(f"**Estimated Downtime Cost:** SGD {estimated_loss:,.0f}")
        st.write(f"**Prediction Class:** {int(prediction)}")

    st.markdown("### Input Parameters")
    chart_data = pd.DataFrame(
        {
            "Parameter": ["Temperature", "Pressure", "Vibration", "Humidity"],
            "Value": [temperature, pressure, vibration, humidity]
        }
    )
    st.bar_chart(chart_data.set_index("Parameter"))

    # Portfolio-wide risk simulation for filtered set
    sim_df = filtered_df.copy()
    sim_input = pd.DataFrame({
        "temperature": sim_df[temp_col].astype(float),
        "pressure": sim_df[pressure_col].astype(float),
        "vibration": sim_df[vib_col].astype(float),
        "humidity": 40.0
    })

    sim_probs = model.predict_proba(sim_input)[:, 1]
    sim_df["failure_probability"] = sim_probs
    sim_df["estimated_risk_cost"] = sim_df["failure_probability"] * 10000
    sim_df["risk_level"] = sim_df["failure_probability"].apply(
        lambda x: "High" if x > 0.7 else ("Medium" if x > 0.4 else "Low")
    )

    st.markdown("### Risk Distribution Overview")
    r1, r2, r3 = st.columns(3)
    r1.metric("High Risk Machines", int((sim_df["risk_level"] == "High").sum()))
    r2.metric("Medium Risk Machines", int((sim_df["risk_level"] == "Medium").sum()))
    r3.metric("Low Risk Machines", int((sim_df["risk_level"] == "Low").sum()))

    st.markdown("### Top 5 Highest-Risk Machines")
    top_risk_cols = [machine_id_col, "failure_probability", "risk_level", "estimated_risk_cost"]
    if line_col:
        top_risk_cols.insert(1, line_col)
    if shift_col:
        top_risk_cols.insert(2 if line_col else 1, shift_col)

    top_risk_df = sim_df[top_risk_cols].sort_values("failure_probability", ascending=False).head(5).copy()
    top_risk_df["failure_probability"] = top_risk_df["failure_probability"].map(lambda x: f"{x:.2%}")
    top_risk_df["estimated_risk_cost"] = top_risk_df["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")
    st.dataframe(top_risk_df, use_container_width=True)

    st.markdown("### Filtered Machine Risk Snapshot")
    snapshot_cols = [machine_id_col]
    if line_col:
        snapshot_cols.append(line_col)
    if shift_col:
        snapshot_cols.append(shift_col)
    if hours_col:
        snapshot_cols.append(hours_col)
    snapshot_cols += ["failure_probability", "risk_level", "estimated_risk_cost"]

    snapshot_df = sim_df[snapshot_cols].copy()
    snapshot_df["failure_probability"] = snapshot_df["failure_probability"].map(lambda x: f"{x:.2%}")
    snapshot_df["estimated_risk_cost"] = snapshot_df["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")
    st.dataframe(snapshot_df, use_container_width=True)

    csv_export_df = sim_df.copy()
    csv_bytes = csv_export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Risk Data (CSV)",
        data=csv_bytes,
        file_name="filtered_machine_risk_snapshot.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# Defect Detection
# --------------------------------------------------
elif module == "Defect Detection":
    st.subheader("Defect Detection")

    st.markdown(
        """
This module is intended to showcase vision-based inspection:

- defect classification  
- image-based quality control  
- early identification of faulty products  
"""
    )

    possible_pngs = list(DD_DIR.glob("*.png")) + list((DD_DIR / "assets").glob("*.png"))
    possible_csvs = list(DD_DIR.glob("*.csv"))

    defect_df = None
    if possible_csvs:
        try:
            defect_df = pd.read_csv(possible_csvs[0])
            defect_df.columns = [c.strip().lower() for c in defect_df.columns]
        except Exception:
            defect_df = None

    defect_records = len(defect_df) if defect_df is not None else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Inspection Module", "Active")
    c2.metric("Defect Records", defect_records)
    c3.metric("Primary Value", "Reduce Scrap")

    left, right = st.columns([1.2, 1])

    with left:
        if possible_pngs:
            st.subheader("Sample Output / Visuals")
            st.image(str(possible_pngs[0]), use_container_width=True)
        else:
            st.info("Place one sample defect image or output screenshot inside 02-Defect-Detection to display here.")

    with right:
        if defect_df is not None:
            st.subheader("Sample Defect Data")
            st.dataframe(defect_df.head(), use_container_width=True)
        else:
            st.info("Place a CSV result file inside 02-Defect-Detection to show sample outputs.")

    if defect_df is not None and "defect_type" in defect_df.columns:
        st.markdown("### Defect Type Distribution")
        defect_type_counts = defect_df["defect_type"].astype(str).value_counts()
        st.bar_chart(defect_type_counts)

    st.markdown("### Quality Insight")
    if defect_df is not None and "defect_type" in defect_df.columns:
        top_defect = defect_df["defect_type"].astype(str).value_counts().idxmax()
        st.info(
            f"The current defect dataset suggests that **{top_defect}** is the most frequently observed issue and should be prioritized for root cause review."
        )
    elif defect_records > 0:
        st.info(
            "Defect records are available for review. The next step is to standardize defect labels to enable trend-based quality analysis."
        )
    else:
        st.info(
            "No structured defect dataset was detected. Add a defect CSV and one visual sample to complete this module."
        )

    st.markdown("### Business Value")
    st.markdown(
        """
- Reduce manual inspection effort  
- Detect defects earlier  
- Improve yield and product quality  
- Lower scrap and rework cost  
"""
    )

# --------------------------------------------------
# Demand Forecasting
# --------------------------------------------------
elif module == "Demand Forecasting":
    st.subheader("Demand Forecasting")

    st.markdown(
        """
This module is intended to showcase demand planning and forecasting:

- historical demand trend analysis  
- forecast-based planning  
- inventory and production optimization  
"""
    )

    forecast_path = DF_DIR / "demand_forecast_sample.csv"
    if not forecast_path.exists():
        st.info("Place a demand forecasting CSV inside 03-Demand-Forecasting to display data and charts.")
        st.stop()

    forecast_df = pd.read_csv(forecast_path)
    forecast_df.columns = [c.strip().lower() for c in forecast_df.columns]

    required_cols = {"date", "product_id", "actual_demand", "forecast_demand"}
    if not required_cols.issubset(set(forecast_df.columns)):
        st.error("Demand forecast CSV must contain: date, product_id, actual_demand, forecast_demand")
        st.stop()

    c1, c2, c3 = st.columns(3)
    c1.metric("Planning Module", "Active")
    c2.metric("Use Case", "Forecasting")
    c3.metric("Primary Value", "Improve Planning Accuracy")

    st.subheader("Sample Forecast Data")
    st.dataframe(forecast_df.head(), use_container_width=True)

    product_list = sorted(forecast_df["product_id"].dropna().astype(str).unique().tolist())
    selected_product = st.selectbox("Select Product", product_list)

    product_df = forecast_df[forecast_df["product_id"].astype(str) == selected_product].copy()
    product_df["date"] = pd.to_datetime(product_df["date"])
    product_df = product_df.sort_values("date")

    st.subheader("Demand vs Forecast Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(product_df["date"], product_df["actual_demand"], label="Actual Demand")
    ax.plot(product_df["date"], product_df["forecast_demand"], linestyle="--", label="Forecast")
    ax.set_title(f"Demand Forecast - {selected_product}")
    ax.legend()
    st.pyplot(fig)

    product_df["error"] = (product_df["actual_demand"] - product_df["forecast_demand"]).abs()
    accuracy = 1 - (product_df["error"].mean() / product_df["actual_demand"].mean())
    bias = (product_df["forecast_demand"] - product_df["actual_demand"]).mean()
    avg_actual = product_df["actual_demand"].mean()
    avg_forecast = product_df["forecast_demand"].mean()
    demand_volatility = product_df["actual_demand"].std()

    if accuracy > 0.9:
        accuracy_level = "high"
    elif accuracy > 0.8:
        accuracy_level = "moderate"
    else:
        accuracy_level = "low"

    if bias > 1:
        bias_type = "over-forecasting"
    elif bias < -1:
        bias_type = "under-forecasting"
    else:
        bias_type = "balanced forecasting"

    if demand_volatility > 20:
        volatility_level = "High"
    elif demand_volatility > 10:
        volatility_level = "Medium"
    else:
        volatility_level = "Low"

    st.markdown("### Product KPI Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Forecast Accuracy", f"{accuracy:.2%}")
    k2.metric("Average Actual Demand", f"{avg_actual:.1f}")
    k3.metric("Average Forecast Demand", f"{avg_forecast:.1f}")
    k4.metric("Forecast Bias", bias_type)

    if accuracy < 0.8:
        st.error("Alert: Forecast accuracy is below acceptable threshold. Immediate model review recommended.")
    elif bias > 10:
        st.warning("Warning: Significant over-forecasting detected.")

    st.markdown("### AI-Generated Business Insights")
    trend = "increasing" if product_df["actual_demand"].iloc[-1] > product_df["actual_demand"].iloc[0] else "stable / declining"
    st.info(
        f"""
- **Demand Trend:** Demand is **{trend}** over the observed period.  
- **Forecast Performance:** The model shows **{accuracy_level} accuracy** ({accuracy:.2%}).  
- **Forecast Bias:** The system is **{bias_type}**, indicating potential planning risk.  
- **Demand Volatility:** Demand volatility is assessed as **{volatility_level}**, which affects planning confidence.  
"""
    )

    st.markdown("### Product Summary Table")
    summary_rows = []
    for product in product_list:
        tmp = forecast_df[forecast_df["product_id"].astype(str) == product].copy()
        tmp["error"] = (tmp["actual_demand"] - tmp["forecast_demand"]).abs()
        tmp_acc = 1 - (tmp["error"].mean() / tmp["actual_demand"].mean())
        tmp_bias = (tmp["forecast_demand"] - tmp["actual_demand"]).mean()

        if tmp_bias > 1:
            tmp_bias_type = "Over"
        elif tmp_bias < -1:
            tmp_bias_type = "Under"
        else:
            tmp_bias_type = "Balanced"

        summary_rows.append(
            {
                "product_id": product,
                "forecast_accuracy": f"{tmp_acc:.2%}",
                "avg_actual_demand": round(tmp["actual_demand"].mean(), 1),
                "avg_forecast_demand": round(tmp["forecast_demand"].mean(), 1),
                "bias_type": tmp_bias_type
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True)