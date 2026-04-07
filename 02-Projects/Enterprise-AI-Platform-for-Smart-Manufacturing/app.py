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

# --------------------------------------------------
# Branding
# --------------------------------------------------
PLATFORM_TITLE = "Enterprise AI Platform for Smart Manufacturing"
PLATFORM_SUBTITLE = "Executive control tower for reliability, quality, and planning"

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


def classify_risk(probability: float):
    if probability > 0.7:
        return "High", "Immediate maintenance required"
    if probability > 0.4:
        return "Medium", "Schedule inspection"
    return "Low", "Continue normal operation"


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


def executive_banner(title, subtitle):
    st.markdown(
        f"""
<div style="padding:16px 18px; border-radius:10px; background-color:#f6f8fb; border:1px solid #e6eaf0; margin-bottom:14px;">
    <div style="font-size:28px; font-weight:700; margin-bottom:4px;">{title}</div>
    <div style="font-size:15px; color:#4b5563;">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True
    )


def section_header(title):
    st.markdown(f"### {title}")


def info_box(text):
    st.markdown(
        f"""
<div style="padding:12px 14px; border-radius:8px; background-color:#eef6ff; border-left:5px solid #3b82f6; margin-bottom:12px;">
{text}
</div>
""",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title(PLATFORM_TITLE)
st.caption(PLATFORM_SUBTITLE)

# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------
st.sidebar.title("Navigation")
module = st.sidebar.radio(
    "Select View",
    [
        "Executive Overview",
        "Predictive Maintenance",
        "Defect Detection",
        "Demand Forecasting"
    ]
)

# --------------------------------------------------
# Executive Overview
# --------------------------------------------------
if module == "Executive Overview":
    executive_banner(
        "Executive Overview",
        "Integrated AI visibility across maintenance, quality, and demand planning"
    )

    high_risk_machines, total_risk_exposure, defect_records, forecast_accuracy_display = get_platform_kpis()
    health = module_health_status()

    info_box(
        f"""
<strong>Board Summary:</strong> The platform consolidates three AI use cases into one decision layer.
Current indicators show <strong>{high_risk_machines}</strong> high-risk machine(s), 
<strong>SGD {total_risk_exposure:,.0f}</strong> estimated maintenance exposure,
<strong>{defect_records}</strong> defect record(s), and
forecast accuracy of <strong>{forecast_accuracy_display}</strong>.
"""
    )

    section_header("Platform KPI Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("High-Risk Machines", high_risk_machines)
    k2.metric("Risk Exposure", f"SGD {total_risk_exposure:,.0f}")
    k3.metric("Defect Records", defect_records)
    k4.metric("Forecast Accuracy", forecast_accuracy_display)

    section_header("Module Health")
    h1, h2, h3 = st.columns(3)
    h1.metric("Predictive Maintenance", "Active" if health["pm"] else "Needs Data")
    h2.metric("Defect Detection", "Active" if health["dd"] else "Needs Data")
    h3.metric("Demand Forecasting", "Active" if health["df"] else "Needs Data")

    section_header("Strategic Scope")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
**Operational Priorities**
- Improve asset reliability
- Reduce quality defects
- Strengthen planning accuracy
- Increase enterprise visibility

**Transformation Shift**
- Reactive maintenance → predictive maintenance
- Manual inspection → AI-assisted quality control
- Historical planning → forecast-led planning
"""
        )

    with c2:
        st.markdown(
            """
**Leadership Objectives**
- Translate model output into actions
- Provide KPI-driven decision support
- Improve cross-functional coordination
- Demonstrate measurable business value from AI
"""
        )

    section_header("Business Value")
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
- Detect issues earlier
- Reduce scrap and rework
- Improve product consistency
"""
        )

    with b3:
        st.markdown(
            """
**Planning**
- Improve forecast confidence
- Support production scheduling
- Reduce planning inefficiencies
"""
        )

    section_header("AI Use Case Portfolio")
    u1, u2, u3 = st.columns(3)

    with u1:
        st.markdown(
            """
#### Predictive Maintenance
**Purpose:** anticipate machine failure risk

**Outputs**
- failure probability
- risk classification
- downtime impact

**Outcome**
- better maintenance prioritization
"""
        )

    with u2:
        st.markdown(
            """
