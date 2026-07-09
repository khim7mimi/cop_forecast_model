import pandas as pd
from config.settings import LAG_SOURCE_COLS, ROLLING_SOURCE_COLS


# สร้าง Time-aware Features สำหรับข้อมูล Time Series ของแต่ละ Compressor
# โดยเพิ่ม Time Features (hour, day_of_week, is_weekend, delta_hours),
# Lag Features (ค่าข้อมูลย้อนหลัง), และ Rolling Statistics (ค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐานย้อนหลัง)
# เพื่อใช้เป็น Input ในการฝึกโมเดลพยากรณ์
def add_time_aware_features(raw_df):
    raw_df = raw_df.copy()
    raw_df["_time"] = pd.to_datetime(raw_df["_time"], utc=True, errors="coerce")

    parts = []
    grouped = raw_df.sort_values(["compressor_id", "_time"]).groupby("compressor_id", sort=False)

    for compressor_id, group in grouped:
        feature_df = group.copy().sort_values("_time")
        feature_df["delta_hours"] = (
            feature_df["_time"].diff().dt.total_seconds() / 3600
        )
        feature_df["hour"] = feature_df["_time"].dt.hour
        feature_df["day_of_week"] = feature_df["_time"].dt.dayofweek
        feature_df["is_weekend"] = feature_df["day_of_week"].isin([5, 6]).astype(int)

        for col in [c for c in LAG_SOURCE_COLS if c in feature_df.columns]:
            for lag in (1, 2, 3):
                feature_df[f"{col}_lag_{lag}"] = feature_df[col].shift(lag)

        time_indexed = feature_df.set_index("_time")
        for col in [c for c in ROLLING_SOURCE_COLS if c in feature_df.columns]:
            for window in ("6h", "12h", "24h"):
                feature_df[f"{col}_mean_{window}"] = (
                    time_indexed[col].rolling(window, min_periods=2).mean().values
                )
                feature_df[f"{col}_std_{window}"] = (
                    time_indexed[col].rolling(window, min_periods=2).std().values
                )

        parts.append(feature_df)

    return pd.concat(parts, ignore_index=True)