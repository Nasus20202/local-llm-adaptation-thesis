from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from ..errors import ConfigurationError
from ..schemas import MetadataDocument
from .yaml_source import _MODELS


def _safe_validation_error(path: Path, error: ValidationError) -> ConfigurationError:
    first = error.errors()[0]
    location = ".".join(str(part) for part in first.get("loc", ())) or str(path)
    error_type = first.get("type")
    if error_type == "extra_forbidden":
        message = "unknown field"
    elif error_type == "missing":
        message = "required field is missing"
    elif error_type == "literal_error" and location == "schema_version":
        message = "unsupported schema version"
    else:
        message = "invalid field"
    return ConfigurationError("invalid_configuration", message, location=f"{path}:{location}")


def validate_document(
    raw: dict[str, object], path: Path, expected_kind: str | None = None
) -> MetadataDocument:
    kind = raw.get("kind")
    if not isinstance(kind, str) or kind not in _MODELS:
        raise ConfigurationError(
            "invalid_configuration", "unknown metadata kind", location=str(path)
        )
    if expected_kind is not None and kind != expected_kind:
        raise ConfigurationError(
            "invalid_configuration",
            "metadata kind does not match reference",
            location=f"{path}:kind",
        )
    model = _MODELS[kind]
    try:
        return model.model_validate(raw)
    except ValidationError as exc:
        raise _safe_validation_error(path, exc) from exc
