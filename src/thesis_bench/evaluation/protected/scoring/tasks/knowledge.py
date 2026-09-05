from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from .....pilot.models import TaskClass
from ...contracts.config import KnowledgeScoreConfiguration, ProtectedSemanticContract
from ..assessment import CriterionAssessment, CriterionDisposition
from ..kernel_helpers import (
    PrimaryScore,
    _assessment_map,
    _require_resolved,
    _require_scoreable_contract,
)

if TYPE_CHECKING:
    from ....calibration import CalibrationSummary
    from ....rubrics import AdjudicationRecord
    from ...judge.records import AuditPolicy, JudgeConfiguration, JudgeQualification
    from ..assessment import AuditSelection


def score_knowledge(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
    human_calibration: CalibrationSummary | None = None,
    human_adjudications: dict[str, AdjudicationRecord] | None = None,
    human_audit_selection: AuditSelection | None = None,
    human_audit_policy: AuditPolicy | None = None,
    response_id: str | None = None,
) -> PrimaryScore:
    _require_scoreable_contract(contract)
    configuration = contract.score_configuration
    if contract.task_class != TaskClass.KNOWLEDGE or not isinstance(
        configuration, KnowledgeScoreConfiguration
    ):
        raise ValueError("knowledge scoring requires a knowledge contract")
    assessment_map = _assessment_map(contract, assessments)
    required_ids = set(configuration.required_criterion_ids) | set(
        configuration.unsupported_criterion_ids
    )
    _require_resolved(
        contract,
        assessment_map,
        required_ids,
        judge_configuration=judge_configuration,
        judge_qualification=judge_qualification,
        human_calibration=human_calibration,
        human_adjudications=human_adjudications,
        human_audit_selection=human_audit_selection,
        human_audit_policy=human_audit_policy,
        response_id=response_id,
    )
    return _score_knowledge_dispositions(
        contract,
        {criterion_id: item.disposition for criterion_id, item in assessment_map.items()},
    )


def _score_knowledge_dispositions(
    contract: ProtectedSemanticContract,
    dispositions: Mapping[str, CriterionDisposition],
) -> PrimaryScore:
    configuration = contract.score_configuration
    if not isinstance(configuration, KnowledgeScoreConfiguration):
        raise ValueError("knowledge scoring requires a knowledge configuration")
    true_positives = sum(
        dispositions[item] == CriterionDisposition.SATISFIED
        for item in configuration.required_criterion_ids
    )
    false_negatives = sum(
        dispositions[item]
        in {CriterionDisposition.NOT_SATISFIED, CriterionDisposition.CONTRADICTED}
        for item in configuration.required_criterion_ids
    )
    false_positives = sum(
        dispositions[item] in {CriterionDisposition.SATISFIED, CriterionDisposition.CONTRADICTED}
        for item in configuration.unsupported_criterion_ids
    )
    denominator = 2 * true_positives + false_positives + false_negatives
    return PrimaryScore(
        schema_version=1,
        task_class=TaskClass.KNOWLEDGE,
        score=(2 * true_positives / denominator) if denominator else 0.0,
        true_positives=true_positives,
        false_positives=false_positives,
        false_negatives=false_negatives,
    )


__all__ = ["score_knowledge"]
