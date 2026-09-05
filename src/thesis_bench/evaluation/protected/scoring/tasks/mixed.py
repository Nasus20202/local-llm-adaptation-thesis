from __future__ import annotations

from typing import TYPE_CHECKING

from .....pilot.models import TaskClass
from ...contracts.config import MixedScoreConfiguration, ProtectedSemanticContract
from ...contracts.records import CriterionRole
from ..assessment import CriterionAssessment, CriterionDisposition
from ..kernel_helpers import (
    PrimaryScore,
    _assessment_map,
    _require_resolved,
    _require_scoreable_contract,
)

if TYPE_CHECKING:
    from ...judge.records import JudgeConfiguration, JudgeQualification


def score_mixed(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> PrimaryScore:
    _require_scoreable_contract(contract)
    configuration = contract.score_configuration
    if contract.task_class != TaskClass.MIXED or not isinstance(
        configuration, MixedScoreConfiguration
    ):
        raise ValueError("mixed scoring requires a mixed contract")
    assessment_map = _assessment_map(contract, assessments)
    prohibited_ids = {
        criterion.criterion_id
        for criterion in contract.criteria
        if CriterionRole.PRIMARY_PROHIBITED in criterion.roles
    }
    required_ids = (
        set(configuration.primary_hard_gate_criterion_ids)
        | set(configuration.point_table)
        | prohibited_ids
    )
    _require_resolved(
        contract,
        assessment_map,
        required_ids,
        judge_configuration=judge_configuration,
        judge_qualification=judge_qualification,
    )
    hard_gate_failed = any(
        assessment_map[item].disposition != CriterionDisposition.SATISFIED
        for item in configuration.primary_hard_gate_criterion_ids
    ) or any(
        assessment_map[item].disposition != CriterionDisposition.NOT_SATISFIED
        for item in prohibited_ids
    )
    if hard_gate_failed:
        return PrimaryScore(
            schema_version=1, task_class=TaskClass.MIXED, score=0.0, hard_gate_failed=True
        )
    points = sum(
        value
        for item, value in configuration.point_table.items()
        if assessment_map[item].disposition == CriterionDisposition.SATISFIED
    )
    score = points / configuration.positive_maximum
    if not 0.0 <= score <= 1.0:
        raise ValueError("mixed score is outside its frozen normalizer")
    return PrimaryScore(schema_version=1, task_class=TaskClass.MIXED, score=score)


__all__ = ["score_mixed"]
