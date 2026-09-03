from __future__ import annotations

from thesis_bench.pilot import (
    ComparatorRecord,
    ConditionAnalysisContract,
    ConditionApplicability,
    FamilyRecord,
    Language,
    PilotManifest,
    ProtectedArtifactReference,
    TargetStratumRecord,
    TaskClass,
    VariantRecord,
    VariantType,
)


def family(number: int, task_class: TaskClass, language: Language) -> FamilyRecord:
    return FamilyRecord(
        schema_version=1,
        family_id=f"family-{number:02d}",
        split="development",
        task_class=task_class,
        language=language,
        answer_contract={
            "schema_version": 1,
            "form": "structured-response",
            "deterministic_gates": ("format",),
            "candidate_primary_metric": "task-score",
        },
        metric_applicability={
            "schema_version": 1,
            "applicable_metrics": ("task-score",),
            "inapplicable_metrics": (),
            "inapplicability_reasons": {},
        },
        target_stratum=TargetStratumRecord(
            schema_version=1,
            stratum_id=f"{task_class.value}-{language.value}",
            conditions=("B0",),
            selection_rule="approved synthetic target-stratum rule",
        ),
        comparator=ComparatorRecord(
            schema_version=1,
            comparator_id="b0-reference",
            condition="B0",
            design_rule="approved reference-condition rule",
        ),
        analysis_contracts=(
            ConditionAnalysisContract(
                schema_version=1,
                condition="B0",
                target_stratum=TargetStratumRecord(
                    schema_version=1,
                    stratum_id=f"{task_class.value}-{language.value}",
                    conditions=("B0",),
                    selection_rule="approved synthetic target-stratum rule",
                ),
                comparators=(
                    ComparatorRecord(
                        schema_version=1,
                        comparator_id="b0-reference",
                        condition="B0",
                        design_rule="approved reference-condition rule",
                    ),
                ),
            ),
        ),
        condition_applicability=tuple(
            ConditionApplicability(
                schema_version=1,
                condition=condition,
                applicable=condition == "B0",
                reason=None if condition == "B0" else "not in this synthetic family stratum",
            )
            for condition in (
                "B0",
                "P1",
                "P2",
                "R1",
                "F1",
                "H1",
                "S1",
                "C1",
                "C2",
                "W1",
            )
        ),
        evaluator_references=(
            ProtectedArtifactReference(
                schema_version=1,
                artifact_id=f"evaluator-{number:02d}",
                artifact_kind="evaluator",
                root_reference={
                    "schema_version": 1,
                    "root_id": "protected-evaluators",
                    "relative_path": f"evaluators/evaluator-{number:02d}.json",
                    "content_sha256": "e" * 64,
                },
            ),
        ),
    )


def balanced_manifest() -> PilotManifest:
    families = tuple(
        family(index, task_class, language)
        for index, (task_class, language) in enumerate(
            (
                pair
                for task_class in TaskClass
                for language in (Language.PL, Language.EN)
                for pair in [(task_class, language)] * 4
            ),
            start=1,
        )
    )
    return PilotManifest(
        schema_version=1,
        manifest_id="pilot-manifest-1",
        policy_version="pilot-policy-v1",
        families=families,
        variants=(
            VariantRecord(
                schema_version=1,
                variant_id="variant-01",
                family_id="family-01",
                split="development",
                variant_type=VariantType.PROMPT_FORMULATION,
                repeat_index=0,
            ),
        ),
    )