#### Defect Detection
**Purpose:** improve inspection visibility

**Outputs**
- defect image review
- defect data analysis
- quality insight

**Outcome**
- better defect control
"""
        )

    with u3:
        st.markdown(
            """
#### Demand Forecasting
**Purpose:** improve planning quality

**Outputs**
- actual vs forecast trend
- forecast accuracy
- bias detection

**Outcome**
- better planning confidence
"""
        )

    section_header("Architecture Overview")
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

    section_header("Recommended Next Actions")
    action_items = []
    if high_risk_machines > 0:
        action_items.append(f"- Prioritize inspection and intervention for **{high_risk_machines} high-risk machine(s)**")
    if defect_records > 0:
        action_items.append(f"- Review **{defect_records} quality record(s)** for repeatable defect patterns")
    if forecast_accuracy_display != "N/A":
        action_items.append(f"- Validate planning assumptions against current forecast accuracy of **{forecast_accuracy_display}**")
    if not action_items:
        action_items.append("- Load module data sources to activate platform-level executive support")

    st.markdown("\n".join(action_items))

    section_header("CIO Perspective")
    st.warning(
        """
This is not a model demo. It is an enterprise decision layer that links AI outputs to operating priorities,
business KPIs, and management action.
"""
    )

# --------------------------------------------------
# Predictive Maintenance
# --------------------------------------------------
elif module == "Predictive Maintenance":
    executive_banner(
        "Predictive Maintenance",
        "Executive view of machine risk, downtime exposure, and maintenance action"
    )

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
    st.sidebar.subheader("Predictive Maintenance Filters")

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

    st.sidebar.markdown("### Simulation Inputs")
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

    info_box(
        f"""
<strong>Executive Summary:</strong> Machine <strong>{selected_machine}</strong> has a predicted failure probability of
<strong>{probability:.2%}</strong>, classified as <strong>{risk_level}</strong> risk, with estimated downtime exposure of
<strong>SGD {estimated_loss:,.0f}</strong>.
"""
    )

    section_header("Maintenance KPI Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Machine Status", "High Risk" if prediction == 1 else "Normal")
    k2.metric("Failure Probability", f"{probability:.2%}")
    k3.metric("Risk Level", risk_level)
    k4.metric("Downtime Exposure", f"SGD {estimated_loss:,.0f}")

    section_header("Selected Machine Details")
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

    section_header("Input Parameter Profile")
    chart_data = pd.DataFrame(
        {
            "Parameter": ["Temperature", "Pressure", "Vibration", "Humidity"],
            "Value": [temperature, pressure, vibration, humidity]
        }
    )
    st.bar_chart(chart_data.set_index("Parameter"))

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

    section_header("Portfolio Risk Distribution")
    r1, r2, r3 = st.columns(3)
    r1.metric("High Risk Machines", int((sim_df["risk_level"] == "High").sum()))
    r2.metric("Medium Risk Machines", int((sim_df["risk_level"] == "Medium").sum()))
    r3.metric("Low Risk Machines", int((sim_df["risk_level"] == "Low").sum()))

    section_header("Top 5 Highest-Risk Machines")
    top_risk_cols = [machine_id_col]
    if line_col:
        top_risk_cols.append(line_col)
    if shift_col:
        top_risk_cols.append(shift_col)
    top_risk_cols += ["failure_probability", "risk_level", "estimated_risk_cost"]

    top_risk_df = sim_df[top_risk_cols].sort_values("failure_probability", ascending=False).head(5).copy()
    top_risk_df["failure_probability"] = top_risk_df["failure_probability"].map(lambda x: f"{x:.2%}")
    top_risk_df["estimated_risk_cost"] = top_risk_df["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")
    st.dataframe(top_risk_df, use_container_width=True)

    section_header("Filtered Machine Risk Snapshot")
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
    executive_banner(
        "Defect Detection",
        "Executive quality view across inspection visuals, defect records, and quality insight"
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

    info_box(
        f"""
