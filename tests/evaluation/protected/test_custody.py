from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    CustodyPurpose,
    CustodyRole,
    ProtectedArtifactReference,
    ProtectedCustodyEvent,
    SafeProtectedHandle,
    load_protected_payload,
    model_facing_safe_handle,
    record_protected_event,
)
from thesis_bench.records import (
    AppendOnlyEventStore,
    DecisionStatus,
    ProtectedRootReference,
    ReasonCode,
)

from .fixtures import artifact


def test_protected_event_wrapper_preserves_append_only_lineage(tmp_path: Path) -> None:
    protected_artifact = artifact()
    event = ProtectedCustodyEvent(
        schema_version=1,
        event_id="protected-event-wrapper-1",
        event_type="protected-review",
        occurred_at="2026-09-05T10:00:00Z",
        status=DecisionStatus.GO,
        reason_codes=(ReasonCode.OK,),
        artifact_id=protected_artifact.artifact_id,
        artifact_kind=protected_artifact.artifact_kind,
        root_id=APPROVED_PROTECTED_ROOT,
        artifact_revision=protected_artifact.revision,
        artifact_sha256=protected_artifact.content_sha256,
        actor_role=CustodyRole.EVALUATOR_AUTHOR_REVIEWER,
        purpose=CustodyPurpose.REVIEW,
    )
    store = AppendOnlyEventStore(tmp_path)
    assert record_protected_event(store, event, artifact=protected_artifact).exists()
    with pytest.raises(ValueError, match="collision"):
        record_protected_event(store, event, artifact=protected_artifact)


def test_protected_access_denies_model_facing_roles_before_read_and_redacts_errors(
    tmp_path: Path,
) -> None:
    reference = ProtectedRootReference(
        schema_version=1,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path="contracts/synthetic.json",
        content_sha256=hashlib.sha256(b"secret-payload").hexdigest(),
    )
    protected_artifact = artifact().model_copy(
        update={"root_reference": reference, "content_sha256": reference.content_sha256}
    )
    store = AppendOnlyEventStore(tmp_path)
    calls: list[str] = []
    with pytest.raises(ValueError) as denied:
        load_protected_payload(
            reference,
            artifact=protected_artifact,
            actor_role=CustodyRole.MODEL_FACING,
            purpose=CustodyPurpose.READ,
            reader=lambda value: calls.append(value) or b"secret-payload",
            event_store=store,
        )
    assert calls == []
    assert "secret-payload" not in str(denied.value)
    loaded = load_protected_payload(
        reference,
        artifact=protected_artifact,
        actor_role=CustodyRole.EVALUATOR_AUTHOR_REVIEWER,
        purpose=CustodyPurpose.READ,
        reader=lambda _: b"secret-payload",
        event_store=store,
    )
    assert loaded == b"secret-payload"


def test_repeated_protected_reads_append_distinct_custody_events(tmp_path: Path) -> None:
    payload = b"repeatable-synthetic-payload"
    reference = ProtectedRootReference(
        schema_version=1,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path="contracts/repeated.json",
        content_sha256=hashlib.sha256(payload).hexdigest(),
    )
    protected_artifact = artifact().model_copy(
        update={"root_reference": reference, "content_sha256": reference.content_sha256}
    )
    store = AppendOnlyEventStore(tmp_path)

    for _ in range(2):
        assert (
            load_protected_payload(
                reference,
                artifact=protected_artifact,
                actor_role=CustodyRole.EVALUATOR_AUTHOR_REVIEWER,
                purpose=CustodyPurpose.READ,
                reader=lambda _: payload,
                event_store=store,
            )
            == payload
        )

    assert len(tuple(tmp_path.glob("*.json"))) == 2


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
