from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="AI-Driven Smart Manufacturing Control Tower",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def classify_pm_risk(prob: float) -> str:
    if prob > 0.7:
        return "HIGH"
    if prob > 0.4:
        return "MEDIUM"
    return "LOW"


def find_first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


# --------------------------------------------------
# Load Predictive Maintenance data
# --------------------------------------------------
def load_pm_data():
    pm_dir = BASE_DIR / "01-Predictive-Maintenance"
    pm_model_path = pm_dir / "model.pkl"
    pm_data_path = find_first_existing([
        pm_dir / "sample_predictive_maintenance_data.csv",
        pm_dir / "sample_machine_data.csv",
    ])

    if not pm_model_path.exists():
        return None, None, "`model.pkl` not found in 01-Predictive-Maintenance."

    if pm_data_path is None:
        return None, None, "No predictive maintenance CSV found in 01-Predictive-Maintenance."

    pm_df = pd.read_csv(pm_data_path)

    required_cols = [
        "air_temperature",
        "process_temperature",
        "rotational_speed",
        "torque",
        "tool_wear",
    ]
    missing_cols = [c for c in required_cols if c not in pm_df.columns]
    if missing_cols:
        return None, None, (
            "Predictive maintenance CSV missing columns: " + ", ".join(missing_cols)
        )

    if "machine_id" not in pm_df.columns:
        pm_df["machine_id"] = [f"M{str(i + 1).zfill(3)}" for i in range(len(pm_df))]

    if "plant" not in pm_df.columns:
        plants = ["Plant MY", "Plant SG", "Plant TH"]
        pm_df["plant"] = [plants[i % len(plants)] for i in range(len(pm_df))]

    if "line" not in pm_df.columns:
        pm_df["line"] = [f"L{(i % 3) + 1}" for i in range(len(pm_df))]

    pm_df["temperature_diff"] = pm_df["process_temperature"] - pm_df["air_temperature"]

    pm_model = joblib.load(pm_model_path)

    score_features = pm_df[[
        "air_temperature",
        "process_temperature",
        "rotational_speed",
        "torque",
        "tool_wear",
        "temperature_diff"
    ]].copy()

    pm_df["failure_probability"] = pm_model.predict_proba(score_features)[:, 1]
    pm_df["risk_level"] = pm_df["failure_probability"].apply(classify_pm_risk)
    pm_df["estimated_risk_cost"] = pm_df["risk_level"].map({
        "HIGH": 50000,
        "MEDIUM": 10000,
        "LOW": 2000
    })

    return pm_df, pm_model, None


# --------------------------------------------------
# Load Defect Detection data
# --------------------------------------------------
def load_defect_data():
    dd_dir = BASE_DIR / "02-Defect-Detection"
    possible_csvs = list(dd_dir.glob("*.csv"))
    possible_pngs = list(dd_dir.glob("*.png")) + list(dd_dir.glob("*.jpg")) + list(dd_dir.glob("*.jpeg"))

    df_defect = None
    if possible_csvs:
        df_defect = pd.read_csv(possible_csvs[0])

    defect_image = possible_pngs[0] if possible_pngs else None

    return df_defect, defect_image


# --------------------------------------------------
# Load Demand Forecasting data
# --------------------------------------------------
def load_demand_data():
    dfc_dir = BASE_DIR / "03-Demand-Forecasting"
    possible_csvs = list(dfc_dir.glob("*.csv"))
    if not possible_csvs:
        return None

    forecast_df = pd.read_csv(possible_csvs[0])

    required_cols = ["date", "product_id", "actual_demand", "forecast_demand"]
    missing_cols = [c for c in required_cols if c not in forecast_df.columns]
    if missing_cols:
        return None

    forecast_df["date"] = pd.to_datetime(forecast_df["date"])
    return forecast_df


# --------------------------------------------------
# Preload all data
# --------------------------------------------------
pm_df, pm_model, pm_error = load_pm_data()
df_defect, defect_image = load_defect_data()
forecast_df = load_demand_data()


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("AI-Driven Smart Manufacturing Control Tower")
st.caption("Integrated AI use cases across maintenance, quality, and planning")

st.markdown(
    """
This platform brings together three manufacturing AI capabilities:

- **Predictive Maintenance** for reliability  
- **Defect Detection** for quality  
- **Demand Forecasting** for planning  
"""
)

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
        "Demand Forecasting",
    ]
)

