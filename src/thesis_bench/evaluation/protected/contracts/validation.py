from __future__ import annotations

from ....pilot.models import Language, TaskClass
from .config import ProtectedSemanticContract
from .records import ProtectedArtifact, ProtectedArtifactState


def validate_protected_contract(
    contract: ProtectedSemanticContract,
    *,
    approved_family_id: str,
    approved_input_id: str,
    approved_input_sha256: str,
    require_frozen: bool = False,
    approved_task_class: TaskClass | None = None,
    approved_language: Language | None = None,
) -> ProtectedSemanticContract:
    contract = ProtectedSemanticContract.model_validate(contract.model_dump(mode="python"))
    if contract.family_id != approved_family_id:
        raise ValueError("protected contract family binding does not match approved input")
    if contract.scenario_input_id != approved_input_id:
        raise ValueError("protected contract input binding does not match approved input")
    if contract.scenario_input_sha256 != approved_input_sha256:
        raise ValueError("protected contract input hash does not match approved input")
    if require_frozen and contract.artifact.state != ProtectedArtifactState.FROZEN:
        raise ValueError("score contract is not frozen")
    if approved_task_class is not None and contract.task_class != approved_task_class:
        raise ValueError("protected contract task class does not match approved input")
    if approved_language is not None and contract.language != approved_language:
        raise ValueError("protected contract language does not match approved input")
    return contract


def validate_successor(prior: ProtectedArtifact, successor: ProtectedArtifact) -> ProtectedArtifact:
    if not isinstance(prior, ProtectedArtifact) or not isinstance(successor, ProtectedArtifact):
        raise TypeError("successor validation requires protected artifacts")
    try:
        prior = ProtectedArtifact.model_validate(prior.model_dump(mode="python"))
        successor = ProtectedArtifact.model_validate(successor.model_dump(mode="python"))
    except ValueError as exc:
        raise ValueError("successor artifact is invalid") from exc
    if prior.state != ProtectedArtifactState.FROZEN:
        raise ValueError("only a frozen artifact can have a successor")
    if successor.state != ProtectedArtifactState.DRAFT:
        raise ValueError("successor must begin in draft state")
    if (
        successor.artifact_id == prior.artifact_id
        or successor.content_sha256 == prior.content_sha256
    ):
        raise ValueError("successor must have a new identity and hash")
    if successor.supersedes_artifact_id != prior.artifact_id:
        raise ValueError("successor must identify the superseded artifact")
    if successor.root_reference.root_id != prior.root_reference.root_id:
        raise ValueError("successor must retain the protected root")
    return successor


__all__ = ["validate_protected_contract", "validate_successor"]
