from __future__ import annotations

import pytest

from tests.pilot.c2 import c2_manifest
from thesis_bench.pilot import (
    C2EligibilityManifest,
    Language,
    TaskClass,
    validate_c2_eligibility,
)


def test_confirmatory_c2_requires_frozen_metadata_only_design_and_fresh_families() -> None:
    manifest = c2_manifest(eligibility_id="c2-eligibility-1")
    assert validate_c2_eligibility(manifest).analysis_status == "confirmatory"

    outcome_selected = manifest.model_copy(
        update={
            "eligibility_id": "c2-exploratory",
            "analysis_status": "confirmatory",
            "outcome_derived_fields": ("selected_from_failures",),
        }
    )
    with pytest.raises(ValueError):
        validate_c2_eligibility(outcome_selected)

    exploratory = c2_manifest(
        eligibility_id="c2-exploratory",
        analysis_status="exploratory",
        outcome_derived_fields=("selected_from_failures",),
    )
    assert validate_c2_eligibility(exploratory).analysis_status == "exploratory"
    with pytest.raises(ValueError):
        validate_c2_eligibility(manifest.model_copy(update={"confirmatory_follow_up": True}))
    with pytest.raises(ValueError):
        validate_c2_eligibility(
            manifest.model_copy(
                update={
                    "confirmatory_follow_up": True,
                    "excluded_family_ids": ("family-02",),
                }
            )
        )
    exploratory = c2_manifest(
        eligibility_id="c2-exploratory-linked",
        analysis_status="exploratory",
        outcome_derived_fields=("selected_from_failures",),
    )
    follow_up = c2_manifest(
        eligibility_id="c2-follow-up",
        confirmatory_follow_up=True,
        family_ids=("family-03", "family-04"),
        excluded_family_ids=exploratory.family_ids,
        exploratory_manifest_id=exploratory.eligibility_id,
    )
    assert (
        validate_c2_eligibility(follow_up, exploratory_manifest=exploratory).confirmatory_follow_up
        is True
    )


def test_confirmatory_c2_rejects_outcome_signals_in_metadata_or_comparator() -> None:
    manifest = c2_manifest(eligibility_id="c2-eligibility-2")
    candidate = manifest.model_copy(update={"outcome_derived_fields": ("selected_from_failures",)})
    with pytest.raises(ValueError):
        validate_c2_eligibility(candidate)


def test_c2_requires_a_typed_pre_outcome_freeze_identity() -> None:
    with pytest.raises(ValueError):
        C2EligibilityManifest.model_validate(
            {
                "schema_version": 1,
                "eligibility_id": "c2-missing-freeze",
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
                "analysis_status": "confirmatory",
            }
        )


def test_c2_rejects_untyped_outcome_descriptions_as_metadata() -> None:
    with pytest.raises(ValueError):
        C2EligibilityManifest(
            schema_version=1,
            eligibility_id="c2-outcome-metadata",
            family_ids=("family-01", "family-02"),
            metadata={
                "schema_version": 1,
                "task_classes": (TaskClass.MIXED,),
                "languages": (Language.EN,),
                "answer_contracts": ("structured-response",),
                "required_capabilities": ("prompt-control", "retrieval"),
                "declared_needs": ("selected_from_failures",),
                "target_stratum": "mixed",
            },
            constituent_conditions=("P1", "R1"),
            comparator={
                "schema_version": 1,
                "comparator_id": "c2-strongest-v1",
                "condition": "P1",
                "design_rule": "strongest-constituent-v1",
            },
            freeze_identity={
                "schema_version": 1,
                "artifact_id": "c2-preregistration-outcome",
                "artifact_revision": "v1",
                "content_sha256": "f" * 64,
                "stage": "pre_outcome",
            },
            analysis_status="confirmatory",
        )


def test_c2_freeze_hash_is_bound_to_the_canonical_declaration() -> None:
    manifest = c2_manifest(eligibility_id="c2-hash")
    changed = manifest.model_copy(
        update={"metadata": manifest.metadata.model_copy(update={"languages": (Language.PL,)})}
    )

    with pytest.raises(ValueError, match="C2 eligibility validation failed"):
        validate_c2_eligibility(changed)


def test_c2_rejects_outcome_independent_selector_order_alternatives() -> None:
    with pytest.raises(ValueError, match="selection order"):
        c2_manifest(eligibility_id="c2-order", selection_order=("R1", "P1"))


def test_c2_derives_follow_up_exclusion_from_linked_exploratory_manifest() -> None:
    exploratory = c2_manifest(
        eligibility_id="c2-exploratory-linked",
        analysis_status="exploratory",
        outcome_derived_fields=("selected_from_failures",),
        family_ids=("family-01", "family-02"),
    )
    overlapping_follow_up = c2_manifest(
        eligibility_id="c2-follow-up-overlap",
        family_ids=("family-01", "family-03"),
        confirmatory_follow_up=True,
        excluded_family_ids=("family-03",),
        exploratory_manifest_id=exploratory.eligibility_id,
    )

    with pytest.raises(ValueError, match="exploratory manifest"):
        validate_c2_eligibility(overlapping_follow_up, exploratory_manifest=exploratory)

    with pytest.raises(ValueError, match="exploratory manifest"):
        validate_c2_eligibility(overlapping_follow_up)


def test_c2_rejects_a_mutated_linked_exploratory_manifest() -> None:
    exploratory = c2_manifest(
        eligibility_id="c2-exploratory-hash-bound",
        analysis_status="exploratory",
        outcome_derived_fields=("selected_from_failures",),
    )
    mutated = exploratory.model_copy(update={"family_ids": ("family-11", "family-12")})
    follow_up = c2_manifest(
        eligibility_id="c2-follow-up-hash-bound",
        family_ids=("family-03", "family-04"),
        confirmatory_follow_up=True,
        excluded_family_ids=mutated.family_ids,
        exploratory_manifest_id=exploratory.eligibility_id,
    )

    with pytest.raises(ValueError, match="hash-bound"):
        validate_c2_eligibility(follow_up, exploratory_manifest=mutated)
