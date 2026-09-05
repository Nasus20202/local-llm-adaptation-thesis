from __future__ import annotations

from collections.abc import Iterable

from ....records import DecisionStatus, ProtectedRootReference
from ..scoring.assessment import AssessmentSource
from .configuration import validate_judge_configuration
from .evidence import (
    confusion_total,
    qualification_digest,
    qualification_id,
    validate_qualification_metrics,
)
from .fairness import check_copying_neutral_fairness
from .records import (
    JudgeConfiguration,
    JudgeFairnessCase,
    JudgeQualification,
    QualificationAdjudicationBinding,
)


def qualify_judge_configuration(
    configuration: JudgeConfiguration,
    *,
    criterion_agreement: dict[str, float],
    confusion_matrix: dict[str, dict[str, dict[str, int]]],
    unresolved_count: int,
    schema_failure_count: int,
    fairness_cases: Iterable[JudgeFairnessCase],
    agreement_statistic: float | None = None,
    qualification_revision: str,
    qualification_root_reference: ProtectedRootReference,
    qualification_adjudications: tuple[QualificationAdjudicationBinding, ...] = (),
    malformed_output_count: int = 0,
    supersedes_qualification_id: str | None = None,
) -> JudgeQualification:
    configuration = validate_judge_configuration(configuration, require_primary_eligibility=True)
    validate_qualification_metrics(
        criterion_agreement,
        confusion_matrix,
        unresolved_count,
        schema_failure_count,
        agreement_statistic,
        malformed_output_count,
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
        and {criterion_id for scope in configuration.scopes for criterion_id in scope.criterion_ids}
        <= {rule_id for case in cases for rule_id in case.exercised_rule_ids()}
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
        criterion_ok
        and evidence_ok
        and unresolved_ok
        and kappa_ok
        and schema_failure_count == 0
        and malformed_output_count == 0
    )
    fairness_scope_status = {
        case.scope_key: result.status for case, result in zip(cases, fairness, strict=True)
    }
    qualification_id_value = qualification_id(
        configuration,
        criterion_agreement,
        confusion_matrix,
        unresolved_count,
        schema_failure_count,
        agreement_statistic,
        fairness_status,
        fairness_scope_status,
        qualification_revision=qualification_revision,
        qualification_root_reference=qualification_root_reference,
        qualification_adjudications=qualification_adjudications,
        malformed_output_count=malformed_output_count,
        supersedes_qualification_id=supersedes_qualification_id,
    )
    candidate = JudgeQualification.model_construct(
        schema_version=1,
        qualification_id=qualification_id_value,
        judge_config_id=configuration.judge_config_id,
        judge_config_sha256=configuration_hash,
        qualification_set_id=configuration.qualification_set_id,
        qualification_set_sha256=configuration.qualification_set_sha256,
        protected_input_contract_id=configuration.protected_input_contract_id,
        protected_input_contract_sha256=configuration.protected_input_contract_sha256,
        qualification_revision=qualification_revision,
        qualification_root_reference=qualification_root_reference,
        qualification_adjudications=qualification_adjudications,
        malformed_output_count=malformed_output_count,
        state="frozen",
        content_sha256="0" * 64,
        supersedes_qualification_id=supersedes_qualification_id,
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
    digest = qualification_digest(candidate)
    bound_root_reference = qualification_root_reference.model_copy(
        update={"content_sha256": digest}
    )
    candidate = candidate.model_copy(update={"qualification_root_reference": bound_root_reference})
    return JudgeQualification.model_validate({**candidate.model_dump(), "content_sha256": digest})


__all__ = ["qualify_judge_configuration"]
