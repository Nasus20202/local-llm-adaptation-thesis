from __future__ import annotations

import pytest

from tests.cluster.fixtures import environment, policy
from thesis_bench.cluster import (
    ClusterExecutor,
    FakeCluster,
    FinalStateFixture,
    FinalStateValidator,
    qualify_cluster,
)
from thesis_bench.records import DecisionStatus, ReasonCode


def test_fake_cluster_reset_hash_and_final_validator_are_deterministic() -> None:
    fake = FakeCluster(initial_state_hash="initial-1", validator_result="pre-task-ok")
    validator = FinalStateValidator(
        schema_version=1,
        validator_id="validator-1",
        version="v1",
        fixtures=(
            FinalStateFixture(
                schema_version=1, fixture_id="positive", category="positive", expected=True
            ),
            FinalStateFixture(
                schema_version=1, fixture_id="negative", category="negative", expected=False
            ),
            FinalStateFixture(
                schema_version=1, fixture_id="boundary", category="boundary", expected=False
            ),
            FinalStateFixture(
                schema_version=1, fixture_id="malformed", category="malformed", expected=False
            ),
            FinalStateFixture(
                schema_version=1, fixture_id="ambiguous", category="ambiguous", expected=False
            ),
        ),
    )
    executor = ClusterExecutor(
        root=None,
        environment=environment(),
        policy=policy(),
        adapter=fake,
        validator=validator,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )

    attempt = executor.start_attempt("family-1", "variant-1")
    assert attempt.started is True
    assert attempt.reset.initial_state_hash == "initial-1"
    assert (
        validator.qualify(
            lambda fixture: validator.evaluate(
                state_satisfies=fixture.expected,
                prohibited_action=False,
            )
        )
        == DecisionStatus.GO
    )


def test_final_state_validator_evaluates_state_without_pydantic_collision() -> None:
    validator = FinalStateValidator(
        schema_version=1,
        validator_id="validator-1",
        version="v1",
        fixtures=tuple(
            FinalStateFixture(
                schema_version=1,
                fixture_id=category,
                category=category,
                expected=category == "positive",
            )
            for category in ("positive", "negative", "boundary", "malformed", "ambiguous")
        ),
    )

    result = validator.evaluate(state_satisfies=True, prohibited_action=False)

    assert result.outcome == "success"


def test_final_state_validator_rejects_nondeterministic_fixture_evaluator() -> None:
    validator = FinalStateValidator(
        schema_version=1,
        validator_id="validator-1",
        version="v1",
        fixtures=tuple(
            FinalStateFixture(
                schema_version=1,
                fixture_id=category,
                category=category,
                expected=category == "positive",
            )
            for category in ("positive", "negative", "boundary", "malformed", "ambiguous")
        ),
    )
    calls = 0

    def nondeterministic(fixture: FinalStateFixture):
        nonlocal calls
        calls += 1
        return validator.evaluate(state_satisfies=calls % 2 == 1)

    assert validator.qualify(nondeterministic) == DecisionStatus.AMEND


def test_final_state_qualification_runs_each_fixture_and_rejects_broken_validator() -> None:
    validator = FinalStateValidator(
        schema_version=1,
        validator_id="validator-1",
        version="v1",
        fixtures=tuple(
            FinalStateFixture(
                schema_version=1,
                fixture_id=category,
                category=category,
                expected=category == "positive",
            )
            for category in ("positive", "negative", "boundary", "malformed", "ambiguous")
        ),
    )

    broken = validator.qualify(
        lambda fixture: validator.evaluate(state_satisfies=True, prohibited_action=False)
    )
    correct = validator.qualify(
        lambda fixture: validator.evaluate(
            state_satisfies=fixture.expected,
            prohibited_action=False,
        )
    )

    assert broken == DecisionStatus.AMEND
    assert correct == DecisionStatus.GO


def test_environment_rejects_mutable_image_tags_and_qualification_requires_all_checks() -> None:
    with pytest.raises(ValueError):
        environment(node_image_digest="node:mutable")
    with pytest.raises(ValueError):
        environment(workload_image_digests=("workload:mutable",))
    with pytest.raises(ValueError):
        environment(workload_image_digests=("sha256:" + "g" * 64,))

    report = qualify_cluster(
        reset_hashes=("h" * 64,) * 10,
        reset_validator_results=("ok",) * 10,
        egress_denials=(True,) * 10,
        permission_checks=(True, True),
        validator_status=DecisionStatus.GO,
        matched_access=True,
        paired_variants=True,
        reset_durations_seconds=(10.0,) * 10,
        reset_validation_durations_seconds=(12.0,) * 10,
        attempt_durations_seconds=(30.0,) * 10,
    )
    assert report.status == DecisionStatus.GO
    assert report.reason_codes == (ReasonCode.OK,)

    missing_permissions = qualify_cluster(
        reset_hashes=("h" * 64,) * 10,
        reset_validator_results=("ok",) * 10,
        egress_denials=(True,) * 10,
        permission_checks=(),
        validator_status=DecisionStatus.GO,
        matched_access=True,
        paired_variants=True,
        reset_durations_seconds=(10.0,) * 10,
        reset_validation_durations_seconds=(12.0,) * 10,
        attempt_durations_seconds=(30.0,) * 10,
    )
    assert missing_permissions.status == DecisionStatus.STOP_DEFER
    assert ReasonCode.PERMISSION_FAILURE in missing_permissions.reason_codes

    overlong_attempt = qualify_cluster(
        reset_hashes=("h" * 64,) * 10,
        reset_validator_results=("ok",) * 10,
        egress_denials=(True,) * 10,
        permission_checks=(True,),
        validator_status=DecisionStatus.GO,
        matched_access=True,
        paired_variants=True,
        reset_durations_seconds=(10.0,) * 10,
        reset_validation_durations_seconds=(12.0,) * 10,
        attempt_durations_seconds=(301.0,) * 10,
    )
    assert overlong_attempt.status == DecisionStatus.AMEND
    assert overlong_attempt.max_attempt_seconds == 301.0
