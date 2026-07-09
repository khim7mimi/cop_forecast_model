import json
import pandas as pd
from joblib import load

from preprocessing.add_time_aware_features import add_time_aware_features
from config.settings import RESULT_FEATURE_MAP


class COPPredictor:

    def __init__(self, compressor_type):

        if compressor_type == "high":
            model_path = "model/xgboost_high_performance_COP_forecast_6h.joblib"
        elif compressor_type == "booster":
            model_path = "model/xgboost_booster_performance_COP_forecast_6h.joblib"
        else:
            raise ValueError("compressor_type must be 'high' or 'booster'")

        self.model = load(model_path)

        with open("config/feature_cols.json", "r", encoding="utf-8") as f:
            self.feature_cols = json.load(f)

    def predict(self, sensor_df):

        feature_df = add_time_aware_features(sensor_df.copy())

        missing = [
            col
            for col in self.feature_cols
            if col not in feature_df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing features:\n{missing}"
            )

        # เวลาที่ต้องการพยากรณ์
        feature_df["forecast_time"] = (
            pd.to_datetime(feature_df["_time"], utc=True)
            + pd.Timedelta(hours=6)
        )

        # ทำนาย
        feature_df["prediction_COP_6h"] = self.model.predict(
            feature_df[self.feature_cols]
        )

        # -------------------------------
        # ดึง COP จริงของเวลา forecast_time
        # -------------------------------
        if "performance_COP" in sensor_df.columns:

            actual_df = sensor_df[
                ["_time", "compressor_id", "performance_COP"]
            ].copy()

            actual_df["_time"] = pd.to_datetime(
                actual_df["_time"],
                utc=True,
                errors="coerce",
            )

            actual_df = actual_df.rename(
                columns={
                    "_time": "forecast_time",
                    "performance_COP": "actual_COP_6h",
                }
            )

            feature_df = feature_df.merge(
                actual_df,
                on=["forecast_time", "compressor_id"],
                how="left",
            )

        return feature_df[
            [
                "_time",
                "forecast_time",
                "compressor_id",
                "prediction_COP_6h",
                "actual_COP_6h",
            ]
        ]
    
    def convert_columns(sensor_df):
        """
        Convert frontend column names to model column names.
        """

        sensor_df = sensor_df.copy()

        reverse_map = {
            value: key
            for key, value in RESULT_FEATURE_MAP.items()
        }

        sensor_df = sensor_df.rename(columns=reverse_map)

        return sensor_df


if __name__ == "__main__":

    compressor_type = "high"      # เปลี่ยนเป็น "booster" ได้

    sensor_df = pd.read_csv(
        f"data/sensordata_{compressor_type}.csv"
    ).merge(
        pd.read_csv(
            f"data/sensordata_{compressor_type}_result.csv"
        ),
        on=["_time", "compressor_id"],
        how="left",
    )

    sensor_df = COPPredictor.convert_columns(sensor_df)

    predictor = COPPredictor(compressor_type)

    result = predictor.predict(sensor_df)

    result.to_csv(
        f"prediction_{compressor_type}.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(f"{compressor_type} prediction completed.")