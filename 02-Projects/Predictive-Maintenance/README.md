# Predictive Maintenance for Smart Factory

A starter portfolio project that demonstrates how a manufacturing team can use machine sensor data to predict equipment failure risk in the next 7 days.

## Project goal
Reduce unplanned downtime by turning sensor and maintenance signals into a ranked risk score for maintenance planners.

## Repository contents
- `sample_machine_data.csv` — synthetic machine health dataset with 1,200 records
- `src/predictive_maintenance.py` — training and evaluation script
- `assets/` — charts used in the presentation
- `predictive_maintenance_project_deck.pptx` — stakeholder presentation
- `requirements.txt` — Python dependencies

## Business scenario
A multi-line factory wants to shift from reactive maintenance to condition-based maintenance. The use case focuses on rotating equipment and packaging assets where downtime is costly and maintenance windows are limited.

## Data fields
- `machine_id`
- `production_line`
- `shift`
- `operating_hours_per_day`
- `temperature_c`
- `vibration_mm_s`
- `pressure_psi`
- `current_a`
- `humidity_pct`
- `line_speed_units_min`
- `days_since_maintenance`
- `defect_rate_pct`
- `energy_spike_flag`
- `failure_next_7d`

## Modeling approach
The baseline project uses a random forest classifier with one-hot encoded categorical features.

## Sample results
- ROC AUC: 0.772
- Precision: 0.677
- Recall: 0.757
- F1 score: 0.715

These figures are illustrative because the project uses synthetic sample data.

## How to run
```bash
pip install -r requirements.txt
python src/predictive_maintenance.py
```

## Recommended portfolio extensions
1. Replace the synthetic data with historian / MES / CMMS data.
2. Add time-series features such as rolling vibration trend and temperature drift.
3. Calibrate alert thresholds by machine criticality.
4. Deploy the model behind an API or scheduled batch job.
5. Connect alerts to a maintenance ticket workflow.

## Why this project matters
This project shows how AI can create measurable business value in smart manufacturing:
- fewer unplanned stops
- better maintenance prioritization
- improved spare-parts planning
- better coordination between OT, engineering, and IT

## Notes
All data and model outputs in this starter package are synthetic and intended for demonstration and portfolio use.
