from __future__ import annotations

from pydantic import Field
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ....pilot.models import TaskClass
from ....records import ReasonCode, VersionedRecord
from ..contracts.config import ProtectedSemanticContract
from ..contracts.records import CriterionRole
from ..contracts.scoring import (
    KnowledgeScoreConfiguration,
    MixedScoreConfiguration,
    ProceduralScoreConfiguration,
)
from ..contracts.validation import validate_protected_contract
from .assessment import (
    AssessmentSource,
    CalibratedHumanCriterionAssessment,
    CriterionAssessment,
    CriterionDisposition,
    QualifiedCriterionAssessment,
)


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
        validate_protected_contract(
            contract,
            approved_family_id=contract.family_id,
            approved_input_id=contract.scenario_input_id,
            approved_input_sha256=contract.scenario_input_sha256,
            require_frozen=True,
        )
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
) -> None:
    criteria = {criterion.criterion_id: criterion for criterion in contract.criteria}
    for criterion_id in required_ids:
        assessment = assessments.get(criterion_id)
        if assessment is None:
            raise ValueError("missing primary criterion assessment")
        if assessment.disposition == CriterionDisposition.UNRESOLVED:
            raise ScoreBlockedError()
        criterion = criteria[criterion_id]
        if (
            CriterionRole.DETERMINISTIC in criterion.roles
            and assessment.source != AssessmentSource.DETERMINISTIC
        ):
            raise ValueError("deterministic criterion cannot use a semantic assessor")
        if assessment.source == AssessmentSource.QUALIFIED_SEMANTIC_JUDGE and not isinstance(
            assessment, QualifiedCriterionAssessment
        ):
            raise ValueError("semantic judge assessment is not qualified for primary scoring")
        if assessment.source == AssessmentSource.HUMAN_ADJUDICATION and not isinstance(
            assessment, CalibratedHumanCriterionAssessment
        ):
            raise ValueError("human assessment is not calibrated for primary scoring")


def score_knowledge(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
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
    _require_resolved(contract, assessment_map, required_ids)
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


def score_procedural(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
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
    _require_resolved(contract, assessment_map, required_ids)
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


def score_mixed(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
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
    _require_resolved(contract, assessment_map, required_ids)
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


def derive_primary_score(
    contract: ProtectedSemanticContract,
    assessments: tuple[CriterionAssessment, ...] | list[CriterionAssessment],
) -> PrimaryScore:
    if contract.task_class == TaskClass.KNOWLEDGE:
        return score_knowledge(contract, assessments)
    if contract.task_class == TaskClass.PROCEDURAL:
        return score_procedural(contract, assessments)
    if contract.task_class == TaskClass.MIXED:
        return score_mixed(contract, assessments)
    raise ValueError("unsupported task class")


__all__ = [
    "PrimaryScore",
    "ScoreBlockedError",
    "derive_primary_score",
    "score_knowledge",
    "score_mixed",
    "score_procedural",
]
