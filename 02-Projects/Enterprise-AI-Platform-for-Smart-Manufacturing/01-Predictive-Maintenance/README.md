# Predictive Maintenance for Smart Factory

## Executive Summary
This project demonstrates how manufacturing organizations can leverage machine learning to transition from reactive maintenance to predictive maintenance, reducing unplanned downtime and optimizing maintenance planning.

By analyzing machine sensor data, the solution predicts equipment failure risk within the next 7 days, enabling proactive intervention and improved operational efficiency.

---

## Business Problem
Unplanned equipment downtime is one of the most significant cost drivers in manufacturing operations. Traditional maintenance approaches are:
- Reactive (fix after failure)
- Time-based (scheduled regardless of condition)

These approaches lead to:
- Production losses
- Increased maintenance costs
- Inefficient resource allocation

---

## Solution Overview
This project builds a predictive maintenance model that converts machine sensor signals into a **risk-based prioritization system** for maintenance teams.

### Key Capabilities:
- Predict failure probability within a 7-day horizon
- Rank machines by failure risk
- Enable condition-based maintenance decisions

---

## Smart Manufacturing Context (Industry 4.0)
This solution aligns with Industry 4.0 initiatives by integrating:

- Data-driven decision making
- Machine-level analytics
- Predictive AI models
- Operational optimization

It supports the evolution toward:
👉 **Smart Factory / Autonomous Maintenance Systems**

---

## Business Impact (Estimated)
Implementing predictive maintenance can deliver:

- 🔻 20–40% reduction in unplanned downtime
- 🔻 10–30% reduction in maintenance costs
- 🔺 Improved asset utilization
- 🔺 Better production planning and scheduling

---

## Solution Architecture

**Data → Model → Insights → Action**

1. Machine sensor and operational data collected
2. Data processed and features engineered
3. Machine learning model predicts failure risk
4. Output delivered as ranked maintenance priorities

---

## Repository Contents

- `sample_machine_data.csv`  
  Synthetic dataset (1,200 records of machine health signals)

- `src/predictive_maintenance.py`  
  Model training and evaluation script

- `assets/`  
  Visualizations and model output charts

- `predictive_maintenance_project_deck.pptx`  
  Executive-level presentation for stakeholders

- `requirements.txt`  
  Python dependencies

---

## Business Scenario
A multi-line manufacturing plant aims to shift from reactive maintenance to condition-based maintenance.

The use case focuses on:
- Rotating equipment
- Packaging lines
- High-utilization assets

Where downtime is costly and maintenance windows are constrained.

---

## Data Fields (Sample)

- `machine_id`
- `production_line`
- `shift`
- `operating_hours_per_day`
- Sensor readings (temperature, vibration, etc.)

---

## Technology Stack

- Python
- Pandas / NumPy
- Scikit-learn
- Data visualization libraries

---

## Future Enhancements

- Integration with IoT platforms (Azure IoT Hub)
- Real-time streaming analytics
- Dashboard visualization (Power BI / Tableau)
- Integration with MES / ERP systems

---

## Strategic Value for Organizations

This project demonstrates how AI can be embedded into manufacturing operations to:

- Improve reliability engineering
- Enable data-driven maintenance strategies
- Support digital transformation initiatives

---

## Author
Vincent Eng Ping Choon  
Group Head of IT / Digital Transformation Leader