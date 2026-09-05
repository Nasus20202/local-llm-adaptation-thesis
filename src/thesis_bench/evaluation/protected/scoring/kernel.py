from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING

from ....pilot.models import TaskClass
from ..contracts.config import ProtectedSemanticContract
from .assessment import CriterionAssessment, CriterionDisposition
from .kernel_helpers import PrimaryScore, ScoreBlockedError, _require_scoreable_contract
from .tasks import score_knowledge, score_mixed, score_procedural

if TYPE_CHECKING:
    from ...calibration import CalibrationSummary
    from ...rubrics import AdjudicationRecord
    from ..judge.records import AuditPolicy, JudgeConfiguration, JudgeQualification
    from .assessment import AuditSelection


def derive_primary_score(
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
    if contract.task_class == TaskClass.KNOWLEDGE:
        return score_knowledge(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
            human_calibration=human_calibration,
            human_adjudications=human_adjudications,
            human_audit_selection=human_audit_selection,
            human_audit_policy=human_audit_policy,
            response_id=response_id,
        )
    if contract.task_class == TaskClass.PROCEDURAL:
        return score_procedural(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
            human_calibration=human_calibration,
            human_adjudications=human_adjudications,
            human_audit_selection=human_audit_selection,
            human_audit_policy=human_audit_policy,
            response_id=response_id,
        )
    if contract.task_class == TaskClass.MIXED:
        return score_mixed(
            contract,
            assessments,
            judge_configuration=judge_configuration,
            judge_qualification=judge_qualification,
            human_calibration=human_calibration,
            human_adjudications=human_adjudications,
            human_audit_selection=human_audit_selection,
            human_audit_policy=human_audit_policy,
            response_id=response_id,
        )
    raise ValueError("unsupported task class")


def derive_primary_score_from_dispositions(
    contract: ProtectedSemanticContract,
    dispositions: Mapping[str, CriterionDisposition],
) -> PrimaryScore:
    _require_scoreable_contract(contract)
    known = {criterion.criterion_id for criterion in contract.criteria}
    if not set(dispositions) <= known:
        raise ValueError("dispositions reference an unknown criterion")
    configuration = contract.score_configuration
    if contract.task_class == TaskClass.KNOWLEDGE:
        from ..contracts.scoring import KnowledgeScoreConfiguration
        from .tasks.knowledge import _score_knowledge_dispositions

        if not isinstance(configuration, KnowledgeScoreConfiguration):
            raise ValueError("knowledge scoring requires a knowledge configuration")
        required = set(configuration.required_criterion_ids) | set(
            configuration.unsupported_criterion_ids
        )
        return _score_from_dispositions(
            required, dispositions, lambda: _score_knowledge_dispositions(contract, dispositions)
        )
    if contract.task_class == TaskClass.PROCEDURAL:
        from ..contracts.scoring import ProceduralScoreConfiguration
        from .tasks.procedural import _score_procedural_dispositions

        if not isinstance(configuration, ProceduralScoreConfiguration):
            raise ValueError("procedural scoring requires a procedural configuration")
        required = set(configuration.primary_required_criterion_ids) | set(
            configuration.primary_prohibited_criterion_ids
        )
        return _score_from_dispositions(
            required, dispositions, lambda: _score_procedural_dispositions(contract, dispositions)
        )
    if contract.task_class == TaskClass.MIXED:
        from ..contracts.records import CriterionRole
        from ..contracts.scoring import MixedScoreConfiguration
        from .tasks.mixed import _score_mixed_dispositions

        if not isinstance(configuration, MixedScoreConfiguration):
            raise ValueError("mixed scoring requires a mixed configuration")
        prohibited = {
            item.criterion_id
            for item in contract.criteria
            if CriterionRole.PRIMARY_PROHIBITED in item.roles
        }
        required = (
            set(configuration.primary_hard_gate_criterion_ids)
            | set(configuration.point_table)
            | prohibited
        )
        return _score_from_dispositions(
            required, dispositions, lambda: _score_mixed_dispositions(contract, dispositions)
        )
    raise ValueError("unsupported task class")


def _score_from_dispositions(
    required: set[str],
    dispositions: Mapping[str, CriterionDisposition],
    scorer: Callable[[], PrimaryScore],
) -> PrimaryScore:
    if not required <= set(dispositions):
        raise ValueError("missing primary criterion disposition")
    if any(dispositions[item] == CriterionDisposition.UNRESOLVED for item in required):
        raise ScoreBlockedError()
    return scorer()


__all__ = [
    "PrimaryScore",
    "ScoreBlockedError",
    "derive_primary_score",
    "derive_primary_score_from_dispositions",
    "score_knowledge",
    "score_mixed",
    "score_procedural",
]
