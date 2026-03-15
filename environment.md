# Environment & Dependencies

This project is designed to run on a **managed Lakehouse platform** where core dependencies (Spark, Delta Lake) are provided by the platform runtime.

It is not a standalone Python package and cannot be run via `pip install`.

---

## Recommended Platform

| Platform | Support |
|----------|---------|
| Microsoft Fabric Lakehouse | ✅ Recommended |
| Databricks (with Delta Lake) | ✅ Compatible |
| Local PySpark (manual setup) | ⚠️ Possible but not tested |

---

## Runtime Requirements

| Component | Version |
|-----------|---------|
| Python | 3.10+ |
| Apache Spark (PySpark) | 3.4+ |
| Delta Lake | 2.4+ |
| Microsoft Fabric Runtime | 1.2+ (Spark 3.4 / Delta 2.4) |

---

## Python Libraries Used

All libraries below are available in the Microsoft Fabric / Databricks managed runtime and do not require manual installation.

| Library | Usage |
|---------|-------|
| `pyspark` | Distributed data processing and transformations |
| `pyspark.sql.functions` | Column operations, aggregations, type casting |
| `delta.tables` | Delta Lake merge (upsert) operations |
| `uuid` | Generating unique run identifiers |
| `datetime` | Timestamps for run logging and batch IDs |

---

## Storage Requirements

- Raw Yelp JSON files must be available in the Lakehouse file storage path:
  ```
  Files/yelp/raw/
  ├── yelp_business.json
  ├── yelp_review.json
  ├── yelp_user.json
  ├── yelp_checkin.json
  └── yelp_tip.json
  ```
- All Delta tables are written to the default Lakehouse catalog (`yelp_lakehouse.dbo`)

---

## Notes

- This project was developed and tested on **Microsoft Fabric** with the default Starter Pool (PySpark).
- All notebooks use the `synapse_pyspark` kernel.
- No additional pip packages are required beyond the managed runtime.
