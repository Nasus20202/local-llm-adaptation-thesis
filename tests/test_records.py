from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from thesis_bench.records import (
    AppendOnlyEvent,
    AppendOnlyEventStore,
    DecisionStatus,
    Identity,
    ProtectedRootReference,
    ReasonCode,
    canonical_json_bytes,
    content_sha256,
    load_record,
    model_facing_json,
)


def test_versioned_identity_is_frozen_and_unknown_version_is_rejected() -> None:
    identity = Identity(
        schema_version=1,
        kind="synthetic-record",
        identity_id="record-1",
        revision="v1",
        content_sha256="a" * 64,
    )

    with pytest.raises(ValidationError):
        Identity(
            schema_version=2,
            kind="synthetic-record",
            identity_id="record-1",
            revision="v1",
            content_sha256="a" * 64,
        )

    with pytest.raises(ValidationError):
        identity.identity_id = "record-2"  # type: ignore[misc]


def test_append_only_store_rejects_collisions_and_overwrites(tmp_path: Path) -> None:
    event = AppendOnlyEvent(
        schema_version=1,
        event_id="event-1",
        event_type="synthetic-observation",
        occurred_at="2026-09-03T10:00:00Z",
        status=DecisionStatus.GO,
        reason_codes=(ReasonCode.OK,),
    )
    store = AppendOnlyEventStore(tmp_path)

    store.append(event)
    original = (tmp_path / "event-1.json").read_bytes()

    with pytest.raises(ValueError, match="collision"):
        store.append(event)

    with pytest.raises(ValueError, match="overwrite"):
        store.overwrite(event)
    assert (tmp_path / "event-1.json").read_bytes() == original


def test_canonical_bytes_and_hash_are_stable_for_key_order_variations() -> None:
    first = {"z": [2, 1], "a": {"payload": "synthetic"}}
    second = {"a": {"payload": "synthetic"}, "z": [2, 1]}

    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert content_sha256(first) == content_sha256(second)


def test_protected_root_is_portable_and_model_facing_output_is_redacted() -> None:
    reference = ProtectedRootReference(
        schema_version=1,
        root_id="protected-evaluator",
        relative_path="records/input.json",
        content_sha256="b" * 64,
    )
    assert reference.relative_path == "records/input.json"

    protected_value = "synthetic-protected-payload-7"
    with pytest.raises(ValueError) as raised:
        model_facing_json(
            {"identity": reference, "payload": protected_value},
            protected_values=(protected_value,),
        )
    assert protected_value not in str(raised.value)

    encoded = model_facing_json({"identity": reference})
    assert protected_value not in encoded
    assert json.loads(encoded)["identity"]["root_id"] == "protected-evaluator"


def test_protected_root_rejects_absolute_and_parent_paths() -> None:
    for path in ("/tmp/secret.json", "../secret.json", "records/../../secret.json"):
        with pytest.raises(ValidationError):
            ProtectedRootReference(
                schema_version=1,
                root_id="protected-evaluator",
                relative_path=path,
                content_sha256="c" * 64,
            )


def test_load_record_uses_redacted_diagnostics(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    protected_value = "synthetic-protected-payload-8"
    path.write_text(
        json.dumps(
            {
                "schema_version": 99,
                "event_id": "event-2",
                "event_type": protected_value,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as raised:
        load_record(path, AppendOnlyEvent)
    assert protected_value not in str(raised.value)