<strong>Executive Summary:</strong> The quality module is currently supporting inspection review with
<strong>{defect_records}</strong> available defect-related record(s).
"""
    )

    section_header("Quality KPI Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Inspection Module", "Active")
    c2.metric("Defect Records", defect_records)
    c3.metric("Primary Value", "Reduce Scrap")

    left, right = st.columns([1.2, 1])

    with left:
        if possible_pngs:
            st.markdown("### Sample Inspection Visual")
            st.image(str(possible_pngs[0]), use_container_width=True)
        else:
            st.info("Place one sample defect image or output screenshot inside 02-Defect-Detection to display here.")

    with right:
        if defect_df is not None:
            st.markdown("### Defect Data Snapshot")
            st.dataframe(defect_df.head(), use_container_width=True)
        else:
            st.info("Place a CSV result file inside 02-Defect-Detection to show sample outputs.")

    if defect_df is not None and "defect_type" in defect_df.columns:
        section_header("Defect Type Distribution")
        defect_type_counts = defect_df["defect_type"].astype(str).value_counts()
        st.bar_chart(defect_type_counts)

    section_header("Executive Quality Insight")
    if defect_df is not None and "defect_type" in defect_df.columns:
        top_defect = defect_df["defect_type"].astype(str).value_counts().idxmax()
        st.info(
            f"The current defect dataset indicates that **{top_defect}** is the most frequently observed issue and should be prioritized for root cause analysis."
        )
    elif defect_records > 0:
        st.info(
            "Defect records are available for review. Standardized defect categories would improve trend visibility and executive reporting."
        )
    else:
        st.info(
            "No structured defect dataset was detected. Add one image and one CSV to complete the quality module."
        )

    section_header("Business Value")
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
    executive_banner(
        "Demand Forecasting",
        "Executive planning view across forecast accuracy, bias, and product demand trends"
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

    section_header("Planning Module Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Planning Module", "Active")
    c2.metric("Use Case", "Forecasting")
    c3.metric("Primary Value", "Improve Planning Accuracy")

    st.markdown("### Demand Data Snapshot")
    st.dataframe(forecast_df.head(), use_container_width=True)

    product_list = sorted(forecast_df["product_id"].dropna().astype(str).unique().tolist())
    selected_product = st.selectbox("Select Product", product_list)

    product_df = forecast_df[forecast_df["product_id"].astype(str) == selected_product].copy()
    product_df["date"] = pd.to_datetime(product_df["date"])
    product_df = product_df.sort_values("date")

    info_box(
        f"""
<strong>Executive Summary:</strong> Product <strong>{selected_product}</strong> is being assessed for planning quality through
actual demand vs forecast comparison, forecast accuracy, and bias analysis.
"""
    )

    section_header("Demand vs Forecast Trend")
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
        accuracy_level = "High"
    elif accuracy > 0.8:
        accuracy_level = "Moderate"
    else:
        accuracy_level = "Low"

    if bias > 1:
        bias_type = "Over-Forecasting"
    elif bias < -1:
        bias_type = "Under-Forecasting"
    else:
        bias_type = "Balanced"

    if demand_volatility > 20:
        volatility_level = "High"
    elif demand_volatility > 10:
        volatility_level = "Medium"
    else:
        volatility_level = "Low"

    section_header("Product KPI Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Forecast Accuracy", f"{accuracy:.2%}")
    k2.metric("Average Actual Demand", f"{avg_actual:.1f}")
    k3.metric("Average Forecast", f"{avg_forecast:.1f}")
    k4.metric("Forecast Bias", bias_type)

    if accuracy < 0.8:
        st.error("Forecast accuracy is below acceptable threshold. Model review is recommended.")
    elif bias > 10:
        st.warning("Significant over-forecasting detected.")

    section_header("AI-Generated Planning Insight")
    trend = "increasing" if product_df["actual_demand"].iloc[-1] > product_df["actual_demand"].iloc[0] else "stable / declining"
    st.info(
        f"""
- **Demand Trend:** Demand is **{trend}** over the observed period.  
- **Forecast Performance:** The model shows **{accuracy_level.lower()} accuracy** ({accuracy:.2%}).  
- **Forecast Bias:** The system is **{bias_type.lower()}**, indicating potential planning risk.  
- **Demand Volatility:** Volatility is assessed as **{volatility_level.lower()}**, which influences confidence in planning.  
"""
    )

    section_header("Product Summary Table")
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