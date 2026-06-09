import pandas as pd
import psycopg2
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

DB_CONFIG = {"dbname": "mvenzor_db", "user": "mvenzor"}

def get_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM dev.mart_machine_monitoring", conn)
    conn.close()
    return df

def train_and_save():
    df = get_data()
    le = LabelEncoder()
    df["product_type_enc"] = le.fit_transform(df["product_type"])

    feature_cols = [
        "product_type_enc", "air_temperature_k", "process_temperature_k",
        "rotational_speed_rpm", "torque_nm", "tool_wear_min",
        "temperature_delta_k", "power_kw"
    ]

    X = df[feature_cols]
    y = df["machine_failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/xgb_failure_classifier.pkl")
    joblib.dump(le, "models/label_encoder.pkl")
    joblib.dump(feature_cols, "models/feature_cols.pkl")
    print("Modelo guardado en models/xgb_failure_classifier.pkl")

if __name__ == "__main__":
    train_and_save()
