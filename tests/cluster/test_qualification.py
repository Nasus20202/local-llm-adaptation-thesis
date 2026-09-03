from __future__ import annotations

from thesis_bench.cluster import (
    qualify_cluster,
    real_kind_qualification_help,
)
from thesis_bench.records import DecisionStatus, ReasonCode


def test_isolation_failure_is_stop_defer_and_real_kind_is_help_only_by_default() -> None:
    report = qualify_cluster(
        reset_hashes=("h" * 64,) * 10,
        reset_validator_results=("ok",) * 10,
        egress_denials=(False,) * 10,
        permission_checks=(True,),
        validator_status=DecisionStatus.GO,
        matched_access=True,
        paired_variants=True,
        reset_durations_seconds=(10.0,) * 10,
        reset_validation_durations_seconds=(12.0,) * 10,
        attempt_durations_seconds=(30.0,) * 10,
    )
    assert report.status == DecisionStatus.STOP_DEFER
    assert ReasonCode.EGRESS_FAILURE in report.reason_codes
    help_record = real_kind_qualification_help()
    assert help_record.status == "not_exposed"
