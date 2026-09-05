from __future__ import annotations

from collections.abc import Iterable

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
    confusion_total,
    qualification_id,
    thresholds_satisfied,
    validate_qualification_metrics,
)
from .fairness import check_copying_neutral_fairness
from .records import JudgeConfiguration, JudgeFairnessCase, JudgeQualification


def qualify_judge_configuration(
    configuration: JudgeConfiguration,
    *,
    criterion_agreement: dict[str, float],
    confusion_matrix: dict[str, dict[str, dict[str, int]]],
    unresolved_count: int,
    schema_failure_count: int,
    fairness_cases: Iterable[JudgeFairnessCase],
    agreement_statistic: float | None = None,
) -> JudgeQualification:
    configuration = validate_judge_configuration(configuration, require_primary_eligibility=True)
    validate_qualification_metrics(
        criterion_agreement,
        confusion_matrix,
        unresolved_count,
        schema_failure_count,
        agreement_statistic,
    )
    cases = tuple(fairness_cases)
    if any(
        assessment.source != AssessmentSource.QUALIFIED_SEMANTIC_JUDGE
        or assessment.judge_config_id != configuration.judge_config_id
        for case in cases
        for assessments in case.variants.values()
        for assessment in assessments
    ):
        raise ValueError("fairness evidence is not bound to the configured judge")
    fairness = tuple(check_copying_neutral_fairness(case) for case in cases)
    scope_pairs = {(scope.task_class, scope.language) for scope in configuration.scopes}
    case_pairs = {(case.contract.task_class, case.contract.language) for case in cases}
    fairness_complete = (
        bool(fairness)
        and len({case.scope_key for case in cases}) == len(cases)
        and scope_pairs <= case_pairs
    )
    fairness_status = (
        DecisionStatus.GO
        if fairness_complete and all(item.status == DecisionStatus.GO for item in fairness)
        else DecisionStatus.AMEND
    )
    thresholds = configuration.qualification_thresholds
    minimum_agreement = thresholds.minimum_criterion_agreement
    maximum_unresolved = thresholds.maximum_unresolved_rate
    configuration_hash = configuration.content_sha256
    if minimum_agreement is None or maximum_unresolved is None or configuration_hash is None:
        raise ValueError("judge qualification threshold configuration is deferred")
    total = confusion_total(confusion_matrix)
    unresolved_rate = unresolved_count / total if total else 1.0
    scoped_criteria = {
        criterion_id for scope in configuration.scopes for criterion_id in scope.criterion_ids
    }
    criterion_ok = (
        scoped_criteria <= set(criterion_agreement)
        and all(criterion_agreement[item] >= minimum_agreement for item in scoped_criteria)
        and scoped_criteria <= set(confusion_matrix)
    )
    unresolved_ok = unresolved_rate <= maximum_unresolved
    evidence_ok = total > 0
    kappa_ok = thresholds.minimum_kappa is None or (
        agreement_statistic is not None and agreement_statistic >= thresholds.minimum_kappa
    )
    threshold_ok = (
        criterion_ok and evidence_ok and unresolved_ok and kappa_ok and schema_failure_count == 0
    )
    fairness_scope_status = {
        case.scope_key: result.status for case, result in zip(cases, fairness, strict=True)
    }
    return JudgeQualification(
        schema_version=1,
        qualification_id=qualification_id(
            configuration,
            criterion_agreement,
            confusion_matrix,
            unresolved_count,
            schema_failure_count,
            agreement_statistic,
            fairness_status,
            fairness_scope_status,
        ),
        judge_config_id=configuration.judge_config_id,
        judge_config_sha256=configuration_hash,
        qualification_set_id=configuration.qualification_set_id,
        qualification_set_sha256=configuration.qualification_set_sha256,
        protected_input_contract_id=configuration.protected_input_contract_id,
        protected_input_contract_sha256=configuration.protected_input_contract_sha256,
        criterion_agreement=criterion_agreement,
        confusion_matrix=confusion_matrix,
        agreement_statistic=agreement_statistic,
        unresolved_count=unresolved_count,
        schema_failure_count=schema_failure_count,
        fairness_status=fairness_status,
        fairness_scope_status=fairness_scope_status,
        thresholds_satisfied=threshold_ok,
        status=DecisionStatus.GO
        if threshold_ok and fairness_status == DecisionStatus.GO
        else DecisionStatus.AMEND,
    )


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
    configuration = validate_judge_configuration(configuration, require_primary_eligibility=True)
    try:
        qualification = JudgeQualification.model_validate(qualification.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge qualification is invalid") from None
    validate_qualification_metrics(
        qualification.criterion_agreement,
        qualification.confusion_matrix,
        qualification.unresolved_count,
        qualification.schema_failure_count,
        qualification.agreement_statistic,
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
    )
    if (
        qualification.status != DecisionStatus.GO
        or qualification.fairness_status != DecisionStatus.GO
        or not qualification.fairness_scope_status
        or any(
            status != DecisionStatus.GO for status in qualification.fairness_scope_status.values()
        )
        or qualification.thresholds_satisfied
        is not thresholds_satisfied(configuration, qualification)
        or qualification.qualification_id != expected_qualification_id
    ):
        raise ValueError("judge qualification is not eligible for primary assessment")
    if (
        qualification.qualification_set_id != configuration.qualification_set_id
        or qualification.qualification_set_sha256 != configuration.qualification_set_sha256
        or qualification.protected_input_contract_id != configuration.protected_input_contract_id
        or qualification.protected_input_contract_sha256
        != configuration.protected_input_contract_sha256
    ):
        raise ValueError("judge qualification protected inputs do not match")
    try:
        assessment_type = (
            QualifiedCriterionAssessment
            if isinstance(assessment, QualifiedCriterionAssessment)
            else CriterionAssessment
        )
        assessment = assessment_type.model_validate(assessment.model_dump(mode="python"))
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


__all__ = ["qualify_judge_configuration", "validate_primary_judge_assessment"]
