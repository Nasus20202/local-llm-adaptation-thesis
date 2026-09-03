from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import model_validator
from pydantic.types import StrictBool, StrictInt

from ..records import ReasonCode, VersionedRecord


class InvalidityClassification(VersionedRecord):
    reason_code: ReasonCode
    valid: StrictBool
    outcome: Literal["failure", "invalid"]

    @model_validator(mode="after")
    def require_frozen_classification(self) -> InvalidityClassification:
        if self.reason_code.value not in _VALID_FAILURES | _INVALID_REASONS:
            raise ValueError("unknown frozen invalidity reason")
        expected_valid = self.reason_code.value in _VALID_FAILURES
        expected_outcome = "failure" if expected_valid else "invalid"
        if self.valid != expected_valid or self.outcome != expected_outcome:
            raise ValueError("invalidity classification does not match frozen reason")
        return self


_VALID_FAILURES = {
    "wrong_answer",
    "refusal",
    "malformed_answer",
    "budget_exhausted",
    "evaluated_system_timeout",
    "remediation_failed",
    "runtime_failure",
}

_INVALID_REASONS = {
    "capture_hash_mismatch",
    "missing_provenance",
    "infrastructure_failure",
    "evaluator_infrastructure_failure",
    "hardware_measurement_failure",
}


def classify_invalidity(reason_code: str) -> InvalidityClassification:
    if reason_code in _VALID_FAILURES:
        valid = True
    elif reason_code in _INVALID_REASONS:
        valid = False
    else:
        raise ValueError("unknown frozen invalidity reason")
    return InvalidityClassification(
        schema_version=1,
        reason_code=ReasonCode(reason_code),
        valid=valid,
        outcome="failure" if valid else "invalid",
    )


class SensitivityInputs(VersionedRecord):
    complete_case_count: StrictInt
    all_fail_successes: StrictInt
    observed_successes: StrictInt
    total_count: StrictInt


def sensitivity_inputs(
    validity_flags: Sequence[bool], success_flags: Sequence[bool] | None = None
) -> SensitivityInputs:
    if success_flags is None:
        success_flags = (False,) * len(validity_flags)
    if len(validity_flags) != len(success_flags):
        raise ValueError("validity and success inputs must be aligned")
    complete = sum(validity_flags)
    return SensitivityInputs(
        schema_version=1,
        complete_case_count=complete,
        all_fail_successes=sum(
            success for valid, success in zip(validity_flags, success_flags, strict=True) if valid
        ),
        observed_successes=sum(success_flags),
        total_count=len(validity_flags),
    )
