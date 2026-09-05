from __future__ import annotations

from collections.abc import Mapping

from ....records import DecisionStatus, ProtectedRootReference, content_sha256
from ..scoring.assessment import CriterionDisposition
from .records import JudgeConfiguration, JudgeQualification


def confusion_total(confusion_matrix: Mapping[str, Mapping[str, Mapping[str, int]]]) -> int:
    return sum(
        count
        for actual in confusion_matrix.values()
        for predicted in actual.values()
        for count in predicted.values()
    )


def validate_qualification_metrics(
    criterion_agreement: Mapping[str, float],
    confusion_matrix: Mapping[str, Mapping[str, Mapping[str, int]]],
    unresolved_count: int,
    schema_failure_count: int,
    agreement_statistic: float | None,
    malformed_output_count: int = 0,
) -> None:
    if any(not 0.0 <= value <= 1.0 for value in criterion_agreement.values()):
        raise ValueError("criterion agreement must be within [0, 1]")
    if unresolved_count < 0 or schema_failure_count < 0 or malformed_output_count < 0:
        raise ValueError("qualification failure counts cannot be negative")
    if agreement_statistic is not None and not -1.0 <= agreement_statistic <= 1.0:
        raise ValueError("agreement statistic must be within [-1, 1]")
    dispositions = {item.value for item in CriterionDisposition}
    for actual_by_criterion in confusion_matrix.values():
        for actual, predicted in actual_by_criterion.items():
            if actual not in dispositions:
                raise ValueError("confusion matrix contains an unknown disposition")
            for predicted_value, count in predicted.items():
                if predicted_value not in dispositions:
                    raise ValueError("confusion matrix contains an unknown disposition")
                if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                    raise ValueError("confusion matrix counts must be non-negative integers")


def thresholds_satisfied(
    configuration: JudgeConfiguration, qualification: JudgeQualification
) -> bool:
    thresholds = configuration.qualification_thresholds
    minimum_agreement = thresholds.minimum_criterion_agreement
    maximum_unresolved = thresholds.maximum_unresolved_rate
    if minimum_agreement is None or maximum_unresolved is None:
        return False
    scoped_criteria = {
        criterion_id for scope in configuration.scopes for criterion_id in scope.criterion_ids
    }
    if not scoped_criteria <= set(qualification.criterion_agreement):
        return False
    if not scoped_criteria <= set(qualification.confusion_matrix):
        return False
    total = confusion_total(qualification.confusion_matrix)
    if total == 0:
        return False
    if any(qualification.criterion_agreement[item] < minimum_agreement for item in scoped_criteria):
        return False
    unresolved_rate = qualification.unresolved_count / total if total else 1.0
    kappa_ok = thresholds.minimum_kappa is None or (
        qualification.agreement_statistic is not None
        and qualification.agreement_statistic >= thresholds.minimum_kappa
    )
    return (
        unresolved_rate <= maximum_unresolved
        and kappa_ok
        and qualification.schema_failure_count == 0
        and qualification.malformed_output_count == 0
    )


def qualification_digest(qualification: JudgeQualification) -> str:
    payload = qualification.model_dump(mode="json", exclude={"content_sha256"})
    root_reference = payload["qualification_root_reference"]
    if isinstance(root_reference, dict):
        root_reference["content_sha256"] = ""
    return content_sha256(payload)


def qualification_id(
    configuration: JudgeConfiguration,
    criterion_agreement: Mapping[str, float],
    confusion_matrix: Mapping[str, Mapping[str, Mapping[str, int]]],
    unresolved_count: int,
    schema_failure_count: int,
    agreement_statistic: float | None,
    fairness_status: DecisionStatus,
    fairness_scope_status: Mapping[str, DecisionStatus],
    *,
    qualification_revision: str,
    qualification_root_reference: ProtectedRootReference,
    qualification_adjudication_ids: tuple[str, ...],
    malformed_output_count: int,
    supersedes_qualification_id: str | None = None,
) -> str:
    root_reference = qualification_root_reference.model_dump(mode="json")
    root_reference["content_sha256"] = ""
    evidence = {
        "judge_config_id": configuration.judge_config_id,
        "judge_config_sha256": configuration.content_sha256,
        "qualification_set_id": configuration.qualification_set_id,
        "qualification_set_sha256": configuration.qualification_set_sha256,
        "criterion_agreement": criterion_agreement,
        "confusion_matrix": confusion_matrix,
        "unresolved_count": unresolved_count,
        "schema_failure_count": schema_failure_count,
        "agreement_statistic": agreement_statistic,
        "fairness_status": fairness_status,
        "fairness_scope_status": fairness_scope_status,
        "qualification_revision": qualification_revision,
        "qualification_root_reference": root_reference,
        "qualification_adjudication_ids": qualification_adjudication_ids,
        "malformed_output_count": malformed_output_count,
        "supersedes_qualification_id": supersedes_qualification_id,
    }
    return f"qualification-{configuration.judge_config_id}-{content_sha256(evidence)[:24]}"


__all__ = [
    "confusion_total",
    "qualification_digest",
    "qualification_id",
    "thresholds_satisfied",
    "validate_qualification_metrics",
]
