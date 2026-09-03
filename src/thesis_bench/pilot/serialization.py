from __future__ import annotations

import json
from pathlib import Path

from ..records import canonical_json_bytes
from .composition import validate_composition
from .manifest import PilotManifest
from .models import ProtectedArtifactReference


def load_pilot_manifest(path: Path, *, require_composition: bool = False) -> PilotManifest:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        manifest = validate_pilot_manifest(raw, require_composition=require_composition)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError("pilot manifest validation failed") from exc
    return manifest


def validate_pilot_manifest(
    manifest: PilotManifest | dict[str, object], *, require_composition: bool = False
) -> PilotManifest:
    try:
        parsed = PilotManifest.model_validate(
            _tuplify(
                manifest.model_dump(mode="python")
                if isinstance(manifest, PilotManifest)
                else manifest
            )
        )
        if require_composition:
            validate_composition(parsed)
    except (TypeError, ValueError) as exc:
        raise ValueError("pilot manifest validation failed") from exc
    return parsed


def _tuplify(value: object) -> object:
    if isinstance(value, list):
        return tuple(_tuplify(item) for item in value)
    if isinstance(value, dict):
        return {key: _tuplify(item) for key, item in value.items()}
    return value


def _contains_protected_marker(value: object) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in {
                "golden",
                "golden_answer",
                "expected_answer",
                "expected_result",
                "evidence_map",
                "rubric",
                "adjudication",
                "adjudication_notes",
                "protected_payload",
            }:
                return True
            if _contains_protected_marker(item):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_contains_protected_marker(item) for item in value)
    elif isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in ("final-test", "golden", "expected_answer"))
    return False


def model_facing_manifest(
    manifest: PilotManifest | dict[str, object],
    *,
    protected_references: tuple[ProtectedArtifactReference, ...] = (),
) -> str:
    validated = validate_pilot_manifest(manifest)
    raw = validated.model_dump(mode="json")
    if _contains_protected_marker(raw):
        raise ValueError("protected content cannot enter model-facing manifest")
    result: dict[str, object] = dict(raw)
    if protected_references:
        result["protected_artifact_references"] = [
            reference.model_dump(mode="json") for reference in protected_references
        ]
    return canonical_json_bytes(result).decode("utf-8")
