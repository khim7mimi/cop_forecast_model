# COP Forecast Model (6-Hour Ahead)

## Overview

This project predicts the **Coefficient of Performance (COP)** of an industrial refrigeration compressor **6 hours in advance** using an XGBoost Regression model.

The model is trained from historical compressor sensor data together with engineered time-series features.

---

# Project Structure

```
cop_forecast_model/
│
├── model/
│   ├── xgboost_high_performance_COP_forecast_6h.joblib
│   └── xgboost_booster_performance_COP_forecast_6h.joblib
│
├── config/
│   ├── feature_cols.json
│   └── settings.py
│
├── preprocessing/
│   ├── __init__.py
│   └── add_time_aware_features.py
│
├── predict.py
├── requirements.txt
└── README.md
```

---

# Requirements

Python 3.10+

Install required packages

```bash
pip install -r requirements.txt
```

Required packages

```
numpy
pandas
xgboost
scikit-learn
joblib
```

---

# Model Information

| Item | Value |
|------|-------|
| Algorithm | XGBoost Regressor |
| Forecast Horizon | 6 Hours |
| Target | performance_COP |
| Features | 68 |

---

# Model Performance

### High Compressor

| Metric | Value |
|---------|------:|
| MAE | 0.236 |
| RMSE | 0.313 |
| R² | 0.610 |
| SMAPE | 7.04% |

### Booster Compressor

| Metric | Value |
|---------|------:|
| MAE | 0.306 |
| RMSE | 0.400 |
| R² | 0.092 |
| SMAPE | 9.85% |

---

# Input Data

The model requires historical sensor data.

Example columns

```
_time
compressor_id
amp
sp
dp
st
dt
glycol_temp
glycol_level
oil_filter
oil_level
op
ot
slide_valve
nh3_level
nh3_pump
room_1b
room_1c
room_2b
room_2c
room_3b
run_hour
h1
h2
h3
h4
superheat
subcool
T_evap
T_cond
```

---

# Feature Engineering

Before prediction, additional features must be generated automatically.

Generated Features include

- Hour
- Day of Week
- Weekend Flag
- Delta Hours

Lag Features

```
amp_lag_1
amp_lag_2
amp_lag_3

sp_lag_1
...

slide_valve_lag_3
```

Rolling Mean

```
6 Hours
12 Hours
24 Hours
```

Rolling Standard Deviation

```
6 Hours
12 Hours
24 Hours
```

Feature generation is performed by

```
preprocessing/add_time_aware_features.py
```

---

# Prediction Workflow

```
Sensor Data

        │

        ▼

Generate Time-aware Features

        │

        ▼

Select Features

(feature_cols.json)

        │

        ▼

Load XGBoost Model

        │

        ▼

Predict COP (6 Hours Ahead)
```

---

# Example Usage

```python
import pandas as pd

from predict import COPPredictor

predictor = COPPredictor(
    model_path="model/xgboost_high_performance_COP_forecast_6h.joblib",
    feature_path="config/feature_cols.json"
)

sensor_df = pd.read_csv("sensor_data.csv")

prediction = predictor.predict(sensor_df)

print(prediction)
```

---

# Output

The prediction result contains

```
_time

compressor_id

prediction_COP_6h
```

Example

| Time | Compressor | Predicted COP |
|------|------------|--------------:|
|2026-01-01 08:00|4|3.81|

---

# Important Notes

The model **cannot predict from a single sensor record**.

Historical data is required because the model uses

- Lag Features
- Rolling Mean
- Rolling Standard Deviation

The backend should provide enough historical records (at least **24 hours**) before calling the prediction function.

---

# Feature List

The model only accepts the feature names and order defined in

```
config/feature_cols.json
```

Do not

- change feature order
- remove features
- rename columns

---

# Output Target

```
prediction_COP_6h
```

Represents the predicted compressor COP **6 hours after the input timestamp**.

---

# Contact

If preprocessing logic or feature engineering is modified, the model should be retrained before deployment.