from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    APPROVED_REPOSITORY_SUBTREE,
    ProtectedArtifactReference,
    SafeProtectedHandle,
    model_facing_safe_handle,
)
from thesis_bench.records import ProtectedRootReference, ReasonCode


def test_safe_protected_handle_has_only_identity_integrity_and_status_fields() -> None:
    reference = ProtectedArtifactReference(
        schema_version=1,
        artifact_id="evaluator-contract-1",
        artifact_kind="evaluator",
        root_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path="contracts/synthetic.json",
            content_sha256="a" * 64,
        ),
    )
    handle = SafeProtectedHandle(
        schema_version=1,
        artifact_id=reference.artifact_id,
        artifact_kind=reference.artifact_kind,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path=reference.root_reference.relative_path,
        content_sha256=reference.root_reference.content_sha256,
        status="frozen",
        reason_codes=(ReasonCode.OK,),
        assessor_configuration_id="judge-config-identity-only",
        provenance_id="provenance-identity-only",
    )
    encoded = model_facing_safe_handle(handle)
    assert set(encoded) == {
        "schema_version",
        "artifact_id",
        "artifact_kind",
        "root_id",
        "relative_path",
        "content_sha256",
        "status",
        "reason_codes",
        "assessor_configuration_id",
        "provenance_id",
    }
    assert "claim" not in str(encoded)
    assert "a" * 64 in str(encoded)


def test_repository_evaluator_handle_cannot_be_model_facing() -> None:
    handle = SafeProtectedHandle(
        schema_version=1,
        artifact_id="evaluator-contract-1",
        artifact_kind="evaluator",
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path=f"{APPROVED_REPOSITORY_SUBTREE}/dev-k-pl-01/contract.json",
        content_sha256="a" * 64,
        status="frozen",
    )
    with pytest.raises(ValueError, match="not model-facing"):
        model_facing_safe_handle(handle)
