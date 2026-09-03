from __future__ import annotations

import pytest

from tests.web.fixtures import provider
from thesis_bench.records import DecisionStatus, ReasonCode
from thesis_bench.web import (
    SearchResult,
    W1Attempt,
    W1Policy,
    provider_qualification_help,
    qualify_w1,
    source_drift_precheck,
)


def test_w1_budgets_allow_exact_boundaries_and_deny_the_next_operation() -> None:
    results = tuple(
        SearchResult(
            schema_version=1,
            result_id=f"result-{index}",
            url="https://kubernetes.io/docs/synthetic-page",
            title="synthetic",
        )
        for index in range(5)
    )
    fake = provider()
    fake.search_results = results
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"), provider=fake
    )

    for _ in range(3):
        assert len(attempt.search("synthetic query").results) == 5
    with pytest.raises(ValueError, match="budget"):
        attempt.search("synthetic query")
    assert attempt.records[-1].reason_code == ReasonCode.BUDGET_EXHAUSTED
    assert attempt.records[-1].captured is True


def test_source_drift_and_feasibility_are_explicit_progression_inputs() -> None:
    assert (
        source_drift_precheck(
            frozen_hash="a" * 64,
            current_hash="b" * 64,
            source_available=True,
            reviewer_id="reviewer-1",
            semantic_compatible=True,
            rationale="answer contract unchanged",
        ).status
        == DecisionStatus.GO
    )
    drift = source_drift_precheck(
        frozen_hash="a" * 64,
        current_hash="b" * 64,
        source_available=True,
        reviewer_id="reviewer-1",
        semantic_compatible=False,
        rationale="required constraint changed",
    )
    assert drift.status == DecisionStatus.STOP_DEFER
    assert drift.reason_code == ReasonCode.SOURCE_DRIFT

    report = qualify_w1(
        eligible_attempts=(True,) * 10,
        complete_provenance=(True,) * 10,
        deny_fixture_safe=(True,) * 10,
        redirects_safe=(True,) * 10,
        within_budget=(True,) * 9 + (False,),
    )
    assert report.status == DecisionStatus.GO
    assert report.completion_rate == 0.9

    unsafe = qualify_w1(
        eligible_attempts=(True,) * 10,
        complete_provenance=(True,) * 10,
        deny_fixture_safe=(False,) + (True,) * 9,
        redirects_safe=(True,) * 10,
        within_budget=(True,) * 10,
    )
    assert unsafe.status == DecisionStatus.STOP_DEFER


def test_source_drift_requires_human_semantic_compatibility_evidence() -> None:
    with pytest.raises(ValueError, match="review"):
        source_drift_precheck(
            frozen_hash="a" * 64,
            current_hash="a" * 64,
            source_available=True,
            reviewer_id="",
            semantic_compatible=True,
            rationale="",
        )


def test_w1_feasibility_counts_only_predeclared_eligible_attempts() -> None:
    report = qualify_w1(
        eligible_attempts=(True, False, True),
        complete_provenance=(True, False, True),
        deny_fixture_safe=(True, False, True),
        redirects_safe=(True, False, True),
        within_budget=(True, False, True),
    )

    assert report.completion_rate == 1.0
    assert report.status == DecisionStatus.GO


def test_provider_qualification_entry_point_does_not_contact_external_services() -> None:
    record = provider_qualification_help()
    assert record.status == "not_exposed"