# ==================================================
# 1. Executive Overview
# ==================================================
if module == "Executive Overview":
    st.subheader("Enterprise AI Control Tower")

    total_risk_exposure = 0
    high_risk_count = 0
    top_plant = "N/A"

    if pm_df is not None:
        total_risk_exposure = int(pm_df["estimated_risk_cost"].sum())
        high_risk_count = int((pm_df["risk_level"] == "HIGH").sum())
        plant_risk = pm_df.groupby("plant")["estimated_risk_cost"].sum()
        top_plant = plant_risk.idxmax()

    defect_rate = None
    avg_confidence = None
    if df_defect is not None and "inspection_result" in df_defect.columns:
        defect_rate = (df_defect["inspection_result"].astype(str).str.lower() == "defective").mean()
    if df_defect is not None and "confidence" in df_defect.columns:
        avg_confidence = df_defect["confidence"].mean()

    forecast_accuracy = None
    demand_trend_text = "N/A"
    if forecast_df is not None:
        temp_df = forecast_df.copy()
        temp_df["error"] = (temp_df["actual_demand"] - temp_df["forecast_demand"]).abs()
        forecast_accuracy = 1 - (temp_df["error"].mean() / temp_df["actual_demand"].mean())

        demand_by_date = temp_df.groupby("date")["actual_demand"].sum().reset_index()
        if demand_by_date["actual_demand"].iloc[-1] > demand_by_date["actual_demand"].iloc[0]:
            demand_trend_text = "Increasing"
        else:
            demand_trend_text = "Decreasing"

    st.markdown("### Executive KPI Snapshot")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Risk Exposure (SGD)", f"${total_risk_exposure:,.0f}")
    col2.metric("High Risk Machines", f"{high_risk_count}")
    col3.metric("Defect Rate", f"{defect_rate:.2%}" if defect_rate is not None else "N/A")
    col4.metric("Forecast Accuracy", f"{forecast_accuracy:.2%}" if forecast_accuracy is not None else "N/A")

    st.markdown("### Platform Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Use Cases", "3")
    c2.metric("Domains", "3")
    c3.metric("Platform Type", "Enterprise AI Portfolio")
    st.write("Domains covered: Reliability, Quality, Planning")

    st.markdown("### Strategic Scope")
    st.markdown(
        """
- **Predictive Maintenance** helps reduce downtime and maintenance cost  
- **Defect Detection** improves quality inspection and lowers scrap  
- **Demand Forecasting** improves planning accuracy and inventory control  
"""
    )

    st.markdown("### Business Value")
    st.markdown(
        """
- Reduce unplanned downtime  
- Improve product quality  
- Lower scrap and rework  
- Improve demand planning accuracy  
- Support data-driven manufacturing decisions  
"""
    )

    st.markdown("### Executive Summary")
    if forecast_accuracy is not None and defect_rate is not None:
        st.info(
            f"""
- Operational risk is currently most concentrated in **{top_plant}**.
- The maintenance model has flagged **{high_risk_count} high-risk machines**.
- Quality inspection shows a defect rate of **{defect_rate:.2%}**.
- Demand trend is currently **{demand_trend_text.lower()}** with forecast accuracy at **{forecast_accuracy:.2%}**.
- This unified control tower helps leadership prioritize maintenance, protect product quality, and stabilize planning.
"""
        )
    else:
        st.info(
            """
Some modules are available, but one or more datasets are still incomplete.
The platform structure is ready and will automatically strengthen the executive
summary as more production data is connected.
"""
        )

    st.markdown("### Cross-Module AI Insights")
    insight_lines = []

    if pm_df is not None:
        insight_lines.append(
            f"⚠ Maintenance risk remains elevated with **{high_risk_count} high-risk machines**, creating **SGD {total_risk_exposure:,.0f}** estimated exposure."
        )

    if defect_rate is not None:
        if defect_rate > 0.1:
            insight_lines.append(
                f"⚠ Quality risk is material. Current defect rate is **{defect_rate:.2%}**, suggesting possible upstream process instability."
            )
        else:
            insight_lines.append(
                f"✅ Quality performance is relatively stable with a defect rate of **{defect_rate:.2%}**."
            )

    if forecast_accuracy is not None:
        if forecast_accuracy < 0.85:
            insight_lines.append(
                f"⚠ Planning accuracy needs attention. Forecast accuracy is **{forecast_accuracy:.2%}**, which may create inventory imbalance."
            )
        else:
            insight_lines.append(
                f"✅ Planning performance is healthy. Forecast accuracy is **{forecast_accuracy:.2%}**."
            )

    if high_risk_count > 0 and defect_rate is not None and defect_rate > 0.1:
        insight_lines.append(
            "🔗 Combined signal: Elevated maintenance risk and higher defect rate together may indicate asset-condition impact on product quality."
        )

    if high_risk_count > 0 and forecast_accuracy is not None and forecast_accuracy < 0.85:
        insight_lines.append(
            "🔗 Combined signal: Maintenance instability plus weaker forecasting could amplify production planning risk."
        )

    if not insight_lines:
        insight_lines.append("Connect additional data sources to activate executive intelligence.")

    for line in insight_lines:
        st.markdown(f"- {line}")

    st.markdown("### Executive Visuals")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if pm_df is not None:
            st.markdown("#### Maintenance Risk Distribution")
            risk_counts = pm_df["risk_level"].value_counts().reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
            fig1, ax1 = plt.subplots()
            risk_counts.plot(kind="bar", ax=ax1)
            ax1.set_title("Machine Risk Distribution")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)
        else:
            st.info("Predictive Maintenance data not available.")

    with chart_col2:
        if df_defect is not None and "defect_type" in df_defect.columns:
            st.markdown("#### Defect Type Distribution")
            fig2, ax2 = plt.subplots()
            df_defect["defect_type"].value_counts().plot(kind="bar", ax=ax2)
            ax2.set_title("Defect Type Distribution")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)
        else:
            st.info("Defect Detection data not available.")

    if forecast_df is not None:
        st.markdown("#### Enterprise Demand Trend")
        demand_summary = forecast_df.groupby("date")[["actual_demand", "forecast_demand"]].sum()
        fig3, ax3 = plt.subplots()
        demand_summary.plot(ax=ax3)
        ax3.set_title("Enterprise Demand vs Forecast")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.info("Demand Forecasting data not available.")

    st.markdown("### Suggested Architecture")
    st.code(
        """ERP / MES / Sensors / Images / Demand History
        ↓
Data Preparation / Feature Engineering
        ↓
Machine Learning Models
        ↓
Model Outputs / KPIs / Alerts
        ↓
Executive Dashboard / Decision Making""",
        language="text"
    )

    st.markdown("### Strategic Value")
    st.markdown(
        """
- Improves manufacturing visibility across maintenance, quality, and planning  
- Converts AI outputs into financial and operational decisions  
- Provides a foundation for smart factory scaling and Industry 4.0 transformation  
"""
    )

