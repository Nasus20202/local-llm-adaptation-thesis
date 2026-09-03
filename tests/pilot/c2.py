from __future__ import annotations

from thesis_bench.pilot import (
    C2EligibilityManifest,
    C2EligibilityMetadata,
    C2FreezeIdentity,
    ComparatorRecord,
    Language,
    TaskClass,
)
from thesis_bench.records import content_sha256


def c2_manifest(
    *,
    eligibility_id: str,
    analysis_status: str = "confirmatory",
    outcome_derived_fields: tuple[str, ...] = (),
    confirmatory_follow_up: bool = False,
    excluded_family_ids: tuple[str, ...] = (),
    exploratory_manifest_id: str | None = None,
) -> C2EligibilityManifest:
    values: dict[str, object] = {
        "schema_version": 1,
        "eligibility_id": eligibility_id,
        "family_ids": ("family-01", "family-02"),
        "metadata": {
            "schema_version": 1,
            "task_classes": (TaskClass.MIXED,),
            "languages": (Language.EN,),
            "answer_contracts": ("structured-response",),
            "required_capabilities": ("prompt-control", "retrieval"),
            "declared_needs": ("evidence",),
            "target_stratum": "mixed",
        },
        "constituent_conditions": ("P1", "R1"),
        "comparator": {
            "schema_version": 1,
            "comparator_id": "c2-strongest-v1",
            "condition": "P1",
            "design_rule": "strongest-constituent-v1",
        },
        "analysis_status": analysis_status,
        "outcome_derived_fields": outcome_derived_fields,
        "confirmatory_follow_up": confirmatory_follow_up,
        "excluded_family_ids": excluded_family_ids,
        "exploratory_manifest_id": exploratory_manifest_id,
        "freeze_identity": {
            "schema_version": 1,
            "artifact_id": f"{eligibility_id}-preregistration",
            "artifact_revision": "v1",
            "content_sha256": "0" * 64,
            "stage": "pre_outcome",
        },
    }
    values["metadata"] = C2EligibilityMetadata(**values["metadata"])
    values["comparator"] = ComparatorRecord(**values["comparator"])
    values["freeze_identity"] = C2FreezeIdentity(**values["freeze_identity"])
    provisional = C2EligibilityManifest.model_construct(**values)
    declaration = provisional.model_dump(mode="json", exclude={"freeze_identity"})
    freeze_identity = C2FreezeIdentity.model_validate(values["freeze_identity"])
    values["freeze_identity"] = {
        **freeze_identity.model_dump(mode="json"),
        "content_sha256": content_sha256(
            {
                "declaration": declaration,
                "artifact_id": freeze_identity.artifact_id,
                "artifact_revision": freeze_identity.artifact_revision,
                "stage": freeze_identity.stage,
            }
        ),
    }
    return C2EligibilityManifest(**values)
