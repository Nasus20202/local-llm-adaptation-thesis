from __future__ import annotations

from ....pilot.models import Language, TaskClass
from ....records import DecisionStatus
from ..contracts.config import (
    KnowledgeScoreConfiguration,
    MixedScoreConfiguration,
    ProceduralScoreConfiguration,
)
from ..contracts.records import CriterionRole
from ..scoring.assessment import CriterionAssessment, CriterionDisposition
from ..scoring.kernel import derive_primary_score_from_dispositions
from .records import (
    FairnessQualification,
    JudgeFairnessCase,
    MetamorphicFixtureGroup,
    MetamorphicVariantKind,
)


def _dispositions(assessments: tuple[CriterionAssessment, ...]) -> dict[str, CriterionDisposition]:
    result = {item.criterion_id: item.disposition for item in assessments}
    if len(result) != len(assessments):
        raise ValueError("fairness variants cannot duplicate criterion assessments")
    return result


def _required_rule_ids(case: JudgeFairnessCase) -> frozenset[str]:
    config = case.contract.score_configuration
    if isinstance(config, KnowledgeScoreConfiguration):
        return frozenset(config.required_criterion_ids) | frozenset(
            config.unsupported_criterion_ids
        )
    if isinstance(config, ProceduralScoreConfiguration):
        return frozenset(config.primary_required_criterion_ids) | frozenset(
            config.primary_prohibited_criterion_ids
        )
    if isinstance(config, MixedScoreConfiguration):
        return frozenset(config.primary_hard_gate_criterion_ids) | frozenset(config.point_table)
    raise ValueError("fairness contract has an unsupported score configuration")


def _score_variants(case: JudgeFairnessCase) -> dict[MetamorphicVariantKind, float]:
    return {
        kind: derive_primary_score_from_dispositions(
            case.contract, _dispositions(assessments)
        ).score
        for kind, assessments in case.variants.items()
    }


def _disposition_improved(
    case: JudgeFairnessCase,
    criterion_id: str,
    before: CriterionDisposition,
    after: CriterionDisposition,
) -> bool:
    criterion = next(item for item in case.contract.criteria if item.criterion_id == criterion_id)
    if CriterionRole.UNSUPPORTED_OR_CONTRADICTORY in criterion.roles:
        ranks = {
            CriterionDisposition.UNRESOLVED: 0,
            CriterionDisposition.SATISFIED: 0,
            CriterionDisposition.CONTRADICTED: 0,
            CriterionDisposition.NOT_SATISFIED: 1,
        }
    else:
        ranks = {
            CriterionDisposition.UNRESOLVED: 0,
            CriterionDisposition.CONTRADICTED: 1,
            CriterionDisposition.NOT_SATISFIED: 2,
            CriterionDisposition.SATISFIED: 3,
        }
    return ranks[after] > ranks[before]


def check_copying_neutral_fairness(case: JudgeFairnessCase) -> FairnessQualification:
    violations: list[str] = []
    try:
        scores = _score_variants(case)
    except ValueError:
        return FairnessQualification(
            schema_version=1,
            status=DecisionStatus.AMEND,
            violations=("invalid-fairness-score-input",),
        )
    if not _required_rule_ids(case) <= case.exercised_rule_ids():
        violations.append("missing-scoring-rule-coverage")
    variants = case.variants
    equivalent = (
        MetamorphicVariantKind.CONCISE_CORRECT_PARAPHRASE,
        MetamorphicVariantKind.CORRECT_SOURCE_LIKE,
        MetamorphicVariantKind.ACCEPTED_SYNONYM_REORDERING,
    )
    baseline = _dispositions(variants[equivalent[0]])
    for kind in equivalent[1:]:
        observed = _dispositions(variants[kind])
        if observed != baseline:
            violations.append(f"non-equivalent-{kind.value}")
        if scores[kind] != scores[equivalent[0]]:
            violations.append(f"non-equivalent-primary-score-{kind.value}")

    appended = MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED
    appended_dispositions = _dispositions(variants[appended])
    if scores[appended] > scores[equivalent[0]]:
        violations.append("irrelevant-source-improved-primary-score")
    for criterion_id, disposition in appended_dispositions.items():
        if criterion_id in baseline and _disposition_improved(
            case, criterion_id, baseline[criterion_id], disposition
        ):
            violations.append(f"irrelevant-source-improved-{criterion_id}")

    for kind in (
        MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG,
        MetamorphicVariantKind.PARTIAL_MISSING_CLAIM,
    ):
        observed = _dispositions(variants[kind])
        if scores[kind] >= scores[equivalent[0]]:
            violations.append(f"not-worse-primary-score-{kind.value}")
        changed = {
            criterion_id
            for criterion_id, disposition in observed.items()
            if disposition != baseline.get(criterion_id)
        }
        if not changed:
            violations.append(f"missing-affected-criterion-{kind.value}")
        if any(
            observed[criterion_id] == CriterionDisposition.SATISFIED for criterion_id in changed
        ):
            violations.append(f"rescued-{kind.value}")
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
    covered = {rule_id for group in groups for rule_id in group.scoring_rule_ids()}
    if not set(required_rule_ids) <= covered:
        raise ValueError("fairness fixtures do not cover every required scoring rule")
    return tuple(groups)


__all__ = ["check_copying_neutral_fairness", "validate_fairness_coverage"]
