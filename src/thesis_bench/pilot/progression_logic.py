from __future__ import annotations

from ..records import DecisionStatus, ReasonCode
from .progression_models import (
    _PROGRESS_EVIDENCE_FIELDS,
    ProgressCriterion,
    ProgressionReport,
    ProgressObservation,
)


def _status_rank(status: DecisionStatus) -> int:
    return {
        DecisionStatus.GO: 0,
        DecisionStatus.AMEND: 1,
        DecisionStatus.STOP_DEFER: 2,
    }[status]


def derive_progression(
    observations: tuple[ProgressObservation, ...], *, report_id: str = "pilot-progression-1"
) -> ProgressionReport:
    if not observations:
        raise ValueError("progression requires observations")
    if len({observation.criterion for observation in observations}) != len(observations):
        raise ValueError("progression criteria must be unique")
    approved = set(ProgressCriterion)
    present = {observation.criterion for observation in observations}
    if present != approved:
        raise ValueError("progression must include all approved feasibility criteria")
    derived_observations = tuple(
        observation.model_copy(
            update={
                "status": status,
                "reason_codes": reason_codes,
            }
        )
        for observation in observations
        for status, reason_codes in [_derive_observation(observation)]
    )
    status = max((observation.status for observation in derived_observations), key=_status_rank)
    return ProgressionReport(
        schema_version=1,
        report_id=report_id,
        status=status,
        observations=derived_observations,
    )


def _derive_observation(
    observation: ProgressObservation,
) -> tuple[DecisionStatus, tuple[ReasonCode, ...]]:
    reasons = list(observation.reason_codes)
    if any(
        reason
        in {
            ReasonCode.PROTECTED_PAYLOAD,
            ReasonCode.POLICY_VIOLATION,
            ReasonCode.FAMILY_OVERLAP,
            ReasonCode.FINAL_TEST_FORBIDDEN,
            ReasonCode.MISSING_PROVENANCE,
            ReasonCode.SAFETY_FAILURE,
            ReasonCode.PERMISSION_FAILURE,
            ReasonCode.EGRESS_FAILURE,
        }
        for reason in observation.reason_codes
    ):
        return DecisionStatus.STOP_DEFER, tuple(dict.fromkeys(reasons))
    field = _PROGRESS_EVIDENCE_FIELDS[observation.criterion]
    evidence = getattr(observation.evidence, field)
    if observation.criterion == ProgressCriterion.DETERMINISTIC_EVALUATION:
        if not evidence.idempotent:
            reasons.append(ReasonCode.NON_DETERMINISTIC)
            status = DecisionStatus.STOP_DEFER
        else:
            status = DecisionStatus.GO if evidence.agreement >= 1.0 else DecisionStatus.AMEND
    elif observation.criterion == ProgressCriterion.HUMAN_CALIBRATION:
        if evidence.systematic_critical_disagreement:
            reasons.append(ReasonCode.INVALID_CONFIGURATION)
            status = DecisionStatus.STOP_DEFER
        elif evidence.qualification_attempt > 1 and not (
            evidence.alpha >= 0.80
            and evidence.lower_bound >= 0.67
            and evidence.critical_exact_min >= 0.90
        ):
            status = DecisionStatus.STOP_DEFER
        elif evidence.alpha < 0.67:
            status = DecisionStatus.STOP_DEFER
        elif (
            evidence.alpha >= 0.80
            and evidence.lower_bound >= 0.67
            and evidence.critical_exact_min >= 0.90
        ):
            status = DecisionStatus.GO
        else:
            status = DecisionStatus.AMEND
    elif observation.criterion == ProgressCriterion.SOLVABILITY:
        if not evidence.complete_evidence_mapping:
            reasons.append(ReasonCode.MISSING_PROVENANCE)
            status = DecisionStatus.STOP_DEFER
        elif evidence.solvable_rate >= 0.90:
            status = DecisionStatus.GO
        elif evidence.solvable_rate >= 0.80:
            status = DecisionStatus.AMEND
        else:
            status = DecisionStatus.STOP_DEFER
    elif observation.criterion == ProgressCriterion.HEADROOM:
        complete = all(stratum.has_success and stratum.has_failure for stratum in evidence.strata)
        in_band = all(0.20 <= stratum.success_rate <= 0.80 for stratum in evidence.strata)
        if evidence.construct_mismatch:
            reasons.append(ReasonCode.INVALID_CONFIGURATION)
            status = DecisionStatus.STOP_DEFER
        else:
            status = DecisionStatus.GO if complete and in_band else DecisionStatus.AMEND
    elif observation.criterion == ProgressCriterion.INVALIDITY:
        if evidence.invalidity_rate <= 0.05:
            status = DecisionStatus.GO
        elif evidence.invalidity_rate <= 0.10:
            status = DecisionStatus.AMEND
        else:
            status = DecisionStatus.STOP_DEFER
    elif observation.criterion == ProgressCriterion.CONTAMINATION:
        if evidence.direct_match:
            reasons.append(ReasonCode.PROTECTED_PAYLOAD)
            status = DecisionStatus.STOP_DEFER
        else:
            status = DecisionStatus.AMEND if evidence.pending_semantic_match else DecisionStatus.GO
    elif observation.criterion == ProgressCriterion.KIND:
        if not evidence.isolation_safe:
            reasons.append(ReasonCode.SAFETY_FAILURE)
            status = DecisionStatus.STOP_DEFER
        elif not evidence.privilege_safe:
            reasons.append(ReasonCode.PERMISSION_FAILURE)
            status = DecisionStatus.STOP_DEFER
        elif not evidence.egress_safe:
            reasons.append(ReasonCode.EGRESS_FAILURE)
            status = DecisionStatus.STOP_DEFER
        elif not evidence.permission_safe:
            reasons.append(ReasonCode.PERMISSION_FAILURE)
            status = DecisionStatus.STOP_DEFER
        else:
            status = DecisionStatus.GO
    elif observation.criterion == ProgressCriterion.W1:
        if not evidence.provenance_complete:
            reasons.append(ReasonCode.MISSING_PROVENANCE)
            status = DecisionStatus.STOP_DEFER
        elif not evidence.access_safe or not evidence.redirects_safe:
            reasons.append(ReasonCode.POLICY_VIOLATION)
            status = DecisionStatus.STOP_DEFER
        else:
            status = DecisionStatus.GO if evidence.completion_rate >= 0.90 else DecisionStatus.AMEND
    elif observation.criterion == ProgressCriterion.FAIRNESS:
        if (
            evidence.hidden_information
            or evidence.unequal_permissions
            or evidence.uncaptured_mutation
        ):
            reasons.append(ReasonCode.POLICY_VIOLATION)
            status = DecisionStatus.STOP_DEFER
        else:
            status = (
                DecisionStatus.GO
                if evidence.provenance_complete and evidence.matched_permissions
                else DecisionStatus.AMEND
            )
    else:
        status = DecisionStatus.GO if evidence.feasible else DecisionStatus.AMEND
    return status, tuple(dict.fromkeys(reasons))


def _derive_observation_status(observation: ProgressObservation) -> DecisionStatus:
    """Compatibility helper for callers that only need the derived status."""
    return _derive_observation(observation)[0]
