# Enterprise AI Platform for Smart Manufacturing

## Executive Summary

This project demonstrates how Artificial Intelligence can be operationalized as an **enterprise capability**, rather than isolated use cases.

The platform integrates multiple AI domains into a unified **Executive Control Tower**, enabling leadership to make data-driven decisions across:

- Maintenance (Reliability)
- Quality (Defect Detection)
- Planning (Demand Forecasting)

This reflects how modern CIOs drive **AI-led transformation in manufacturing environments**.

---

## 🎯 Business Problem

Manufacturing organizations face three core challenges:

- Unplanned equipment downtime
- Inconsistent product quality
- Inefficient demand planning

These issues are often addressed in silos, resulting in:

- Reactive decision-making
- Limited visibility across operations
- Underutilization of data

---

## 💡 Solution Overview

This platform consolidates three AI use cases into a single interface:

### 1. Predictive Maintenance
- Predicts machine failure probability
- Classifies risk levels (High / Medium / Low)
- Estimates financial impact of downtime

### 2. Defect Detection
- Supports visual inspection workflows
- Enables defect classification and tracking
- Improves quality assurance processes

### 3. Demand Forecasting
- Compares actual vs forecast demand
- Measures forecast accuracy
- Identifies planning bias (over/under forecasting)

---

## 🧠 Executive Control Tower

The platform provides:

- **Platform KPI Summary**
  - High-risk machines
  - Total risk exposure (SGD)
  - Defect record volume
  - Forecast accuracy

- **Module Health Monitoring**
  - Ensures data and models are active

- **Executive Insights**
  - Translates AI outputs into business actions

This transforms AI into a **decision-support system**, not just a technical model.

---

## 🏭 Business Value

### Reliability
- Reduce unplanned downtime
- Optimize maintenance scheduling
- Improve asset utilization

### Quality
- Detect defects earlier
- Reduce scrap and rework
- Improve product consistency

### Planning
- Improve forecast accuracy
- Enable proactive production planning
- Reduce inventory inefficiencies

## 🧩 Architecture Overview
ERP / MES / IoT Sensors / Inspection Data / Demand Data
↓
Data Processing & Feature Engineering
↓
Machine Learning Models (by Use Case)
↓
Business Logic / KPI Layer / Risk Scoring
↓
Executive AI Control Tower (Streamlit)

## 🛠 Technology Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- Matplotlib
- Joblib

---

## 📂 Project Structure


AI-Learning-Journey/
│
├── 01-Predictive-Maintenance/
│ ├── train_model.py
│ ├── model.pkl
│ └── sample_machine_data.csv
│
├── 02-Defect-Detection/
│ ├── sample data / images
│
├── 03-Demand-Forecasting/
│ └── demand_forecast_sample.csv
│
├── app.py
├── README.md


---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py --server.port 8503


