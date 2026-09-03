from __future__ import annotations

from thesis_bench.cluster import (
    ClusterPolicy,
    PinnedEnvironment,
)


def environment(**updates: object) -> PinnedEnvironment:
    values: dict[str, object] = {
        "schema_version": 1,
        "kind_revision": "kind-v1.2.3",
        "node_image_digest": "sha256:" + "a" * 64,
        "workload_image_digests": ("sha256:" + "b" * 64,),
        "cluster_config_sha256": "c" * 64,
        "host_runtime_identity": "runtime-v1",
        "namespace": "synthetic-isolated",
        "reset_policy": "recreate-v1",
        "validator_version": "validator-v1",
    }
    values.update(updates)
    return PinnedEnvironment(**values)


def policy(**updates: object) -> ClusterPolicy:
    values: dict[str, object] = {
        "schema_version": 1,
        "policy_id": "neutral-policy-1",
        "namespace": "synthetic-isolated",
        "allowed_commands": ("inspect", "repair"),
        "allowed_permissions": ("read", "namespaced-write"),
        "allowed_observations": ("status",),
        "context_budget": 100,
        "max_actions": 3,
        "max_output_bytes": 200,
        "max_duration_seconds": 30,
        "allow_privileged": False,
        "allow_host_mounts": False,
        "allow_cluster_scope": False,
        "allow_egress": False,
    }
    values.update(updates)
    return ClusterPolicy(**values)
