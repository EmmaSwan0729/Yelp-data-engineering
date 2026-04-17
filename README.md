#!/usr/bin/env python
# coding: utf-8

# ## README
# 
# null

# # Yelp Lakehouse Data Engineering Pipeline 
# #### (Bronze → Silver → DQ → Gold → Monitoring)

# This project builds an end-to-end Lakehouse data pipeline using the Yelp public dataset,
# designed to transform raw, evolving business and review data into reliable analytical
# tables.
# 
# The pipeline emphasizes incremental processing, data quality validation, and operational
# observability to reflect real-world data engineering challenges, such as late-arriving data,
# schema consistency, and explainable pipeline behavior.

# ---

# ## Architecture

# ### High-level flow

# ```mermaid
# flowchart LR
#   A[Bronze\nRaw Ingest] --> B[Silver\nClean & Conform]
#   B --> C[DQ Checks\n(dq_rule_result)]
#   C --> D[Gate\nPASS / DEGRADED / BLOCKED]
#   D -->|PASS or DEGRADED| E[Gold\nBusiness Metrics]
#   D -->|BLOCKED| F[SKIPPED Gold Run]
# 
#   B --> G[pipeline_run_log\n(run status, duration, timestamps)]
#   C --> G
#   E --> G
# 
#   G --> H[Monitoring Views\n7d windows]
#   H --> I[Dashboard / Reporting\n(Power BI)]
# 
# ```

# ### Components
# - **Bronze**: raw ingestion with metadata (e.g., source file, ingest timestamp)
# - **Silver**: cleaned schema, type casting, derived columns, incremental scope
# - **DQ**: rule-based checks producing a standardized report table `gold_dq_report`
# - **Gold**: curated aggregates for analytics / BI
# - **Monitoring**: run log + views to track status, duration, DQ outcomes, and skip reasons

# ---

# ## Tech Stack 

# ### Data Processing
# - **Apache Spark (PySpark)** – distributed data processing and transformation
# - **Spark SQL** – aggregation, joins, and analytical queries
# 
# ### Lakehouse & Storage
# - **Delta Lake** – ACID-compliant tables for Bronze / Silver / Gold layers
# - **Lakehouse Architecture** – layered design for raw, cleaned, and curated data
# 
# ### Data Quality & Observability
# - **Custom Data Quality Framework** – rule-based checks with severity levels
# - **Pipeline Run Logging** – run-level observability including status, duration, and metrics
# - **Gate-controlled Execution** – SKIP and BLOCK logic to protect downstream Gold tables
# 
# ### Languages & Tooling
# - **Python** – pipeline logic, DQ rules, and utilities
# - **SQL** – data validation, monitoring views, and analysis
# - **Databricks / Microsoft Fabric Notebooks** – development and execution environment
# 

# ---

# ## Project Highlights

# ### Incremental processing with lookback window
# - Supports late-arriving data
# - Recomputes impacted business keys only, while preserving historical correctness

# ### Data Quality framework → standardized DQ report table
# - DQ rules produce structured metrics (row count, null ratio, value range, etc.)
# - Outputs as `gold_dq_report`, enabling auditability and trend monitoring

# ### Run observability via `pipeline_run_log`
# - Every run writes a log record including:
#   - pipeline name, run_id, timestamps, duration
#   - status (SUCCESS / FAILED / SKIPPED)
#   - counts and key metrics
#   - error context and skip reason

# ### Gate & Control Flow (production-style)
# - If upstream data not found → **SKIP**
# - If DQ severity is high → **BLOCK** downstream Gold write
# - Clear, explainable control flow for reliable operations

# ### SCD Type 2 dimensional model
# - `dim_business` and `dim_user` implement SCD Type 2 using Delta Lake MERGE
# - Three tracking columns added: `is_current`, `effective_from`, `effective_to`
# - When tracked attributes change, the old record is expired (`is_current = false`, `effective_to` set) and a new current record is inserted
# - Tracked attributes: name, city, state, stars, review_count, categories (business); name, review_count, average_stars, fans (user)
# - `fact_review` joins to dimensions on `is_current = true` to always reflect the latest version

# ---

# ## Repository Structure

