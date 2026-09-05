from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import model_validator

from ....pilot.models import Language, TaskClass
from ....records import ProtectedRootReference, VersionedRecord
from ....schemas import Identifier, Sha256
from ..contracts.records import ProtectedArtifact
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path

if TYPE_CHECKING:
    from ..judge.records import JudgeConfiguration, JudgeQualification


class JudgeAccessGrant(VersionedRecord):
    judge_config_id: Identifier
    qualification_id: Identifier
    task_class: TaskClass
    language: Language
    criterion_id: Identifier
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    artifact_id: Identifier
    artifact_kind: Identifier
    artifact_sha256: Sha256
    root_reference: ProtectedRootReference

    @model_validator(mode="after")
    def validate_root(self) -> JudgeAccessGrant:
        if self.root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("judge access grant must use the approved protected root")
        validate_protected_relative_path(self.root_reference.relative_path)
        return self


def validate_judge_access_grant(
    grant: JudgeAccessGrant,
    *,
    configuration: JudgeConfiguration,
    qualification: JudgeQualification,
    artifact: ProtectedArtifact,
) -> JudgeAccessGrant:
    from ..judge.eligibility import validate_judge_qualification

    try:
        grant = JudgeAccessGrant.model_validate(grant.model_dump(mode="python"))
        artifact = ProtectedArtifact.model_validate(artifact.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge access scope is invalid") from None
    validate_judge_qualification(configuration, qualification, require_primary_eligibility=True)
    if grant.judge_config_id != configuration.judge_config_id:
        raise ValueError("judge access scope configuration does not match")
    if grant.qualification_id != qualification.qualification_id:
        raise ValueError("judge access scope qualification does not match")
    if grant.task_class not in {scope.task_class for scope in configuration.scopes}:
        raise ValueError("judge access scope task class is not qualified")
    if not any(
        scope.task_class == grant.task_class
        and scope.language == grant.language
        and grant.criterion_id in scope.criterion_ids
        for scope in configuration.scopes
    ):
        raise ValueError("judge access scope criterion is not qualified")
    if (
        grant.protected_input_contract_id != configuration.protected_input_contract_id
        or grant.protected_input_contract_sha256 != configuration.protected_input_contract_sha256
    ):
        raise ValueError("judge access scope protected input does not match")
    if (
        grant.artifact_id != artifact.artifact_id
        or grant.artifact_kind != artifact.artifact_kind
        or grant.artifact_sha256 != artifact.content_sha256
    ):
        raise ValueError("judge access scope artifact does not match")
    if grant.root_reference != artifact.root_reference:
        raise ValueError("judge access scope root reference does not match")
    return grant


__all__ = ["JudgeAccessGrant", "validate_judge_access_grant"]
