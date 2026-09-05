from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    CustodyPurpose,
    CustodyRole,
    JudgeAccessGrant,
    ProtectedArtifact,
    ProtectedArtifactState,
    ProtectedCustodyEvent,
    load_protected_payload,
    record_protected_event,
)
from thesis_bench.records import (
    AppendOnlyEventStore,
    DecisionStatus,
    ProtectedRootReference,
    ReasonCode,
)

from .fixtures import artifact
from .judge_fixtures import qualified_judge


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


def test_protected_access_requires_append_only_evidence_store(tmp_path: Path) -> None:
    payload = b"custody-required-payload"
    reference = ProtectedRootReference(
        schema_version=1,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path="contracts/custody-required.json",
        content_sha256=hashlib.sha256(payload).hexdigest(),
    )
    protected_artifact = artifact().model_copy(
        update={"root_reference": reference, "content_sha256": reference.content_sha256}
    )
    with pytest.raises(TypeError, match="event_store"):
        load_protected_payload(
            reference,
            artifact=protected_artifact,
            actor_role=CustodyRole.EVALUATOR_AUTHOR_REVIEWER,
            purpose=CustodyPurpose.READ,
            reader=lambda _: payload,
        )

    class BrokenStore(AppendOnlyEventStore):
        def append(self, event):
            del event
            raise ValueError("synthetic append failure")

    with pytest.raises(ValueError, match="evidence"):
        load_protected_payload(
            reference,
            artifact=protected_artifact,
            actor_role=CustodyRole.EVALUATOR_AUTHOR_REVIEWER,
            purpose=CustodyPurpose.READ,
            reader=lambda _: payload,
            event_store=BrokenStore(tmp_path),
        )


def test_qualified_judge_access_requires_an_exact_scope_grant(tmp_path: Path) -> None:
    payload = b"judge-scope-payload"
    reference = ProtectedRootReference(
        schema_version=1,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path="contracts/judge-scope.json",
        content_sha256=hashlib.sha256(payload).hexdigest(),
    )
    protected_artifact = artifact().model_copy(
        update={"root_reference": reference, "content_sha256": reference.content_sha256}
    )
    with pytest.raises(ValueError, match="scope"):
        load_protected_payload(
            reference,
            artifact=protected_artifact,
            actor_role=CustodyRole.QUALIFIED_SEMANTIC_JUDGE,
            purpose=CustodyPurpose.READ,
            reader=lambda _: payload,
            event_store=AppendOnlyEventStore(tmp_path),
        )


def test_qualified_judge_denies_a_cross_criterion_artifact_before_reader(tmp_path: Path) -> None:
    configuration, qualification = qualified_judge()
    authorization = configuration.scopes[0].criterion_authorizations[0]
    authorized_artifact = ProtectedArtifact(
        schema_version=1,
        artifact_id=authorization.artifact_id,
        artifact_kind=authorization.artifact_kind,
        revision="v1",
        content_sha256=authorization.artifact_sha256,
        state=ProtectedArtifactState.FROZEN,
        root_reference=authorization.root_reference,
    )
    wrong_reference = authorization.root_reference.model_copy(
        update={"relative_path": "judge-inputs/unrelated.json", "content_sha256": "7" * 64}
    )
    wrong_artifact = authorized_artifact.model_copy(
        update={
            "artifact_id": "criterion-input-unrelated-1",
            "content_sha256": "7" * 64,
            "root_reference": wrong_reference,
        }
    )
    grant = JudgeAccessGrant(
        schema_version=1,
        judge_config_id=configuration.judge_config_id,
        qualification_id=qualification.qualification_id,
        task_class=configuration.scopes[0].task_class,
        language=configuration.scopes[0].language,
        criterion_id=authorization.criterion_id,
        protected_input_contract_id=authorization.protected_input_contract_id,
        protected_input_contract_sha256=authorization.protected_input_contract_sha256,
        artifact_id=wrong_artifact.artifact_id,
        artifact_kind=wrong_artifact.artifact_kind,
        artifact_sha256=wrong_artifact.content_sha256,
        root_reference=wrong_artifact.root_reference,
    )
    calls: list[str] = []
    with pytest.raises(ValueError, match="authorized"):
        load_protected_payload(
            wrong_artifact.root_reference,
            artifact=wrong_artifact,
            actor_role=CustodyRole.QUALIFIED_SEMANTIC_JUDGE,
            purpose=CustodyPurpose.READ,
            reader=lambda value: calls.append(value) or b"wrong-payload",
            event_store=AppendOnlyEventStore(tmp_path),
            judge_access=grant,
            judge_configuration=configuration,
            judge_qualification=qualification,
        )
    assert calls == []


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
