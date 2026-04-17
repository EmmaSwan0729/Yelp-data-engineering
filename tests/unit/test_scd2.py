import pytest
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType, TimestampType

def make_dim(spark, rows):
    """Helper: create a dim_business-like DataFrame."""
    
    return spark.createDataFrame(rows, schema=[
        "business_id", "name", "city", "state", "stars", "review_count", "is_current"
    ])

# ── Test 1: new record should be inserted with is_current=True ─────────────
def test_new_record_is_current(spark):
    df = make_dim(spark, [
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True)
    ])
    current = df.filter(F.col("is_current") == True)
    assert current.count() == 1

# ── Test 2: unchanged record should not produce a new version ──────────────
def test_unchanged_record_no_new_version(spark):
    existing = make_dim(spark, [
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True)
    ])
    incoming = make_dim(spark,[
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True)
    ])
    scd_cols = ["name", "city", "state", "stars", "review_count"]
    change_connd = " OR ".join([f"current.{c} <> new.{c}" for c in scd_cols])

    df_changed = (
        existing.alias("current")
        .join(incoming.alias("new"), "business_id")
        .filter(change_connd)
    )
    assert df_changed.count() == 0

# ── Test 3: changed record should be detected ──────────────────────────────
def test_changed_record_detected(spark):
    existing = make_dim(spark,[
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True)
    ])
    incoming = make_dim(spark, [
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.5, 150, True)  
    ])

    scd_rows = ["name", "city", "state", "stars", "review_count"]
    change_connd = " OR ".join([f"current.{c} <> new.{c}" for c in scd_rows])

    df_changed = (
        existing.alias("current")
        .join(incoming.alias("new"), "business_id")
        .filter(change_connd)
    )

    assert df_changed.count() == 1

# ── Test 4: brand new business_id should be identified as new insert ───────
def test_brand_new_record_inserted(spark):
    existing = make_dim(spark,[
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True)
    ])
    incoming = make_dim(spark, [
        ("biz_001", "Joe's Diner", "Phoenix", "AZ", 4.0, 100, True),
        ("biz_002", "New Place", "Tucson", "AZ", 3.5, 50, True) 
    ])

    existing_ids = existing.select("business_id")
    df_new = incoming.join(existing_ids, "business_id", "left_anti")

    assert df_new.count() == 1
    assert df_new.collect()[0]["business_id"] == "biz_002"