# ==================================================
# 2. Predictive Maintenance
# ==================================================
elif module == "Predictive Maintenance":
    st.subheader("Predictive Maintenance")

    if pm_error:
        st.error(pm_error)
    elif pm_df is None:
        st.error("Predictive maintenance data unavailable.")
    else:
        st.sidebar.markdown("---")
        st.sidebar.subheader("PM Filters")

        plant_options = ["All"] + sorted(pm_df["plant"].unique().tolist())
        selected_plant = st.sidebar.selectbox("Plant Filter", plant_options, key="pm_plant")

        filtered_df = pm_df.copy()
        if selected_plant != "All":
            filtered_df = filtered_df[filtered_df["plant"] == selected_plant].copy()

        machine_options = filtered_df["machine_id"].tolist()
        selected_machine = st.sidebar.selectbox("Select Machine", machine_options, key="pm_machine")
        selected_row = filtered_df[filtered_df["machine_id"] == selected_machine].iloc[0]

        st.sidebar.subheader("Simulation")

        air_temperature = st.sidebar.slider(
            "Air Temperature",
            float(pm_df["air_temperature"].min() - 5),
            float(pm_df["air_temperature"].max() + 5),
            float(selected_row["air_temperature"]),
            key="pm_air"
        )

        process_temperature = st.sidebar.slider(
            "Process Temperature",
            float(pm_df["process_temperature"].min() - 5),
            float(pm_df["process_temperature"].max() + 5),
            float(selected_row["process_temperature"]),
            key="pm_process"
        )

        rotational_speed = st.sidebar.slider(
            "Rotational Speed",
            int(pm_df["rotational_speed"].min() - 100),
            int(pm_df["rotational_speed"].max() + 100),
            int(selected_row["rotational_speed"]),
            key="pm_speed"
        )

        torque = st.sidebar.slider(
            "Torque",
            float(pm_df["torque"].min() - 10),
            float(pm_df["torque"].max() + 10),
            float(selected_row["torque"]),
            key="pm_torque"
        )

        tool_wear = st.sidebar.slider(
            "Tool Wear",
            int(pm_df["tool_wear"].min()),
            int(pm_df["tool_wear"].max() + 20),
            int(selected_row["tool_wear"]),
            key="pm_tool"
        )

        temperature_diff = process_temperature - air_temperature

        selected_features = pd.DataFrame([{
            "air_temperature": air_temperature,
            "process_temperature": process_temperature,
            "rotational_speed": rotational_speed,
            "torque": torque,
            "tool_wear": tool_wear,
            "temperature_diff": temperature_diff
        }])

        failure_probability = pm_model.predict_proba(selected_features)[0][1]
        prediction = pm_model.predict(selected_features)[0]

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

        high_count = int((filtered_df["risk_level"] == "HIGH").sum())
        medium_count = int((filtered_df["risk_level"] == "MEDIUM").sum())
        low_count = int((filtered_df["risk_level"] == "LOW").sum())
        total_risk_exposure = int(filtered_df["estimated_risk_cost"].sum())

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

        st.subheader("Factory Maintenance KPIs")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("High Risk Machines", high_count)
        c2.metric("Medium Risk Machines", medium_count)
        c3.metric("Low Risk Machines", low_count)
        c4.metric("Total Risk Exposure (SGD)", f"${total_risk_exposure:,.0f}")

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

        st.subheader("Risk Distribution")
        risk_counts = filtered_df["risk_level"].value_counts().reindex(
            ["HIGH", "MEDIUM", "LOW"], fill_value=0
        )
        fig4, ax4 = plt.subplots()
        risk_counts.plot(kind="bar", ax=ax4)
        ax4.set_title("Machine Risk Distribution")
        ax4.set_ylabel("Number of Machines")
        ax4.set_xlabel("Risk Level")
        st.pyplot(fig4)

        st.subheader("Plant Risk Exposure")
        fig5, ax5 = plt.subplots()
        plant_risk.plot(kind="bar", ax=ax5)
        ax5.set_title("Risk Exposure by Plant")
        ax5.set_ylabel("Estimated Risk Cost (SGD)")
        ax5.set_xlabel("Plant")
        st.pyplot(fig5)

        st.subheader("Top 5 High-Risk Machines")
        top5 = filtered_df.sort_values(by="failure_probability", ascending=False).head(5).copy()
        top5["failure_probability"] = top5["failure_probability"].map(lambda x: f"{x:.2%}")
        top5["estimated_risk_cost"] = top5["estimated_risk_cost"].map(lambda x: f"SGD {x:,.0f}")
        st.dataframe(
            top5[["machine_id", "plant", "line", "failure_probability", "risk_level", "estimated_risk_cost"]],
            use_container_width=True
        )

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

