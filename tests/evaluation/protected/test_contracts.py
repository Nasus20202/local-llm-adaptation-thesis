from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    ProtectedArtifactState,
    SourceEvidenceReference,
    validate_protected_contract,
    validate_source_identity,
    validate_successor,
)

from .fixtures import artifact, knowledge_contract, source_identity


def test_contract_validation_binds_family_input_root_and_frozen_source() -> None:
    contract = knowledge_contract()
    assert (
        validate_protected_contract(
            contract,
            approved_family_id="synthetic-family-1",
            approved_input_id="synthetic-input-1",
            approved_input_sha256="d" * 64,
            require_frozen=True,
        )
        == contract
    )
    with pytest.raises(ValueError):
        validate_protected_contract(
            contract,
            approved_family_id="different-family",
            approved_input_id="synthetic-input-1",
            approved_input_sha256="d" * 64,
        )
    altered = contract.model_copy(
        update={
            "artifact": contract.artifact.model_copy(
                update={
                    "root_reference": contract.artifact.root_reference.model_copy(
                        update={"root_id": "other-root"}
                    )
                }
            )
        }
    )
    with pytest.raises(ValueError):
        validate_protected_contract(
            altered,
            approved_family_id="synthetic-family-1",
            approved_input_id="synthetic-input-1",
            approved_input_sha256="d" * 64,
        )


def test_contract_rejects_review_note_and_unfrozen_source_identity() -> None:
    with pytest.raises(ValueError):
        SourceEvidenceReference(
            schema_version=1,
            evidence_id="evidence-note",
            source=source_identity().model_copy(
                update={"path_or_selector": "Expected answer — reviewer note"}
            ),
            source_role="construction",
        )
    altered = source_identity().model_copy(
        update={
            "path_or_selector": "content/en/docs/not-in-frozen-inventory.md",
            "content_sha256": "e" * 64,
            "git_blob_sha1": "a" * 40,
        }
    )
    with pytest.raises(ValueError):
        validate_source_identity(altered)


def test_frozen_protected_artifact_corrections_require_an_immutable_successor() -> None:
    prior = artifact()
    successor_hash = "d" * 64
    successor = prior.model_copy(
        update={
            "artifact_id": "evaluator-contract-2",
            "content_sha256": successor_hash,
            "root_reference": prior.root_reference.model_copy(
                update={"content_sha256": successor_hash}
            ),
            "supersedes_artifact_id": prior.artifact_id,
            "state": ProtectedArtifactState.DRAFT,
        }
    )
    assert validate_successor(prior, successor) == successor
    with pytest.raises(ValueError):
        validate_successor(prior, prior.model_copy(update={"state": ProtectedArtifactState.DRAFT}))
