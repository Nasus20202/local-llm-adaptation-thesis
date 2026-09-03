from __future__ import annotations

from collections.abc import Sequence

from pydantic import Field
from pydantic.types import StrictFloat

from ..records import DecisionStatus, ReasonCode, VersionedRecord


class W1FeasibilityReport(VersionedRecord):
    status: DecisionStatus
    completion_rate: StrictFloat
    reason_codes: tuple[ReasonCode, ...] = Field(min_length=1)


def qualify_w1(
    *,
    eligible_attempts: Sequence[bool],
    complete_provenance: Sequence[bool],
    deny_fixture_safe: Sequence[bool],
    redirects_safe: Sequence[bool],
    within_budget: Sequence[bool],
) -> W1FeasibilityReport:
    sequences = (
        eligible_attempts,
        complete_provenance,
        deny_fixture_safe,
        redirects_safe,
        within_budget,
    )
    if len({len(sequence) for sequence in sequences}) != 1:
        raise ValueError("W1 qualification inputs must be aligned")
    eligible_indices = tuple(index for index, eligible in enumerate(eligible_attempts) if eligible)
    count = len(eligible_indices)
    if count == 0:
        raise ValueError("W1 qualification requires eligible attempts")
    rate = sum(within_budget[index] for index in eligible_indices) / count
    reasons: list[ReasonCode] = []
    status = DecisionStatus.GO
    if not all(complete_provenance[index] for index in eligible_indices):
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.INFRASTRUCTURE_FAILURE)
    if not all(deny_fixture_safe[index] for index in eligible_indices):
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.POLICY_VIOLATION)
    if not all(redirects_safe[index] for index in eligible_indices):
        status = DecisionStatus.STOP_DEFER
        reasons.append(ReasonCode.POLICY_VIOLATION)
    if rate < 0.9 and status != DecisionStatus.STOP_DEFER:
        status = DecisionStatus.AMEND
        reasons.append(ReasonCode.PROVIDER_UNAVAILABLE)
    if not reasons:
        reasons.append(ReasonCode.OK)
    return W1FeasibilityReport(
        schema_version=1,
        status=status,
        completion_rate=rate,
        reason_codes=tuple(dict.fromkeys(reasons)),
    )