# ==================================================
# 3. Defect Detection
# ==================================================
elif module == "Defect Detection":
    st.subheader("Defect Detection")

    dd_dir = BASE_DIR / "02-Defect-Detection"
    possible_csvs = list(dd_dir.glob("*.csv"))
    possible_pngs = list(dd_dir.glob("*.png")) + list(dd_dir.glob("*.jpg")) + list(dd_dir.glob("*.jpeg"))

    st.markdown(
        """
This module is intended to showcase vision-based inspection:

- defect classification  
- image-based quality control  
- early identification of faulty products  
"""
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Inspection Module", "Active")
    c2.metric("Use Case", "Quality Control")
    c3.metric("Primary Value", "Reduce Scrap")

    if possible_pngs:
        st.subheader("Sample Output / Visuals")
        st.image(str(possible_pngs[0]), width="stretch")
    else:
        st.info("Place one sample defect image or output screenshot inside 02-Defect-Detection to display here.")

    if possible_csvs:
        df_defect_local = pd.read_csv(possible_csvs[0])
        st.subheader("Sample Defect Data")
        st.dataframe(df_defect_local.head(), use_container_width=True)

        if "defect_type" in df_defect_local.columns:
            st.subheader("Defect Type Distribution")
            fig6, ax6 = plt.subplots()
            df_defect_local["defect_type"].value_counts().plot(kind="bar", ax=ax6)
            ax6.set_title("Defect Type Distribution")
            ax6.set_ylabel("Count")
            st.pyplot(fig6)

        metric_cols = st.columns(2)

        if "inspection_result" in df_defect_local.columns:
            defect_rate_local = (
                df_defect_local["inspection_result"].astype(str).str.lower() == "defective"
            ).mean()
            metric_cols[0].metric("Defect Rate", f"{defect_rate_local:.2%}")

        if "confidence" in df_defect_local.columns:
            avg_confidence_local = df_defect_local["confidence"].mean()
            metric_cols[1].metric("Average Confidence", f"{avg_confidence_local:.2f}")

    else:
        st.info("Place a CSV result file inside 02-Defect-Detection to show sample outputs.")

    st.markdown("### Business Value")
    st.markdown(
        """
- Reduce manual inspection effort  
- Detect defects earlier  
- Improve yield and product quality  
- Lower scrap and rework cost  
"""
    )

# ==================================================
# 4. Demand Forecasting
# ==================================================
elif module == "Demand Forecasting":
    st.subheader("Demand Forecasting")

    dfc_dir = BASE_DIR / "03-Demand-Forecasting"
    possible_csvs = list(dfc_dir.glob("*.csv"))

    st.markdown(
        """
This module is intended to showcase demand planning and forecasting:

- historical demand trend analysis  
- forecast-based planning  
- inventory and production optimization  
"""
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Planning Module", "Active")
    c2.metric("Use Case", "Forecasting")
    c3.metric("Primary Value", "Improve Planning Accuracy")

    if possible_csvs:
        forecast_df_local = pd.read_csv(possible_csvs[0])

        required_cols = ["date", "product_id", "actual_demand", "forecast_demand"]
        missing_cols = [c for c in required_cols if c not in forecast_df_local.columns]

        if missing_cols:
            st.error("Demand forecasting CSV missing columns: " + ", ".join(missing_cols))
        else:
            st.subheader("Sample Forecast Data")
            st.dataframe(
                forecast_df_local[["date", "product_id", "actual_demand", "forecast_demand"]].head(12),
                use_container_width=True
            )

            forecast_df_local["date"] = pd.to_datetime(forecast_df_local["date"])

            product_list = forecast_df_local["product_id"].dropna().unique().tolist()
            selected_product = st.selectbox("Select Product", product_list)

            product_df = forecast_df_local[forecast_df_local["product_id"] == selected_product].copy()

            st.subheader("Demand vs Forecast Trend")
            fig7, ax7 = plt.subplots()
            ax7.plot(product_df["date"], product_df["actual_demand"], label="Actual Demand")
            ax7.plot(product_df["date"], product_df["forecast_demand"], linestyle="--", label="Forecast")
            ax7.legend()
            ax7.set_title(f"Demand Forecast - {selected_product}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig7)

            product_df["error"] = (product_df["actual_demand"] - product_df["forecast_demand"]).abs()
            accuracy = 1 - (product_df["error"].mean() / product_df["actual_demand"].mean())

            st.metric("Forecast Accuracy", f"{accuracy:.2%}")

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Average Actual Demand", f"{product_df['actual_demand'].mean():.1f}")
            col_b.metric("Average Forecast Demand", f"{product_df['forecast_demand'].mean():.1f}")
            col_c.metric("Average Forecast Error", f"{product_df['error'].mean():.1f}")

            st.markdown("### AI-Generated Business Insights")

            trend = "increasing" if product_df["actual_demand"].iloc[-1] > product_df["actual_demand"].iloc[0] else "decreasing"
            bias = (product_df["forecast_demand"] - product_df["actual_demand"]).mean()

            if bias > 0:
                bias_type = "over-forecasting"
                recommendation = "Reduce production buffer and inventory levels."
                risk_text = "overproduction"
            else:
                bias_type = "under-forecasting"
                recommendation = "Increase safety stock and production planning."
                risk_text = "stockouts"

            if accuracy > 0.9:
                accuracy_level = "high"
            elif accuracy > 0.8:
                accuracy_level = "moderate"
            else:
                accuracy_level = "low"

            if accuracy < 0.8:
                st.error("⚠ ALERT: Forecast accuracy is below acceptable threshold. Immediate model review required.")
            elif bias > 10:
                st.warning("⚠ Warning: Significant over-forecasting detected.")

            st.info(
                f"""
📊 Demand Trend: Demand is **{trend}** over the observed period.

🎯 Forecast Performance: The model shows **{accuracy_level} accuracy** ({accuracy:.2%}).

⚖ Forecast Bias: The system is **{bias_type}**, indicating potential risk of **{risk_text}**.

💡 Recommendation:
- {recommendation}
- Continue monitoring forecast accuracy and retrain model if accuracy drops below 85%.
"""
            )

    else:
        st.info("Place a demand forecasting CSV inside 03-Demand-Forecasting to display data and charts.")

    st.markdown("### Business Value")
    st.markdown(
        """
- Improve forecast accuracy  
- Reduce overstock and shortages  
- Strengthen production planning  
- Support better inventory control  
"""
    )