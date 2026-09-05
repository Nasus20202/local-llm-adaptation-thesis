from __future__ import annotations

import inspect

import pytest

from thesis_bench.evaluation.protected import (
    CriterionDisposition,
    Language,
    MetamorphicVariantKind,
    QualificationThresholds,
    TaskClass,
    check_copying_neutral_fairness,
    derive_primary_score,
    validate_fairness_coverage,
)
from thesis_bench.records import DecisionStatus

from .fairness_fixtures import fairness_group
from .fixtures import assessment
from .judge_fixtures import judge_configuration, judge_fairness_case, rehash_judge_configuration


def test_copying_neutral_fairness_relations_are_checked_without_text_similarity() -> None:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
    )
    case = judge_fairness_case(config)
    qualification = check_copying_neutral_fairness(case)
    assert qualification.status == DecisionStatus.GO
    assert qualification.violations == ()

    bad = case.model_copy(
        update={
            "variants": {
                **case.variants,
                MetamorphicVariantKind.CORRECT_SOURCE_LIKE: tuple(
                    assessment(item.criterion_id, CriterionDisposition.NOT_SATISFIED)
                    for item in case.variants[MetamorphicVariantKind.CORRECT_SOURCE_LIKE]
                ),
            }
        }
    )
    failed = check_copying_neutral_fairness(bad)
    assert failed.status == DecisionStatus.AMEND
    assert failed.violations

    appended_irrelevant_claim = case.model_copy(
        update={
            "variants": {
                **case.variants,
                MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED: tuple(
                    assessment(
                        item.criterion_id,
                        CriterionDisposition.NOT_SATISFIED
                        if item.criterion_id == "claim-a"
                        else item.disposition,
                        item.source,
                        judge_config_id=config.judge_config_id,
                    )
                    for item in case.variants[MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED]
                ),
            },
            "primary_scores": {
                **getattr(case, "primary_scores", {}),
                MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED: 0.5,
            },
        }
    )
    assert check_copying_neutral_fairness(appended_irrelevant_claim).status == DecisionStatus.GO


def test_fairness_coverage_requires_all_knowledge_mixed_language_cells_and_six_variants() -> None:
    groups = tuple(
        fairness_group(task_class, language)
        for task_class in (TaskClass.KNOWLEDGE, TaskClass.MIXED)
        for language in (Language.PL, Language.EN)
    )
    assert validate_fairness_coverage(groups) == groups
    extra_rule_group = groups[0].model_copy(update={"group_id": "group-extra-rule"})
    assert validate_fairness_coverage(
        groups + (extra_rule_group,), required_rule_ids=("synthetic-rule",)
    )
    with pytest.raises(ValueError):
        validate_fairness_coverage(groups[:-1])
    duplicate = groups[:-1] + (groups[0].model_copy(update={"group_id": groups[0].group_id}),)
    with pytest.raises(ValueError):
        validate_fairness_coverage(duplicate)


def test_score_kernel_has_no_similarity_or_confidence_feature_parameters() -> None:
    forbidden = {
        "token_overlap",
        "ngram_overlap",
        "edit_distance",
        "rouge",
        "bleu",
        "source_similarity",
        "embedding_similarity",
        "judge_confidence",
    }
    assert forbidden.isdisjoint(set(inspect.signature(derive_primary_score).parameters))
