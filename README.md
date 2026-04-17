# Yelp Lakehouse Data Engineering Pipeline
#### (Bronze → Silver → DQ → Gold → Monitoring)

This project builds an end-to-end Lakehouse data pipeline using the Yelp public dataset, designed to transform raw, evolving business and review data into reliable analytical tables.

The pipeline emphasizes incremental processing, data quality validation, and operational observability to reflect real-world data engineering challenges, such as late-arriving data, schema consistency, and explainable pipeline behavior.

---

## Architecture

### High-level flow

```mermaid
flowchart LR
  A[Bronze\nRaw Ingest] --> B[Silver\nClean & Conform]
  B --> C[DQ Checks\n(dq_rule_result)]
  C --> D[Gate\nPASS / DEGRADED / BLOCKED]
  D -->|PASS or DEGRADED| E[Gold\nBusiness Metrics]
  D -->|BLOCKED| F[SKIPPED Gold Run]

  B --> G[pipeline_run_log\n(run status, duration, timestamps)]
  C --> G
  E --> G

  G --> H[Monitoring Views\n7d windows]
  H --> I[Dashboard / Reporting\n(Power BI)]
```

### Components
- **Bronze**: raw ingestion with metadata (e.g., source file, ingest timestamp)
- **Silver**: cleaned schema, type casting, derived columns, incremental scope
- **DQ**: rule-based checks producing a standardized report table `dq_rule_result`
- **Gold**: curated aggregates for analytics / BI
- **Monitoring**: run log + views to track status, duration, DQ outcomes, and skip reasons

---

## Tech Stack

### Data Processing
- **Apache Spark (PySpark)** – distributed data processing and transformation
- **Spark SQL** – aggregation, joins, and analytical queries

### Lakehouse & Storage
- **Delta Lake** – ACID-compliant tables for Bronze / Silver / Gold layers
- **Lakehouse Architecture** – layered design for raw, cleaned, and curated data

### Data Quality & Observability
- **Custom Data Quality Framework** – rule-based checks with severity levels
- **Pipeline Run Logging** – run-level observability including status, duration, and metrics
- **Gate-controlled Execution** – SKIP and BLOCK logic to protect downstream Gold tables

### Languages & Tooling
- **Python** – pipeline logic, DQ rules, and utilities
- **SQL** – data validation, monitoring views, and analysis
- **Microsoft Fabric Notebooks** – development and execution environment

---

## Project Highlights

### Medallion architecture with incremental processing
- Full Bronze → Silver → Gold pipeline with metadata columns (`_ingest_ts`, `_source_file`, `_batch_id`)
- Supports late-arriving data with lookback window reprocessing

### Custom data quality framework
- Rule-based checks with severity levels (CRITICAL / MAJOR)
- Structured results written to `dq_rule_result` and `dq_table_gate`
- Gate decision (PASS / DEGRADED / BLOCKED) controls whether Gold runs

### SCD Type 2 dimensional model
- `dim_business` and `dim_user` implement SCD Type 2 using Delta Lake MERGE
- Three tracking columns added: `is_current`, `effective_from`, `effective_to`
- When tracked attributes change, the old record is expired (`is_current = false`, `effective_to` set) and a new current record is inserted
- Tracked attributes: name, city, state, stars, review_count, categories (business); name, review_count, average_stars, fans (user)
- `fact_review` joins to dimensions on `is_current = true` to always reflect the latest version

### Gate & control flow (production-style)
- CRITICAL DQ failure → BLOCKED, downstream Gold write is prevented
- MAJOR DQ failure → DEGRADED, Gold write proceeds with warning
- Intentional non-execution tracked as SKIPPED, not FAILED, to avoid false alerts

### Pipeline observability via `pipeline_run_log`
- Every run logs pipeline name, run ID, timestamps, input/output row counts, and DQ status
- Status categories: SUCCESS / DEGRADED / BLOCKED / SKIPPED / FAILED

### Fabric Pipeline orchestration
- `PL_Master` orchestrates the full Bronze → Silver → DQ → Gold → Monitoring flow
- DQ gate decision is passed via exit value to control downstream execution
- Each stage is independently re-runnable for debugging

### Monitoring framework (7-day rolling window)
- Runtime intelligence: P50 / P95 / drift detection
- SLA monitoring with config-driven thresholds (`pipeline_sla_config`)
- Composite health score (0–100) with HEALTHY / WARNING / CRITICAL classification

### Idempotency
Each pipeline stage is designed to be safely re-runnable:

| Layer | Strategy | Detail |
|-------|----------|--------|
| Bronze | `overwrite` | Full reload from raw source files on each run |
| Silver | `overwrite` | Rebuilt from Bronze on each run; dedup and filters ensure consistent output |
| Gold (dims) | SCD2 MERGE | Changed records are versioned; unchanged records are untouched |
| Gold (facts/metrics) | `overwrite` | Recomputed from Silver on each run |
| DQ | `append` | Results are additive by design for audit trail |

### Unit testing & CI
- 15 unit tests covering SCD2 logic, Silver dedup/filter rules, and DQ rule engine
- GitHub Actions CI runs tests automatically on every push to `main`

