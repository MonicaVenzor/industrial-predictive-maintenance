import pandas as pd
import psycopg2

DB_CONFIG = {"dbname": "mvenzor_db", "user": "mvenzor"}

def get_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM dev.mart_machine_monitoring", conn)
    conn.close()
    return df

def run_eda():
    df = get_data()
    total = len(df)
    failures = df["machine_failure"].sum()

    print(f"\n{'='*50}")
    print(f"DATASET: {total:,} registros, {len(df.columns)} columnas")
    print(f"{'='*50}")

    print("\n--- DISTRIBUCION DE FALLAS ---")
    print(f"Sin falla:  {total - failures:,} ({(total-failures)/total*100:.1f}%)")
    print(f"Con falla:  {failures:,} ({failures/total*100:.1f}%)")

    print("\n--- TIPOS DE FALLA ---")
    for col in ["twf", "hdf", "pwf", "osf", "rnf"]:
        n = df[col].sum()
        print(f"  {col.upper()}: {n:,} casos ({n/total*100:.2f}%)")

    print("\n--- DISTRIBUCION POR TIPO DE PRODUCTO ---")
    print(df["product_type"].value_counts().to_string())

    print("\n--- ESTADISTICAS DE SENSORES ---")
    sensor_cols = ["air_temperature_k", "process_temperature_k",
                   "rotational_speed_rpm", "torque_nm", "tool_wear_min",
                   "temperature_delta_k", "power_kw"]
    print(df[sensor_cols].describe().round(2).to_string())

    print("\n--- FALLAS POR CATEGORIA DE DESGASTE ---")
    print(df.groupby("tool_wear_category")["machine_failure"].agg(["sum","count","mean"]).round(3).to_string())

if __name__ == "__main__":
    run_eda()
