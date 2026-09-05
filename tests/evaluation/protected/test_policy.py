from __future__ import annotations

from collections.abc import Mapping

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    APPROVED_REPOSITORY_SUBTREE,
    FrozenSourceIdentity,
    is_repository_protected_path,
    protected_policy,
    validate_repository_protected_path,
)


def test_protected_policy_is_the_single_source_for_frozen_root_and_allowlist() -> None:
    policy = protected_policy()
    assert policy["protected_root"] == APPROVED_PROTECTED_ROOT
    inventories = policy["source_inventories"]
    assert isinstance(inventories, Mapping)
    website = inventories["website-v1.36.4-development-pilot-v1"]
    assert isinstance(website, Mapping)
    paths = website["allowed_paths"]
    assert isinstance(paths, tuple)
    assert len(paths) == len(set(paths)) == 44
    assert "content/en/docs/tasks/debug/debug-application/debug-statefulset.md" in paths
    assert "expected answer" not in str(policy).lower()

    with pytest.raises(TypeError):
        policy["protected_root"] = "other-root"  # type: ignore[index]


def test_website_source_requires_a_frozen_per_file_hash() -> None:
    with pytest.raises(ValueError, match="hash"):
        FrozenSourceIdentity(
            schema_version=1,
            source_entry_id="website-source-without-file-hash",
            source_registry_id="development-pilot-source-rights-v1",
            inventory_id="website-v1.36.4-development-pilot-v1",
            source_kind="website_markdown",
            repository="https://github.com/kubernetes/website",
            release="v1.36.4",
            revision="1de955ebabe7e17da1ebb4f582635491227f4157",
            path_or_selector="content/en/docs/concepts/configuration/configmap.md",
            git_blob_sha1="aa3e6ac3c18b995a2057bd1f8ca19eb6861606e7",
            content_sha256="2" * 64,
            content_index_sha256="ff6e098274f45cf35dd669d0de61e566129e891baad8e0e49d7fe6922c432127",
        )


def test_repository_binding_accepts_only_the_dedicated_subtree() -> None:
    valid = f"{APPROVED_REPOSITORY_SUBTREE}/dev-k-pl-01/contract.json"
    assert is_repository_protected_path(valid)
    assert validate_repository_protected_path(valid) == valid
    assert not is_repository_protected_path("data/benchmark/development/model-facing/x.json")
    with pytest.raises(ValueError, match="repository subtree"):
        validate_repository_protected_path("contracts/contract.json")
