from __future__ import annotations

import hashlib
import json

from ..errors import ConfigurationError
from ..schemas import MetadataDocument


def canonical_json_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(
            "invalid_configuration", "metadata cannot be canonicalized"
        ) from exc


def source_sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def semantic_sha256(document: MetadataDocument) -> str:
    return hashlib.sha256(canonical_json_bytes(document.model_dump(mode="json"))).hexdigest()