# ```
# flowchart LR
# 
#   %% Execution Layer
#   A[Bronze\nRaw Ingest] --> B[Silver\nClean & Conform]
#   B --> C[DQ Checks\n(dq_rule_result)]
#   C --> D[Gate\nPASS / DEGRADED / BLOCKED]
#   D -->|PASS or DEGRADED| E[Gold\nBusiness Metrics]
#   D -->|BLOCKED| F[SKIPPED Gold Run]
# 
#   %% Logging Layer
#   B --> G[pipeline_run_log]
#   C --> G
#   E --> G
# 
#   %% Monitoring Layer
#   G --> H[Monitoring Views\n(7d rolling)]
#   H --> H1[Runtime Intelligence\n(P50 / P95 / Drift)]
#   H --> H2[SLA Monitoring\n(Config-driven)]
# 
#   %% Governance Layer
#   H2 --> J[SLA Summary]
#   H --> K[Composite Health Score]
# 
#   %% Config Table
#   S[pipeline_sla_config] --> H2
# 
#   %% Dashboard
#   J --> I[Dashboard / Reporting]
#   K --> I
#   H1 --> I
# 
# ```
# 

# ---

# ## Tables & Contracts

# #### `gold_dq_report`
# 
# Stores DQ check outcomes in a queryable format.
# 
# **Typical columns**
# - run_id: string (nullable = true)
# - layer: string (nullable = true)
# - dataset: string (nullable = true)
# - rule_name: string (nullable = true)
# - rule_type: string (nullable = true)
# - column_name: string (nullable = true)
# - metric_value: double (nullable = true)
# - threshold: double (nullable = true)
# - status: string (nullable = true)
# - checked_at: timestamp (nullable = true)
# - details: string (nullable = true)

# #### `pipeline_run_log`
# 
# Tracks pipeline run lifecycle for observability.
# 
# **Typical columns**
# - pipeline_run_id: string (nullable = true)
# - pipeline_name: string (nullable = true)
# - layer: string (nullable = true)
# - target_table: string (nullable = true)
# - status: string (nullable = true)
# - start_ts: timestamp (nullable = true)
# - end_ts: timestamp (nullable = true)
# - duration_sec: double (nullable = true)
# - dq_run_id: string (nullable = true)
# - dq_status: string (nullable = true)
# - dq_checked_table: string (nullable = true)
# - input_rows: long (nullable = true)
# - output_rows: long (nullable = true)
# - error_message: string (nullable = true)
# - created_at: timestamp (nullable = true)
# 

# ### Gold Analytical Tables
# 
# Other Gold tables are business-oriented aggregates derived from Silver data.
# 
# Their schemas may evolve based on analytical requirements and are therefore not treated as stable data contracts in this project.
# 
# This separation ensures that monitoring and governance layers rely only on explicitly defined contract tables.

# ---

# ## Monitoring & Observability
# 
# 

# ### Monitoring Framework Overview
# 
# The monitoring layer provides a production-style observability framework on top of all pipeline executions.
# 
# All pipeline runs are recorded in pipeline_run_log, and data quality results are persisted in:
# 
# - `dq_rule_result`
# 
# - `gold_dq_report`
# 
# Monitoring views aggregate these logs using a 7-day rolling window to provide structured operational visibility.
# 
# ---

# ### Observability Architecture
# 
# The monitoring layer is built on top of execution logs and DQ evidence tables.
# 
# It enables visibility into:
# 
# - Execution reliability
# 
# - Data quality stability
# 
# - Runtime behavior
# 
# - Skip / block patterns
# 
# - SLA compliance
# 
# The system separates:
# 
# - Raw execution logs (audit layer)
# 
# - Monitoring views (operational layer)
# 
# - Aggregated summaries (management layer)
# 
# - Composite health metrics (KPI layer)
# 
# This layered design ensures both traceability and operational clarity.
# 
# ---

# ### Execution Semantics
# 
# Pipeline execution outcomes are explicitly categorized:
# 
# - SUCCESS – Pipeline executed successfully
# 
# - DEGRADED – Pipeline executed with acceptable DQ risk
# 
# - BLOCKED – Execution prevented due to upstream conditions or CRITICAL DQ failure
# 
# - SKIPPED – Pipeline intentionally not executed (e.g., upstream Gate BLOCKED)
# 
# - FAILED – Pipeline terminated due to runtime or system errors
# 
# SKIPPED is treated as a first-class state to avoid false failure alerts and preserve semantic clarity.
# 
# ---

# ### Success Rate Semantics
# 
# Two success rate metrics are provided.
# 
# **1) Success Rate (Excluding SKIPPED)**  
# SKIPPED runs are excluded from the denominator because they represent intentional non-execution rather than failure.
# 
# Success Rate = SUCCESS / NULLIF((TOTAL - SKIPPED), 2)
# 
# If all runs are SKIPPED, the metric returns NULL to avoid misleading 0% values.
# 
# This metric reflects true execution reliability.
# 
# **2) Success Rate (Including SKIPPED)**  
# Success Rate = SUCCESS / TOTAL
# 
# This metric reflects overall pipeline experience, including intentional skips.
# 
# This design ensures that intentional non-execution (SKIPPED) does not artificially degrade reliability metrics.
# 
# ---

