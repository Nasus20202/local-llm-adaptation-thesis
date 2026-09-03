from __future__ import annotations

from tests.cluster.fixtures import environment, policy
from thesis_bench.cluster import (
    ActionRequest,
    ActionResponse,
    ClusterExecutor,
    FakeCluster,
    FinalStateFixture,
    FinalStateValidator,
    compare_neutral_policies,
)
from thesis_bench.records import ReasonCode


def test_cumulative_output_budget_exhaustion_dominates_final_state_success() -> None:
    fake = FakeCluster(
        initial_state_hash="initial-1",
        validator_result="pre-task-ok",
        responses={
            "chunk": ActionResponse(
                schema_version=1,
                outcome="allowed",
                output="x" * 150,
            )
        },
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
        policy=policy(allowed_commands=("chunk",)),
        adapter=fake,
        validator=validator,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )
    attempt = executor.start_attempt("family-1", "variant-1")

    first = attempt.action(ActionRequest(schema_version=1, command="chunk", permission="read"))
    second = attempt.action(ActionRequest(schema_version=1, command="chunk", permission="read"))

    assert first.outcome == "allowed"
    assert second.reason_code == ReasonCode.BUDGET_EXHAUSTED
    assert attempt.terminal_reason == ReasonCode.BUDGET_EXHAUSTED
    assert attempt.terminal_outcome == "failure"
    assert attempt.final_state().outcome == "failure"
    assert attempt.final_state().reason_code == ReasonCode.BUDGET_EXHAUSTED


def test_retries_receive_new_append_only_attempt_ids(tmp_path) -> None:
    fake = FakeCluster(initial_state_hash="initial-1", validator_result="pre-task-ok")
    executor = ClusterExecutor(
        root=tmp_path,
        environment=environment(),
        policy=policy(),
        adapter=fake,
        validator=None,
        initial_state_hash="initial-1",
        initial_validator_result="pre-task-ok",
    )

    first = executor.start_attempt("family-1", "variant-1")
    second = executor.start_attempt("family-1", "variant-1")

    assert first.record.attempt_id != second.record.attempt_id
    assert sorted(path.name for path in tmp_path.iterdir()) == ["attempt-1", "attempt-2"]
    assert (tmp_path / "attempt-1" / "record.json").is_file()
    assert (tmp_path / "attempt-2" / "record.json").is_file()


def test_action_capture_directory_preserves_timestamps_arguments_and_resource(tmp_path) -> None:
    fake = FakeCluster(initial_state_hash="initial-1", validator_result="pre-task-ok")
    executor = ClusterExecutor(
        root=tmp_path,
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
            command="repair",
            permission="namespaced-write",
            observation="status",
            state_resource_id="resource-1",
        )
    )

    assert capture.started_at.endswith("Z")
    assert capture.ended_at.endswith("Z")
    assert '"command":"repair"' in capture.normalized_arguments
    assert capture.state_changing_resource_id == "resource-1"
    action_log = tmp_path / "attempt-1" / "actions.jsonl"
    assert action_log.is_file()
    assert action_log.read_text(encoding="utf-8").count("\n") == 1


def test_matched_neutral_policy_rejects_extra_permission_or_budget() -> None:
    assert compare_neutral_policies((policy(), policy(policy_id="neutral-policy-2"))).valid is True
    comparison = compare_neutral_policies((policy(), policy(max_output_bytes=201)))
    assert comparison.valid is False
    assert "output" in comparison.differences[0]
