from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ....pilot.models import TaskClass
from ....records import ReasonCode, VersionedRecord
from ..contracts.config import ProtectedSemanticContract
from ..contracts.records import CriterionRole
from ..contracts.validation import validate_protected_contract
from .assessment import (
    AssessmentSource,
    CalibratedHumanCriterionAssessment,
    CriterionAssessment,
    CriterionDisposition,
    QualifiedCriterionAssessment,
)

if TYPE_CHECKING:
    from ..judge.records import JudgeConfiguration, JudgeQualification


class PrimaryScore(VersionedRecord):
    task_class: TaskClass
    score: StrictFloat = Field(ge=0.0, le=1.0)
    resolved: StrictBool = True
    true_positives: StrictInt | None = None
    false_positives: StrictInt | None = None
    false_negatives: StrictInt | None = None
    success: StrictBool | None = None
    hard_gate_failed: StrictBool = False


class ScoreBlockedError(ValueError):
    reason_code = ReasonCode.UNRESOLVED_CRITERION

    def __init__(self) -> None:
        super().__init__("primary score is blocked by an unresolved criterion")


def _require_scoreable_contract(contract: ProtectedSemanticContract) -> None:
    try:
        validate_protected_contract(contract, require_frozen=True)
    except ValueError as exc:
        raise ValueError("score contract is invalid") from exc


def _assessment_map(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
) -> dict[str, CriterionAssessment]:
    known = {criterion.criterion_id for criterion in contract.criteria}
    result: dict[str, CriterionAssessment] = {}
    for assessment in assessments:
        if assessment.criterion_id not in known:
            raise ValueError("assessment references an unknown criterion")
        if assessment.criterion_id in result:
            raise ValueError("duplicate criterion assessment")
        result[assessment.criterion_id] = assessment
    return result


def _require_resolved(
    contract: ProtectedSemanticContract,
    assessments: dict[str, CriterionAssessment],
    required_ids: set[str],
    *,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> None:
    criteria = {criterion.criterion_id: criterion for criterion in contract.criteria}
    for criterion_id in required_ids:
        assessment = assessments.get(criterion_id)
        if assessment is None:
            raise ValueError("missing primary criterion assessment")
        if assessment.disposition == CriterionDisposition.UNRESOLVED:
            raise ScoreBlockedError()
        criterion = criteria[criterion_id]
        if assessment.source == AssessmentSource.QUALIFIED_SEMANTIC_JUDGE and not isinstance(
            assessment, QualifiedCriterionAssessment
        ):
            raise ValueError("semantic judge assessment is not qualified for primary scoring")
        if (
            CriterionRole.DETERMINISTIC in criterion.roles
            and CriterionRole.SEMANTIC not in criterion.roles
            and assessment.source != AssessmentSource.DETERMINISTIC
        ):
            raise ValueError("deterministic criterion cannot use a semantic assessor")
        if (
            CriterionRole.DETERMINISTIC in criterion.roles
            and assessment.source == AssessmentSource.DETERMINISTIC
            and (assessment.predicate_id is None or assessment.predicate_version is None)
        ):
            raise ValueError("deterministic predicate binding is required")
        if assessment.source == AssessmentSource.DETERMINISTIC:
            if CriterionRole.DETERMINISTIC not in criterion.roles:
                raise ValueError("deterministic assessment requires a declared predicate")
            predicate = next(
                item for item in contract.predicates if item.criterion_id == criterion_id
            )
            if (
                assessment.predicate_id != predicate.predicate_id
                or assessment.predicate_version != predicate.predicate_version
            ):
                raise ValueError("deterministic assessment predicate binding is invalid")
        if assessment.source == AssessmentSource.QUALIFIED_SEMANTIC_JUDGE:
            if judge_configuration is None or judge_qualification is None:
                raise ValueError("judge qualification context is required for primary scoring")
            from ..judge.eligibility import validate_primary_judge_assessment

            validated = validate_primary_judge_assessment(
                judge_configuration,
                judge_qualification,
                assessment,
                task_class=contract.task_class,
                language=contract.language,
            )
            if validated.model_dump(mode="python") != assessment.model_dump(mode="python"):
                raise ValueError("semantic judge assessment provenance is not qualified")
        if assessment.source == AssessmentSource.HUMAN_ADJUDICATION and not isinstance(
            assessment, CalibratedHumanCriterionAssessment
        ):
            raise ValueError("human assessment is not calibrated for primary scoring")


__all__ = [
    "PrimaryScore",
    "ScoreBlockedError",
    "_assessment_map",
    "_require_resolved",
    "_require_scoreable_contract",
]