# ### Runtime Intelligence
# 
# Beyond binary success/failure monitoring, the system tracks runtime behavior.
# 
# Monitoring views provide:
# 
# - P50 runtime percentile (median execution time)
# 
# - P95 runtime percentile (tail latency indicator)
# 
# - Average duration
# 
# - Runtime drift detection (3-day vs 7-day comparison)
# 
# This enables detection of gradual performance degradation even when pipelines are still succeeding.
# 
# ---

# ### SLA Monitoring (Config-Driven)
# 
# SLA thresholds are externalized into a configuration table (pipeline_sla_config) rather than hardcoded.
# 
# This enables:
# 
# - Dynamic SLA updates without modifying monitoring logic
# 
# - Different thresholds per pipeline
# 
# - Future support for environment-specific configurations
# 
# SLA compliance is evaluated via:
# 
# - `v_monitor_sla_7d`
# 
# - `v_monitor_sla_summary_7d`
# 
# Breach counts and breach rates are aggregated over a 7-day rolling window.
# 
# ---

# ### Composite Run Health Score
# 
# A composite operational health score integrates multiple monitoring signals:
# 
# - Execution reliability (success rate)  (40%)
# 
# - SLA compliance  (30%)
# 
# - Blocked frequency  (20%)
# 
# - Critical DQ failures  (10%)
# 
# Weighting ensures that execution reliability and SLA compliance have greater impact on overall health than isolated DQ incidents.
# 
# 
# Each pipeline receives:
# 
# - A weighted health score (0–100)
# 
# A health classification:
# 
# - HEALTHY
# 
# - WARNING
# 
# - CRITICAL
# 
# This abstraction provides a management-level KPI for pipeline stability.
# 
# ---

# ### Operational Actionability
# 
# Monitoring outputs are designed to be actionable:
# 
# - FAILED runs surface error context
# 
# - SKIPPED runs include explicit skip reasons
# 
# - BLOCKED runs indicate upstream DQ issues
# 
# - SLA breaches highlight performance risks
# 
# - Critical DQ failures are prioritized for remediation
# 
# The monitoring layer is modular and extensible, allowing additional metrics to be added without altering pipeline execution logic.

# Together, these layers form a modular observability framework that separates execution logging, operational monitoring, governance control, and management-level KPIs.
# 

# ---

# ## How to Run
# 
# ### Production
# Trigger `PL_Master` in Microsoft Fabric. The pipeline orchestrates the full 
# Bronze → Silver → DQ → Gold → Monitoring flow automatically, including 
# DQ gate control and failure handling.
# 
# ### Manual / Debug
# Individual stages can be triggered via their dedicated notebooks:
# - `01_0_bronze_run_all` — Bronze ingestion
# - `02_0_silver_run_all` — Silver conformance
# - `03_2_dq_silver_run_all` — DQ checks
# - `04_7_run_gold_pipeline` — Gold marts
# - `05_1_monitoring_views` — Monitoring views

# ### Environment
# 
# This project is designed to run in:
# 
# Microsoft Fabric Lakehouse (recommended)
# 
# Databricks with Delta Lake support
# 
# Ensure that all Bronze raw data files are available in the configured storage location.

# ### Execution Order
# 
# #### 1. Bronze Ingestion
# 
# - Ingest raw Yelp data into Bronze tables.
# 
# Metadata columns such as _ingest_ts and _source_file are added.
# 
# #### 2. Silver Conform (Incremental Processing)
# 
# - Clean and standardize schemas.
# 
# - Apply incremental lookback window.
# 
# - Write conformed Silver tables.
# 
# #### 3. Data Quality Checks
# 
# - Execute DQ rules on Silver outputs.
# 
# - Write results to gold_dq_report and dq_rule_result.
# 
# #### 4. Gate Evaluation
# 
# - If no incremental data → SKIPPED
# 
# - If CRITICAL DQ failure → BLOCKED
# 
# - Otherwise → PASS
# 
# #### 5. Gold Aggregation
# 
# - Execute Gold transformations only when Gate = PASS or DEGRADED.
# 
# - Log run results in pipeline_run_log.
# 
# #### 6. Monitoring Layer
# 
# - Run 04_monitoring_views notebook.
# 
# - Refresh monitoring views:
# 
#   - Success rate
# 
#   - Runtime intelligence
# 
#   - SLA compliance
# 
#   - Composite health score
