from __future__ import annotations

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    CriterionAssessment,
    CriterionDisposition,
    DeterministicPredicateResult,
)
from thesis_bench.records import content_sha256


def assessment(
    criterion_id: str,
    disposition: CriterionDisposition,
    source: AssessmentSource = AssessmentSource.DETERMINISTIC,
    *,
    judge_config_id: str | None = None,
    review_id: str | None = None,
    contract_id: str | None = None,
    contract_sha256: str | None = None,
) -> CriterionAssessment:
    predicate_ids = {
        "claim-a": "predicate-claim-a",
        "claim-b": "predicate-claim-b",
        "unsupported-a": "predicate-unsupported-a",
        "required-state": "predicate-state",
        "prohibited-action": "predicate-action",
        "semantic-point": "predicate-semantic-point",
    }
    predicate_id = (
        predicate_ids.get(criterion_id) if source == AssessmentSource.DETERMINISTIC else None
    )
    predicate_version = (
        "predicate-v1"
        if source == AssessmentSource.DETERMINISTIC and criterion_id in predicate_ids
        else None
    )
    contract_ids = {
        "claim-a": ("evaluator-contract-1", "c" * 64),
        "claim-b": ("evaluator-contract-1", "c" * 64),
        "unsupported-a": ("evaluator-contract-1", "c" * 64),
        "required-state": ("procedural-1", "c" * 64),
        "prohibited-action": ("procedural-1", "c" * 64),
        "semantic-point": ("mixed-1", "c" * 64),
    }
    result = None
    if source == AssessmentSource.DETERMINISTIC and predicate_id and predicate_version:
        resolved_contract_id, resolved_contract_sha256 = contract_ids[criterion_id]
        result_candidate = DeterministicPredicateResult.model_construct(
            schema_version=1,
            result_id=f"result-{criterion_id}-{disposition.value}",
            criterion_id=criterion_id,
            predicate_id=predicate_id,
            predicate_version=predicate_version,
            disposition=disposition,
            contract_id=contract_id or resolved_contract_id,
            contract_sha256=contract_sha256 or resolved_contract_sha256,
            observation_sha256=content_sha256({"observation": criterion_id, "value": disposition}),
            result_sha256="0" * 64,
        )
        result = result_candidate.model_copy(
            update={
                "result_sha256": content_sha256(
                    result_candidate.model_dump(mode="json", exclude={"result_sha256"})
                )
            }
        )
    return CriterionAssessment(
        schema_version=1,
        assessment_id=f"assessment-{criterion_id}-{disposition.value}",
        criterion_id=criterion_id,
        disposition=disposition,
        source=source,
        assessor_id="assessor-1",
        judge_config_id=judge_config_id,
        review_id=review_id,
        predicate_id=predicate_id,
        predicate_version=predicate_version,
        deterministic_result=result,
    )


def complete_knowledge_assessments(
    claim_a: CriterionDisposition = CriterionDisposition.SATISFIED,
    claim_b: CriterionDisposition = CriterionDisposition.SATISFIED,
    unsupported: CriterionDisposition = CriterionDisposition.NOT_SATISFIED,
) -> tuple[CriterionAssessment, ...]:
    return (
        assessment("claim-a", claim_a),
        assessment("claim-b", claim_b),
        assessment("unsupported-a", unsupported),
    )
