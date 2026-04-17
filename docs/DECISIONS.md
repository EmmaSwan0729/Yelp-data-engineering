# Architecture Decision Records

This document records key design decisions made during the development of this pipeline,
including the rationale behind each choice.

---

## ADR-001: Star Schema over One Big Table (OBT)

**Decision**: Use a star schema with `fact_review` at the center, joined to `dim_business`, `dim_user`, and `dim_date`.

**Rationale**:
- OBT simplifies queries but duplicates dimension data across millions of fact rows, increasing storage cost and making dimension updates expensive
- Star schema separates facts and dimensions cleanly, making SCD2 updates on dimensions straightforward without touching the fact table
- Better alignment with BI tools like Power BI, which are optimized for star schema relationships

**Trade-off**: Queries require joins, but Z-Order and partition pruning on `fact_review` mitigate the performance cost.

---

## ADR-002: Partition `fact_review` by `date_id`

**Decision**: Partition `fact_review` by `date_id` rather than `business_id` or `user_id`.

**Rationale**:
- The most common analytical queries filter by time range (e.g. reviews in the last 30 days)
- Date-based partitioning enables partition pruning, avoiding full table scans for time-bounded queries
- `business_id` and `user_id` have high cardinality, which would create too many small partitions and degrade performance

**Trade-off**: Queries filtering only by `business_id` without a date range cannot benefit from partition pruning, but Z-Order on `business_id` within each partition compensates.

---

## ADR-003: SCD Type 2 for `dim_business` and `dim_user`

**Decision**: Implement SCD Type 2 for dimension tables rather than SCD Type 1 (overwrite).

**Rationale**:
- Business attributes like `stars` and `review_count` change over time; SCD1 would silently overwrite history
- SCD2 preserves historical snapshots, enabling point-in-time analysis (e.g. what was a business's rating when a review was written)
- Delta Lake MERGE makes SCD2 implementation straightforward without custom deduplication logic

**Trade-off**: Table size grows over time as historical versions accumulate; `is_current = true` filter must be applied consistently in downstream queries.

---

## ADR-004: Severity-based DQ gating (CRITICAL / MAJOR)

**Decision**: Distinguish between CRITICAL and MAJOR DQ failures, with only CRITICAL failures blocking Gold execution.

**Rationale**:
- Not all data quality issues are equally severe; a small percentage of null values in a non-key column should not halt the entire pipeline
- CRITICAL failures (e.g. null primary keys) indicate data that cannot be trusted at all
- MAJOR failures (e.g. slightly elevated null rates in optional fields) result in DEGRADED status, allowing Gold to proceed with a warning
- This avoids over-alerting while still surfacing genuine data integrity issues

**Trade-off**: Requires careful classification of rules; misclassifying a MAJOR rule as CRITICAL could cause unnecessary pipeline failures.

---

## ADR-005: Gold layer remains in Lakehouse (not Warehouse)

**Decision**: Keep Gold tables in the Lakehouse rather than moving them to a Fabric Warehouse.

**Rationale**:
- Keeping the full pipeline within Delta Lake maintains a unified technology stack and avoids additional data movement steps
- Delta Lake MERGE is required for SCD2 on dimension tables, which is not natively supported in Fabric Warehouse
- The Lakehouse SQL Analytics Endpoint provides sufficient query performance for the current analytical workload
- If Gold data is consumed by machine learning workloads, Lakehouse is the preferred choice as ML frameworks (PySpark, sklearn) read Delta files directly and benefit from Delta Time Travel for reproducible training datasets

**Trade-off**: BI query performance may be lower than a native Warehouse for high-concurrency workloads; if this becomes a bottleneck, Fabric Shortcuts can expose Gold tables to a Warehouse without duplicating data.

---

---

## ADR-006: `batch_id` propagated from PL_Master through all pipeline stages

**Decision**: Generate a single `batch_id` in `PL_Master` and pass it through all notebook stages.

**Rationale**:
- A shared `batch_id` across Bronze, Silver, DQ, and Gold allows all logs and DQ results from a single pipeline run to be correlated
- Without a shared ID, diagnosing issues across layers requires matching by timestamp, which is error-prone
- Pipeline-level ID generation ensures consistency even when individual notebooks are re-run for debugging

**Trade-off**: Notebooks must accept `batch_id` as an external parameter; fallback to a locally generated ID is provided for manual execution.