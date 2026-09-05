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
        MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED,
    )
    if any(kind not in variants for kind in equivalent):
        violations.append("missing-equivalent-variant")
    else:
        baseline = dispositions(equivalent[0])
        for kind in equivalent[1:]:
            if dispositions(kind) != baseline:
                violations.append(f"non-equivalent-{kind.value}")
    for kind in (
        MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG,
        MetamorphicVariantKind.PARTIAL_MISSING_CLAIM,
    ):
        if kind not in variants:
            violations.append(f"missing-{kind.value}")
            continue
        observed = dispositions(kind)
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
) -> tuple[MetamorphicFixtureGroup, ...]:
    expected = {
        (task_class, language)
        for task_class in (TaskClass.KNOWLEDGE, TaskClass.MIXED)
        for language in Language
    }
    observed = {(group.task_class, group.language) for group in groups}
    if (
        observed != expected
        or len(observed) != len(groups)
        or len({group.group_id for group in groups}) != len(groups)
    ):
        raise ValueError("fairness fixtures must cover each task-class/language cell exactly once")
    return tuple(groups)


__all__ = ["check_copying_neutral_fairness", "validate_fairness_coverage"]
