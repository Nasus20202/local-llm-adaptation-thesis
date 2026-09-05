from __future__ import annotations

import json
from collections.abc import Mapping
from enum import StrEnum
from functools import lru_cache
from importlib.resources import files
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Literal

from pydantic import ConfigDict, field_validator, model_validator
from pydantic.types import StrictStr

from ...records import VersionedRecord
from ...schemas import Identifier, NonBlankStr, Sha256


@lru_cache(maxsize=1)
def protected_policy() -> Mapping[str, object]:
    raw = files(__package__).joinpath("policy.json").read_text(encoding="utf-8")
    parsed = json.loads(raw)
    policy = _freeze(parsed)
    if not isinstance(policy, Mapping) or policy.get("schema_version") != 1:
        raise RuntimeError("protected evaluator policy is invalid")
    return policy


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


_POLICY = protected_policy()
APPROVED_PROTECTED_ROOT = str(_POLICY["protected_root"])
APPROVED_SOURCE_RIGHTS_MANIFEST = str(_POLICY["source_rights_manifest"])
APPROVED_PREAUTHORING_FREEZE = str(_POLICY["preauthoring_freeze"])
APPROVED_EVALUATION_CLARIFICATION = str(_POLICY["evaluation_clarification"])
KUBERNETES_RELEASE = str(_POLICY["kubernetes_release"])
_inventories = _POLICY["source_inventories"]
if not isinstance(_inventories, Mapping):
    raise RuntimeError("protected evaluator source inventories are invalid")
_INVENTORIES: Mapping[str, object] = _inventories


def _inventory(inventory_id: str) -> Mapping[str, object]:
    inventory = _INVENTORIES.get(inventory_id)
    if not isinstance(inventory, Mapping):
        raise ValueError("source identity is outside the frozen source inventory")
    return inventory


def validate_protected_relative_path(value: str) -> str:
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
        or PurePosixPath(value).as_posix() != value
    ):
        raise ValueError("protected reference path must be canonical and root-relative")
    return value


class SourceKind(StrEnum):
    WEBSITE_MARKDOWN = "website_markdown"
    OPENAPI_SCHEMA = "openapi_schema"


class _ProtectedSourceRecord(VersionedRecord):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, hide_input_in_errors=True)


class FrozenSourceIdentity(_ProtectedSourceRecord):
    source_entry_id: Identifier
    source_registry_id: NonBlankStr
    inventory_id: NonBlankStr
    source_kind: SourceKind
    repository: NonBlankStr
    release: NonBlankStr
    revision: StrictStr
    path_or_selector: NonBlankStr
    git_blob_sha1: StrictStr
    content_sha256: Sha256
    content_index_sha256: Sha256 | None = None

    @field_validator("source_kind", mode="before")
    @classmethod
    def parse_source_kind(cls, value: object) -> object:
        return SourceKind(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_source_shape(self) -> FrozenSourceIdentity:
        if self.source_registry_id != APPROVED_SOURCE_RIGHTS_MANIFEST:
            raise ValueError("source identity is outside the approved rights manifest")
        inventory = _inventory(self.inventory_id)
        if self.release != KUBERNETES_RELEASE:
            raise ValueError("source identity release is not frozen")
        if self.source_kind.value != inventory.get("source_kind"):
            raise ValueError("source identity kind does not match its inventory")
        if self.repository != inventory.get("repository") or self.revision != inventory.get(
            "revision"
        ):
            raise ValueError("source identity revision is outside the frozen inventory")
        if self.inventory_id.startswith("website-"):
            paths = inventory.get("allowed_paths", ())
            if not isinstance(paths, (tuple, list)) or self.path_or_selector not in paths:
                raise ValueError("source path is outside the frozen website inventory")
            if self.content_index_sha256 != inventory.get("content_index_sha256"):
                raise ValueError("website content index does not match the frozen inventory")
            known = inventory.get("exact_hashes", {})
            if not isinstance(known, Mapping) or self.path_or_selector not in known:
                raise ValueError("website source file hash is not frozen")
            expected = known[self.path_or_selector]
            if not isinstance(expected, Mapping) or (
                self.git_blob_sha1 != expected.get("git_blob_sha1")
                or self.content_sha256 != expected.get("content_sha256")
            ):
                raise ValueError("source identity hash does not match the frozen source")
        else:
            if (
                self.path_or_selector != inventory.get("path_or_selector")
                or self.git_blob_sha1 != inventory.get("git_blob_sha1")
                or self.content_sha256 != inventory.get("content_sha256")
                or self.content_index_sha256 is not None
            ):
                raise ValueError("source identity is outside the frozen OpenAPI inventory")
        if len(self.revision) != 40 or any(
            char not in "0123456789abcdef" for char in self.revision
        ):
            raise ValueError("source revision must be a lowercase SHA-1")
        if len(self.git_blob_sha1) != 40 or any(
            char not in "0123456789abcdef" for char in self.git_blob_sha1
        ):
            raise ValueError("source blob identity must be a lowercase SHA-1")
        return self


def reject_reviewer_note(value: object) -> object:
    if isinstance(value, str):
        lowered = value.lower()
        if "expected answer" in lowered or "reviewer note" in lowered:
            raise ValueError("reviewer convenience notes cannot provide evaluator truth")
    elif isinstance(value, Mapping):
        for key, item in value.items():
            reject_reviewer_note(key)
            reject_reviewer_note(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            reject_reviewer_note(item)
    return value


class SourceEvidenceReference(_ProtectedSourceRecord):
    evidence_id: Identifier
    source: FrozenSourceIdentity
    source_role: Literal["construction", "deterministic", "semantic", "qualification"]

    @model_validator(mode="after")
    def reject_convenience_note(self) -> SourceEvidenceReference:
        reject_reviewer_note(self.model_dump(mode="python"))
        return self


def validate_source_identity(source: FrozenSourceIdentity) -> FrozenSourceIdentity:
    return FrozenSourceIdentity.model_validate(source.model_dump(mode="python"))


__all__ = [
    "APPROVED_EVALUATION_CLARIFICATION",
    "APPROVED_PREAUTHORING_FREEZE",
    "APPROVED_PROTECTED_ROOT",
    "APPROVED_SOURCE_RIGHTS_MANIFEST",
    "FrozenSourceIdentity",
    "KUBERNETES_RELEASE",
    "SourceEvidenceReference",
    "SourceKind",
    "protected_policy",
    "reject_reviewer_note",
    "validate_protected_relative_path",
    "validate_source_identity",
]
