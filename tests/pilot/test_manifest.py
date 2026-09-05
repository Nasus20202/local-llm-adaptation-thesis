from __future__ import annotations

import pytest

from tests.pilot.manifests import balanced_manifest, family
from thesis_bench.pilot import (
    FamilyRecord,
    Language,
    ProtectedArtifactReference,
    TaskClass,
    model_facing_manifest,
    validate_composition,
    validate_pilot_manifest,
)
from thesis_bench.records import ProtectedRootReference


def test_balanced_development_manifest_passes_and_nested_variant_is_not_counted() -> None:
    manifest = balanced_manifest()

    report = validate_composition(manifest)

    assert report.valid is True
    assert report.independent_family_count == 24
    assert report.nested_variant_count == 1


def test_pilot_manifest_validation_entry_point_accepts_models_and_json_mappings() -> None:
    manifest = balanced_manifest()

    assert validate_pilot_manifest(manifest).manifest_id == manifest.manifest_id
    parsed = validate_pilot_manifest(manifest.model_dump(mode="json"))
    assert parsed.manifest_id == manifest.manifest_id


def test_composition_reports_each_class_and_language_deviation() -> None:
    manifest = balanced_manifest()
    families = list(manifest.families)
    families[-1] = family(24, TaskClass.KNOWLEDGE, Language.PL)
    altered = manifest.model_copy(update={"families": tuple(families)})

    with pytest.raises(ValueError) as raised:
        validate_composition(altered)

    message = str(raised.value)
    assert "task_class" in message
    assert "language" in message


def test_final_test_and_nested_family_miscounts_are_rejected() -> None:
    with pytest.raises(ValueError):
        FamilyRecord.model_validate(
            family(1, TaskClass.KNOWLEDGE, Language.EN).model_dump() | {"split": "final-test"}
        )

    manifest = balanced_manifest()
    nested_as_independent = manifest.variants[0].model_copy(update={"counts_as_independent": True})
    with pytest.raises(ValueError, match="nested"):
        validate_composition(manifest.model_copy(update={"variants": (nested_as_independent,)}))


def test_family_contract_rejects_untyped_target_and_comparator_drift() -> None:
    record = family(1, TaskClass.KNOWLEDGE, Language.EN).model_dump(mode="json")
    record["target_stratum"] = "whatever"
    record["comparator"] = "completely-arbitrary"

    with pytest.raises(ValueError):
        FamilyRecord.model_validate(record)


def test_family_contract_enforces_condition_specific_comparator_matrix() -> None:
    record = family(1, TaskClass.KNOWLEDGE, Language.EN).model_dump(mode="json")
    record["condition_applicability"] = [
        {**item, "applicable": item["condition"] in {"B0", "P2"}, "reason": None}
        if item["condition"] in {"B0", "P2"}
        else item
        for item in record["condition_applicability"]
    ]
    record["target_stratum"]["conditions"] = ["B0", "P2"]
    record["analysis_contracts"] = [
        record["analysis_contracts"][0],
        {
            "schema_version": 1,
            "condition": "P2",
            "target_stratum": record["target_stratum"],
            "comparators": [
                {
                    "schema_version": 1,
                    "comparator_id": "wrong-p2-comparator",
                    "condition": "B0",
                    "design_rule": "wrong-rule",
                }
            ],
        },
    ]

    with pytest.raises(ValueError, match="P2"):
        FamilyRecord.model_validate(record)


def test_c2_family_contract_rejects_outcome_selected_strongest_constituent() -> None:
    record = family(1, TaskClass.KNOWLEDGE, Language.EN).model_dump(mode="python")
    target = {**record["target_stratum"], "conditions": ("B0", "C2")}
    record["target_stratum"] = target
    record["condition_applicability"] = tuple(
        {**item, "applicable": item["condition"] in {"B0", "C2"}, "reason": None}
        if item["condition"] in {"B0", "C2"}
        else item
        for item in record["condition_applicability"]
    )
    record["analysis_contracts"] = (
        {
            **record["analysis_contracts"][0],
            "target_stratum": target,
        },
        {
            "schema_version": 1,
            "condition": "C2",
            "target_stratum": target,
            "comparators": (
                {
                    "schema_version": 1,
                    "comparator_id": "outcome-selected-c2",
                    "condition": "R1",
                    "design_rule": "strongest-constituent-v1",
                    "selection_order": ("P1", "R1"),
                },
            ),
        },
    )

    with pytest.raises(ValueError, match="frozen strongest"):
        FamilyRecord.model_validate(record)


def test_model_facing_manifest_rejects_protected_markers_but_allows_references() -> None:
    manifest = balanced_manifest()
    reference = ProtectedArtifactReference(
        schema_version=1,
        artifact_id="rubric-1",
        artifact_kind="rubric",
        root_reference={
            "schema_version": 1,
            "root_id": "protected-evaluator",
            "relative_path": "rubrics/rubric-1.json",
            "content_sha256": "d" * 64,
        },
    )
    safe = model_facing_manifest(manifest, protected_references=(reference,))
    assert "rubric-1" in safe

    public_evaluator_reference = reference.model_copy(
        update={
            "artifact_id": "evaluator-1",
            "artifact_kind": "evaluator",
            "root_reference": ProtectedRootReference(
                schema_version=1,
                root_id="protected-evaluator",
                relative_path=(
                    "data/benchmark/development/protected-evaluator/dev-k-pl-01/contract.json"
                ),
                content_sha256="d" * 64,
            ),
        }
    )
    with pytest.raises(ValueError, match="cannot enter model-facing"):
        model_facing_manifest(manifest, protected_references=(public_evaluator_reference,))

    with pytest.raises(ValueError) as raised:
        model_facing_manifest(manifest.model_dump() | {"golden": "synthetic-secret"})
    assert "synthetic-secret" not in str(raised.value)
    with pytest.raises(ValueError):
        model_facing_manifest(manifest.model_dump() | {"protected_path": "final-test/items"})
