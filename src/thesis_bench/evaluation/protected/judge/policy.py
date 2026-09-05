from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator, model_validator

from ....pilot.models import Language, TaskClass
from ....records import ProtectedRootReference, VersionedRecord
from ....schemas import Identifier, Sha256
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path


class JudgeCriterionAuthorization(VersionedRecord):
    task_class: TaskClass
    language: Language
    criterion_id: Identifier
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    artifact_id: Identifier
    artifact_kind: Identifier
    artifact_sha256: Sha256
    root_reference: ProtectedRootReference

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_artifact_binding(self) -> JudgeCriterionAuthorization:
        if self.root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("judge criterion authorization must use the approved root")
        validate_protected_relative_path(self.root_reference.relative_path)
        if self.root_reference.content_sha256 != self.artifact_sha256:
            raise ValueError("judge criterion authorization hash does not match its root")
        return self


class AuditPolicy(VersionedRecord):
    audit_policy_id: Identifier
    sampling_identity: Identifier
    frozen_before_outcomes: Literal[True]
    blinded: Literal[True]
    membership_manifest_id: Identifier
    membership_manifest_sha256: Sha256
    membership_manifest_root_reference: ProtectedRootReference
    selected_response_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_membership_manifest(self) -> AuditPolicy:
        if self.membership_manifest_root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("audit membership manifest must use the approved protected root")
        validate_protected_relative_path(self.membership_manifest_root_reference.relative_path)
        if self.membership_manifest_root_reference.content_sha256 != (
            self.membership_manifest_sha256
        ):
            raise ValueError("audit membership manifest hash does not match its root reference")
        if len(set(self.selected_response_ids)) != len(self.selected_response_ids):
            raise ValueError("audit membership response identities must be unique")
        return self


class JudgeScope(VersionedRecord):
    task_class: TaskClass
    language: Language
    criterion_ids: tuple[Identifier, ...] = Field(min_length=1)
    criterion_authorizations: tuple[JudgeCriterionAuthorization, ...] = Field(min_length=1)

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_unique_scope_criteria(self) -> JudgeScope:
        if len(set(self.criterion_ids)) != len(self.criterion_ids):
            raise ValueError("judge scope criterion identifiers must be unique")
        authorization_keys = {
            (item.task_class, item.language, item.criterion_id)
            for item in self.criterion_authorizations
        }
        if authorization_keys != {
            (self.task_class, self.language, criterion_id) for criterion_id in self.criterion_ids
        }:
            raise ValueError(
                "judge scope requires one protected artifact authorization per criterion"
            )
        return self


class QualificationAdjudicationBinding(VersionedRecord):
    adjudication_id: Identifier
    content_sha256: Sha256
    root_reference: ProtectedRootReference

    @model_validator(mode="after")
    def validate_adjudication_artifact(self) -> QualificationAdjudicationBinding:
        if self.root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("qualification adjudication must use the approved root")
        validate_protected_relative_path(self.root_reference.relative_path)
        if self.root_reference.content_sha256 != self.content_sha256:
            raise ValueError("qualification adjudication hash does not match its root")
        return self


__all__ = [
    "AuditPolicy",
    "JudgeCriterionAuthorization",
    "JudgeScope",
    "QualificationAdjudicationBinding",
]
