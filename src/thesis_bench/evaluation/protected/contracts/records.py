from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.types import StrictBool, StrictFloat, StrictInt, StrictStr

from ....pilot.models import Language, TaskClass
from ....records import ProtectedRootReference, VersionedRecord
from ....schemas import Identifier, Sha256
from ..source import (
    APPROVED_PROTECTED_ROOT,
    reject_reviewer_note,
    validate_protected_relative_path,
)


class CriterionRole(StrEnum):
    REQUIRED_CLAIM = "required_claim"
    UNSUPPORTED_OR_CONTRADICTORY = "unsupported_or_contradictory"
    PRIMARY_REQUIRED = "primary_required"
    PRIMARY_PROHIBITED = "primary_prohibited"
    PRIMARY_HARD_GATE = "primary_hard_gate"
    SCORE_BEARING = "score_bearing"
    DETERMINISTIC = "deterministic"
    SEMANTIC = "semantic"


class CustodyRole(StrEnum):
    HUMAN_RESEARCHER_CUSTODIAN = "human-researcher-custodian"
    DEVELOPMENT_AUTHOR = "development-author"
    EVALUATOR_AUTHOR_REVIEWER = "evaluator-author-reviewer"
    BLINDED_RATER_ADJUDICATOR = "blinded-rater-adjudicator"
    MODEL_FACING = "model-facing-runner-retriever-prompt-harness-skill-or-w1"
    FUTURE_TRAINING = "future-training-builder-or-trainer"
    QUALIFIED_SEMANTIC_JUDGE = "qualified-semantic-judge"


class CustodyPurpose(StrEnum):
    READ = "read"
    WRITE = "write"
    FREEZE = "freeze"
    REVIEW = "review"
    JUDGE_ASSESSMENT = "judge-assessment"
    ADJUDICATION = "adjudication"
    AUDIT = "audit"
    SUPERSESSION = "supersession"


class ProtectedArtifactState(StrEnum):
    DRAFT = "draft"
    FROZEN = "frozen"
    SUPERSEDED = "superseded"


class _ProtectedRecord(VersionedRecord):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, hide_input_in_errors=True)


class AcceptedSemanticAlternative(_ProtectedRecord):
    alternative_id: Identifier
    criterion_id: Identifier
    relation: Literal["paraphrase", "synonym", "reordering", "equivalent"]

    @model_validator(mode="after")
    def reject_answer_text(self) -> AcceptedSemanticAlternative:
        reject_reviewer_note(self.model_dump(mode="python"))
        return self


class ProtectedCriterion(_ProtectedRecord):
    criterion_id: Identifier
    roles: tuple[CriterionRole, ...] = Field(min_length=1)
    accepted_alternatives: tuple[AcceptedSemanticAlternative, ...] = ()
    deterministic_predicate_id: Identifier | None = None
    evidence_ids: tuple[Identifier, ...] = Field(min_length=1)

    @field_validator("roles", mode="before")
    @classmethod
    def parse_roles(cls, value: object) -> object:
        if not isinstance(value, (tuple, list)):
            return value
        return tuple(CriterionRole(item) if isinstance(item, str) else item for item in value)

    @model_validator(mode="after")
    def validate_criterion_contract(self) -> ProtectedCriterion:
        if len(set(self.roles)) != len(self.roles):
            raise ValueError("criterion roles must be unique")
        alternative_ids = [item.alternative_id for item in self.accepted_alternatives]
        if len(set(alternative_ids)) != len(alternative_ids):
            raise ValueError("accepted alternatives must be unique")
        if any(item.criterion_id != self.criterion_id for item in self.accepted_alternatives):
            raise ValueError("accepted alternatives must map to their criterion")
        if CriterionRole.DETERMINISTIC in self.roles and self.deterministic_predicate_id is None:
            raise ValueError("deterministic criteria require a predicate")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("criterion evidence identifiers must be unique")
        return self


class DeterministicPredicate(_ProtectedRecord):
    predicate_id: Identifier
    criterion_id: Identifier
    predicate_kind: Literal[
        "parse",
        "schema",
        "exact_literal",
        "exact_value",
        "exact_structure",
        "count",
        "command_bound",
        "action_bound",
        "mutation_scope",
        "final_state",
        "custom",
    ]
    predicate_version: Identifier
    exact_literal: StrictStr | None = None
    exact_value: StrictStr | StrictInt | StrictFloat | StrictBool | None = None
    exact_structure_id: Identifier | None = None
    schema_id: Identifier | None = None
    expected_count: StrictInt | None = Field(default=None, ge=0)
    command_rule_id: Identifier | None = None
    action_rule_id: Identifier | None = None
    mutation_scope_id: Identifier | None = None
    final_state_id: Identifier | None = None

    @model_validator(mode="after")
    def reject_convenience_note(self) -> DeterministicPredicate:
        reject_reviewer_note(self.model_dump(mode="python"))
        return self


class SemanticCriterion(_ProtectedRecord):
    criterion_id: Identifier
    anchor_id: Identifier
    allowed_assessor_modes: tuple[
        Literal["qualified_semantic_judge", "human_adjudication"], ...
    ] = ("qualified_semantic_judge", "human_adjudication")

    @model_validator(mode="after")
    def require_assessor_mode(self) -> SemanticCriterion:
        if not self.allowed_assessor_modes:
            raise ValueError("semantic criteria require an assessor mode")
        if len(set(self.allowed_assessor_modes)) != len(self.allowed_assessor_modes):
            raise ValueError("semantic assessor modes must be unique")
        return self


class ProtectedArtifact(_ProtectedRecord):
    artifact_id: Identifier
    artifact_kind: Identifier
    revision: Identifier
    content_sha256: Sha256
    state: ProtectedArtifactState
    root_reference: ProtectedRootReference
    supersedes_artifact_id: Identifier | None = None

    @field_validator("state", mode="before")
    @classmethod
    def parse_state(cls, value: object) -> object:
        return ProtectedArtifactState(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_artifact_reference(self) -> ProtectedArtifact:
        if self.root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("protected artifact must use the approved protected root")
        validate_protected_relative_path(self.root_reference.relative_path)
        if self.root_reference.content_sha256 != self.content_sha256:
            raise ValueError("protected artifact hash must match its root reference")
        if self.state == ProtectedArtifactState.SUPERSEDED and self.supersedes_artifact_id is None:
            raise ValueError("superseded artifact must identify its predecessor")
        return self


class ApprovedScenarioBinding(_ProtectedRecord):
    family_id: Identifier
    input_id: Identifier
    input_sha256: Sha256
    task_class: TaskClass
    language: Language
    split: Literal["development"] = "development"

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value


__all__ = [
    "AcceptedSemanticAlternative",
    "ApprovedScenarioBinding",
    "CriterionRole",
    "CustodyPurpose",
    "CustodyRole",
    "DeterministicPredicate",
    "Language",
    "ProtectedArtifact",
    "ProtectedArtifactState",
    "ProtectedCriterion",
    "SemanticCriterion",
    "TaskClass",
]
