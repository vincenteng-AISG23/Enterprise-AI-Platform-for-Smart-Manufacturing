# Executive Summary — Predictive Maintenance V2

## Objective
Predict whether a machine is likely to fail within the next 7 days using operational and sensor data.

## Why this matters
Unplanned machine downtime causes:
- production loss
- delayed customer shipments
- emergency maintenance cost
- quality risk
- reduced OEE

## Business value
A successful pilot can support:
- earlier maintenance intervention
- fewer breakdowns
- lower maintenance cost
- improved production continuity
- stronger confidence in smart factory investment

## Recommended pilot scope
- 1 plant
- 1 production line
- 3 to 5 critical machines
- 8 to 12 weeks of validation

## Suggested KPIs
- downtime hours reduced
- breakdown incidents reduced
- maintenance response lead time
- false positive rate
- precision / recall of failure alerts
- cost avoided from prevented stoppages

## Enterprise architecture view
Data sources:
- PLC / SCADA / sensor gateway
- MES
- CMMS
- ERP

ML flow:
- ingest sensor and work-order history
- engineer features
- train and score model
- push alert to maintenance / operations dashboard

## CIO message to business leaders
This is not an AI science experiment. It is an operational decision-support capability designed to reduce downtime and improve production reliability.
