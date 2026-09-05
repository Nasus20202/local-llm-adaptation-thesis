from __future__ import annotations

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
    from ...judge.records import JudgeConfiguration, JudgeQualification


def score_knowledge(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
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
    )
    true_positives = sum(
        assessment_map[item].disposition == CriterionDisposition.SATISFIED
        for item in configuration.required_criterion_ids
    )
    false_negatives = sum(
        assessment_map[item].disposition
        in {CriterionDisposition.NOT_SATISFIED, CriterionDisposition.CONTRADICTED}
        for item in configuration.required_criterion_ids
    )
    false_positives = sum(
        assessment_map[item].disposition
        in {CriterionDisposition.SATISFIED, CriterionDisposition.CONTRADICTED}
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
