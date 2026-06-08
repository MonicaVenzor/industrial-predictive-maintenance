"""
load_raw.py
-----------
Carga el dataset AI4I 2020 crudo a PostgreSQL sin transformaciones.
Principio: datos raw son inmutables - equivalente a cadena de custodia ISO 17025.
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": "mvenzor_db",
    "user": "mvenzor"
}

RAW_CSV = Path("data/raw/ai4i2020.csv")
TABLE_NAME = "raw_ai4i2020"


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def load_raw():
    log.info(f"Leyendo dataset desde {RAW_CSV}")
    df = pd.read_csv(RAW_CSV)
    log.info(f"Registros leidos: {len(df):,} | Columnas: {list(df.columns)}")

    # Normalizar nombres de columnas para PostgreSQL
    df.columns = [c.lower().replace(" ", "_").replace("[", "").replace("]", "").replace("/", "_") for c in df.columns]
    log.info(f"Columnas normalizadas: {list(df.columns)}")

    conn = get_conn()
    cur = conn.cursor()

    # Crear tabla
    cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cols_def = ", ".join([f"{col} TEXT" for col in df.columns])
    cur.execute(f"CREATE TABLE {TABLE_NAME} ({cols_def})")
    log.info(f"Tabla {TABLE_NAME} creada")

    # Insertar datos
    rows = [tuple(row) for row in df.itertuples(index=False)]
    cols = ", ".join(df.columns)
    execute_values(cur, f"INSERT INTO {TABLE_NAME} ({cols}) VALUES %s", rows)
    conn.commit()
    log.info(f"Datos insertados en {TABLE_NAME}")

    # Verificacion
    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    if count == len(df):
        log.info(f"Verificacion OK: {count:,} registros en PostgreSQL == {len(df):,} en CSV")
    else:
        log.error(f"Discrepancia: {count} en DB vs {len(df)} en CSV")
        sys.exit(1)


if __name__ == "__main__":
    load_raw()
