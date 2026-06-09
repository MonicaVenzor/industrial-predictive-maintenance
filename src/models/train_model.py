import pandas as pd
import psycopg2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

DB_CONFIG = {"dbname": "mvenzor_db", "user": "mvenzor"}

def get_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM dev.mart_machine_monitoring", conn)
    conn.close()
    return df

def train():
    df = get_data()
    print(f"Dataset: {len(df):,} registros")

    # Features y target
    le = LabelEncoder()
    df["product_type_enc"] = le.fit_transform(df["product_type"])

    feature_cols = [
        "product_type_enc", "air_temperature_k", "process_temperature_k",
        "rotational_speed_rpm", "torque_nm", "tool_wear_min",
        "temperature_delta_k", "power_kw"
    ]

    X = df[feature_cols]
    y = df["machine_failure"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")
    print(f"Fallas en test: {y_test.sum()} ({y_test.mean()*100:.1f}%)")

    # Calcular scale_pos_weight para desbalance
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    print(f"scale_pos_weight: {scale_pos_weight:.1f}")

    # Modelo
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    # Evaluacion
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n--- REPORTE DE CLASIFICACION ---")
    print(classification_report(y_test, y_pred, target_names=["No falla", "Falla"]))

    auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC: {auc:.4f}")

    # Feature importance
    print("\n--- IMPORTANCIA DE VARIABLES ---")
    importance = pd.Series(model.feature_importances_, index=feature_cols)
    print(importance.sort_values(ascending=False).round(4).to_string())

if __name__ == "__main__":
    train()
