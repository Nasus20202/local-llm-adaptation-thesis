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

from .fixtures import artifact, input_binding, knowledge_contract


def procedural_contract() -> ProtectedSemanticContract:
    base = knowledge_contract()
    binding = input_binding(TaskClass.PROCEDURAL)
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
            "family_id": binding.family_id,
            "scenario_input_id": binding.scenario_input_id,
            "scenario_input_sha256": binding.input_sha256,
            "criteria": criteria,
            "predicates": (
                DeterministicPredicate(
                    schema_version=1,
                    predicate_id="predicate-state",
                    criterion_id="required-state",
                    predicate_kind="final_state",
                    predicate_version="predicate-v1",
                    final_state_id="state-complete",
                ),
                DeterministicPredicate(
                    schema_version=1,
                    predicate_id="predicate-action",
                    criterion_id="prohibited-action",
                    predicate_kind="action_bound",
                    predicate_version="predicate-v1",
                    action_rule_id="action-prohibited",
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
    binding = input_binding(TaskClass.MIXED)
    criteria = (*base.criteria,)
    criteria += (
        ProtectedCriterion(
            schema_version=1,
            criterion_id="semantic-point",
            roles=(
                CriterionRole.SCORE_BEARING,
                CriterionRole.SEMANTIC,
                CriterionRole.DETERMINISTIC,
            ),
            deterministic_predicate_id="predicate-semantic-point",
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
            "family_id": binding.family_id,
            "scenario_input_id": binding.scenario_input_id,
            "scenario_input_sha256": binding.input_sha256,
            "criteria": criteria,
            "semantic_criteria": (
                SemanticCriterion(
                    schema_version=1, criterion_id="semantic-point", anchor_id="anchor-point"
                ),
            ),
            "predicates": (
                *base.predicates,
                DeterministicPredicate(
                    schema_version=1,
                    predicate_id="predicate-semantic-point",
                    criterion_id="semantic-point",
                    predicate_kind="custom",
                    predicate_version="predicate-v1",
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
