from __future__ import annotations

import pytest

from tests.cluster.fixtures import environment, policy
from thesis_bench.cluster import (
    ActionRequest,
    ActionResponse,
    ClusterExecutor,
    FakeCluster,
    FinalStateFixture,
    FinalStateValidator,
)
from thesis_bench.records import ReasonCode


def test_attempt_final_state_comes_from_adapter_not_caller_supplied_boolean() -> None:
    fake = FakeCluster(
        initial_state_hash="initial-1",
        validator_result="pre-task-ok",
        final_state_satisfies=False,
    )
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

    assert attempt.final_state().outcome == "failure"


def test_reset_mismatch_blocks_actions_before_the_fake_adapter_runs() -> None:
    fake = FakeCluster(initial_state_hash="wrong", validator_result="pre-task-ok")
    executor = ClusterExecutor(
        root=None,
        environment=environment(),
        policy=policy(),
        adapter=fake,
        validator=None,
        initial_state_hash="expected",
        initial_validator_result="pre-task-ok",
    )

    attempt = executor.start_attempt("family-1", "variant-1")
    assert attempt.started is False
    assert attempt.reason_code == ReasonCode.INFRASTRUCTURE_FAILURE
    assert fake.actions == ()


def test_boundary_denials_and_budget_exhaustion_are_captured() -> None:
    fake = FakeCluster(initial_state_hash="initial-1", validator_result="pre-task-ok")
    executor = ClusterExecutor(
        root=None,
        environment=environment(),
        policy=policy(max_actions=1),
        adapter=fake,
        validator=None,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )
    attempt = executor.start_attempt("family-1", "variant-1")
    allowed = attempt.action(
        ActionRequest(schema_version=1, command="inspect", permission="read", output="ok")
    )
    denied = attempt.action(
        ActionRequest(schema_version=1, command="host-shell", permission="host", output="secret")
    )
    exhausted = attempt.action(
        ActionRequest(schema_version=1, command="inspect", permission="read", output="ok")
    )

    assert allowed.outcome == "allowed"
    assert denied.outcome == "denied"
    assert exhausted.outcome == "denied"
    assert len(attempt.captures) == 3
    assert denied.reason_code == ReasonCode.DENIED_OPERATION
    assert exhausted.reason_code == ReasonCode.BUDGET_EXHAUSTED
    with pytest.raises(ValueError, match="terminated"):
        attempt.action(
            ActionRequest(schema_version=1, command="inspect", permission="read", output="ok")
        )


def test_unsafe_request_is_captured_and_denied_at_the_adapter_boundary() -> None:
    fake = FakeCluster(initial_state_hash="initial-1", validator_result="pre-task-ok")
    executor = ClusterExecutor(
        root=None,
        environment=environment(),
        policy=policy(),
        adapter=fake,
        validator=None,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )
    attempt = executor.start_attempt("family-1", "variant-1")

    capture = attempt.action(
        ActionRequest(
            schema_version=1,
            command="inspect",
            permission="read",
            privileged=True,
            egress=True,
        )
    )

    assert capture.outcome == "denied"
    assert capture.reason_code == ReasonCode.SAFETY_FAILURE
    assert fake.actions == ()


def test_fake_timeout_and_overlarge_output_fail_closed_with_capture() -> None:
    fake = FakeCluster(
        initial_state_hash="initial-1",
        validator_result="pre-task-ok",
        responses={
            "slow": ActionResponse(
                schema_version=1,
                outcome="timeout",
                output="partial",
                duration_seconds=31.0,
            ),
            "large": ActionResponse(
                schema_version=1,
                outcome="allowed",
                output="x" * 201,
                duration_seconds=0.0,
            ),
        },
    )
    executor = ClusterExecutor(
        root=None,
        environment=environment(),
        policy=policy(allowed_commands=("inspect", "repair", "slow", "large")),
        adapter=fake,
        validator=None,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )
    attempt = executor.start_attempt("family-1", "variant-1")

    large = attempt.action(ActionRequest(schema_version=1, command="large", permission="read"))
    timeout_attempt = executor.start_attempt("family-1", "variant-2")
    timeout = timeout_attempt.action(
        ActionRequest(schema_version=1, command="slow", permission="read")
    )

    assert timeout.reason_code == ReasonCode.TIMEOUT
    assert large.reason_code == ReasonCode.BUDGET_EXHAUSTED
