from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ....records import DecisionStatus, ProtectedRootReference, VersionedRecord
from ....schemas import Identifier, Sha256
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path
from .fairness_records import (
    FairnessQualification,
    JudgeFairnessCase,
    MetamorphicFixtureGroup,
    MetamorphicVariant,
    MetamorphicVariantKind,
)
from .policy import (
    AuditPolicy,
    JudgeCriterionAuthorization,
    JudgeScope,
    QualificationAdjudicationBinding,
)


class DecodingPolicy(VersionedRecord):
    temperature: StrictFloat = Field(ge=0.0)
    top_p: StrictFloat = Field(gt=0.0, le=1.0)
    max_output_tokens: StrictInt = Field(gt=0)
    max_retries: StrictInt = Field(ge=0)
    failure_policy: Literal["route_to_human", "fail_closed"]


class JudgeResponseSchema(VersionedRecord):
    schema_id: Identifier
    schema_version_id: Identifier
    schema_sha256: Sha256


class QualificationThresholds(VersionedRecord):
    threshold_set_id: Identifier
    minimum_criterion_agreement: StrictFloat | None = Field(default=None, ge=0.0, le=1.0)
    minimum_kappa: StrictFloat | None = Field(default=None, ge=-1.0, le=1.0)
    maximum_unresolved_rate: StrictFloat | None = Field(default=None, ge=0.0, le=1.0)

    @property
    def is_frozen(self) -> bool:
        return all(
            value is not None
            for value in (
                self.minimum_criterion_agreement,
                self.maximum_unresolved_rate,
            )
        )


class JudgeConfiguration(VersionedRecord):
    judge_config_id: Identifier
    revision: Identifier
    model_identity: Identifier
    provider_or_artifact_identity: Identifier
    backend_identity: Identifier
    prompt_template_identity: Identifier
    prompt_template_sha256: Sha256
    response_schema: JudgeResponseSchema
    decoding_policy: DecodingPolicy
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    qualification_set_id: Identifier
    qualification_set_sha256: Sha256
    qualification_thresholds: QualificationThresholds
    audit_policy: AuditPolicy
    scopes: tuple[JudgeScope, ...] = Field(min_length=1)
    state: Literal["draft", "frozen", "superseded"]
    suspension_state: Literal["active", "suspended", "requalification_required"] = "active"
    suspension_reason: Identifier | None = None
    content_sha256: Sha256 | None = None
    supersedes_judge_config_id: Identifier | None = None

    @model_validator(mode="after")
    def validate_configuration_scope(self) -> JudgeConfiguration:
        if self.suspension_state == "active" and self.suspension_reason is not None:
            raise ValueError("active judge configurations cannot carry a suspension reason")
        if self.suspension_state != "active" and self.suspension_reason is None:
            raise ValueError("suspended judge configurations require a reason")
        scope_keys = {
            (scope.task_class, scope.language, criterion_id)
            for scope in self.scopes
            for criterion_id in scope.criterion_ids
        }
        authorization_keys = {
            (scope.task_class, scope.language, item.criterion_id)
            for scope in self.scopes
            for item in scope.criterion_authorizations
        }
        if scope_keys != authorization_keys:
            raise ValueError(
                "judge configuration must authorize every scoped criterion exactly once"
            )
        if any(
            item.protected_input_contract_id != self.protected_input_contract_id
            or item.protected_input_contract_sha256 != self.protected_input_contract_sha256
            for scope in self.scopes
            for item in scope.criterion_authorizations
        ):
            raise ValueError("judge criterion authorization protected input does not match")
        return self


class JudgeQualification(VersionedRecord):
    qualification_id: Identifier
    judge_config_id: Identifier
    judge_config_sha256: Sha256
    qualification_set_id: Identifier
    qualification_set_sha256: Sha256
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    qualification_revision: Identifier
    qualification_root_reference: ProtectedRootReference
    qualification_adjudications: tuple[QualificationAdjudicationBinding, ...] = ()
    malformed_output_count: StrictInt = Field(ge=0)
    state: Literal["frozen", "superseded"]
    content_sha256: Sha256
    supersedes_qualification_id: Identifier | None = None
    criterion_agreement: dict[Identifier, StrictFloat]
    confusion_matrix: dict[Identifier, dict[str, dict[str, StrictInt]]]
    agreement_statistic: StrictFloat | None = None
    unresolved_count: StrictInt = Field(ge=0)
    schema_failure_count: StrictInt = Field(ge=0)
    fairness_status: DecisionStatus
    fairness_scope_status: dict[Identifier, DecisionStatus] = {}
    thresholds_satisfied: StrictBool
    status: DecisionStatus

    @model_validator(mode="after")
    def validate_qualification_artifact(self) -> JudgeQualification:
        if self.qualification_root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("judge qualification must use the approved protected root")
        validate_protected_relative_path(self.qualification_root_reference.relative_path)
        if self.qualification_root_reference.content_sha256 != self.content_sha256:
            raise ValueError("judge qualification root hash must match its content hash")
        adjudication_ids = [item.adjudication_id for item in self.qualification_adjudications]
        if len(set(adjudication_ids)) != len(adjudication_ids):
            raise ValueError("judge qualification adjudication evidence must be unique")
        if self.state == "superseded" and self.supersedes_qualification_id is None:
            raise ValueError("superseded qualification must identify its predecessor")
        if self.supersedes_qualification_id == self.qualification_id:
            raise ValueError("qualification cannot supersede itself")
        return self


__all__ = [
    "AuditPolicy",
    "DecodingPolicy",
    "FairnessQualification",
    "JudgeConfiguration",
    "JudgeCriterionAuthorization",
    "JudgeFairnessCase",
    "JudgeQualification",
    "JudgeResponseSchema",
    "JudgeScope",
    "MetamorphicFixtureGroup",
    "MetamorphicVariant",
    "MetamorphicVariantKind",
    "QualificationThresholds",
    "QualificationAdjudicationBinding",
]
