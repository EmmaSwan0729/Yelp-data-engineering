import pytest
from datetime import datetime
from pyspark.sql import functions as F

# ── Copy core functions from 03_1_dq_rule_engine ──────────────────────────
def make_rule_result_row(
    dq_run_id, pipeline_run_id, run_ts, layer, table_name,
    rule_id, rule_name, rule_type, column_name, severity, dimension,
    total_count, failed_count, failed_rate, threshold_rate, status, rule_message
):
    return {
        "dq_run_id": dq_run_id,
        "pipeline_run_id": pipeline_run_id,
        "run_ts": run_ts,
        "layer": layer,
        "table_name": table_name,
        "rule_id": rule_id,
        "rule_name": rule_name,
        "rule_type": rule_type,
        "column_name": column_name,
        "severity": severity,
        "dimension": dimension,
        "total_count": int(total_count) if total_count is not None else None,
        "failed_count": int(failed_count) if failed_count is not None else None,
        "failed_rate": float(failed_rate) if failed_rate is not None else None,
        "threshold_rate": float(threshold_rate) if threshold_rate is not None else None,
        "status": status,
        "rule_message": rule_message
    }

def eval_standard_rule(df, rule, dq_run_id, pipeline_run_id, layer, table_name, run_ts):
    total_count = df.count()
    failed_count = df.filter(rule["fail_cond"]).count()
    failed_rate = failed_count / total_count if total_count > 0 else 0.0
    threshold_rate = rule["threshold_rate"]
    status = "FAIL" if failed_rate > threshold_rate else "PASS"
    rule_message = (
        f"{rule['rule_name']} failed_rate = {failed_rate:.6f}, "
        f"threshold_rate = {threshold_rate:.6f}"
    )
    return make_rule_result_row(
        dq_run_id=dq_run_id, 
        pipeline_run_id=pipeline_run_id, 
        run_ts=run_ts,
        layer=layer, 
        table_name=table_name, 
        rule_id=rule["rule_id"],
        rule_name=rule["rule_name"], 
        rule_type=rule["rule_type"],
        column_name=rule.get("column_name"), severity=rule["severity"],
        dimension=rule["dimension"], 
        total_count=total_count,
        failed_count=failed_count, 
        failed_rate=failed_rate,
        threshold_rate=threshold_rate, 
        status=status, 
        rule_message=rule_message
    )

def build_gate_result(rule_results, dq_run_id, pipeline_run_id, layer, table_name, run_ts):
    total_rules = len(rule_results)
    passed_rules = sum(1 for r in rule_results if r["status"] == "PASS")
    failed_rules = sum(1 for r in rule_results if r["status"] == "FAIL")
    critical_failed = sum(1 for r in rule_results if r["status"] == "FAIL" and r["severity"] == "CRITICAL")
    major_failed = sum(1 for r in rule_results if r["status"] == "FAIL" and r["severity"] == "MAJOR")

    if critical_failed > 0:
        decision = "BLOCKED"
        reason = "At least on CRITICAL rule failed."
    elif major_failed > 0:
        decision = "DEGRADED"
        reason = "All rules passed or only non-blocking issues found."
    else:
        decision = "PASS"
        reason = "All rules passed or only non-blocking issues found."
    
    return {
        "dq_run_id": dq_run_id,
        "pipeline_run_id": pipeline_run_id,
        "run_ts": run_ts,
        "layer": layer,
        "table_name": table_name,
        "total_rules": total_rules,
        "passed_rules": passed_rules,
        "failed_rules": failed_rules,
        "critical_rules": critical_failed,
        "major_rules": major_failed,
        "decision": decision,
        "reason": reason
    }
# ── Fixtures ───────────────────────────────────────────────────────────────
@pytest.fixture
def run_meta():
    return {
        "dq_run_id": "dq_test_001",
        "pipeline_run_id": "pipeline_test_001",
        "run_ts": datetime(2026,1,1),
        "layer": "silver",
        "table_name": "business_silver"
    }

# ── Test 1: null check should PASS when no nulls ───────────────────────────
def test_null_check_passes(spark, run_meta):
    df = spark.createDataFrame(
        [("biz_001",), ("biz_002",)], schema=["business_id"]
    )
    rule = {
        "rule_id": "bus_001",
        "rule_name": "business_id_not_null",
        "rule_type": "null_check",
        "column_name": "business_id",
        "severity": "CRITICAL",
        "dimension": "completeness",
        "fail_cond": F.col("business_id").isNull(), 
        "threshold_rate": 0.0
    }
    result = eval_standard_rule(df,rule, **run_meta)
    assert result["status"] == "PASS"
    assert result["failed_count"] == 0
    
# ── Test 2: null check should FAIL when null rate exceeds threshold ─────────
def test_null_check_fails(spark, run_meta):
    df = spark.createDataFrame(
        [("biz_001",), (None,)], schema=["business_id"]
    )
    rule = {
        "rule_id": "bus_001",
        "rule_name": "business_id_not_null",
        "rule_type": "null_check",
        "column_name": "business_id",
        "severity": "CRITICAL",
        "dimension": "completeness",
        "fail_cond": F.col("business_id").isNull(), 
        "threshold_rate": 0.0
    }
    result = eval_standard_rule(df, rule, **run_meta)
    assert result["status"] == "FAIL"
    assert result["failed_count"] == 1

# ── Test 3: gate should be BLOCKED when a CRITICAL rule fails ──────────────
def test_gate_blocked_on_critical_fail():
    rule_results = [
        {"status": "FAIL", "severity": "CRITICAL"},
        {"status": "PASS", "severity": "MAJOR"},
    ]
    gate = build_gate_result(
        rule_results, 
        dq_run_id="dq_test",
        pipeline_run_id="pipe_test",
        layer="silver",
        table_name="business_silver",
        run_ts=datetime(2026,1,1)
    )
    assert gate["decision"] == "BLOCKED"

# ── Test 4: gate should be DEGRADED when only MAJOR rules fail ─────────────
def test_gate_degraded_on_major_fail():
    rule_results = [
        {"status": "PASS", "severity": "CRITICAL"},
        {"status": "FAIL", "severity": "MAJOR"},
    ]
    gate = build_gate_result(
        rule_results,
        dq_run_id="dq_test",
        pipeline_run_id="pipe_test",
        layer="silver",
        table_name="business_silver",
        run_ts=datetime(2026,1,1)
    )
    assert gate["decision"] == "DEGRADED"

# ── Test 5: gate should be PASS when all rules pass ────────────────────────
def test_gate_pass_when_all_pass(run_meta):
    rule_results = [
        {"status": "PASS", "severity": "CRITICAL"},
        {"status": "PASS", "severity": "MAJOR"},
    ]
    gate = build_gate_result(
        rule_results,
        dq_run_id="dq_test",
        pipeline_run_id="pipe_test",
        layer="silver",
        table_name="business_silver",
        run_ts=datetime(2026,1,1)
    )
    assert gate["decision"] == "PASS"