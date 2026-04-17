import pytest
from pyspark.sql import functions as F

def make_business(spark, rows):
    """Helper:create a business_bronze-like DataFrame"""
    return spark.createDataFrame(rows, schema=[
        "business_id", "name", "stars", "review_count", "is_open"
    ])

def apply_silver_logic(df):
    """Replicate the core silver transformation logic"""
    return (
        df
        .withColumn("stars", F.col("stars").cast("double"))
        .withColumn("review_count", F.col("review_count").cast("int"))
        .withColumn("is_open", F.col("is_open").cast("int"))
        .dropDuplicates(["business_id"])
        .filter(F.col("business_id").isNotNull())
        .filter(F.col("stars").isNotNull())
        .filter((F.col("stars") >= 0 ) & (F.col("stars") <= 5))
        .filter(F.col("review_count").isNotNull())
        .filter(F.col("review_count") >= 0)
        .filter(F.col("is_open").isNotNull())
        .filter(F.col("is_open").isin(0,1))
    )

# ── Test 1: duplicate business_id should be deduplicated to one record ─────
def test_dedup_removes_duplicates(spark):
    df = make_business(spark, [
        ("biz_001", "Joe's Diner", 4.0, 100, 1),
        ("biz_001", "Joe's Diner", 4.0, 100, 1), # duplicate
    ])
    result = apply_silver_logic(df)
    assert result.count() == 1

# ── Test 2: null business_id should be filtered out ────────────────────────
def test_null_business_id_filtered(spark):
    df = make_business(spark, [
        ("biz_001", "Joe's Diner", 4.0, 100, 1),
        (None, "Unknown", 3.0, 50, 1),  # null business_id
    ])
    result = apply_silver_logic(df)
    assert result.count() == 1

# ── Test 3: stars out of range should be filtered out ──────────────────────
def test_invalid_stars_filtered(spark):
    df = make_business(spark, [
        ("biz_001", "Joe's Diner", 4.0, 100, 1),
        ("biz_002", "Bad Stars",   6.0, 50,  1),  # stars > 5
        ("biz_003", "Neg Stars",  -1.0, 50,  1),  # stars < 0
    ])
    result = apply_silver_logic(df)
    assert result.count() == 1

# ── Test 4: negative review_count should be filtered out ───────────────────
def test_negative_review_count_filtered(spark):
    df = make_business(spark, [
        ("biz_001", "Joe's Diner", 4.0,  100, 1),
        ("biz_002", "Bad Count",   3.0,  -1,  1),  # negative review_count
    ])

    result = apply_silver_logic(df)
    assert result.count() == 1

# ── Test 5: invalid is_open value should be filtered out ───────────────────
def test_invalid_is_open_filtered(spark):
    df = make_business(spark, [
        ("biz_001", "Joe's Diner", 4.0, 100, 1),
        ("biz_002", "Bad Open",    3.0,  50, 2),  # is_open not in (0, 1)
    ])
    result = apply_silver_logic(df)
    assert result.count() == 1