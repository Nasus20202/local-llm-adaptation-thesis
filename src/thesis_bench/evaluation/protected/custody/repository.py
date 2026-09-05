from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ....pilot.models import ProtectedArtifactReference
from ....records import AppendOnlyEventStore, ProtectedRootReference
from ..contracts.records import CustodyPurpose, CustodyRole, ProtectedArtifact
from ..source import validate_repository_protected_path
from .access import load_protected_payload
from .judge_access import JudgeAccessGrant

if TYPE_CHECKING:
    from ..judge.records import JudgeConfiguration, JudgeQualification


def load_repository_protected_payload(
    reference: ProtectedRootReference,
    *,
    artifact: ProtectedArtifact,
    repository_root: Path,
    actor_role: CustodyRole | str,
    purpose: CustodyPurpose | str,
    event_store: AppendOnlyEventStore,
    judge_access: JudgeAccessGrant | None = None,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> bytes:
    """Load a protected artifact from the approved repository subtree."""
    validate_repository_protected_path(reference.relative_path)
    root = repository_root.resolve()

    def reader(relative_path: str) -> bytes:
        if relative_path != reference.relative_path:
            raise ValueError("protected reference changed during repository read")
        candidate = (root / relative_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            raise ValueError("protected repository path escaped the repository root") from None
        return candidate.read_bytes()

    return load_protected_payload(
        reference,
        artifact=artifact,
        actor_role=actor_role,
        purpose=purpose,
        reader=reader,
        event_store=event_store,
        judge_access=judge_access,
        judge_configuration=judge_configuration,
        judge_qualification=judge_qualification,
    )


def repository_protected_reference(
    reference: ProtectedArtifactReference,
) -> ProtectedArtifactReference:
    """Validate that a public evaluator reference uses the repository binding."""
    validate_repository_protected_path(reference.root_reference.relative_path)
    return reference


__all__ = ["load_repository_protected_payload", "repository_protected_reference"]
