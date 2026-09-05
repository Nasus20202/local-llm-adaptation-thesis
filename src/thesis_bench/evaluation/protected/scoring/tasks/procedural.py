from __future__ import annotations

from typing import TYPE_CHECKING

from .....pilot.models import TaskClass
from ...contracts.config import ProceduralScoreConfiguration, ProtectedSemanticContract
from ..assessment import CriterionAssessment, CriterionDisposition
from ..kernel_helpers import (
    PrimaryScore,
    _assessment_map,
    _require_resolved,
    _require_scoreable_contract,
)

if TYPE_CHECKING:
    from ...judge.records import JudgeConfiguration, JudgeQualification


def score_procedural(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> PrimaryScore:
    _require_scoreable_contract(contract)
    configuration = contract.score_configuration
    if contract.task_class != TaskClass.PROCEDURAL or not isinstance(
        configuration, ProceduralScoreConfiguration
    ):
        raise ValueError("procedural scoring requires a procedural contract")
    assessment_map = _assessment_map(contract, assessments)
    required_ids = set(configuration.primary_required_criterion_ids) | set(
        configuration.primary_prohibited_criterion_ids
    )
    _require_resolved(
        contract,
        assessment_map,
        required_ids,
        judge_configuration=judge_configuration,
        judge_qualification=judge_qualification,
    )
    success = all(
        assessment_map[item].disposition == CriterionDisposition.SATISFIED
        for item in configuration.primary_required_criterion_ids
    ) and all(
        assessment_map[item].disposition == CriterionDisposition.NOT_SATISFIED
        for item in configuration.primary_prohibited_criterion_ids
    )
    return PrimaryScore(
        schema_version=1,
        task_class=TaskClass.PROCEDURAL,
        score=1.0 if success else 0.0,
        success=success,
    )


__all__ = ["score_procedural"]
