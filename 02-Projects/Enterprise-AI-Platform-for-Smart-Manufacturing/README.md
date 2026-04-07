# 🚀 Enterprise AI Control Tower for Smart Manufacturing

## Executive Summary

This project demonstrates how Artificial Intelligence can be operationalized as an enterprise capability, not isolated use cases.

The platform integrates multiple AI domains into a unified Executive Control Tower, enabling leadership to make data-driven decisions across:

- Maintenance (Reliability)
- Quality (Defect Detection)
- Planning (Demand Forecasting)

This reflects how modern CIOs drive AI-led transformation in manufacturing environments.

---

## 🎯 Business Problem

Manufacturing organizations face three core challenges:

- Unplanned equipment downtime  
- Inconsistent product quality  
- Inefficient demand planning  

These issues are often addressed in silos, resulting in:

- Reactive decision-making  
- Limited operational visibility  
- Underutilization of enterprise data  

---

## 💡 Solution Overview

This platform consolidates three AI use cases into a single interface:

### 1. Predictive Maintenance
- Predicts machine failure probability  
- Classifies risk levels (High / Medium / Low)  
- Estimates financial impact of downtime  

### 2. Defect Detection
- Supports inspection workflows  
- Enables defect classification and tracking  
- Improves quality assurance processes  

### 3. Demand Forecasting
- Compares actual vs forecast demand  
- Measures forecast accuracy  
- Identifies planning bias (over / under forecasting)  

---

## 🧠 Executive Control Tower

The platform provides:

- Platform KPI Summary
  - High-risk machines  
  - Total risk exposure (SGD)  
  - Defect record volume  
  - Forecast accuracy  

- Module Health Monitoring
  - Ensures data pipelines and models are active  

- Executive Insights
  - Translates AI outputs into business actions  

This transforms AI into a decision-support system, not just a technical model.

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

---

## 🧩 Architecture Overview

```
ERP / MES / IoT Sensors / Inspection Data / Demand Data
                        ↓
            Data Processing & Feature Engineering
                        ↓
        Machine Learning Models (by Use Case)
                        ↓
      Business Logic / KPI Layer / Risk Scoring
                        ↓
        Executive AI Control Tower (Streamlit)
```

---

## 🛠 Technology Stack

- Python  
- Streamlit  
- Scikit-learn  
- Pandas  
- Matplotlib  
- Joblib  

---

## 📂 Project Structure

```
AI-Learning-Journey/
│
├── 01-Predictive-Maintenance/
│   ├── train_model.py
│   ├── model.pkl
│   └── sample_machine_data.csv
│
├── 02-Defect-Detection/
│   ├── sample data / images
│
├── 03-Demand-Forecasting/
│   └── demand_forecast_sample.csv
│
├── app.py
├── README.md
```

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py --server.port 8503
```

---

## 📊 Platform Preview (Recommended)

Add your screenshots here after uploading images to GitHub:

images/
├── executive_overview.png
├── predictive_maintenance.png

Then reference them:

![Executive Overview](images/executive_overview.png)
![Predictive Maintenance](images/predictive_maintenance.png)

---

## 🔭 Roadmap (Next Phase)

- Integration with MES / ERP / IoT systems  
- Multi-plant deployment  
- Real-time data streaming  
- Model monitoring and retraining (MLOps)  
- Role-based dashboards for operations leaders  

---

## 👔 CIO Perspective

This project demonstrates:

- How AI aligns with business outcomes  
- How multiple AI use cases integrate into a single enterprise platform  
- How CIOs lead data-driven transformation in manufacturing  

AI is not just about models — it is about embedding intelligence into operations and decision-making.

---

## 📌 Author

Vincent Eng  
Group Head of IT | Smart Manufacturing | AI Transformation Leader
