# Industrial Predictive Maintenance
> End-to-end data pipeline for industrial failure prediction using AI4I 2020 dataset (UCI)

## Quick Summary
- **10,000 records** processed through a full analytics pipeline
- **XGBoost classifier** with ROC-AUC of 0.98 and 84% recall on failure detection
- **13 automated data quality tests** — 100% pass rate across all pipeline layers
- **762 high-risk machines** identified via tool wear classification
- **2 Power BI dashboards** — operational and executive views

## Tech Stack

| Layer | Tool |
|-------|------|
| Storage | PostgreSQL 16 |
| Transformation | dbt-core 1.11, dbt-postgres 1.10 |
| ML | scikit-learn, XGBoost 3.x |
| Orchestration | Apache Airflow 2.9.3 (Docker) |
| Reporting | Power BI Desktop (May 2026) |
| Version Control | Git + GitHub |
| Environment | WSL2 Ubuntu 24.04, Python 3.11.9 |

## Dataset

**AI4I 2020 Predictive Maintenance Dataset** — UCI Machine Learning Repository
10,000 records | 14 features | 5 failure types | 3.4% failure rate

| Failure Type | Cases | Rate |
|---|---|---|
| HDF — Heat Dissipation Failure | 115 | 1.15% |
| OSF — Overstrain Failure | 98 | 0.98% |
| PWF — Power Failure | 95 | 0.95% |
| TWF — Tool Wear Failure | 46 | 0.46% |
| RNF — Random Failure | 19 | 0.19% |

## For Analytics Engineer Roles

This project demonstrates end-to-end ownership of a data pipeline with production-grade practices:

- **dbt transformation layers** with documented lineage from raw ingestion to business-ready marts
- **13 automated data quality tests** covering nullability, uniqueness, and accepted value ranges
- **Dimensional modeling** with staging and mart separation, snake_case conventions, and schema-level isolation
- **DAX measures** and dual-view Power BI dashboard connected directly to PostgreSQL

The pipeline architecture mirrors what Analytics Engineers own in production: raw to staging to mart to reporting, with quality gates at each layer.

## For Data Engineer Jr Roles

This project demonstrates infrastructure and pipeline engineering fundamentals:

- **PostgreSQL ingestion pipeline** using psycopg2 with Unix socket authentication, bypassing SQLAlchemy version conflicts with Airflow
- **Apache Airflow 2.9.3 on Docker** with LocalExecutor, docker-compose configuration, and a DAG with 4 sequential tasks and retry logic
- **Dependency conflict resolution**: maintained SQLAlchemy <2.0 for Airflow compatibility while using psycopg2 directly for ingestion
- **Git history management**: purged binary files from commit history using git filter-branch after accidental .venv commit

Infrastructure decisions are documented with rationale in commit messages and code comments.

## For Data Scientist Jr Roles

This project demonstrates applied ML with industrial context:

- **Class imbalance handling**: 96.6%/3.4% split addressed with scale_pos_weight=28.5 in XGBoost — chosen over SMOTE given the imbalance level and dataset size
- **Feature engineering**: derived temperature_delta_k, power_kw, and tool_wear_category from raw sensor readings — domain-informed variables
- **Model evaluation beyond accuracy**: ROC-AUC (0.98), F1-score (0.73), and recall (84%) reported — accuracy alone would be misleading at 96.6% baseline
- **Top predictors**: rotational_speed_rpm (33%) and power_kw (21%) — findings with direct operational implications for maintenance scheduling

Model artifacts serialized with joblib for pipeline integration.

## Project Structure
industrial-predictive-maintenance/
├── data/
│   ├── raw/              # Original dataset (not tracked in git)
│   └── processed/        # Pipeline outputs
├── src/
│   ├── ingestion/        # load_raw.py
│   ├── features/         # eda.py
│   └── models/           # train_model.py, save_model.py
├── dbt/
│   └── predictive_maintenance/
│       └── models/
│           ├── staging/  # stg_ai4i2020.sql
│           └── marts/    # mart_machine_monitoring.sql
├── airflow/
│   ├── dags/             # predictive_maintenance_dag.py
│   └── docker-compose.yml
├── reports/              # Power BI .pbix
└── requirements.txt
```

## Reproducing This Project

```bash
# 1. Clone and set up environment
git clone https://github.com/MonicaVenzor/industrial-predictive-maintenance.git
cd industrial-predictive-maintenance
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Download dataset and place ai4i2020.csv in data/raw/

# 3. Run ingestion
python src/ingestion/load_raw.py

# 4. Run dbt transformations
cd dbt/predictive_maintenance
dbt run && dbt test

# 5. Train model
cd ../..
python src/models/save_model.py
```

## Author

**Monica Venzor** — Data Analytics | Genomic Biotechnology background
ISO 17025/9001 certified internal auditor | Industrial regulated environments
[GitHub](https://github.com/MonicaVenzor)
