import pandas as pd

FORECAST_HORIZON = pd.Timedelta(hours=6)

MAX_TARGET_DELAY = pd.Timedelta(hours=2)

BASE_FEATURES = [
    "amp",
    "sp",
    "dp",
    "st",
    "dt",
    "glycol_temp",
    "glycol_level",
    "oil_filter",
    "oil_level",
    "op",
    "ot",
    "slide_valve",
    "nh3_level",
    "nh3_pump",
    "room_1b",
    "room_1c",
    "room_2b",
    "room_2c",
    "room_3b",
    "run_hour",
    "compressor_id",
    "h1",
    "h2",
    "h3",
    "h4",
    "superheat",
    "subcool",
    "T_evap",
    "T_cond",
]

LAG_SOURCE_COLS = [
    "performance_COP",
    "amp",
    "sp",
    "dp",
    "slide_valve",
]

ROLLING_SOURCE_COLS = [
    "performance_COP",
    "amp",
    "sp",
    "dp",
    "slide_valve",
]

RESULT_FEATURE_MAP = {
    "h1": "enthalpy_h1",
    "h2": "enthalpy_h2",
    "h3": "enthalpy_h3",
    "h4": "enthalpy_h4",
    "superheat": "saturation_superheat",
    "subcool": "saturation_subcool",
    "T_evap": "saturation_T_evap",
    "T_cond": "saturation_T_cond",
}