# COP Forecast Model (6-Hour Ahead)

## Overview

This module predicts compressor COP (Coefficient of Performance) 6 hours ahead using pre-trained XGBoost models.

Current implementation supports 2 compressor types:
- high
- booster

Prediction flow:
1. Read historical sensor data.
2. Generate time-aware features (time, lag, rolling windows).
3. Select features from config/feature_cols.json.
4. Predict prediction_COP_6h.
5. Optionally attach actual_COP_6h if performance_COP exists in input.

## Project Structure

```text
cop_forecast_model/
|- config/
|  |- feature_cols.json
|  \- settings.py
|- data/
|  |- sensordata_high.csv
|  |- sensordata_high_result.csv
|  |- sensordata_booster.csv
|  \- sensordata_booster_result.csv
|- model/
|  |- xgboost_high_performance_COP_forecast_6h.joblib
|  \- xgboost_booster_performance_COP_forecast_6h.joblib
|- preprocessing/
|  \- add_time_aware_features.py
|- predict.py
|- requirements.txt
\- readme.md
```

## Requirements

Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

Packages in requirements.txt:
- numpy
- pandas
- joblib
- xgboost
- scikit-learn
- matplotlib

## Input Data

Required minimum columns for prediction pipeline:
- _time
- compressor_id
- base sensor columns used by config/feature_cols.json

Typical base columns:
- amp, sp, dp, st, dt
- glycol_temp, glycol_level
- oil_filter, oil_level
- op, ot, slide_valve
- nh3_level, nh3_pump
- room_1b, room_1c, room_2b, room_2c, room_3b
- run_hour
- h1, h2, h3, h4
- superheat, subcool, T_evap, T_cond

Optional:
- performance_COP (if present, output will include actual_COP_6h for comparison)

Notes:
- Raw exports can contain extra columns (for example Column1, result, _start, _stop, _measurement). Extra columns are ignored.
- _time is parsed as UTC.

## Feature Engineering

Implemented in preprocessing/add_time_aware_features.py.

Generated features include:
- time features: hour, day_of_week, is_weekend, delta_hours
- lag features (1,2,3) for available columns in settings.LAG_SOURCE_COLS
- rolling mean/std with windows 6h, 12h, 24h for available columns in settings.ROLLING_SOURCE_COLS

Feature columns and order must match config/feature_cols.json exactly.

## Run Script

From cop_forecast_model folder:

```bash
python predict.py
```

Current default behavior in predict.py:
- Uses high dataset from data/sensordata_high.csv
- Merges with data/sensordata_high_result.csv
- Converts frontend/result column names via COPPredictor.convert_columns()
- Loads high model
- Writes output to prediction_high.csv

## Python Usage

```python
import pandas as pd
from predict import COPPredictor

sensor_df = pd.read_csv("data/sensordata_high.csv").merge(
    pd.read_csv("data/sensordata_high_result.csv"),
    on=["_time", "compressor_id"],
    how="left",
)

sensor_df = COPPredictor.convert_columns(sensor_df)

predictor = COPPredictor("high")  # or "booster"
result = predictor.predict(sensor_df)
print(result.head())
```

## Output

Returned/saved columns:
- _time
- forecast_time
- compressor_id
- prediction_COP_6h
- actual_COP_6h (may be NaN when future actual is unavailable)

Example output file:
- prediction_high.csv

## Common Errors

- ValueError: compressor_type must be 'high' or 'booster'
  - Pass only supported compressor type.

- ValueError: Missing features: [...]
  - Input does not contain all required features after preprocessing.
  - Check config/feature_cols.json and column mapping in config/settings.py.

## Maintenance Notes

- If feature engineering logic or feature list changes, retrain models and update feature_cols.json together.
- Keep model filenames consistent with predict.py loading logic.