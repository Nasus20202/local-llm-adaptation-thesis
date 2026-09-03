from __future__ import annotations

import statistics
from collections.abc import Sequence

from pydantic import Field
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ..records import DecisionStatus, ReasonCode, VersionedRecord
from ..schemas import NonBlankStr
from .models import ClusterPolicy


class PolicyComparison(VersionedRecord):
    valid: StrictBool
    differences: tuple[NonBlankStr, ...] = ()


def compare_neutral_policies(policies: Sequence[ClusterPolicy]) -> PolicyComparison:
    if len(policies) < 2:
        raise ValueError("policy comparison requires two conditions")
    reference = policies[0]
    fields = (
        "namespace",
        "allowed_commands",
        "allowed_permissions",
        "allowed_observations",
        "context_budget",
        "max_actions",
        "max_output_bytes",
        "max_duration_seconds",
        "allow_privileged",
        "allow_host_mounts",
        "allow_cluster_scope",
        "allow_egress",
    )
    differences = tuple(
        field
        for field in fields
        if any(getattr(policy, field) != getattr(reference, field) for policy in policies[1:])
    )
    return PolicyComparison(schema_version=1, valid=not differences, differences=differences)


class ClusterQualification(VersionedRecord):
    status: DecisionStatus
    reason_codes: tuple[ReasonCode, ...] = Field(min_length=1)
    reset_count: StrictInt
    deny_probe_count: StrictInt
    median_reset_seconds: StrictFloat
    median_reset_validation_seconds: StrictFloat
    max_attempt_seconds: StrictFloat


def qualify_cluster(
    *,
    reset_hashes: Sequence[str],
    reset_validator_results: Sequence[str],
    egress_denials: Sequence[bool],
    permission_checks: Sequence[bool],
    validator_status: DecisionStatus,
    matched_access: bool,
    paired_variants: bool,
    reset_durations_seconds: Sequence[float],
    reset_validation_durations_seconds: Sequence[float],
    attempt_durations_seconds: Sequence[float],
) -> ClusterQualification:
    reasons: list[ReasonCode] = []
    status = DecisionStatus.GO
    if len(reset_hashes) != 10 or len(reset_validator_results) != 10:
        status = DecisionStatus.AMEND
        reasons.append(ReasonCode.INFRASTRUCTURE_FAILURE)
    if len(reset_hashes) == 10 and len(set(reset_hashes)) != 1:
        status = DecisionStatus.AMEND
        reasons.append(ReasonCode.INFRASTRUCTURE_FAILURE)
    if len(reset_validator_results) == 10 and len(set(reset_validator_results)) != 1:
        status = DecisionStatus.AMEND
        reasons.append(ReasonCode.INFRASTRUCTURE_FAILURE)
    if len(egress_denials) != 10 or not all(egress_denials):
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.EGRESS_FAILURE)
    if not permission_checks or not all(permission_checks):
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.PERMISSION_FAILURE)
    if validator_status != DecisionStatus.GO:
        status = max(
            (status, validator_status),
            key=lambda item: {
                DecisionStatus.GO: 0,
                DecisionStatus.AMEND: 1,
                DecisionStatus.STOP_DEFER: 2,
            }[item],
        )
        reasons.append(ReasonCode.INVALID_CONFIGURATION)
    if not matched_access:
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.POLICY_VIOLATION)
    if not paired_variants:
        status = DecisionStatus.AMEND
        reasons.append(ReasonCode.INVALID_CONFIGURATION)
    median_duration = (
        statistics.median(reset_durations_seconds) if reset_durations_seconds else float("inf")
    )
    median_reset_validation = (
        statistics.median(reset_validation_durations_seconds)
        if reset_validation_durations_seconds
        else float("inf")
    )
    max_duration = max(attempt_durations_seconds, default=float("inf"))
    if median_reset_validation > 180 or max_duration > 300:
        if status != DecisionStatus.STOP_DEFER:
            status = DecisionStatus.AMEND
        reasons.append(ReasonCode.TIMEOUT)
    if not reasons:
        reasons.append(ReasonCode.OK)
    return ClusterQualification(
        schema_version=1,
        status=status,
        reason_codes=tuple(dict.fromkeys(reasons)),
        reset_count=len(reset_hashes),
        deny_probe_count=len(egress_denials),
        median_reset_seconds=median_duration,
        median_reset_validation_seconds=median_reset_validation,
        max_attempt_seconds=max_duration,
    )
