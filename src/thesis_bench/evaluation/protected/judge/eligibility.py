from __future__ import annotations

from ....pilot.models import Language, TaskClass
from ....records import DecisionStatus
from ..scoring.assessment import (
    AssessmentSource,
    CriterionAssessment,
    CriterionDisposition,
    QualifiedCriterionAssessment,
)
from .configuration import validate_judge_configuration
from .evidence import (
    qualification_digest,
    qualification_id,
    thresholds_satisfied,
    validate_qualification_metrics,
)
from .records import JudgeConfiguration, JudgeQualification


def validate_judge_qualification(
    configuration: JudgeConfiguration,
    qualification: JudgeQualification,
    *,
    require_primary_eligibility: bool = False,
) -> JudgeQualification:
    configuration = validate_judge_configuration(
        configuration, require_primary_eligibility=require_primary_eligibility
    )
    try:
        qualification = JudgeQualification.model_validate(qualification.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge qualification is invalid") from None
    if qualification.content_sha256 != qualification_digest(qualification):
        raise ValueError("judge qualification hash does not cover its artifact")
    validate_qualification_metrics(
        qualification.criterion_agreement,
        qualification.confusion_matrix,
        qualification.unresolved_count,
        qualification.schema_failure_count,
        qualification.agreement_statistic,
        qualification.malformed_output_count,
    )
    if qualification.judge_config_id != configuration.judge_config_id:
        raise ValueError("judge qualification configuration does not match")
    if qualification.judge_config_sha256 != configuration.content_sha256:
        raise ValueError("judge qualification configuration has changed")
    expected_qualification_id = qualification_id(
        configuration,
        qualification.criterion_agreement,
        qualification.confusion_matrix,
        qualification.unresolved_count,
        qualification.schema_failure_count,
        qualification.agreement_statistic,
        qualification.fairness_status,
        qualification.fairness_scope_status,
        qualification_revision=qualification.qualification_revision,
        qualification_root_reference=qualification.qualification_root_reference,
        qualification_adjudication_ids=qualification.qualification_adjudication_ids,
        malformed_output_count=qualification.malformed_output_count,
        supersedes_qualification_id=qualification.supersedes_qualification_id,
    )
    if qualification.qualification_id != expected_qualification_id:
        raise ValueError("judge qualification identity is not reproducible")
    if (
        qualification.qualification_set_id != configuration.qualification_set_id
        or qualification.qualification_set_sha256 != configuration.qualification_set_sha256
        or qualification.protected_input_contract_id != configuration.protected_input_contract_id
        or qualification.protected_input_contract_sha256
        != configuration.protected_input_contract_sha256
    ):
        raise ValueError("judge qualification protected inputs do not match")
    eligible = (
        qualification.state == "frozen"
        and qualification.status == DecisionStatus.GO
        and qualification.fairness_status == DecisionStatus.GO
        and bool(qualification.fairness_scope_status)
        and all(
            status == DecisionStatus.GO for status in qualification.fairness_scope_status.values()
        )
        and qualification.thresholds_satisfied is thresholds_satisfied(configuration, qualification)
    )
    if require_primary_eligibility and not eligible:
        raise ValueError("judge qualification is not eligible for primary assessment")
    return qualification


def _scope_contains(
    configuration: JudgeConfiguration, task_class: TaskClass, language: Language, criterion_id: str
) -> bool:
    return any(
        scope.task_class == task_class
        and scope.language == language
        and criterion_id in scope.criterion_ids
        for scope in configuration.scopes
    )


def validate_primary_judge_assessment(
    configuration: JudgeConfiguration,
    qualification: JudgeQualification,
    assessment: CriterionAssessment,
    *,
    task_class: TaskClass,
    language: Language,
) -> QualifiedCriterionAssessment:
    qualification = validate_judge_qualification(
        configuration, qualification, require_primary_eligibility=True
    )
    try:
        assessment = type(assessment).model_validate(assessment.model_dump(mode="python"))
    except ValueError:
        raise ValueError("primary semantic assessment is invalid") from None
    if assessment.source != AssessmentSource.QUALIFIED_SEMANTIC_JUDGE:
        raise ValueError("primary semantic assessment requires the qualified judge source")
    if assessment.judge_config_id != configuration.judge_config_id:
        raise ValueError("assessment judge configuration does not match")
    if assessment.disposition == CriterionDisposition.UNRESOLVED:
        raise ValueError("primary semantic assessment is unresolved")
    if not _scope_contains(configuration, task_class, language, assessment.criterion_id):
        raise ValueError("criterion is outside the qualified judge scope")
    if assessment.criterion_id not in qualification.criterion_agreement:
        raise ValueError("criterion lacks qualification evidence")
    if isinstance(assessment, QualifiedCriterionAssessment):
        if (
            assessment.judge_config_sha256 != configuration.content_sha256
            or assessment.qualification_id != qualification.qualification_id
        ):
            raise ValueError("semantic assessment qualification provenance does not match")
    return QualifiedCriterionAssessment(
        schema_version=1,
        assessment_id=assessment.assessment_id,
        criterion_id=assessment.criterion_id,
        disposition=assessment.disposition,
        source=assessment.source,
        assessor_id=assessment.assessor_id,
        judge_config_id=configuration.judge_config_id,
        judge_config_sha256=configuration.content_sha256 or "",
        qualification_id=qualification.qualification_id,
    )


def validate_judge_qualification_successor(
    prior: JudgeQualification, successor: JudgeQualification
) -> JudgeQualification:
    try:
        prior = JudgeQualification.model_validate(prior.model_dump(mode="python"))
        successor = JudgeQualification.model_validate(successor.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge qualification successor is invalid") from None
    if prior.content_sha256 != qualification_digest(prior):
        raise ValueError("prior judge qualification artifact is invalid")
    if successor.qualification_id == prior.qualification_id:
        raise ValueError("judge qualification successor must have a new identity")
    if successor.supersedes_qualification_id != prior.qualification_id:
        raise ValueError("judge qualification successor must identify its predecessor")
    if successor.content_sha256 == prior.content_sha256:
        raise ValueError("judge qualification successor must have a new artifact hash")
    if successor.state != "frozen" or successor.content_sha256 != qualification_digest(successor):
        raise ValueError("judge qualification successor artifact is invalid")
    return successor


__all__ = [
    "validate_judge_qualification",
    "validate_judge_qualification_successor",
    "validate_primary_judge_assessment",
]
