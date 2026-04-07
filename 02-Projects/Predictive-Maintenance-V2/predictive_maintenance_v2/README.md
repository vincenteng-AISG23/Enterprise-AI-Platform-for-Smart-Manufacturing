# Predictive Maintenance V2

A practical, portfolio-ready predictive maintenance project designed for a CIO / Head of IT audience.

## What this project demonstrates
- End-to-end machine learning workflow
- Synthetic industrial sensor data generation
- Failure-risk prediction for equipment
- Model training, evaluation, and inference
- Executive-friendly outputs for business discussion
- Simple Streamlit app for demonstration

## Business problem
Manufacturing plants often rely on reactive or calendar-based maintenance. This project predicts whether a machine is at high risk of failure within the next 7 days based on sensor and operating data.

## Target outcome
Reduce unplanned downtime by identifying high-risk assets early enough for planned intervention.

## Project structure
```text
predictive_maintenance_v2/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_sensor_data.csv
├── docs/
│   └── executive_summary.md
├── models/
│   └── model.joblib
├── outputs/
│   ├── metrics.json
│   ├── feature_importance.csv
│   └── feature_importance.png
└── src/
    ├── data_simulation.py
    ├── train.py
    ├── predict.py
    └── evaluate.py
```

## Key features used
- temperature_c
- vibration_mm_s
- pressure_bar
- sound_db
- load_pct
- rpm
- humidity_pct
- maintenance_overdue_days
- machine_age_years
- shift

## Quick start
### 1) Create a virtual environment
```bash
python -m venv .venv
```

### 2) Activate it
**Windows**
```bash
.venv\Scripts\activate
```

**Mac/Linux**
```bash
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Regenerate sample data (optional)
```bash
python src/data_simulation.py
```

### 5) Train the model
```bash
python src/train.py
```

### 6) Run a sample prediction
```bash
python src/predict.py
```

### 7) Launch the demo dashboard
```bash
streamlit run app.py
```

## Model used
Random Forest Classifier with preprocessing:
- one-hot encoding for categorical columns
- standard scaling for numeric columns

This is intentionally business-friendly:
- robust baseline
- handles nonlinear relationships
- easier to explain than deep learning
- strong first model for industrial pilots

## Suggested CIO narrative
1. Start with one line and 3–5 critical assets.
2. Prove downtime reduction or earlier intervention.
3. Integrate with MES / CMMS / ERP for work-order orchestration.
4. Scale plant-by-plant with MLOps and data governance.

## Next enhancements
- Replace synthetic data with real PLC / SCADA / IoT streams
- Add anomaly detection
- Add time-window features
- Add maintenance recommendations
- Push alerts into Teams / email / CMMS