---

## Repository Structure

```
Yelp-data-engineering/
├── 01_bronze_ingest/
│   ├── 01_0_bronze_run_all.ipynb
│   ├── 01_1_bronze_business.ipynb
│   ├── 01_2_bronze_review.ipynb
│   ├── 01_3_bronze_checkin.ipynb
│   ├── 01_4_bronze_user.ipynb
│   └── 01_5_bronze_tip.ipynb
├── 02_silver_conform/
│   ├── 02_0_silver_run_all.ipynb
│   ├── 02_1_silver_business.ipynb
│   ├── 02_2_silver_review.ipynb
│   ├── 02_3_silver_checkin.ipynb
│   ├── 02_4_silver_user.ipynb
│   └── 02_5_silver_tip.ipynb
├── 03_dq_framework/
│   ├── 03_0_dq_init_tables.ipynb
│   ├── 03_1_dq_rule_engine.ipynb
│   ├── 03_1_1_dq_rule_config.ipynb
│   └── 03_2_dq_silver_run_all.ipynb
├── 04_gold_marts/
│   ├── 04_1_gold_fact_review.ipynb
│   ├── 04_2_gold_dim_business.ipynb
│   ├── 04_3_gold_dim_user.ipynb
│   ├── 04_4_gold_dim_date.ipynb
│   ├── 04_5_gold_business_metrics.ipynb
│   ├── 04_6_gold_city_metrics.ipynb
│   └── 04_7_run_gold_pipeline.ipynb
├── 05_monitoring/
│   ├── 05_0_monitoring_init.ipynb
│   └── 05_1_monitoring_views.ipynb
├── tests/
│   └── unit/
│       ├── conftest.py
│       ├── test_scd2.py
│       ├── test_silver_dedup.py
│       └── test_dq_rule_engine.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements-dev.txt
├── README.md
└── environment.md
```

---

## Monitoring & Observability

### Execution Semantics

Pipeline execution outcomes are explicitly categorized:

- **SUCCESS** – Pipeline executed successfully
- **DEGRADED** – Pipeline executed with acceptable DQ risk
- **BLOCKED** – Execution prevented due to CRITICAL DQ failure
- **SKIPPED** – Pipeline intentionally not executed (e.g., upstream Gate BLOCKED)
- **FAILED** – Pipeline terminated due to runtime or system errors

SKIPPED is treated as a first-class state to avoid false failure alerts.

### Success Rate Semantics

Two success rate metrics are provided:

**1) Success Rate (Excluding SKIPPED)**
SKIPPED runs are excluded from the denominator because they represent intentional non-execution rather than failure.

`Success Rate = SUCCESS / NULLIF((TOTAL - SKIPPED), 0)`

**2) Success Rate (Including SKIPPED)**

`Success Rate = SUCCESS / TOTAL`

### Runtime Intelligence

Monitoring views provide:
- P50 runtime percentile (median execution time)
- P95 runtime percentile (tail latency indicator)
- Average duration
- Runtime drift detection (3-day vs 7-day comparison)

### SLA Monitoring (Config-Driven)

SLA thresholds are externalized into `pipeline_sla_config` rather than hardcoded, enabling dynamic updates without modifying monitoring logic. SLA compliance is evaluated via `v_monitor_sla_7d` and `v_monitor_sla_summary_7d`.

### Composite Run Health Score

A composite operational health score integrates multiple monitoring signals:

| Signal | Weight |
|--------|--------|
| Execution reliability (success rate) | 40% |
| SLA compliance | 30% |
| Blocked frequency | 20% |
| Critical DQ failures | 10% |

Each pipeline receives a weighted health score (0–100) and a classification: **HEALTHY** / **WARNING** / **CRITICAL**.

---

## How to Run

### Production
Trigger `PL_Master` in Microsoft Fabric. The pipeline orchestrates the full Bronze → Silver → DQ → Gold → Monitoring flow automatically, including DQ gate control and failure handling.

### Manual / Debug
Individual stages can be triggered via their dedicated notebooks:
- `01_0_bronze_run_all` — Bronze ingestion
- `02_0_silver_run_all` — Silver conformance
- `03_2_dq_silver_run_all` — DQ checks
- `04_7_run_gold_pipeline` — Gold marts
- `05_1_monitoring_views` — Monitoring views

### Environment

This project is designed to run in Microsoft Fabric Lakehouse. Ensure that all Bronze raw data files are available in the configured storage location.

See `environment.md` for platform and runtime requirements.

---

## Acknowledgements

- **Yelp Dataset**: This project uses the [Yelp Open Dataset](https://www.yelp.com/dataset), kindly made available by Yelp Inc. for academic and personal learning purposes.
- **Microsoft Fabric**: Pipeline development and execution were carried out using [Microsoft Fabric](https://www.microsoft.com/en-us/microsoft-fabric).

---

## Disclaimer

This project is built solely for personal learning purposes. It is not intended for commercial use. All data used is publicly available and used in accordance with the Yelp Dataset Terms of Use.
