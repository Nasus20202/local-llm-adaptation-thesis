from __future__ import annotations

from ....pilot.models import Language, TaskClass
from ....records import DecisionStatus
from ..scoring.assessment import CriterionDisposition
from .records import (
    FairnessQualification,
    JudgeFairnessCase,
    MetamorphicFixtureGroup,
    MetamorphicVariantKind,
)


def check_copying_neutral_fairness(case: JudgeFairnessCase) -> FairnessQualification:
    variants = case.variants
    violations: list[str] = []

    def dispositions(kind: MetamorphicVariantKind) -> dict[str, CriterionDisposition]:
        return {item.criterion_id: item.disposition for item in variants[kind]}

    equivalent = (
        MetamorphicVariantKind.CONCISE_CORRECT_PARAPHRASE,
        MetamorphicVariantKind.CORRECT_SOURCE_LIKE,
        MetamorphicVariantKind.ACCEPTED_SYNONYM_REORDERING,
    )
    if any(kind not in variants for kind in equivalent):
        violations.append("missing-equivalent-variant")
    else:
        baseline = dispositions(equivalent[0])
        for kind in equivalent[1:]:
            if dispositions(kind) != baseline:
                violations.append(f"non-equivalent-{kind.value}")
        baseline_score = case.primary_scores[equivalent[0]]
        for kind in equivalent[1:]:
            if case.primary_scores[kind] != baseline_score:
                violations.append(f"non-equivalent-primary-score-{kind.value}")
    appended = MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED
    if appended not in variants:
        violations.append(f"missing-{appended.value}")
    elif case.primary_scores[appended] > case.primary_scores[equivalent[0]]:
        violations.append("irrelevant-source-improved-primary-score")
    else:
        baseline = dispositions(equivalent[0])
        observed = dispositions(appended)
        ranks = {
            CriterionDisposition.UNRESOLVED: 0,
            CriterionDisposition.CONTRADICTED: 1,
            CriterionDisposition.NOT_SATISFIED: 2,
            CriterionDisposition.SATISFIED: 3,
        }
        for criterion_id, disposition in observed.items():
            baseline_disposition = baseline.get(criterion_id, CriterionDisposition.UNRESOLVED)
            if ranks[disposition] > ranks[baseline_disposition]:
                violations.append(f"irrelevant-source-improved-{criterion_id}")
    for kind in (
        MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG,
        MetamorphicVariantKind.PARTIAL_MISSING_CLAIM,
    ):
        if kind not in variants:
            violations.append(f"missing-{kind.value}")
            continue
        observed = dispositions(kind)
        if (
            case.primary_scores[kind]
            >= case.primary_scores[MetamorphicVariantKind.CONCISE_CORRECT_PARAPHRASE]
        ):
            violations.append(f"not-worse-primary-score-{kind.value}")
        for criterion_id in case.affected_criterion_ids.get(kind, ()):
            if observed.get(criterion_id) == CriterionDisposition.SATISFIED:
                violations.append(f"rescued-{kind.value}-{criterion_id}")
    return FairnessQualification(
        schema_version=1,
        status=DecisionStatus.GO if not violations else DecisionStatus.AMEND,
        violations=tuple(violations),
    )


def validate_fairness_coverage(
    groups: tuple[MetamorphicFixtureGroup, ...] | list[MetamorphicFixtureGroup],
    *,
    required_rule_ids: tuple[str, ...] = (),
) -> tuple[MetamorphicFixtureGroup, ...]:
    expected = {
        (task_class, language)
        for task_class in (TaskClass.KNOWLEDGE, TaskClass.MIXED)
        for language in Language
    }
    observed = {(group.task_class, group.language) for group in groups}
    if observed != expected or len({group.group_id for group in groups}) != len(groups):
        raise ValueError("fairness fixtures must cover each task-class/language cell")
    covered = {rule_id for group in groups for rule_id in group.covered_rule_ids}
    if not set(required_rule_ids) <= covered:
        raise ValueError("fairness fixtures do not cover every required scoring rule")
    return tuple(groups)


__all__ = ["check_copying_neutral_fairness", "validate_fairness_coverage"]
