from __future__ import annotations

from typing import TYPE_CHECKING

from ....pilot.models import TaskClass
from ..contracts.config import ProtectedSemanticContract
from .assessment import CriterionAssessment
from .kernel_helpers import PrimaryScore, ScoreBlockedError
from .tasks import score_knowledge, score_mixed, score_procedural

if TYPE_CHECKING:
    from ..judge.records import JudgeConfiguration, JudgeQualification


def derive_primary_score(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> PrimaryScore:
    if contract.task_class == TaskClass.KNOWLEDGE:
        return score_knowledge(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
        )
    if contract.task_class == TaskClass.PROCEDURAL:
        return score_procedural(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
        )
    if contract.task_class == TaskClass.MIXED:
        return score_mixed(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
        )
    raise ValueError("unsupported task class")


__all__ = [
    "PrimaryScore",
    "ScoreBlockedError",
    "derive_primary_score",
    "score_knowledge",
    "score_mixed",
    "score_procedural",
]
