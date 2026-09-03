from __future__ import annotations

import pytest

from thesis_bench.evaluation import (
    CalibrationStatus,
    InvalidityClassification,
    JudgePolicy,
    classify_invalidity,
    sensitivity_inputs,
    validate_judge_policy,
)


def test_invalidity_keeps_evaluated_system_failures_valid_and_supports_sensitivity_inputs() -> None:
    assert classify_invalidity("malformed_answer").valid is True
    assert classify_invalidity("evaluated_system_timeout").valid is True
    assert classify_invalidity("capture_hash_mismatch").valid is False
    inputs = sensitivity_inputs((True, False, True), success_flags=(True, True, False))
    assert inputs.complete_case_count == 2
    assert inputs.all_fail_successes == 1
    assert inputs.observed_successes == 2
    with pytest.raises(ValueError):
        InvalidityClassification(
            schema_version=1,
            reason_code="unknown-reason",
            valid=True,
            outcome="failure",
        )


def test_supplemental_judge_must_be_frozen_qualified_and_non_primary() -> None:
    with pytest.raises(ValueError):
        validate_judge_policy(
            JudgePolicy(
                schema_version=1,
                judge_id="judge-1",
                model_revision="model-v1",
                prompt_revision="prompt-v1",
                languages=("en",),
                calibrated=False,
                primary=True,
            )
        )
    accepted = validate_judge_policy(
        JudgePolicy(
            schema_version=1,
            judge_id="judge-2",
            model_revision="model-v1",
            prompt_revision="prompt-v1",
            languages=("en", "pl"),
            calibrated=True,
            primary=False,
        )
    )
    assert accepted.status == CalibrationStatus.GO
