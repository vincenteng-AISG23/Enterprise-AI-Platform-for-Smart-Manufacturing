# 🏭 AI Predictive Maintenance Dashboard

## 📌 Overview

This project demonstrates an **AI-powered predictive maintenance system** for smart manufacturing.

It analyzes machine operating conditions and predicts the likelihood of failure, translating technical signals into **actionable business decisions and financial impact**.

---

## 🎯 Business Objective

To reduce unplanned downtime and optimize maintenance planning by:

* Identifying high-risk machines early
* Prioritizing maintenance actions
* Quantifying potential business impact

---

## 🚀 Key Features

### 1. Executive Alert System

* Real-time alert when high-risk machines are detected
* Enables immediate operational response

---

### 2. Factory Maintenance KPIs

* High / Medium / Low risk machine counts
* Total estimated risk exposure (SGD)
* Designed for leadership-level visibility

---

### 3. Risk Distribution Visualization

* Visual breakdown of machine risk levels
* Enables quick understanding of overall plant condition

---

### 4. Machine-Level Risk Analysis

* Predicted failure risk (%)
* Asset health score
* Estimated downtime cost
* Recommended maintenance action

---

### 5. Explainable AI (Why This Machine is at Risk)

* Identifies key contributing factors (e.g. torque, temperature, tool wear)
* Improves trust and decision-making

---

### 6. Fleet Maintenance Overview

* All machines ranked by risk priority
* High-risk machines appear at the top
* Supports maintenance scheduling and resource allocation

---

### 7. Simulation Capability

* Adjust machine parameters (temperature, torque, wear, etc.)
* Observe how risk changes in real-time
* Enables “what-if” scenario analysis

---

## 🧠 AI / ML Approach

* Model: Random Forest Classifier

* Inputs:

  * Air temperature
  * Process temperature
  * Temperature difference
  * Rotational speed
  * Torque
  * Tool wear

* Output:

  * Failure probability
  * Risk classification (HIGH / MEDIUM / LOW)

---

## 💰 Business Impact

This system enables:

* Reduced unplanned equipment downtime
* Better prioritization of maintenance resources
* Lower production disruption risk
* Improved plant reliability and planning

---

## 🖥️ Dashboard Preview

> Example insights:

* 9 machines flagged as **HIGH risk**
* Estimated exposure: **SGD 292,000**
* Immediate action required for critical assets

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 📂 Project Structure

```
predictive-maintenance/
│
├── app.py
├── requirements.txt
├── README.md
├── sample_predictive_maintenance_data.csv
│
└── src/
    └── predictive_maintenance.py
```

---

## 🧩 Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-learn

---

## 🎯 Strategic Value

This project demonstrates how AI can be applied in manufacturing to:

* Move from reactive to predictive maintenance
* Bridge data science with business operations
* Deliver measurable financial impact

---

## 👤 Author

Vincent Eng Ping Choon
CIO / Head of IT | Smart Manufacturing & Digital Transformation

---
