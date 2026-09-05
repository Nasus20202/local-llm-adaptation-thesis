from __future__ import annotations

from collections.abc import Mapping

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    protected_policy,
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
