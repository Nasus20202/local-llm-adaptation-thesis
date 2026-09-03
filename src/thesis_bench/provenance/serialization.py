from __future__ import annotations

import hashlib
import json

from pydantic import ValidationError

from ..errors import IntegrityError
from .models import Manifest


def _canonical_manifest_bytes(manifest: Manifest) -> bytes:
    try:
        text = json.dumps(
            manifest.model_dump(mode="json"),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise IntegrityError("invalid_manifest", "manifest cannot be canonicalized") from exc
    return text.encode("utf-8") + b"\n"


def manifest_to_bytes(manifest: Manifest) -> bytes:
    return _canonical_manifest_bytes(manifest)


def manifest_semantic_sha256(manifest: Manifest) -> str:
    return hashlib.sha256(_canonical_manifest_bytes(manifest)[:-1]).hexdigest()


def load_manifest(source: bytes) -> Manifest:
    try:
        manifest = Manifest.model_validate_json(source)
    except (ValueError, ValidationError) as exc:
        raise IntegrityError("invalid_manifest", "stored manifest is invalid") from exc
    return manifest
