from __future__ import annotations

from thesis_bench.evaluation.identity import EvaluatorIdentity
from thesis_bench.evaluation.protected import (
    CriterionRole,
    DeterministicPredicate,
    MixedScoreConfiguration,
    ProceduralScoreConfiguration,
    ProtectedCriterion,
    ProtectedSemanticContract,
    SemanticCriterion,
    TaskClass,
)

from .fixtures import artifact, knowledge_contract


def procedural_contract() -> ProtectedSemanticContract:
    base = knowledge_contract()
    criteria = (
        ProtectedCriterion(
            schema_version=1,
            criterion_id="required-state",
            roles=(
                CriterionRole.PRIMARY_REQUIRED,
                CriterionRole.PRIMARY_HARD_GATE,
                CriterionRole.DETERMINISTIC,
            ),
            deterministic_predicate_id="predicate-state",
            evidence_ids=("evidence-a",),
        ),
        ProtectedCriterion(
            schema_version=1,
            criterion_id="prohibited-action",
            roles=(CriterionRole.PRIMARY_PROHIBITED, CriterionRole.DETERMINISTIC),
            deterministic_predicate_id="predicate-action",
            evidence_ids=("evidence-b",),
        ),
    )
    return base.model_copy(
        update={
            "artifact": artifact("procedural"),
            "evaluator_identity": EvaluatorIdentity(
                schema_version=1,
                identity_id="procedural-1",
                revision="v1",
                content_sha256="c" * 64,
            ),
            "task_class": TaskClass.PROCEDURAL,
            "criteria": criteria,
            "predicates": (
                DeterministicPredicate(
                    schema_version=1,
                    predicate_id="predicate-state",
                    criterion_id="required-state",
                    predicate_kind="final_state",
                    predicate_version="predicate-v1",
                ),
                DeterministicPredicate(
                    schema_version=1,
                    predicate_id="predicate-action",
                    criterion_id="prohibited-action",
                    predicate_kind="action_bound",
                    predicate_version="predicate-v1",
                ),
            ),
            "semantic_criteria": (),
            "score_configuration": ProceduralScoreConfiguration(
                schema_version=1,
                primary_required_criterion_ids=("required-state",),
                primary_prohibited_criterion_ids=("prohibited-action",),
            ),
        }
    )


def mixed_contract() -> ProtectedSemanticContract:
    base = procedural_contract()
    criteria = (*base.criteria,)
    criteria += (
        ProtectedCriterion(
            schema_version=1,
            criterion_id="semantic-point",
            roles=(CriterionRole.SCORE_BEARING, CriterionRole.SEMANTIC),
            evidence_ids=("evidence-a",),
        ),
    )
    return base.model_copy(
        update={
            "artifact": artifact("mixed"),
            "evaluator_identity": EvaluatorIdentity(
                schema_version=1,
                identity_id="mixed-1",
                revision="v1",
                content_sha256="c" * 64,
            ),
            "task_class": TaskClass.MIXED,
            "criteria": criteria,
            "semantic_criteria": (
                SemanticCriterion(
                    schema_version=1, criterion_id="semantic-point", anchor_id="anchor-point"
                ),
            ),
            "score_configuration": MixedScoreConfiguration(
                schema_version=1,
                primary_hard_gate_criterion_ids=("required-state",),
                point_table={"semantic-point": 2.0},
                positive_maximum=2.0,
            ),
        }
    )
