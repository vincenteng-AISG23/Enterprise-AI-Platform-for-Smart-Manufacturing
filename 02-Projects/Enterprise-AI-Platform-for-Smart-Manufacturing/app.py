import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

# Optional plotting
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Enterprise AI Platform for Smart Manufacturing",
    page_icon="🏭",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}
.exec-banner {
    background: #f3f4f6;
    padding: 0.8rem 1rem;
    border-radius: 0.6rem;
    border-left: 6px solid #111827;
    margin-bottom: 1rem;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 0.8rem;
    padding: 1rem 1rem 0.8rem 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.kpi-label {
    font-size: 0.82rem;
    color: #6b7280;
    margin-bottom: 0.2rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.2;
}
.kpi-sub {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 0.3rem;
}
.small-note {
    color: #6b7280;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Helpers
# -----------------------------
ROOT = Path.cwd()


def find_first_file(patterns):
    for pattern in patterns:
        matches = list(ROOT.rglob(pattern))
        if matches:
            return matches[0]
    return None


def safe_read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def first_existing_column(df: pd.DataFrame, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in cols_lower:
            return cols_lower[c.lower()]
    return None


def standardize_pm_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    mapping = {
        "machine_id": ["machine_id", "machine", "id", "asset_id"],
        "production_line": ["production_line", "line", "prod_line"],
        "shift": ["shift"],
        "operating_hours_per_day": ["operating_hours_per_day", "operating_hours", "hours_per_day", "run_hours"],
        "temperature_c": ["temperature_c", "temperature", "temp_c", "temp"],
        "vibration_mm_s": ["vibration_mm_s", "vibration", "vibration_mms"],
        "pressure_psi": ["pressure_psi", "pressure", "pressure_bar"],
        "current_a": ["current_a", "current", "ampere", "amps"],
        "failure": ["failure", "failure_flag", "breakdown", "target"],
        "plant": ["plant", "site"],
    }

    renamed = {}
    for std_name, candidates in mapping.items():
        col = first_existing_column(out, candidates)
        if col:
            renamed[col] = std_name

    out = out.rename(columns=renamed)

    if "machine_id" not in out.columns:
        out["machine_id"] = [f"M-{i:03d}" for i in range(1, len(out) + 1)]

    if "production_line" not in out.columns:
        out["production_line"] = np.random.choice(["Line A", "Line B", "Line C"], len(out))

    if "shift" not in out.columns:
        out["shift"] = np.random.choice(["Day", "Night", "Swing"], len(out))

    if "operating_hours_per_day" not in out.columns:
        out["operating_hours_per_day"] = np.random.uniform(8, 22, len(out)).round(1)

    if "temperature_c" not in out.columns:
        out["temperature_c"] = np.random.uniform(55, 95, len(out)).round(1)

    if "vibration_mm_s" not in out.columns:
        out["vibration_mm_s"] = np.random.uniform(1.0, 12.0, len(out)).round(1)

    if "pressure_psi" not in out.columns:
        out["pressure_psi"] = np.random.uniform(70, 130, len(out)).round(1)

    if "current_a" not in out.columns:
        out["current_a"] = np.random.uniform(15, 60, len(out)).round(1)

    if "failure" not in out.columns:
        risk_score = (
            (out["temperature_c"] - out["temperature_c"].min()) / max(1e-9, (out["temperature_c"].max() - out["temperature_c"].min())) * 0.30
            + (out["vibration_mm_s"] - out["vibration_mm_s"].min()) / max(1e-9, (out["vibration_mm_s"].max() - out["vibration_mm_s"].min())) * 0.35
            + (out["pressure_psi"] - out["pressure_psi"].min()) / max(1e-9, (out["pressure_psi"].max() - out["pressure_psi"].min())) * 0.15
            + (out["current_a"] - out["current_a"].min()) / max(1e-9, (out["current_a"].max() - out["current_a"].min())) * 0.10
            + (out["operating_hours_per_day"] - out["operating_hours_per_day"].min()) / max(1e-9, (out["operating_hours_per_day"].max() - out["operating_hours_per_day"].min())) * 0.10
        )
        out["failure"] = (risk_score > 0.58).astype(int)

    if "plant" not in out.columns:
        out["plant"] = np.random.choice(["Plant SG", "Plant MY", "Plant TH"], len(out))

    return out


def standardize_demand_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    mapping = {
        "date": ["date", "month", "period"],
        "product_id": ["product_id", "product", "sku"],
        "actual_demand": ["actual_demand", "actual", "demand", "sales"],
        "forecast_demand": ["forecast_demand", "forecast", "predicted_demand", "prediction"],
    }

    renamed = {}
    for std_name, candidates in mapping.items():
        col = first_existing_column(out, candidates)
        if col:
            renamed[col] = std_name

    out = out.rename(columns=renamed)

    if "date" not in out.columns:
        out["date"] = pd.date_range("2025-01-01", periods=len(out), freq="M")

    if "product_id" not in out.columns:
        out["product_id"] = np.random.choice(["P-100", "P-200", "P-300"], len(out))

    if "actual_demand" not in out.columns:
        out["actual_demand"] = np.random.randint(80, 180, len(out))

    if "forecast_demand" not in out.columns:
        noise = np.random.randint(-15, 16, len(out))
        out["forecast_demand"] = out["actual_demand"] + noise

    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["forecast_error"] = out["forecast_demand"] - out["actual_demand"]
    out["abs_error"] = out["forecast_error"].abs()
    out["accuracy_pct"] = 100 - ((out["abs_error"] / out["actual_demand"].replace(0, np.nan)) * 100)
    out["accuracy_pct"] = out["accuracy_pct"].fillna(0).clip(lower=0, upper=100)

    return out


def build_defect_df(n=120):
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    lines = np.random.choice(["Line A", "Line B", "Line C"], n)
    units_checked = np.random.randint(800, 1400, n)
    defect_rate = np.random.uniform(0.8, 3.8, n)
    defects_found = (units_checked * defect_rate / 100).astype(int)

    return pd.DataFrame({
        "date": dates,
        "production_line": lines,
        "units_checked": units_checked,
        "defects_found": defects_found,
        "defect_rate_pct": defect_rate.round(2),
    })


def risk_band(prob):
    if prob >= 0.70:
        return "High"
    if prob >= 0.45:
        return "Medium"
    return "Low"


def traffic_status(value, good_threshold, watch_threshold, reverse=False):
    if reverse:
        if value <= good_threshold:
            return "Good"
        if value <= watch_threshold:
            return "Watch"
        return "Risk"
    else:
        if value >= good_threshold:
            return "Good"
        if value >= watch_threshold:
            return "Watch"
        return "Risk"


def status_badge_text(status):
    if status == "Good":
        return "🟢 Good"
    if status == "Watch":
        return "🟠 Watch"
    return "🔴 Risk"


def calc_pm_probability(row):
    temp_score = min(max((row["temperature_c"] - 55) / 40, 0), 1)
    vib_score = min(max((row["vibration_mm_s"] - 1) / 11, 0), 1)
    press_score = min(max((row["pressure_psi"] - 70) / 60, 0), 1)
    current_score = min(max((row["current_a"] - 15) / 45, 0), 1)
    hours_score = min(max((row["operating_hours_per_day"] - 8) / 14, 0), 1)

    prob = (
        0.30 * temp_score
        + 0.35 * vib_score
        + 0.12 * press_score
        + 0.10 * current_score
        + 0.13 * hours_score
    )
    return round(float(min(max(prob, 0), 1)), 4)


def metric_card(label, value, subtext=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Load data
# -----------------------------
pm_path = find_first_file([
    "sample_machine_data.csv",
    "sample_predictive_maintenance_data.csv",
    "*machine*.csv",
    "*predictive*maintenance*.csv",
])

demand_path = find_first_file([
    "demand_forecast_sample.csv",
    "sample_demand_data.csv",
    "*demand*.csv",
    "*forecast*.csv",
])

defect_image = find_first_file([
    "defect_sample.png",
    "*.png",
    "*.jpg",
    "*.jpeg",
])

pm_df = standardize_pm_df(safe_read_csv(pm_path) if pm_path else pd.DataFrame())
demand_df = standardize_demand_df(safe_read_csv(demand_path) if demand_path else pd.DataFrame())
defect_df = build_defect_df()

if pm_df.empty:
    st.error("No predictive maintenance data found.")
    st.stop()

# -----------------------------
# Core calculations
# -----------------------------
pm_df["failure_probability"] = pm_df.apply(calc_pm_probability, axis=1)
pm_df["risk_level"] = pm_df["failure_probability"].apply(risk_band)
pm_df["estimated_downtime_cost"] = (pm_df["failure_probability"] * 10000).round(0)

overall_pm_risk = pm_df["failure_probability"].mean() * 100
high_risk_assets = int((pm_df["risk_level"] == "High").sum())
avg_downtime_cost = pm_df["estimated_downtime_cost"].mean()

overall_defect_rate = defect_df["defect_rate_pct"].mean()
quality_yield = 100 - overall_defect_rate

forecast_accuracy = demand_df["accuracy_pct"].mean() if not demand_df.empty else 0
inventory_impact_pct = max(0, round((forecast_accuracy - 70) * 0.45, 1))

platform_health_score = round(
    (
        (100 - overall_pm_risk) * 0.40
        + quality_yield * 0.30
        + forecast_accuracy * 0.30
    ),
    1
)

overall_status = traffic_status(platform_health_score, good_threshold=85, watch_threshold=70, reverse=False)
pm_status = traffic_status(100 - overall_pm_risk, good_threshold=75, watch_threshold=55, reverse=False)
defect_status = traffic_status(overall_defect_rate, good_threshold=1.5, watch_threshold=2.8, reverse=True)
forecast_status = traffic_status(forecast_accuracy, good_threshold=88, watch_threshold=78, reverse=False)

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Platform Navigation")
module = st.sidebar.radio(
    "Select Module",
    [
        "Executive Overview",
        "Predictive Maintenance",
        "Defect Detection",
        "Demand Forecasting",
    ]
)

# -----------------------------
# Sidebar filters - module specific
# -----------------------------
st.sidebar.markdown("---")

selected_line = "All"
selected_shift = "All"
selected_machine = None
selected_defect_line = "All"
selected_product = "All"

filtered_pm = pm_df.copy()
selected_row = pm_df.iloc[0]

# Predictive Maintenance sidebar only
if module == "Predictive Maintenance":
    st.sidebar.markdown("### Predictive Maintenance Filters")

    line_options = ["All"] + sorted(pm_df["production_line"].astype(str).unique().tolist())
    shift_options = ["All"] + sorted(pm_df["shift"].astype(str).unique().tolist())

    selected_line = st.sidebar.selectbox("Production Line", line_options)
    selected_shift = st.sidebar.selectbox("Shift", shift_options)

    if selected_line != "All":
        filtered_pm = filtered_pm[filtered_pm["production_line"] == selected_line]
    if selected_shift != "All":
        filtered_pm = filtered_pm[filtered_pm["shift"] == selected_shift]

    if filtered_pm.empty:
        filtered_pm = pm_df.copy()

    selected_machine = st.sidebar.selectbox(
        "Select Machine",
        filtered_pm["machine_id"].astype(str).unique().tolist()
    )
    selected_row = filtered_pm[filtered_pm["machine_id"] == selected_machine].iloc[0]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Simulation")

    sim_temp = st.sidebar.slider("Temperature (°C)", 40.0, 110.0, float(selected_row["temperature_c"]), 0.1)
    sim_vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 15.0, float(selected_row["vibration_mm_s"]), 0.1)
    sim_pressure = st.sidebar.slider("Pressure (psi)", 50.0, 150.0, float(selected_row["pressure_psi"]), 0.1)
    sim_current = st.sidebar.slider("Current (A)", 5.0, 80.0, float(selected_row["current_a"]), 0.1)
    sim_hours = st.sidebar.slider("Operating Hours / Day", 1.0, 24.0, float(selected_row["operating_hours_per_day"]), 0.1)
else:
    sim_temp = float(selected_row["temperature_c"])
    sim_vibration = float(selected_row["vibration_mm_s"])
    sim_pressure = float(selected_row["pressure_psi"])
    sim_current = float(selected_row["current_a"])
    sim_hours = float(selected_row["operating_hours_per_day"])

# Defect Detection sidebar only
if module == "Defect Detection":
    st.sidebar.markdown("### Defect Detection Filters")
    defect_line_options = ["All"] + sorted(defect_df["production_line"].astype(str).unique().tolist())
    selected_defect_line = st.sidebar.selectbox("Inspection Line", defect_line_options)

# Demand Forecasting sidebar only
if module == "Demand Forecasting":
    st.sidebar.markdown("### Demand Forecasting Filters")
    if not demand_df.empty:
        product_options = ["All"] + sorted(demand_df["product_id"].astype(str).unique().tolist())
        selected_product = st.sidebar.selectbox("Product", product_options)

# Executive Overview sidebar
if module == "Executive Overview":
    st.sidebar.info("Executive Overview shows platform-level KPIs across all modules.")

# -----------------------------
# Filtered datasets
# -----------------------------
filtered_defect_df = defect_df.copy()
if selected_defect_line != "All":
    filtered_defect_df = filtered_defect_df[filtered_defect_df["production_line"] == selected_defect_line]

filtered_demand_df = demand_df.copy()
if selected_product != "All" and not demand_df.empty:
    filtered_demand_df = filtered_demand_df[filtered_demand_df["product_id"] == selected_product]

# -----------------------------
# PM simulation metrics
# -----------------------------
sim_probability = calc_pm_probability(pd.Series({
    "temperature_c": sim_temp,
    "vibration_mm_s": sim_vibration,
    "pressure_psi": sim_pressure,
    "current_a": sim_current,
    "operating_hours_per_day": sim_hours
}))
sim_risk = risk_band(sim_probability)
sim_cost = round(sim_probability * 10000, 0)

# -----------------------------
# Header
# -----------------------------
st.title("Enterprise AI Platform for Smart Manufacturing")
st.caption("CIO-led digital and AI transformation platform for reliability, quality, and planning")

st.markdown(
    f"""
    <div class="exec-banner">
        <strong>Executive Summary:</strong>
        Platform Health Score is <strong>{platform_health_score}</strong>/100.
        Predictive Maintenance is <strong>{status_badge_text(pm_status)}</strong>,
        Quality AI is <strong>{status_badge_text(defect_status)}</strong>,
        and Demand Forecasting is <strong>{status_badge_text(forecast_status)}</strong>.
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Executive Overview
# -----------------------------
if module == "Executive Overview":
    st.markdown('<div class="section-title">Platform KPI Row</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Platform Health Score", f"{platform_health_score}", status_badge_text(overall_status))
    with c2:
        metric_card("Avg Failure Risk", f"{overall_pm_risk:.1f}%", f"{high_risk_assets} high-risk assets")
    with c3:
        metric_card("Quality Yield", f"{quality_yield:.1f}%", f"Avg defect rate {overall_defect_rate:.2f}%")
    with c4:
        metric_card("Forecast Accuracy", f"{forecast_accuracy:.1f}%", f"Estimated inventory gain {inventory_impact_pct:.1f}%")

    st.markdown('<div class="section-title">Module Health Row</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Predictive Maintenance", status_badge_text(pm_status), f"Risk score {(100 - overall_pm_risk):.1f}/100")
    with m2:
        metric_card("Defect Detection", status_badge_text(defect_status), f"Defect rate {overall_defect_rate:.2f}%")
    with m3:
        metric_card("Demand Forecasting", status_badge_text(forecast_status), f"Accuracy {forecast_accuracy:.1f}%")

    st.markdown('<div class="section-title">Business Impact Summary</div>', unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        metric_card("Downtime Cost Exposure", f"SGD {avg_downtime_cost:,.0f}", "Predictive maintenance portfolio")
    with b2:
        metric_card("High-Risk Assets", f"{high_risk_assets}", "Assets requiring intervention")
    with b3:
        metric_card("Quality Loss Proxy", f"{overall_defect_rate:.2f}%", "Average defect leakage")
    with b4:
        metric_card("Planning Uplift", f"{inventory_impact_pct:.1f}%", "Inventory / forecast improvement")

    st.markdown('<div class="section-title">Executive Platform Narrative</div>', unsafe_allow_html=True)
    st.markdown("""
- **Predictive Maintenance** improves asset reliability by highlighting high-risk machines before breakdown.
- **Defect Detection** improves quality performance by reducing defect leakage and manual inspection dependency.
- **Demand Forecasting** improves planning accuracy and supports inventory and production balancing.
- The platform demonstrates how a CIO can connect **operations, quality, and planning** into a single executive control tower.
""")

    st.markdown('<div class="section-title">Module KPI Table</div>', unsafe_allow_html=True)
    summary_table = pd.DataFrame({
        "Module": ["Predictive Maintenance", "Defect Detection", "Demand Forecasting"],
        "Primary KPI": [
            f"Avg Failure Risk = {overall_pm_risk:.1f}%",
            f"Defect Rate = {overall_defect_rate:.2f}%",
            f"Forecast Accuracy = {forecast_accuracy:.1f}%"
        ],
        "Status": [
            status_badge_text(pm_status),
            status_badge_text(defect_status),
            status_badge_text(forecast_status)
        ],
        "Business Meaning": [
            "Asset reliability and downtime prevention",
            "Product quality and defect leakage reduction",
            "Planning, inventory, and service level improvement"
        ]
    })
    st.dataframe(summary_table, use_container_width=True)

    if PLOTLY_AVAILABLE:
        st.markdown('<div class="section-title">Control Tower Scorecard</div>', unsafe_allow_html=True)
        score_df = pd.DataFrame({
            "Area": ["Reliability", "Quality", "Planning"],
            "Score": [round(100 - overall_pm_risk, 1), round(quality_yield, 1), round(forecast_accuracy, 1)]
        })
        fig = px.bar(score_df, x="Area", y="Score", text="Score")
        fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Predictive Maintenance
# -----------------------------
elif module == "Predictive Maintenance":
    st.markdown('<div class="section-title">Predictive Maintenance</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="exec-banner">
            <strong>Executive Summary:</strong>
            Machine <strong>{selected_machine}</strong> has a predicted failure probability of
            <strong>{sim_probability * 100:.2f}%</strong>, categorized as
            <strong>{sim_risk}</strong> risk. Estimated downtime exposure is
            <strong>SGD {sim_cost:,.0f}</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Machine Status", status_badge_text("Risk" if sim_risk == "High" else "Watch" if sim_risk == "Medium" else "Good"), f"{selected_machine}")
    with c2:
        metric_card("Failure Probability", f"{sim_probability * 100:.2f}%", f"Risk band: {sim_risk}")
    with c3:
        metric_card("Production Line", f"{selected_row['production_line']}", f"Shift: {selected_row['shift']}")
    with c4:
        metric_card("Estimated Downtime Cost", f"SGD {sim_cost:,.0f}", "Business exposure")

    d1, d2 = st.columns([1.15, 1])
    with d1:
        st.markdown("#### Selected Machine Details")
        detail_df = pd.DataFrame({
            "Attribute": [
                "Machine ID", "Plant", "Production Line", "Shift",
                "Operating Hours / Day", "Temperature (°C)", "Vibration (mm/s)",
                "Pressure (psi)", "Current (A)"
            ],
            "Value": [
                selected_machine,
                selected_row["plant"],
                selected_row["production_line"],
                selected_row["shift"],
                sim_hours,
                sim_temp,
                sim_vibration,
                sim_pressure,
                sim_current
            ]
        })
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

    with d2:
        st.markdown("#### Recommended Action")
        if sim_risk == "High":
            st.error("Immediate maintenance inspection recommended. High probability of failure.")
        elif sim_risk == "Medium":
            st.warning("Monitor closely and schedule maintenance in next cycle.")
        else:
            st.success("Operating within acceptable range. Continue normal monitoring.")

        st.markdown(
            f"""
- **Prediction Class:** {"1 (Potential Failure)" if sim_probability >= 0.5 else "0 (Normal)"}  
- **Risk Level:** {sim_risk}  
- **Estimated Downtime Cost:** SGD {sim_cost:,.0f}  
- **Business Interpretation:** {"Potential production disruption" if sim_probability >= 0.5 else "Acceptable operating profile"}  
"""
        )

    if PLOTLY_AVAILABLE:
        st.markdown("#### Machine Risk Driver Profile")
        risk_driver_df = pd.DataFrame({
            "Parameter": ["Temperature", "Vibration", "Pressure", "Current", "Operating Hours"],
            "Value": [sim_temp, sim_vibration, sim_pressure, sim_current, sim_hours]
        })
        fig = px.bar(risk_driver_df, x="Parameter", y="Value", text="Value")
        fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Portfolio Risk by Machine")
        pm_rank = filtered_pm.sort_values("failure_probability", ascending=False)[["machine_id", "failure_probability", "production_line"]].head(12)
        fig2 = px.bar(pm_rank, x="machine_id", y="failure_probability", color="production_line", text="failure_probability")
        fig2.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Defect Detection
# -----------------------------
elif module == "Defect Detection":
    current_defect_rate = filtered_defect_df["defect_rate_pct"].mean()
    current_quality_yield = 100 - current_defect_rate
    current_defect_status = traffic_status(current_defect_rate, good_threshold=1.5, watch_threshold=2.8, reverse=True)

    st.markdown('<div class="section-title">Defect Detection</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="exec-banner">
            <strong>Executive Summary:</strong>
            Current average defect rate is <strong>{current_defect_rate:.2f}%</strong>,
            translating to an estimated quality yield of <strong>{current_quality_yield:.2f}%</strong>.
            Overall module status is <strong>{status_badge_text(current_defect_status)}</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Defect Rate", f"{current_defect_rate:.2f}%", "Average across inspected batches")
    with c2:
        metric_card("Quality Yield", f"{current_quality_yield:.2f}%", "Proxy first-pass quality")
    with c3:
        metric_card("Units Checked", f"{int(filtered_defect_df['units_checked'].sum()):,}", "Inspection coverage")
    with c4:
        metric_card("Defects Found", f"{int(filtered_defect_df['defects_found'].sum()):,}", "Detected quality issues")

    if defect_image and defect_image.exists():
        st.markdown("#### Sample Inspection Image")
        st.image(str(defect_image), use_container_width=True)
    else:
        st.info("No defect sample image found. Add a PNG/JPG into the defect detection folder if you want it shown here.")

    if PLOTLY_AVAILABLE:
        st.markdown("#### Defect Trend")
        defect_daily = filtered_defect_df.groupby("date", as_index=False)["defect_rate_pct"].mean()
        fig = px.line(defect_daily, x="date", y="defect_rate_pct")
        fig.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Defect Rate by Production Line")
        line_df = filtered_defect_df.groupby("production_line", as_index=False)["defect_rate_pct"].mean()
        fig2 = px.bar(line_df, x="production_line", y="defect_rate_pct", text="defect_rate_pct")
        fig2.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Quality Management Interpretation")
    st.markdown("""
- **Business Use Case:** Reduce manual inspection effort and defect leakage.
- **Operational Value:** Earlier detection improves yield and reduces rework.
- **Leadership Signal:** Defect trend should be monitored alongside line performance and scrap cost.
""")

# -----------------------------
# Demand Forecasting
# -----------------------------
elif module == "Demand Forecasting":
    current_forecast_accuracy = filtered_demand_df["accuracy_pct"].mean() if not filtered_demand_df.empty else 0
    current_inventory_impact = max(0, round((current_forecast_accuracy - 70) * 0.45, 1))
    current_forecast_status = traffic_status(current_forecast_accuracy, good_threshold=88, watch_threshold=78, reverse=False)

    st.markdown('<div class="section-title">Demand Forecasting</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="exec-banner">
            <strong>Executive Summary:</strong>
            Current forecast accuracy is <strong>{current_forecast_accuracy:.2f}%</strong>,
            with estimated planning and inventory benefit of <strong>{current_inventory_impact:.1f}%</strong>.
            Overall module status is <strong>{status_badge_text(current_forecast_status)}</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Forecast Accuracy", f"{current_forecast_accuracy:.2f}%", "Portfolio accuracy")
    with c2:
        metric_card("Average Actual Demand", f"{filtered_demand_df['actual_demand'].mean():.0f}", "Across demand periods")
    with c3:
        metric_card("Average Forecast", f"{filtered_demand_df['forecast_demand'].mean():.0f}", "Model output average")
    with c4:
        metric_card("Inventory / Planning Gain", f"{current_inventory_impact:.1f}%", "Estimated impact proxy")

    if PLOTLY_AVAILABLE and not filtered_demand_df.empty:
        st.markdown("#### Actual vs Forecast Demand")
        trend_df = filtered_demand_df.groupby("date", as_index=False)[["actual_demand", "forecast_demand"]].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend_df["date"], y=trend_df["actual_demand"], mode="lines+markers", name="Actual Demand"))
        fig.add_trace(go.Scatter(x=trend_df["date"], y=trend_df["forecast_demand"], mode="lines+markers", name="Forecast Demand"))
        fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Product-Level Forecast Accuracy")
        product_summary = filtered_demand_df.groupby("product_id", as_index=False)["accuracy_pct"].mean()
        fig2 = px.bar(product_summary, x="product_id", y="accuracy_pct", text="accuracy_pct")
        fig2.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Forecasting Management Interpretation")
    st.markdown("""
- **Business Use Case:** Improve production planning and inventory alignment.
- **Operational Value:** Better forecast accuracy reduces stock imbalance and schedule volatility.
- **Leadership Signal:** Forecast performance should be reviewed alongside service level and inventory days.
""")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<div class='small-note'>Enterprise AI Platform for Smart Manufacturing | CIO-led portfolio demonstration across reliability, quality, and planning</div>",
    unsafe_allow_html=True
)