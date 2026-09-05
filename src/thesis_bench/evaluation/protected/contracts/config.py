from __future__ import annotations

from pydantic import Field, field_validator, model_validator

from ....pilot.models import Language, TaskClass
from ....schemas import Identifier, Sha256
from ...identity import EvaluatorIdentity
from ..source import (
    APPROVED_EVALUATION_CLARIFICATION,
    APPROVED_PREAUTHORING_FREEZE,
    APPROVED_SOURCE_RIGHTS_MANIFEST,
    SourceEvidenceReference,
    reject_reviewer_note,
)
from .records import (
    CriterionRole,
    DeterministicPredicate,
    ProtectedArtifact,
    ProtectedCriterion,
    SemanticCriterion,
    _ProtectedRecord,
)
from .scoring import (
    KnowledgeScoreConfiguration,
    MixedScoreConfiguration,
    ProceduralScoreConfiguration,
)


class ProtectedSemanticContract(_ProtectedRecord):
    artifact: ProtectedArtifact
    family_id: Identifier
    scenario_input_id: Identifier
    scenario_input_sha256: Sha256
    task_class: TaskClass
    language: Language
    source_rights_manifest_id: str
    preauthoring_freeze_id: str
    evaluation_clarification_id: str
    evaluator_identity: EvaluatorIdentity
    criteria: tuple[ProtectedCriterion, ...] = Field(min_length=1)
    predicates: tuple[DeterministicPredicate, ...] = ()
    semantic_criteria: tuple[SemanticCriterion, ...] = ()
    evidence: tuple[SourceEvidenceReference, ...] = Field(min_length=1)
    score_configuration: (
        KnowledgeScoreConfiguration | ProceduralScoreConfiguration | MixedScoreConfiguration
    )

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_contract_shape(self) -> ProtectedSemanticContract:
        reject_reviewer_note(self.model_dump(mode="python"))
        if self.artifact.artifact_kind != "evaluator-contract":
            raise ValueError("protected contract requires an evaluator-contract artifact")
        if (
            self.evaluator_identity.identity_id != self.artifact.artifact_id
            or self.evaluator_identity.revision != self.artifact.revision
            or self.evaluator_identity.content_sha256 != self.artifact.content_sha256
        ):
            raise ValueError("contract evaluator identity does not match its artifact")
        if self.source_rights_manifest_id != APPROVED_SOURCE_RIGHTS_MANIFEST:
            raise ValueError("contract source rights manifest is not approved")
        if self.preauthoring_freeze_id != APPROVED_PREAUTHORING_FREEZE:
            raise ValueError("contract preauthoring freeze is not approved")
        if self.evaluation_clarification_id != APPROVED_EVALUATION_CLARIFICATION:
            raise ValueError("contract evaluation clarification is not approved")
        criterion_ids = [criterion.criterion_id for criterion in self.criteria]
        if len(set(criterion_ids)) != len(criterion_ids):
            raise ValueError("contract criterion identifiers must be unique")
        semantic_ids = [item.criterion_id for item in self.semantic_criteria]
        if len(set(semantic_ids)) != len(semantic_ids):
            raise ValueError("semantic criterion identifiers must be unique")
        evidence_ids = {item.evidence_id for item in self.evidence}
        if len(evidence_ids) != len(self.evidence):
            raise ValueError("contract evidence identifiers must be unique")
        criteria_by_id = {criterion.criterion_id: criterion for criterion in self.criteria}
        for criterion in self.criteria:
            if not set(criterion.evidence_ids) <= evidence_ids:
                raise ValueError("every criterion must map to protected evidence")
        for predicate in self.predicates:
            if (
                predicate.criterion_id not in criteria_by_id
                or criteria_by_id[predicate.criterion_id].deterministic_predicate_id
                != predicate.predicate_id
            ):
                raise ValueError("deterministic predicate is not bound to its criterion")
        for semantic in self.semantic_criteria:
            semantic_criterion = criteria_by_id.get(semantic.criterion_id)
            if semantic_criterion is None or CriterionRole.SEMANTIC not in semantic_criterion.roles:
                raise ValueError("semantic criterion must bind to a semantic contract criterion")
        if {
            criterion.criterion_id
            for criterion in self.criteria
            if CriterionRole.SEMANTIC in criterion.roles
        } != set(semantic_ids):
            raise ValueError("every semantic contract criterion requires an assessor definition")
        configured = self._configured_criteria()
        if not configured <= set(criterion_ids):
            raise ValueError("score configuration references an unknown criterion")
        self._validate_task_configuration(criteria_by_id)
        return self

    def _configured_criteria(self) -> set[str]:
        config = self.score_configuration
        if isinstance(config, KnowledgeScoreConfiguration):
            return set(config.required_criterion_ids) | set(config.unsupported_criterion_ids)
        if isinstance(config, ProceduralScoreConfiguration):
            return set(config.primary_required_criterion_ids) | set(
                config.primary_prohibited_criterion_ids
            )
        return set(config.primary_hard_gate_criterion_ids) | set(config.point_table)

    def _validate_task_configuration(self, criteria: dict[str, ProtectedCriterion]) -> None:
        config = self.score_configuration
        if self.task_class == TaskClass.KNOWLEDGE and isinstance(
            config, KnowledgeScoreConfiguration
        ):
            required_claims = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.REQUIRED_CLAIM in item.roles
            }
            unsupported = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.UNSUPPORTED_OR_CONTRADICTORY in item.roles
            }
            if required_claims != set(config.required_criterion_ids):
                raise ValueError("knowledge required claims must match the score configuration")
            if unsupported != set(config.unsupported_criterion_ids):
                raise ValueError(
                    "knowledge unsupported criteria must match the score configuration"
                )
            if any(
                CriterionRole.REQUIRED_CLAIM not in criteria[item].roles
                for item in config.required_criterion_ids
            ):
                raise ValueError("knowledge required criteria must declare required claims")
            if any(
                CriterionRole.UNSUPPORTED_OR_CONTRADICTORY not in criteria[item].roles
                for item in config.unsupported_criterion_ids
            ):
                raise ValueError("knowledge false-positive criteria must be contract-declared")
            if not any(
                CriterionRole.REQUIRED_CLAIM in criteria[item].roles
                for item in config.required_criterion_ids
            ):
                raise ValueError("knowledge contract requires an atomic required claim")
        elif self.task_class == TaskClass.PROCEDURAL and isinstance(
            config, ProceduralScoreConfiguration
        ):
            required = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.PRIMARY_REQUIRED in item.roles
            }
            prohibited = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.PRIMARY_PROHIBITED in item.roles
            }
            if required != set(config.primary_required_criterion_ids):
                raise ValueError("procedural required criteria must match the score configuration")
            if prohibited != set(config.primary_prohibited_criterion_ids):
                raise ValueError(
                    "procedural prohibited criteria must match the score configuration"
                )
        elif self.task_class == TaskClass.MIXED and isinstance(config, MixedScoreConfiguration):
            hard_gates = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.PRIMARY_HARD_GATE in item.roles
            }
            if hard_gates != set(config.primary_hard_gate_criterion_ids):
                raise ValueError("mixed hard gates must match the score configuration")
            if any(
                CriterionRole.PRIMARY_HARD_GATE not in criteria[item].roles
                for item in config.primary_hard_gate_criterion_ids
            ):
                raise ValueError("mixed hard gates must be contract-declared")
            score_bearing = {
                item.criterion_id
                for item in criteria.values()
                if CriterionRole.SCORE_BEARING in item.roles
            }
            if score_bearing - set(config.point_table):
                raise ValueError("every mixed score-bearing criterion requires a point mapping")
            if any(
                CriterionRole.SCORE_BEARING not in criteria[item].roles
                for item in config.point_table
            ):
                raise ValueError("mixed point entries must be score-bearing criteria")
        else:
            raise ValueError("score configuration does not match task class")


__all__ = [
    "KnowledgeScoreConfiguration",
    "MixedScoreConfiguration",
    "ProceduralScoreConfiguration",
    "ProtectedSemanticContract",
]
