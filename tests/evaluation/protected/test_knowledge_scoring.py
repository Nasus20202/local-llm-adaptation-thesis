from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    CriterionDisposition,
    score_knowledge,
)

from .fixtures import assessment, complete_knowledge_assessments, knowledge_contract


def test_knowledge_score_is_id_based_and_fail_closed_for_unresolved() -> None:
    contract = knowledge_contract()
    score = score_knowledge(contract, complete_knowledge_assessments())
    assert score.true_positives == 2
    assert score.false_negatives == 0
    assert score.false_positives == 0
    assert score.score == pytest.approx(1.0)

    repeated = (
        *complete_knowledge_assessments(),
        assessment("claim-a", CriterionDisposition.SATISFIED),
    )
    with pytest.raises(ValueError, match="duplicate"):
        score_knowledge(contract, repeated)
    with pytest.raises(ValueError, match="unresolved"):
        score_knowledge(
            contract,
            complete_knowledge_assessments(claim_a=CriterionDisposition.UNRESOLVED),
        )


def test_knowledge_false_positive_requires_contract_declared_unsupported_criterion() -> None:
    score = score_knowledge(
        knowledge_contract(),
        complete_knowledge_assessments(unsupported=CriterionDisposition.SATISFIED),
    )
    assert score.false_positives == 1
    assert score.score == pytest.approx(4 / 5)


def test_unqualified_semantic_assessments_cannot_enter_the_score_kernel() -> None:
    raw_judge_assessments = tuple(
        assessment(
            item.criterion_id,
            item.disposition,
            AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
            judge_config_id="unqualified-judge",
        )
        for item in complete_knowledge_assessments()
    )
    with pytest.raises(ValueError, match="qualified"):
        score_knowledge(knowledge_contract(), raw_judge_assessments)
